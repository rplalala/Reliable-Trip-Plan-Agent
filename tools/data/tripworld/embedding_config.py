"""Offline batch embedding configuration, results and provider protocol."""


from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal, Protocol

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

Variant = Literal["raw", "enriched"]


class EmbeddingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    provider: Literal["openai"] = "openai"
    model_name: Literal["text-embedding-3-small"] = "text-embedding-3-small"
    dimension: Literal[1536] = 1536
    dimensions_parameter: None = None
    normalize: Literal[True] = True
    distance_metric: Literal["cosine"] = "cosine"
    query_prefix: Literal[""] = ""
    document_prefix: Literal[""] = ""
    tokenizer: Literal["cl100k_base"] = "cl100k_base"
    max_input_tokens: int = Field(default=8191, ge=1, le=8192)
    max_batch_inputs: int = Field(default=64, ge=1, le=2048)
    max_batch_tokens: int = Field(default=20000, ge=1, le=300000)
    max_attempts: int = Field(default=3, ge=1, le=5)
    timeout_seconds: float = Field(default=60, gt=0, le=120)
    max_run_usd: float = Field(default=0.10, gt=0)
    input_usd_per_million_tokens: float = Field(default=0.02, gt=0)
    pricing_checked_on: str = "2026-09-18"
    dtype: Literal["float32"] = "float32"
    embedding_version: str = "tripworld-openai-embedding-v1"


@dataclass(frozen=True)
class EncodedBatch:
    vectors: np.ndarray
    prompt_tokens: int
    total_tokens: int
    response_model: str
    request_id: str | None = None
    attempts: int = 1


class EmbeddingProvider(Protocol):
    config: EmbeddingConfig

    def encode(self, texts: Sequence[str], *, query: bool = False) -> EncodedBatch: ...


def production_config() -> EmbeddingConfig:
    return EmbeddingConfig(max_batch_inputs=64, max_batch_tokens=20000, max_run_usd=5)
