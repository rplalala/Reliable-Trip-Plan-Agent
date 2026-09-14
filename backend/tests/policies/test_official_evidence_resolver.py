"""Claim-scoped baseline, exception, and conflict resolution."""

from datetime import UTC, date, datetime, time

from backend.app.evidence.effective_models import (
    EvidenceDimension,
    EvidenceRelation,
    OperationalDayStatus,
    StructuredEvidenceClaim,
)
from backend.app.evidence.models import EvidenceAvailability, OpeningHoursEvidence, PlaceEvidence
from backend.app.evidence.official_models import (
    EvidenceSourceBlock,
    HoursScheduleScope,
    OfficialClaimCandidate,
    OfficialClaimKind,
    OfficialCurrentEvidence,
    OfficialGapStatus,
    SourceKind,
    SubjectScope,
    TemporalBasis,
)
from backend.app.evidence.web_models import (
    OfficialInformationNeed,
    RequestedFacet,
    WebEvidenceTask,
    WebTriggerReason,
    canonical_facets,
)
from backend.app.integrations.web.models import WebSearchHit, WebSearchObservation
from backend.app.policies.official_evidence_gate import accept_official_candidate
from backend.app.policies.official_evidence_resolver import resolve_effective_evidence
from backend.app.runtime.config_loader import load_runtime_config

START = date(2026, 9, 15)
END = date(2026, 9, 17)


def _place(*, business_status="OPERATIONAL", hours=None):
    return PlaceEvidence(
        place_id="museum",
        name="Australian Museum",
        latitude=-33.8,
        longitude=151.2,
        business_status=business_status,
        opening_hours=hours,
        availability=EvidenceAvailability.AVAILABLE,
        website_uri="https://australian.museum",
        source_ref="google_places:museum",
        retrieved_at=datetime(2026, 9, 13, tzinfo=UTC),
    )


def _official(
    kind,
    value,
    ref,
    *,
    need=OfficialInformationNeed.ADMISSION_TICKET,
    basis=TemporalBasis.CURRENT_GENERAL_POLICY,
    scope=SubjectScope.WHOLE_VENUE,
    scope_text=None,
    start=None,
    end=None,
    opens=None,
    closes=None,
    amount=None,
):
    return OfficialCurrentEvidence(
        place_id="museum",
        place_name="Australian Museum",
        information_need=need,
        claim_kind=kind,
        value_text=value,
        source_kind=SourceKind.FETCHED_HTML,
        source_url="https://australian.museum/visit",
        final_url="https://australian.museum/visit",
        supporting_excerpt=f"Australian Museum {value}.",
        subject_scope=scope,
        subject_text="Australian Museum",
        predicate_text=value,
        scope_text=scope_text,
        temporal_basis=basis,
        applicable_start_date=start,
        applicable_end_date=end,
        opens_at=opens,
        closes_at=closes,
        schedule_scope=(
            HoursScheduleScope.DAILY if kind is OfficialClaimKind.REGULAR_HOURS else None
        ),
        schedule_text="daily" if kind is OfficialClaimKind.REGULAR_HOURS else None,
        amount=amount,
        authority_basis="places_first_party_website",
        retrieved_at=datetime(2026, 9, 13, tzinfo=UTC),
        source_ref=ref,
    )


def _resolve(
    *claims,
    place=None,
    structured=(),
    needs=(),
    facets=(),
    scope=SubjectScope.WHOLE_VENUE,
    scope_text=None,
):
    return resolve_effective_evidence(
        place or _place(),
        tuple(claims),
        trip_start=START,
        trip_end=END,
        structured_claims=tuple(structured),
        needs=tuple(needs),
        requested_facets=canonical_facets(tuple(facets)),
        requested_subject_scope=scope,
        requested_scope_text=scope_text,
    )


def test_australian_museum_general_admission_is_available_without_explicit_trip_date() -> None:
    free = _official(
        OfficialClaimKind.FREE_GENERAL_ADMISSION, "FREE general entry", "official:free"
    )
    effective = _resolve(free)
    assert effective.need_statuses[0].status is OfficialGapStatus.AVAILABLE
    admission = next(
        fact for fact in effective.facts if fact.dimension is EvidenceDimension.ADMISSION_POLICY
    )
    assert admission.value_text == "FREE general entry"
    assert admission.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY
    assert admission.date is None
    assert admission.relation is EvidenceRelation.GENERAL_BASELINE


