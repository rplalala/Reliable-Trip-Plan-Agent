"""Real SDK parsing over MockTransport; no live endpoints or model judgments."""

import asyncio
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest
from openai import AsyncOpenAI

from backend.app.evidence.experience_models import (
    ALLOWED_VALUES,
    ExperienceProfile,
    ExperienceSignal,
)
from backend.app.llm.azure_foundry.client import (
    AzureFoundryStructuredLLMClient,
    requirement_wire_format,
)
from backend.app.policies.interpreted_requirements import (
    assess_requirements,
    canonicalize_requirements,
    require_resolved_hard,
)
from backend.app.policies.planning_supply import SupplyCandidate, select_planning_supply
from backend.app.schemas.interpreted_requirements import ClarificationRequired, InterpretationDraft
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.app.services.planning_supply_pipeline import planner_supply_projection
from backend.app.services.preference_prompts import PREFERENCE_INTERPRETATION_SYSTEM_PROMPT
from backend.tests.llm.azure_foundry.test_dto import assert_foundry_schema_contract
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v1.test_interpreted_requirements import draft_for
from tools.validation.requirement_capture import DevelopmentRequirementCapture

TEXT = (
    "I like architecture. Mother avoids long walks. Our two friends like parks. "
    "We dislike crowds. Absolutely no stairs."
)


def wire_draft():
    data = draft_for().model_dump(mode="json")
    quotes = [
        "I like architecture.",
        "Mother avoids long walks.",
        "Our two friends like parks.",
        "We dislike crowds.",
    ]
    data["subjects"] = [
        {"local_key": handle, "label": label, "source_refs": [{"quote": quote, "occurrence": 0}]}
        for handle, label, quote in zip(
            ("me", "mom", "pair"), ("Requester", "Mother", "Two friends"), quotes[:3], strict=True
        )
    ]
    base = data["semantic_requirements"][0]
    data["semantic_requirements"] = [
        {
            **copy.deepcopy(base),
            "local_key": f"r{i}",
            "normalized_text": quote,
            "polarity": "avoid" if i in (1, 3) else "favor",
            "subject_target": {"kind": "party"}
            if i == 3
            else {
                "kind": "specified",
                "first_ref": ("me", "mom", "pair")[i],
                "additional_refs": [],
            },
            "source_refs": [{"quote": quote, "occurrence": 0}],
        }
        for i, quote in enumerate(quotes)
    ]
    data["discovery_intents"] = [
        {
            "requirement_refs": ["r0", "r2"],
            "purpose": "semantic_discovery",
            "query_text": "Architectural parks",
        }
    ]
    data["experience_evidence_requests"] = [
        {
            "requirement_ref": "r1",
            "dimension": "walking_intensity",
            "preferred_values": ["LIGHT"],
            "avoided_values": ["HIGH"],
        }
    ]
    return data


async def interpret(
    data,
    *,
    capture=None,
    status="completed",
    refusal=False,
    http_status=200,
    text=TEXT,
    after=None,
    canonical=True,
):
    requests = []
    content = data if isinstance(data, str) else json.dumps(data, ensure_ascii=True)

    def handler(request):
        requests.append(json.loads(request.content))
        assert request.url.path == "/openai/v1/responses"
        if http_status != 200:
            return httpx.Response(
                http_status,
                json={"error": {"message": "fixture failure", "type": "invalid_request_error"}},
            )
        return httpx.Response(
            200,
            json={
                "id": "resp_fixture",
                "created_at": 0,
                "object": "response",
                "status": status,
                "error": None,
                "incomplete_details": {"reason": "max_output_tokens"}
                if status == "incomplete"
                else None,
                "model": "fixture-model",
                "output": [
                    {
                        "type": "message",
                        "id": "msg_fixture",
                        "status": "completed",
                        "role": "assistant",
                        "content": [{"type": "refusal", "refusal": "fixture refusal"}]
                        if refusal
                        else [{"type": "output_text", "text": content, "annotations": []}],
                    }
                ],
                "parallel_tool_calls": True,
                "tool_choice": "auto",
                "tools": [],
                "temperature": 1,
                "top_p": 1,
                "usage": {
                    "input_tokens": 30,
                    "output_tokens": 10,
                    "total_tokens": 40,
                    "input_tokens_details": {"cached_tokens": 0},
                    "output_tokens_details": {"reasoning_tokens": 0},
                },
            },
        )

    client = AzureFoundryStructuredLLMClient(
        endpoint="https://fixture.invalid/openai/v1",
        deployment="fixture-model",
        api_key="test-secret-key",
        requirement_capture=capture,
    )
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        client._chat_model.root_async_client = AsyncOpenAI(
            api_key="test-secret-key",
            base_url="https://fixture.invalid/openai/v1",
            http_client=http,
            max_retries=0,
        )
        draft = await client.generate_structured(
            system_prompt=PREFERENCE_INTERPRETATION_SYSTEM_PROMPT,
            user_prompt=text,
            response_schema=InterpretationDraft,
        )
        try:
            result = canonicalize_requirements(draft, make_request(text)) if canonical else draft
        except Exception as exc:
            client.capture_requirement_outcome(draft, exc)
            raise
        client.capture_requirement_outcome(draft)
        if after:
            after(result, requests)
        return result, requests


