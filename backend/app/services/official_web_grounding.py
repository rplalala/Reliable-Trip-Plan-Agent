"""Bounded Phase 2 grounding after one completed Phase 1 Web task."""

from datetime import UTC, datetime
from urllib.parse import urlsplit

from backend.app.evidence.models import PlaceEvidence
from backend.app.evidence.official_models import (
    EvidenceSourceBlock,
    OfficialCurrentEvidence,
    OfficialGapOutcome,
    OfficialGapStatus,
    SourceKind,
)
from backend.app.evidence.web_models import WebTaskOutcome, WebTaskStatus
from backend.app.integrations.web.extraction_protocols import OfficialEvidenceReasoner
from backend.app.integrations.web.page_models import PageFetchRequest, PageFetchStatus
from backend.app.integrations.web.protocols import PageRetriever
from backend.app.observability.run_trace import RunTracer
from backend.app.policies.official_evidence_gate import accept_official_candidate
from backend.app.policies.official_evidence_resolver import resolve_effective_evidence
from backend.app.policies.official_web import authorized_domains, normalize_phrase
from backend.app.runtime.budget import ToolBudget, ToolBudgetExceededError, ToolBudgetKey
from backend.app.runtime.config_models import WebEvidenceConfig

_NON_HTML_EXTENSIONS = (".pdf", ".jpg", ".jpeg", ".png", ".gif", ".webp", ".zip", ".docx", ".mp4")
_NEED_WORDS = {
    "current_operational_status": ("open", "closed", "status"),
    "date_specific_operational_exception": ("closure", "closed", "maintenance", "reopen", "hours"),
    "special_date_hours": ("hours", "open", "holiday"),
    "admission_ticket": ("admission", "ticket", "entry"),
    "reservation_requirement": ("reservation", "booking", "book"),
}


def _eligible_targets(
    outcome: WebTaskOutcome, place: PlaceEvidence, config: WebEvidenceConfig
) -> tuple[str, ...]:
    """Filter by authority, then rank place phrase, need word, and observed hit index."""

    observation = outcome.observation
    if observation is None:
        return ()
    authority = authorized_domains(place, outcome.task.information_need, config)
    scored: list[tuple[int, int, int, str]] = []
    seen: set[str] = set()
    for index, hit in enumerate(observation.hits):
        if not hit.allowed_domain or hit.url in seen:
            continue
        seen.add(hit.url)
        try:
            parts = urlsplit(hit.url)
            host = (parts.hostname or "").casefold()
        except ValueError:
            continue
        if parts.scheme.casefold() != "https" or parts.username or parts.password:
            continue
        if parts.path.casefold().endswith(_NON_HTML_EXTENSIONS):
            continue
        if not any(host == domain or host.endswith(f".{domain}") for domain in authority):
            continue
        text = normalize_phrase(" ".join((hit.title or "", hit.snippet or "", parts.path)))
        subject = int(f" {normalize_phrase(outcome.task.place_name)} " in f" {text} ")
        tokens = set(text.split())
        need = int(any(word in tokens for word in _NEED_WORDS[outcome.task.information_need.value]))
        scored.append((-subject, -need, index, hit.url))
    return tuple(item[3] for item in sorted(scored))


