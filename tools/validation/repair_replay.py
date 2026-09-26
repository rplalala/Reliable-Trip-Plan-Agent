"""Bounded development snapshots and evidence-only, no-provider Repair preparation."""

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from backend.app.evidence.selection_models import PlaceSelectionInput
from backend.app.runtime.config_models import RuntimeConfig
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.poi_semantics import POISemanticAssessment
from backend.app.services import poi_semantics
from backend.app.tripworld.retrieval.geography import GeographicScope
from backend.app.versions.v3.repair_acceptance import assess
from backend.app.versions.v3.repair_budget import RepairBudget
from backend.app.versions.v3.repair_candidates import prepare_candidates
from backend.app.versions.v3.repair_models import RepairScope, ValidationContext
from backend.app.versions.v3.repair_projection import REPAIR_SYSTEM_PROMPT
from backend.app.versions.v3.repair_targets import insertion_windows
from backend.app.versions.v3.wiring import operation_scope
from tools.validation.requirement_capture import DevelopmentRequirementCapture

MAX_BYTES = 4 * 1024 * 1024


class CapturedRepair:
    """One opt-in stage-entry artifact, immutable and capped for the whole case."""

    def __init__(self, client, directory, metadata, errors):
        self.client, self.metadata, self.errors = client, metadata, errors
        self.capture, self.attempted, self.saved = None, False, False
        try:
            self.capture = DevelopmentRequirementCapture(
                directory,
                scenario_id=metadata.get("case_id", "development"),
                secrets=getattr(client, "_capture_secrets", ()),
            )
        except Exception as exc:
            self.errors.append("repair_capture_" + type(exc).__name__)

    def __getattr__(self, name):
        return getattr(self.client, name)

    def capture_repair_snapshot(self, **inputs):
        if self.attempted:
            self.errors.append("repair_capture_duplicate_stage")
            return
        self.attempted = True
        if self.capture is None:
            return
        try:
            snapshot = make_snapshot(
                **inputs, request_limit=self.metadata.get("request_budget_seconds")
            )
            path = self.capture.record(
                self.metadata.get("case_id", "development"),
                "before_repair_stage",
                {"snapshot": snapshot.model_dump(mode="json")},
                max_bytes=MAX_BYTES,
            )
            self.saved = path is not None
            if not self.saved:
                self.errors.append("repair_capture_write_failed")
        except Exception as exc:
            self.errors.append("repair_capture_" + type(exc).__name__)


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


class SnapshotModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class SemanticSnapshot(SnapshotModel):
    prompt_sha256: str
    cache: dict[str, POISemanticAssessment]
    named_bindings: dict[str, str]
    calls: int = Field(ge=0)
    elapsed: float = Field(ge=0)
    failed: bool


class ReplaySnapshot(SnapshotModel):
    version: Literal[1]
    phase: Literal["before_repair_stage"]
    provenance: Literal["captured", "synthetic"]
    original: Itinerary
    context: ValidationContext
    scope: RepairScope | None
    enriched: tuple[PlaceSelectionInput, ...]
    admitted: tuple[PlaceSelectionInput, ...]
    runtime: RuntimeConfig
    runtime_sha256: str
    repair_prompt_sha256: str
    request_remaining: float = Field(ge=0)
    request_limit: float | None = Field(ge=0)
    request_elapsed: float | None = Field(ge=0)
    repair_remaining: float = Field(ge=0)
    repair_used: dict[str, int]
    repair_limits: dict[str, int]
    cache_identities: dict[str, str]
    cached_key_hashes: tuple[str, ...]
    semantics: SemanticSnapshot | None
    geographic_scope: GeographicScope | None
    intent_ids: tuple[str, ...]


def make_snapshot(
    *,
    original,
    context,
    scope,
    enriched,
    admitted,
    runtime,
    request_remaining,
    cache,
    semantic_service,
    geographic_scope,
    intent_ids,
    provenance="captured",
    request_limit=None,
):
    """Record stage-entry allowances; no Repair operation has consumed this ledger yet."""
    remaining = max(0, request_remaining)
    budget = RepairBudget(remaining, clock=lambda: 0, runtime_config=runtime)
    semantics = None
    if semantic_service is not None:
        semantics = SemanticSnapshot(
            prompt_sha256=digest(poi_semantics.POI_SEMANTICS_PROMPT),
            cache=semantic_service.cache.copy(),
            named_bindings=semantic_service.named_bindings.copy(),
            calls=semantic_service.calls,
            elapsed=semantic_service.elapsed,
            failed=semantic_service.failed,
        )
    # Hash identities only. Never serialize provider envelopes or executable cache values.
    identities = {digest(repr(k)): v for k, v in cache.attempts.items()}
    return ReplaySnapshot(
        version=1,
        phase="before_repair_stage",
        provenance=provenance,
        original=original,
        context=context,
        scope=scope,
        enriched=enriched,
        admitted=admitted,
        runtime=runtime,
        runtime_sha256=digest(runtime.model_dump_json()),
        repair_prompt_sha256=digest(REPAIR_SYSTEM_PROMPT),
        request_remaining=remaining,
        request_limit=request_limit,
        request_elapsed=max(0, request_limit - remaining) if request_limit is not None else None,
        repair_remaining=budget.remaining(),
        repair_used=dict(budget.used),
        repair_limits=budget.limits,
        cache_identities=identities,
        cached_key_hashes=tuple(sorted(digest(repr(k)) for k in cache._values)),
        semantics=semantics,
        geographic_scope=geographic_scope,
        intent_ids=intent_ids,
    )


