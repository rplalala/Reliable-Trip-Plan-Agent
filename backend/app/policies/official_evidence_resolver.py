"""Deterministic claim-, scope-, and date-specific evidence composition."""

import re
from dataclasses import dataclass
from datetime import date, time, timedelta

from backend.app.evidence.effective_models import (
    EffectiveFacetStatus,
    EffectiveFact,
    EffectiveNeedStatus,
    EffectiveOperationalDay,
    EffectivePlaceEvidence,
    EvidenceDimension,
    EvidenceRelation,
    OperationalDayStatus,
    StructuredEvidenceClaim,
)
from backend.app.evidence.models import PlaceEvidence
from backend.app.evidence.official_models import (
    HoursScheduleScope,
    OfficialClaimKind,
    OfficialCurrentEvidence,
    OfficialGapStatus,
    TemporalBasis,
)
from backend.app.evidence.scope_models import SubjectScope
from backend.app.evidence.web_models import (
    OfficialInformationNeed,
    RequestedFacet,
    canonical_facets,
)
from backend.app.policies.official_web import normalize_phrase

_OPERATIONAL = {
    OfficialClaimKind.CURRENT_OPEN,
    OfficialClaimKind.CURRENT_CLOSED,
    OfficialClaimKind.TEMPORARY_CLOSURE,
    OfficialClaimKind.MAINTENANCE_CLOSURE,
    OfficialClaimKind.REOPENING,
    OfficialClaimKind.SPECIAL_OPENING,
}
_HOURS = {
    OfficialClaimKind.REGULAR_HOURS,
    OfficialClaimKind.SPECIAL_HOURS,
    OfficialClaimKind.EARLY_CLOSURE,
}
_ADMISSION = {OfficialClaimKind.FREE_GENERAL_ADMISSION, OfficialClaimKind.PAID_ADMISSION}
_TICKET = {OfficialClaimKind.TICKET_REQUIRED, OfficialClaimKind.TICKET_NOT_REQUIRED}
_ADVANCE_TICKET = {
    OfficialClaimKind.ADVANCE_TICKET_PURCHASE_REQUIRED,
    OfficialClaimKind.ADVANCE_TICKET_PURCHASE_NOT_REQUIRED,
}
_RESERVATION = {
    OfficialClaimKind.RESERVATION_REQUIRED,
    OfficialClaimKind.RESERVATION_NOT_REQUIRED,
}
_CLOSED = {
    OfficialClaimKind.CURRENT_CLOSED,
    OfficialClaimKind.TEMPORARY_CLOSURE,
    OfficialClaimKind.MAINTENANCE_CLOSURE,
}
_OPEN = {
    OfficialClaimKind.CURRENT_OPEN,
    OfficialClaimKind.REOPENING,
    OfficialClaimKind.SPECIAL_OPENING,
}


def claim_dimension(kind: OfficialClaimKind) -> EvidenceDimension:
    if kind in _OPERATIONAL:
        return EvidenceDimension.OPERATIONAL_AVAILABILITY
    if kind in _HOURS:
        return EvidenceDimension.OPENING_HOURS
    if kind in _ADMISSION:
        return EvidenceDimension.ADMISSION_POLICY
    if kind in _TICKET:
        return EvidenceDimension.TICKET_REQUIREMENT
    if kind in _ADVANCE_TICKET:
        return EvidenceDimension.ADVANCE_TICKET_PURCHASE_REQUIREMENT
    if kind in _RESERVATION:
        return EvidenceDimension.RESERVATION_REQUIREMENT
    raise ValueError("Unsupported official claim kind")


@dataclass(frozen=True)
class _Record:
    dimension: EvidenceDimension
    subject_scope: SubjectScope
    scope_text: str | None
    value_kind: str
    value_text: str
    temporal_basis: TemporalBasis
    start: date | None
    end: date | None
    opens_at: time | None
    closes_at: time | None
    schedule_scope: HoursScheduleScope | None
    schedule_text: str | None
    amount: str | None
    currency: str | None
    source_ref: str
    official: bool
    authority_basis: str = "google_places"
    updated_at: date | None = None

    @property
    def scope_key(self) -> tuple[SubjectScope, str]:
        if self.subject_scope is SubjectScope.WHOLE_VENUE:
            return self.subject_scope, ""
        return self.subject_scope, normalize_phrase(self.scope_text or "")

    def applies_on(self, day: date) -> bool:
        return bool(self.start and self.end and self.start <= day <= self.end)

    @property
    def explicit(self) -> bool:
        return self.temporal_basis is TemporalBasis.EXPLICIT_DATE_OR_RANGE


