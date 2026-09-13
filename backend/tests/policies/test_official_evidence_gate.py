"""Grounding/provenance checks without a positive English claim dictionary."""

from datetime import UTC, date, datetime, time

import pytest

from backend.app.evidence.models import EvidenceAvailability, PlaceEvidence
from backend.app.evidence.official_models import (
    EvidenceSourceBlock,
    HoursScheduleScope,
    OfficialClaimCandidate,
    OfficialClaimKind,
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
)
from backend.app.integrations.web.http_page_retriever import RawPageResponse, _html_text
from backend.app.integrations.web.models import WebSearchHit, WebSearchObservation
from backend.app.policies.official_evidence_gate import accept_official_candidate
from backend.app.policies.official_evidence_resolver import resolve_effective_evidence
from backend.app.runtime.config_loader import load_runtime_config

DAY = date(2026, 12, 25)
URL = "https://alpha.example.org/notice"


def _place(name="Alpha Zoo", website="https://alpha.example.org"):
    return PlaceEvidence(
        place_id="alpha",
        name=name,
        latitude=-33.8,
        longitude=151.2,
        business_status="OPERATIONAL",
        availability=EvidenceAvailability.AVAILABLE,
        website_uri=website,
        source_ref="google_places:alpha",
        retrieved_at=datetime(2026, 12, 20, tzinfo=UTC),
    )


def _task(need=OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION, name="Alpha Zoo"):
    return WebEvidenceTask(
        task_id="task-1",
        place_id="alpha",
        place_name=name,
        information_need=need,
        applicable_start_date=DAY,
        applicable_end_date=DAY,
        allowed_domains=("alpha.example.org",),
        trigger_reasons=(WebTriggerReason.EXPLICIT_DATE_QUESTION,),
        priority_group=2,
        shortlist_index=0,
    )


def _source(text, *, url=URL, kind=SourceKind.NATIVE_SNIPPET, final=None, redirects=()):
    return EvidenceSourceBlock(
        task_id="task-1",
        source_kind=kind,
        source_url=url,
        final_url=final,
        redirect_chain=redirects,
        text=text,
        body_sha256="abc" if kind is SourceKind.FETCHED_HTML else None,
    )


def _candidate(
    source,
    *,
    need=OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
    kind=OfficialClaimKind.MAINTENANCE_CLOSURE,
    value="will not open",
    subject="Alpha Zoo",
    predicate=None,
    scope=SubjectScope.WHOLE_VENUE,
    temporal=TemporalBasis.EXPLICIT_DATE_OR_RANGE,
    date_text="25 December 2026",
    start=DAY,
    end=DAY,
    **other,
):
    data = dict(
        source_key=source.source_key,
        place_id="alpha",
        place_name="Alpha Zoo",
        information_need=need,
        claim_kind=kind,
        source_kind=source.source_kind,
        source_url=source.source_url,
        final_url=source.final_url,
        supporting_excerpt=source.text,
        subject_scope=scope,
        subject_text=subject,
        predicate_text=predicate or source.text.split(subject, 1)[-1].strip().rstrip("."),
        scope_text=None,
        value_text=value,
        temporal_basis=temporal,
        date_text=date_text,
        applicable_start_date=start,
        applicable_end_date=end,
    )
    data.update(other)
    return OfficialClaimCandidate(**data)


def _gate(candidate, source, *, task=None, place=None, observation=None, sources=None):
    observation = observation or WebSearchObservation(
        provider_status="completed",
        hits=(
            WebSearchHit(
                url=source.source_url,
                source_domain="alpha.example.org",
                snippet=source.text,
                action_index=0,
                result_index=0,
                allowed_domain=True,
            ),
        ),
    )
    return accept_official_candidate(
        candidate,
        task=task or _task(candidate.information_need),
        observation=observation,
        sources=sources or (source,),
        place=place or _place(),
        config=load_runtime_config().web_evidence,
        retrieved_at=datetime(2026, 12, 20, tzinfo=UTC),
    )


def _page_source(html: str) -> EvidenceSourceBlock:
    html = html.replace("<title>", "<head><title>", 1).replace("</title>", "</title></head>", 1)
    text, title, blocks = _html_text(
        RawPageResponse(200, {"content-type": "text/html"}, html.encode()), 20000
    )
    return EvidenceSourceBlock(
        task_id="task-1",
        source_kind=SourceKind.FETCHED_HTML,
        source_url=URL,
        final_url=URL,
        text=text,
        body_sha256="fixture-body-hash",
        page_title=title,
        content_blocks=blocks,
    )