def downstream(contract):
    places = [
        SupplyCandidate(
            place_id=p,
            primary_type="park",
            rating=4.5,
            latitude=0,
            longitude=0,
            intent_ids=(contract.discovery_intents[0].intent_id,),
        )
        for p in ("a", "b")
    ]
    profiles = {
        "a": ExperienceProfile(
            place_id="a",
            availability="available",
            signals=(
                ExperienceSignal(
                    dimension="walking_intensity",
                    value="HIGH",
                    confidence="medium",
                    review_refs=("review_1",),
                ),
            ),
        ),
        "b": ExperienceProfile(
            place_id="b",
            availability="available",
            signals=(
                ExperienceSignal(
                    dimension="walking_intensity",
                    value="LIGHT",
                    confidence="medium",
                    review_refs=("review_2",),
                ),
            ),
        ),
    }
    supply = select_planning_supply(
        places,
        contract,
        required_ids=(),
        excluded_ids=(),
        capacity=2,
        hard_capacity=2,
        destination_coordinates=(0, 0),
        profiles=profiles,
    )
    view = planner_supply_projection(SimpleNamespace(policy_result=supply), contract)
    return supply.model_dump(exclude={"elapsed_seconds", "cpu_seconds"}), view


@pytest.mark.parametrize("length", [1, 44, 100, 256])
@pytest.mark.parametrize("permute", [False, True])
def test_handle_renaming_length_and_definition_permutation_preserve_graph(length, permute):
    original = wire_draft()
    baseline, _ = asyncio.run(interpret(original))
    changed = copy.deepcopy(original)
    subjects = {s["local_key"]: chr(97 + i) * length for i, s in enumerate(changed["subjects"])}
    semantics = {
        r["local_key"]: chr(107 + i) * length
        for i, r in enumerate(changed["semantic_requirements"])
    }
    for s in changed["subjects"]:
        s["local_key"] = subjects[s["local_key"]]
    for r in changed["semantic_requirements"]:
        r["local_key"] = semantics[r["local_key"]]
        if r["subject_target"]["kind"] == "specified":
            r["subject_target"]["first_ref"] = subjects[r["subject_target"]["first_ref"]]
    for d in changed["discovery_intents"]:
        d["requirement_refs"] = [semantics[r] for r in d["requirement_refs"]]
    for e in changed["experience_evidence_requests"]:
        e["requirement_ref"] = semantics[e["requirement_ref"]]
    if permute:
        for k in (
            "subjects",
            "semantic_requirements",
            "discovery_intents",
            "experience_evidence_requests",
        ):
            changed[k].reverse()
    result, _ = asyncio.run(interpret(changed))
    assert result.model_dump() == baseline.model_dump()
    assert downstream(result) == downstream(baseline)
    assert canonicalize_requirements(result, make_request(TEXT)).model_dump() == result.model_dump()


