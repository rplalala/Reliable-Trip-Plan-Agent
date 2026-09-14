"""Offline Phase 2 state-machine, cache-independent page budget, and outcome checks."""

import asyncio
from datetime import UTC, date, datetime
from uuid import UUID

from backend.app.evidence.models import EvidenceAvailability, PlaceEvidence
from backend.app.evidence.official_models import (
    EvidenceReasonerAssessment,
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
    WebTaskOutcome,
    WebTaskStatus,
    WebTriggerReason,
)
from backend.app.integrations.azure_foundry.evidence_reasoner import AzureFoundryEvidenceReasoner
from backend.app.integrations.web.models import WebSearchHit, WebSearchObservation
from backend.app.integrations.web.page_models import (
    PageContentBlock,
    PageFetchResult,
    PageFetchStatus,
)
from backend.app.observability.run_trace import NullRunTracer
from backend.app.runtime.budget import ToolBudget, ToolBudgetKey, ToolBudgetLimits
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.services.official_web_grounding import (
    OfficialWebGroundingService,
    _eligible_targets,
)

URL = "https://alpha.example.org/admission"
TEXT = "Alpha Zoo offers free general admission."
DAY = date(2026, 12, 25)


def _place():
    return PlaceEvidence(
        place_id="alpha",
        name="Alpha Zoo",
        latitude=-33.8,
        longitude=151.2,
        business_status="OPERATIONAL",
        availability=EvidenceAvailability.AVAILABLE,
        website_uri="https://alpha.example.org",
        source_ref="google_places:alpha",
        retrieved_at=datetime(2026, 12, 20, tzinfo=UTC),
    )


def _task(need=OfficialInformationNeed.ADMISSION_TICKET):
    return WebEvidenceTask(
        task_id="task-1",
        place_id="alpha",
        place_name="Alpha Zoo",
        information_need=need,
        applicable_start_date=DAY,
        applicable_end_date=DAY,
        allowed_domains=("alpha.example.org",),
        trigger_reasons=(WebTriggerReason.RESIDUAL_MISSING,),
        priority_group=2,
        shortlist_index=0,
    )


def _outcome(*, snippet=TEXT, urls=(URL,), need=OfficialInformationNeed.ADMISSION_TICKET):
    hits = tuple(
        WebSearchHit(
            url=url,
            source_domain="alpha.example.org",
            title=None,
            snippet=snippet,
            action_index=0,
            result_index=index,
            allowed_domain=True,
        )
        for index, url in enumerate(urls)
    )
    return WebTaskOutcome(
        task=_task(need),
        status=WebTaskStatus.COMPLETED_WITH_SOURCES,
        observation=WebSearchObservation(provider_status="completed", hits=hits),
    )


def _admission(source_kind, source_url=URL, *, final_url=None, text=TEXT):
    return OfficialClaimCandidate(
        place_id="alpha",
        place_name="Alpha Zoo",
        information_need=OfficialInformationNeed.ADMISSION_TICKET,
        claim_kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
        value_text="free general admission",
        source_kind=source_kind,
        source_url=source_url,
        final_url=final_url,
        supporting_excerpt=text,
    )


class FakeReasoner:
    def __init__(self, answer):
        self.answer = answer
        self.calls = []

    async def reason(self, task, sources, baseline):
        self.calls.append(sources)
        assessments = []
        for candidate in self.answer(sources):
            source = next(
                (
                    item
                    for item in sources
                    if item.source_url == candidate.source_url
                    and item.source_kind is candidate.source_kind
                ),
                sources[0],
            )
            excerpt = candidate.supporting_excerpt
            predicate = excerpt.split("Alpha Zoo", 1)[-1].strip().rstrip(".")
            updates = {
                "source_key": source.source_key,
                "subject_scope": SubjectScope.WHOLE_VENUE,
                "subject_text": "Alpha Zoo",
                "predicate_text": predicate,
                "temporal_basis": (
                    TemporalBasis.EXPLICIT_DATE_OR_RANGE
                    if candidate.date_text
                    else TemporalBasis.CURRENT_GENERAL_POLICY
                    if candidate.claim_kind
                    in {
                        OfficialClaimKind.FREE_GENERAL_ADMISSION,
                        OfficialClaimKind.PAID_ADMISSION,
                        OfficialClaimKind.RESERVATION_NOT_REQUIRED,
                    }
                    else TemporalBasis.UNSPECIFIED
                ),
                "time_text": candidate.value_text
                if candidate.opens_at or candidate.closes_at
                else None,
                "amount_text": candidate.value_text if candidate.amount else None,
            }
            hydrated = candidate.model_copy(update=updates)
            assessments.append(
                EvidenceReasonerAssessment(
                    relevant=True,
                    supports_information_need=True,
                    candidate=hydrated,
                )
            )
        return tuple(assessments)