class OfficialWebGroundingService:
    """No new search; one native extraction and at most two observed-page attempts."""

    def __init__(
        self,
        *,
        page_retriever: PageRetriever,
        reasoner: OfficialEvidenceReasoner,
        budget: ToolBudget,
        tracer: RunTracer,
        config: WebEvidenceConfig,
    ) -> None:
        self._page_retriever = page_retriever
        self._reasoner = reasoner
        self._budget = budget
        self._tracer = tracer
        self._config = config

    async def ground(self, outcome: WebTaskOutcome, place: PlaceEvidence) -> OfficialGapOutcome:
        task = outcome.task
        if place.place_id != task.place_id:
            raise ValueError("Web task and Place Evidence IDs must align")
        reasons: list[str] = []
        accepted: list[OfficialCurrentEvidence] = []
        extraction_calls = 0
        page_attempts = 0

        def resolved():
            return resolve_effective_evidence(
                place,
                tuple(accepted),
                trip_start=task.applicable_start_date,
                trip_end=task.applicable_end_date,
                needs=(task.information_need,),
                requested_facets=task.requested_facets,
                requested_subject_scope=task.requested_subject_scope,
                requested_scope_text=task.requested_scope_text,
            )

        def finish(status: OfficialGapStatus, *, completed: bool = False) -> OfficialGapOutcome:
            effective = resolved()
            conflicts = effective.conflict_source_refs
            if accepted:
                need_status = effective.need_statuses[0]
                status = need_status.status
                reasons.extend(need_status.reason_codes)
            relation_by_ref: dict[str, str] = {}
            for fact in effective.facts:
                if len(fact.source_refs) == 1:
                    relation_by_ref.setdefault(fact.source_refs[0], fact.relation.value)
            meaningful = tuple(
                item
                for item in accepted
                if item.source_ref not in conflicts
                and relation_by_ref.get(item.source_ref) != "duplicate"
            )
            result = OfficialGapOutcome(
                task_id=task.task_id,
                place_id=task.place_id,
                information_need=task.information_need,
                status=status,
                accepted_evidence=tuple(accepted),
                meaningful_evidence=meaningful,
                conflict_source_refs=conflicts,
                reason_codes=tuple(dict.fromkeys(reasons)),
                page_target_attempts=page_attempts,
                extraction_calls=extraction_calls,
                bounded_check_completed=completed,
            )
            self._tracer.event(
                "official_gap_outcome",
                {
                    "task_id": task.task_id,
                    "status": result.status.value,
                    "requested_facets": [item.value for item in task.requested_facets],
                    "requested_subject_scope": task.requested_subject_scope.value,
                    "requested_scope_text": task.requested_scope_text,
                    "facet_statuses": [
                        {"facet": item.requested_facet.value, "status": item.status.value}
                        for item in effective.facet_statuses
                    ],
                    "accepted_count": len(result.accepted_evidence),
                    "meaningful_count": len(result.meaningful_evidence),
                    "conflict_count": len(result.conflict_source_refs),
                    "page_target_attempts": page_attempts,
                    "extraction_calls": extraction_calls,
                    "reasons": list(result.reason_codes),
                },
            )
            return result

        if outcome.status in {
            WebTaskStatus.NO_AUTHORIZED_DOMAIN,
            WebTaskStatus.BUDGET_NOT_ATTEMPTED,
            WebTaskStatus.PROVIDER_FAILED,
        }:
            reasons.append(outcome.status.value)
            return finish(OfficialGapStatus.UNAVAILABLE)
        observation = outcome.observation
        if observation is None or not observation.hits:
            reasons.append("no_visible_sources")
            return finish(OfficialGapStatus.UNKNOWN, completed=True)

        def complete() -> bool:
            return bool(
                accepted and resolved().need_statuses[0].status is OfficialGapStatus.AVAILABLE
            )

        async def reason_and_gate(sources: tuple[EvidenceSourceBlock, ...]) -> None:
            nonlocal extraction_calls
            if extraction_calls >= self._config.claim_extraction.max_calls_per_need:
                reasons.append("extraction_call_limit")
                return
            extraction_calls += 1
            source_kind = sources[0].source_kind.value
            source_count = len(sources)
            try:
                assessments = await self._reasoner.reason(task, sources, place)
            except Exception as exc:
                reasons.append("reasoner_failed")
                self._tracer.event(
                    "official_reasoner_completed",
                    {
                        "task_id": task.task_id,
                        "source_kind": source_kind,
                        "source_count": source_count,
                        "assessment_count": 0,
                        "proposed_claim_count": 0,
                        "status": "failure",
                    },
                )
                self._tracer.event(
                    "official_extraction_completed",
                    {
                        "task_id": task.task_id,
                        "source_kind": source_kind,
                        "source_count": source_count,
                        "candidate_count": 0,
                        "status": "failure",
                    },
                )
                self._tracer.event(
                    "official_extraction_failed",
                    {
                        "task_id": task.task_id,
                        "error_type": type(exc).__name__,
                    },
                )
                return
            if len(assessments) > self._config.claim_extraction.max_candidates_per_call:
                reasons.append("reasoner_assessment_limit")
                self._tracer.event(
                    "official_reasoner_completed",
                    {
                        "task_id": task.task_id,
                        "source_kind": source_kind,
                        "source_count": source_count,
                        "assessment_count": len(assessments),
                        "proposed_claim_count": 0,
                        "status": "failure",
                    },
                )
                self._tracer.event(
                    "official_extraction_completed",
                    {
                        "task_id": task.task_id,
                        "source_kind": source_kind,
                        "source_count": source_count,
                        "candidate_count": len(assessments),
                        "status": "failure",
                    },
                )
                return
            self._tracer.event(
                "official_reasoner_completed",
                {
                    "task_id": task.task_id,
                    "source_kind": source_kind,
                    "source_count": source_count,
                    "assessment_count": len(assessments),
                    "proposed_claim_count": sum(item.candidate is not None for item in assessments),
                    "status": "success",
                },
            )
            self._tracer.event(
                "official_extraction_completed",
                {
                    "task_id": task.task_id,
                    "source_kind": source_kind,
                    "source_count": source_count,
                    "candidate_count": sum(item.candidate is not None for item in assessments),
                    "status": "success",
                },
            )
            for assessment in assessments:
                candidate = assessment.candidate
                if candidate is None or not assessment.relevant:
                    continue
                evidence, reason = accept_official_candidate(
                    candidate,
                    task=task,
                    observation=observation,
                    sources=sources,
                    place=place,
                    config=self._config,
                    retrieved_at=datetime.now(UTC),
                )
                self._tracer.event(
                    "official_candidate_gate",
                    {
                        "task_id": task.task_id,
                        "source_url": candidate.source_url,
                        "accepted": evidence is not None,
                        "reason": reason,
                        "supports_information_need_advisory": assessment.supports_information_need,
                    },
                )
                if evidence is None:
                    reasons.append(reason)
                elif evidence.source_ref not in {item.source_ref for item in accepted}:
                    accepted.append(evidence)

        native_sources = tuple(
            EvidenceSourceBlock(
                task_id=task.task_id,
                source_kind=SourceKind.NATIVE_SNIPPET,
                source_url=hit.url,
                text=hit.snippet[: self._config.claim_extraction.max_native_snippet_chars],
            )
            for hit in observation.hits
            if hit.allowed_domain and hit.snippet
        )[: self._config.claim_extraction.max_native_sources]
        if native_sources:
            await reason_and_gate(native_sources)
            if complete():
                return finish(
                    OfficialGapStatus.PARTIAL
                    if observation.partial
                    else OfficialGapStatus.AVAILABLE,
                    completed=True,
                )

        observed_urls = tuple(hit.url for hit in observation.hits)
        targets = _eligible_targets(outcome, place, self._config)[
            : self._config.page_retrieval.max_targets_per_need
        ]
        for target in targets:
            if complete():
                break
            try:
                self._budget.consume(ToolBudgetKey.PAGE_FETCHES)
            except ToolBudgetExceededError:
                reasons.append("page_budget_not_attempted")
                break
            page_attempts += 1
            try:
                result = await self._page_retriever.fetch(
                    PageFetchRequest(
                        task_id=task.task_id,
                        observed_url=target,
                        observed_urls=observed_urls,
                        allowed_domains=task.allowed_domains,
                    )
                )
            except Exception as exc:
                reasons.append("page_retriever_failed")
                self._tracer.event(
                    "official_page_failed",
                    {"task_id": task.task_id, "error_type": type(exc).__name__},
                )
                continue
            self._tracer.event(
                "official_page_attempt",
                {
                    "task_id": task.task_id,
                    "observed_url": target,
                    "status": result.status.value,
                    "final_url": result.final_url,
                    "http_request_count": result.http_request_count,
                    "reason": result.reason,
                },
            )
            if result.task_id != task.task_id or result.observed_url != target:
                reasons.append("page_binding_mismatch")
                continue
            if result.status is not PageFetchStatus.FETCHED or not result.text:
                reasons.append(f"page_{result.status.value}")
                continue
            await reason_and_gate(
                (
                    EvidenceSourceBlock(
                        task_id=task.task_id,
                        source_kind=SourceKind.FETCHED_HTML,
                        source_url=target,
                        final_url=result.final_url,
                        redirect_chain=result.redirect_chain,
                        text=result.text,
                        body_sha256=result.body_sha256,
                        page_title=result.page_title,
                        content_blocks=result.content_blocks,
                    ),
                )
            )

        if accepted:
            return finish(
                OfficialGapStatus.PARTIAL
                if observation.partial or not complete()
                else OfficialGapStatus.AVAILABLE,
                completed=True,
            )
        if "page_budget_not_attempted" in reasons or any(
            reason.startswith("page_") and reason not in {"page_fetched"} for reason in reasons
        ):
            return finish(OfficialGapStatus.UNAVAILABLE)
        return finish(OfficialGapStatus.UNKNOWN, completed=True)
