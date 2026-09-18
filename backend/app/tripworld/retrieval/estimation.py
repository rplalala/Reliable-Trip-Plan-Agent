"""Offline corpus-wide token counts and explicit storage/cost assumptions."""

import os
from collections import Counter
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
import tiktoken

from backend.app.tripworld.artifacts import write_json_if_changed
from backend.app.tripworld.retrieval.embedding import EmbeddingConfig
from backend.app.tripworld.source import sha256_file

ROOT = Path(__file__).resolve().parents[4] / "data" / "tripworld"


def tokenizer() -> tiktoken.Encoding:
    # Public tokenizer data only; no embedding model weights or hosted local inference.
    os.environ.setdefault("TIKTOKEN_CACHE_DIR", str(ROOT / "tokenizer_cache"))
    return tiktoken.get_encoding("cl100k_base")


def estimate_embeddings(entities: Path, output: Path, config: EmbeddingConfig) -> dict:
    encoding = tokenizer()
    counts = {"raw": [], "enriched": []}
    lengths = Counter()
    overflow = []
    for batch in pq.ParquetFile(entities).iter_batches(batch_size=4096):
        for row in batch.to_pylist():
            for variant, field in (("raw", "raw_retrieval_text"), ("enriched", "retrieval_text")):
                text = row[field]
                count = len(encoding.encode_ordinary(text))
                counts[variant].append(count)
                lengths[variant] += len(text.encode("utf-8"))
                if count > config.max_input_tokens:
                    overflow.append(
                        {
                            "entity_id": row["retrieval_entity_id"],
                            "variant": variant,
                            "tokens": count,
                        }
                    )
    n = len(counts["raw"])
    report = {
        "estimate_version": "tripworld-openai-estimate-v1",
        "entity_artifact_sha256": sha256_file(entities),
        "entity_count": n,
        "tokenizer": "cl100k_base",
        "pricing_checked_on": config.pricing_checked_on,
        "input_usd_per_million_tokens": config.input_usd_per_million_tokens,
        "pricing_source": "https://developers.openai.com/api/docs/models/text-embedding-3-small",
        "variants": {},
        "overlong_documents": overflow,
        "storage_scenarios": {},
    }
    for variant, values in counts.items():
        report["variants"][variant] = {
            "total_tokens": sum(values),
            "empty_count": values.count(0),
            "mean_tokens": sum(values) / n,
            "max_tokens": max(values),
            "p50_tokens": float(np.percentile(values, 50)),
            "p95_tokens": float(np.percentile(values, 95)),
            "p99_tokens": float(np.percentile(values, 99)),
            "standard_api_usd": sum(values) / 1e6 * config.input_usd_per_million_tokens,
            "text_utf8_bytes": lengths[variant],
        }
    for dimension in (1536, 768, 512):
        vector_bytes = n * dimension * 4
        report["storage_scenarios"][str(dimension)] = {
            "one_variant_float32_bytes": vector_bytes,
            "two_variant_float32_bytes": 2 * vector_bytes,
            "one_variant_pgvector_payload_bytes": n * (dimension * 4 + 8),
            "postgres_planning_low_bytes": int((vector_bytes + n * 1024) * 1.2),
            "postgres_planning_high_bytes": int((vector_bytes + n * 4096) * 1.5),
            "assumptions": (
                "One vector per entity; 1-4 KiB metadata/entity and 20-50% heap/TOAST/index "
                "headroom; excludes HNSW, WAL, replicas/backups; estimate, not measured DB size"
            ),
        }
    write_json_if_changed(output, report)
    return report
