"""Tests for the pinned TripWorld source contract."""

from pathlib import Path

import httpx
import pyarrow as pa
import pytest
from pydantic import ValidationError

from backend.app.tripworld.manifest import SELECTED_FIELD_NAMES, TripWorldManifest
from tools.data.tripworld.source import SourceValidationError, download_source, validate_source_file
from tools.data.tripworld.source_schema import SourceSchemaError, validate_source_schema


def test_manifest_pins_source_and_exact_field_contract(
    tripworld_manifest: TripWorldManifest,
) -> None:
    assert tripworld_manifest.dataset.revision == ("421bc1dc63068bb398055b1ce987265fe22415db")
    assert tripworld_manifest.dataset.source_path == "metadata/metadata_all.parquet"
    assert tripworld_manifest.selected_field_names == SELECTED_FIELD_NAMES
    assert tripworld_manifest.dataset.download_url.endswith(
        "/421bc1dc63068bb398055b1ce987265fe22415db/metadata/metadata_all.parquet"
    )


def test_manifest_rejects_changed_field_order(
    tripworld_manifest: TripWorldManifest,
) -> None:
    payload = tripworld_manifest.model_dump(mode="json")
    payload["selected_fields"] = list(reversed(payload["selected_fields"]))
    with pytest.raises(ValidationError, match="fixed 11-field contract"):
        TripWorldManifest.model_validate(payload)


def test_source_validation_checks_checksum_schema_and_rows(
    tiny_source: Path,
    tiny_manifest: TripWorldManifest,
) -> None:
    validation = validate_source_file(tiny_source, tiny_manifest)
    assert validation.row_count == 6
    assert validation.sha256 == tiny_manifest.dataset.sha256


def test_source_validation_rejects_checksum_mismatch(
    tmp_path: Path,
    tiny_source: Path,
    tiny_manifest: TripWorldManifest,
) -> None:
    corrupt = tmp_path / "corrupt.parquet"
    content = bytearray(tiny_source.read_bytes())
    content[-1] ^= 1
    corrupt.write_bytes(content)
    with pytest.raises(SourceValidationError, match="checksum mismatch"):
        validate_source_file(corrupt, tiny_manifest)


def test_source_schema_rejects_missing_selected_field(
    tiny_manifest: TripWorldManifest,
) -> None:
    incomplete = pa.schema([pa.field("fsq_place_id", pa.string())])
    with pytest.raises(SourceSchemaError, match="missing field: fsq_name"):
        validate_source_schema(incomplete, tiny_manifest)


def test_download_uses_mock_transport_and_reuses_valid_file(
    tmp_path: Path,
    tiny_source: Path,
    tiny_manifest: TripWorldManifest,
) -> None:
    calls = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        assert str(request.url) == tiny_manifest.dataset.download_url
        return httpx.Response(200, content=tiny_source.read_bytes())

    destination = tmp_path / "metadata_all.parquet"
    first = download_source(
        tiny_manifest,
        destination,
        transport=httpx.MockTransport(handler),
    )
    second = download_source(
        tiny_manifest,
        destination,
        transport=httpx.MockTransport(handler),
    )
    assert first.downloaded is True
    assert second.downloaded is False
    assert calls == 1