def test_live_backed_australian_museum_sentence_passes_gate_and_resolves_as_general_policy() -> (
    None
):
    url = "https://australian.museum/visit/admission"
    text = "The Australian Museum has FREE general entry."
    source = EvidenceSourceBlock(
        task_id="admission-task",
        source_kind=SourceKind.FETCHED_HTML,
        source_url=url,
        final_url=url,
        text=text,
        body_sha256="offline-fixture-hash",
    )
    task = WebEvidenceTask(
        task_id="admission-task",
        place_id="museum",
        place_name="Australian Museum",
        information_need=OfficialInformationNeed.ADMISSION_TICKET,
        applicable_start_date=START,
        applicable_end_date=START,
        allowed_domains=("australian.museum",),
        trigger_reasons=(WebTriggerReason.RESIDUAL_MISSING,),
        priority_group=2,
        shortlist_index=0,
    )
    candidate = OfficialClaimCandidate(
        source_key=source.source_key,
        place_id="museum",
        place_name="Australian Museum",
        information_need=OfficialInformationNeed.ADMISSION_TICKET,
        claim_kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
        source_kind=SourceKind.FETCHED_HTML,
        source_url=url,
        final_url=url,
        supporting_excerpt=text,
        subject_scope=SubjectScope.WHOLE_VENUE,
        subject_text="The Australian Museum",
        predicate_text="has",
        value_text="FREE general entry",
        temporal_basis=TemporalBasis.CURRENT_GENERAL_POLICY,
    )
    observation = WebSearchObservation(
        provider_status="completed",
        hits=(
            WebSearchHit(
                url=url,
                source_domain="australian.museum",
                snippet=None,
                action_index=0,
                result_index=0,
                allowed_domain=True,
            ),
        ),
    )
    accepted, reason = accept_official_candidate(
        candidate,
        task=task,
        observation=observation,
        sources=(source,),
        place=_place(),
        config=load_runtime_config().web_evidence,
    )
    assert reason == "accepted"
    assert accepted is not None
    assert accepted.value_text == "FREE general entry"
    assert accepted.temporal_basis is TemporalBasis.CURRENT_GENERAL_POLICY
    assert accepted.applicable_start_date is None
    assert accepted.applicable_end_date is None
    effective = resolve_effective_evidence(_place(), (accepted,), trip_start=START, trip_end=START)
    assert effective.need_statuses[0].status is OfficialGapStatus.AVAILABLE
    admission = next(
        fact for fact in effective.facts if fact.dimension is EvidenceDimension.ADMISSION_POLICY
    )
    assert admission.date is None
    assert admission.applicable_start_date is None


def test_point_status_and_no_proactive_exception_do_not_confirm_future_open() -> None:
    current = _official(
        OfficialClaimKind.CURRENT_OPEN,
        "currently open",
        "official:now",
        need=OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS,
        basis=TemporalBasis.CURRENT_POINT_STATUS,
    )
    effective = _resolve(
        current, needs=(OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,)
    )
    assert all(
        day.status is OperationalDayStatus.UNKNOWN_DATE_STATUS for day in effective.operational_days
    )
    assert effective.need_statuses[0].status is OfficialGapStatus.UNKNOWN
    no_web = _resolve(needs=(OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,))
    assert all(
        day.status is OperationalDayStatus.UNKNOWN_DATE_STATUS for day in no_web.operational_days
    )


def test_places_date_closed_and_web_free_admission_do_not_conflict() -> None:
    closed = StructuredEvidenceClaim(
        place_id="museum",
        dimension=EvidenceDimension.OPERATIONAL_AVAILABILITY,
        value_kind="closed",
        value_text="Closed on September 15",
        temporal_basis=TemporalBasis.EXPLICIT_DATE_OR_RANGE,
        applicable_start_date=START,
        applicable_end_date=START,
        source_ref="google_places:dated-closure",
    )
    free = _official(
        OfficialClaimKind.FREE_GENERAL_ADMISSION, "FREE general entry", "official:free"
    )
    effective = _resolve(free, structured=(closed,))
    assert effective.operational_days[0].status is OperationalDayStatus.CONFIRMED_DATE_CLOSED
    assert effective.need_statuses[0].status is OfficialGapStatus.AVAILABLE
    assert effective.conflict_source_refs == ()


