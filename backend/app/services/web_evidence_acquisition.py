"""Request-scoped Web discovery service; no claim acceptance or graph integration."""

import asyncio
import unicodedata
from dataclasses import dataclass

from backend.app.evidence.models import PlaceCandidate, PlaceEvidence
from backend.app.evidence.web_models import (
    InformationGap,
    WebEvidenceTask,
    WebTaskOutcome,
    WebTaskStatus,
)
from backend.app.integrations.web.models import WebEvidenceSearchRequest, WebSearchObservation
from backend.app.integrations.web.protocols import WebEvidenceProvider
from backend.app.observability.run_trace import RunTracer, TracePayloadMode
from backend.app.policies.official_web import (
    build_search_request,
    canonicalize_allowed_domains,
    plan_official_web_tasks,
)
from backend.app.runtime.budget import ToolBudget, ToolBudgetExceededError, ToolBudgetKey
from backend.app.runtime.cache import RequestCache
from backend.app.runtime.config_models import WebEvidenceConfig
from backend.app.schemas.request import TravelRequest, TravelRequirements


@dataclass(frozen=True)
class _CachedAcquisition:
    status: WebTaskStatus
    observation: WebSearchObservation | None = None
    error_type: str | None = None


def _semantic_cache_key(
    request: WebEvidenceSearchRequest,
    *,
    provider_identity: str,
    config: WebEvidenceConfig,
) -> tuple[object, ...]:
    """Exclude task_id and trace IDs from identity; include every acquisition input."""

    instruction = " ".join(unicodedata.normalize("NFKC", request.task_instruction).split())
    return (
        "web_evidence_task",
        request.place_id,
        request.place_name,
        request.information_need,
        request.requested_facets,
        request.requested_subject_scope,
        " ".join(
            unicodedata.normalize("NFKC", request.requested_scope_text or "").casefold().split()
        ),
        request.applicable_start_date,
        request.applicable_end_date,
        canonicalize_allowed_domains(request.allowed_domains),
        request.template_version,
        instruction,
        provider_identity,
        config.reasoning_effort,
        config.max_tool_calls,
        config.search_context_size,
    )