class FakeRetriever:
    def __init__(self, status=PageFetchStatus.FETCHED, text=TEXT):
        self.status = status
        self.text = text
        self.calls = []

    async def fetch(self, request):
        self.calls.append(request)
        return PageFetchResult(
            task_id=request.task_id,
            observed_url=request.observed_url,
            status=self.status,
            final_url=request.observed_url,
            authorized_domain="alpha.example.org",
            text=self.text if self.status is PageFetchStatus.FETCHED else None,
            body_sha256="abc" if self.status is PageFetchStatus.FETCHED else None,
            http_request_count=3,
            reason=None,
        )


class TraceCollector:
    def __init__(self):
        self.events = []

    def event(self, name, payload=None):
        self.events.append((name, payload))


def _service(reasoner, retriever, *, page_limit=6, tracer=None):
    budget = ToolBudget(ToolBudgetLimits(max_page_fetches=page_limit))
    service = OfficialWebGroundingService(
        page_retriever=retriever,
        reasoner=reasoner,
        budget=budget,
        tracer=tracer or NullRunTracer(UUID("00000000-0000-0000-0000-000000000018")),
        config=load_runtime_config().web_evidence,
    )
    return service, budget


def test_native_snippet_sufficient_stops_without_page_retrieval() -> None:
    extractor = FakeReasoner(lambda sources: (_admission(SourceKind.NATIVE_SNIPPET),))
    retriever = FakeRetriever()
    service, budget = _service(extractor, retriever)
    result = asyncio.run(service.ground(_outcome(), _place()))
    assert result.status is OfficialGapStatus.AVAILABLE
    assert "trip_date_applicability_unverified" not in result.reason_codes
    assert len(result.accepted_evidence) == len(result.meaningful_evidence) == 1
    assert result.extraction_calls == 1
    assert result.page_target_attempts == 0
    assert retriever.calls == []
    assert budget.summary()[ToolBudgetKey.PAGE_FETCHES.value]["used"] == 0


def test_related_direct_claim_is_retained_without_satisfying_requested_fee() -> None:
    text = "Alpha Zoo tickets are required."

    class RelatedReasoner:
        async def reason(self, task, sources, baseline):
            source = sources[0]
            return (
                EvidenceReasonerAssessment(
                    relevant=True,
                    supports_information_need=False,
                    candidate=OfficialClaimCandidate(
                        source_key=source.source_key,
                        place_id="alpha",
                        place_name="Alpha Zoo",
                        information_need=OfficialInformationNeed.ADMISSION_TICKET,
                        claim_kind=OfficialClaimKind.TICKET_REQUIRED,
                        value_text="tickets are required",
                        source_kind=SourceKind.NATIVE_SNIPPET,
                        source_url=URL,
                        supporting_excerpt=text,
                        subject_scope=SubjectScope.WHOLE_VENUE,
                        subject_text="Alpha Zoo",
                        predicate_text="tickets are required",
                        temporal_basis=TemporalBasis.CURRENT_GENERAL_POLICY,
                    ),
                ),
            )

    retriever = FakeRetriever()
    service, budget = _service(RelatedReasoner(), retriever, page_limit=0)
    outcome = _outcome(snippet=text).model_copy(
        update={
            "task": _task().model_copy(update={"requested_facets": (RequestedFacet.ADMISSION_FEE,)})
        }
    )
    result = asyncio.run(service.ground(outcome, _place()))
    assert result.status is OfficialGapStatus.PARTIAL
    assert len(result.accepted_evidence) == len(result.meaningful_evidence) == 1
    assert result.accepted_evidence[0].claim_kind is OfficialClaimKind.TICKET_REQUIRED
    assert "facet_scope_insufficient" in result.reason_codes
    assert retriever.calls == []
    assert budget.summary()[ToolBudgetKey.PAGE_FETCHES.value]["used"] == 0


