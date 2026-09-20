"""Content-addressed production vectors; model space is independent of job settings."""










from backend.app.tripworld.artifacts import payload_fingerprint

SPACE = {
    "provider": "openai",
    "model": "text-embedding-3-small",
    "dimensions": 1536,
    "dimensions_parameter": None,
    "metric": "cosine",
    "normalize": True,
    "query_prefix": "",
    "document_prefix": "",
    "variant": "enriched",
    "version": "tripworld-production-embedding-v1",
}


SPACE_ID = payload_fingerprint(SPACE)




def validate_space(conn):
    row = conn.execute(
        "SELECT configuration FROM tripworld.embedding_spaces WHERE space_id=%s", (SPACE_ID,)
    ).fetchone()
    if row is None or row["configuration"] != SPACE:
        raise ValueError("Embedding space compatibility mismatch")
