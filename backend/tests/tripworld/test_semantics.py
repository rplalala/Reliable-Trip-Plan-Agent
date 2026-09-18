"""Tests for category normalization and retrieval-document semantics."""

from backend.app.tripworld.semantics import (
    CategorySemanticMapping,
    enrich_row,
    normalize_fsq_categories,
    normalize_google_categories,
)


def test_category_normalization_handles_nulls_hierarchy_and_serialized_lists() -> None:
    assert normalize_fsq_categories(None) == ()
    assert normalize_fsq_categories([" Arts  >  Museum ", "arts > museum", "Museum"]) == (
        "Arts > Museum",
        "Museum",
    )
    assert normalize_google_categories(
        ["Coffee_shop", "coffee shop", '["Art gallery", "Tourist attraction"]']
    ) == ("Coffee shop", "Art gallery", "Tourist attraction")


def test_semantic_enrichment_is_deterministic_and_separates_inference(
    semantic_mapping: CategorySemanticMapping,
) -> None:
    row = {
        "fsq_place_id": "hidden-fsq-id",
        "fsq_name": "Harbour Library",
        "fsq_latitude": -33.8,
        "fsq_longitude": 151.2,
        "fsq_locality": "Sydney",
        "fsq_region": "NSW",
        "fsq_country": "AU",
        "fsq_category_labels": ["Library", "Arts > Library"],
        "google_name": "harbour library",
        "google_categories": ["Public library"],
        "google_place_id": "hidden-google-id",
    }
    first = enrich_row(row, semantic_mapping)
    second = enrich_row(row, semantic_mapping)

    assert first == second
    assert first.semantic_rule_ids == ("library",)
    assert first.direct_semantics == ("books, reading, and research spaces",)
    assert "quiet indoor visit" in first.inferred_semantics
    assert "Alternative name:" not in first.retrieval_text
    assert "hidden-fsq-id" not in first.retrieval_text
    assert "hidden-google-id" not in first.retrieval_text
    assert "-33.8" not in first.retrieval_text
    assert "Potential travel uses inferred from category types" in (first.retrieval_description)


def test_multi_category_merge_deduplicates_semantics(
    semantic_mapping: CategorySemanticMapping,
) -> None:
    result = enrich_row(
        {
            "fsq_name": "Culture Stop",
            "fsq_category_labels": ["Museum", "Art Gallery", "Library"],
            "google_categories": ["Museum", "Public library"],
        },
        semantic_mapping,
    )
    assert result.semantic_rule_ids == ("museum", "art_gallery", "library")
    assert result.inferred_semantics.count("cultural visit") == 1
    assert result.inferred_semantics.count("indoor activity") == 1
    assert result.inferred_semantics.count("rainy-day option") == 1


def test_unknown_category_stays_searchable_without_invented_description(
    semantic_mapping: CategorySemanticMapping,
) -> None:
    result = enrich_row(
        {
            "fsq_name": "Unknown Place",
            "fsq_locality": "Somewhere",
            "fsq_category_labels": ["Unmapped Category"],
            "google_categories": None,
        },
        semantic_mapping,
    )
    assert result.semantic_rule_ids == ()
    assert result.direct_semantics == ()
    assert result.inferred_semantics == ()
    assert result.retrieval_description == ""
    assert "Unmapped Category" in result.retrieval_text
