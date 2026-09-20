"""Content-addressed production vectors; model space is independent of job settings."""

import hashlib

import numpy as np
from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

from backend.app.tripworld.database.vectors import SPACE, SPACE_ID, validate_space
from backend.app.tripworld.retrieval.embedding import validate_vectors


def prepare_space(conn):
    register_vector(conn)
    conn.execute(
        "INSERT INTO tripworld.embedding_spaces VALUES (%s,%s) ON CONFLICT DO NOTHING",
        (SPACE_ID, Jsonb(SPACE)),
    )
    validate_space(conn)
    conn.commit()


def store_vectors(conn, hashes: list[str], vectors: np.ndarray, metadata: dict) -> int:
    validate_vectors(vectors, len(hashes), 1536)
    if len(set(hashes)) != len(hashes):
        raise ValueError("Duplicate vector text hashes")
    with conn.transaction():
        conn.execute(
            "CREATE TEMP TABLE vector_batch (LIKE tripworld.embeddings INCLUDING DEFAULTS) "
            "ON COMMIT DROP"
        )
        with conn.cursor().copy(
            "COPY vector_batch(space_id,text_hash,embedding,vector_hash,generation_metadata) "
            "FROM STDIN WITH (FORMAT BINARY)"
        ) as copy:
            copy.set_types(["text", "text", "vector", "text", "jsonb"])
            for digest, vector in zip(hashes, vectors, strict=True):
                copy.write_row(
                    (
                        SPACE_ID,
                        digest,
                        vector,
                        hashlib.sha256(vector.tobytes()).hexdigest(),
                        Jsonb(metadata),
                    )
                )
        count = conn.execute(
            "INSERT INTO tripworld.embeddings SELECT * FROM vector_batch "
            "ON CONFLICT (space_id,text_hash) DO NOTHING"
        ).rowcount
    conn.commit()
    return count
