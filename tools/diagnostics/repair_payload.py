"""Actual Repair serializer sizing over bounded synthetic fixtures; no clients or services."""

import json
from datetime import date, datetime, timedelta

from backend.app.evidence.models import PlaceEvidence
from backend.app.policies.trip_dates import create_trip_date_window
from backend.app.runtime.token_counting import count_tokens
from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements
from backend.app.schemas.itinerary import Activity, Itinerary, ItineraryDay
from backend.app.schemas.request import PlanningRequest
from backend.app.versions.v3.repair_acceptance import assess
from backend.app.versions.v3.repair_models import (
    CandidateDecision,
    CandidatePreparation,
    RepairCandidate,
    RepairScope,
    ValidationContext,
)
from backend.app.versions.v3.repair_projection import FoundryRepairPatchDTO, build_repair_input


def enriched_fixture():
    """Long interpreted requirements and conflicting accepted date-specific evidence."""
    from datetime import time

    from backend.app.evidence.official_models import OfficialCurrentEvidence
    from backend.app.policies.official_evidence_resolver import resolve_effective_evidence

    itinerary, _, scope, context, whitelist = fixture(10, 28)
    data = context.contract.model_dump()
    data["interpretation_origin"] = "model"
    sentence = "Prefer museums with architectural exhibits and varied experiences."
    data["semantic_requirements"] = [
        dict(
            requirement_id=f"semantic_{i + 1}",
            normalized_text=(sentence * 4)[:248],
            kind="preference",
            polarity="favor",
            strength="medium",
            scope="selected_poi_set",
            subject_refs=("party",),
            source_refs=({"quote": sentence, "start": 0, "end": len(sentence), "occurrence": 0},),
        )
        for i in range(24)
    ]
    effective = []
    for p in context.places:
        facts = tuple(
            OfficialCurrentEvidence(
                place_id=p.place_id,
                place_name=p.name,
                information_need="special_date_hours",
                claim_kind="special_hours",
                value_text=f"Synthetic daily hours closing at {hour}:00.",
                source_kind="fetched_html",
                source_url="https://venue.example/hours",
                supporting_excerpt="Synthetic hours notice",
                subject_scope="whole_venue",
                temporal_basis="explicit_date_or_range",
                applicable_start_date=itinerary.start_date,
                applicable_end_date=itinerary.end_date,
                schedule_scope="daily",
                opens_at=time(9),
                closes_at=time(hour),
                authority_basis="places_first_party_website",
                retrieved_at=p.retrieved_at,
                source_ref=f"fixture:{p.place_id}:{hour}",
            )
            for hour in (16, 17)
        )
        effective.append(
            resolve_effective_evidence(
                p, facts, trip_start=itinerary.start_date, trip_end=itinerary.end_date
            )
        )
    context = context.model_copy(
        update={
            "contract": InterpretedTripRequirements.model_validate(data),
            "effective_places": tuple(effective),
        }
    )
    report = assess(itinerary, context)
    scope = scope.model_copy(
        update={"target_ids": tuple(f.finding_id for f in report.findings if f.check == "overlap")}
    )
    return itinerary, report, scope, context, whitelist


