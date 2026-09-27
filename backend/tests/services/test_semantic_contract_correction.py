"""Bounded correction at the public semantic service boundary."""

import asyncio
import json

import pytest

from backend.app.schemas.poi_semantics import SemanticAssessmentError
from backend.tests.services.test_poi_semantics import Model, service
from backend.tests.versions.v3.test_validation import contract, place


class SequenceModel(Model):
    def __init__(self, mutations):
        super().__init__()
        self.mutations = mutations
        self.inputs = []

    async def generate_poi_semantics_structured(self, **kwargs):
        self.inputs.append(json.loads(kwargs["user_prompt"]))
        result = await super().generate_poi_semantics_structured(**kwargs)
        mutation = self.mutations[min(self.calls - 1, len(self.mutations) - 1)]
        mutation(result["assessments"])
        return result


def unchanged(rows):
    pass


def wrong_identity(rows):
    rows[0]["candidate_ref"] = "invented"
    rows[0]["evidence_refs"] = ["places:invented"]


@pytest.mark.parametrize(
    "mutation,missing,unexpected,duplicate",
    [
        (wrong_identity, ["p01"], ["invented"], []),
        (lambda rows: rows.pop(), ["p02"], [], []),
        (lambda rows: rows.append(rows[0].copy()), [], [], ["p01"]),
    ],
)
def test_identity_contract_is_corrected_as_complete_batch(mutation, missing, unexpected, duplicate):
    model = SequenceModel([mutation, unchanged])
    svc = service(model)

    async def run():
        result = await svc.prepare([place("a"), place("b")], contract())
        assert set(result) == {"a", "b"}
        assert result["a"].evidence_refs == ["places:a"]
        await svc.assess([place("a"), place("b")], contract())

    asyncio.run(run())
    assert model.calls == 2
    details = model.inputs[1]["contract_correction"]["details"]
    assert details["missing_ids"] == missing
    assert details["unexpected_ids"] == unexpected
    assert details["duplicate_ids"] == duplicate
    assert model.inputs[0]["places"] == model.inputs[1]["places"]
    assert svc.records[1]["correction_of"] == svc.records[0]["call_id"]


def food_contract(*, authorized=False):
    from backend.app.schemas.interpreted_requirements import ExperienceGoal
    from backend.tests.policies.test_planning_supply import contract as make_contract

    req = make_contract()
    semantic = req.semantic_requirements[0].model_copy(
        update={
            "normalized_text": "We enjoy local food.",
            "experience_goal": ExperienceGoal(
                frequency="one_off" if authorized else "continuing",
                count=None,
                target="category",
                distinct_dates=False,
                explicit_primary_exception=authorized,
                trip_scope="ordinary",
            ),
        }
    )
    return req.model_copy(update={"semantic_requirements": (semantic,)})


def exception_claim(rows):
    rows[0].update(
        role="exception_only",
        exception_requirement_ids=["semantic_1"],
        matches=[dict(requirement_id="semantic_1", relation="supported", evidence_refs=["e01"])],
    )


def non_main(rows):
    rows[0]["role"] = "non_main"


def test_ordinary_food_exception_can_be_corrected_without_granting_permission():
    model = SequenceModel([exception_claim, non_main])
    svc = service(model)
    result = asyncio.run(svc.prepare([place()], food_contract()))
    assert not result["a"].main_eligible
    assert model.calls == 2
    details = model.inputs[1]["contract_correction"]["details"]
    assert details["code"] == "unauthorized_exception"
    assert details["place_id"] == "p01"
    assert details["requirement_id"] == "semantic_1"
    assert details["explicit_primary_exception"] is False
    assert details["permission_granted"] is False
    assert details["supported_match"] is True
    assert details["allowed_exception_requirement_ids"] == []


@pytest.mark.parametrize(
    "mutations",
    [
        [wrong_identity, lambda rows: rows[0].update(evidence_refs=["wrong"])],
        [exception_claim, wrong_identity],
        [exception_claim, exception_claim],
        [wrong_identity, wrong_identity],
    ],
)
def test_cross_class_failures_share_one_correction_and_never_cache(mutations):
    model = SequenceModel(mutations)
    svc = service(model)
    with pytest.raises(SemanticAssessmentError):
        asyncio.run(svc.prepare([place()], food_contract()))
    assert model.calls == 2 and not svc.cache and not svc.ledger
    with pytest.raises(SemanticAssessmentError, match="already failed"):
        asyncio.run(svc.assess([place()], food_contract()))
    assert model.calls == 2


@pytest.mark.parametrize("authorized", [False, True])
def test_semantic_exception_authorization_stays_strict(authorized):
    model = SequenceModel([exception_claim])
    svc = service(model)
    if authorized:
        result = asyncio.run(svc.assess([place()], food_contract(authorized=True)))
        assert result["a"].main_eligible and model.calls == 1
    else:
        with pytest.raises(SemanticAssessmentError, match="Unauthorized"):
            asyncio.run(svc.assess([place()], food_contract()))
        assert model.calls == 2 and not svc.ledger


def test_authorized_exception_wrong_role_is_corrected():
    def wrong_role(rows):
        exception_claim(rows)
        rows[0]["role"] = "attraction"

    model = SequenceModel([wrong_role, exception_claim])
    svc = service(model)
    assert asyncio.run(svc.assess([place()], food_contract(authorized=True)))["a"].main_eligible
    assert model.calls == 2
    assert model.inputs[1]["contract_correction"]["details"]["code"] == "exception_role_mismatch"


@pytest.mark.parametrize("mutation", [wrong_identity, exception_claim])
def test_new_contract_classes_cannot_bypass_call_budget(mutation):
    model = SequenceModel([mutation, unchanged])
    svc = service(model, max_calls=1)
    with pytest.raises(SemanticAssessmentError, match="correction unavailable"):
        asyncio.run(svc.prepare([place()], food_contract()))
    assert model.calls == 1 and not svc.ledger
    assert svc.records[-1]["reason"] == "poi_semantics_call_budget_exhausted"


def test_identity_feedback_is_bounded_and_does_not_invent_mapping():
    def long_id(rows):
        rows[0]["candidate_ref"] = "x" * 2000

    model = SequenceModel([long_id, unchanged])
    svc = service(model)
    asyncio.run(svc.assess([place()], contract()))
    details = model.inputs[1]["contract_correction"]["details"]
    assert details["unexpected_ids"] == ["x" * 256]
    assert details["missing_ids"] == ["p01"] and details["truncated"]


@pytest.mark.parametrize("relation", ["supported", "unresolved", None])
def test_named_permission_requires_binding_and_supported_match(relation):
    def named_claim(rows):
        rows[0].update(
            role="exception_only",
            exception_requirement_ids=["named_1"],
            matches=[dict(requirement_id="named_1", relation=relation, evidence_refs=["e01"])]
            if relation
            else [],
        )

    for inclusion, binding in [("REQUIRED", "a"), ("REQUIRED", "b"), ("OPTIONAL", "a")]:
        model = SequenceModel([named_claim])
        svc = service(model)
        svc.named_bindings = {"named_1": binding}
        if inclusion == "REQUIRED" and binding == "a" and relation == "supported":
            assert asyncio.run(svc.assess([place()], contract(inclusion)))["a"].main_eligible
            assert model.calls == 1
        else:
            with pytest.raises(SemanticAssessmentError):
                asyncio.run(svc.assess([place()], contract(inclusion)))
            assert model.calls == 2
