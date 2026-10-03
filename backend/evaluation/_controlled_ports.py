"""Strict, typed frozen collaborators and logical time for offline V3 replay."""

import asyncio
from collections import defaultdict, deque
from contextlib import contextmanager
from copy import deepcopy
from math import isfinite
from unittest.mock import patch

from pydantic import ValidationError

from backend.app.integrations.models import PlaceDetailsDTO, PlaceSearchResponse, RouteMatrixDTO
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.poi_semantics import FoundrySemanticAssessmentBatch
from backend.app.services.evidence_acquisition import _ProviderResult
from backend.app.services.poi_semantics import POISemanticsService, semantic_cache_key
from backend.app.tripworld.database.vectors import SPACE
from backend.app.tripworld.retrieval.entities import RetrievalEntity
from backend.app.versions.v3.repair_models import RepairPatch

from .records import canonical_digest

TYPES = {"search": PlaceSearchResponse, "details": PlaceDetailsDTO, "routes": RouteMatrixDTO}


class ReplayMismatch(RuntimeError):
    """Invalid frozen execution material, never a quality verdict."""


def key_tuple(value):
    if isinstance(value, (tuple, list)):
        return tuple(key_tuple(v) for v in value)
    if value is None or type(value) in (str, int, float, bool):
        return value
    raise ValueError("Cache keys require JSON scalar/tuple components")


def restore_cache(saved):
    cache = RequestCache()
    for entry in saved.cache:
        key = key_tuple(entry.key)
        if key in cache._values:
            raise ValueError("Duplicate frozen cache key")
        value = (
            TYPES[entry.value_type].model_validate(entry.value)
            if entry.value_type in TYPES
            else deepcopy(entry.value)
        )
        cache._values[key] = _ProviderResult(value=value) if entry.provider_envelope else value
    for entry in saved.attempts:
        key = key_tuple(entry.key)
        if key in cache.attempts:
            raise ValueError("Duplicate frozen attempt key")
        cache.attempts[key] = entry.status
    return cache


