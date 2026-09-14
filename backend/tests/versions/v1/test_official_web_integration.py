"""Offline V1-B Phase 3 orchestration and planner boundary checks."""

import asyncio
from dataclasses import replace
from datetime import UTC, date, datetime
from uuid import UUID

import pytest

from backend.app.evidence.effective_models import OperationalDayStatus
from backend.app.evidence.models import EvidenceAvailability, PlaceCandidate, PlaceEvidence
from backend.app.evidence.official_models import (
    EvidenceReasonerAssessment,
    OfficialClaimCandidate,
    OfficialClaimKind,
    OfficialCurrentEvidence,
    OfficialGapOutcome,
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
from backend.app.integrations.web.models import WebSearchHit, WebSearchObservation
from backend.app.integrations.web.page_models import PageFetchResult, PageFetchStatus
from backend.app.observability.run_trace import NullRunTracer
from backend.app.runtime.budget import ToolBudget, ToolBudgetKey, ToolBudgetLimits
from backend.app.runtime.cache import RequestCache
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.schemas.planning import SystemVersion
from backend.app.schemas.request import TravelRequest, TravelRequirements
from backend.app.services.official_web_grounding import OfficialWebGroundingService
from backend.app.services.official_web_integration import OfficialWebIntegrationService
from backend.app.services.web_evidence_acquisition import WebEvidenceAcquisitionService
from backend.app.versions.v1.official_planner import build_official_planner_evidence
from backend.app.versions.v1.official_web import OfficialWebProjection
from backend.app.versions.v1.runner import run_v1
from backend.tests.versions.v0.fakes import FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    make_extraction,
    make_itinerary,
)

DAY = date(2026, 12, 25)
TEXT = "Alpha Zoo offers free general admission."
URL = "https://alpha.example.org/admission"


class RecordingTracer(NullRunTracer):
    def __init__(self) -> None:
        super().__init__(UUID("00000000-0000-0000-0000-000000000031"))
        self.events: list[tuple[str, object | None]] = []

    def event(self, event_type: str, payload: object | None = None) -> None:
        self.events.append((event_type, payload))


class FakeWeb:
    cache_identity = "phase3-offline"

    def __init__(self, *, failure: bool = False, no_sources: bool = False) -> None:
        self.calls = []
        self.failure = failure
        self.no_sources = no_sources

    async def search(self, request):
        self.calls.append(request)
        if self.failure:
            raise RuntimeError("offline provider failure")
        if self.no_sources:
            return WebSearchObservation(provider_status="completed")
        return WebSearchObservation(
            provider_status="completed",
            hits=(
                WebSearchHit(
                    url=URL,
                    source_domain="alpha.example.org",
                    title="Alpha Zoo admission",
                    snippet=TEXT,
                    action_index=0,
                    result_index=0,
                    allowed_domain=True,
                ),
            ),
        )


class FakeReasoner:
    def __init__(self, *, reject: bool = False, empty: bool = False) -> None:
        self.calls = []
        self.reject = reject
        self.empty = empty

    async def reason(self, task, sources, baseline):
        self.calls.append(task.task_id)
        if task.information_need.value != "admission_ticket" or self.empty:
            return ()
        source = sources[0]
        candidate = OfficialClaimCandidate(
            source_key=source.source_key,
            place_id=task.place_id,
            place_name=task.place_name,
            information_need=task.information_need,
            claim_kind=OfficialClaimKind.FREE_GENERAL_ADMISSION,
            value_text="unsupported free admission" if self.reject else "free general admission",
            source_kind=source.source_kind,
            source_url=source.source_url,
            final_url=source.final_url,
            supporting_excerpt=TEXT,
            subject_scope=SubjectScope.WHOLE_VENUE,
            subject_text="Alpha Zoo",
            predicate_text="offers",
            temporal_basis=TemporalBasis.CURRENT_GENERAL_POLICY,
        )
        return (
            EvidenceReasonerAssessment(
                relevant=True,
                supports_information_need=True,
                candidate=candidate,
            ),
        )