def test_undated_reservation_policy_is_available_without_inventing_a_date() -> None:
    text = "Alpha Zoo booking is not required."
    extractor = FakeReasoner(
        lambda sources: (
            OfficialClaimCandidate(
                place_id="alpha",
                place_name="Alpha Zoo",
                information_need=OfficialInformationNeed.RESERVATION_REQUIREMENT,
                claim_kind=OfficialClaimKind.RESERVATION_NOT_REQUIRED,
                value_text="booking is not required",
                source_kind=SourceKind.NATIVE_SNIPPET,
                source_url=URL,
                supporting_excerpt=text,
            ),
        )
    )
    retriever = FakeRetriever()
    service, budget = _service(extractor, retriever)
    result = asyncio.run(
        service.ground(
            _outcome(snippet=text, need=OfficialInformationNeed.RESERVATION_REQUIREMENT),
            _place(),
        )
    )
    assert result.status is OfficialGapStatus.AVAILABLE
    assert len(result.accepted_evidence) == 1
    assert result.accepted_evidence[0].applicable_start_date is None
    assert "trip_date_applicability_unverified" not in result.reason_codes
    assert retriever.calls == []
    assert budget.summary()[ToolBudgetKey.PAGE_FETCHES.value]["used"] == 0


def test_task_date_cannot_support_undated_operational_closure() -> None:
    source_url = "https://alpha.example.org/notice.pdf"
    text = "Alpha Zoo is closed for maintenance."
    extractor = FakeReasoner(
        lambda sources: (
            OfficialClaimCandidate(
                place_id="alpha",
                place_name="Alpha Zoo",
                information_need=OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
                claim_kind=OfficialClaimKind.MAINTENANCE_CLOSURE,
                value_text="closed for maintenance",
                source_kind=SourceKind.NATIVE_SNIPPET,
                source_url=source_url,
                supporting_excerpt=text,
                applicable_start_date=DAY,
                applicable_end_date=DAY,
            ),
        )
    )
    retriever = FakeRetriever()
    service, _ = _service(extractor, retriever)
    result = asyncio.run(
        service.ground(
            _outcome(
                snippet=text,
                urls=(source_url,),
                need=OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
            ),
            _place(),
        )
    )
    assert result.status is OfficialGapStatus.UNKNOWN
    assert result.accepted_evidence == ()
    assert "unsupported_date_scope" in result.reason_codes
    assert retriever.calls == []


def test_source_dated_closure_can_cover_the_requested_date_without_page_fetch() -> None:
    text = "Alpha Zoo is closed for maintenance on 25 December 2026."
    extractor = FakeReasoner(
        lambda sources: (
            OfficialClaimCandidate(
                place_id="alpha",
                place_name="Alpha Zoo",
                information_need=OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
                claim_kind=OfficialClaimKind.MAINTENANCE_CLOSURE,
                value_text="closed for maintenance",
                source_kind=SourceKind.NATIVE_SNIPPET,
                source_url=URL,
                supporting_excerpt=text,
                date_text="25 December 2026",
                applicable_start_date=DAY,
                applicable_end_date=DAY,
            ),
        )
    )
    retriever = FakeRetriever()
    service, budget = _service(extractor, retriever)
    result = asyncio.run(
        service.ground(
            _outcome(
                snippet=text,
                need=OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
            ),
            _place(),
        )
    )
    assert result.status is OfficialGapStatus.AVAILABLE
    assert len(result.accepted_evidence) == 1
    assert result.page_target_attempts == 0
    assert budget.summary()[ToolBudgetKey.PAGE_FETCHES.value]["used"] == 0