@pytest.mark.parametrize(
    "mutation",
    [
        "dangling_subject",
        "dangling_requirement",
        "duplicate_subject",
        "duplicate_semantic",
        "missing_first",
        "blank_first",
        "wrong_dimension",
        "contradictory_targets",
        "wrong_occurrence",
        "extra_canonical_id",
        "named_local_key",
        "oversized_handle",
        "null_target",
    ],
)
def test_invalid_contracts_fail_without_user_clarification(mutation):
    data = wire_draft()
    if mutation == "dangling_subject":
        data["subjects"][0]["local_key"] = "renamed"
    elif mutation == "dangling_requirement":
        data["semantic_requirements"][0]["local_key"] = "renamed"
    elif mutation == "duplicate_subject":
        data["subjects"].append({**data["subjects"][0], "label": "Someone else"})
    elif mutation == "duplicate_semantic":
        data["semantic_requirements"].append(
            {**data["semantic_requirements"][0], "normalized_text": "Conflicting definition"}
        )
    elif mutation == "missing_first":
        del data["semantic_requirements"][0]["subject_target"]["first_ref"]
    elif mutation == "blank_first":
        data["semantic_requirements"][0]["subject_target"]["first_ref"] = ""
    elif mutation == "wrong_dimension":
        data["experience_evidence_requests"][0]["preferred_values"] = ["ACCESSIBLE"]
    elif mutation == "contradictory_targets":
        data["experience_evidence_requests"][0]["avoided_values"] = ["LIGHT"]
    elif mutation == "wrong_occurrence":
        data["semantic_requirements"][0]["source_refs"][0]["occurrence"] = 99
    elif mutation == "extra_canonical_id":
        data["discovery_intents"][0]["intent_id"] = "discovery_distinctive_architectural_cultural"
    elif mutation == "named_local_key":
        data["named_places"] = [
            {
                "local_key": "unnecessary",
                "place_text": "Opera House",
                "inclusion": "REQUIRED",
                "source_refs": [],
            }
        ]
    elif mutation == "oversized_handle":
        data["subjects"][0]["local_key"] = "a" * 257
    elif mutation == "null_target":
        data["semantic_requirements"][0]["subject_target"] = None
    with pytest.raises(RequirementBoundaryError) as error:
        asyncio.run(interpret(data))
    assert error.value.category == "invalid_model_contract"


def test_party_requester_people_subgroups_and_shared_targets_remain_distinct():
    data = wire_draft()
    data["semantic_requirements"][0]["subject_target"]["additional_refs"] = ["mom"]
    result, _ = asyncio.run(interpret(data))
    refs = [s.subject_refs for s in result.semantic_requirements]
    assert refs == [("subject_1", "subject_2"), ("subject_2",), ("subject_3",), ("party",)]
    assert [s.label for s in result.subjects] == ["Requester", "Mother", "Two friends"]
    # A temporary handle spelled party has no special semantic authority.
    data["subjects"][0]["local_key"] = "party"
    data["semantic_requirements"][0]["subject_target"]["first_ref"] = "party"
    renamed, _ = asyncio.run(interpret(data))
    assert renamed.model_dump() == result.model_dump()


def test_lossless_dedup_rewrites_discovery_and_evidence_links():
    data = wire_draft()
    duplicate = copy.deepcopy(data["semantic_requirements"][1])
    duplicate["local_key"] = "repeat"
    data["semantic_requirements"].append(duplicate)
    data["experience_evidence_requests"].append(
        {**data["experience_evidence_requests"][0], "requirement_ref": "repeat"}
    )
    data["discovery_intents"].append(
        {**data["discovery_intents"][0], "requirement_refs": ["repeat"]}
    )
    result, _ = asyncio.run(interpret(data))
    assert len(result.semantic_requirements) == 4
    assert len(result.experience_evidence_requests) == 1
    assert len(result.discovery_intents[0].requirement_refs) == 3
    supply, _ = downstream(result)
    assert supply["selected_place_ids"] == ("b", "a")
    data["experience_evidence_requests"][-1]["preferred_values"] = ["HIGH"]
    data["experience_evidence_requests"][-1]["avoided_values"] = ["LIGHT"]
    with pytest.raises(RequirementBoundaryError, match="conflicting_experience_targets"):
        asyncio.run(interpret(data))


def test_unknown_direction_remains_unknown_and_hard_is_not_softened():
    data = wire_draft()
    evidence = data["experience_evidence_requests"][0]
    evidence["preferred_values"] = evidence["avoided_values"] = []
    hard = copy.deepcopy(data["semantic_requirements"][0])
    hard.update(
        local_key="hard",
        normalized_text="Absolutely no stairs.",
        strength="hard",
        source_refs=[{"quote": "Absolutely no stairs.", "occurrence": 0}],
    )
    data["semantic_requirements"].append(hard)
    result, _ = asyncio.run(interpret(data))
    assert result.semantic_requirements[-1].strength == "hard"
    with pytest.raises(ClarificationRequired, match="unsupported_hard"):
        require_resolved_hard(assess_requirements(result))
    supply, _ = downstream(result)
    assert all(
        r["relation"] == "unknown" for rows in supply["profile_relations"].values() for r in rows
    )


