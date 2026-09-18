"""OpenAI embedding contracts and resumable, content-addressed local artifacts."""

import hashlib
import importlib.metadata
import json
import os
import time
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal, Protocol

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from backend.app.tripworld.artifacts import (
    artifact_is_current,
    load_json_object,
    payload_fingerprint,
    write_json_if_changed,
)
from backend.app.tripworld.retrieval.entities import RetrievalEntity
from backend.app.tripworld.source import sha256_file

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


def validate_vectors(vectors: np.ndarray, rows: int, dimension: int) -> None:
    if vectors.shape != (rows, dimension) or vectors.dtype != np.float32:
        raise ValueError("Embedding shape/dtype mismatch")
    if not np.isfinite(vectors).all():
        raise ValueError("Embedding contains nonfinite values")
    if not np.allclose(np.linalg.norm(vectors, axis=1), 1.0, atol=1e-5):
        raise ValueError("Embedding vectors must be L2-normalized")


def text_for(entity: RetrievalEntity, variant: Variant) -> str:
    if variant not in ("raw", "enriched"):
        raise ValueError("Unknown retrieval variant")
    return entity.raw_retrieval_text if variant == "raw" else entity.retrieval_text


def content_hash(entities: Sequence[RetrievalEntity], variant: Variant) -> str:
    digest = hashlib.sha256()
    for entity in entities:
        digest.update(
            json.dumps(
                [entity.retrieval_entity_id, entity.content_hash, text_for(entity, variant)],
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode()
        )
        digest.update(b"\n")
    return digest.hexdigest()


def embedding_inputs(
    entities: Sequence[RetrievalEntity],
    variant: Variant,
    config: EmbeddingConfig,
    entity_metadata: dict,
    sample_hash: str,
) -> dict:
    inputs = entity_metadata["inputs"]
    return {
        "tripworld_revision": inputs["tripworld_revision"],
        "retrieval_corpus_hash": inputs["source_retrieval_corpus_hash"],
        "retrieval_entity_artifact_hash": entity_metadata["output_sha256"],
        "retrieval_entity_builder_version": inputs["retrieval_entity_builder_version"],
        "semantic_mapping_version": inputs["semantic_mapping_version"],
        "retrieval_text_template_version": inputs["retrieval_text_template_version"],
        "retrieval_variant": variant,
        "embedding_model": config.model_dump(),
        "entity_count": len(entities),
        "content_hash": content_hash(entities, variant),
        "sample_artifact_hash": sample_hash,
        "entity_ids": [entity.retrieval_entity_id for entity in entities],
        "software_versions": {
            name: importlib.metadata.version(name) for name in ("numpy", "openai", "tiktoken")
        },
    }


def encode_resumable(
    texts: Sequence[str],
    provider: EmbeddingProvider,
    directory: Path,
    *,
    query: bool = False,
    token_counts: Sequence[int],
    batch_size: int | None = None,
    verbose: bool = True,
) -> tuple[np.ndarray, dict]:
    """Persist each completed API batch atomically before requesting the next batch.

    A lost response before durable checkpoint may be billed again on retry; no API-level
    exactly-once guarantee is claimed. Completed checkpoints are never regenerated.
    """
    config = provider.config
    if len(texts) != len(token_counts) or not texts:
        raise ValueError("Token counts must match nonempty embedding inputs")
    if any(not text.strip() for text in texts):
        raise ValueError("Empty embedding input")
    if any(count < 1 or count > config.max_input_tokens for count in token_counts):
        raise ValueError("Embedding input exceeds configured token limit")
    size = config.max_batch_inputs if batch_size is None else batch_size
    if not 1 <= size <= config.max_batch_inputs:
        raise ValueError("Batch size exceeds configured API limit")
    chunks: list[tuple[int, int]] = []
    start, tokens = 0, 0
    for i, count in enumerate(token_counts):
        if count > config.max_batch_tokens:
            raise ValueError("One input exceeds batch token budget")
        if i > start and (i - start >= size or tokens + count > config.max_batch_tokens):
            chunks.append((start, i))
            start, tokens = i, 0
        tokens += count
    chunks.append((start, len(texts)))
    # Worst-case retry exposure is bounded before any paid request.
    estimated_cost = sum(token_counts) / 1e6 * config.input_usd_per_million_tokens
    if estimated_cost * config.max_attempts > config.max_run_usd:
        raise ValueError("Embedding run exceeds configured worst-case retry cost budget")
    directory.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    arrays = []
    reused, new = 0, 0
    new_usage = total_usage = attempts = 0
    new_documents = new_local_tokens = 0
    records = []
    for first, last in chunks:
        chunk_texts = list(texts[first:last])
        inputs = {"config": config.model_dump(), "query": query, "texts": chunk_texts}
        fingerprint = payload_fingerprint(inputs)
        path = directory / (fingerprint + ".npz")
        if path.exists():
            with np.load(path, allow_pickle=False) as checkpoint:
                vectors = checkpoint["vectors"]
                metadata = json.loads(str(checkpoint["metadata"].item()))
            validate_vectors(vectors, last - first, config.dimension)
            if metadata["input_fingerprint"] != fingerprint:
                raise ValueError("Embedding checkpoint input mismatch")
            if hashlib.sha256(vectors.tobytes()).hexdigest() != metadata["vectors_sha256"]:
                raise ValueError("Embedding checkpoint checksum mismatch")
            reused += 1
        else:
            result = provider.encode(chunk_texts, query=query)
            vectors = result.vectors
            validate_vectors(vectors, last - first, config.dimension)
            metadata = {
                "input_fingerprint": fingerprint,
                "vectors_sha256": hashlib.sha256(vectors.tobytes()).hexdigest(),
                "prompt_tokens": result.prompt_tokens,
                "total_tokens": result.total_tokens,
                "response_model": result.response_model,
                "request_id": result.request_id,
                "attempts": result.attempts,
                "created_at": datetime.now(UTC).isoformat(),
            }
            temporary = path.with_suffix(".npz.part")
            with temporary.open("wb") as handle:
                np.savez(handle, vectors=vectors, metadata=json.dumps(metadata, sort_keys=True))
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
            new += 1
            new_usage += result.total_tokens
            attempts += result.attempts
            new_documents += last - first
            new_local_tokens += sum(token_counts[first:last])
        total_usage += metadata["total_tokens"]
        records.append({"checkpoint": path.name, **metadata})
        arrays.append(vectors)
        if verbose and new % 8 == 1:
            print(f"Embedded/checkpointed {last}/{len(texts)} texts", flush=True)
    elapsed = time.perf_counter() - started
    return np.vstack(arrays), {
        "encode_seconds": elapsed,
        "new_api_batches": new,
        "reused_batches": reused,
        "new_api_attempts": attempts,
        "new_usage_tokens": new_usage,
        "artifact_usage_tokens": total_usage,
        "new_documents": new_documents,
        "new_local_token_estimate": new_local_tokens,
        "estimated_new_cost_usd": new_usage / 1e6 * config.input_usd_per_million_tokens,
        "documents_per_second": new_documents / elapsed if new_documents else None,
        "checkpoints": records,
    }


def build_embeddings(
    entities: Sequence[RetrievalEntity],
    variant: Variant,
    provider: EmbeddingProvider,
    directory: Path,
    entity_metadata: dict,
    sample_hash: str,
    *,
    batch_size: int = 64,
    token_counts: Sequence[int] | None = None,
) -> dict:
    if not entities or len({e.retrieval_entity_id for e in entities}) != len(entities):
        raise ValueError("Embedding build requires nonempty unique entities")
    inputs = embedding_inputs(entities, variant, provider.config, entity_metadata, sample_hash)
    fingerprint = payload_fingerprint(inputs)
    path = directory / f"{variant}.npy"
    sidecar = directory / f"{variant}.manifest.json"
    if artifact_is_current(path, sidecar, input_fingerprint=fingerprint):
        metadata = load_json_object(sidecar)
        return {
            **metadata,
            "artifact_creation_usage": {
                key: value
                for key, value in metadata.items()
                if key not in ("inputs", "checkpoints")
            },
            "reused": True,
            "encode_seconds": 0.0,
            "new_api_batches": 0,
            "new_api_attempts": 0,
            "new_usage_tokens": 0,
            "new_documents": 0,
            "new_local_token_estimate": 0,
            "estimated_new_cost_usd": 0.0,
            "documents_per_second": None,
        }
    texts = [text_for(entity, variant) for entity in entities]
    if token_counts is None:
        from backend.app.tripworld.retrieval.estimation import tokenizer

        encoding = tokenizer()
        token_counts = [len(encoding.encode_ordinary(text)) for text in texts]
    vectors, usage = encode_resumable(
        texts,
        provider,
        directory / "checkpoints",
        token_counts=token_counts,
        batch_size=batch_size,
    )
    temporary = path.with_suffix(".npy.part")
    with temporary.open("wb") as handle:
        np.save(handle, vectors, allow_pickle=False)
    os.replace(temporary, path)
    metadata = {
        "inputs": inputs,
        "input_fingerprint": fingerprint,
        "output_sha256": sha256_file(path),
        "output_size_bytes": path.stat().st_size,
        **usage,
    }
    write_json_if_changed(sidecar, metadata)
    return {**metadata, "reused": False}


def load_embeddings(path: Path, expected_inputs: dict) -> tuple[np.ndarray, dict]:
    metadata = load_json_object(path.with_suffix(".manifest.json"))
    fingerprint = payload_fingerprint(expected_inputs)
    if metadata["inputs"] != expected_inputs or not artifact_is_current(
        path,
        path.with_suffix(".manifest.json"),
        input_fingerprint=fingerprint,
    ):
        raise ValueError("Embedding artifact/version/content mismatch")
    vectors = np.load(path, mmap_mode="r", allow_pickle=False)
    validate_vectors(
        vectors, expected_inputs["entity_count"], expected_inputs["embedding_model"]["dimension"]
    )
    return vectors, metadata
