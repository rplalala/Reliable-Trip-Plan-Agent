"""Bounded global embedding preflight and streaming resumable production build."""

import shutil
import threading
import time
from collections import Counter, deque
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

from backend.app.tripworld.artifacts import load_json_object
from backend.app.tripworld.database.policy import POLICY_VERSION, exclusion_reasons, text_hash
from backend.app.tripworld.database.vectors import SPACE_ID
from backend.app.tripworld.hashing import sha256_file
from backend.app.tripworld.retrieval.entities import RetrievalEntity
from tools.data.tripworld.artifact_persistence import write_json_if_changed
from tools.data.tripworld.embedding_build import embedding_inputs, encode_resumable, load_embeddings
from tools.data.tripworld.embedding_config import EmbeddingConfig, production_config
from tools.data.tripworld.estimation import tokenizer
from tools.data.tripworld.openai_adapter import OpenAIEmbeddingAdapter
from tools.data.tripworld.vector_store import prepare_space, store_vectors


def write_progress(path: Path, payload: dict) -> None:
    """A Windows reader may briefly lock a report; never lose paid work for telemetry."""
    for attempt in range(5):
        try:
            write_json_if_changed(path, payload)
            return
        except OSError:
            time.sleep(0.05 * (attempt + 1))
    print("Progress report unavailable; durable database/checkpoint state retained", flush=True)


def preflight(conn, root: Path) -> dict:
    encoding = tokenizer()
    counts = conn.execute(
        "SELECT count(*) AS total, count(*) FILTER (WHERE discovery_allowed) AS production "
        "FROM tripworld.entities"
    ).fetchone()
    reasons = Counter()
    exclusive = Counter()
    for row in conn.execute(
        "SELECT exclusion_reasons,count(*) AS n FROM tripworld.entities "
        "WHERE NOT discovery_allowed GROUP BY exclusion_reasons"
    ):
        reasons.update({reason: row["n"] for reason in row["exclusion_reasons"]})
        exclusive[row["exclusion_reasons"][0]] += row["n"]
    total_tokens = unique_tokens = unique_texts = max_tokens = 0
    with conn.cursor(name="preflight_texts") as cursor:
        cursor.execute(
            "SELECT text_hash,retrieval_text,count(*) AS n FROM tripworld.entities "
            "WHERE discovery_allowed GROUP BY text_hash,retrieval_text"
        )
        for row in cursor:
            tokens = len(encoding.encode_ordinary(row["retrieval_text"]))
            max_tokens = max(tokens, max_tokens)
            total_tokens += tokens * row["n"]
            unique_tokens += tokens
            unique_texts += 1
    manifest = conn.execute(
        "SELECT DISTINCT artifact_hash,policy_version FROM tripworld.entities"
    ).fetchall()
    conn.commit()
    if len(manifest) != 1 or manifest[0]["policy_version"] != POLICY_VERSION:
        raise ValueError("Production corpus must have one artifact and current policy")
    payload = counts["production"] * 1536 * 4
    result = {
        **counts,
        "unique_texts": unique_texts,
        "exclusions_overlapping": dict(reasons),
        "exclusions_first_reason": dict(exclusive),
        "policy_version": POLICY_VERSION,
        "artifact_hash": manifest[0]["artifact_hash"],
        "entity_tokens": total_tokens,
        "unique_text_tokens": unique_tokens,
        "max_input_tokens": max_tokens,
        "estimated_usd": unique_tokens / 1e6 * 0.02,
        "max_retry_exposure_usd": unique_tokens / 1e6 * 0.02 * 3,
        "vector_payload_bytes": payload,
        "estimated_database_bytes_low": int((payload + counts["total"] * 1024) * 1.2),
        "estimated_database_bytes_high": int((payload + counts["total"] * 4096) * 1.5),
        "available_workspace_disk_bytes": shutil.disk_usage(root).free,
        "estimated_serial_seconds_at_phase4_rate": unique_texts / 51.963225620332736,
        "storage_caveat": "Excludes checkpoint copies, WAL, Docker VM overhead and backups",
        "price_source": "https://developers.openai.com/api/docs/models/text-embedding-3-small",
    }
    result["approved_low_cost_range"] = (
        result["estimated_usd"] <= 2
        and result["max_retry_exposure_usd"] <= 5
        and max_tokens <= 8191
        and result["available_workspace_disk_bytes"] >= 25 * 1024**3
    )
    write_json_if_changed(root / "reports/phase5_preflight.json", result)
    return result


def reuse_spike(conn, root: Path) -> int:
    directory = root / "artifacts/phase4"
    if not (directory / "enriched.npy").exists():
        return 0
    sample = directory / "sample_entities.parquet"
    entities = [RetrievalEntity.model_validate(r) for r in pq.read_table(sample).to_pylist()]
    meta = load_json_object(root / "artifacts/retrieval_entities.parquet.manifest.json")
    config = EmbeddingConfig.model_validate_json(
        (root / "embedding_model.v1.json").read_text(encoding="utf-8")
    )
    vectors, metadata = load_embeddings(
        directory / "enriched.npy",
        embedding_inputs(entities, "enriched", config, meta, sha256_file(sample)),
    )
    indexes = {}
    for index, e in enumerate(entities):
        if not exclusion_reasons(e):
            indexes.setdefault(text_hash(e.retrieval_text), index)
    return store_vectors(
        conn,
        list(indexes),
        np.array(vectors[list(indexes.values())]),
        {"source": "phase4_enriched", "artifact_sha256": metadata["output_sha256"]},
    )