def test_official_dated_maintenance_qualifies_places_general_baseline_only_on_covered_days() -> (
    None
):
    hours = OpeningHoursEvidence(
        applicability="regular_weekly_pattern",
        weekday_descriptions=[
            "Tuesday: 09:00-17:00",
            "Wednesday: 09:00-17:00",
            "Thursday: 09:00-17:00",
        ],
    )
    closure = _official(
        OfficialClaimKind.MAINTENANCE_CLOSURE,
        "closed for maintenance",
        "official:closure",
        need=OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
        basis=TemporalBasis.EXPLICIT_DATE_OR_RANGE,
        start=START,
        end=date(2026, 9, 16),
    )
    effective = _resolve(closure, place=_place(hours=hours))
    assert [day.status for day in effective.operational_days] == [
        OperationalDayStatus.CONFIRMED_DATE_CLOSED,
        OperationalDayStatus.CONFIRMED_DATE_CLOSED,
        OperationalDayStatus.GENERAL_BASELINE,
    ]
    assert effective.conflict_source_refs == ()
    assert any(
        fact.relation is EvidenceRelation.SCOPED_OVERRIDE
        for fact in effective.facts
        if fact.value_kind == "maintenance_closure"
    )


def test_regular_hours_and_early_close_compose_only_on_the_exception_date() -> None:
    regular = _official(
        OfficialClaimKind.REGULAR_HOURS,
        "09:00–17:00",
        "official:regular",
        need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        opens=time(9),
        closes=time(17),
    )
    early = _official(
        OfficialClaimKind.EARLY_CLOSURE,
        "closes at 14:00",
        "official:early",
        need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        basis=TemporalBasis.EXPLICIT_DATE_OR_RANGE,
        start=date(2026, 9, 16),
        end=date(2026, 9, 16),
        closes=time(14),
    )
    effective = _resolve(regular, early)
    day_facts = {
        fact.date: fact
        for fact in effective.facts
        if fact.dimension is EvidenceDimension.OPENING_HOURS and fact.date
    }
    assert day_facts[START].opens_at == time(9)
    assert day_facts[START].closes_at == time(17)
    assert day_facts[date(2026, 9, 16)].closes_at == time(14)
    assert day_facts[END].closes_at == time(17)
    assert day_facts[date(2026, 9, 16)].relation is EvidenceRelation.SCOPED_OVERRIDE


def test_special_exhibition_price_does_not_conflict_with_general_free_entry() -> None:
    free = _official(
        OfficialClaimKind.FREE_GENERAL_ADMISSION, "FREE general entry", "official:free"
    )
    paid_exhibition = _official(
        OfficialClaimKind.PAID_ADMISSION,
        "AUD 20",
        "official:exhibition",
        scope=SubjectScope.EXHIBITION,
        scope_text="Birds of Australia exhibition",
        amount="20",
    )
    effective = _resolve(free, paid_exhibition)
    assert effective.conflict_source_refs == ()
    assert (
        len(
            [
                fact
                for fact in effective.facts
                if fact.dimension is EvidenceDimension.ADMISSION_POLICY
            ]
        )
        == 2
    )


def test_same_scope_incompatible_official_claims_remain_unresolved() -> None:
    free = _official(
        OfficialClaimKind.FREE_GENERAL_ADMISSION, "FREE general entry", "official:free"
    )
    paid = _official(
        OfficialClaimKind.PAID_ADMISSION, "AUD 20 admission", "official:paid", amount="20"
    )
    effective = _resolve(free, paid)
    assert effective.conflict_source_refs == ("official:free", "official:paid")
    assert effective.need_statuses[0].status is OfficialGapStatus.PARTIAL
    assert all(
        fact.relation is EvidenceRelation.CONFLICT
        for fact in effective.facts
        if fact.dimension is EvidenceDimension.ADMISSION_POLICY
    )


def test_incompatible_reservation_statements_on_one_official_page_remain_conflict() -> None:
    required = _official(
        OfficialClaimKind.RESERVATION_REQUIRED,
        "booking required",
        "official:required",
        need=OfficialInformationNeed.RESERVATION_REQUIREMENT,
    )
    optional = _official(
        OfficialClaimKind.RESERVATION_NOT_REQUIRED,
        "booking not required",
        "official:optional",
        need=OfficialInformationNeed.RESERVATION_REQUIREMENT,
    )
    effective = _resolve(required, optional)
    assert effective.need_statuses[0].status is OfficialGapStatus.PARTIAL
    assert effective.conflict_source_refs == ("official:optional", "official:required")