def test_zero_candidate_extraction_emits_explicit_trace_event() -> None:
    tracer = TraceCollector()
    extractor = FakeReasoner(lambda sources: ())
    retriever = FakeRetriever(status=PageFetchStatus.BLOCKED)
    service, _ = _service(extractor, retriever, tracer=tracer)
    asyncio.run(service.ground(_outcome(), _place()))
    completions = [
        payload for name, payload in tracer.events if name == "official_extraction_completed"
    ]
    assert completions == [
        {
            "task_id": "task-1",
            "source_kind": "native_snippet",
            "source_count": 1,
            "candidate_count": 0,
            "status": "success",
        }
    ]
    reasoner_events = [
        payload for name, payload in tracer.events if name == "official_reasoner_completed"
    ]
    assert reasoner_events[0]["assessment_count"] == 0
    assert reasoner_events[0]["status"] == "success"


def test_failed_extraction_emits_failure_status_without_raw_output() -> None:
    class FailingReasoner:
        async def reason(self, task, sources, baseline):
            raise RuntimeError("provider response unavailable")

    tracer = TraceCollector()
    service, _ = _service(
        FailingReasoner(), FakeRetriever(status=PageFetchStatus.BLOCKED), tracer=tracer
    )
    asyncio.run(service.ground(_outcome(), _place()))
    completions = [
        payload for name, payload in tracer.events if name == "official_extraction_completed"
    ]
    assert completions == [
        {
            "task_id": "task-1",
            "source_kind": "native_snippet",
            "source_count": 1,
            "candidate_count": 0,
            "status": "failure",
        }
    ]
    assert "provider response unavailable" not in str(tracer.events)


def test_validation_failure_traces_bounded_field_path_and_source_identity_only() -> None:
    class InvalidReasoner:
        async def reason(self, task, sources, baseline):
            EvidenceReasonerAssessment.model_validate(
                {
                    "relevant": "untrusted raw model output",
                    "supports_information_need": False,
                    "candidate": None,
                }
            )

    tracer = TraceCollector()
    service, _ = _service(InvalidReasoner(), FakeRetriever(), tracer=tracer)
    asyncio.run(service.ground(_outcome(), _place()))
    failures = [payload for name, payload in tracer.events if name == "official_extraction_failed"]
    assert failures[0]["error_type"] == "ValidationError"
    assert failures[0]["validation_errors"] == [{"path": ["relevant"], "code": "bool_parsing"}]
    assert len(failures[0]["sources"][0]["source_key"]) == 24
    assert failures[0]["sources"][0]["source_kind"] == "native_snippet"
    assert failures[0]["sources"][0]["page_url"] == URL
    assert failures[1]["sources"][0]["source_kind"] == "fetched_html"
    assert failures[1]["sources"][0]["page_url"] == URL
    assert "untrusted raw model output" not in str(tracer.events)
    assert TEXT not in str(tracer.events)


