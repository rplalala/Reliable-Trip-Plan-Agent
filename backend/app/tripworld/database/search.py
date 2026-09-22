"""Exact pgvector retrieval after generic geographic and structured policy filters."""

import numpy as np
from pgvector.psycopg import register_vector

from backend.app.tripworld.database.policy import POLICY_VERSION, normalized_name
from backend.app.tripworld.database.vectors import SPACE_ID, validate_space
from backend.app.tripworld.retrieval.embedding import validate_vectors
from backend.app.tripworld.retrieval.geography import GeographicScope, bounding_box

DISTANCE = """12742.0176 * asin(sqrt(least(1.0, greatest(0.0,
    power(sin(radians(latitude - %(lat)s) / 2), 2)
    + cos(radians(%(lat)s)) * cos(radians(latitude))
    * power(sin(radians(longitude - %(lon)s) / 2), 2)))))"""


def geographic_sql(scope: GeographicScope):
    low, high, width = bounding_box(scope)
    params = {
        "lat": scope.latitude,
        "lon": scope.longitude,
        "radius": scope.radius_km,
        "low": low,
        "high": high,
    }
    where = "latitude BETWEEN %(low)s AND %(high)s"
    if width < 180:
        left, right = scope.longitude - width, scope.longitude + width
        if left < -180:
            where += " AND (longitude >= %(left)s OR longitude <= %(right)s)"
            left += 360
        elif right > 180:
            where += " AND (longitude >= %(left)s OR longitude <= %(right)s)"
            right -= 360
        else:
            where += " AND longitude BETWEEN %(left)s AND %(right)s"
        params.update(left=left, right=right)
    if scope.country:
        where += " AND (country = %(country)s OR country IS NULL)"
        params["country"] = scope.country.strip().upper()
    return where, params


def search_query(scope, vector, top_k):
    if not isinstance(top_k, int) or not 1 <= top_k <= 1000:
        raise ValueError("Top-K must be between 1 and 1000")
    vector = np.asarray(vector, dtype=np.float32)
    validate_vectors(vector.reshape(1, -1), 1, 1536)
    where, params = geographic_sql(scope)
    params.update(vector=vector, space=SPACE_ID, k=top_k)
    query = f"""
        WITH geographic AS MATERIALIZED (
            SELECT retrieval_entity_id,text_hash,{DISTANCE} AS distance_km
            FROM tripworld.entities
            WHERE discovery_allowed AND {where}
        ), ranked AS MATERIALIZED (
            SELECT g.retrieval_entity_id,g.distance_km,
                   1 - (v.embedding <=> %(vector)s::vector) AS similarity_score
            FROM geographic g JOIN tripworld.embeddings v
                ON v.text_hash=g.text_hash AND v.space_id=%(space)s
            WHERE g.distance_km <= %(radius)s + 1e-9
            ORDER BY similarity_score DESC,g.retrieval_entity_id COLLATE "C"
            LIMIT %(k)s
        )
        SELECT r.*,e.metadata AS entity,e.artifact_hash AS retrieval_entity_artifact_hash,
               e.text_hash AS embedding_text_hash FROM ranked r
        JOIN tripworld.entities e USING (retrieval_entity_id)
        ORDER BY similarity_score DESC,retrieval_entity_id COLLATE "C"
    """
    return query, params


class PostgresSearch:
    def __init__(self, conn):
        self.conn = conn
        register_vector(conn)
        policies = conn.execute("SELECT DISTINCT policy_version FROM tripworld.entities").fetchall()
        if any(row["policy_version"] != POLICY_VERSION for row in policies):
            raise ValueError("Discovery policy version mismatch; re-ingest entity metadata")

    def search(self, vector, scope, top_k=10):
        validate_space(self.conn)
        query, params = search_query(scope, vector, top_k)
        rows = self.conn.execute(query, params).fetchall()
        return [{"rank": i, **row} for i, row in enumerate(rows, 1)]

    def counts(self, scope):
        where, params = geographic_sql(scope)
        return self.conn.execute(
            f"SELECT count(*) AS geographic_count, "
            f"count(*) FILTER (WHERE discovery_allowed) AS post_policy_count "
            f"FROM tripworld.entities WHERE {where} AND {DISTANCE} <= %(radius)s + 1e-9",
            params,
        ).fetchone()

    def lexical(self, name, scope, top_k=10):
        if not name.strip() or not 1 <= top_k <= 1000:
            raise ValueError("Nonempty name and Top-K 1..1000 are required")
        where, params = geographic_sql(scope)
        params.update(name=[normalized_name(name)], k=top_k)
        rows = self.conn.execute(
            f"SELECT retrieval_entity_id,metadata AS entity,{DISTANCE} AS distance_km, "
            "artifact_hash AS retrieval_entity_artifact_hash "
            f"FROM tripworld.entities WHERE discovery_allowed AND {where} "
            f"AND normalized_names @> %(name)s::text[] AND {DISTANCE} <= %(radius)s + 1e-9 "
            'ORDER BY distance_km,retrieval_entity_id COLLATE "C" LIMIT %(k)s',
            params,
        ).fetchall()
        return [{"rank": i, **row} for i, row in enumerate(rows, 1)]