def test_genuine_unresolved_attribution_is_clarification():
    data = wire_draft()
    data["semantic_requirements"][0]["subject_target"] = {
        "kind": "unresolved",
        "reason": "Pronoun referent is unclear",
    }
    with pytest.raises(ClarificationRequired, match="unresolved_subject_attribution"):
        asyncio.run(interpret(data))


def test_final_sdk_wire_schema_ownership():
    _, requests = asyncio.run(interpret(wire_draft()))
    assert len(requests) == 1
    wire = requests[0]["text"]["format"]
    assert wire == {"type": "json_schema", **requirement_wire_format()["json_schema"]}
    assert_foundry_schema_contract(wire["schema"])
    definitions = wire["schema"]["$defs"]
    assert "intent_id" not in definitions["FoundryDiscoveryDTO"]["properties"]
    assert "local_key" not in definitions["FoundryNamedRequirementDTO"]["properties"]
    assert "first_ref" in definitions["FoundrySpecifiedTargetDTO"]["required"]
    assert definitions["FoundryPartyTargetDTO"]["properties"]["kind"]["enum"] == ["party"]
    assert set(
        definitions["FoundryEvidenceRequestDTO"]["properties"]["preferred_values"]["items"]["enum"]
    ) == {v.value for values in ALLOWED_VALUES.values() for v in values}


@pytest.mark.parametrize(
    "mode,category",
    [
        ("refusal", "provider_refusal"),
        ("incomplete", "provider_incomplete"),
        ("bad_config", "configuration_failure"),
        ("service_failure", "transport_failure"),
    ],
)
def test_provider_outcomes_are_not_user_ambiguity(mode, category):
    kwargs = (
        {"refusal": True}
        if mode == "refusal"
        else {"status": "incomplete"}
        if mode == "incomplete"
        else {"http_status": 400 if mode == "bad_config" else 503}
    )
    with pytest.raises(RequirementBoundaryError) as error:
        asyncio.run(interpret(wire_draft(), **kwargs))
    assert error.value.category == category


def test_failed_dto_response_is_captured_exactly_and_redacted_without_overwrite(tmp_path):
    data = wire_draft()
    data["semantic_requirements"][0]["subject_target"] = {
        "kind": "specified",
        "additional_refs": [],
    }
    content = json.dumps(data, indent=3) + "  "
    capture = DevelopmentRequirementCapture(tmp_path, scenario_id="synthetic-dto-failure")
    for _ in range(2):
        with pytest.raises(RequirementBoundaryError):
            asyncio.run(interpret(content, capture=capture))
    records = [json.loads(p.read_text()) for p in tmp_path.glob("*.json")]
    responses = [r for r in records if r["validation_stage"] == "response_received"]
    assert len(responses) == 2 and responses[0]["call_id"] != responses[1]["call_id"]
    assert responses[0]["content"][0]["text"] == content
    assert any(r.get("errors") for r in records)
    assert (tmp_path / ".gitignore").read_text() == "*\n"
    capture.record("x", "synthetic", {"content": "test-secret-key"}, secrets=("test-secret-key",))
    assert all("test-secret-key" not in p.read_text() for p in tmp_path.glob("*.json"))


def test_json_duplicate_keys_and_partial_json_are_not_repaired():
    for text in ('{"requirements":{},"requirements":{}}', '{"requirements":'):
        with pytest.raises(RequirementBoundaryError):
            asyncio.run(interpret(text))


def test_canonical_failure_capture_preserves_response_and_failure_stage(tmp_path):
    data = wire_draft()
    data["subjects"][0]["local_key"] = "unlinked_definition"
    capture = DevelopmentRequirementCapture(tmp_path, scenario_id="synthetic-link-failure")
    with pytest.raises(RequirementBoundaryError, match="unknown_subject_reference"):
        asyncio.run(interpret(data, capture=capture))
    records = [json.loads(p.read_text()) for p in tmp_path.glob("*.json")]
    assert len({r["call_id"] for r in records}) == 1
    assert {r["validation_stage"] for r in records} == {
        "response_received",
        "draft_validated",
        "canonicalization",
    }
    failure = next(r for r in records if r["validation_stage"] == "canonicalization")
    assert failure["code"] == "unknown_subject_reference"
    assert failure["status"] == "invalid_model_contract"


def test_capture_is_disabled_by_default():
    client = AzureFoundryStructuredLLMClient(
        endpoint="https://fixture.invalid/openai/v1",
        deployment="fixture-model",
        api_key="test-secret-key",
    )
    assert client.requirement_capture is None


