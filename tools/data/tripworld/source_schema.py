"""Offline raw Parquet schema validation against the shared manifest."""

import pyarrow as pa

from backend.app.tripworld.manifest import TripWorldManifest


class SourceSchemaError(ValueError):
    """The source Parquet schema does not satisfy the pinned contract."""


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
