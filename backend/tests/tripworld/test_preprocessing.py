"""Tests for the exact TripWorld source projection."""

from pathlib import Path

import pyarrow.parquet as pq

from backend.app.tripworld.manifest import SELECTED_FIELD_NAMES, TripWorldManifest
from backend.app.tripworld.preprocessing import project_source, validate_projected_file


def test_projection_keeps_only_fixed_fields_and_is_idempotent(
    tmp_path: Path,
    tiny_source: Path,
    tiny_manifest: TripWorldManifest,
) -> None:
    assert "unused_source_field" in pq.ParquetFile(tiny_source).schema_arrow.names
    output = tmp_path / "selected.parquet"
    first = project_source(tiny_source, output, tiny_manifest)
    first_modified_ns = output.stat().st_mtime_ns
    second = project_source(tiny_source, output, tiny_manifest)

    assert first.reused is False
    assert second.reused is True
    assert second.sha256 == first.sha256
    assert output.stat().st_mtime_ns == first_modified_ns
    assert pq.ParquetFile(output).schema_arrow.names == list(SELECTED_FIELD_NAMES)
    assert validate_projected_file(output, tiny_manifest).num_rows == 6