def _official_record(item: OfficialCurrentEvidence) -> _Record:
    return _Record(
        dimension=claim_dimension(item.claim_kind),
        subject_scope=item.subject_scope,
        scope_text=item.scope_text,
        value_kind=item.claim_kind.value,
        value_text=item.value_text,
        temporal_basis=item.temporal_basis,
        start=item.applicable_start_date,
        end=item.applicable_end_date,
        opens_at=item.opens_at,
        closes_at=item.closes_at,
        schedule_scope=item.schedule_scope,
        schedule_text=item.schedule_text,
        amount=item.amount,
        currency=item.currency,
        source_ref=item.source_ref,
        official=True,
        authority_basis=item.authority_basis,
        updated_at=item.updated_at,
    )


def _structured_record(item: StructuredEvidenceClaim) -> _Record:
    return _Record(
        dimension=item.dimension,
        subject_scope=item.subject_scope,
        scope_text=item.scope_text,
        value_kind=item.value_kind,
        value_text=item.value_text,
        temporal_basis=item.temporal_basis,
        start=item.applicable_start_date,
        end=item.applicable_end_date,
        opens_at=item.opens_at,
        closes_at=item.closes_at,
        schedule_scope=item.schedule_scope,
        schedule_text=item.schedule_text,
        amount=None,
        currency=None,
        source_ref=item.source_ref,
        official=False,
        authority_basis=item.authority_basis,
        updated_at=item.source_updated_at,
    )


def _place_records(place: PlaceEvidence) -> tuple[_Record, ...]:
    records: list[_Record] = []
    if place.business_status:
        records.append(
            _Record(
                EvidenceDimension.OPERATIONAL_AVAILABILITY,
                SubjectScope.WHOLE_VENUE,
                None,
                place.business_status.casefold(),
                place.business_status,
                TemporalBasis.CURRENT_POINT_STATUS,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                place.source_ref,
                False,
            )
        )
    if place.opening_hours and place.opening_hours.weekday_descriptions:
        records.append(
            _Record(
                EvidenceDimension.OPENING_HOURS,
                SubjectScope.WHOLE_VENUE,
                None,
                "places_opening_baseline",
                "; ".join(place.opening_hours.weekday_descriptions),
                TemporalBasis.CURRENT_GENERAL_POLICY,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                place.source_ref,
                False,
            )
        )
    return tuple(records)


def _same_group(left: _Record, right: _Record) -> bool:
    return left.dimension is right.dimension and left.scope_key == right.scope_key


def _overlap(left: _Record, right: _Record) -> bool:
    if left.explicit and right.explicit:
        return bool(
            left.start
            and left.end
            and right.start
            and right.end
            and left.start <= right.end
            and right.start <= left.end
        )
    return True


def _same_value(left: _Record, right: _Record) -> bool:
    if left.dimension is EvidenceDimension.OPERATIONAL_AVAILABILITY:
        closed = {"closed", "closed_temporarily", "closed_permanently"} | {
            item.value for item in _CLOSED
        }
        open_values = {"open", "operational"} | {item.value for item in _OPEN}
        if left.value_kind in closed and right.value_kind in closed:
            return True
        if left.value_kind in open_values and right.value_kind in open_values:
            return True
    if left.value_kind != right.value_kind:
        return False
    if left.dimension is EvidenceDimension.OPENING_HOURS:
        return (
            left.opens_at,
            left.closes_at,
            left.schedule_scope,
            normalize_phrase(left.schedule_text or ""),
        ) == (
            right.opens_at,
            right.closes_at,
            right.schedule_scope,
            normalize_phrase(right.schedule_text or ""),
        )
    if left.dimension is EvidenceDimension.ADMISSION_POLICY and left.value_kind == "paid_admission":
        return (left.amount, left.currency) == (right.amount, right.currency)
    return True