class FakePage:
    def __init__(self, *, failure: bool = False) -> None:
        self.calls = []
        self.failure = failure

    async def fetch(self, request):
        self.calls.append(request)
        if self.failure:
            raise RuntimeError("offline page failure")
        return PageFetchResult(
            task_id=request.task_id,
            observed_url=request.observed_url,
            status=PageFetchStatus.INACCESSIBLE,
            reason="offline fixture",
        )


def _projection() -> OfficialWebProjection:
    candidate = PlaceCandidate(
        place_id="alpha",
        name="Alpha Zoo",
        latitude=-33.8,
        longitude=151.2,
        business_status="OPERATIONAL",
        source_query="Sydney zoos",
        category="zoo",
        provider_rank=0,
    )
    place = PlaceEvidence(
        place_id="alpha",
        name="Alpha Zoo",
        latitude=-33.8,
        longitude=151.2,
        business_status="OPERATIONAL",
        website_uri="https://alpha.example.org",
        availability=EvidenceAvailability.AVAILABLE,
        retrieved_at=datetime(2026, 12, 20, tzinfo=UTC),
        source_ref="google_places:alpha",
    )
    return OfficialWebProjection(
        candidates=[candidate],
        places=[place],
        named_place_ids=frozenset({"alpha"}),
        must_visit_place_ids=frozenset({"alpha"}),
    )


def _service(web, page=None, reasoner=None, *, web_limit=1, page_limit=1):
    budget = ToolBudget(
        ToolBudgetLimits(max_web_evidence_tasks=web_limit, max_page_fetches=page_limit)
    )
    cache = RequestCache()
    tracer = RecordingTracer()
    config = load_runtime_config().web_evidence
    page = page or FakePage()
    reasoner = reasoner or FakeReasoner()
    service = OfficialWebIntegrationService(
        acquisition=WebEvidenceAcquisitionService(
            provider=web, budget=budget, cache=cache, tracer=tracer, config=config
        ),
        grounding=OfficialWebGroundingService(
            page_retriever=page, reasoner=reasoner, budget=budget, tracer=tracer, config=config
        ),
        budget=budget,
        tracer=tracer,
    )
    return service, budget, tracer


def _run(service):
    return asyncio.run(
        service.run(
            request=TravelRequest(request_text="How much is Alpha Zoo admission?"),
            requirements=TravelRequirements(destination="Sydney", start_date=DAY, end_date=DAY),
            projection=_projection(),
        )
    )


def test_accepted_claim_is_resolved_and_cache_replay_spends_no_new_web_task() -> None:
    web = FakeWeb()
    page = FakePage()
    service, budget, tracer = _service(web, page)
    first = _run(service)
    second = _run(service)
    planner = build_official_planner_evidence(first)
    assert len(web.calls) == 1
    assert budget.summary()[ToolBudgetKey.WEB_EVIDENCE_TASKS.value]["used"] == 1
    assert first.acquisition_outcomes[0].status is WebTaskStatus.COMPLETED_WITH_SOURCES
    assert second.acquisition_outcomes[0].cache_hit is True
    assert first.gap_outcomes[0].status is OfficialGapStatus.AVAILABLE
    assert len(first.accepted_evidence) == 1
    assert first.accepted_evidence[0].claim_kind is OfficialClaimKind.FREE_GENERAL_ADMISSION
    assert planner[0]["accepted_effective_facts"][0]["value_text"] == "free general admission"
    assert all("snippet" not in str(item) for item in planner)
    assert page.calls == []
    assert any(name == "official_effective_place_resolved" for name, _ in tracer.events)
    completed = [
        payload for name, payload in tracer.events if name == "official_web_integration_completed"
    ]
    assert completed[0]["web_budget_before"]["used"] == 0
    assert completed[0]["web_budget_after"]["used"] == 1
    assert completed[1]["web_budget_before"]["used"] == 1
    assert completed[1]["web_budget_after"]["used"] == 1


