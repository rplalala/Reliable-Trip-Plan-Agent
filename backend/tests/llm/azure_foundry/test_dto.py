"""Tests for strict Microsoft Foundry transport DTO contracts."""

from typing import Any

import pytest
from pydantic import ValidationError

from backend.app.llm.azure_foundry.dto import (
    FoundryActivityDTO,
    FoundryDateTimeDTO,
    FoundryInterpretationDTO,
    FoundryItineraryDayDTO,
    FoundryItineraryDTO,
    FoundryMoneyDTO,
    FoundryPrimaryItineraryDTO,
)

UNSUPPORTED_KEYWORDS = {
    "contains",
    "default",
    "format",
    "maxContains",
    "maxItems",
    "maxLength",
    "maxProperties",
    "maximum",
    "minContains",
    "minItems",
    "minLength",
    "minProperties",
    "minimum",
    "multipleOf",
    "pattern",
    "patternProperties",
    "propertyNames",
    "unevaluatedItems",
    "unevaluatedProperties",
    "uniqueItems",
}

DTO_TYPES = (
    FoundryMoneyDTO,
    FoundryDateTimeDTO,
    FoundryActivityDTO,
    FoundryInterpretationDTO,
    FoundryItineraryDayDTO,
    FoundryItineraryDTO,
)


def assert_foundry_schema_contract(schema: object) -> None:
    if isinstance(schema, list):
        for item in schema:
            assert_foundry_schema_contract(item)
        return
    if not isinstance(schema, dict):
        return

    assert not set(schema) & UNSUPPORTED_KEYWORDS
    if schema.get("type") == "object":
        properties = schema.get("properties", {})
        assert schema.get("additionalProperties") is False
        assert set(schema.get("required", [])) == set(properties)

    for value in schema.values():
        assert_foundry_schema_contract(value)


@pytest.mark.parametrize("dto_type", DTO_TYPES)
def test_dto_schema_is_directly_foundry_compatible(dto_type: type[Any]) -> None:
    assert_foundry_schema_contract(dto_type.model_json_schema())


def test_dto_rejects_implicit_type_coercion() -> None:
    with pytest.raises(ValidationError, match="valid string"):
        FoundryDateTimeDTO.model_validate(
            {
                "date": 20261001,
                "time": "13:30:00",
                "utc_offset": "+09:00",
            }
        )


def test_dto_rejects_missing_datetime_component() -> None:
    with pytest.raises(ValidationError, match="Field required"):
        FoundryDateTimeDTO.model_validate(
            {
                "date": "2026-10-01",
                "time": "13:30:00",
            }
        )


def test_dto_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        FoundryDateTimeDTO.model_validate(
            {
                "date": "2026-10-01",
                "time": "13:30:00",
                "utc_offset": "+09:00",
                "timezone_name": "Asia/Tokyo",
            }
        )


def test_only_v0_provider_activities_require_nullable_transport_declaration() -> None:
    schema = FoundryItineraryDTO.model_json_schema()
    day = schema["$defs"]["FoundryItineraryDayDTO"]
    activity_ref = day["properties"]["activities"]["items"]["$ref"].split("/")[-1]
    activity = schema["$defs"][activity_ref]
    assert "transport" in activity["required"]
    branches = activity["properties"]["transport"]["anyOf"]
    assert {"type": "null"} in branches
    declaration_ref = next(branch["$ref"] for branch in branches if "$ref" in branch)
    declaration = schema["$defs"][declaration_ref.split("/")[-1]]
    assert set(declaration["required"]) == {"mode", "from_activity_id", "to_activity_id"}
    primary = FoundryPrimaryItineraryDTO.model_json_schema()["$defs"]["FoundryPrimaryActivityDTO"]
    assert "transport" not in primary["properties"]
