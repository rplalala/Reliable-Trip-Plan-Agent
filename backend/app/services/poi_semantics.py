"""Request-owned, fail-closed candidate judgment with offline input accounting."""

import asyncio
import hashlib
import json
from time import perf_counter
from uuid import uuid4

from backend.app.runtime.token_counting import count_tokens
from backend.app.schemas.poi_semantics import (
    SEMANTICS_VERSION,
    FoundrySemanticAssessmentBatch,
    SemanticAssessmentBatch,
    SemanticAssessmentError,
    SemanticPreparationLimit,
)
from backend.app.services.poi_semantics_prompts import (
    POI_SEMANTICS_PROMPT,
    POI_SEMANTICS_PROMPT_VERSION,
)


def serialize_semantic_input(places, contract, named_bindings=None):
    return json.dumps(
        {
            "version": SEMANTICS_VERSION,
            "requirements": [r.model_dump(mode="json") for r in contract.semantic_requirements],
            "named_requirements": [r.model_dump(mode="json") for r in contract.named_places],
            "application_named_bindings": named_bindings or {},
            "places": [
                {
                    "place_id": p.place_id,
                    "name": p.name,
                    "primary_type": p.primary_type,
                    "address": p.formatted_address,
                    "source_ref": p.source_ref,
                }
                for p in places
            ],
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def semantic_input_tokens(payload, framing):
    schema = json.dumps(FoundrySemanticAssessmentBatch.model_json_schema(), sort_keys=True)
    return (
        count_tokens(payload) + count_tokens(POI_SEMANTICS_PROMPT) + count_tokens(schema) + framing
    )


class POISemanticsService:
    def __init__(self, llm, config, framing, *, tracer=None, deadline=None):
        self.llm, self.config, self.framing = llm, config, framing
        self.tracer, self.deadline = tracer, deadline
        self.cache, self.ledger, self.records = {}, {}, []
        self.calls = 0
        self.cache_hits = 0
        self.elapsed = 0.0
        self.failed = False
        self.named_bindings = {}

    def capture(self, stage, payload, record):
        """Optional development observer; storage cannot change planning decisions."""
        observer = getattr(self.llm, "capture_poi_semantics", None)
        if observer:
            try:
                observer(stage, payload)
            except Exception as exc:
                record.setdefault("capture_errors", []).append(type(exc).__name__)

    def snapshot(self):
        return dict(
            version=SEMANTICS_VERSION,
            prompt_version=POI_SEMANTICS_PROMPT_VERSION,
            prompt_sha256=hashlib.sha256(POI_SEMANTICS_PROMPT.encode()).hexdigest(),
            calls=self.calls,
            cache_hits=self.cache_hits,
            elapsed_seconds=self.elapsed,
            failed=self.failed,
            records=self.records,
            assessments=[r.model_dump(mode="json") for r in self.ledger.values()],
            effective_policy=self.config.model_dump(mode="json"),
            policy_sha256=hashlib.sha256(self.config.model_dump_json().encode()).hexdigest(),
            usage_note="Per-call usage is already included in outer callbacks when present",
        )

    async def assess(self, places, contract, *, deadline=None):
        if self.failed:
            raise SemanticAssessmentError("Semantic assessment already failed; no retry")
        unique = {p.place_id: p for p in places}
        pending = []
        for p in unique.values():
            key = hashlib.sha256(
                (
                    POI_SEMANTICS_PROMPT
                    + serialize_semantic_input([p], contract, self.named_bindings)
                ).encode()
            ).hexdigest()
            if key in self.cache:
                self.cache_hits += 1
                self.ledger[p.place_id] = self.cache[key]
            else:
                self.ledger.pop(p.place_id, None)
                pending.append((p, key))
        try:
            for offset in range(0, len(pending), self.config.batch_size):
                batch = pending[offset : offset + self.config.batch_size]
                payload = serialize_semantic_input(
                    [p for p, _ in batch], contract, self.named_bindings
                )
                tokens = semantic_input_tokens(payload, self.framing)
                if tokens > self.config.input_tokens:
                    raise SemanticPreparationLimit("poi_semantics_input_overflow")
                if self.calls >= self.config.max_calls:
                    raise SemanticPreparationLimit("poi_semantics_call_budget_exhausted")
                remaining = min(
                    self.config.call_timeout_seconds,
                    self.config.total_seconds - self.elapsed,
                    *[d - perf_counter() for d in (deadline, self.deadline) if d is not None],
                )
                if remaining <= 0:
                    raise SemanticPreparationLimit("poi_semantics_deadline")
                record = {
                    "call_id": uuid4().hex,
                    "prompt_version": POI_SEMANTICS_PROMPT_VERSION,
                    "prompt_sha256": hashlib.sha256(POI_SEMANTICS_PROMPT.encode()).hexdigest(),
                    "identities": [p.place_id for p, _ in batch],
                    "engineering_tokens": tokens,
                    "call": self.calls + 1,
                    "input_sha256": hashlib.sha256(payload.encode()).hexdigest(),
                    "status": "started",
                }
                self.records.append(record)
                self.calls += 1
                started = perf_counter()
                from langchain_core.callbacks import UsageMetadataCallbackHandler

                callback = UsageMetadataCallbackHandler()
                identity = {
                    k: record[k]
                    for k in ("call_id", "call", "prompt_version", "prompt_sha256", "input_sha256")
                }
                try:
                    self.capture("input", identity | {"input": json.loads(payload)}, record)
                    async with asyncio.timeout(remaining):
                        raw = await self.llm.generate_poi_semantics_structured(
                            system_prompt=POI_SEMANTICS_PROMPT,
                            user_prompt=payload,
                            output_tokens=self.config.output_tokens,
                            usage_callback=callback,
                        )
                    result = SemanticAssessmentBatch.model_validate(raw)
                    self.capture(
                        "output", identity | {"output": result.model_dump(mode="json")}, record
                    )
                    self._validate(result, [p for p, _ in batch], contract)
                    rows = {r.place_id: r for r in result.assessments}
                    for p, key in batch:
                        self.cache[key] = self.ledger[p.place_id] = rows[p.place_id]
                    record["status"] = "accepted"
                    record["assessments"] = result.model_dump(mode="json")
                except asyncio.CancelledError:
                    record["status"] = "cancelled"
                    raise
                except Exception as exc:
                    record.update(status="failed", error_type=type(exc).__name__)
                    if isinstance(exc, SemanticAssessmentError) and exc.details:
                        record["error_details"] = exc.details
                    raise
                finally:
                    spent = perf_counter() - started
                    self.elapsed += spent
                    record["elapsed_seconds"] = spent
                    record["usage"] = dict(callback.usage_metadata)
                    self.capture("outcome", dict(record), record)
                    if self.tracer:
                        self.tracer.event("poi_semantic_assessment", record)
        except SemanticPreparationLimit as exc:
            self.records.append({"status": "pre_send_stop", "reason": str(exc)})
            raise
        except asyncio.CancelledError:
            self.failed = True
            raise
        except Exception as exc:
            self.failed = True
            if isinstance(exc, SemanticAssessmentError):
                raise
            raise SemanticAssessmentError("poi_semantics_system_failure") from exc
        return {pid: self.ledger[pid] for pid in unique}

    async def prepare(self, places, contract, *, deadline=None):
        """Do not turn an unassessed identity into permission when a local budget stops."""
        try:
            await self.assess(places, contract, deadline=deadline)
        except SemanticPreparationLimit:
            pass
        return {p.place_id: self.ledger[p.place_id] for p in places if p.place_id in self.ledger}

    def _validate(self, result, places, contract):
        sources = {p.place_id: {p.source_ref} for p in places}
        ids = [r.place_id for r in result.assessments]
        if len(set(ids)) != len(ids) or set(ids) != set(sources):
            raise SemanticAssessmentError("Semantic result identity set differs from input")
        requirements = {r.requirement_id: r for r in contract.semantic_requirements}
        named = {r.requirement_id: r for r in contract.named_places}
        known_refs = requirements.keys() | named.keys()
        for row in result.assessments:
            matches = {m.requirement_id: m for m in row.matches}
            if len(matches) != len(row.matches) or not matches.keys() <= known_refs:
                raise SemanticAssessmentError("Invalid semantic requirement references")
            if not row.evidence_refs or not set(row.evidence_refs) <= sources[row.place_id]:
                raise SemanticAssessmentError("Invalid semantic evidence references")
            for match in row.matches:
                if not set(match.evidence_refs) <= sources[row.place_id]:
                    invalid = [
                        ref for ref in match.evidence_refs if ref not in sources[row.place_id]
                    ]
                    raise SemanticAssessmentError(
                        "Invalid match evidence references",
                        details={
                            "place_id": row.place_id[:256],
                            "requirement_id": match.requirement_id[:256],
                            "relation": match.relation,
                            "allowed_refs": [ref[:256] for ref in sorted(sources[row.place_id])],
                            "offending_refs": [ref[:256] for ref in invalid[:8]],
                            "truncated": any(
                                len(ref) > 256
                                for ref in [
                                    row.place_id,
                                    match.requirement_id,
                                    *sources[row.place_id],
                                    *invalid,
                                ]
                            ),
                        },
                    )
                if match.relation == "supported" and not match.evidence_refs:
                    raise SemanticAssessmentError("Supported match requires input evidence")
            for ref in row.exception_requirement_ids:
                req = requirements.get(ref)
                goal = req.experience_goal if req else None
                authorized = bool(
                    goal and goal.explicit_primary_exception and req.polarity == "favor"
                ) or (
                    ref in named
                    and named[ref].inclusion == "REQUIRED"
                    and self.named_bindings.get(ref) == row.place_id
                )
                if not authorized or ref not in matches or matches[ref].relation != "supported":
                    raise SemanticAssessmentError("Unauthorized primary exception")
            if row.exception_requirement_ids and row.role != "exception_only":
                raise SemanticAssessmentError("Exception ownership belongs to exception_only")
