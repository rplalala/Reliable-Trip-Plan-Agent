"""Offline service checks for semantic caching and atomic Web task budgeting."""

import asyncio
from datetime import date
from uuid import UUID

from backend.app.evidence.scope_models import SubjectScope
from backend.app.evidence.web_models import (
    OfficialInformationNeed,
    RequestedFacet,
    WebEvidenceTask,
    WebTaskStatus,
    WebTriggerReason,
)
from backend.app.integrations.web.models import WebSearchHit, WebSearchObservation
from backend.app.observability.run_trace import NullRunTracer
from backend.app.runtime.budget import ToolBudget, ToolBudgetKey, ToolBudgetLimits
from backend.app.runtime.cache import RequestCache
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.services.web_evidence_acquisition import WebEvidenceAcquisitionService


class RecordingTracer(NullRunTracer):
    def __init__(self) -> None:
        super().__init__(UUID("00000000-0000-0000-0000-000000000012"))
        self.events: list[tuple[str, object | None]] = []

    def event(self, event_type: str, payload: object | None = None) -> None:
        self.events.append((event_type, payload))


class FakeWebProvider:
    def __init__(
        self, *, failure: bool = False, partial: bool = False, no_sources: bool = False
    ) -> None:
        self.calls = []
        self.failure = failure
        self.partial = partial
        self.no_sources = no_sources

    @property
    def cache_identity(self) -> str:
        return "fake-web:v1"

    async def search(self, request):
        self.calls.append(request)
        if self.failure:
            raise RuntimeError("provider unavailable")
        if self.no_sources:
            return WebSearchObservation(provider_status="completed")
        return WebSearchObservation(
            provider_status="completed",
            hits=(
                WebSearchHit(
                    url="https://a.example.org/notice",
                    source_domain="a.example.org",
                    title="Notice",
                    snippet="Maintenance notice",
                    action_index=0,
                    result_index=0,
                    allowed_domain=True,
                ),
            ),
            partial=self.partial,
        )


def _task(task_id: str, *, place_id: str = "alpha", domains=("a.example.org",)):
    return WebEvidenceTask(
        task_id=task_id,
        place_id=place_id,
        place_name="Alpha Zoo",
        information_need=OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
        applicable_start_date=date(2026, 12, 25),
        applicable_end_date=date(2026, 12, 25),
        allowed_domains=domains,
        trigger_reasons=(WebTriggerReason.PROACTIVE_CRITICAL_CURRENT,),
        priority_group=5,
        shortlist_index=0,
    )


def _service(provider, *, limit=1):
    budget = ToolBudget(ToolBudgetLimits(max_web_evidence_tasks=limit))
    tracer = RecordingTracer()
    service = WebEvidenceAcquisitionService(
        provider=provider,
        budget=budget,
        cache=RequestCache(),
        tracer=tracer,
        config=load_runtime_config().web_evidence,
    )
    return service, budget, tracer


def test_cache_identity_ignores_task_id_and_canonicalizes_domain_order() -> None:
    provider = FakeWebProvider()
    service, budget, _ = _service(provider)
    first, second = asyncio.run(
        service.acquire(
            [
                _task("trace-one", domains=("B.Example.Org", "a.example.org")),
                _task("trace-two", domains=("a.example.org", "b.example.org")),
            ]
        )
    )
    assert first.status is second.status is WebTaskStatus.COMPLETED_WITH_SOURCES
    assert first.cache_hit is False
    assert second.cache_hit is True
    assert second.task.task_id == "trace-two"
    assert len(provider.calls) == 1
    assert provider.calls[0].allowed_domains == ("a.example.org", "b.example.org")
    assert budget.summary()[ToolBudgetKey.WEB_EVIDENCE_TASKS.value]["used"] == 1


def test_facet_and_scope_isolate_cache_but_semantic_replay_reuses_budget() -> None:
    provider = FakeWebProvider()
    service, budget, _ = _service(provider, limit=3)
    base = _task("fee-one").model_copy(
        update={
            "information_need": OfficialInformationNeed.ADMISSION_TICKET,
            "requested_facets": (RequestedFacet.ADMISSION_FEE,),
        }
    )
    ticket = base.model_copy(
        update={
            "task_id": "ticket",
            "requested_facets": (RequestedFacet.TICKET_REQUIREMENT,),
        }
    )
    exhibition = ticket.model_copy(
        update={
            "task_id": "exhibition",
            "requested_subject_scope": SubjectScope.EXHIBITION,
            "requested_scope_text": "Permanent Exhibitions",
        }
    )
    replay = base.model_copy(update={"task_id": "fee-two"})
    first, second, third, fourth = asyncio.run(service.acquire([base, ticket, exhibition, replay]))
    assert [item.cache_hit for item in (first, second, third, fourth)] == [
        False,
        False,
        False,
        True,
    ]
    assert len(provider.calls) == 3
    assert provider.calls[2].requested_scope_text == "Permanent Exhibitions"
    assert budget.summary()[ToolBudgetKey.WEB_EVIDENCE_TASKS.value]["used"] == 3


