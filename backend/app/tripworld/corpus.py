"""Deterministic TripWorld retrieval-corpus construction."""

import os
from dataclasses import dataclass
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from backend.app.tripworld.artifacts import (
    artifact_is_current,
    load_json_object,
    payload_fingerprint,
    write_json_if_changed,
)
from backend.app.tripworld.manifest import TripWorldManifest
from backend.app.tripworld.preprocessing import selected_arrow_schema, validate_projected_file
from backend.app.tripworld.semantics import (
    CategorySemanticMapping,
    enrich_row,
    semantic_mapping_payload,
)
from backend.app.tripworld.source import sha256_file

DERIVED_FIELDS = (
    "normalized_fsq_categories",
    "normalized_google_categories",
    "semantic_rule_ids",
    "direct_semantics",
    "inferred_semantics",
    "semantic_eligibility_hints",
    "retrieval_description",
    "retrieval_text",
)


@dataclass(frozen=True)
class CorpusResult:
    path: Path
    metadata_path: Path
    row_count: int
    mapped_row_count: int
    retrieval_text_count: int
    size_bytes: int
    sha256: str
    reused: bool


def corpus_schema(manifest: TripWorldManifest) -> pa.Schema:
    list_string = pa.list_(pa.string())
    return selected_arrow_schema(manifest).append(pa.field(DERIVED_FIELDS[0], list_string)).append(
        pa.field(DERIVED_FIELDS[1], list_string)
    ).append(pa.field(DERIVED_FIELDS[2], list_string)).append(
        pa.field(DERIVED_FIELDS[3], list_string)
    ).append(pa.field(DERIVED_FIELDS[4], list_string)).append(
        pa.field(DERIVED_FIELDS[5], list_string)
    ).append(pa.field(DERIVED_FIELDS[6], pa.string())).append(
        pa.field(DERIVED_FIELDS[7], pa.string())
    )


def _fingerprint_inputs(
    selected_path: Path,
    manifest: TripWorldManifest,
    mapping: CategorySemanticMapping,
) -> tuple[str, dict[str, object]]:
    inputs: dict[str, object] = {
        "selected_artifact_sha256": sha256_file(selected_path),
        "selected_schema_version": manifest.selected_schema_version,
        "artifact_version": manifest.artifact_version,
        "semantic_mapping_version": manifest.semantic_mapping_version,
        "retrieval_description_version": manifest.retrieval_description_version,
        "retrieval_text_template_version": manifest.retrieval_text_template_version,
        "semantic_mapping": semantic_mapping_payload(mapping),
        "writer": {
            "format": "parquet",
            "version": "2.6",
            "compression": "zstd",
            "dictionary_encoding": True,
        },
    }
    return payload_fingerprint(inputs), inputs


def build_corpus(
    selected_path: Path,
    output_path: Path,
    manifest: TripWorldManifest,
    mapping: CategorySemanticMapping,
    *,
    batch_size: int = 20_000,
) -> CorpusResult:
    """Enrich every selected row without filtering or changing source metadata."""

    if mapping.mapping_version != manifest.semantic_mapping_version:
        raise ValueError("Semantic mapping version does not match the TripWorld manifest")
    if mapping.description_version != manifest.retrieval_description_version:
        raise ValueError("Description version does not match the TripWorld manifest")
    validate_projected_file(selected_path, manifest)
    metadata_path = output_path.with_suffix(output_path.suffix + ".manifest.json")
    fingerprint, inputs = _fingerprint_inputs(selected_path, manifest, mapping)
    if artifact_is_current(output_path, metadata_path, input_fingerprint=fingerprint):
        metadata = load_json_object(metadata_path)
        return CorpusResult(
            output_path,
            metadata_path,
            int(metadata["row_count"]),
            int(metadata["mapped_row_count"]),
            int(metadata["retrieval_text_count"]),
            int(metadata["output_size_bytes"]),
            str(metadata["output_sha256"]),
            reused=True,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_suffix(output_path.suffix + ".part")
    temporary.unlink(missing_ok=True)
    writer = pq.ParquetWriter(
        temporary,
        corpus_schema(manifest),
        compression="zstd",
        use_dictionary=True,
        write_statistics=True,
        version="2.6",
    )
    row_count = 0
    mapped_row_count = 0
    retrieval_text_count = 0
    try:
        parquet = pq.ParquetFile(selected_path)
        for batch in parquet.iter_batches(batch_size=batch_size):
            enriched_rows: list[dict[str, object]] = []
            for row in batch.to_pylist():
                enrichment = enrich_row(row, mapping)
                enriched = dict(row)
                enriched.update(enrichment.model_dump(mode="python"))
                enriched_rows.append(enriched)
                row_count += 1
                mapped_row_count += bool(enrichment.semantic_rule_ids)
                retrieval_text_count += bool(enrichment.retrieval_text)
            writer.write_table(
                pa.Table.from_pylist(enriched_rows, schema=corpus_schema(manifest))
            )
    except Exception:
        writer.close()
        temporary.unlink(missing_ok=True)
        raise
    writer.close()
    os.replace(temporary, output_path)
    output_hash = sha256_file(output_path)
    metadata = {
        "artifact_kind": "tripworld-retrieval-corpus",
        "input_fingerprint": fingerprint,
        "inputs": inputs,
        "row_count": row_count,
        "mapped_row_count": mapped_row_count,
        "retrieval_text_count": retrieval_text_count,
        "output_size_bytes": output_path.stat().st_size,
        "output_sha256": output_hash,
        "output_schema": [
            {"name": field.name, "type": str(field.type)}
            for field in corpus_schema(manifest)
        ],
        "metadata_fields_excluded_from_retrieval_text": [
            "fsq_place_id",
            "google_place_id",
            "fsq_latitude",
            "fsq_longitude",
        ],
    }
    write_json_if_changed(metadata_path, metadata)
    return CorpusResult(
        output_path,
        metadata_path,
        row_count,
        mapped_row_count,
        retrieval_text_count,
        output_path.stat().st_size,
        output_hash,
        reused=False,
    )