def test_price_rejection_traces_typed_shape_without_source_prose() -> None:
    text = "Alpha Zoo admission costs AUD 0 and is free general entry."

    class PriceReasoner:
        async def reason(self, task, sources, baseline):
            source = sources[0]
            return (
                (
                    EvidenceReasonerAssessment(
                        relevant=True,
                        supports_information_need=True,
                        candidate=OfficialClaimCandidate(
                            source_key=source.source_key,
                            place_id=task.place_id,
                            place_name=task.place_name,
                            information_need=task.information_need,
                            claim_kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
                            value_text="free general entry",
                            source_kind=source.source_kind,
                            source_url=source.source_url,
                            final_url=source.final_url,
                            supporting_excerpt=text,
                            subject_scope=SubjectScope.WHOLE_VENUE,
                            subject_text="Alpha Zoo",
                            predicate_text="admission costs AUD 0 and is free general entry",
                            temporal_basis=TemporalBasis.CURRENT_GENERAL_POLICY,
                            amount="0",
                            amount_text="AUD 0",
                            currency="AUD",
                        ),
                    ),
                )
                if source.source_kind is SourceKind.NATIVE_SNIPPET
                else ()
            )

    tracer = TraceCollector()
    service, _ = _service(
        PriceReasoner(), FakeRetriever(status=PageFetchStatus.BLOCKED), tracer=tracer
    )
    task = _task().model_copy(update={"requested_facets": (RequestedFacet.ADMISSION_FEE,)})
    outcome = _outcome(snippet=text).model_copy(update={"task": task})
    result = asyncio.run(service.ground(outcome, _place()))
    rejected = [
        payload
        for name, payload in tracer.events
        if name == "official_candidate_gate" and not payload["accepted"]
    ]
    assert result.accepted_evidence == ()
    assert len(rejected) == 1
    assert rejected[0]["reason"] == "unsupported_price_field"
    assert rejected[0]["claim_kind"] == "free_general_admission"
    assert rejected[0]["requested_facets"] == ["admission_fee"]
    assert rejected[0]["price_fields_present"] == ["amount", "currency", "amount_text"]
    assert rejected[0]["price_field_invariant"] == "non_paid_claim_requires_no_price_fields"
    assert rejected[0]["amount_field_type"] == "string"
    assert rejected[0]["amount_numeric_class"] == "zero"
    assert rejected[0]["subject_text_present"] is True
    assert rejected[0]["subject_text_length"] == len("Alpha Zoo")
    assert rejected[0]["local_binding_condition"] == "bound"
    assert text not in str(tracer.events)
    assert "AUD 0" not in str(tracer.events)


def test_scope_rejection_traces_available_page_binding_structure() -> None:
    body = "Alpha Zoo Special Exhibition has FREE general entry."
    page_text = "Admission - Alpha Zoo\nTickets\n" + body

    class PageReasoner:
        async def reason(self, task, sources, baseline):
            source = sources[0]
            if source.source_kind is SourceKind.NATIVE_SNIPPET:
                return ()
            return (
                EvidenceReasonerAssessment(
                    relevant=True,
                    supports_information_need=True,
                    candidate=OfficialClaimCandidate(
                        source_key=source.source_key,
                        place_id=task.place_id,
                        place_name=task.place_name,
                        information_need=task.information_need,
                        claim_kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
                        value_text="FREE general entry",
                        source_kind=SourceKind.FETCHED_HTML,
                        source_url=URL,
                        final_url=URL,
                        supporting_excerpt=body,
                        subject_scope=SubjectScope.WHOLE_VENUE,
                        subject_text="Alpha Zoo",
                        predicate_text="has",
                        temporal_basis=TemporalBasis.CURRENT_GENERAL_POLICY,
                    ),
                ),
            )

    class StructuredRetriever(FakeRetriever):
        async def fetch(self, request):
            self.calls.append(request)
            return PageFetchResult(
                task_id=request.task_id,
                observed_url=request.observed_url,
                status=PageFetchStatus.FETCHED,
                final_url=URL,
                authorized_domain="alpha.example.org",
                text=page_text,
                body_sha256="abc",
                page_title="Admission - Alpha Zoo",
                content_blocks=(
                    PageContentBlock(text=body, section_headings=("Admission", "Tickets")),
                ),
                http_request_count=1,
            )

    tracer = TraceCollector()
    service, _ = _service(PageReasoner(), StructuredRetriever(), tracer=tracer)
    result = asyncio.run(service.ground(_outcome(snippet="Visitor information."), _place()))
    rejected = [
        payload
        for name, payload in tracer.events
        if name == "official_candidate_gate" and not payload["accepted"]
    ]
    assert result.accepted_evidence == ()
    assert len(rejected) == 1
    assert rejected[0]["reason"] == "subject_scope_not_bound"
    assert rejected[0]["claim_kind"] == "free_general_admission"
    assert rejected[0]["subject_scope"] == "whole_venue"
    assert rejected[0]["local_binding_condition"] == "whole_venue_prefix_subentity"
    assert rejected[0]["page_level_venue_subject_verified"] is True
    assert rejected[0]["page_binding_condition"] == "local_heading_or_requested_scope_mismatch"
    assert rejected[0]["page_title_available"] is True
    assert rejected[0]["main_heading_available"] is None
    assert rejected[0]["source_heading_path_available"] is True
    assert rejected[0]["heading_path_available"] is True
    assert rejected[0]["heading_path_depth"] == 2
    assert rejected[0]["local_body_block_index"] == 0
    assert rejected[0]["local_scope_metadata_available"] is True
    page_attempt = next(
        payload for name, payload in tracer.events if name == "official_page_attempt"
    )
    assert page_attempt["page_content_block_count"] == 1
    assert page_attempt["heading_path_available"] is True
    assert page_attempt["main_heading_available"] is None
    assert body not in str(tracer.events)
    assert page_text not in str(tracer.events)


