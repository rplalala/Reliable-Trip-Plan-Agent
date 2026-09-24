"""Pure V3 checks over an existing snapshot. No acquisition, model or repair calls."""

from collections import defaultdict
from itertools import combinations
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from backend.app.evidence.effective_models import EffectivePlaceEvidence
from backend.app.evidence.models import PlaceEvidence, RouteEvidenceBundle
from backend.app.policies.generation_diagnostics import observe_generation
from backend.app.policies.itinerary_output import validate_output_sources
from backend.app.policies.poi_funnel import NamedPlaceResolution
from backend.app.policies.trip_dates import TripDateWindow, validate_itinerary_dates
from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements
from backend.app.schemas.itinerary import Itinerary
from backend.app.versions.v3.models import (
    Finding,
    ImprovementTarget,
    PlaceUseObservation,
    ValidationPolicy,
    ValidationReport,
)


def validate_draft(
    itinerary: Itinerary,
    contract: InterpretedTripRequirements,
    *,
    window: TripDateWindow,
    supplied_ids: tuple[str, ...],
    places: tuple[PlaceEvidence, ...],
    named_resolutions: tuple[NamedPlaceResolution, ...] = (),
    effective_places: tuple[EffectivePlaceEvidence, ...] = (),
    routes: RouteEvidenceBundle | None = None,
    policy: ValidationPolicy | None = None,
    route_evidence: tuple = (),
    transitions: tuple = (),
    original_supply_ids: tuple[str, ...] | None = None,
    schedule=None,
    visit_bindings=(),
) -> ValidationReport:
    """Validate already accepted application inputs, without changing even array order.

    Shared schema/source/date errors still raise at the shared boundary. Nearby is
    ignored, never promoted to primary supply. Effective facts must be outputs of the
    existing official evidence resolver, not model-authored or TripWorld priors.
    """
    policy = policy or ValidationPolicy()
    # Reuse shared checks on a detached primary-only copy; discard normalization.
    primary = itinerary.model_copy(deep=True, update={"reference_recommendations": []})
    validate_output_sources(primary, places=places, supplied_ids=supplied_ids)
    validate_itinerary_dates(contract.requirements, primary, window)
    by_id = {p.place_id: p for p in places}
    effective = {p.place_id: p for p in effective_places}
    if len(by_id) != len(places) or len(effective) != len(effective_places):
        raise ValueError("Duplicate evidence identity")
    if not set(effective) <= set(by_id):
        raise ValueError("Effective evidence must belong to supplied Details snapshot")
    diagnostics = observe_generation(
        itinerary,
        contract.requirements,
        reference_date=window.reference_date,
        supplied_ids=supplied_ids,
        related_requirement_ids=tuple(r.requirement_id for r in contract.semantic_requirements),
    )
    if original_supply_ids is not None:
        scheduled = {
            a.source_place_id
            for d in itinerary.days
            for a in d.activities
            if a.activity_kind == "main_poi" and a.source_place_id
        }
        original_ids = set(original_supply_ids)
        diagnostics = diagnostics.model_copy(
            update={
                "unused_supply": len(original_ids - scheduled),
                "scheduled_unique_supply": len(original_ids & scheduled),
            }
        )
    findings = []

    def add(check, status, reason, **kwargs):
        findings.append(
            Finding(
                finding_id=f"finding_{len(findings) + 1}",
                check=check,
                status=status,
                reason=reason,
                is_violation=status == "CONFIRMED",
                **kwargs,
            )
        )

    for row in diagnostics.days:
        count = row.distinct_main_poi_count
        if (
            row.target_status == "not_assessable"
            or count < policy.daily_main_min
            or count > policy.daily_main_max
        ):
            add(
                "overfull"
                if count > policy.daily_main_max and row.target_status != "not_assessable"
                else "coverage",
                "UNKNOWN" if row.target_status == "not_assessable" else "NEEDS_REVIEW",
                "default_target_observation_without_executable_exception_contract",
                dates=(row.date,),
                evidence_refs=(f"generation_diagnostics:{row.date}",),
            )

    if schedule is not None:
        for day in itinerary.days:
            if str(day.date) in schedule.unresolved_dates:
                add(
                    "semantic_requirements",
                    "UNKNOWN",
                    "scoped_time_protection_unresolved",
                    dates=(day.date,),
                )
            for a in day.activities:
                if a.activity_kind == "free_time":
                    continue  # Rest placeholders may cover fixed rest; visits may not.
                for fixed in schedule.fixed:
                    if a.start_time.utcoffset() is None:
                        continue  # Existing overlap checks preserve timezone uncertainty.
                    overlap = (
                        min(a.end_time, fixed.end) - max(a.start_time, fixed.start)
                    ).total_seconds()
                    if overlap > 0:
                        add(
                            "semantic_requirements",
                            "CONFIRMED" if a.activity_kind == "main_poi" else "UNKNOWN",
                            "fixed_user_time_overlap"
                            if a.activity_kind == "main_poi"
                            else "activity_time_protection_relationship_unbound",
                            dates=(day.date,),
                            activity_ids=(a.activity_id,),
                            requirement_ids=(fixed.root_activity_id,),
                            magnitude=overlap,
                            evidence_refs=(fixed.source,),
                        )

    activities = [a for day in itinerary.days for a in day.activities]
    scheduled = {a.source_place_id for a in activities if a.source_place_id}
    visits = defaultdict(list)
    for a in activities:
        if a.activity_kind == "main_poi" and a.source_place_id:
            visits[a.source_place_id].append(a)
    for pid, items in visits.items():
        if len(items) > 1:
            add(
                "repetition",
                "NEEDS_REVIEW",
                "repeated_identity_not_proof_of_redundancy",
                place_ids=(pid,),
                activity_ids=tuple(a.activity_id for a in items),
                dates=tuple(sorted({a.start_time.date() for a in items})),
            )

    # Compare every pair, including nested and cross-day intervals. Mixed awareness
    # cannot be compared safely; wall-clock or prose assumptions are not introduced.
    for left, right in combinations(activities, 2):
        fields = dict(
            activity_ids=(left.activity_id, right.activity_id),
            dates=tuple(sorted({left.start_time.date(), right.start_time.date()})),
        )
        if (left.start_time.utcoffset() is None) != (right.start_time.utcoffset() is None):
            add("overlap", "UNKNOWN", "mixed_timezone_awareness", **fields)
        elif max(left.start_time, right.start_time) < min(left.end_time, right.end_time):
            add(
                "overlap",
                "CONFIRMED",
                "scheduled_intervals_overlap",
                evidence_refs=(
                    f"draft:activity:{left.activity_id}",
                    f"draft:activity:{right.activity_id}",
                ),
                **fields,
            )

    bindings = defaultdict(list)
    for resolution in named_resolutions:
        bindings[resolution.search_intent_id].append(resolution)
    known_requirements = {r.requirement_id for r in contract.named_places}
    if not set(bindings) <= known_requirements:
        raise ValueError("Named resolution has no canonical requirement provenance")
    for requirement in contract.named_places:
        if requirement.inclusion == "OPTIONAL" and not any(
            v.requirement_id == requirement.requirement_id
            for v in contract.visit_requirements or ()
        ):
            continue
        matches = bindings.get(requirement.requirement_id, [])
        resolution = matches[0] if len(matches) == 1 else None
        valid = (
            resolution is not None
            and resolution.status == "resolved"
            and resolution.resolved_place_id is not None
            and resolution.matching_place_ids == (resolution.resolved_place_id,)
            and resolution.named_place_intent.place_text == requirement.place_text
            and resolution.named_place_intent.source_text
            in {source.quote for source in requirement.source_refs}
        )
        if not valid:
            add(
                "named_requirement",
                "UNKNOWN",
                "missing_or_inconsistent_identity_binding",
                requirement_ids=(requirement.requirement_id,),
            )
            continue
        pid = resolution.resolved_place_id
        present = pid in scheduled
        conflict = (requirement.inclusion == "REQUIRED" and not present) or (
            requirement.inclusion == "EXCLUDED" and present
        )
        visit_specs = [
            v
            for v in contract.visit_requirements or ()
            if v.requirement_id == requirement.requirement_id
        ]
        executable = [v for v in visit_specs if v.status == "executable"]
        actual = [
            a for a in activities if a.activity_kind == "main_poi" and a.source_place_id == pid
        ]
        obligation_unmet = any(
            len(actual) < v.minimum_visits
            or not set(v.dates) <= {a.start_time.date() for a in actual}
            for v in executable
        )
        from backend.app.versions.v3.repair_obligations import visit_binding

        mode_unverified = False
        for spec in executable:
            if not spec.access_mode:
                continue
            applicable = [
                a
                for a in actual
                if (binding := visit_binding(a, visit_bindings))
                and binding.mode == spec.access_mode
            ]
            if len(applicable) < spec.minimum_visits or not set(spec.dates) <= {
                a.start_time.date() for a in applicable
            }:
                mode_unverified = True
        conflict = conflict or obligation_unmet
        add(
            "named_requirement",
            "CONFIRMED"
            if conflict
            else "UNKNOWN"
            if mode_unverified or any(v.status == "unresolved" for v in visit_specs)
            else "PASS",
            "visit_requirement_unresolved"
            if not conflict
            and (mode_unverified or any(v.status == "unresolved" for v in visit_specs))
            else "required_visit_obligation_unmet"
            if obligation_unmet
            else "required_identity_omitted"
            if conflict and not present
            else "excluded_identity_scheduled"
            if conflict
            else "identity_inclusion_only",
            requirement_ids=(requirement.requirement_id,),
            place_ids=(pid,),
            evidence_refs=(
                f"requirements:{requirement.requirement_id}",
                f"named_resolution:{requirement.requirement_id}",
            ),
        )

    for activity in activities:
        if not activity.source_place_id or activity.activity_kind in {"transport", "free_time"}:
            continue
        place = by_id[activity.source_place_id]
        evidence = effective.get(place.place_id)
        from backend.app.versions.v3.repair_obligations import visit_binding

        binding = visit_binding(activity, visit_bindings)
        status, reason, refs = _opening(activity, place, evidence, binding)
        fields = dict(
            activity_ids=(activity.activity_id,),
            place_ids=(place.place_id,),
            dates=(activity.start_time.date(),),
        )
        add(
            "opening",
            status,
            reason,
            evidence_refs=refs,
            magnitude=_opening_magnitude(activity, place, evidence)
            if status in {"CONFIRMED", "PASS"}
            else None,
            **fields,
        )
        add(
            "visitor_suitability",
            "UNKNOWN",
            "public_access_and_visit_mode_not_typed",
            evidence_refs=(place.source_ref,),
            **fields,
        )

    # Current Activity has no per-leg travel mode or departure applicability binding.
    # Even direct provider observations cannot certify the planned transition.
    route_refs = (
        ()
        if routes is None
        else tuple(r.source_ref for r in (routes.baseline, *routes.alternatives))
    )
    if transitions:
        from backend.app.versions.v3.repair_routes import check_transitions

        available_routes = (
            *route_evidence,
            *((routes.baseline, *routes.alternatives) if routes else ()),
        )
        for assessment in check_transitions(itinerary, transitions, available_routes, schedule):
            add("route", **assessment)
    else:
        add(
            "route",
            "UNKNOWN",
            "per_leg_mode_and_departure_binding_not_supported",
            evidence_refs=route_refs,
        )
    add("budget", "UNKNOWN", "verified_party_currency_cost_coverage_not_supported")
    if contract.semantic_requirements:
        add(
            "semantic_requirements",
            "UNKNOWN",
            "open_semantics_not_executable_predicates",
            requirement_ids=tuple(r.requirement_id for r in contract.semantic_requirements),
        )
    targets = tuple(
        ImprovementTarget(
            finding_id=f.finding_id,
            basis="confirmed_conflict" if f.status == "CONFIRMED" else "review_policy",
        )
        for f in findings
        if f.status == "CONFIRMED"
        or (f.status == "NEEDS_REVIEW" and f.check in policy.review_targets)
    )
    return ValidationReport(
        diagnostics=diagnostics,
        findings=tuple(findings),
        place_use_observations=tuple(
            PlaceUseObservation(
                place_id=pid, primary_type=by_id[pid].primary_type, source_ref=by_id[pid].source_ref
            )
            for pid in sorted(scheduled)
        ),
        improvement_targets=targets,
    )


