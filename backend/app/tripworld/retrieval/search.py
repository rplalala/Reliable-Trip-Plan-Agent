"""Exact cosine search after geographic filtering, independent of query construction."""

from collections.abc import Sequence
from time import perf_counter
from typing import Protocol

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from backend.app.tripworld.retrieval.embedding import Variant
from backend.app.tripworld.retrieval.entities import RetrievalEntity
from backend.app.tripworld.retrieval.geography import GeographicScope, haversine_km
from backend.app.tripworld.retrieval.sampling import geographic_mask


class DiscoveryIntent(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    semantic_query: str = Field(min_length=1)

    def query_text(self) -> str:
        text = " ".join(self.semantic_query.split())
        if not text:
            raise ValueError("Semantic discovery query cannot be blank")
        return text


class VectorSearch(Protocol):
    def search(
        self,
        query_vector: np.ndarray,
        scope: GeographicScope,
        top_k: int,
        *,
        exclude_ineligible: bool = False,
    ) -> dict: ...


class ExactIndex:
    def __init__(
        self,
        entities: Sequence[RetrievalEntity],
        vectors: np.ndarray,
        variant: Variant,
        embedding_metadata: dict,
    ):
        if variant not in ("raw", "enriched"):
            raise ValueError("Unknown retrieval variant")
        if vectors.ndim != 2 or len(vectors) != len(entities):
            raise ValueError("Entity/vector count mismatch")
        if not np.isfinite(vectors).all():
            raise ValueError("Nonfinite vectors")
        norms = np.linalg.norm(vectors, axis=1)
        if not np.allclose(norms, 1, atol=1e-5):
            raise ValueError("Cosine index requires normalized vectors")
        self.entities = entities
        self.vectors = vectors
        self.variant = variant
        self.metadata = embedding_metadata
        self.ids = np.array([entity.retrieval_entity_id for entity in entities])
        if len(set(self.ids)) != len(self.ids):
            raise ValueError("Duplicate retrieval entities")
        self.latitudes = np.array(
            [e.latitude if e.latitude is not None else np.nan for e in entities]
        )
        self.longitudes = np.array(
            [e.longitude if e.longitude is not None else np.nan for e in entities]
        )
        self.countries = np.array([e.country for e in entities], dtype=object)

    def search(
        self,
        query_vector: np.ndarray,
        scope: GeographicScope,
        top_k: int,
        *,
        exclude_ineligible: bool = False,
    ) -> dict:
        if not isinstance(top_k, int) or top_k < 1:
            raise ValueError("Top-K must be a positive integer")
        vector = np.asarray(query_vector, dtype=np.float32)
        if vector.shape != (self.vectors.shape[1],) or not np.isfinite(vector).all():
            raise ValueError("Query vector shape/value mismatch")
        norm = np.linalg.norm(vector)
        if norm == 0:
            raise ValueError("Query vector must be nonzero")
        vector = vector / norm
        start = perf_counter()
        coarse, exact = geographic_mask(self.latitudes, self.longitudes, self.countries, scope)
        geographic_count = int(exact.sum())
        if exclude_ineligible:
            exact &= np.array([e.eligibility_hint != "ineligible" for e in self.entities])
        indices = np.flatnonzero(exact)
        filter_seconds = perf_counter() - start
        ranking_start = perf_counter()
        scores = self.vectors[indices] @ vector
        order = np.lexsort((self.ids[indices], -scores))[:top_k]
        ranking_seconds = perf_counter() - ranking_start
        results = []
        for rank, position in enumerate(order, start=1):
            entity = self.entities[int(indices[position])]
            results.append(
                {
                    "rank": rank,
                    "similarity_score": float(scores[position]),
                    "distance_km": haversine_km(
                        scope.latitude,
                        scope.longitude,
                        entity.latitude,
                        entity.longitude,
                    ),
                    "entity": entity.model_dump(mode="json"),
                }
            )
        return {
            "variant": self.variant,
            "scope": scope.model_dump(),
            "top_k": top_k,
            "exclude_ineligible": exclude_ineligible,
            "bounding_box_count": int(coarse.sum()),
            "geographic_count": geographic_count,
            "eligible_or_unknown_count": len(indices),
            "filter_seconds": filter_seconds,
            "ranking_seconds": ranking_seconds,
            "results": results,
            "embedding_model": self.metadata.get("inputs", {}).get("embedding_model"),
        }