class FrozenPorts:
    def __init__(self, saved):
        self.calls, self.errors = [], []
        self.elapsed = 0.0
        self.scripts = defaultdict(deque)
        for row in saved.calls:
            self.scripts[(row.operation, canonical_digest(row.request))].append(row)
        self.artifact_hash = saved.rag_artifact_hash
        self.embedding_allowed = saved.rag_embedding_allowed
        self.search_allowed = saved.rag_search_allowed
        self.phase = "initial"

    def clock(self):
        return self.elapsed

    async def call(self, operation, request):
        record = {"operation": operation, "request": deepcopy(request)}
        self.calls.append(record)
        matches = self.scripts[(operation, canonical_digest(request))]
        if not matches:
            reason = f"missing_or_mismatched_frozen_call:{operation}"
            record["status"] = "unmatched"
            self.errors.append(reason)
            raise ReplayMismatch(reason)
        script = matches.popleft()
        self.elapsed += script.duration_seconds
        record.update(
            status="declared_failure" if script.error else "returned",
            duration_seconds=script.duration_seconds,
            response_hash=canonical_digest(script.response),
        )
        # Let the real asyncio timeout handles observe the advanced logical loop clock.
        # Two zero-delay turns run due timers before delivering the scripted response.
        try:
            await asyncio.sleep(0)
            await asyncio.sleep(0)
        except asyncio.CancelledError:
            record["status"] = "cancelled_before_response"
            raise
        if script.error:
            raise RuntimeError("Declared frozen failure: " + script.error)
        return deepcopy(script.response)

    async def generate_repair_structured(self, **kwargs):
        response = await self.call(
            "repair_model", {k: v for k, v in kwargs.items() if k != "usage_callback"}
        )
        try:
            RepairPatch.model_validate(response)
        except ValidationError as exc:
            self.errors.append("invalid_frozen_response:repair_model")
            raise ReplayMismatch(self.errors[-1]) from exc
        return response

    async def generate_poi_semantics_structured(self, **kwargs):
        response = await self.call(
            "poi_semantics", {k: v for k, v in kwargs.items() if k != "usage_callback"}
        )
        try:
            return FoundrySemanticAssessmentBatch.model_validate(response).model_dump(mode="json")
        except ValidationError as exc:
            self.errors.append("invalid_frozen_response:poi_semantics")
            raise ReplayMismatch(self.errors[-1]) from exc

    async def search_text(self, request):
        return await self.typed("places_search", request, PlaceSearchResponse)

    async def get_place_details(self, request):
        return await self.typed("places_details", request, PlaceDetailsDTO)

    async def compute_route_matrix(self, request):
        return await self.typed("route_matrix", request, RouteMatrixDTO)

    async def typed(self, operation, request, schema):
        response = await self.call(operation, request.model_dump(mode="json"))
        try:
            return schema.model_validate(response)
        except ValidationError as exc:
            self.errors.append("invalid_frozen_response:" + operation)
            raise ReplayMismatch(self.errors[-1]) from exc

    def allows_embedding(self, texts):
        return self.embedding_allowed

    def allows_search(self, vector, scope):
        return self.search_allowed

    async def embed(self, texts):
        result = await self.call("rag_embed", {"texts": texts})
        if (
            not isinstance(result, list)
            or len(result) != len(texts)
            or any(
                not isinstance(vector, list)
                or len(vector) != SPACE["dimensions"]
                or any(type(v) not in (int, float) or not isfinite(v) for v in vector)
                for vector in result
            )
        ):
            self.errors.append("invalid_frozen_response:rag_embed")
            raise ReplayMismatch(self.errors[-1])
        return result

    async def search(self, vector, scope, top_k):
        result = await self.call(
            "rag_search", {"vector": vector, "scope": scope.model_dump(mode="json"), "top_k": top_k}
        )
        try:
            if not isinstance(result, list):
                raise ValueError("Retrieval response must be a row list")
            for row in result:
                RetrievalEntity.model_validate(row["entity"])
                score = row["similarity_score"]
                if (
                    type(score) not in (int, float)
                    or not isfinite(score)
                    or row["retrieval_entity_artifact_hash"] != self.artifact_hash
                ):
                    raise ValueError("Invalid retrieval score/artifact linkage")
        except (ValueError, TypeError, KeyError) as exc:
            self.errors.append("invalid_frozen_response:rag_search")
            raise ReplayMismatch(self.errors[-1]) from exc
        return result

    @contextmanager
    def offline(self):
        def blocked(*args, **kwargs):
            self.errors.append("unexpected_live_io")
            raise ReplayMismatch("Controlled replay forbids live network/database access")

        with (
            patch.object(asyncio.get_running_loop(), "time", self.clock),
            patch("socket.create_connection", blocked),
            patch("socket.socket.connect", blocked),
            patch("socket.socket.connect_ex", blocked),
        ):
            yield


def restore_semantics(saved, ports):
    """Restore state into the production service, including its budgets and validation."""
    if saved.semantics is None:
        return None
    service = POISemanticsService(
        ports,
        saved.runtime.poi_semantics,
        saved.runtime.main_generation.framing_tokens,
        clock=ports.clock,
    )
    state = saved.semantics
    places = {p.place_id: p for p in saved.places}
    places.update(
        {
            c.candidate.place_id: c.structured_evidence
            for c in (*saved.enriched, *saved.admitted)
            if c.structured_evidence is not None
        }
    )
    for place in places.values():
        key = semantic_cache_key(place, saved.requirements, state.named_bindings)
        if key in state.cache and state.cache[key].place_id != place.place_id:
            raise ValueError("Frozen semantic cache identity mismatch")
    service.cache = dict(state.cache)
    service.ledger = {r.place_id: r for r in saved.semantic_assessments}
    service.calls, service.elapsed = state.calls, state.elapsed
    service.failed, service.named_bindings = state.failed, dict(state.named_bindings)
    return service
