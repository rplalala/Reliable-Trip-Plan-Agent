"""Validated full-snapshot COPY ingestion with atomic upsert and removal of stale rows."""

from pathlib import Path
from time import perf_counter

import pyarrow.parquet as pq
from psycopg.types.json import Jsonb

from backend.app.tripworld.artifacts import load_json_object
from backend.app.tripworld.database.policy import POLICY_VERSION, exclusion_reasons, normalized_name
from backend.app.tripworld.database.policy import text_hash as hash_text
from backend.app.tripworld.hashing import sha256_file
from backend.app.tripworld.retrieval.entities import ENTITY_VERSION, TEXT_VERSION, RetrievalEntity

COLS = (
    "retrieval_entity_id,google_place_id,preferred_name,normalized_names,latitude,longitude,"
    "country,eligibility_hint,exclusion_reasons,policy_version,discovery_allowed,"
    "retrieval_text,text_hash,content_hash,artifact_hash,metadata"
)


def validate_artifact(path: Path) -> dict:
    meta = load_json_object(path.with_suffix(".parquet.manifest.json"))
    if sha256_file(path) != meta["output_sha256"]:
        raise ValueError("RetrievalEntity artifact hash mismatch")
    inputs = meta["inputs"]
    if (
        inputs["retrieval_entity_builder_version"] != ENTITY_VERSION
        or inputs["retrieval_text_template_version"] != TEXT_VERSION
    ):
        raise ValueError("Unsupported entity builder/text version")
    return meta


def ingest(conn, path: Path) -> dict:
    started = perf_counter()
    manifest = validate_artifact(path)
    artifact_hash = manifest["output_sha256"]
    count = 0
    with conn.transaction():
        conn.execute("SELECT pg_advisory_xact_lock(74501903)")
        conn.execute("SELECT pg_advisory_xact_lock(74501902)")
        conn.execute(
            "INSERT INTO tripworld.corpus_builds(artifact_hash,manifest,row_count) "
            "VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
            (artifact_hash, Jsonb(manifest), manifest["entity_count"]),
        )
        conn.execute("CREATE TEMP TABLE incoming (LIKE tripworld.entities) ON COMMIT DROP")
        with conn.cursor().copy(f"COPY incoming ({COLS}) FROM STDIN") as copy:
            for batch in pq.ParquetFile(path).iter_batches(batch_size=4096):
                for row in batch.to_pylist():
                    e = RetrievalEntity.model_validate(row)
                    for field in (
                        "tripworld_revision",
                        "semantic_mapping_version",
                        "retrieval_entity_builder_version",
                        "retrieval_text_template_version",
                    ):
                        if getattr(e, field) != manifest["inputs"][field]:
                            raise ValueError("Entity/manifest version mismatch")
                    reasons = exclusion_reasons(e)
                    names = sorted(
                        {normalized_name(n) for n in (e.preferred_name, *e.aliases) if n}
                    )
                    copy.write_row(
                        (
                            e.retrieval_entity_id,
                            e.google_place_id,
                            e.preferred_name,
                            names,
                            e.latitude,
                            e.longitude,
                            e.country.upper() if e.country else None,
                            e.eligibility_hint,
                            reasons,
                            POLICY_VERSION,
                            not reasons,
                            e.retrieval_text,
                            hash_text(e.retrieval_text),
                            e.content_hash,
                            artifact_hash,
                            Jsonb(e.model_dump(mode="json")),
                        )
                    )
                    count += 1
        if count != manifest["entity_count"]:
            raise ValueError("Entity count mismatch")
        if conn.execute(
            "SELECT count(*) AS n FROM (SELECT retrieval_entity_id FROM incoming "
            "GROUP BY retrieval_entity_id HAVING count(*)>1) duplicates"
        ).fetchone()["n"]:
            raise ValueError("Duplicate incoming entity IDs")
        assignments = ",".join(f"{c}=EXCLUDED.{c}" for c in COLS.split(",")[1:])
        changed = conn.execute(
            f"INSERT INTO tripworld.entities ({COLS}) SELECT {COLS} FROM incoming "
            f"ON CONFLICT (retrieval_entity_id) DO UPDATE SET {assignments} "
            "WHERE tripworld.entities.content_hash <> EXCLUDED.content_hash "
            "OR tripworld.entities.artifact_hash <> EXCLUDED.artifact_hash "
            "OR tripworld.entities.policy_version <> EXCLUDED.policy_version"
        ).rowcount
        removed = conn.execute(
            "DELETE FROM tripworld.entities e WHERE NOT EXISTS "
            "(SELECT 1 FROM incoming i WHERE i.retrieval_entity_id=e.retrieval_entity_id)"
        ).rowcount
    conn.commit()
    conn.execute("ANALYZE tripworld.entities")
    conn.commit()
    return {
        "rows": count,
        "changed": changed,
        "removed": removed,
        "artifact_hash": artifact_hash,
        "seconds": perf_counter() - started,
    }