def test_zero_justified_tasks_spend_no_budget_and_add_no_web_fact() -> None:
    web = FakeWeb()
    page = FakePage()
    reasoner = FakeReasoner()
    service, budget, tracer = _service(web, page, reasoner)
    result = asyncio.run(
        service.run(
            request=TravelRequest(request_text="Visit Alpha Zoo during my Sydney trip."),
            requirements=TravelRequirements(destination="Sydney", start_date=DAY, end_date=DAY),
            projection=_projection(),
        )
    )
    planner = build_official_planner_evidence(result)
    assert result.tasks == result.information_gaps == result.accepted_evidence == ()
    assert web.calls == page.calls == reasoner.calls == []
    assert budget.summary()[ToolBudgetKey.WEB_EVIDENCE_TASKS.value]["used"] == 0
    assert budget.summary()[ToolBudgetKey.PAGE_FETCHES.value]["used"] == 0
    assert planner[0]["tasks"] == []
    assert planner[0]["accepted_effective_facts"] == []
    assert any(
        name == "official_gap_assessed" and payload["decision"] == "no_task"
        for name, payload in tracer.events
    )


def test_projected_opening_date_conflict_reaches_risk_task_and_trace() -> None:
    web = FakeWeb(no_sources=True)
    service, budget, tracer = _service(web)
    result = asyncio.run(
        service.run(
            request=TravelRequest(request_text="Visit Alpha Zoo during my Sydney trip."),
            requirements=TravelRequirements(destination="Sydney", start_date=DAY, end_date=DAY),
            projection=replace(_projection(), opening_date_conflicts={"alpha": (DAY,)}),
        )
    )
    assert len(result.tasks) == len(web.calls) == 1
    assert result.tasks[0].priority_group == 3
    assert result.tasks[0].trigger_reasons == (WebTriggerReason.OPENING_DATE_CONFLICT,)
    assert budget.summary()[ToolBudgetKey.WEB_EVIDENCE_TASKS.value]["used"] == 1
    assert result.accepted_evidence == ()
    assert any(
        name == "web_task_prioritized" and payload["trigger_reasons"] == ["opening_date_conflict"]
        for name, payload in tracer.events
    )


@pytest.mark.parametrize(
    ("failure", "no_sources", "web_limit", "expected"),
    [
        (False, False, 0, WebTaskStatus.BUDGET_NOT_ATTEMPTED),
        (True, False, 1, WebTaskStatus.PROVIDER_FAILED),
        (False, True, 1, WebTaskStatus.COMPLETED_NO_SOURCES),
    ],
)
def test_unavailable_web_never_becomes_a_factual_negative(
    failure: bool, no_sources: bool, web_limit: int, expected: WebTaskStatus
) -> None:
    web = FakeWeb(failure=failure, no_sources=no_sources)
    service, _, _ = _service(web, web_limit=web_limit)
    result = _run(service)
    planner = build_official_planner_evidence(result)
    assert result.acquisition_outcomes[0].status is expected
    assert result.accepted_evidence == ()
    assert planner[0]["accepted_effective_facts"] == []
    assert planner[0]["tasks"][0]["acquisition_status"] == expected.value
    assert "no closure" not in str(planner).lower()
    assert len(web.calls) == (0 if web_limit == 0 else 1)


@pytest.mark.parametrize("reject", [False, True])
def test_page_failure_or_gate_rejection_never_reaches_planner(reject: bool) -> None:
    web = FakeWeb()
    page = FakePage(failure=True)
    reasoner = FakeReasoner(reject=reject, empty=not reject)
    service, _, tracer = _service(web, page, reasoner, page_limit=1)
    result = _run(service)
    planner = build_official_planner_evidence(result)
    assert result.accepted_evidence == ()
    assert planner[0]["accepted_effective_facts"] == []
    assert page.calls
    if reject:
        assert any(
            name == "official_candidate_gate" and not payload["accepted"]
            for name, payload in tracer.events
        )
    else:
        assert "page_retriever_failed" in result.gap_outcomes[0].reason_codes
    assert result.acquisition_outcomes[0].status is WebTaskStatus.COMPLETED_WITH_SOURCES