def test_incompatible_general_hours_do_not_create_usable_daily_hours() -> None:
    early = _official(
        OfficialClaimKind.REGULAR_HOURS,
        "09:00–17:00",
        "official:hours-one",
        need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        opens=time(9),
        closes=time(17),
    )
    late = _official(
        OfficialClaimKind.REGULAR_HOURS,
        "10:00–18:00",
        "official:hours-two",
        need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        opens=time(10),
        closes=time(18),
    )
    effective = _resolve(early, late, place=_place(business_status=None))
    assert effective.need_statuses[0].status is OfficialGapStatus.PARTIAL
    assert all(
        day.status is OperationalDayStatus.UNKNOWN_DATE_STATUS for day in effective.operational_days
    )
    assert all(
        day.unresolved_reason == "conflicting_general_hours" for day in effective.operational_days
    )


def test_general_hours_alone_do_not_answer_specific_holiday_hours() -> None:
    regular = _official(
        OfficialClaimKind.REGULAR_HOURS,
        "09:00–17:00",
        "official:regular",
        need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        opens=time(9),
        closes=time(17),
    )
    effective = _resolve(regular)
    assert effective.need_statuses[0].status is OfficialGapStatus.PARTIAL


def test_regular_hours_without_daily_scope_are_not_projected_to_each_day() -> None:
    regular = _official(
        OfficialClaimKind.REGULAR_HOURS,
        "09:00–17:00",
        "official:weekday-hours",
        need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        opens=time(9),
        closes=time(17),
    ).model_copy(update={"schedule_scope": None, "schedule_text": None})
    effective = _resolve(regular, place=_place(business_status=None))
    assert all(
        day.status is OperationalDayStatus.UNKNOWN_DATE_STATUS for day in effective.operational_days
    )
    assert not any(
        fact.date for fact in effective.facts if fact.dimension is EvidenceDimension.OPENING_HOURS
    )


def test_temporally_unspecified_admission_does_not_become_near_term_policy() -> None:
    uncertain = _official(
        OfficialClaimKind.FREE_GENERAL_ADMISSION,
        "complimentary entry",
        "official:undated-archive",
        basis=TemporalBasis.UNSPECIFIED,
    )
    effective = _resolve(uncertain)
    assert effective.need_statuses[0].status is OfficialGapStatus.PARTIAL
    assert effective.facts[0].temporal_basis is TemporalBasis.UNSPECIFIED


def test_free_admission_answers_fee_and_policy_but_not_ticket_requirement() -> None:
    free = _official(
        OfficialClaimKind.FREE_GENERAL_ADMISSION, "FREE general entry", "official:free"
    )
    effective = _resolve(
        free,
        facets=(
            RequestedFacet.GENERAL_ADMISSION_POLICY,
            RequestedFacet.ADMISSION_FEE,
            RequestedFacet.TICKET_REQUIREMENT,
        ),
    )
    assert [item.status for item in effective.facet_statuses] == [
        OfficialGapStatus.AVAILABLE,
        OfficialGapStatus.AVAILABLE,
        OfficialGapStatus.UNKNOWN,
    ]
    assert effective.need_statuses[0].status is OfficialGapStatus.PARTIAL
    assert all(
        day.status is OperationalDayStatus.UNKNOWN_DATE_STATUS for day in effective.operational_days
    )


def test_ticket_required_does_not_answer_admission_fee_or_reservation() -> None:
    ticket = _official(OfficialClaimKind.TICKET_REQUIRED, "Tickets required", "official:ticket")
    fee = _resolve(ticket, facets=(RequestedFacet.ADMISSION_FEE,))
    assert fee.facet_statuses[0].status is OfficialGapStatus.UNKNOWN
    assert fee.need_statuses[0].status is OfficialGapStatus.PARTIAL
    reservation = _resolve(
        _official(
            OfficialClaimKind.RESERVATION_NOT_REQUIRED,
            "Booking not required",
            "official:booking",
            need=OfficialInformationNeed.RESERVATION_REQUIREMENT,
        ),
        needs=(OfficialInformationNeed.RESERVATION_REQUIREMENT,),
        facets=(RequestedFacet.RESERVATION_REQUIREMENT,),
    )
    assert reservation.facet_statuses[0].status is OfficialGapStatus.AVAILABLE
    assert not any(
        fact.dimension is EvidenceDimension.TICKET_REQUIREMENT for fact in reservation.facts
    )