def fixture(days, candidates, stress=False):
    start = date(2026, 9, 26)
    end = start + timedelta(days=days - 1)
    request = PlanningRequest(
        destination="Synthetic city",
        start_date=start,
        end_date=end,
        traveler_count=2,
        budget={"amount": 2000, "currency": "GBP"},
    )
    contract = InterpretedTripRequirements(
        request_sha256="synthetic",
        structured_input_sha256=request.structured_hash(),
        interpretation_origin="skipped_empty",
        requirements=request.trip_requirements(),
        named_places=(),
        requested_place_information=(),
        transport_preference=None,
        semantic_requirements=(),
        subjects=(),
        discovery_intents=(),
        experience_evidence_requests=(),
        extraction_issues=(),
    )
    name = "Synthetic museum"
    if stress:
        # Deliberately adversarial but field-valid text, below the 12k candidate-object bound.
        name = " ".join(f"venue{i:05x}" for i in range(650))
    places = tuple(
        PlaceEvidence(
            place_id=f"place_{i}",
            name=name,
            latitude=0,
            longitude=0,
            timezone_id="UTC",
            business_status="OPERATIONAL",
            availability="available",
            retrieved_at=datetime.fromisoformat("2026-09-25T12:00:00+00:00"),
            source_ref=f"fixture:{i}",
        )
        for i in range(candidates)
    )
    itinerary = Itinerary(
        output_version="itinerary_2",
        destination=request.destination,
        start_date=start,
        end_date=end,
        days=[
            ItineraryDay(
                date=start + timedelta(days=d),
                activities=[
                    Activity(
                        activity_id=f"activity_{d}_{j}",
                        activity_kind="main_poi",
                        title="Fixture visit",
                        place_name=places[d * 2 + j].name,
                        source_place_id=places[d * 2 + j].place_id,
                        start_time=(
                            f"{start + timedelta(days=d)}T10:{'00' if j == 0 else '30'}:00+00:00"
                        ),
                        end_time=(
                            f"{start + timedelta(days=d)}T11:{'00' if j == 0 else '30'}:00+00:00"
                        ),
                    )
                    for j in range(2)
                ],
            )
            for d in range(days)
        ],
    )
    context = ValidationContext(
        contract=contract,
        window=create_trip_date_window(start - timedelta(days=1)),
        original_supply_ids=tuple(p.place_id for p in places[:20]),
        places=places,
    )
    report = assess(itinerary, context)
    scope = RepairScope(
        dates=tuple(d.date for d in itinerary.days),
        permissions=tuple(
            {"activity_id": a.activity_id, "operations": ("retime",)}
            for d in itinerary.days
            for a in d.activities
        ),
        target_ids=tuple(f.finding_id for f in report.findings if f.check == "overlap"),
    )
    whitelist = tuple(
        RepairCandidate(
            place=p,
            origin="original_supply" if i < 20 else "comparison_pool",
            provenance=(p.source_ref,),
        )
        for i, p in enumerate(places)
    )
    scheduled = {a.source_place_id for d in itinerary.days for a in d.activities}
    # Explicit replacement permissions keep candidate-rich stress inputs representative.
    scope = scope.model_copy(
        update={
            "permissions": tuple(
                p.model_copy(update={"operations": frozenset({"retime", "replace"})})
                for p in scope.permissions
            )
        }
    )
    preparation = CandidatePreparation(
        ledger=whitelist,
        input_candidates=whitelist,
        scheduled_ids=tuple(sorted(scheduled)),
        authorizations=tuple(
            CandidateDecision(
                place_id=c.place.place_id,
                target_id=scope.target_ids[0],
                date=scope.dates[0],
                operation="replace",
                disposition="selected",
                reason="sizing_fixture",
                evidence_refs=c.provenance,
            )
            for c in whitelist
        ),
    )
    return itinerary, report, scope, context, preparation


def addition_fixture(days=1, candidates=28):
    from backend.app.versions.v3.models import ValidationPolicy

    original, _, _, context, preparation = fixture(days, candidates)
    for day in original.days:
        day.activities = day.activities[:1]
    context = context.model_copy(update={"policy": ValidationPolicy(review_targets={"coverage"})})
    report = assess(original, context)
    scope = RepairScope(
        dates=tuple(d.date for d in original.days),
        permissions=(),
        add_dates=tuple(d.date for d in original.days),
        target_ids=tuple(f.finding_id for f in report.findings if f.check == "coverage"),
    )
    scheduled = {a.source_place_id for d in original.days for a in d.activities}
    candidates = tuple(c for c in preparation.ledger if c.place.place_id not in scheduled)
    auth = tuple(
        CandidateDecision(
            place_id=c.place.place_id,
            target_id=f.finding_id,
            date=f.dates[0],
            operation="add",
            disposition="selected",
            reason="sizing_fixture",
            evidence_refs=c.provenance,
            unknowns=("target_date_hours_missing",),
        )
        for c in candidates
        for f in report.findings
        if f.check == "coverage"
    )
    preparation = preparation.model_copy(
        update={
            "input_candidates": candidates,
            "scheduled_ids": tuple(sorted(scheduled)),
            "authorizations": auth,
        }
    )
    return original, report, scope, context, preparation


def retime_fixture():
    original, report, scope, context, prep = fixture(1, 3)
    scope = scope.model_copy(
        update={
            "permissions": tuple(
                p.model_copy(update={"operations": frozenset({"retime"})})
                for p in scope.permissions
            )
        }
    )
    prep = prep.model_copy(update={"input_candidates": (), "authorizations": ()})
    return original, report, scope, context, prep