def test_exhaustion_does_not_stop_traversal_or_block_later_cache_hit() -> None:
    provider = FakeWebProvider()
    service, budget, tracer = _service(provider)
    outcomes = asyncio.run(
        service.acquire(
            [
                _task("first"),
                _task("miss-after-exhaustion", place_id="beta"),
                _task("later-hit"),
                _task("another-miss", place_id="gamma"),
            ]
        )
    )
    assert [item.status for item in outcomes] == [
        WebTaskStatus.COMPLETED_WITH_SOURCES,
        WebTaskStatus.BUDGET_NOT_ATTEMPTED,
        WebTaskStatus.COMPLETED_WITH_SOURCES,
        WebTaskStatus.BUDGET_NOT_ATTEMPTED,
    ]
    assert outcomes[2].cache_hit is True
    assert len(provider.calls) == 1
    assert budget.summary()[ToolBudgetKey.WEB_EVIDENCE_TASKS.value]["used"] == 1
    assert sum(name == "web_task_skipped" for name, _ in tracer.events) == 2


def test_budget_not_attempted_is_not_cached() -> None:
    provider = FakeWebProvider()
    service, _, tracer = _service(provider, limit=0)
    first, second = asyncio.run(service.acquire([_task("one"), _task("two")]))
    assert first.status is second.status is WebTaskStatus.BUDGET_NOT_ATTEMPTED
    assert first.cache_hit is second.cache_hit is False
    assert len(provider.calls) == 0
    assert sum(name == "web_task_cache_lookup" for name, _ in tracer.events) == 2


def test_missing_domain_precedes_cache_and_budget() -> None:
    provider = FakeWebProvider()
    service, budget, tracer = _service(provider)
    outcome = asyncio.run(service.execute_task(_task("none", domains=())))
    assert outcome.status is WebTaskStatus.NO_AUTHORIZED_DOMAIN
    assert not provider.calls
    assert budget.summary()[ToolBudgetKey.WEB_EVIDENCE_TASKS.value]["used"] == 0
    assert not any(name == "web_task_cache_lookup" for name, _ in tracer.events)


def test_provider_failure_and_partial_response_are_cached() -> None:
    for provider, expected in (
        (FakeWebProvider(failure=True), WebTaskStatus.PROVIDER_FAILED),
        (FakeWebProvider(partial=True), WebTaskStatus.PARTIAL_RESPONSE),
        (FakeWebProvider(no_sources=True), WebTaskStatus.COMPLETED_NO_SOURCES),
    ):
        service, budget, _ = _service(provider)
        first, second = asyncio.run(service.acquire([_task("one"), _task("two")]))
        assert first.status is second.status is expected
        assert second.cache_hit is True
        assert len(provider.calls) == 1
        assert budget.summary()[ToolBudgetKey.WEB_EVIDENCE_TASKS.value]["used"] == 1


def test_concurrent_distinct_cache_misses_cannot_oversubscribe_budget() -> None:
    provider = FakeWebProvider()
    service, budget, _ = _service(provider)

    async def run():
        return await asyncio.gather(
            service.execute_task(_task("alpha")),
            service.execute_task(_task("beta", place_id="beta")),
        )

    outcomes = asyncio.run(run())
    assert sorted(item.status.value for item in outcomes) == sorted(
        [
            WebTaskStatus.COMPLETED_WITH_SOURCES.value,
            WebTaskStatus.BUDGET_NOT_ATTEMPTED.value,
        ]
    )
    assert len(provider.calls) == 1
    assert budget.summary()[ToolBudgetKey.WEB_EVIDENCE_TASKS.value]["used"] == 1


def test_concurrent_same_semantic_task_dispatches_only_once() -> None:
    provider = FakeWebProvider()
    service, budget, _ = _service(provider, limit=2)

    async def run():
        return await asyncio.gather(
            service.execute_task(_task("first-trace")),
            service.execute_task(_task("second-trace")),
        )

    first, second = asyncio.run(run())
    assert first.cache_hit is False
    assert second.cache_hit is True
    assert second.task.task_id == "second-trace"
    assert len(provider.calls) == 1
    assert budget.summary()[ToolBudgetKey.WEB_EVIDENCE_TASKS.value]["used"] == 1