def test_json_failure_traces_parser_shape_without_raw_output() -> None:
    raw_output = '{"RAW_REASONER_SECRET": "unfinished'

    class InvalidResponses:
        async def create(self, **kwargs):
            return {
                "status": "incomplete",
                "incomplete_details": {"reason": "max_output_tokens"},
                "output_text": raw_output,
                "output": [{"type": "reasoning"}, {"type": "message"}],
            }

    reasoner = AzureFoundryEvidenceReasoner(
        endpoint="https://example.test/openai/v1",
        deployment="gpt-5.6-luna",
        api_key="unused-test-value",
        config=load_runtime_config().web_evidence,
        responses_client=InvalidResponses(),
    )
    tracer = TraceCollector()
    service, _ = _service(reasoner, FakeRetriever(status=PageFetchStatus.BLOCKED), tracer=tracer)
    asyncio.run(service.ground(_outcome(), _place()))
    failures = [payload for name, payload in tracer.events if name == "official_extraction_failed"]
    assert failures[0]["error_type"] == "JSONDecodeError"
    assert failures[0]["task_id"] == "task-1"
    assert failures[0]["requested_information_need"] == "admission_ticket"
    assert failures[0]["parser_stage"] == "json.loads"
    assert failures[0]["response_item_types"] == ["reasoning", "message"]
    assert failures[0]["textual_content_existed"] is True
    assert failures[0]["textual_content_length"] == len(raw_output)
    assert failures[0]["provider_status"] == "incomplete"
    assert failures[0]["provider_finish_reason"] == "max_output_tokens"
    assert failures[0]["output_appeared_truncated"] is True
    assert failures[0]["json_error_position"] >= 0
    assert failures[0]["sources"][0]["page_url"] == URL
    assert raw_output not in str(tracer.events)
    assert "RAW_REASONER_SECRET" not in str(tracer.events)
    assert TEXT not in str(tracer.events)


def test_insufficient_native_snippet_uses_one_observed_page_and_one_budget_unit() -> None:
    extractor = FakeReasoner(
        lambda sources: (
            (
                _admission(SourceKind.FETCHED_HTML, final_url=URL)
                if sources[0].source_kind is SourceKind.FETCHED_HTML
                else None,
            )
            if sources[0].source_kind is SourceKind.FETCHED_HTML
            else ()
        )
    )
    retriever = FakeRetriever()
    service, budget = _service(extractor, retriever)
    result = asyncio.run(
        service.ground(
            _outcome(
                snippet="Alpha Zoo visitor information.",
                urls=(URL, "https://alpha.example.org/second"),
            ),
            _place(),
        )
    )
    assert result.status is OfficialGapStatus.AVAILABLE
    assert "trip_date_applicability_unverified" not in result.reason_codes
    assert result.extraction_calls == 2
    assert result.page_target_attempts == 1
    assert len(retriever.calls) == 1
    assert retriever.calls[0].observed_url == URL
    assert budget.summary()[ToolBudgetKey.PAGE_FETCHES.value]["used"] == 1
    assert len(result.meaningful_evidence) == 1


def test_unobserved_model_url_is_rejected_and_never_selected_for_fetch() -> None:
    invented = "https://evil.example.net/invented"
    extractor = FakeReasoner(
        lambda sources: (
            (_admission(SourceKind.NATIVE_SNIPPET, invented),)
            if sources[0].source_kind is SourceKind.NATIVE_SNIPPET
            else ()
        )
    )
    retriever = FakeRetriever(status=PageFetchStatus.BLOCKED)
    service, _ = _service(extractor, retriever)
    result = asyncio.run(service.ground(_outcome(), _place()))
    assert "unobserved_source_url" in result.reason_codes
    assert all(call.observed_url == URL for call in retriever.calls)
    assert all(invented not in call.observed_urls for call in retriever.calls)