def _page_candidate(
    source: EvidenceSourceBlock,
    sentence: str,
    *,
    kind: OfficialClaimKind,
    subject: str,
    predicate: str,
    value: str,
    scope: SubjectScope,
    scope_text: str | None,
) -> OfficialClaimCandidate:
    return _candidate(
        source,
        need=OfficialInformationNeed.ADMISSION_TICKET,
        kind=kind,
        subject=subject,
        predicate=predicate,
        value=value,
        scope=scope,
        scope_text=scope_text,
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    ).model_copy(update={"supporting_excerpt": sentence})


def test_first_party_title_section_and_local_scope_ground_ticket_without_venue_repeat() -> None:
    sentence = "Tickets are not required for permanent exhibitions."
    source = _page_source(
        "<title>Admission - Alpha Zoo</title><main><h1>Admission</h1>"
        f"<h2>Tickets</h2><p>{sentence}</p></main>"
    )
    candidate = _page_candidate(
        source,
        sentence,
        kind=OfficialClaimKind.TICKET_NOT_REQUIRED,
        subject="Tickets",
        predicate="are not required for",
        value="not required",
        scope=SubjectScope.EXHIBITION,
        scope_text="permanent exhibitions",
    )
    accepted, reason = _gate(candidate, source)
    assert reason == "accepted"
    assert accepted is not None
    assert accepted.subject_scope is SubjectScope.EXHIBITION
    assert accepted.scope_text == "permanent exhibitions"


def test_source_visible_local_subject_canonicalizes_secondary_scope_qualifier() -> None:
    sentence = "Tickets are not required for permanent exhibitions with FREE General Entry."
    source = _page_source(
        "<title>Admission - Alpha Zoo</title><main><h1>Admission</h1>"
        f"<h2>Tickets</h2><p>{sentence}</p></main>"
    )
    task = _task(OfficialInformationNeed.ADMISSION_TICKET).model_copy(
        update={
            "requested_facets": (RequestedFacet.TICKET_REQUIREMENT,),
            "requested_subject_scope": SubjectScope.EXHIBITION,
            "requested_scope_text": "permanent exhibitions",
        }
    )
    candidate = _page_candidate(
        source,
        sentence,
        kind=OfficialClaimKind.TICKET_NOT_REQUIRED,
        subject="permanent exhibitions",
        predicate="with FREE General Entry",
        value="not required",
        scope=SubjectScope.EXHIBITION,
        scope_text="with FREE General Entry",
    ).model_copy(update={"supporting_excerpt": f"Tickets\n{sentence}"})
    accepted, reason = _gate(candidate, source, task=task)
    assert reason == "accepted"
    assert accepted is not None
    assert accepted.scope_text == "permanent exhibitions"
    matching = resolve_effective_evidence(
        _place(),
        (accepted,),
        trip_start=DAY,
        trip_end=DAY,
        needs=(OfficialInformationNeed.ADMISSION_TICKET,),
        requested_facets=(RequestedFacet.TICKET_REQUIREMENT,),
        requested_subject_scope=SubjectScope.EXHIBITION,
        requested_scope_text="permanent exhibitions",
    )
    whole = resolve_effective_evidence(
        _place(),
        (accepted,),
        trip_start=DAY,
        trip_end=DAY,
        needs=(OfficialInformationNeed.ADMISSION_TICKET,),
        requested_facets=(RequestedFacet.TICKET_REQUIREMENT,),
    )
    assert matching.facet_statuses[0].status is OfficialGapStatus.AVAILABLE
    assert whole.facet_statuses[0].status is OfficialGapStatus.UNKNOWN


def test_first_party_title_can_ground_local_whole_venue_claim_without_name_repeat() -> None:
    sentence = "Admission is free."
    source = _page_source(
        f"<title>Admission - Alpha Zoo</title><main><h1>Admission</h1><p>{sentence}</p></main>"
    )
    candidate = _page_candidate(
        source,
        sentence,
        kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
        subject="Admission",
        predicate="is",
        value="free",
        scope=SubjectScope.WHOLE_VENUE,
        scope_text=None,
    )
    accepted, reason = _gate(candidate, source)
    assert reason == "accepted"
    assert accepted is not None
    assert accepted.subject_scope is SubjectScope.WHOLE_VENUE