def time_window_fixture(*, later=False, long=False):
    """New synthetic A context; never evidence attributed to historical live runs."""
    from backend.app.schemas.interpreted_requirements import TimeProtection
    from backend.app.versions.v3.repair_acceptance import apply_patch
    from backend.app.versions.v3.repair_budget import configured_policy
    from backend.app.versions.v3.repair_models import RepairPatch
    from backend.app.versions.v3.repair_schedule import (
        build_schedule,
        consume_windows,
        window_projection,
    )

    original, _, scope, context, prep = addition_fixture(3 if long else 1)
    protection = TimeProtection(
        dates=(),
        start_time="12:00",
        end_time="13:00",
        status="fixed",
        reason=None,
        source_refs=({"quote": "Private time", "occurrence": 0, "start": 0, "end": 12},),
    )
    contract = context.contract.model_copy(update={"time_protections": (protection,)})
    for day in original.days:
        day.activities.append(
            Activity(
                activity_id=f"free_{day.date}",
                activity_kind="free_time",
                title="Generated free afternoon",
                start_time=f"{day.date}T11:00:00+00:00",
                end_time=f"{day.date}T18:00:00+00:00",
            )
        )
    state = build_schedule(original, contract, context.places, primary_generated=True)
    context = context.model_copy(update={"schedule": state, "contract": contract})
    scope = scope.model_copy(
        update={"window_roots": tuple(w.root_activity_id for w in state.windows)}
    )
    if later:
        patch = RepairPatch(
            edits=(
                {
                    "operation": "add",
                    "activity_id": None,
                    "date": original.start_date,
                    "place_id": "place_1",
                    "start_time": f"{original.start_date}T14:00:00+00:00",
                    "end_time": f"{original.start_date}T15:00:00+00:00",
                },
            )
        )
        proposal, _ = apply_patch(original, patch, scope, prep)
        original, state, _ = consume_windows(
            original,
            proposal,
            scope,
            state,
            context.places,
            (),
            configured_policy().spatial,
            prefix="sizing_r1",
        )
        context = context.model_copy(update={"schedule": state})
        prep = prep.model_copy(
            update={
                "input_candidates": tuple(
                    c for c in prep.input_candidates if c.place.place_id != "place_1"
                ),
                "scheduled_ids": tuple(
                    sorted(
                        {
                            a.source_place_id
                            for d in original.days
                            for a in d.activities
                            if a.source_place_id
                        }
                    )
                ),
                "authorizations": tuple(a for a in prep.authorizations if a.place_id != "place_1"),
            }
        )
    if long:
        long_contract = enriched_fixture()[3].contract
        context = context.model_copy(
            update={
                "contract": context.contract.model_copy(
                    update={"semantic_requirements": long_contract.semantic_requirements}
                )
            }
        )
    prep = prep.model_copy(
        update={"elastic_windows": tuple(window_projection(original, state, scope.window_roots))}
    )
    return original, assess(original, context), scope, context, prep


def b_fixture(kind):
    """Synthetic B contracts; real scope, candidate preparation and serializer."""
    import asyncio
    from time import monotonic

    from backend.app.versions.v3.models import ValidationPolicy
    from backend.app.versions.v3.repair_budget import RepairBudget, configured_policy
    from backend.app.versions.v3.repair_candidates import prepare_candidates
    from backend.app.versions.v3.repair_schedule import build_schedule
    from backend.app.versions.v3.repair_targets import prepare_blank_windows
    from backend.app.versions.v3.wiring import operation_scope

    original, _, _, context, prep = fixture(3 if kind == "feedback" else 2, 28)
    for day in original.days:
        day.activities[1].start_time += timedelta(hours=2)
        day.activities[1].end_time += timedelta(hours=2)
    if kind == "missing":
        original.days = original.days[:1]
    elif kind == "move":
        first = original.days[0].activities[0]
        original.days[0].activities = [
            first.model_copy(
                update={
                    "activity_id": f"crowded_{i}",
                    "source_place_id": f"place_{i + 4}",
                    "start_time": first.start_time + timedelta(hours=i),
                    "end_time": first.start_time + timedelta(hours=i, minutes=30),
                }
            )
            for i in range(6)
        ]
    else:
        original.days[1].activities[0].source_place_id = (
            original.days[0].activities[0].source_place_id
        )
    policy = configured_policy()
    context = context.model_copy(
        update={
            "contract": context.contract.model_copy(
                update={"time_protections": (), "visit_requirements": ()}
            ),
            "identity_ledger": prep.ledger,
            "policy": ValidationPolicy(review_targets={"coverage", "repetition", "overfull"}),
        }
    )
    context = context.model_copy(
        update={
            "schedule": build_schedule(
                original, context.contract, context.places, primary_generated=True
            )
        }
    )
    context = context.model_copy(
        update={"schedule": prepare_blank_windows(original, context, policy)}
    )
    report = assess(original, context)
    scope = operation_scope(original, report, context=context, policy=policy, mode="WALK")
    if kind == "feedback":
        from backend.app.versions.v3.repair_targets import related_progress

        adopted = original.model_copy(deep=True)
        adopted.days[1].activities[0].source_place_id = "place_10"
        children = related_progress(original, adopted, scope, context.schedule)
        context = context.model_copy(update={"active_related": children})
        original = adopted
        report = assess(original, context)
        scope = scope.model_copy(
            update={
                "active_related": children,
                "target_ids": tuple(
                    f.finding_id for f in report.findings if f.check == "repetition"
                ),
            }
        )
    prep = asyncio.run(
        prepare_candidates(
            context, scope, RepairBudget(monotonic() + 600, policy=policy), original=original
        )
    )
    return original, report, scope, context, prep


