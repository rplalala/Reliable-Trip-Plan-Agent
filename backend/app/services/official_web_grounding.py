"""Bounded Phase 2 grounding after one completed Phase 1 Web task."""

import json
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from urllib.parse import urlsplit

from pydantic import ValidationError

from backend.app.evidence.models import PlaceEvidence
from backend.app.evidence.official_models import (
    EvidenceSourceBlock,
    OfficialClaimCandidate,
    OfficialCurrentEvidence,
    OfficialGapOutcome,
    OfficialGapStatus,
    SourceKind,
)
from backend.app.evidence.web_models import WebEvidenceTask, WebTaskOutcome, WebTaskStatus
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


def _safe_trace_url(url: str | None) -> str | None:
    """Retain only source URL identity, excluding query, fragment, and userinfo."""

    if url is None:
        return None
    try:
        parts = urlsplit(url)
        if parts.scheme.casefold() != "https" or not parts.hostname:
            return None
        host = parts.hostname
        port = f":{parts.port}" if parts.port is not None else ""
        return f"https://{host}{port}{parts.path}"
    except ValueError:
        return None


def _source_trace_identity(source: EvidenceSourceBlock) -> dict[str, str | None]:
    """Identify a failed source without logging its text or URL query."""

    return {
        "source_key": source.source_key,
        "source_kind": source.source_kind.value,
        "page_url": _safe_trace_url(source.final_url or source.source_url),
    }


def _candidate_trace_metadata(
    candidate: OfficialClaimCandidate,
    task: WebEvidenceTask,
    sources: tuple[EvidenceSourceBlock, ...],
    reason: str,
    binding: dict[str, object],
) -> dict[str, object]:
    """Expose typed candidate shape and available page structure without source prose."""

    source = next(
        (
            item
            for item in sources
            if item.source_key == candidate.source_key
            and item.source_url == candidate.source_url
            and item.source_kind is candidate.source_kind
        ),
        None,
    )
    text_fields = ("subject_text", "predicate_text", "value_text", "scope_text")
    price_fields = ("amount", "currency", "amount_text")

    def amount_class() -> str:
        if candidate.amount is None:
            return "absent"
        try:
            amount = Decimal(candidate.amount)
            if not amount.is_finite():
                return "nonfinite"
            if amount == 0:
                return "zero"
            return "positive" if amount > 0 else "negative"
        except InvalidOperation:
            return "unparseable"

    details: dict[str, object] = {
        "place_id": task.place_id,
        "requested_information_need": task.information_need.value,
        "requested_facets": [facet.value for facet in task.requested_facets],
        "requested_subject_scope": task.requested_subject_scope.value,
        "requested_scope_text_present": task.requested_scope_text is not None,
        "requested_scope_text_length": len(task.requested_scope_text or ""),
        "source_key": candidate.source_key,
        "source_kind": candidate.source_kind.value,
        "source_url": _safe_trace_url(candidate.source_url),
        "final_url": _safe_trace_url(candidate.final_url),
        "source_block_matched": source is not None,
        "claim_kind": candidate.claim_kind.value,
        "candidate_information_need": candidate.information_need.value,
        "temporal_basis": candidate.temporal_basis.value,
        "subject_scope": candidate.subject_scope.value,
        "schedule_scope": candidate.schedule_scope.value if candidate.schedule_scope else None,
        "supporting_excerpt_length": len(candidate.supporting_excerpt),
        "price_fields_present": [
            field for field in price_fields if getattr(candidate, field) is not None
        ],
        "price_field_invariant": (
            "non_paid_claim_requires_no_price_fields"
            if reason == "unsupported_price_field"
            else None
        ),
        "amount_field_type": "string" if candidate.amount is not None else None,
        "amount_numeric_class": amount_class(),
        "page_title_available": bool(source.page_title) if source else None,
        # The PageContentBlock contract retains paths, not heading levels or a distinct h1.
        "main_heading_available": None,
        "page_content_block_count": len(source.content_blocks) if source else None,
        "source_heading_path_available": (
            any(block.section_headings for block in source.content_blocks) if source else None
        ),
        "local_binding_condition": binding.get("local_binding_condition"),
        "page_binding_condition": binding.get("page_binding_condition"),
        "page_level_venue_subject_verified": binding.get("page_level_venue_subject_verified"),
        "local_body_block_index": binding.get("local_body_block_index"),
        "heading_path_available": binding.get("heading_path_available"),
        "heading_path_depth": binding.get("heading_path_depth"),
        "local_scope_metadata_available": binding.get("local_scope_metadata_available"),
    }
    for field in text_fields:
        value = getattr(candidate, field)
        details[f"{field}_present"] = value is not None
        details[f"{field}_length"] = len(value or "")
    for field in (
        *price_fields,
        "date_text",
        "applicable_start_date",
        "applicable_end_date",
        "updated_at",
        "updated_at_text",
        "time_text",
        "opens_at",
        "closes_at",
        "schedule_scope",
        "schedule_text",
    ):
        details[f"{field}_present"] = getattr(candidate, field) is not None
    return details


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
                validation_details: dict[str, object] = {}
                if isinstance(exc, ValidationError):
                    validation_details = {
                        "validation_errors": [
                            {
                                "path": [
                                    part
                                    if isinstance(part, int)
                                    or (
                                        isinstance(part, str)
                                        and len(part) <= 64
                                        and part.isidentifier()
                                    )
                                    else "<dynamic>"
                                    for part in error["loc"][:8]
                                ],
                                "code": error["type"],
                            }
                            for error in exc.errors(include_input=False, include_url=False)[:8]
                        ],
                        "sources": [_source_trace_identity(source) for source in sources],
                    }
                parse_details: dict[str, object] = {}
                if isinstance(exc, json.JSONDecodeError):
                    parse_details = {
                        "parser_stage": "json.loads",
                        "json_error_message": exc.msg[:120],
                        "json_error_position": exc.pos,
                        "json_error_line": exc.lineno,
                        "json_error_column": exc.colno,
                        "sources": [_source_trace_identity(source) for source in sources],
                        **getattr(exc, "_official_reasoner_parse_diagnostics", {}),
                    }
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
                        "place_id": task.place_id,
                        "requested_information_need": task.information_need.value,
                        "requested_facets": [item.value for item in task.requested_facets],
                        "error_type": type(exc).__name__,
                        **validation_details,
                        **parse_details,
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
                binding_diagnostics: dict[str, object] = {}
                evidence, reason = accept_official_candidate(
                    candidate,
                    task=task,
                    observation=observation,
                    sources=sources,
                    place=place,
                    config=self._config,
                    retrieved_at=datetime.now(UTC),
                    diagnostics=binding_diagnostics,
                )
                try:
                    candidate_metadata = _candidate_trace_metadata(
                        candidate, task, sources, reason, binding_diagnostics
                    )
                except Exception:
                    candidate_metadata = {"diagnostic_status": "unavailable"}
                self._tracer.event(
                    "official_candidate_gate",
                    {
                        "task_id": task.task_id,
                        "accepted": evidence is not None,
                        "reason": reason,
                        "supports_information_need_advisory": assessment.supports_information_need,
                        **candidate_metadata,
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
                    "page_title_available": bool(result.page_title),
                    "page_content_block_count": len(result.content_blocks),
                    "heading_path_available": any(
                        block.section_headings for block in result.content_blocks
                    ),
                    "main_heading_available": None,
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
