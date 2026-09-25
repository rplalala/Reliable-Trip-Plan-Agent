"""Typed synthetic outcomes test contracts, not real-model classification accuracy."""

import asyncio
import json
from pathlib import Path

import pytest

from backend.app.llm.azure_foundry.client import requirement_wire_format
from backend.app.policies.preference_input import PreferenceInputBlocked
from backend.app.services.preference_prompts import PREFERENCE_INTERPRETATION_SYSTEM_PROMPT
from backend.tests.llm.azure_foundry.test_requirement_boundary import interpret
from backend.tests.services.test_preference_input_gate import draft, issue, run

FIXTURES = Path(__file__).parents[1] / "fixtures/preference_gate"


@pytest.mark.parametrize(
    "name,kind,disposition",
    [
        ("contradiction", "semantic_ambiguity", "CLARIFICATION_REQUIRED"),
        ("scope", "destination_scope_conflict", "REWRITE_REQUIRED"),
    ],
)
def test_historical_mismatch_is_valid_and_never_automatically_reclassified(name, kind, disposition):
    saved = json.loads((FIXTURES / f"historical_{name}_taxonomy.json").read_text())
    payload = json.loads(saved["raw_model_response"][0]["text"])
    assert payload == saved["strict_parsed_dto"]
    # Synthetic wire migration only; historical raw artifacts are not changed.
    for row in payload.get("semantic_requirements") or ():
        row["experience_goal"] = None
    for row in payload.get("visit_requirements") or ():
        row.update(exact_visits=None, distinct_dates=False)
    text = saved["input"]["additional_preferences"]
    value, _ = asyncio.run(interpret(payload, text=text, canonical=False))
    with pytest.raises(PreferenceInputBlocked) as error:
        run(value, text)
    assert error.value.input_disposition == disposition
    assert error.value.issues[0]["issue_type"] == kind
    assert kind not in saved["frozen_expected"]["expected_issue_types"]
    assert (
        error.value.issues[0]["source_refs"]
        == saved["application_outcome"]["issues"][0]["source_refs"]
    )


@pytest.mark.parametrize(
    "sentences,kind,disposition,field",
    [
        (
            ("I only want to walk everywhere.", "I must use the metro for every transfer."),
            "internal_requirement_contradiction",
            "REWRITE_REQUIRED",
            None,
        ),
        (
            ("I never want to use cars.", "I must travel by car between every attraction."),
            "internal_requirement_contradiction",
            "REWRITE_REQUIRED",
            None,
        ),
        (
            ("Apply the mandatory transport restriction I mentioned earlier.",),
            "semantic_ambiguity",
            "CLARIFICATION_REQUIRED",
            None,
        ),
        (
            ("I want to visit the Bronx Zoo in New York.",),
            "destination_scope_conflict",
            "REWRITE_REQUIRED",
            "destination",
        ),
        (
            ("Plan my trip to Tokyo instead.",),
            "destination_scope_conflict",
            "REWRITE_REQUIRED",
            "destination",
        ),
        (
            ("I also want to spend one full day sightseeing in London.",),
            "unsupported_request_scope",
            "CLARIFICATION_REQUIRED",
            None,
        ),
    ],
)
def test_synthetic_boundary_passes_wire_domain_and_exact_application_grounding(
    sentences, kind, disposition, field
):
    text = " ".join(sentences)
    value = draft(
        issue(
            kind,
            related_field=field,
            source_refs=[{"quote": q, "occurrence": 0} for q in sentences],
        ),
        disposition=disposition,
    )
    parsed, _ = asyncio.run(interpret(value.model_dump(mode="json"), text=text, canonical=False))
    with pytest.raises(PreferenceInputBlocked) as error:
        run(parsed, text)
    assert error.value.input_disposition == disposition
    assert error.value.safety_disposition == "CLEAR"
    row = error.value.issues[0]
    assert row["issue_type"] == kind
    assert [r["quote"] for r in row["source_refs"]] == list(sentences)
    assert all(r["match_mode"] == "exact" for r in row["source_refs"])
    assert row["current_value"] == ("Paris" if field else None)


@pytest.mark.parametrize(
    "text",
    [
        "I prefer walking, but public transport is fine for longer distances.",
        "Walk for short trips and use metro for long trips.",
        "One traveler prefers walking and another prefers metro.",
        "Use walking or metro depending on what works for me.",
        "I would like to visit Versailles.",
        "I love New York-style jazz bars.",
        "I want something similar to the Bronx Zoo.",
    ],
)
def test_synthetic_valid_contrasts_are_not_reclassified_by_application(text):
    value = draft(disposition="VALID")
    parsed, _ = asyncio.run(interpret(value.model_dump(mode="json"), text=text, canonical=False))
    assert run(parsed, text).requirements.destination == "Paris"


def test_prompt_has_decision_order_without_changing_wire_ownership():
    prompt = PREFERENCE_INTERPRETATION_SYSTEM_PROMPT
    assert "preference_prompt_16" in prompt
    assert (
        "Not knowing which clear requirement the user will give up is NOT semantic ambiguity"
        in prompt
    )
    assert "Do not downgrade a clear exclusive/prohibitive/mandatory requirement" in prompt
    assert "Geographic/scope decision" in prompt
    assert "unsupported_request_scope or semantic_ambiguity" not in prompt
    assert "Conflicting unresolved modes require an extraction issue" not in prompt
    schema = requirement_wire_format()
    assert schema["json_schema"]["name"] == "PreferenceDraftV9"
    props = schema["json_schema"]["schema"]["$defs"]["FoundryOtherInputIssueDTO"]["properties"]
    assert props["operational_conflict_index"]["type"] == "null"