def _opening(activity, place, evidence, binding=None):
    """Find date-specific window differences without inventing visit/access scope.

    Only an explicit application binding distinguishes entry from exterior viewing.
    Unbound activity mismatches remain reviewable; intent never proves public access.
    """
    unknown = ("UNKNOWN", "applicable_structured_hours_unavailable", ())
    if (
        evidence is None
        or evidence.place_id != place.place_id
        or place.availability == "unavailable"
    ):
        return unknown
    if not place.timezone_id or activity.start_time.utcoffset() is None:
        return "UNKNOWN", "venue_timezone_or_activity_offset_missing", ()
    try:
        zone = ZoneInfo(place.timezone_id)
    except ZoneInfoNotFoundError:
        return "UNKNOWN", "venue_timezone_unrecognized", ()
    start, end = activity.start_time.astimezone(zone), activity.end_time.astimezone(zone)
    if start.date() != end.date():
        return "UNKNOWN", "overnight_hours_not_supported", ()
    day = next((d for d in evidence.operational_days if d.date == start.date()), None)
    if day and (day.status == "unresolved_conflict" or day.unresolved_reason):
        return "UNKNOWN", "conflicting_operational_evidence", day.source_refs
    bound = binding is not None and binding.mode == "venue_entry"
    if binding is not None and binding.mode == "exterior":
        return "UNKNOWN", "exterior_access_not_established_by_venue_hours", ()
    closure_facts = [
        f
        for f in evidence.facts
        if f.dimension == "operational_availability"
        and f.subject_scope == "whole_venue"
        and f.temporal_basis == "explicit_date_or_range"
        and f.applicable_start_date
        and f.applicable_end_date
        and f.applicable_start_date <= start.date() <= f.applicable_end_date
    ]
    if any(f.relation in {"conflict", "unresolved"} or f.unresolved_reason for f in closure_facts):
        return (
            "UNKNOWN",
            "conflicting_operational_evidence",
            tuple(r for f in closure_facts for r in f.source_refs),
        )
    if day and day.status == "confirmed_date_closed" and day.source_refs:
        if bound and any(
            f.source_refs
            and f.authority_bases
            and f.value_kind in {"temporary_closure", "permanent_closure"}
            and set(f.source_refs) & set(day.source_refs)
            for f in closure_facts
        ):
            return "CONFIRMED", "bound_entry_date_closed", day.source_refs
        return (
            ("UNKNOWN", "closure_provenance_or_scope_insufficient", day.source_refs)
            if bound
            else ("NEEDS_REVIEW", "venue_closed_but_visit_mode_unbound", day.source_refs)
        )
    facts = [
        f
        for f in evidence.facts
        if f.dimension == "opening_hours"
        and f.subject_scope == "whole_venue"
        and f.temporal_basis == "explicit_date_or_range"
        and f.applicable_start_date
        and f.applicable_end_date
        and f.applicable_start_date <= start.date() <= f.applicable_end_date
    ]
    if any(f.relation in {"conflict", "unresolved"} or f.unresolved_reason for f in facts):
        return (
            "UNKNOWN",
            "conflicting_hours_evidence",
            tuple(sorted({ref for f in facts for ref in f.source_refs})),
        )
    usable = _usable_hours(facts)
    if not usable or len({(f.opens_at, f.closes_at) for f in usable}) != 1:
        return unknown
    fact = usable[0]
    if start.time() < fact.opens_at or end.time() > fact.closes_at:
        return (
            ("CONFIRMED", "bound_entry_outside_hours", fact.source_refs)
            if bound
            else ("NEEDS_REVIEW", "outside_venue_hours_but_visit_mode_unbound", fact.source_refs)
        )
    # Matching hours do not establish admission or the absence of special restrictions.
    return (
        ("PASS", "bound_entry_hours_only", fact.source_refs)
        if bound
        else ("UNKNOWN", "within_hours_but_visit_access_unverified", fact.source_refs)
    )