def _is_exception_pair(left: _Record, right: _Record) -> bool:
    if not _same_group(left, right):
        return False
    return (left.explicit and right.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY) or (
        right.explicit and left.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY
    )


def _conflicts(records: tuple[_Record, ...]) -> tuple[str, ...]:
    conflicts: set[str] = set()
    for index, left in enumerate(records):
        for right in records[index + 1 :]:
            if not _same_group(left, right) or not _overlap(left, right):
                continue
            if _is_exception_pair(left, right) or _same_value(left, right):
                continue
            if "places_opening_baseline" in {left.value_kind, right.value_kind}:
                continue
            if left.temporal_basis is TemporalBasis.CURRENT_POINT_STATUS or (
                right.temporal_basis is TemporalBasis.CURRENT_POINT_STATUS
            ):
                continue
            if left.explicit != right.explicit:
                continue
            conflicts.update((left.source_ref, right.source_ref))
    return tuple(sorted(conflicts))


def _relation(
    record: _Record, others: tuple[_Record, ...], conflicts: set[str]
) -> EvidenceRelation:
    if record.source_ref in conflicts:
        return EvidenceRelation.CONFLICT
    if record.subject_scope is SubjectScope.UNKNOWN:
        return EvidenceRelation.UNRESOLVED
    related = tuple(
        item
        for item in others
        if item.source_ref != record.source_ref and _same_group(record, item)
    )
    if record.explicit:
        if any(
            item.explicit and _same_value(record, item) and _overlap(record, item)
            for item in related
        ):
            return EvidenceRelation.DUPLICATE
        if any(item.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY for item in related) or (
            record.dimension is EvidenceDimension.OPERATIONAL_AVAILABILITY
            and any(
                not item.official and item.temporal_basis is TemporalBasis.CURRENT_POINT_STATUS
                for item in related
            )
        ):
            return EvidenceRelation.SCOPED_OVERRIDE
        return EvidenceRelation.DATE_SPECIFIC_EXCEPTION
    if any(_same_value(record, item) and _overlap(record, item) for item in related):
        return EvidenceRelation.DUPLICATE
    if record.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY:
        return EvidenceRelation.GENERAL_BASELINE
    return EvidenceRelation.COMPATIBLE_ADDITION


