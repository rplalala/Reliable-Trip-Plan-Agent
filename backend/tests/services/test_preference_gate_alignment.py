"""Historical malformed output and synthetic alignment cases; no provider calls."""

import asyncio
import copy
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from backend.app.llm.azure_foundry.client import requirement_wire_format
from backend.app.llm.azure_foundry.dto import FoundryInterpretationDTO
from backend.app.schemas.interpreted_requirements import InterpretationDraft
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.app.services.preference_prompts import PREFERENCE_INTERPRETATION_SYSTEM_PROMPT
from backend.tests.llm.azure_foundry.test_requirement_boundary import interpret
from backend.tests.services.test_preference_input_gate import (
    NY,
    PreferenceInputBlocked,
    draft,
    issue,
    run,
)

FIXTURE = Path(__file__).parents[1] / "fixtures/preference_gate/historical_destination_index.json"


def historical():
    saved = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert json.loads(saved["raw_structured_text"]) == saved["payload"]
    return copy.deepcopy(saved["payload"])


def test_historical_index_is_rejected_by_new_wire_and_unchanged_domain():
    data = historical()
    for schema in (FoundryInterpretationDTO, InterpretationDraft):
        with pytest.raises(ValidationError):
            schema.model_validate(data)
    with pytest.raises(RequirementBoundaryError) as error:
        asyncio.run(interpret(data, text=NY, canonical=False))
    assert error.value.stage == "transport_dto"
    assert (
        historical()["preference_input_assessment"]["issues"][0]["operational_conflict_index"] == 0
    )


def test_corrected_synthetic_destination_shape_reaches_application_rewrite():
    data = historical()
    data["preference_input_assessment"]["issues"][0]["operational_conflict_index"] = None
    data["operational_conflicts"] = []  # Do not duplicate the destination issue.
    value, _ = asyncio.run(interpret(data, text=NY, canonical=False))
    with pytest.raises(PreferenceInputBlocked) as error:
        run(value)
    row = error.value.issues[0]
    assert error.value.input_disposition == "REWRITE_REQUIRED"
    assert error.value.safety_disposition == "CLEAR"
    assert row["current_value"] == "Paris"
    assert row["source_refs"][0]["quote"] == NY


@pytest.mark.parametrize("located", [True, False])
def test_structured_link_remains_valid_with_exact_basis(located):
    data = historical()
    row = data["preference_input_assessment"]["issues"][0]
    row["issue_type"] = "structured_request_conflict"
    if not located:
        row.update(source_refs=[], quote_status="unavailable")
    value, _ = asyncio.run(interpret(data, text=NY, canonical=False))
    with pytest.raises(PreferenceInputBlocked) as error:
        run(value)
    assert error.value.issues[0]["basis_refs"][0]["quote"] == NY


@pytest.mark.parametrize(
    "invalid", ["index", "field", "occurrence", "unrelated", "other_occurrence"]
)
def test_structured_link_invalid_basis_fails_closed(invalid):
    text = NY + " I prefer Rome. " + NY
    data = historical()
    row = data["preference_input_assessment"]["issues"][0]
    row["issue_type"] = "structured_request_conflict"
    conflict = data["operational_conflicts"][0]
    if invalid == "index":
        row["operational_conflict_index"] = 1
    elif invalid == "field":
        row["related_field"] = "end_date"
    elif invalid == "occurrence":
        conflict["source_refs"][0]["occurrence"] = 2
    elif invalid == "unrelated":
        conflict["source_refs"] = [{"quote": "I prefer Rome.", "occurrence": 0}]
    else:
        conflict["source_refs"][0]["occurrence"] = 1
    value = InterpretationDraft.model_validate(
        FoundryInterpretationDTO.model_validate(data).model_dump()
    )
    with pytest.raises(RequirementBoundaryError):
        run(value, text)


def test_actual_schema_structurally_owns_index_and_prompt_gives_exact_example():
    schema = requirement_wire_format()["json_schema"]["schema"]
    branches = schema["$defs"]["FoundryPreferenceInputAssessmentDTO"]["properties"]["issues"][
        "items"
    ]["anyOf"]
    assert len(branches) == 2
    other = schema["$defs"]["FoundryOtherInputIssueDTO"]["properties"]
    assert other["operational_conflict_index"]["type"] == "null"
    assert "structured_request_conflict" not in other["issue_type"]["enum"]
    assert other["quote_status"]["enum"] == ["located"]
    assert '"operational_conflict_index":null' in PREFERENCE_INTERPRETATION_SYSTEM_PROMPT
    assert NY in PREFERENCE_INTERPRETATION_SYSTEM_PROMPT


@pytest.mark.parametrize(
    "change", ["destination_field", "empty_sources", "contradiction", "unavailable", "safety"]
)
def test_remaining_cross_field_rules_are_hard_enforced_offline(change):
    row = issue()
    safety = "CLEAR"
    if change == "destination_field":
        row["related_field"] = None
    elif change == "empty_sources":
        row["source_refs"] = []
    elif change == "contradiction":
        row["issue_type"] = "internal_requirement_contradiction"
    elif change == "unavailable":
        row.update(
            issue_type="structured_request_conflict", source_refs=[], quote_status="unavailable"
        )
    else:
        safety = "SAFETY_BLOCK"
    with pytest.raises((ValidationError, RequirementBoundaryError)):
        run(draft(row, safety=safety))