def test_integrated_graph_orders_web_after_routes_and_before_generation() -> None:
    llm = FakeStructuredLLMClient([make_extraction(), make_itinerary()])
    tracer = RecordingTracer()
    web = FakeWeb(no_sources=True)
    page = FakePage()
    reasoner = FakeReasoner()
    result = asyncio.run(
        run_v1(
            TravelRequest(request_text="Plan two days in Sydney."),
            llm,
            FakePlacesProvider(),
            FakeWeatherProvider(),
            FakeRoutesProvider(),
            reference_date=date(2026, 9, 11),
            tracer=tracer,
            web_provider=web,
            page_retriever=page,
            official_reasoner=reasoner,
        )
    )
    names = [name for name, _ in tracer.events]
    assert result.system_version is SystemVersion.V1
    assert names.index("final_poi_selection_completed") < names.index("weather_completed")
    assert names.index("weather_completed") < names.index("route_matrix_completed")
    assert names.index("route_matrix_completed") < names.index("official_web_projection_completed")
    assert names.index("official_web_integration_completed") < names.index("generation_started")
    completed = next(
        payload for name, payload in tracer.events if name == "official_web_integration_completed"
    )
    assert completed["gap_count"] == 0
    assert completed["task_count"] == 0
    assert completed["web_budget_after"]["used"] == 0
    assert completed["page_budget_after"]["used"] == 0
    planner_trace = next(
        payload for name, payload in tracer.events if name == "official_planner_evidence_prepared"
    )
    assert len(planner_trace["places"]) == 6
    assert all(item["accepted_facts"] == [] for item in planner_trace["places"])
    prompt = llm.calls[-1].user_prompt
    assert "<official_current_evidence>" in prompt
    assert '"acquisition_status": "completed_no_sources"' not in prompt
    assert '"rating"' not in prompt
    assert '"ExperienceProfile"' not in prompt
    assert '"reviews"' not in prompt
    assert web.calls == page.calls == reasoner.calls == []


def _accepted(
    task: WebEvidenceTask,
    kind: OfficialClaimKind,
    source_ref: str,
    *,
    scope: SubjectScope = SubjectScope.WHOLE_VENUE,
    scope_text: str | None = None,
    dated: bool = False,
    amount: str | None = None,
) -> OfficialCurrentEvidence:
    return OfficialCurrentEvidence(
        place_id="alpha",
        place_name="Alpha Zoo",
        information_need=task.information_need,
        claim_kind=kind,
        value_text=kind.value,
        source_kind=SourceKind.FETCHED_HTML,
        source_url=f"https://alpha.example.org/{source_ref}",
        supporting_excerpt=f"Alpha Zoo {kind.value}",
        subject_scope=scope,
        scope_text=scope_text,
        temporal_basis=(
            TemporalBasis.EXPLICIT_DATE_OR_RANGE if dated else TemporalBasis.CURRENT_GENERAL_POLICY
        ),
        applicable_start_date=DAY if dated else None,
        applicable_end_date=DAY if dated else None,
        amount=amount,
        currency="AUD" if amount else None,
        authority_basis="places_first_party_website",
        retrieved_at=datetime(2026, 12, 20, tzinfo=UTC),
        source_ref=source_ref,
    )


