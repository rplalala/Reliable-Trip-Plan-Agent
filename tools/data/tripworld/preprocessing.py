"""Exact 11-field TripWorld projection."""

import os
from dataclasses import dataclass
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from backend.app.tripworld.artifacts import load_json_object, payload_fingerprint
from backend.app.tripworld.hashing import sha256_file
from backend.app.tripworld.manifest import TripWorldManifest
from tools.data.tripworld.artifact_persistence import artifact_is_current, write_json_if_changed
from tools.data.tripworld.source import validate_source_file


@dataclass(frozen=True)
class ArtifactResult:
    path: Path
    metadata_path: Path
    row_count: int
    size_bytes: int
    sha256: str
    reused: bool


def _arrow_type(logical_type: str) -> pa.DataType:
    if logical_type == "string":
        return pa.string()
    if logical_type == "float64":
        return pa.float64()
    if logical_type == "list<string>":
        return pa.list_(pa.string())
    raise ValueError(f"Unsupported TripWorld logical type: {logical_type}")


def selected_arrow_schema(manifest: TripWorldManifest) -> pa.Schema:
    return pa.schema(
        [
            pa.field(field.name, _arrow_type(field.logical_type))
            for field in manifest.selected_fields
        ]
    )


def validate_projected_file(path: Path, manifest: TripWorldManifest) -> pq.FileMetaData:
    if not path.is_file():
        raise ValueError(f"Projected TripWorld artifact does not exist: {path}")
    parquet = pq.ParquetFile(path)
    expected_schema = selected_arrow_schema(manifest)
    if not parquet.schema_arrow.equals(expected_schema, check_metadata=False):
        raise ValueError(
            "Projected TripWorld schema mismatch: "
            f"expected {expected_schema}, got {parquet.schema_arrow}"
        )
    if parquet.metadata.num_rows != manifest.dataset.row_count:
        raise ValueError(
            "Projected TripWorld row-count mismatch: "
            f"expected {manifest.dataset.row_count}, got {parquet.metadata.num_rows}"
        )
    return parquet.metadata


def projection_fingerprint(manifest: TripWorldManifest) -> tuple[str, dict[str, object]]:
    inputs: dict[str, object] = {
        "dataset_revision": manifest.dataset.revision,
        "source_sha256": manifest.dataset.sha256,
        "selected_schema_version": manifest.selected_schema_version,
        "selected_fields": list(manifest.selected_field_names),
        "preprocessing_version": manifest.preprocessing_version,
        "writer": {
            "format": "parquet",
            "version": "2.6",
            "compression": "zstd",
            "dictionary_encoding": True,
        },
    }
    return payload_fingerprint(inputs), inputs


def project_source(
    source_path: Path,
    output_path: Path,
    manifest: TripWorldManifest,
) -> ArtifactResult:
    """Validate and project the pinned source into a stable 11-field Parquet artifact."""

    source_validation = validate_source_file(source_path, manifest)
    metadata_path = output_path.with_suffix(output_path.suffix + ".manifest.json")
    fingerprint, inputs = projection_fingerprint(manifest)
    if artifact_is_current(output_path, metadata_path, input_fingerprint=fingerprint):
        metadata = load_json_object(metadata_path)
        return ArtifactResult(
            output_path,
            metadata_path,
            int(metadata["row_count"]),
            int(metadata["output_size_bytes"]),
            str(metadata["output_sha256"]),
            reused=True,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".part")
    temporary.unlink(missing_ok=True)
    try:
        table = pq.read_table(source_path, columns=list(manifest.selected_field_names))
        table = table.cast(selected_arrow_schema(manifest), safe=True)
        pq.write_table(
            table,
            temporary,
            compression="zstd",
            use_dictionary=True,
            write_statistics=True,
            version="2.6",
        )
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    os.replace(temporary, output_path)
    output_hash = sha256_file(output_path)
    metadata = {
        "artifact_kind": "tripworld-selected-fields",
        "input_fingerprint": fingerprint,
        "inputs": inputs,
        "source_size_bytes": source_validation.size_bytes,
        "row_count": table.num_rows,
        "output_size_bytes": output_path.stat().st_size,
        "output_sha256": output_hash,
        "output_schema": [
            {"name": field.name, "type": str(field.type)} for field in table.schema
        ],
    }
    write_json_if_changed(metadata_path, metadata)
    return ArtifactResult(
        output_path,
        metadata_path,
        table.num_rows,
        output_path.stat().st_size,
        output_hash,
        reused=False,
    )