def _opening_magnitude(activity, place, evidence):
    """Seconds outside the supported explicit daily window; closed day loses the visit."""
    start, end = (
        activity.start_time.astimezone(ZoneInfo(place.timezone_id)),
        activity.end_time.astimezone(ZoneInfo(place.timezone_id)),
    )
    if any(
        d.date == start.date() and d.status == "confirmed_date_closed"
        for d in evidence.operational_days
    ):
        return (end - start).total_seconds()
    facts = _usable_hours(
        [
            f
            for f in evidence.facts
            if f.dimension == "opening_hours"
            and f.subject_scope == "whole_venue"
            and f.temporal_basis == "explicit_date_or_range"
            and f.applicable_start_date
            and f.applicable_end_date
            and f.applicable_start_date <= start.date() <= f.applicable_end_date
        ]
    )
    f = facts[0]
    opens = start.replace(
        hour=f.opens_at.hour, minute=f.opens_at.minute, second=f.opens_at.second, microsecond=0
    )
    closes = start.replace(
        hour=f.closes_at.hour, minute=f.closes_at.minute, second=f.closes_at.second, microsecond=0
    )
    return max(
        0,
        (end - start).total_seconds()
        - max(0, (min(end, closes) - max(start, opens)).total_seconds()),
    )


def _usable_hours(facts):
    return [
        f
        for f in facts
        if f.source_refs
        and f.authority_bases
        and f.opens_at is not None
        and f.closes_at is not None
        and f.opens_at.tzinfo is None
        and f.closes_at.tzinfo is None
        and f.opens_at < f.closes_at
        and f.schedule_scope == "daily"
    ]
