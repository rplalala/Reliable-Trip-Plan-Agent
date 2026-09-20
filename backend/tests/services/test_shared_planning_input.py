"""Shared-foundation contracts exercised without external network or model access."""

import asyncio
import hashlib
import json
from datetime import date
from uuid import uuid4

import pytest
from pydantic import ValidationError

from backend.app.llm.azure_foundry.dto import FoundryInterpretationDTO
from backend.app.observability.run_trace import NullRunTracer
from backend.app.schemas.interpreted_requirements import ClarificationRequired, InterpretationDraft
from backend.app.schemas.request import PlanningRequest
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.app.services.preference_interpretation import (
    empty_preference_draft,
    interpret_preferences,
)
from backend.app.versions.v0.graph import build_v0_graph
from backend.app.versions.v0.runner import run_v0
from backend.app.versions.v1.graph import build_v1_graph
from backend.app.versions.v1.runner import run_v1
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v0.fakes import (
    FakeStructuredLLMClient,
    make_itinerary,
    make_requirements,
)
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
)
from backend.tests.versions.v1.fakes import make_itinerary as v1_itinerary
from backend.tests.versions.v1.test_interpreted_requirements import draft_for

REF = date(2026, 9, 11)


@pytest.mark.parametrize(
    "field",
    [
        "destination",
        "start_date",
        "end_date",
        "traveler_count",
        "budget",
        "budget.amount",
        "budget.currency",
    ],
)
@pytest.mark.parametrize("engine", ["v0", "v1"])
def test_missing_mandatory_fields_fail_before_any_call(field, engine):
    data = make_request().model_dump(mode="json")
    if "." in field:
        del data["budget"][field.split(".")[1]]
    else:
        del data[field]
    client = FakeStructuredLLMClient([])
    places, weather, routes = FakePlacesProvider(), FakeWeatherProvider(), FakeRoutesProvider()
    with pytest.raises(ValidationError):
        if engine == "v0":
            asyncio.run(run_v0(data, client, reference_date=REF))
        else:
            asyncio.run(run_v1(data, client, places, weather, routes, reference_date=REF))
    assert not client.calls and not places.search_requests and not places.details_requests


@pytest.mark.parametrize(
    "field,value",
    [
        ("traveler_count", True),
        ("traveler_count", 1.5),
        ("traveler_count", 0),
        ("traveler_count", -1),
        ("traveler_count", "2"),
        ("traveler_count", None),
        ("budget.amount", -1),
        ("budget.amount", "NaN"),
        ("budget.amount", "Infinity"),
        ("budget.amount", True),
        ("budget.amount", "100-200"),
        ("budget.amount", None),
        ("budget.currency", "$"),
        ("budget.currency", "aud"),
        ("budget.currency", None),
        ("destination", "  "),
        ("additional_preferences", 42),
        ("start_date", "invalid"),
        ("start_date", "2026-09-15"),
        ("input_version", "v1_structured_1"),
    ],
)
def test_invalid_forms_never_reach_interpretation(field, value):
    data = make_request().model_dump(mode="json")
    if "." in field:
        data["budget"][field.split(".")[1]] = value
    else:
        data[field] = value
    client = FakeStructuredLLMClient([])
    with pytest.raises(ValidationError):
        asyncio.run(run_v0(data, client, reference_date=REF))
    assert not client.calls


@pytest.mark.parametrize("preferences", [None, "", "  \n\t"])
def test_empty_preferences_skip_shared_interpreter(preferences):
    request = make_request(preferences)
    client = FakeStructuredLLMClient([])
    contract = asyncio.run(interpret_preferences(request, REF, client))
    assert not client.calls
    assert contract.interpretation_origin == "skipped_empty"
    assert not contract.semantic_requirements and not contract.named_places
    assert not contract.experience_evidence_requests and not contract.discovery_intents
    assert contract.requirements == request.trip_requirements()
    assert contract.request_sha256 == hashlib.sha256(b"").hexdigest()


def test_both_graphs_send_identical_shared_interpretation_and_canonical_context():
    request = make_request("Prefer local places")
    first, second = FakeStructuredLLMClient([draft_for()]), FakeStructuredLLMClient([draft_for()])

    class ForbiddenEvidence:
        def __getattr__(self, name):
            raise AssertionError(f"No evidence allowed at shared boundary: {name}")

    v0 = build_v0_graph(first)
    v1 = build_v1_graph(second, ForbiddenEvidence(), NullRunTracer(uuid4()))
    state = {"request": request, "reference_date": REF}
    a = asyncio.run(v0.nodes["extract_requirements"].bound.ainvoke(state))
    b = asyncio.run(v1.nodes["extract_requirements"].bound.ainvoke(state))
    assert first.calls == second.calls and len(first.calls) == 1
    assert a["interpreted_requirements"] == b["interpreted_requirements"]
    payload = json.loads(first.calls[0].user_prompt)
    assert payload["read_only_trip_facts"]["traveler_count"] == 2
    assert payload["additional_preferences"] == request.additional_preferences