def _day_status(
    day: date,
    records: tuple[_Record, ...],
    conflicts: set[str],
    place: PlaceEvidence,
) -> EffectiveOperationalDay:
    relevant = tuple(
        item
        for item in records
        if (
            item.dimension is EvidenceDimension.OPERATIONAL_AVAILABILITY
            and item.subject_scope is SubjectScope.WHOLE_VENUE
            and item.explicit
            and item.applies_on(day)
        )
    )
    if any(item.source_ref in conflicts for item in relevant):
        return EffectiveOperationalDay(
            date=day,
            status=OperationalDayStatus.UNRESOLVED_CONFLICT,
            source_refs=tuple(sorted({item.source_ref for item in relevant})),
            unresolved_reason="conflicting_date_specific_operational_claims",
        )
    if relevant:
        kinds = {item.value_kind for item in relevant}
        closed = any(kind in {item.value for item in _CLOSED} | {"closed"} for kind in kinds)
        opened = any(kind in {item.value for item in _OPEN} | {"open"} for kind in kinds)
        if closed and opened:
            return EffectiveOperationalDay(
                date=day,
                status=OperationalDayStatus.UNRESOLVED_CONFLICT,
                source_refs=tuple(sorted({item.source_ref for item in relevant})),
                unresolved_reason="incompatible_operational_states",
            )
        if closed or opened:
            return EffectiveOperationalDay(
                date=day,
                status=(
                    OperationalDayStatus.CONFIRMED_DATE_CLOSED
                    if closed
                    else OperationalDayStatus.CONFIRMED_DATE_OPEN
                ),
                source_refs=tuple(sorted({item.source_ref for item in relevant})),
            )
    daily_official = tuple(
        item
        for item in records
        if item.official
        and item.dimension is EvidenceDimension.OPENING_HOURS
        and item.subject_scope is SubjectScope.WHOLE_VENUE
        and item.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY
        and item.schedule_scope is HoursScheduleScope.DAILY
    )
    if daily_official and any(item.source_ref in conflicts for item in daily_official):
        return EffectiveOperationalDay(
            date=day,
            status=OperationalDayStatus.UNKNOWN_DATE_STATUS,
            source_refs=tuple(item.source_ref for item in daily_official),
            unresolved_reason="conflicting_general_hours",
        )
    if daily_official:
        return EffectiveOperationalDay(
            date=day,
            status=OperationalDayStatus.GENERAL_BASELINE,
            source_refs=tuple(item.source_ref for item in daily_official),
            general_baseline="Current official daily hours; date-specific exception unknown",
        )
    day_name = day.strftime("%A").casefold() + ":"
    matching_places_hours = bool(
        place.opening_hours
        and any(
            line.casefold().startswith(day_name) and re.search(r"\d", line)
            for line in place.opening_hours.weekday_descriptions
        )
    )
    if matching_places_hours:
        return EffectiveOperationalDay(
            date=day,
            status=OperationalDayStatus.GENERAL_BASELINE,
            source_refs=(place.source_ref,),
            general_baseline="Places opening-hours pattern; date-specific exception unknown",
        )
    return EffectiveOperationalDay(
        date=day,
        status=OperationalDayStatus.UNKNOWN_DATE_STATUS,
        source_refs=(place.source_ref,) if place.business_status else (),
        general_baseline=(
            "Places current operational status only" if place.business_status else None
        ),
    )


def _facet_claim_matches(facet: RequestedFacet, item: OfficialCurrentEvidence) -> bool:
    if facet is RequestedFacet.GENERAL_ADMISSION_POLICY:
        return item.claim_kind in _ADMISSION
    if facet is RequestedFacet.ADMISSION_FEE:
        return item.claim_kind is OfficialClaimKind.FREE_GENERAL_ADMISSION or (
            item.claim_kind is OfficialClaimKind.PAID_ADMISSION and item.amount is not None
        )
    if facet is RequestedFacet.TICKET_REQUIREMENT:
        return item.claim_kind in _TICKET
    if facet is RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT:
        return item.claim_kind in _ADVANCE_TICKET
    return item.claim_kind in _RESERVATION


def _requested_scope_matches(
    item: OfficialCurrentEvidence, scope: SubjectScope, scope_text: str | None
) -> bool:
    if item.subject_scope is not scope:
        return False
    if scope is SubjectScope.WHOLE_VENUE:
        return True
    requested = normalize_phrase(scope_text or "")
    actual = normalize_phrase(item.scope_text or item.subject_text or "")
    return bool(requested and f" {requested} " in f" {actual} ")


def _policy_applies(item: OfficialCurrentEvidence, start: date, end: date) -> bool:
    return item.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY or bool(
        item.temporal_basis is TemporalBasis.EXPLICIT_DATE_OR_RANGE
        and item.applicable_start_date
        and item.applicable_end_date
        and item.applicable_start_date <= start
        and item.applicable_end_date >= end
    )


def _facet_status(
    need: OfficialInformationNeed,
    facet: RequestedFacet,
    official: tuple[OfficialCurrentEvidence, ...],
    conflicts: set[str],
    start: date,
    end: date,
    scope: SubjectScope,
    scope_text: str | None,
) -> EffectiveFacetStatus:
    direct = tuple(
        item
        for item in official
        if item.information_need is need
        and _facet_claim_matches(facet, item)
        and _requested_scope_matches(item, scope, scope_text)
        and _policy_applies(item, start, end)
    )
    refs = tuple(sorted({item.source_ref for item in direct}))
    if any(item.source_ref in conflicts for item in direct):
        status = OfficialGapStatus.PARTIAL
        reasons = ("conflicting_official_claims",)
    elif direct:
        status = OfficialGapStatus.AVAILABLE
        reasons = ()
    else:
        status = OfficialGapStatus.UNKNOWN
        reasons = ("requested_facet_unanswered",)
    return EffectiveFacetStatus(
        information_need=need,
        requested_facet=facet,
        requested_subject_scope=scope,
        requested_scope_text=scope_text,
        status=status,
        source_refs=refs,
        reason_codes=reasons,
    )