def missing_batches(conn, encoding, config):
    """Keyset pagination keeps memory bounded and avoids a long database snapshot."""
    last_hash = ""
    batch, tokens = [], 0
    while True:
        rows = conn.execute(
            "SELECT DISTINCT e.text_hash,e.retrieval_text FROM tripworld.entities e "
            "WHERE e.discovery_allowed AND e.text_hash>%s AND NOT EXISTS "
            "(SELECT 1 FROM tripworld.embeddings v WHERE v.space_id=%s "
            "AND v.text_hash=e.text_hash) ORDER BY e.text_hash LIMIT 2048",
            (last_hash, SPACE_ID),
        ).fetchall()
        conn.commit()
        if not rows:
            break
        for row in rows:
            n = len(encoding.encode_ordinary(row["retrieval_text"]))
            if n < 1 or n > config.max_input_tokens:
                raise ValueError("Invalid production input token count")
            if batch and (
                len(batch) >= config.max_batch_inputs or tokens + n > config.max_batch_tokens
            ):
                yield batch
                batch, tokens = [], 0
            batch.append((row["text_hash"], row["retrieval_text"], n))
            tokens += n
        last_hash = rows[-1]["text_hash"]
    if batch:
        yield batch


def build(conn, root: Path, *, workers: int = 16, provider_factory=OpenAIEmbeddingAdapter) -> dict:
    if not 1 <= workers <= 16:
        raise ValueError("Production build supports one to sixteen workers")
    report = load_json_object(root / "reports/phase5_preflight.json")
    current = conn.execute(
        "SELECT DISTINCT artifact_hash,policy_version FROM tripworld.entities"
    ).fetchall()
    if not report["approved_low_cost_range"] or current != [
        {"artifact_hash": report["artifact_hash"], "policy_version": report["policy_version"]}
    ]:
        raise ValueError("Run and review production preflight for the current corpus")
    conn.commit()
    # One writer prevents duplicate paid jobs against this database.
    if not conn.execute("SELECT pg_try_advisory_lock(74501903) AS acquired").fetchone()["acquired"]:
        raise ValueError("Another production embedding build is active")
    conn.commit()
    started = time.perf_counter()
    config = production_config()
    usage = Counter()
    report_path = root / "reports/phase5_embedding_run.json"
    prior = load_json_object(report_path) if report_path.exists() else {}
    history = prior.get("run_history", [])
    if prior.get("status") == "running":
        history = [
            *history,
            {
                "status": "interrupted",
                "wall_seconds": prior.get("wall_seconds"),
                **prior.get("current_run", {}),
            },
        ]

    thread_state = threading.local()
    providers = []
    next_submission = time.monotonic()

    def submit(executor, batch):
        nonlocal next_submission
        # Observed account limit is 1M tokens/minute; leave 10% headroom.
        # Pacing also bounds bursts when requests finish faster than expected.
        time.sleep(max(0.0, next_submission - time.monotonic()))
        next_submission = time.monotonic() + sum(row[2] for row in batch) / 15000
        return executor.submit(encode, batch)

    def encode(batch):
        if not hasattr(thread_state, "provider"):
            thread_state.provider = provider_factory(config)
            providers.append(thread_state.provider)
        vectors, stats = encode_resumable(
            [r[1] for r in batch],
            thread_state.provider,
            root / "artifacts/phase5/checkpoints",
            token_counts=[r[2] for r in batch],
            batch_size=config.max_batch_inputs,
            verbose=False,
        )
        return batch, vectors, stats

    status = "running"
    error_type = None
    try:
        prepare_space(conn)
        usage["reused_phase4_vectors"] = reuse_spike(conn, root)
        batches = iter(missing_batches(conn, tokenizer(), config))
        with ThreadPoolExecutor(max_workers=workers) as executor:
            pending = deque()
            for _ in range(workers):
                if (batch := next(batches, None)) is not None:
                    pending.append(submit(executor, batch))
            while pending:
                batch, vectors, stats = pending.popleft().result()
                stored = store_vectors(conn, [r[0] for r in batch], vectors, stats)
                for key in (
                    "new_api_batches",
                    "new_api_attempts",
                    "new_usage_tokens",
                    "reused_batches",
                ):
                    usage[key] += stats[key]
                usage["stored_vectors"] += stored
                if usage["new_api_batches"] % 250 == 0:
                    print(f"Production progress: {dict(usage)}", flush=True)
                write_progress(
                    report_path,
                    {
                        "status": status,
                        "current_run": dict(usage),
                        "run_history": history,
                        "wall_seconds": time.perf_counter() - started,
                    },
                )
                if (batch := next(batches, None)) is not None:
                    pending.append(submit(executor, batch))
        status = "complete"
    except Exception as exc:
        status, error_type = "failed", type(exc).__name__
        raise
    finally:
        for provider in providers:
            provider.close()
        conn.rollback()
        conn.execute("SELECT pg_advisory_unlock(74501903)")
        conn.commit()
        usage["estimated_usd"] = usage["new_usage_tokens"] / 1e6 * 0.02
        result = {
            "status": status,
            "error_type": error_type,
            "current_run": dict(usage),
            "wall_seconds": time.perf_counter() - started,
            "run_history": [
                *history,
                {"status": status, "wall_seconds": time.perf_counter() - started, **dict(usage)},
            ],
        }
        write_progress(report_path, result)
    return result