@pytest.mark.parametrize("conflict", [False, True])
def test_cross_task_resolver_preserves_date_scope_facet_and_conflict(conflict: bool) -> None:
    def task(
        task_id: str,
        need: OfficialInformationNeed,
        facets: tuple[RequestedFacet, ...] = (),
        scope: SubjectScope = SubjectScope.WHOLE_VENUE,
        scope_text: str | None = None,
    ) -> WebEvidenceTask:
        return WebEvidenceTask(
            task_id=task_id,
            place_id="alpha",
            place_name="Alpha Zoo",
            information_need=need,
            requested_facets=facets,
            requested_subject_scope=scope,
            requested_scope_text=scope_text,
            applicable_start_date=DAY,
            applicable_end_date=DAY,
            allowed_domains=("alpha.example.org",),
            trigger_reasons=(WebTriggerReason.RESIDUAL_MISSING,),
            priority_group=1,
            shortlist_index=0,
        )

    general = task(
        "general",
        OfficialInformationNeed.ADMISSION_TICKET,
        (RequestedFacet.GENERAL_ADMISSION_POLICY,),
    )
    exhibition = task(
        "exhibition",
        OfficialInformationNeed.ADMISSION_TICKET,
        (RequestedFacet.TICKET_REQUIREMENT,),
        SubjectScope.EXHIBITION,
        "permanent exhibitions",
    )
    closure = task("closure", OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION)
    tasks = [general, exhibition, closure]
    accepted = {
        "general": _accepted(general, OfficialClaimKind.FREE_GENERAL_ADMISSION, "official:free"),
        "exhibition": _accepted(
            exhibition,
            OfficialClaimKind.TICKET_NOT_REQUIRED,
            "official:ticket",
            scope=SubjectScope.EXHIBITION,
            scope_text="permanent exhibitions",
        ),
        "closure": _accepted(
            closure, OfficialClaimKind.MAINTENANCE_CLOSURE, "official:closure", dated=True
        ),
    }
    if conflict:
        paid = task(
            "paid", OfficialInformationNeed.ADMISSION_TICKET, (RequestedFacet.ADMISSION_FEE,)
        )
        tasks.append(paid)
        accepted["paid"] = _accepted(
            paid, OfficialClaimKind.PAID_ADMISSION, "official:paid", amount="20"
        )

    class Acquisition:
        def plan_tasks(self, request, requirements, shortlist, places, **kwargs):
            return tasks, []

        async def acquire(self, planned):
            return [
                WebTaskOutcome(task=item, status=WebTaskStatus.COMPLETED_WITH_SOURCES)
                for item in planned
            ]

    class Grounding:
        async def ground(self, outcome, place):
            fact = accepted[outcome.task.task_id]
            return OfficialGapOutcome(
                task_id=outcome.task.task_id,
                place_id=place.place_id,
                information_need=outcome.task.information_need,
                status=OfficialGapStatus.AVAILABLE,
                accepted_evidence=(fact,),
                meaningful_evidence=(fact,),
            )

    result = asyncio.run(
        OfficialWebIntegrationService(
            acquisition=Acquisition(),
            grounding=Grounding(),
            budget=ToolBudget(),
            tracer=RecordingTracer(),
        ).run(
            request=TravelRequest(request_text="Alpha Zoo admission and closure."),
            requirements=TravelRequirements(destination="Sydney", start_date=DAY, end_date=DAY),
            projection=_projection(),
        )
    )
    planner = build_official_planner_evidence(result)[0]
    assert (
        result.effective_places[0].operational_days[0].status
        is OperationalDayStatus.CONFIRMED_DATE_CLOSED
    )
    assert any(
        item["requested_facet"] == "ticket_requirement"
        and item["requested_subject_scope"] == "exhibition"
        and item["status"] == "available"
        for task_item in planner["tasks"]
        for item in task_item["facet_statuses"]
    )
    assert any(
        item["value_kind"] == "maintenance_closure" for item in planner["accepted_effective_facts"]
    )
    if conflict:
        assert set(planner["unresolved_conflict_source_refs"]) == {"official:free", "official:paid"}
        assert not any(
            item["value_kind"] in {"free_general_admission", "paid_admission"}
            for item in planner["accepted_effective_facts"]
        )
        assert any(item["status"] == "partial" for item in planner["need_statuses"])
    else:
        assert planner["unresolved_conflict_source_refs"] == []
        assert any(
            item["value_kind"] == "free_general_admission"
            for item in planner["accepted_effective_facts"]
        )