def _need_status(
    need: OfficialInformationNeed,
    official: tuple[OfficialCurrentEvidence, ...],
    conflicts: set[str],
    start: date,
    end: date,
) -> EffectiveNeedStatus:
    items = tuple(
        item
        for item in official
        if item.information_need is need and item.subject_scope is SubjectScope.WHOLE_VENUE
    )
    if not items:
        return EffectiveNeedStatus(information_need=need, status=OfficialGapStatus.UNKNOWN)
    refs = tuple(sorted({item.source_ref for item in items}))
    if any(item.source_ref in conflicts for item in items):
        return EffectiveNeedStatus(
            information_need=need,
            status=OfficialGapStatus.PARTIAL,
            source_refs=refs,
            reason_codes=("conflicting_official_claims",),
        )
    adequate = False
    if need is OfficialInformationNeed.ADMISSION_TICKET:
        adequate = any(
            item.claim_kind is OfficialClaimKind.FREE_GENERAL_ADMISSION
            or (item.claim_kind is OfficialClaimKind.PAID_ADMISSION and item.amount is not None)
            for item in items
            if item.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY
            or (
                item.applicable_start_date is not None
                and item.applicable_start_date <= start
                and item.applicable_end_date is not None
                and item.applicable_end_date >= end
            )
        )
    elif need is OfficialInformationNeed.RESERVATION_REQUIREMENT:
        adequate = any(
            item.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY
            or (
                item.applicable_start_date is not None
                and item.applicable_start_date <= start
                and item.applicable_end_date is not None
                and item.applicable_end_date >= end
            )
            for item in items
        )
    elif need is OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS:
        adequate = any(item.temporal_basis is TemporalBasis.CURRENT_POINT_STATUS for item in items)
    elif need is OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION:
        adequate = any(
            item.temporal_basis is TemporalBasis.EXPLICIT_DATE_OR_RANGE
            and item.applicable_start_date is not None
            and item.applicable_start_date <= start
            and item.applicable_end_date is not None
            and item.applicable_end_date >= end
            for item in items
        )
    elif need is OfficialInformationNeed.SPECIAL_DATE_HOURS:
        has_daily_baseline = any(
            item.claim_kind is OfficialClaimKind.REGULAR_HOURS
            and item.schedule_scope is HoursScheduleScope.DAILY
            and item.opens_at is not None
            and item.closes_at is not None
            and item.source_ref not in conflicts
            for item in official
        )
        adequate = any(
            item.temporal_basis is TemporalBasis.EXPLICIT_DATE_OR_RANGE
            and item.applicable_start_date is not None
            and item.applicable_start_date <= start
            and item.applicable_end_date is not None
            and item.applicable_end_date >= end
            and (
                (item.opens_at is not None and item.closes_at is not None)
                or (item.claim_kind is OfficialClaimKind.EARLY_CLOSURE and has_daily_baseline)
            )
            for item in items
        )
    return EffectiveNeedStatus(
        information_need=need,
        status=OfficialGapStatus.AVAILABLE if adequate else OfficialGapStatus.PARTIAL,
        source_refs=refs,
        reason_codes=() if adequate else ("claim_scope_insufficient",),
    )