def test_captured_b_draft_reexpressed_in_v2_keeps_meaning_and_party_scope():
    fixture = json.loads(
        (
            Path(__file__).parents[2] / "fixtures/requirement_boundary/captured_b_domain_draft.json"
        ).read_text()
    )
    assert fixture["provenance"]["kind"] == "captured_parsed_domain_draft"
    data = copy.deepcopy(fixture["draft"])
    data.pop("requirements")  # Historical captured form is not model output in revision 3.
    data["operational_conflicts"] = []
    assert any(s["subject_id"] == "party" for s in data["subjects"])
    # Explicit test fixture migration, NOT a runtime legacy repair/fallback.
    data["subjects"] = [
        {"local_key": s["subject_id"], "label": s["label"], "source_refs": s["source_refs"]}
        for s in data["subjects"]
        if s["subject_id"] != "party"
    ]
    for r in data["semantic_requirements"]:
        refs = r.pop("subject_refs")
        r["subject_target"] = (
            {"kind": "party"}
            if refs == ["party"]
            else {"kind": "specified", "first_ref": refs[0], "additional_refs": refs[1:]}
        )
    for n in data["named_places"]:
        n.pop("local_key")
    for d in data["discovery_intents"]:
        d.pop("intent_id")
    for e in data["experience_evidence_requests"]:
        e["requirement_ref"] = e.pop("requirement_id")
    result, _ = asyncio.run(interpret(data, text=fixture["request"]))
    assert len(result.semantic_requirements) == 4 and len(result.subjects) == 1
    assert [r.normalized_text for r in result.semantic_requirements] == [
        r["normalized_text"] for r in fixture["draft"]["semantic_requirements"]
    ]
    assert [r.subject_refs for r in result.semantic_requirements] == [("party",)] * 3 + [
        ("subject_1",)
    ]
    assert result.named_places[0].inclusion == "REQUIRED"


def test_first_reference_is_not_priority_and_negation_conditions_survive():
    data = wire_draft()
    requirement = data["semantic_requirements"][0]
    requirement["subject_target"]["additional_refs"] = ["mom"]
    requirement["normalized_text"] = "Avoid long transfers unless the place is distinctive."
    requirement["polarity"] = "avoid"
    text = TEXT + " Avoid long transfers unless the place is distinctive."
    requirement["source_refs"] = [{"quote": requirement["normalized_text"], "occurrence": 0}]
    first, _ = asyncio.run(interpret(data, text=text))
    requirement["subject_target"].update(first_ref="mom", additional_refs=["me"])
    second, _ = asyncio.run(interpret(data, text=text))
    assert first.model_dump() == second.model_dump()
    assert first.semantic_requirements[-1].normalized_text == requirement["normalized_text"]
    assert first.semantic_requirements[-1].polarity == "avoid"


def test_canonical_validation_rejects_dangling_and_fabricated_provenance():
    result, _ = asyncio.run(interpret(wire_draft()))
    changed = result.model_copy(
        update={
            "semantic_requirements": (
                result.semantic_requirements[0].model_copy(
                    update={"subject_refs": ("nonexistent",)}
                ),
                *result.semantic_requirements[1:],
            )
        }
    )
    with pytest.raises(RequirementBoundaryError, match="invalid_canonical_contract"):
        canonicalize_requirements(changed, make_request(TEXT))
    bad_ref = (
        result.semantic_requirements[0].source_refs[0].model_copy(update={"start": 1, "end": 21})
    )
    changed = result.model_copy(
        update={
            "semantic_requirements": (
                result.semantic_requirements[0].model_copy(update={"source_refs": (bad_ref,)}),
                *result.semantic_requirements[1:],
            )
        }
    )
    with pytest.raises(RequirementBoundaryError):
        canonicalize_requirements(changed, make_request(TEXT))


def test_enum_and_resource_bound_parity():
    from backend.app.schemas.interpreted_requirements import DRAFT_HANDLE_LIMIT, SemanticDraft

    schema = SemanticDraft.model_json_schema()
    wire = requirement_wire_format()["json_schema"]["schema"]["$defs"]["FoundrySemanticDTO"]
    for field in ("kind", "polarity", "strength", "scope"):
        assert wire["properties"][field]["enum"] == schema["properties"][field]["enum"]
    assert DRAFT_HANDLE_LIMIT == 256
    data = wire_draft()
    data["semantic_requirements"][0]["normalized_text"] = "x" * 321
    with pytest.raises(RequirementBoundaryError) as error:
        asyncio.run(interpret(data))
    assert error.value.stage == "draft_domain"