def test_exhibition_ticket_not_required_is_scope_bound() -> None:
    ticket = _official(
        OfficialClaimKind.TICKET_NOT_REQUIRED,
        "Tickets not required for permanent exhibitions",
        "official:exhibitions",
        scope=SubjectScope.EXHIBITION,
        scope_text="permanent exhibitions",
    )
    exhibition = _resolve(
        ticket,
        facets=(RequestedFacet.TICKET_REQUIREMENT,),
        scope=SubjectScope.EXHIBITION,
        scope_text="permanent exhibitions",
    )
    assert exhibition.facet_statuses[0].status is OfficialGapStatus.AVAILABLE
    assert exhibition.need_statuses[0].status is OfficialGapStatus.AVAILABLE
    whole = _resolve(ticket, facets=(RequestedFacet.TICKET_REQUIREMENT,))
    assert whole.facet_statuses[0].status is OfficialGapStatus.UNKNOWN
    assert whole.need_statuses[0].status is OfficialGapStatus.PARTIAL
    special = _resolve(
        ticket,
        facets=(RequestedFacet.TICKET_REQUIREMENT,),
        scope=SubjectScope.EXHIBITION,
        scope_text="special exhibitions",
    )
    assert special.facet_statuses[0].status is OfficialGapStatus.UNKNOWN


def test_ticket_claim_alone_does_not_establish_reservation_policy() -> None:
    ticket = _official(
        OfficialClaimKind.TICKET_NOT_REQUIRED,
        "Tickets not required",
        "official:no-ticket",
    )
    effective = _resolve(
        ticket,
        needs=(OfficialInformationNeed.RESERVATION_REQUIREMENT,),
        facets=(RequestedFacet.RESERVATION_REQUIREMENT,),
    )
    assert effective.facet_statuses[0].status is OfficialGapStatus.UNKNOWN
    assert effective.need_statuses[0].status is OfficialGapStatus.UNKNOWN
    assert any(fact.dimension is EvidenceDimension.TICKET_REQUIREMENT for fact in effective.facts)


def test_ticket_need_requires_temporally_applicable_claim() -> None:
    dated = _official(
        OfficialClaimKind.TICKET_REQUIRED,
        "Tickets required on 1 December",
        "official:old-ticket",
        basis=TemporalBasis.EXPLICIT_DATE_OR_RANGE,
        start=date(2026, 12, 1),
        end=date(2026, 12, 1),
    )
    effective = _resolve(dated, facets=(RequestedFacet.TICKET_REQUIREMENT,))
    assert effective.facet_statuses[0].status is OfficialGapStatus.UNKNOWN
    assert effective.need_statuses[0].status is OfficialGapStatus.PARTIAL


def test_advance_purchase_claim_is_distinct_from_ticket_requirement() -> None:
    advance = _official(
        OfficialClaimKind.ADVANCE_TICKET_PURCHASE_NOT_REQUIRED,
        "Tickets need not be purchased in advance",
        "official:advance",
    )
    effective = _resolve(
        advance,
        facets=(
            RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT,
            RequestedFacet.TICKET_REQUIREMENT,
        ),
    )
    assert [item.status for item in effective.facet_statuses] == [
        OfficialGapStatus.AVAILABLE,
        OfficialGapStatus.UNKNOWN,
    ]


def test_paid_admission_without_amount_is_policy_but_not_fee() -> None:
    paid = _official(OfficialClaimKind.PAID_ADMISSION, "Admission is paid", "official:paid")
    effective = _resolve(
        paid,
        facets=(RequestedFacet.GENERAL_ADMISSION_POLICY, RequestedFacet.ADMISSION_FEE),
    )
    assert [item.status for item in effective.facet_statuses] == [
        OfficialGapStatus.UNKNOWN,
        OfficialGapStatus.AVAILABLE,
    ]
    with_amount = _resolve(
        paid.model_copy(update={"amount": "20"}),
        facets=(RequestedFacet.ADMISSION_FEE,),
    )
    assert with_amount.facet_statuses[0].status is OfficialGapStatus.AVAILABLE


def test_same_scope_opposing_ticket_claims_keep_facet_partial() -> None:
    required = _official(OfficialClaimKind.TICKET_REQUIRED, "Tickets required", "official:yes")
    not_required = _official(
        OfficialClaimKind.TICKET_NOT_REQUIRED, "Tickets not required", "official:no"
    )
    effective = _resolve(required, not_required, facets=(RequestedFacet.TICKET_REQUIREMENT,))
    assert effective.facet_statuses[0].status is OfficialGapStatus.PARTIAL
    assert effective.need_statuses[0].status is OfficialGapStatus.PARTIAL
