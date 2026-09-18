"""Global entity, geography, artifact, and exact-search contract tests."""

import json
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq
import pytest
from pydantic import ValidationError

from backend.app.tripworld.artifacts import write_json_if_changed
from backend.app.tripworld.corpus import build_corpus
from backend.app.tripworld.preprocessing import project_source
from backend.app.tripworld.retrieval.embedding import (
    EmbeddingConfig,
    EncodedBatch,
    build_embeddings,
    embedding_inputs,
    load_embeddings,
    validate_vectors,
)
from backend.app.tripworld.retrieval.entities import (
    RetrievalEntity,
    build_entities,
    merge_entity,
    stable_union,
)
from backend.app.tripworld.retrieval.geography import (
    GeographicScope,
    haversine_km,
    in_bounding_box,
    in_radius,
)
from backend.app.tripworld.retrieval.sampling import geographic_mask
from backend.app.tripworld.retrieval.search import DiscoveryIntent, ExactIndex
from backend.app.tripworld.source import sha256_file


def source_row(fsq: str, google: str | None = "g", **overrides) -> dict:
    return {
        "fsq_place_id": fsq,
        "google_place_id": google,
        "fsq_name": "Museum",
        "google_name": "The Museum",
        "fsq_latitude": 10.0,
        "fsq_longitude": 20.0,
        "fsq_locality": "Example",
        "fsq_region": "Region",
        "fsq_country": "ZZ",
        "normalized_fsq_categories": ["Arts > Museum"],
        "normalized_google_categories": ["Museum"],
        "direct_semantics": ["exhibitions"],
        "inferred_semantics": ["indoor visit"],
        "semantic_rule_ids": ["museum"],
        "semantic_eligibility_hints": ["eligible"],
        **overrides,
    }


def test_google_group_merge_order_alias_category_semantic_determinism(tiny_manifest):
    rows = [
        source_row("a"),
        source_row(
            "b",
            fsq_name="Alternative Museum",
            google_name="the museum",
            normalized_fsq_categories=["arts > museum", "Gallery"],
            normalized_google_categories=["Art gallery", "museum"],
            direct_semantics=["exhibitions", "art"],
        ),
    ]
    entity = merge_entity(rows, tiny_manifest)
    assert entity == merge_entity(list(reversed(rows)), tiny_manifest)
    assert entity.retrieval_entity_id == "google:g"
    assert entity.source_fsq_place_ids == ("a", "b")
    assert entity.preferred_name == "The Museum"
    assert entity.aliases == ("Alternative Museum", "Museum")
    assert entity.fsq_categories == ("Arts > Museum", "Gallery")
    assert entity.google_categories == ("Art gallery", "Museum")
    assert entity.direct_semantics == ("art", "exhibitions")
    assert entity.retrieval_text != entity.raw_retrieval_text
    assert "indoor visit" not in entity.raw_retrieval_text
    assert "google:g" not in entity.retrieval_text
    assert "20.0" not in entity.retrieval_text


def test_fsq_only_and_blank_google_ids_preserved(tiny_manifest):
    assert merge_entity([source_row("a", None)], tiny_manifest).retrieval_entity_id == "fsq:a"
    assert merge_entity([source_row("b", " ")], tiny_manifest).retrieval_entity_id == "fsq:b"
    with pytest.raises(ValueError, match="identity group"):
        merge_entity([source_row("a", None), source_row("b", None)], tiny_manifest)


def test_coordinate_medoid_and_country_conflicts(tiny_manifest):
    rows = [
        source_row("a"),
        source_row("b", fsq_longitude=20.01),
        source_row("c", fsq_longitude=80, fsq_country="YY"),
    ]
    entity = merge_entity(rows, tiny_manifest)
    assert entity.longitude == 20.01
    assert entity.coordinate_spread_km > 100
    assert "country_conflict" in entity.location_flags
    assert "coordinate_spread_over_10km" in entity.location_flags
    assert entity.countries == ("YY", "ZZ")
    assert entity.country == "ZZ"


def test_missing_invalid_coordinates_and_mixed_eligibility(tiny_manifest):
    entity = merge_entity(
        [
            source_row("a", fsq_latitude=float("nan")),
            source_row("b", fsq_latitude=100, semantic_eligibility_hints=["ineligible"]),
        ],
        tiny_manifest,
    )
    assert entity.latitude is None and entity.longitude is None
    assert entity.eligibility_hint == "unknown"
    assert entity.location_flags == ("missing_valid_coordinates",)


