"""Metadata-only runtime observations and explicitly enabled development vectors."""

import asyncio
import hashlib
import json
from contextlib import contextmanager
from pathlib import Path
from time import perf_counter
from uuid import uuid4

import numpy as np

from backend.app.tripworld.database.vectors import SPACE, SPACE_ID


@contextmanager
def measure(records, stage):
    row = {"stage": stage, "status": "running"}
    records.append(row)
    started = perf_counter()
    try:
        yield row
        row["status"] = "completed"
    except BaseException as exc:
        row.update(
            status="cancelled" if isinstance(exc, asyncio.CancelledError) else "failed",
            exception_type=type(exc).__name__,
            sqlstate=getattr(exc, "sqlstate", None),
        )
        raise
    finally:
        row["seconds"] = perf_counter() - started


def capture_vectors(directory, texts, vectors, artifact_hash):
    """No raw text; hashes link the batch to separately authorized request capture."""
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    metadata = {
        "version": "runtime_query_capture_1",
        "space": SPACE,
        "space_id": SPACE_ID,
        "artifact_hash": artifact_hash,
        "text_sha256": [hashlib.sha256(t.encode()).hexdigest() for t in texts],
        "vectors_sha256": hashlib.sha256(vectors.tobytes()).hexdigest(),
        "shape": list(vectors.shape),
        "dtype": str(vectors.dtype),
    }
    path = target / f"query-{uuid4().hex}.npz"
    with path.open("xb") as stream:
        np.savez(stream, vectors=vectors, metadata=json.dumps(metadata, sort_keys=True))
    return path.name
