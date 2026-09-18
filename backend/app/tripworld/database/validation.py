"""Engineering validation of full DB retrieval, not a formal relevance benchmark."""

import time
from pathlib import Path

import numpy as np

from backend.app.tripworld.artifacts import load_json_object, write_json_if_changed
from backend.app.tripworld.database.policy import exclusion_reasons
from backend.app.tripworld.database.search import PostgresSearch, geographic_sql, search_query
from backend.app.tripworld.database.vectors import SPACE_ID
from backend.app.tripworld.retrieval.embedding import EmbeddingConfig, encode_resumable
from backend.app.tripworld.retrieval.entities import RetrievalEntity
from backend.app.tripworld.retrieval.estimation import tokenizer
from backend.app.tripworld.retrieval.geography import GeographicScope, haversine_km


def validate_database(conn, root: Path) -> dict:
    search = PostgresSearch(conn)
    missing = conn.execute(
        "SELECT count(*) AS n FROM tripworld.entities e WHERE discovery_allowed "
        "AND NOT EXISTS (SELECT 1 FROM tripworld.embeddings v "
        "WHERE v.text_hash=e.text_hash AND v.space_id=%s)",
        (SPACE_ID,),
    ).fetchone()["n"]
    if missing:
        raise ValueError(f"Production build incomplete: {missing} entity vectors missing")
    config = EmbeddingConfig.model_validate_json(
        (root / "embedding_model.v1.json").read_text(encoding="utf-8")
    )

    class CachedQueriesOnly:
        def encode(self, *_args, **_kwargs):
            raise ValueError(
                "Phase 4 query cache is missing; no validation API calls authorized here"
            )

    provider = CachedQueriesOnly()
    provider.config = config
    queries = [
        {"intent": row["intent"], "language": language, "text": row[language]}
        for row in load_json_object(root / "retrieval_queries.v1.json")["queries"]
        for language in ("en", "zh")
    ]
    encoding = tokenizer()
    vectors, _ = encode_resumable(
        [q["text"] for q in queries],
        provider,
        root / "artifacts/phase4/checkpoints",
        query=True,
        token_counts=[len(encoding.encode_ordinary(q["text"])) for q in queries],
    )
    destinations = load_json_object(root / "artifacts/phase4/destinations.json")["destinations"]
    cases, timings, explanations, lexical = [], [], [], []
    conn.execute("ANALYZE tripworld.embeddings")
    conn.commit()
    for dest in destinations:
        scope = GeographicScope.model_validate(dest["scope"])
        for radius in (5, 15, 30):
            area = scope.model_copy(update={"radius_km": radius})
            counts = search.counts(area)
            # First touch is not an OS-cache flush; report its limited meaning explicitly.
            for index in (0, 3):
                query, params = search_query(area, vectors[index], 10)
                plan = conn.execute(
                    "EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) " + query, params
                ).fetchone()["QUERY PLAN"][0]
                explanations.append(
                    {
                        "destination": dest["label"],
                        "radius_km": radius,
                        "query": queries[index],
                        "plan": plan,
                    }
                )
                elapsed, sql_times = [], []
                for _ in range(5):
                    started = time.perf_counter()
                    warm = conn.execute(
                        "EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) " + query, params
                    ).fetchone()["QUERY PLAN"][0]
                    elapsed.append((time.perf_counter() - started) * 1000)
                    sql_times.append(warm["Execution Time"])
                timings.append(
                    {
                        "destination": dest["label"],
                        "country": dest["country"],
                        "radius_km": radius,
                        "query": queries[index],
                        **counts,
                        "first_touch_sql_ms": plan["Execution Time"],
                        "warm_sql_ms": sql_times,
                        "warm_sql_p50_ms": float(np.percentile(sql_times, 50)),
                        "warm_sql_p95_ms": float(np.percentile(sql_times, 95)),
                        "warm_client_ms": elapsed,
                    }
                )
        for query, vector in zip(queries, vectors, strict=True):
            hits = search.search(vector, scope, 20)
            ids = [h["retrieval_entity_id"] for h in hits]
            assert len(ids) == len(set(ids))
            for h in hits:
                entity = RetrievalEntity.model_validate(h["entity"])
                assert not exclusion_reasons(entity)
                assert (
                    haversine_km(scope.latitude, scope.longitude, entity.latitude, entity.longitude)
                    <= scope.radius_km + 1e-9
                )
            cases.append(
                {
                    "destination": dest["label"],
                    "country": dest["country"],
                    "query": query,
                    "results": hits,
                }
            )
        example = cases[-24]["results"][0]["entity"]
        for name in (example["preferred_name"], *example["aliases"][:1]):
            if name:
                hits = search.lexical(name, scope)
                assert any(
                    h["entity"]["retrieval_entity_id"] == example["retrieval_entity_id"]
                    for h in hits
                )
                lexical.append({"destination": dest["label"], "name": name, "hits": hits})
        print(f"Validated database destination: {dest['country']}", flush=True)
    # Independent NumPy exact ranking over a complete medium-density 15 km pool.
    scope = GeographicScope.model_validate(destinations[2]["scope"])
    where, params = geographic_sql(scope)
    params["space"] = SPACE_ID
    rows = conn.execute(
        f"SELECT e.retrieval_entity_id,e.latitude,e.longitude,v.embedding "
        f"FROM tripworld.entities e JOIN tripworld.embeddings v USING(text_hash) "
        f"WHERE e.discovery_allowed AND {where} AND v.space_id=%(space)s",
        params,
    ).fetchall()
    rows = [
        r
        for r in rows
        if haversine_km(scope.latitude, scope.longitude, r["latitude"], r["longitude"])
        <= scope.radius_km + 1e-9
    ]
    scores = np.array([r["embedding"].to_numpy() for r in rows]) @ vectors[0]
    order = np.lexsort((np.array([r["retrieval_entity_id"] for r in rows]), -scores))[:20]
    actual = search.search(vectors[0], scope, 20)
    assert [rows[i]["retrieval_entity_id"] for i in order] == [
        h["retrieval_entity_id"] for h in actual
    ]
    report = {
        "case_count": len(cases),
        "cases": cases,
        "benchmarks": timings,
        "lexical": lexical,
        "explain_analyze": explanations,
        "numpy_exact_top20_match": True,
        "cold_caveat": "First-touch after embedding build; shared/OS caches not flushed",
        "database_bytes": conn.execute(
            "SELECT pg_database_size(current_database()) AS n"
        ).fetchone()["n"],
        "tables": conn.execute(
            "SELECT relname,pg_total_relation_size(relid) AS bytes "
            "FROM pg_catalog.pg_statio_user_tables WHERE schemaname='tripworld'"
        ).fetchall(),
        "indexes": conn.execute(
            "SELECT indexname,indexdef FROM pg_indexes WHERE schemaname='tripworld'"
        ).fetchall(),
    }
    write_json_if_changed(root / "reports/phase5_validation.json", report)
    return {k: v for k, v in report.items() if k not in ("cases", "explain_analyze", "lexical")}