def test_unicode_union_is_order_independent():
    values = [" Museum ", "museum", "Ａrt", "Art", None, ""]
    assert stable_union(values) == stable_union(reversed(values)) == ("Art", "Museum")


@pytest.mark.parametrize(
    "center,inside,outside",
    [
        ((0, 179.9), (0, -179.9), (0, -178)),
        ((89.9, 0), (89.9, 180), (88, 0)),
        ((-89.9, 90), (-89.9, -90), (-88, 90)),
        ((0, 0), (0.1, 0.1), (1, 1)),
    ],
)
def test_global_bounding_box_and_haversine_poles_dateline(center, inside, outside):
    scope = GeographicScope(latitude=center[0], longitude=center[1], radius_km=30)
    assert in_bounding_box(*inside, scope)
    assert in_radius(*inside, scope)
    assert not in_radius(*outside, scope)
    assert haversine_km(*center, *inside) <= 30


def test_bounding_box_coarse_filter_requires_exact_radius():
    scope = GeographicScope(latitude=0, longitude=0, radius_km=100)
    assert in_bounding_box(0.8, 0.8, scope)
    assert not in_radius(0.8, 0.8, scope)
    coarse, exact = geographic_mask(
        np.array([0.8, 0.1, np.nan]),
        np.array([0.8, 0.1, 1.0]),
        np.array(["ZZ", "ZZ", "ZZ"]),
        scope,
    )
    assert coarse.tolist() == [True, True, False]
    assert exact.tolist() == [False, True, False]


def test_country_missing_metadata_and_radius_boundary():
    scope = GeographicScope(latitude=10, longitude=20, radius_km=1, country="ZZ")
    _, exact = geographic_mask(
        np.array([10.0, 10.0, 10.0]),
        np.array([20.0, 20.0, 20.0]),
        np.array(["zz", None, "AA"], dtype=object),
        scope,
    )
    assert exact.tolist() == [True, True, False]
    with pytest.raises(ValidationError):
        GeographicScope(latitude=91, longitude=20, radius_km=1)


def test_exact_cosine_ranking_ties_topk_and_eligibility(tiny_manifest):
    rows = [
        source_row("b", "b"),
        source_row("a", "a"),
        source_row(
            "c",
            "c",
            semantic_eligibility_hints=["ineligible"],
        ),
        source_row("d", "d", semantic_eligibility_hints=[]),
    ]
    entities = [merge_entity([row], tiny_manifest) for row in rows]
    vectors = np.array([[1, 0], [1, 0], [0, 1], [0.6, 0.8]], dtype=np.float32)
    index = ExactIndex(entities, vectors, "raw", {})
    scope = GeographicScope(latitude=10, longitude=20, radius_km=5)
    result = index.search(np.array([2, 0]), scope, 2)
    assert [r["entity"]["google_place_id"] for r in result["results"]] == ["a", "b"]
    assert [r["similarity_score"] for r in result["results"]] == [1, 1]
    filtered = index.search(np.array([0, 1]), scope, 10, exclude_ineligible=True)
    assert len(filtered["results"]) == 3
    assert filtered["results"][0]["entity"]["eligibility_hint"] == "unknown"
    assert filtered["results"][0]["entity"]["google_place_id"] == "d"
    with pytest.raises(ValueError):
        index.search(np.zeros(2), scope, 1)
    with pytest.raises(ValueError):
        index.search(np.ones(2), scope, 0)
    with pytest.raises(ValueError, match="Duplicate"):
        ExactIndex([entities[0], entities[0]], vectors[:2], "raw", {})


def test_empty_geographic_results_and_query_construction(tiny_manifest):
    entity = merge_entity([source_row("a")], tiny_manifest)
    index = ExactIndex([entity], np.array([[1.0, 0.0]], dtype=np.float32), "raw", {})
    scope = GeographicScope(latitude=-40, longitude=-70, radius_km=1)
    assert index.search(np.ones(2), scope, 20)["results"] == []
    assert DiscoveryIntent(semantic_query="  quiet   places ").query_text() == "quiet places"
    with pytest.raises(ValueError):
        DiscoveryIntent(semantic_query=" ").query_text()


@pytest.fixture
def built_entities(tmp_path, tiny_source, tiny_manifest, semantic_mapping):
    selected = tmp_path / "selected.parquet"
    corpus = tmp_path / "corpus.parquet"
    output = tmp_path / "entities.parquet"
    project_source(tiny_source, selected, tiny_manifest)
    build_corpus(selected, corpus, tiny_manifest, semantic_mapping)
    metadata = build_entities(corpus, output, tiny_manifest)
    return corpus, output, metadata