def test_special_exhibition_ticket_claim_keeps_narrow_scope() -> None:
    sentence = "Tickets are required for special exhibitions."
    source = _page_source(
        "<title>Admission - Alpha Zoo</title><main><h1>Admission</h1>"
        f"<h2>Tickets</h2><p>{sentence}</p></main>"
    )
    candidate = _page_candidate(
        source,
        sentence,
        kind=OfficialClaimKind.TICKET_REQUIRED,
        subject="Tickets",
        predicate="are required for",
        value="required",
        scope=SubjectScope.EXHIBITION,
        scope_text="special exhibitions",
    )
    accepted, reason = _gate(candidate, source)
    assert reason == "accepted"
    assert accepted is not None
    assert accepted.scope_text == "special exhibitions"


def test_another_named_entity_cannot_inherit_first_party_page_subject() -> None:
    sentence = "Beta Zoo tickets are required for special exhibitions."
    source = _page_source(
        "<title>Admission - Alpha Zoo</title><main><h1>Admission</h1>"
        f"<h2>Tickets</h2><p>{sentence}</p></main>"
    )
    candidate = _page_candidate(
        source,
        sentence,
        kind=OfficialClaimKind.TICKET_REQUIRED,
        subject="Beta Zoo",
        predicate="tickets are required for",
        value="required",
        scope=SubjectScope.EXHIBITION,
        scope_text="special exhibitions",
    )
    assert _gate(candidate, source)[1] == "subject_scope_not_bound"


def test_task_place_name_alone_cannot_supply_missing_page_subject() -> None:
    sentence = "Tickets are not required for permanent exhibitions."
    source = _page_source(
        "<title>Admission information</title><main><h1>Admission</h1>"
        f"<h2>Tickets</h2><p>{sentence}</p></main>"
    )
    candidate = _page_candidate(
        source,
        sentence,
        kind=OfficialClaimKind.TICKET_NOT_REQUIRED,
        subject="Tickets",
        predicate="are not required for",
        value="not required",
        scope=SubjectScope.EXHIBITION,
        scope_text="permanent exhibitions",
    )
    assert _gate(candidate, source)[1] == "subject_scope_not_bound"


def test_source_dated_closure_without_old_positive_keyword_is_accepted() -> None:
    source = _source("Alpha Zoo will not open on 25 December 2026.")
    accepted, reason = _gate(_candidate(source), source)
    assert reason == "accepted"
    assert accepted is not None
    assert accepted.temporal_basis is TemporalBasis.EXPLICIT_DATE_OR_RANGE


@pytest.mark.parametrize(
    ("text", "value"),
    [
        ("Alpha Zoo entry is complimentary.", "complimentary"),
        ("Alpha Zoo has FREE general entry.", "FREE general entry"),
    ],
)
def test_semantic_free_admission_is_not_blocked_by_a_keyword_gate(text, value) -> None:
    source = _source(text)
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.ADMISSION_TICKET,
        kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
        value=value,
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    )
    accepted, reason = _gate(candidate, source)
    assert reason == "accepted"
    assert accepted.value_text == value
    assert accepted.applicable_start_date is None


def test_short_source_predicate_does_not_need_to_contain_claim_value() -> None:
    source = _source("Alpha Zoo has FREE general entry.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.ADMISSION_TICKET,
        kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
        value="FREE general entry",
        predicate="has",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    )
    accepted, reason = _gate(candidate, source)
    assert reason == "accepted"
    assert accepted is not None
    assert accepted.predicate_text == "has"
    assert accepted.value_text == "FREE general entry"


def test_source_supported_no_ticket_claim_is_distinct_from_no_reservation() -> None:
    source = _source("Alpha Zoo tickets are not required for general admission.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.ADMISSION_TICKET,
        kind=OfficialClaimKind.TICKET_NOT_REQUIRED,
        value="tickets are not required",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    )
    accepted, reason = _gate(candidate, source)
    assert reason == "accepted"
    assert accepted is not None
    assert accepted.claim_kind is OfficialClaimKind.TICKET_NOT_REQUIRED
    assert (
        _gate(
            candidate.model_copy(update={"claim_kind": OfficialClaimKind.RESERVATION_NOT_REQUIRED}),
            source,
        )[1]
        == "claim_kind_mismatch"
    )


def test_permanent_exhibition_no_ticket_claim_keeps_source_scope() -> None:
    source = _source("Alpha Zoo permanent exhibitions do not require tickets.")
    task = _task(OfficialInformationNeed.ADMISSION_TICKET).model_copy(
        update={
            "requested_facets": (RequestedFacet.TICKET_REQUIREMENT,),
            "requested_subject_scope": SubjectScope.EXHIBITION,
            "requested_scope_text": "permanent exhibitions",
        }
    )
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.ADMISSION_TICKET,
        kind=OfficialClaimKind.TICKET_NOT_REQUIRED,
        value="do not require tickets",
        scope=SubjectScope.EXHIBITION,
        scope_text="permanent exhibitions",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    )
    accepted, reason = _gate(candidate, source, task=task)
    assert reason == "accepted"
    assert accepted is not None
    assert accepted.subject_scope is SubjectScope.EXHIBITION
    assert accepted.scope_text == "permanent exhibitions"


