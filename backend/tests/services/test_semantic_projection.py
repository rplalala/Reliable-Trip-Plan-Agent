"""Canonical identities stay application-owned at the model boundary."""

import asyncio
import json

import pytest

from backend.app.schemas.poi_semantics import SemanticAssessmentError
from backend.tests.services.test_poi_semantics import Model, service
from backend.tests.versions.v3.test_validation import contract, place


def test_model_uses_short_references_and_reordered_results_restore_canonical_identity():
    class WireModel:
        async def generate_poi_semantics_structured(self, **kwargs):
            data = json.loads(kwargs["user_prompt"])
            assert "canonical-long-A" not in kwargs["user_prompt"]
            assert data["places"][0]["candidate_ref"] == "p01"
            assert data["places"][0]["source_ref"] == "e01"
            return {
                "assessments": [
                    dict(
                        candidate_ref=p["candidate_ref"],
                        visit_object=p["name"],
                        role="attraction",
                        categories=[],
                        reason="Supplied facts",
                        evidence_refs=[p["source_ref"]],
                        matches=[],
                        exception_requirement_ids=[],
                    )
                    for p in reversed(data["places"])
                ]
            }

    a = place("canonical-long-A").model_copy(update={"name": "Museum A"})
    b = place("canonical-long-B").model_copy(update={"name": "Museum B"})
    result = asyncio.run(service(WireModel()).assess([a, b], contract()))
    assert result[a.place_id].visit_object == "Museum A"
    assert result[a.place_id].evidence_refs == [a.source_ref]
    assert result[b.place_id].evidence_refs == [b.source_ref]


@pytest.mark.parametrize("bad_ref", ["e02", "e99", "places:a"])
def test_wire_reference_must_belong_to_the_selected_candidate(bad_ref):
    def mutate(rows):
        rows[0]["evidence_refs"] = [bad_ref]

    svc = service(Model(mutate))
    with pytest.raises(SemanticAssessmentError):
        asyncio.run(svc.assess([place("a"), place("b")], contract()))
    assert svc.calls == 2 and not svc.cache and not svc.ledger


def test_correction_keeps_mapping_and_captures_wire_and_canonical_results():
    from backend.tests.services.test_poi_semantics import CorrectingModel

    model = CorrectingModel()
    svc = service(model)
    asyncio.run(svc.assess([place("a"), place("b")], contract()))
    inputs = [payload for stage, payload in model.captures if stage == "input"]
    assert inputs[0]["reference_mapping"] == inputs[1]["reference_mapping"]
    assert inputs[0]["reference_mapping"]["p01"] == {
        "place_id": "a",
        "source_ref": "places:a",
        "evidence_ref": "e01",
    }
    assert inputs[0]["mapping_sha256"] == inputs[1]["mapping_sha256"]
    assert "reference_mapping" not in model.inputs[0]
    output = [p for stage, p in model.captures if stage == "output"][-1]
    assert output["output"]["assessments"][0]["candidate_ref"] == "p01"
    assert svc.records[-1]["assessments"]["assessments"][0]["place_id"] == "a"


def test_named_binding_is_projected_only_into_its_own_batch_and_cache_stays_canonical():
    class BoundModel(Model):
        def __init__(self):
            super().__init__()
            self.inputs = []

        async def generate_poi_semantics_structured(self, **kwargs):
            data = json.loads(kwargs["user_prompt"])
            self.inputs.append(data)
            result = await super().generate_poi_semantics_structured(**kwargs)
            if data["application_named_bindings"]:
                result["assessments"][0].update(
                    role="exception_only",
                    exception_requirement_ids=["named_1"],
                    matches=[
                        dict(requirement_id="named_1", relation="supported", evidence_refs=["e01"])
                    ],
                )
            return result

    model = BoundModel()
    svc = service(model, batch_size=1)
    svc.named_bindings = {"named_1": "b"}

    async def run():
        result = await svc.assess([place("a"), place("b")], contract("REQUIRED"))
        assert result["a"].role == "attraction"
        assert result["b"].role == "exception_only"
        assert result["b"].matches[0].evidence_refs == ["places:b"]
        again = await svc.assess([place("b"), place("a")], contract("REQUIRED"))
        assert again == result and svc.calls == 2

    asyncio.run(run())
    assert model.inputs[0]["application_named_bindings"] == {}
    assert model.inputs[1]["application_named_bindings"] == {"named_1": "p01"}
    assert svc.records[0]["mapping_sha256"] != svc.records[1]["mapping_sha256"]


def test_projection_version_invalidates_cached_assessments(monkeypatch):
    import backend.app.services.poi_semantics as module

    svc = service()
    asyncio.run(svc.assess([place()], contract()))
    monkeypatch.setattr(module, "PROJECTION_VERSION", "changed_wire_version")
    asyncio.run(svc.assess([place()], contract()))
    assert svc.calls == 2