def resolve_effective_evidence(
    place: PlaceEvidence,
    official: tuple[OfficialCurrentEvidence, ...],
    *,
    trip_start: date,
    trip_end: date,
    structured_claims: tuple[StructuredEvidenceClaim, ...] = (),
    needs: tuple[OfficialInformationNeed, ...] = (),
    requested_facets: tuple[RequestedFacet, ...] = (),
    requested_subject_scope: SubjectScope = SubjectScope.WHOLE_VENUE,
    requested_scope_text: str | None = None,
) -> EffectivePlaceEvidence:
    """Produce bounded pre-planner evidence without inferring OPEN from search absence."""

    if trip_end < trip_start or (trip_end - trip_start).days > 9:
        raise ValueError("Effective evidence requires a supported trip window")
    if any(item.place_id != place.place_id for item in (*official, *structured_claims)):
        raise ValueError("Evidence place IDs must match")
    if any(
        item.authority_basis not in {"places_first_party_website", "configured_place_need_domain"}
        for item in official
    ):
        raise ValueError("Official evidence authority is not validated")
    records = (
        *_place_records(place),
        *(_structured_record(item) for item in structured_claims),
        *(_official_record(item) for item in official),
    )
    conflicts = set(_conflicts(records))
    facts: list[EffectiveFact] = []
    for item in records:
        if not item.official and item.temporal_basis is TemporalBasis.CURRENT_POINT_STATUS:
            continue
        facts.append(
            EffectiveFact(
                dimension=item.dimension,
                subject_scope=item.subject_scope,
                scope_text=item.scope_text,
                date=item.start if item.start == item.end else None,
                applicable_start_date=item.start,
                applicable_end_date=item.end,
                value_kind=item.value_kind,
                value_text=item.value_text,
                opens_at=item.opens_at,
                closes_at=item.closes_at,
                schedule_scope=item.schedule_scope,
                schedule_text=item.schedule_text,
                temporal_basis=item.temporal_basis,
                relation=_relation(item, records, conflicts),
                source_refs=(item.source_ref,),
                authority_bases=(item.authority_basis,),
                source_updated_at=item.updated_at,
                unresolved_reason="incompatible_same_scope_claims"
                if item.source_ref in conflicts
                else None,
            )
        )
    for offset in range((trip_end - trip_start).days + 1):
        day = trip_start + timedelta(days=offset)
        hours = tuple(
            item
            for item in records
            if (
                item.dimension is EvidenceDimension.OPENING_HOURS
                and item.subject_scope is SubjectScope.WHOLE_VENUE
                and (
                    item.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY
                    or item.applies_on(day)
                )
            )
        )
        specific = tuple(item for item in hours if item.explicit and item.applies_on(day))
        general = tuple(
            item
            for item in hours
            if item.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY
            and item.schedule_scope is HoursScheduleScope.DAILY
            and item.source_ref not in conflicts
        )
        if specific and not any(item.source_ref in conflicts for item in specific):
            chosen = specific[0]
            baseline = next((item for item in general if item.opens_at), None)
            facts.append(
                EffectiveFact(
                    dimension=EvidenceDimension.OPENING_HOURS,
                    subject_scope=SubjectScope.WHOLE_VENUE,
                    date=day,
                    applicable_start_date=day,
                    applicable_end_date=day,
                    value_kind=chosen.value_kind,
                    value_text=chosen.value_text,
                    opens_at=chosen.opens_at or (baseline.opens_at if baseline else None),
                    closes_at=chosen.closes_at or (baseline.closes_at if baseline else None),
                    temporal_basis=TemporalBasis.EXPLICIT_DATE_OR_RANGE,
                    schedule_scope=chosen.schedule_scope,
                    schedule_text=chosen.schedule_text,
                    relation=(
                        EvidenceRelation.SCOPED_OVERRIDE
                        if baseline
                        else EvidenceRelation.DATE_SPECIFIC_EXCEPTION
                    ),
                    source_refs=tuple(item.source_ref for item in (baseline, chosen) if item),
                    authority_bases=tuple(
                        item.authority_basis for item in (baseline, chosen) if item
                    ),
                    source_updated_at=chosen.updated_at,
                    unresolved_reason=(
                        "opening_baseline_unresolved"
                        if chosen.value_kind == OfficialClaimKind.EARLY_CLOSURE.value
                        and baseline is None
                        else None
                    ),
                )
            )
        elif specific:
            facts.append(
                EffectiveFact(
                    dimension=EvidenceDimension.OPENING_HOURS,
                    subject_scope=SubjectScope.WHOLE_VENUE,
                    date=day,
                    applicable_start_date=day,
                    applicable_end_date=day,
                    value_kind="unresolved_hours",
                    value_text="Conflicting date-specific hours",
                    temporal_basis=TemporalBasis.EXPLICIT_DATE_OR_RANGE,
                    relation=EvidenceRelation.CONFLICT,
                    source_refs=tuple(sorted({item.source_ref for item in specific})),
                    authority_bases=tuple(sorted({item.authority_basis for item in specific})),
                    unresolved_reason="conflicting_date_specific_hours",
                )
            )
        elif general:
            baseline = next((item for item in general if item.opens_at and item.closes_at), None)
            if baseline:
                facts.append(
                    EffectiveFact(
                        dimension=EvidenceDimension.OPENING_HOURS,
                        subject_scope=SubjectScope.WHOLE_VENUE,
                        date=day,
                        applicable_start_date=None,
                        applicable_end_date=None,
                        value_kind=baseline.value_kind,
                        value_text=baseline.value_text,
                        opens_at=baseline.opens_at,
                        closes_at=baseline.closes_at,
                        temporal_basis=TemporalBasis.CURRENT_GENERAL_POLICY,
                        schedule_scope=baseline.schedule_scope,
                        schedule_text=baseline.schedule_text,
                        relation=EvidenceRelation.GENERAL_BASELINE,
                        source_refs=(baseline.source_ref,),
                        authority_bases=(baseline.authority_basis,),
                        source_updated_at=baseline.updated_at,
                    )
                )
        elif any(
            item.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY
            and item.source_ref in conflicts
            for item in hours
        ):
            facts.append(
                EffectiveFact(
                    dimension=EvidenceDimension.OPENING_HOURS,
                    subject_scope=SubjectScope.WHOLE_VENUE,
                    date=day,
                    value_kind="unresolved_hours",
                    value_text="Conflicting general opening hours",
                    temporal_basis=TemporalBasis.UNSPECIFIED,
                    relation=EvidenceRelation.CONFLICT,
                    source_refs=tuple(
                        sorted({item.source_ref for item in hours if item.source_ref in conflicts})
                    ),
                    unresolved_reason="conflicting_general_hours",
                )
            )
    days = tuple(
        _day_status(trip_start + timedelta(days=offset), records, conflicts, place)
        for offset in range((trip_end - trip_start).days + 1)
    )
    selected_needs = needs or tuple(dict.fromkeys(item.information_need for item in official))
    need_statuses = tuple(
        _need_status(need, official, conflicts, trip_start, trip_end) for need in selected_needs
    )
    facet_statuses: tuple[EffectiveFacetStatus, ...] = ()
    if requested_facets:
        if len(selected_needs) != 1 or requested_facets != canonical_facets(requested_facets):
            raise ValueError("Facet evaluation requires one need and canonical facets")
        need = selected_needs[0]
        facet_statuses = tuple(
            _facet_status(
                need,
                facet,
                official,
                conflicts,
                trip_start,
                trip_end,
                requested_subject_scope,
                requested_scope_text,
            )
            for facet in requested_facets
        )
        statuses = {item.status for item in facet_statuses}
        related = any(item.information_need is need for item in official)
        if statuses == {OfficialGapStatus.AVAILABLE}:
            combined = OfficialGapStatus.AVAILABLE
        elif related or statuses & {OfficialGapStatus.AVAILABLE, OfficialGapStatus.PARTIAL}:
            combined = OfficialGapStatus.PARTIAL
        else:
            combined = OfficialGapStatus.UNKNOWN
        need_statuses = (
            EffectiveNeedStatus(
                information_need=need,
                status=combined,
                source_refs=tuple(
                    sorted({ref for item in facet_statuses for ref in item.source_refs})
                ),
                reason_codes=(
                    () if combined is OfficialGapStatus.AVAILABLE else ("facet_scope_insufficient",)
                ),
            ),
        )
    return EffectivePlaceEvidence(
        place_id=place.place_id,
        operational_days=days,
        facts=tuple(facts),
        need_statuses=need_statuses,
        facet_statuses=facet_statuses,
        conflict_source_refs=tuple(sorted(conflicts)),
    )