@pytest.mark.parametrize(
    "text",
    [
        "Alpha Zoo visitors must book in advance.",
        "Alpha Zoo pre-booking is essential.",
    ],
)
def test_semantic_mandatory_booking_is_grounded_without_required_keyword(text) -> None:
    source = _source(text)
    value = text.split("Alpha Zoo ", 1)[1].rstrip(".")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.RESERVATION_REQUIREMENT,
        kind=OfficialClaimKind.RESERVATION_REQUIRED,
        value=value,
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    )
    assert _gate(candidate, source)[1] == "accepted"


def test_explicit_optional_booking_cannot_be_accepted_as_required() -> None:
    source = _source("Alpha Zoo booking is recommended but not required.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.RESERVATION_REQUIREMENT,
        kind=OfficialClaimKind.RESERVATION_REQUIRED,
        value="booking is recommended but not required",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    )
    assert _gate(candidate, source)[1] == "direct_predicate_contradiction"


def test_optional_booking_is_not_mandatory_booking() -> None:
    source = _source("Alpha Zoo booking is optional.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.RESERVATION_REQUIREMENT,
        kind=OfficialClaimKind.RESERVATION_REQUIRED,
        value="booking is optional",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    )
    assert _gate(candidate, source)[1] == "direct_predicate_contradiction"


def test_not_optional_booking_is_not_rejected_by_the_narrow_guard() -> None:
    source = _source("Alpha Zoo booking is not optional.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.RESERVATION_REQUIREMENT,
        kind=OfficialClaimKind.RESERVATION_REQUIRED,
        value="booking is not optional",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    )
    assert _gate(candidate, source)[1] == "accepted"


def test_daily_and_special_hours_accept_source_grounded_12_hour_times() -> None:
    regular = _source("Alpha Zoo opens daily from 9am to 5pm.")
    regular_candidate = _candidate(
        regular,
        need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        kind=OfficialClaimKind.REGULAR_HOURS,
        value="9am to 5pm",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
        time_text="9am to 5pm",
        schedule_scope=HoursScheduleScope.DAILY,
        schedule_text="daily",
        opens_at=time(9),
        closes_at=time(17),
    )
    assert _gate(regular_candidate, regular)[1] == "accepted"
    special = _source("Alpha Zoo opens on 25 December 2026 from 9:30am to 2pm.")
    special_candidate = _candidate(
        special,
        need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        kind=OfficialClaimKind.SPECIAL_HOURS,
        value="9:30am to 2pm",
        time_text="9:30am to 2pm",
        opens_at=time(9, 30),
        closes_at=time(14),
    )
    assert _gate(special_candidate, special)[1] == "accepted"


def test_page_heading_and_nearby_body_can_bind_a_whole_venue() -> None:
    source = _source("Alpha Zoo\nAdmission\nEntry is complimentary.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.ADMISSION_TICKET,
        kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
        value="complimentary",
        predicate="Entry is complimentary",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    )
    assert _gate(candidate, source)[1] == "accepted"


def test_other_venue_and_prefix_subentity_are_not_whole_venue() -> None:
    other = _source("Alpha Zoo is open. Sky Safari will not open on 25 December 2026.")
    assert (
        _gate(_candidate(other, predicate="Sky Safari will not open on 25 December 2026"), other)[1]
        == "subject_scope_not_bound"
    )
    shop = _source("Alpha Zoo Shop will not open on 25 December 2026.")
    assert (
        _gate(_candidate(shop, predicate="will not open on 25 December 2026"), shop)[1]
        == "subject_scope_not_bound"
    )


def test_subentity_scope_requires_source_faithful_scope_text() -> None:
    source = _source("Alpha Zoo special exhibition ticket costs AUD 20.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.ADMISSION_TICKET,
        kind=OfficialClaimKind.PAID_ADMISSION,
        value="AUD 20",
        subject="Alpha Zoo special exhibition",
        predicate="ticket costs AUD 20",
        scope=SubjectScope.EXHIBITION,
        scope_text="special exhibition",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
        amount_text="AUD 20",
        amount="20",
        currency="AUD",
    )
    assert _gate(candidate, source)[1] == "accepted"
    assert (
        _gate(candidate.model_copy(update={"scope_text": "main venue"}), source)[1]
        == "source_span_not_in_excerpt"
    )


