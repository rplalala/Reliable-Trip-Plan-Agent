"""Tests for actual-profile metrics and retrieval-corpus artifacts."""

from pathlib import Path

import pyarrow.parquet as pq
import pytest

from backend.app.tripworld.manifest import SELECTED_FIELD_NAMES, TripWorldManifest
from tools.data.tripworld.corpus import DERIVED_FIELDS, build_corpus
from tools.data.tripworld.preprocessing import project_source
from tools.data.tripworld.profiling import (
    build_profile,
    render_profile_markdown,
    write_profile_outputs,
)
from tools.data.tripworld.semantics import CategorySemanticMapping


def _project_fixture(
    tmp_path: Path,
    tiny_source: Path,
    tiny_manifest: TripWorldManifest,
) -> Path:
    selected = tmp_path / "selected.parquet"
    project_source(tiny_source, selected, tiny_manifest)
    return selected


def test_profile_covers_geography_categories_and_identity_anomalies(
    tmp_path: Path,
    tiny_source: Path,
    tiny_manifest: TripWorldManifest,
) -> None:
    selected = _project_fixture(tmp_path, tiny_source, tiny_manifest)
    profile, taxonomy = build_profile(selected, tiny_manifest, batch_size=2)

    assert profile["row_count"] == 6
    assert profile["geography"]["australia"]["row_count"] == 5
    assert profile["geography"]["sydney"]["radius_counts"]["50"]["all_rows"] == 4
    assert profile["geography"]["sydney"]["radius_counts"]["50"]["retrieval_usable"] == 4
    assert profile["field_coverage"]["fsq_name"]["null_count"] == 0
    assert profile["field_coverage"]["fsq_name"]["blank_or_empty_count"] == 1
    assert profile["coordinates"]["invalid_or_missing_count"] == 1
    assert profile["identity"]["google_ids_with_multiple_fsq_ids_count"] == 1
    assert any(row["value"] == "Art gallery" for row in taxonomy["google_categories"])
    markdown = render_profile_markdown(profile)
    assert "Sydney geographic coverage" in markdown
    assert "Google Place IDs assigned to multiple FSQ IDs: **1**" in markdown


def test_profile_outputs_are_idempotent(
    tmp_path: Path,
    tiny_source: Path,
    tiny_manifest: TripWorldManifest,
) -> None:
    selected = _project_fixture(tmp_path, tiny_source, tiny_manifest)
    report_directory = tmp_path / "reports"
    paths = write_profile_outputs(selected, report_directory, tiny_manifest)
    modified_times = [path.stat().st_mtime_ns for path in paths]
    assert write_profile_outputs(selected, report_directory, tiny_manifest) == paths
    assert [path.stat().st_mtime_ns for path in paths] == modified_times


def test_corpus_keeps_metadata_builds_text_and_is_idempotent(
    tmp_path: Path,
    tiny_source: Path,
    tiny_manifest: TripWorldManifest,
    semantic_mapping: CategorySemanticMapping,
) -> None:
    selected = _project_fixture(tmp_path, tiny_source, tiny_manifest)
    output = tmp_path / "corpus.parquet"
    first = build_corpus(
        selected,
        output,
        tiny_manifest,
        semantic_mapping,
        batch_size=2,
    )
    first_modified_ns = output.stat().st_mtime_ns
    second = build_corpus(selected, output, tiny_manifest, semantic_mapping, batch_size=2)

    assert first.row_count == 6
    assert first.mapped_row_count == 5
    assert first.retrieval_text_count == 6
    assert second.reused is True
    assert output.stat().st_mtime_ns == first_modified_ns
    table = pq.read_table(output)
    assert table.schema.names == [*SELECTED_FIELD_NAMES, *DERIVED_FIELDS]
    rows = {row["fsq_place_id"]: row for row in table.to_pylist()}
    assert "Alternative name:" not in rows["fsq-1"]["retrieval_text"]
    assert "google-shared" not in rows["fsq-1"]["retrieval_text"]
    assert "151.2093" not in rows["fsq-1"]["retrieval_text"]
    assert rows["fsq-4"]["normalized_google_categories"] == [
        "Art gallery",
        "Tourist attraction",
    ]
    assert rows["fsq-5"]["retrieval_description"] == ""
    assert rows["fsq-6"]["semantic_eligibility_hints"] == ["ineligible"]


def test_corpus_rejects_mapping_version_mismatch(
    tmp_path: Path,
    tiny_source: Path,
    tiny_manifest: TripWorldManifest,
    semantic_mapping: CategorySemanticMapping,
) -> None:
    selected = _project_fixture(tmp_path, tiny_source, tiny_manifest)
    wrong_mapping = semantic_mapping.model_copy(update={"mapping_version": "other"})
    with pytest.raises(ValueError, match="mapping version"):
        build_corpus(selected, tmp_path / "corpus.parquet", tiny_manifest, wrong_mapping)
