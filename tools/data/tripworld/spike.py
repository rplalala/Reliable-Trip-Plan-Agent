"""Bounded multilingual RAW/ENRICHED development diagnostics, not a formal benchmark."""

from pathlib import Path

import pyarrow.parquet as pq

from backend.app.tripworld.artifacts import load_json_object
from backend.app.tripworld.hashing import sha256_file
from backend.app.tripworld.retrieval.entities import RetrievalEntity
from backend.app.tripworld.retrieval.geography import GeographicScope
from tools.data.tripworld.artifact_persistence import write_json_if_changed
from tools.data.tripworld.embedding_build import (
    build_embeddings,
    embedding_inputs,
    encode_resumable,
    load_embeddings,
)
from tools.data.tripworld.embedding_config import EmbeddingConfig
from tools.data.tripworld.estimation import tokenizer
from tools.data.tripworld.openai_adapter import OpenAIEmbeddingAdapter
from tools.data.tripworld.search import DiscoveryIntent, ExactIndex


def run_spike(root: Path, *, batch_size: int = 64) -> dict:
    directory = root / "artifacts" / "phase4"
    selection = load_json_object(directory / "destinations.json")
    entity_path = root / "artifacts" / "retrieval_entities.parquet"
    entity_meta = load_json_object(entity_path.with_suffix(".parquet.manifest.json"))
    if sha256_file(entity_path) != selection["entity_artifact_sha256"]:
        raise ValueError("Sample references a different global entity artifact")
    sample = directory / "sample_entities.parquet"
    sample_hash = sha256_file(sample)
    if sample_hash != selection["sample_artifact_sha256"]:
        raise ValueError("Sample artifact hash mismatch")
    entities = [RetrievalEntity.model_validate(row) for row in pq.read_table(sample).to_pylist()]
    if len(entities) > 2500:
        raise ValueError(
            "Phase 4 spike is limited to 2500 entities; full-global run is not enabled"
        )
    config = EmbeddingConfig.model_validate_json((root / "embedding_model.v1.json").read_text())
    encoding = tokenizer()
    estimate_path = root / "reports" / "phase4_cost_estimate.json"
    estimate = load_json_object(estimate_path)
    if estimate["entity_artifact_sha256"] != entity_meta["output_sha256"]:
        raise ValueError("Run the global cost estimate for this entity artifact before the spike")
    token_counts = {
        variant: [
            len(
                encoding.encode_ordinary(
                    entity.raw_retrieval_text if variant == "raw" else entity.retrieval_text
                )
            )
            for entity in entities
        ]
        for variant in ("raw", "enriched")
    }
    query_config = load_json_object(root / "retrieval_queries.v1.json")
    queries = [
        {
            "intent": item["intent"],
            "language": language,
            "text": DiscoveryIntent(semantic_query=item[language]).query_text(),
        }
        for item in query_config["queries"]
        for language in ("en", "zh")
    ]
    query_texts = [query["text"] for query in queries]
    query_token_counts = [len(encoding.encode_ordinary(text)) for text in query_texts]
    projected_cost = (
        (sum(sum(values) for values in token_counts.values()) + sum(query_token_counts))
        / 1e6
        * (config.input_usd_per_million_tokens)
    )
    if projected_cost * config.max_attempts > config.max_run_usd:
        raise ValueError("Combined RAW/ENRICHED worst-case retry budget exceeded")
    provider = OpenAIEmbeddingAdapter(config)
    index_by_variant = {}
    embedding_reports = {}
    for variant in ("raw", "enriched"):
        embedding_reports[variant] = build_embeddings(
            entities,
            variant,
            provider,
            directory,
            entity_meta,
            sample_hash,
            batch_size=batch_size,
            token_counts=token_counts[variant],
        )
        expected = embedding_inputs(entities, variant, config, entity_meta, sample_hash)
        vectors, metadata = load_embeddings(directory / f"{variant}.npy", expected)
        index_by_variant[variant] = ExactIndex(entities, vectors, variant, metadata)
    query_vectors, query_usage = encode_resumable(
        query_texts,
        provider,
        directory / "checkpoints",
        query=True,
        token_counts=query_token_counts,
    )
    provider.close()
    cases = []
    differences = []
    for destination in selection["destinations"]:
        scope = GeographicScope.model_validate(destination["scope"])
        for query, vector in zip(queries, query_vectors, strict=True):
            before_after = {}
            for variant, index in index_by_variant.items():
                for filtered in (False, True):
                    result = index.search(vector, scope, 20, exclude_ineligible=filtered)
                    before_after[(variant, filtered)] = result
                    diagnostics = {}
                    for k in (5, 10, 20):
                        hits = result["results"][:k]
                        ids = [r["entity"]["retrieval_entity_id"] for r in hits]
                        diagnostics[str(k)] = {
                            "returned": len(hits),
                            "duplicate_count": len(ids) - len(set(ids)),
                            "ineligible_count": sum(
                                r["entity"]["eligibility_hint"] == "ineligible" for r in hits
                            ),
                            "unknown_count": sum(
                                r["entity"]["eligibility_hint"] == "unknown" for r in hits
                            ),
                            "location_anomaly_count": sum(
                                bool(r["entity"]["location_flags"]) for r in hits
                            ),
                            "geographic_violation_count": sum(
                                r["distance_km"] > scope.radius_km + 1e-9 for r in hits
                            ),
                            "score_range": (
                                [hits[-1]["similarity_score"], hits[0]["similarity_score"]]
                                if hits
                                else []
                            ),
                        }
                    # Full diagnostic entity payloads remain in the generated report.
                    cases.append(
                        {
                            "destination": destination["label"],
                            "country": destination["country"],
                            "query": query,
                            **result,
                            "top_k_diagnostics": diagnostics,
                        }
                    )
            for filtered in (False, True):
                raw = before_after[("raw", filtered)]["results"]
                enriched = before_after[("enriched", filtered)]["results"]
                differences.append(
                    {
                        "destination": destination["label"],
                        "country": destination["country"],
                        "query": query,
                        "exclude_ineligible": filtered,
                        "top_k_id_overlap": {
                            str(k): len(
                                {r["entity"]["retrieval_entity_id"] for r in raw[:k]}
                                & {r["entity"]["retrieval_entity_id"] for r in enriched[:k]}
                            )
                            for k in (5, 10, 20)
                        },
                    }
                )
    report = {
        "spike_version": "tripworld-retrieval-spike-v1",
        "query_config": query_config,
        "selection": selection,
        "model_config": config.model_dump(),
        "query_usage": query_usage,
        "query_count": len(queries),
        "case_count": len(cases),
        "embedding_artifacts": embedding_reports,
        "differences": differences,
        "cases": cases,
        "full_global_estimates": {
            variant: {
                "seconds": (
                    entity_meta["entity_count"] / meta["documents_per_second"]
                    if meta["documents_per_second"]
                    else None
                ),
                "float32_vector_bytes": entity_meta["entity_count"] * config.dimension * 4,
                "caveat": "Sample API throughput extrapolation; account rate limits may dominate",
            }
            for variant, meta in embedding_reports.items()
        },
        "limits": (
            "Exact cosine over sampled destination pools; no judged relevance metric; no live "
            "Google validation. Inferred semantics are category priors, not POI facts. "
            "Top-K values are diagnostics, not runtime policy."
        ),
    }
    write_json_if_changed(root / "reports" / "phase4_spike.json", report)
    # A compact summary is suitable for terminal output; the full report remains local.
    summary = {
        k: v
        for k, v in report.items()
        if k
        not in (
            "cases",
            "differences",
            "selection",
            "embedding_artifacts",
            "query_config",
        )
    }
    summary["embedding_artifacts"] = {
        variant: {k: v for k, v in metadata.items() if k not in ("inputs", "checkpoints")}
        for variant, metadata in embedding_reports.items()
    }
    write_json_if_changed(root / "reports" / "phase4_summary.json", summary)
    return summary