def c_fixture(kind):
    """Existing resolver plus explicit application intent; no external acquisition."""
    import asyncio
    from datetime import time
    from time import monotonic

    from backend.app.evidence.models import RouteEvidence
    from backend.app.evidence.official_models import OfficialCurrentEvidence
    from backend.app.policies.official_evidence_resolver import resolve_effective_evidence
    from backend.app.versions.v3.models import ValidationPolicy
    from backend.app.versions.v3.repair_budget import RepairBudget, configured_policy
    from backend.app.versions.v3.repair_candidates import prepare_candidates
    from backend.app.versions.v3.repair_models import VisitBinding
    from backend.app.versions.v3.repair_routes import bind_transitions
    from backend.app.versions.v3.repair_schedule import build_schedule
    from backend.app.versions.v3.repair_targets import prepare_blank_windows
    from backend.app.versions.v3.wiring import operation_scope

    original, _, _, context, prep = fixture(2, 28)
    a, b = original.days[0].activities
    a.start_time = a.start_time.replace(hour=17)
    a.end_time = a.end_time.replace(hour=18)
    b.start_time = b.start_time.replace(hour=19, minute=0)
    b.end_time = b.end_time.replace(hour=20, minute=0)
    original.days[1].activities = []
    p = context.places[0]
    official = OfficialCurrentEvidence(
        place_id=p.place_id,
        place_name=p.name,
        information_need="special_date_hours",
        claim_kind="special_hours",
        value_text="Synthetic dated 09:00-17:00",
        source_kind="fetched_html",
        source_url="https://venue.example/hours",
        supporting_excerpt="Synthetic fixture",
        subject_scope="whole_venue",
        temporal_basis="explicit_date_or_range",
        applicable_start_date=original.start_date,
        applicable_end_date=original.end_date,
        schedule_scope="daily",
        opens_at=time(9),
        closes_at=time(17),
        authority_basis="places_first_party_website",
        retrieved_at=p.retrieved_at,
        source_ref="fixture:official",
    )
    evidence = resolve_effective_evidence(
        p, (official,), trip_start=original.start_date, trip_end=original.end_date
    )
    mode = "WALK"
    routes = ()
    bindings = (
        VisitBinding(
            activity_id=a.activity_id,
            place_id=p.place_id,
            mode="venue_entry",
            source_refs=("application:synthetic_intent",),
        ),
    )
    if kind == "route":
        mode = "TRANSIT"
        bindings = ()
        b.start_time = a.end_time + timedelta(minutes=10)
        b.end_time = b.start_time + timedelta(hours=1)
        routes = (
            RouteEvidence(
                travel_mode=mode,
                mode_reason="fixture",
                representative_departure_time=a.end_time,
                availability="available",
                retrieved_at=p.retrieved_at,
                source_ref="fixture:timed_route",
                elements=[
                    dict(
                        origin_place_id=a.source_place_id,
                        destination_place_id=b.source_place_id,
                        condition="ROUTE_EXISTS",
                        duration_seconds=1800,
                        availability="available",
                    )
                ],
            ),
        )
    context = context.model_copy(
        update={
            "contract": context.contract.model_copy(
                update={"time_protections": (), "visit_requirements": ()}
            ),
            "identity_ledger": prep.ledger,
            "policy": ValidationPolicy(review_targets=set()),
            "effective_places": (evidence,),
            "visit_bindings": bindings,
            "route_evidence": routes,
        }
    )
    policy = configured_policy()
    context = context.model_copy(
        update={
            "schedule": build_schedule(
                original, context.contract, context.places, primary_generated=True
            )
        }
    )
    context = context.model_copy(
        update={
            "schedule": prepare_blank_windows(original, context, policy),
            "transitions": bind_transitions(original, mode),
        }
    )
    report = assess(original, context)
    scope = operation_scope(original, report, mode=mode, context=context, policy=policy)
    if kind == "retime":
        scope = scope.model_copy(
            update={
                "permissions": tuple(
                    p.model_copy(update={"operations": frozenset({"retime"}), "move_dates": ()})
                    for p in scope.permissions
                ),
                "add_dates": (),
                "coverage_permissions": (),
            }
        )
    prep = asyncio.run(
        prepare_candidates(
            context, scope, RepairBudget(monotonic() + 600, policy=policy), original=original
        )
    )
    return original, report, scope, context, prep


