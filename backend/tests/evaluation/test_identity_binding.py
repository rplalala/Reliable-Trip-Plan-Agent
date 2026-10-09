"""V0 decision applicability through the public versioned identity interface."""

import copy

import pytest

from backend.evaluation.identity import identity_references
from backend.evaluation.identity_program import resolve_versioned_identities
from backend.tests.evaluation.test_identity import evidence, prepared, search
from backend.tests.evaluation.test_identity_llm import model_material

pytest_plugins = ("backend.tests.evaluation.test_intake",)


def test_v0_decisions_survive_unrelated_batch_revision_with_original_receipt(batch):
    intake = prepared(batch).to_dict()
    observed = evidence(
        intake_object(intake), [search(r, r["name"]) for r in identity_references(intake)]
    )
    material = model_material(intake, observed, historical=False)
    material.update(
        schema_version="rtpeval_identity_model_result_2",
        binding_source={"intake": copy.deepcopy(intake), "evidence": copy.deepcopy(observed)},
    )
    before = copy.deepcopy(material)

    def change(manifest, results, _save, _root):
        manifest["revision"] = "2"
        results["v1"]["itinerary"]["days"][0]["activities"][0]["place_name"] = "Other venue"
        return "v1"

    revised = prepared(batch, change).to_dict()
    updated = evidence(
        intake_object(revised), [search(r, r["name"]) for r in identity_references(revised)]
    )
    for row in updated["records"]:
        row["observation_id"] = "new-wrapper-" + row["reference_id"]
    report = resolve_versioned_identities(revised, updated, model_result=material).to_dict()
    v0 = [r for r in report["records"] if r["version"] == "v0"]
    assert len(v0) == 2 and all(r["grounding_verdict"] == "PASS" for r in v0)
    assert report["batch_revision"] == "2"
    assert material == before
    assert report["model_judgment_provenance"]["binding"] == "verified_v0_case_facts"


def test_bound_requirement_target_rejects_changed_related_count_meaning(batch):
    import json

    manifest, _, _, save, root = batch
    spec = json.loads((root / "requirements.json").read_bytes())
    spec["subjects"] = [{"subject_id": "museum", "place_name": "Museum A"}]
    spec["obligations"] = [
        {
            "obligation_id": "once",
            "kind": "required_visit",
            "resolution": "resolved",
            "subject_ref": "museum",
            "count": {"mode": "exact", "value": 1},
            "source_refs": [{"field_path": "additional_preferences", "quote": "architecture"}],
        }
    ]
    manifest["groups"][0]["requirement_spec_ref"] = save(
        "requirements.json", spec, spec["schema_version"]
    )
    intake = prepared(batch).to_dict()
    observed = evidence(
        intake_object(intake), [search(r, r["name"]) for r in identity_references(intake)]
    )
    material = model_material(intake, observed, historical=False)
    material.update(
        schema_version="rtpeval_identity_model_result_2",
        binding_source={"intake": copy.deepcopy(intake), "evidence": copy.deepcopy(observed)},
    )
    intake["inventory"][0]["requirement_spec"]["obligations"][0]["count"]["value"] = 2
    with pytest.raises(ValueError, match="binding facts changed"):
        resolve_versioned_identities(intake, observed, model_result=material)


class intake_object:
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return self.value


@pytest.mark.parametrize("change", ["claim", "candidate", "capture", "policy", "source"])
def test_bound_decisions_reject_changed_relevant_facts(batch, change):
    intake = prepared(batch).to_dict()
    observed = evidence(
        intake_object(intake), [search(r, r["name"]) for r in identity_references(intake)]
    )
    material = model_material(intake, observed, historical=False)
    material.update(
        schema_version="rtpeval_identity_model_result_2",
        binding_source={"intake": copy.deepcopy(intake), "evidence": copy.deepcopy(observed)},
    )
    row = observed["records"][0]
    if change == "claim":
        intake["inventory"][0]["runs"]["v0"]["final"]["activities"][0]["original"]["place_name"] = (
            "Changed"
        )
    elif change == "candidate":
        row["search"]["candidates"][0]["formatted_address"] = "Changed address"
    elif change == "capture":
        row["search"]["retrieved_at"] = "2026-09-30T00:00:00Z"
    elif change == "policy":
        material["packet"]["association_policy_version"] = "future-policy"
    else:
        material["binding_source"]["evidence"]["records"][0]["search"]["query"] = "Foreign"
    with pytest.raises(ValueError):
        resolve_versioned_identities(intake, observed, model_result=material)
