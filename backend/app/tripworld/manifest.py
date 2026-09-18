"""Versioned TripWorld source and artifact contracts."""

import json
from pathlib import Path
from typing import Self

import pyarrow as pa
from pydantic import BaseModel, ConfigDict, Field, model_validator

SELECTED_FIELD_NAMES = (
    "fsq_place_id",
    "fsq_name",
    "fsq_latitude",
    "fsq_longitude",
    "fsq_locality",
    "fsq_region",
    "fsq_country",
    "fsq_category_labels",
    "google_name",
    "google_categories",
    "google_place_id",
)


class ManifestModel(BaseModel):
    """Strict immutable manifest model."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class DatasetSource(ManifestModel):
    repository: str = Field(min_length=1)
    repository_type: str = Field(min_length=1)
    source_path: str = Field(min_length=1)
    revision: str = Field(pattern=r"^[0-9a-f]{40}$")
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    size_bytes: int = Field(gt=0)
    row_count: int = Field(gt=0)

    @property
    def download_url(self) -> str:
        return (
            f"https://huggingface.co/datasets/{self.repository}/resolve/"
            f"{self.revision}/{self.source_path}"
        )


class SourceField(ManifestModel):
    name: str = Field(min_length=1)
    logical_type: str = Field(pattern=r"^(string|float64|list<string>)$")


class TripWorldManifest(ManifestModel):
    manifest_version: int = Field(ge=1)
    dataset: DatasetSource
    selected_schema_version: str = Field(min_length=1)
    selected_fields: tuple[SourceField, ...]
    preprocessing_version: str = Field(min_length=1)
    semantic_mapping_version: str = Field(min_length=1)
    retrieval_description_version: str = Field(min_length=1)
    retrieval_text_template_version: str = Field(min_length=1)
    artifact_version: str = Field(min_length=1)

    @model_validator(mode="after")
    def selected_contract_is_exact(self) -> Self:
        names = tuple(field.name for field in self.selected_fields)
        if names != SELECTED_FIELD_NAMES:
            raise ValueError("TripWorld selected fields must match the fixed 11-field contract")
        return self

    @property
    def selected_field_names(self) -> tuple[str, ...]:
        return tuple(field.name for field in self.selected_fields)


class SourceSchemaError(ValueError):
    """The source Parquet schema does not satisfy the pinned contract."""


def load_manifest(path: Path) -> TripWorldManifest:
    return TripWorldManifest.model_validate_json(path.read_text(encoding="utf-8"))


def manifest_payload(manifest: TripWorldManifest) -> dict[str, object]:
    return json.loads(manifest.model_dump_json())


def _matches_logical_type(data_type: pa.DataType, logical_type: str) -> bool:
    if logical_type == "string":
        return pa.types.is_string(data_type) or pa.types.is_large_string(data_type)
    if logical_type == "float64":
        return pa.types.is_float64(data_type)
    if logical_type == "list<string>":
        return (
            pa.types.is_list(data_type) or pa.types.is_large_list(data_type)
        ) and (
            pa.types.is_string(data_type.value_type)
            or pa.types.is_large_string(data_type.value_type)
        )
    return False


def validate_source_schema(schema: pa.Schema, manifest: TripWorldManifest) -> pa.Schema:
    """Validate and return the source projection in manifest order."""

    errors: list[str] = []
    fields: list[pa.Field] = []
    for expected in manifest.selected_fields:
        index = schema.get_field_index(expected.name)
        if index < 0:
            errors.append(f"missing field: {expected.name}")
            continue
        actual = schema.field(index)
        if not _matches_logical_type(actual.type, expected.logical_type):
            errors.append(
                f"field {expected.name} expected {expected.logical_type}, got {actual.type}"
            )
        fields.append(actual)
    if errors:
        raise SourceSchemaError("; ".join(errors))
    return pa.schema(fields)