def main():
    rows = []
    samples = [
        ("retime_only", retime_fixture()),
        ("c_opening_retime", c_fixture("retime")),
        ("c_route_reorder_union28", c_fixture("route")),
        ("c_replace_compensate_move_union28", c_fixture("move")),
        ("round2_c_obligation_feedback_union28", c_fixture("move")),
        ("b_dedup_compensation_union28", b_fixture("repeat")),
        ("b_adjacent_move_union28", b_fixture("move")),
        ("b_missing_date_union28", b_fixture("missing")),
        ("round2_b_related_feedback_union28", b_fixture("feedback")),
        ("single_date_addition_union28", addition_fixture()),
        ("three_target_addition_union28", addition_fixture(3)),
        ("ten_day_other_operations_union28", fixture(10, 28)),
        ("long_text_union28", fixture(10, 28, True)),
        ("24_requirements_conflicting_hours", enriched_fixture()),
        ("elastic_fixed_time_union28", time_window_fixture()),
        ("round2_residual_split_union28", time_window_fixture(later=True)),
        ("round2_long_time_context_union28", time_window_fixture(later=True, long=True)),
    ]
    from types import SimpleNamespace

    from backend.app.versions.v3.repair_models import RepairComparison, RepairPatch, TargetProgress
    from backend.app.versions.v3.repair_service import round_feedback

    feedback = round_feedback(
        SimpleNamespace(
            status="REJECTED",
            reason="No verifiable arrangement improvement",
            parsed_patch=RepairPatch(edits=()),
            spatial={"accepted": True, "legs": [], "daily": []},
            comparison=RepairComparison(
                accepted=False,
                reason="No verifiable arrangement improvement",
                progress=(
                    TargetProgress(
                        finding_id="coverage",
                        check="coverage",
                        outcome="unresolved",
                        before=1,
                        after=1,
                    ),
                ),
            ),
        ),
        False,
    )
    later_feedback = dict(
        feedback,
        previous_status="ACCEPTED_PARTIAL",
        reason="partial_target_improvement",
        adjustment="Keep the accepted visit; address the remaining date only.",
    )
    samples.extend(
        [
            ("round2_feedback_union28", addition_fixture(3)),
            ("round3_feedback_union28", addition_fixture(3)),
        ]
    )
    for label, args in samples:
        from backend.app.versions.v3.repair_budget import configured_policy
        from backend.app.versions.v3.repair_candidates import spatial_candidate_options

        original, report, scope, context, preparation = args
        preparation = preparation.model_copy(
            update={
                "spatial_options": spatial_candidate_options(
                    {c.place.place_id for c in preparation.input_candidates},
                    set(preparation.scheduled_ids),
                    preparation.authorizations,
                    {c.place.place_id: c for c in preparation.ledger},
                    configured_policy(),
                    scope.travel_mode,
                )
            }
        )
        args = original, report, scope, context, preparation
        row = {"fixture": label}
        try:
            _, _, counts = build_repair_input(
                *args,
                route_evidence=context.route_evidence,
                feedback=later_feedback
                if label.startswith("round3")
                else feedback
                if label.startswith("round2")
                else None,
            )
            row.update(counts, status="within_ceiling")
        except ValueError as exc:
            row.update(status="rejected", reason=str(exc), **getattr(exc, "counts", {}))
        rows.append(row)
    output = FoundryRepairPatchDTO.model_validate(
        {
            "edits": [
                {
                    "operation": "add",
                    "activity_id": None,
                    "date": "2026-09-26",
                    "place_id": f"place_{i}",
                    "start_time": "2026-09-26T10:00:00+00:00",
                    "end_time": "2026-09-26T11:00:00+00:00",
                }
                for i in range(50)
            ]
        }
    )
    print(
        json.dumps(
            {
                "method": "Actual Repair prompt/DTO/schema; offline o200k; synthetic only",
                "inputs": rows,
                "synthetic_50_edit_output_tokens": count_tokens(output.model_dump_json()),
                "output_limit_is_not_model_completion_guarantee": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