def test_page_budget_exhaustion_prevents_fetch_without_changing_web_task_budget() -> None:
    extractor = FakeReasoner(lambda sources: ())
    retriever = FakeRetriever()
    service, budget = _service(extractor, retriever, page_limit=0)
    result = asyncio.run(
        service.ground(_outcome(snippet="Alpha Zoo visitor information."), _place())
    )
    assert result.status is OfficialGapStatus.UNAVAILABLE
    assert "page_budget_not_attempted" in result.reason_codes
    assert result.page_target_attempts == 0
    assert retriever.calls == []
    assert budget.summary()[ToolBudgetKey.PAGE_FETCHES.value]["used"] == 0


def test_at_most_two_target_pages_and_three_extraction_calls() -> None:
    second = "https://alpha.example.org/visit"
    third = "https://alpha.example.org/other"
    extractor = FakeReasoner(lambda sources: ())
    retriever = FakeRetriever(text="Alpha Zoo visit information.")
    service, budget = _service(extractor, retriever)
    result = asyncio.run(
        service.ground(
            _outcome(snippet="Alpha Zoo visitor information.", urls=(URL, second, third)), _place()
        )
    )
    assert result.page_target_attempts == 2
    assert result.extraction_calls == 3
    assert len(retriever.calls) == 2
    assert budget.summary()[ToolBudgetKey.PAGE_FETCHES.value]["used"] == 2


def test_target_order_is_deterministic_place_then_need_then_observed_rank() -> None:
    first = "https://alpha.example.org/first"
    second = "https://alpha.example.org/alpha-zoo-admission"
    outcome = _outcome(snippet="Generic information.", urls=(first, second))
    assert _eligible_targets(outcome, _place(), load_runtime_config().web_evidence)[0] == second


def test_proactive_no_source_is_unknown_not_confirmed_open() -> None:
    task = _task(OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION)
    outcome = WebTaskOutcome(
        task=task,
        status=WebTaskStatus.COMPLETED_NO_SOURCES,
        observation=WebSearchObservation(provider_status="completed"),
    )
    extractor = FakeReasoner(lambda sources: ())
    retriever = FakeRetriever()
    service, _ = _service(extractor, retriever)
    result = asyncio.run(service.ground(outcome, _place()))
    assert result.status is OfficialGapStatus.UNKNOWN
    assert result.accepted_evidence == ()
    assert result.bounded_check_completed is True
    assert retriever.calls == extractor.calls == []


def test_conflicting_accepted_claims_preserve_both_sources_without_winner() -> None:
    free = "Alpha Zoo offers free general admission."
    paid = "Alpha Zoo admission costs AUD 20."
    extractor = FakeReasoner(
        lambda sources: (
            _admission(SourceKind.NATIVE_SNIPPET, text=free),
            OfficialClaimCandidate(
                place_id="alpha",
                place_name="Alpha Zoo",
                information_need=OfficialInformationNeed.ADMISSION_TICKET,
                claim_kind=OfficialClaimKind.PAID_ADMISSION,
                value_text="AUD 20",
                source_kind=SourceKind.NATIVE_SNIPPET,
                source_url=URL,
                supporting_excerpt=paid,
                amount="20",
                currency="AUD",
            ),
        )
    )
    retriever = FakeRetriever()
    service, budget = _service(extractor, retriever)
    result = asyncio.run(service.ground(_outcome(snippet=f"{free} {paid}"), _place()))
    assert result.status is OfficialGapStatus.PARTIAL
    assert len(result.accepted_evidence) == 2
    assert len(result.conflict_source_refs) == 2
    assert result.meaningful_evidence == ()
    assert "conflicting_official_claims" in result.reason_codes
    assert budget.summary()[ToolBudgetKey.PAGE_FETCHES.value]["used"] == 1