def query_spike(
    root: Path,
    query: str,
    scope: GeographicScope,
    top_k: int,
    variant: str,
    *,
    exclude_ineligible: bool = False,
) -> dict:
    directory = root / "artifacts" / "phase4"
    sample = directory / "sample_entities.parquet"
    entities = [RetrievalEntity.model_validate(row) for row in pq.read_table(sample).to_pylist()]
    meta = load_json_object(root / "artifacts" / "retrieval_entities.parquet.manifest.json")
    config = EmbeddingConfig.model_validate_json((root / "embedding_model.v1.json").read_text())
    inputs = embedding_inputs(entities, variant, config, meta, sha256_file(sample))
    vectors, metadata = load_embeddings(directory / f"{variant}.npy", inputs)
    provider = OpenAIEmbeddingAdapter(config)
    text = DiscoveryIntent(semantic_query=query).query_text()
    encoding = tokenizer()
    vectors_query, usage = encode_resumable(
        [text],
        provider,
        directory / "checkpoints",
        query=True,
        token_counts=[len(encoding.encode_ordinary(text))],
    )
    provider.close()
    vector = vectors_query[0]
    index = ExactIndex(entities, vectors, variant, metadata)
    return {
        "semantic_query": text,
        "corpus_scope": "phase4_sample_only",
        "query_usage": usage,
        **index.search(vector, scope, top_k, exclude_ineligible=exclude_ineligible),
    }