def test_global_entity_artifact_grouping_idempotence_and_mismatch(built_entities, tiny_manifest):
    corpus, output, metadata = built_entities
    assert metadata["source_row_count"] == 6
    assert metadata["entity_count"] == 5
    assert metadata["google_backed_count"] == 3
    assert metadata["fsq_only_count"] == 2
    assert metadata["duplicate_row_reduction"] == 1
    timestamp = output.stat().st_mtime_ns
    assert build_entities(corpus, output, tiny_manifest)["reused"]
    assert timestamp == output.stat().st_mtime_ns
    entities = [RetrievalEntity.model_validate(row) for row in pq.read_table(output).to_pylist()]
    assert len({entity.retrieval_entity_id for entity in entities}) == 5
    sidecar = corpus.with_suffix(".parquet.manifest.json")
    payload = json.loads(sidecar.read_text())
    payload["inputs"]["semantic_mapping_version"] = "wrong"
    write_json_if_changed(sidecar, payload)
    with pytest.raises(ValueError, match="version mismatch"):
        build_entities(corpus, output, tiny_manifest)


def test_rebuild_after_source_reordering_is_byte_identical(
    built_entities,
    tiny_manifest,
    tmp_path,
):
    corpus, output, _ = built_entities
    expected = sha256_file(output)
    table = pq.read_table(corpus)
    pq.write_table(table.take(list(reversed(range(table.num_rows)))), corpus)
    sidecar = corpus.with_suffix(".parquet.manifest.json")
    metadata = json.loads(sidecar.read_text())
    metadata["output_sha256"] = sha256_file(corpus)
    write_json_if_changed(sidecar, metadata)
    other = tmp_path / "reordered.parquet"
    build_entities(corpus, other, tiny_manifest)
    assert sha256_file(other) == expected


class FakeEmbedding:
    def __init__(self):
        root = Path(__file__).resolve().parents[3]
        self.config = EmbeddingConfig.model_validate_json(
            (root / "data/tripworld/embedding_model.v1.json").read_text()
        )
        self.calls = 0

    def encode(self, texts, *, query=False):
        self.calls += 1
        vectors = np.zeros((len(texts), 1536), dtype=np.float32)
        for i, text in enumerate(texts):
            vectors[i, len(text) % 1536] = 1
        return EncodedBatch(vectors, 10, 10, self.config.model_name)


def test_embedding_variants_metadata_idempotence_and_corruption(built_entities, tmp_path):
    _, output, metadata = built_entities
    entities = [RetrievalEntity.model_validate(row) for row in pq.read_table(output).to_pylist()]
    provider = FakeEmbedding()
    hashes = {}
    for variant in ("raw", "enriched"):
        result = build_embeddings(
            entities, variant, provider, tmp_path, metadata, "sample", token_counts=[10] * 5
        )
        assert not result["reused"]
        inputs = embedding_inputs(entities, variant, provider.config, metadata, "sample")
        vectors, _ = load_embeddings(tmp_path / f"{variant}.npy", inputs)
        assert vectors.shape == (5, 1536)
        del vectors
        hashes[variant] = inputs["content_hash"]
        reused = build_embeddings(
            entities, variant, provider, tmp_path, metadata, "sample", token_counts=[10] * 5
        )
        assert reused["reused"]
        assert reused["new_api_batches"] == reused["new_usage_tokens"] == 0
        assert reused["estimated_new_cost_usd"] == 0
        assert reused["artifact_creation_usage"]["new_api_batches"] == 1
    assert provider.calls == 2
    assert hashes["raw"] != hashes["enriched"]
    wrong = embedding_inputs(entities, "enriched", provider.config, metadata, "sample")
    with pytest.raises(ValueError, match="mismatch"):
        load_embeddings(tmp_path / "raw.npy", wrong)
    path = tmp_path / "enriched.npy"
    path.write_bytes(path.read_bytes() + b"corruption")
    with pytest.raises(ValueError, match="mismatch"):
        load_embeddings(path, wrong)


def test_model_contract_rejects_unapproved_dimensions_and_bad_vectors():
    config = FakeEmbedding().config.model_dump()
    config["dimension"] = 768
    with pytest.raises(ValidationError):
        EmbeddingConfig.model_validate(config)
    with pytest.raises(ValueError, match="normalized"):
        validate_vectors(np.zeros((1, 1536), dtype=np.float32), 1, 1536)
    with pytest.raises(ValueError, match="nonfinite"):
        validate_vectors(np.full((1, 1536), np.nan, dtype=np.float32), 1, 1536)