def test_unknown_subject_scope_cannot_be_promoted_to_venue_fact() -> None:
    source = _source("Alpha Zoo admission is complimentary.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.ADMISSION_TICKET,
        kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
        value="complimentary",
        scope=SubjectScope.UNKNOWN,
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
    )
    assert _gate(candidate, source)[1] == "subject_scope_not_bound"


def test_task_date_and_unsupported_source_fields_are_rejected() -> None:
    source = _source("Alpha Zoo entry is complimentary.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.ADMISSION_TICKET,
        kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
        value="complimentary",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=DAY,
        end=DAY,
    )
    assert _gate(candidate, source)[1] == "unsupported_date_scope"
    assert (
        _gate(candidate.model_copy(update={"amount": "25"}), source)[1] == "unsupported_price_field"
    )
    assert (
        _gate(candidate.model_copy(update={"updated_at_text": "Updated 25 December 2026"}), source)[
            1
        ]
        == "source_span_not_in_excerpt"
    )


def test_wrong_source_key_excerpt_url_and_authority_are_rejected() -> None:
    source = _source("Alpha Zoo will not open on 25 December 2026.")
    candidate = _candidate(source)
    assert (
        _gate(candidate.model_copy(update={"source_key": "invented"}), source)[1]
        == "supporting_excerpt_not_in_source"
    )
    assert (
        _gate(candidate.model_copy(update={"supporting_excerpt": "Invented excerpt"}), source)[1]
        == "supporting_excerpt_not_in_source"
    )
    assert (
        _gate(
            candidate.model_copy(update={"source_url": "https://evil.example.net/claim"}), source
        )[1]
        == "unobserved_source_url"
    )
    assert (
        _gate(candidate, source, place=_place(website="https://other.example.org"))[1]
        == "authority_not_bound_to_place"
    )


def test_wrong_fetched_final_url_and_redirect_binding_are_rejected() -> None:
    source = _source(
        "Alpha Zoo will not open on 25 December 2026.",
        kind=SourceKind.FETCHED_HTML,
        final=URL,
    )
    candidate = _candidate(source)
    assert (
        _gate(
            candidate.model_copy(update={"final_url": "https://alpha.example.org/other"}), source
        )[1]
        == "supporting_excerpt_not_in_source"
    )
    assert _gate(candidate, source)[1] == "accepted"
    redirected = _source(
        source.text,
        kind=SourceKind.FETCHED_HTML,
        final="https://evil.example.net/final",
        redirects=(URL,),
    )
    assert _gate(_candidate(redirected), redirected)[1] == "unauthorized_source_or_redirect"


def test_unsupported_date_time_amount_and_metadata_cannot_pass() -> None:
    source = _source("Alpha Zoo opens on 25 December 2026 from 9am to 5pm.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        kind=OfficialClaimKind.SPECIAL_HOURS,
        value="9am to 5pm",
        time_text="9am to 5pm",
        opens_at=time(10),
        closes_at=time(17),
    )
    assert _gate(candidate, source)[1] == "time_not_directly_supported"
    assert (
        _gate(candidate.model_copy(update={"opens_at": time(9), "date_text": "Christmas"}), source)[
            1
        ]
        == "source_span_not_in_excerpt"
    )


def test_source_supported_explicit_range_is_accepted() -> None:
    source = _source("Alpha Zoo will not open from 15–17 September 2026.")
    candidate = _candidate(
        source,
        value="will not open",
        date_text="15–17 September 2026",
        start=date(2026, 9, 15),
        end=date(2026, 9, 17),
    )
    task = _task().model_copy(
        update={
            "applicable_start_date": date(2026, 9, 15),
            "applicable_end_date": date(2026, 9, 17),
        }
    )
    assert _gate(candidate, source, task=task)[1] == "accepted"


def test_paid_amount_and_currency_must_be_present_in_source_span() -> None:
    source = _source("Alpha Zoo admission costs AUD 20.")
    candidate = _candidate(
        source,
        need=OfficialInformationNeed.ADMISSION_TICKET,
        kind=OfficialClaimKind.PAID_ADMISSION,
        value="AUD 20",
        temporal=TemporalBasis.CURRENT_GENERAL_POLICY,
        date_text=None,
        start=None,
        end=None,
        amount_text="AUD 20",
        amount="25",
        currency="AUD",
    )
    assert _gate(candidate, source)[1] == "amount_not_directly_supported"
    candidate = candidate.model_copy(update={"amount": "20", "currency": "USD"})
    assert _gate(candidate, source)[1] == "currency_not_directly_supported"