class WebEvidenceAcquisitionService:
    """Plan and run bounded Luna discovery tasks without promoting factual claims."""

    def __init__(
        self,
        *,
        provider: WebEvidenceProvider,
        budget: ToolBudget,
        cache: RequestCache,
        tracer: RunTracer,
        config: WebEvidenceConfig,
    ) -> None:
        self._provider = provider
        self._budget = budget
        self._cache = cache
        self._cache_lock = asyncio.Lock()
        self._tracer = tracer
        self._config = config

    def plan_tasks(
        self,
        request: TravelRequest,
        requirements: TravelRequirements,
        shortlist: list[PlaceCandidate],
        places: list[PlaceEvidence],
    ) -> tuple[list[WebEvidenceTask], list[InformationGap]]:
        tasks, gaps, assessments = plan_official_web_tasks(
            request, requirements, shortlist, places, self._config
        )
        for assessment in assessments:
            self._tracer.event("official_gap_assessed", assessment)
        for rank, task in enumerate(tasks, start=1):
            self._tracer.event(
                "web_task_prioritized",
                {
                    "task_id": task.task_id,
                    "place_id": task.place_id,
                    "information_need": task.information_need.value,
                    "requested_facets": [item.value for item in task.requested_facets],
                    "requested_subject_scope": task.requested_subject_scope.value,
                    "requested_scope_text": task.requested_scope_text,
                    "priority_group": task.priority_group,
                    "rank": rank,
                    "shortlist_index": task.shortlist_index,
                    "trigger_reasons": [item.value for item in task.trigger_reasons],
                    "allowed_domains": list(task.allowed_domains),
                },
            )
        return tasks, gaps

    async def execute_task(self, task: WebEvidenceTask) -> WebTaskOutcome:
        """Check domain, cache, then reserve budget only inside a cache miss."""

        if not task.allowed_domains:
            outcome = WebTaskOutcome(task=task, status=WebTaskStatus.NO_AUTHORIZED_DOMAIN)
            self._tracer.event(
                "web_task_skipped",
                {
                    "task_id": task.task_id,
                    "reason": outcome.status.value,
                },
            )
            return outcome
        domains = canonicalize_allowed_domains(task.allowed_domains)
        canonical_task = task.model_copy(update={"allowed_domains": domains})
        request = build_search_request(canonical_task)
        key = _semantic_cache_key(
            request,
            provider_identity=self._provider.cache_identity,
            config=self._config,
        )

        async def load() -> _CachedAcquisition:
            # Synchronous ToolBudget.consume performs check + reservation without an await.
            self._budget.consume(ToolBudgetKey.WEB_EVIDENCE_TASKS)
            try:
                observation = await self._provider.search(request)
            except Exception as exc:
                return _CachedAcquisition(
                    status=WebTaskStatus.PROVIDER_FAILED,
                    error_type=type(exc).__name__,
                )
            allowed_hits = [hit for hit in observation.hits if hit.allowed_domain]
            if observation.partial:
                status = WebTaskStatus.PARTIAL_RESPONSE
            elif allowed_hits:
                status = WebTaskStatus.COMPLETED_WITH_SOURCES
            else:
                status = WebTaskStatus.COMPLETED_NO_SOURCES
            return _CachedAcquisition(status=status, observation=observation)

        try:
            # Keep same-key misses single-flight without changing shared RequestCache.
            # Phase 1 Web tasks are sequential even if callers schedule execute_task together.
            async with self._cache_lock:
                result, cache_hit = await self._cache.get_or_create(key, load)
        except ToolBudgetExceededError:
            outcome = WebTaskOutcome(task=canonical_task, status=WebTaskStatus.BUDGET_NOT_ATTEMPTED)
            self._tracer.event(
                "web_task_cache_lookup",
                {
                    "task_id": task.task_id,
                    "cache_hit": False,
                },
            )
            self._tracer.event(
                "web_task_skipped",
                {
                    "task_id": task.task_id,
                    "reason": outcome.status.value,
                },
            )
            return outcome

        self._tracer.event(
            "web_task_cache_lookup",
            {
                "task_id": task.task_id,
                "cache_hit": cache_hit,
            },
        )
        outcome = WebTaskOutcome(
            task=canonical_task,
            status=result.status,
            cache_hit=cache_hit,
            observation=result.observation,
            error_type=result.error_type,
        )
        if result.observation is not None:
            self._tracer.event(
                "web_search_observed",
                {
                    "task_id": task.task_id,
                    "cache_hit": cache_hit,
                    "response_id": result.observation.response_id,
                    "provider_status": result.observation.provider_status,
                    "actions": [
                        {
                            "type": action.action_type.value,
                            "status": action.status,
                            "queries": list(action.queries),
                            "source_urls": list(action.source_urls),
                        }
                        for action in result.observation.actions
                    ],
                    "result_urls": [hit.url for hit in result.observation.hits],
                    "latency_ms": result.observation.latency_ms,
                    "usage": (
                        result.observation.usage.model_dump(mode="json")
                        if result.observation.usage
                        else None
                    ),
                },
            )
            self._tracer.payload(
                "tools",
                "web_search_observation",
                result.observation,
                minimum_mode=TracePayloadMode.NORMALIZED,
            )
        if result.error_type is not None:
            self._tracer.event(
                "web_search_failed",
                {
                    "task_id": task.task_id,
                    "error": result.error_type,
                },
            )
        self._tracer.event(
            "web_task_finished",
            {
                "task_id": task.task_id,
                "status": result.status.value,
                "cache_hit": cache_hit,
            },
        )
        return outcome

    async def acquire(self, tasks: list[WebEvidenceTask]) -> list[WebTaskOutcome]:
        """Continue traversal after budget exhaustion so later cache hits still work."""

        outcomes: list[WebTaskOutcome] = []
        for task in tasks:
            outcomes.append(await self.execute_task(task))
        return outcomes