class FrozenSemantics:
    """Only exact saved input fingerprints may grant eligibility; never call a model."""

    def __init__(self, saved, config):
        self.saved, self.config = saved, config
        self.calls, self.elapsed = saved.calls, saved.elapsed
        self.ledger, self.missing = {}, set()

    async def prepare(self, places, contract, *, deadline=None):
        for place in places:
            key = digest(
                poi_semantics.POI_SEMANTICS_PROMPT
                + poi_semantics.serialize_semantic_input(
                    [place], contract, self.saved.named_bindings
                )
            )
            row = self.saved.cache.get(key)
            if row is None or self.saved.failed or row.place_id != place.place_id:
                self.missing.add(place.place_id)
                self.ledger.pop(place.place_id, None)
            else:
                self.ledger[place.place_id] = row
        return {p.place_id: self.ledger[p.place_id] for p in places if p.place_id in self.ledger}


async def replay(saved):
    """Inspect saved scope and preparation, not model proposals or adoption outcomes.

    Request-cache identities are audit-only: unavailable cached values are not recreated.
    No provider, retrieval port, client factory or repair model is constructed or injected.
    """
    if digest(saved.runtime.model_dump_json()) != saved.runtime_sha256:
        raise ValueError("runtime_fingerprint_mismatch")
    if saved.semantics is None:
        raise ValueError("semantic_cache_snapshot_missing")
    budget = RepairBudget(saved.request_remaining, clock=lambda: 0, runtime_config=saved.runtime)
    if budget.limits != saved.repair_limits or saved.repair_used:
        raise ValueError("snapshot_is_not_an_unused_stage_entry_budget")
    budget.deadline = min(budget.deadline, saved.repair_remaining)
    budget.io_deadline = min(budget.deadline, budget.policy.timing.preparation_seconds)
    rich_ids = {c.candidate.place_id for c in saved.enriched}
    pool = (*saved.enriched, *(c for c in saved.admitted if c.candidate.place_id not in rich_ids))
    semantics = FrozenSemantics(saved.semantics, saved.runtime.poi_semantics)
    report = assess(saved.original, saved.context)
    recomputed = operation_scope(
        saved.original,
        report,
        context=saved.context,
        policy=budget.policy,
        mode=saved.scope.travel_mode if saved.scope else None,
    )
    if (recomputed is None) != (saved.scope is None) or (
        recomputed
        and recomputed.model_dump(
            exclude={
                "window_roots",
                "routing_preference",
                "mode_source",
                "unsupported_explicit_mode",
            }
        )
        != saved.scope.model_dump(
            exclude={
                "window_roots",
                "routing_preference",
                "mode_source",
                "unsupported_explicit_mode",
            }
        )
    ):
        raise ValueError("scope_policy_drift")
    preparation = None
    stop = "no_authorized_targets" if saved.scope is None else None
    if saved.scope is not None:
        if budget.remaining() < (
            budget.policy.timing.minimum_model_seconds
            + budget.policy.timing.recheck_reserve_seconds
        ):
            stop = "insufficient_stage_time"
        else:
            preparation = await prepare_candidates(
                saved.context,
                saved.scope,
                budget,
                original=saved.original,
                pool=pool,
                semantic_service=semantics,
                geographic_scope=saved.geographic_scope,
                intent_ids=saved.intent_ids,
            )
    return dict(
        provenance=saved.provenance,
        mode="evidence_only_stage_scope",
        limitations=[
            "No model proposal or adoption replay",
            "Request-cache values and missing provider evidence are not reconstructed",
            "Stage scope is not a localized Repair round or live feasibility proof",
        ],
        pool_ids=[c.candidate.place_id for c in pool],
        scope=saved.scope.model_dump(mode="json") if saved.scope else None,
        windows=insertion_windows(saved.original, saved.context.schedule, saved.scope)
        if saved.scope
        else [],
        preparation=preparation.model_dump(mode="json") if preparation else None,
        budget_used=dict(budget.used),
        repair_remaining=budget.remaining(),
        stop=stop,
        semantic_calls=semantics.calls,
        semantic_elapsed=semantics.elapsed,
        semantic_remaining_calls=max(0, semantics.config.max_calls - semantics.calls),
        semantic_remaining_seconds=max(0, semantics.config.total_seconds - semantics.elapsed),
        request_elapsed=saved.request_elapsed,
        request_remaining=saved.request_remaining,
        missing_snapshot_fields=["request_limit", "request_elapsed"]
        if saved.request_limit is None
        else [],
        repair_prompt_matches=saved.repair_prompt_sha256 == digest(REPAIR_SYSTEM_PROMPT),
        semantic_missing=sorted(semantics.missing),
        semantic_prompt_matches=(
            saved.semantics.prompt_sha256 == digest(poi_semantics.POI_SEMANTICS_PROMPT)
        ),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.snapshot.stat().st_size > MAX_BYTES:
        parser.error("Snapshot exceeds the 4 MiB limit")
    document = json.loads(args.snapshot.read_text(encoding="utf-8"))
    saved = ReplaySnapshot.model_validate(document["snapshot"])
    result = asyncio.run(replay(saved))
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, default=str)


if __name__ == "__main__":
    main()