def test_model_cannot_return_authoritative_trip_fields():
    data = empty_preference_draft().model_dump(mode="json")
    data["requirements"] = make_request().trip_requirements().model_dump(mode="json")
    with pytest.raises(ValidationError):
        InterpretationDraft.model_validate(data)
    with pytest.raises(ValidationError):
        FoundryInterpretationDTO.model_validate(data)


@pytest.mark.parametrize(
    "field",
    ["destination", "start_date", "end_date", "traveler_count", "budget.amount", "budget.currency"],
)
def test_grounded_conflict_preserves_form_and_stops_generation(field):
    text = "Please replace the entered value."
    request = make_request(text)
    draft = empty_preference_draft().model_dump()
    draft["operational_conflicts"] = [
        {"field": field, "source_refs": [{"quote": text, "occurrence": 0}]}
    ]
    client = FakeStructuredLLMClient([InterpretationDraft.model_validate(draft)])
    before = request.model_dump()
    with pytest.raises(ClarificationRequired) as exc:
        asyncio.run(run_v0(request, client, reference_date=REF))
    assert exc.value.code == "structured_input_conflict"
    assert exc.value.conflicts[0]["source_refs"][0]["start"] == 0
    assert before == request.model_dump() and len(client.calls) == 1


def test_context_only_citation_is_not_a_preference_source():
    request = make_request("Prefer local places")
    client = FakeStructuredLLMClient([draft_for("Sydney")])
    with pytest.raises(RequirementBoundaryError):
        asyncio.run(interpret_preferences(request, REF, client))


def test_nonblank_text_and_spans_keep_exact_whitespace():
    request = make_request("  Prefer local places  ")
    contract = asyncio.run(
        interpret_preferences(request, REF, FakeStructuredLLMClient([draft_for()]))
    )
    ref = contract.semantic_requirements[0].source_refs[0]
    assert ref.start == 2 and request.additional_preferences[ref.start : ref.end] == ref.quote
    assert contract.structured_input_sha256 == request.structured_hash()


def test_v0_named_visits_need_no_google_identity_or_tool_pool():
    text = "Visit Fushimi Inari Shrine."
    request = make_request(text, requirements=make_requirements())
    draft = empty_preference_draft().model_dump()
    draft["named_places"] = [
        {
            "place_text": "Fushimi Inari Shrine",
            "inclusion": "REQUIRED",
            "source_refs": [{"quote": text, "occurrence": 0}],
        }
    ]
    client = FakeStructuredLLMClient([InterpretationDraft.model_validate(draft), make_itinerary()])
    result = asyncio.run(run_v0(request, client, reference_date=REF))
    assert result.system_version == "v0" and len(client.calls) == 2
    assert "Fushimi Inari Shrine" in client.calls[-1].user_prompt
    assert '"inclusion":"REQUIRED"' in client.calls[-1].user_prompt
    assert "google_places:" not in client.calls[-1].user_prompt
    assert "planning_supply" not in client.calls[-1].user_prompt


def test_v0_empty_preference_has_only_generation():
    request = make_request(requirements=make_requirements())
    client = FakeStructuredLLMClient([make_itinerary()])
    asyncio.run(run_v0(request, client, reference_date=REF))
    assert len(client.calls) == 1 and client.calls[0].response_schema.__name__ == "Itinerary"


def test_v1_empty_preferences_use_default_discovery_without_reviews():
    client = FakeStructuredLLMClient([v1_itinerary()])
    places, weather, routes = FakePlacesProvider(), FakeWeatherProvider(), FakeRoutesProvider()
    result = asyncio.run(
        run_v1(make_request(), client, places, weather, routes, reference_date=REF)
    )
    assert len(client.calls) == 1
    assert len(places.search_requests) > 1 and places.details_requests
    assert not places.reviews_requests
    assert result.system_version == "v1"
    assert "SystemVersion" not in PlanningRequest.model_json_schema()["properties"]


def test_hard_policy_remains_blocking_with_complete_form():
    text = "Absolutely no stairs."
    draft = draft_for(text)
    draft = draft.model_copy(
        update={
            "semantic_requirements": (
                draft.semantic_requirements[0].model_copy(update={"strength": "hard"}),
            )
        }
    )
    client = FakeStructuredLLMClient([draft])
    with pytest.raises(ClarificationRequired, match="unsupported_hard_requirements"):
        asyncio.run(run_v0(make_request(text), client, reference_date=REF))
    assert len(client.calls) == 1
