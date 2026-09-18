"""Read-only production completeness, vector integrity, storage, and API usage audit."""

import json
from datetime import datetime
from pathlib import Path

import numpy as np

from backend.app.tripworld.artifacts import write_json_if_changed
from backend.app.tripworld.database.vectors import SPACE_ID


def audit(conn, root: Path) -> dict:
    usage = {}
    for path in (root / "artifacts/phase5/checkpoints").glob("*.npz"):
        with np.load(path, allow_pickle=False) as checkpoint:
            metadata = json.loads(str(checkpoint["metadata"].item()))
        key = metadata["request_id"] or path.name
        usage[key] = metadata
    timestamps = sorted(datetime.fromisoformat(m["created_at"]) for m in usage.values())
    counts = conn.execute(
        "SELECT count(*) AS entity_count, "
        "count(*) FILTER (WHERE discovery_allowed) AS production_entity_count "
        "FROM tripworld.entities"
    ).fetchone()
    vectors = conn.execute(
        "SELECT count(*) AS physical_vector_count, "
        "sum(pg_column_size(embedding)) AS payload_bytes, "
        "count(*) FILTER (WHERE vector_dims(embedding)<>1536 "
        "OR abs(vector_norm(embedding)-1)>0.00001) AS invalid_vector_count "
        "FROM tripworld.embeddings WHERE space_id=%s",
        (SPACE_ID,),
    ).fetchone()
    missing = conn.execute(
        "SELECT count(*) AS n FROM tripworld.entities e WHERE discovery_allowed "
        "AND NOT EXISTS (SELECT 1 FROM tripworld.embeddings v "
        "WHERE v.text_hash=e.text_hash AND v.space_id=%s)",
        (SPACE_ID,),
    ).fetchone()["n"]
    total_tokens = sum(m["total_tokens"] for m in usage.values())
    result = {
        **counts,
        **vectors,
        "missing_entity_vectors": missing,
        "observed_successful_api_requests": len(usage),
        "observed_api_attempts_for_saved_responses": sum(m["attempts"] for m in usage.values()),
        "observed_api_tokens": total_tokens,
        "estimated_observed_api_usd": total_tokens / 1e6 * 0.02,
        "first_checkpoint_at": timestamps[0].isoformat() if timestamps else None,
        "last_checkpoint_at": timestamps[-1].isoformat() if timestamps else None,
        "observed_generation_window_seconds": (timestamps[-1] - timestamps[0]).total_seconds()
        if timestamps
        else None,
        "accounting_caveat": "Saved API responses only; interrupted requests with lost responses "
        "may have been billed. Includes production timing probes, excludes reused Phase 4 vectors. "
        "Generation window includes pauses but excludes work before the first saved response.",
        "database_bytes": conn.execute(
            "SELECT pg_database_size(current_database()) AS n"
        ).fetchone()["n"],
        "tables": conn.execute(
            "SELECT relname,pg_total_relation_size(relid) AS bytes "
            "FROM pg_statio_user_tables WHERE schemaname='tripworld'"
        ).fetchall(),
    }
    write_json_if_changed(root / "reports/phase5_audit.json", result)
    return result
