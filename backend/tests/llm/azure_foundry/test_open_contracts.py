"""Strict transport mapping and bounded selector configuration without network calls."""

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from backend.app.llm.azure_foundry.dto import FoundryInterpretationDTO
from backend.app.schemas.interpreted_requirements import InterpretationDraft
from backend.tests.llm.azure_foundry.test_client import FakeChatOpenAI, generate, make_client
from backend.tests.llm.azure_foundry.test_dto import assert_foundry_schema_contract
from backend.tests.versions.v1.fakes import make_revised_extraction


def test_subject_target_requires_explicit_attribution_without_autofill():
    from backend.app.llm.azure_foundry.dto import FoundrySemanticDTO
    from backend.tests.versions.v1.test_interpreted_requirements import draft_for

    item = draft_for().semantic_requirements[0].model_dump(mode="json")
    for invalid in ({}, {"kind": "specified", "additional_refs": []}):
        with pytest.raises(ValidationError):
            FoundrySemanticDTO.model_validate({**item, "subject_target": invalid})
    assert FoundrySemanticDTO.model_validate(item).subject_target.kind == "party"


def test_interpreted_evidence_targets_roundtrip_and_validate_dimension(monkeypatch):
    from backend.app.schemas.interpreted_requirements import (
        EvidenceRequestDraft,
        ExperienceEvidenceRequest,
    )
    from backend.tests.versions.v1.test_interpreted_requirements import draft_for

    target = EvidenceRequestDraft(
        requirement_ref="s",
        dimension="walking_intensity",
        preferred_values=("LIGHT",),
        avoided_values=("HIGH",),
    )
    draft = draft_for(experience_evidence_requests=(target,))
    dto = FoundryInterpretationDTO.model_validate(draft.model_dump(mode="json"))
    FakeChatOpenAI.response = raw_result(dto)
    assert (
        generate(make_client(monkeypatch), InterpretationDraft).model_dump() == draft.model_dump()
    )
    with pytest.raises(ValidationError):
        ExperienceEvidenceRequest(
            requirement_id="s", dimension="walking_intensity", preferred_values=("FAMILY_FRIENDLY",)
        )
    with pytest.raises(ValidationError):
        ExperienceEvidenceRequest(
            requirement_id="s",
            dimension="walking_intensity",
            preferred_values=("LIGHT",),
            avoided_values=("LIGHT",),
        )


def raw_result(dto):
    return {
        "parsed": dto,
        "parsing_error": None,
        "raw": SimpleNamespace(
            response_metadata={"model_name": "fixture-model"},
            id="fixture-id",
            usage_metadata={"input_tokens": 100, "output_tokens": 30, "total_tokens": 130},
        ),
    }


def test_interpreter_dto_maps_open_semantics_without_changing_v0(monkeypatch):
    draft = make_revised_extraction()
    dto = FoundryInterpretationDTO.model_validate(draft.model_dump(mode="json"))
    assert_foundry_schema_contract(dto.model_json_schema())
    FakeChatOpenAI.response = raw_result(dto)
    client = make_client(monkeypatch)
    result = generate(client, InterpretationDraft)
    assert result.model_dump() == draft.model_dump()
    assert FakeChatOpenAI.structured_model.invocation_count == 1
    assert FakeChatOpenAI.structured_kwargs["response_format"]["json_schema"]["strict"] is True
    assert "reasoning" not in FakeChatOpenAI.structured_kwargs
    assert client.last_call_metadata["usage"]["total_tokens"] == 130
