"""V3-only evaluation preparations preserve independent source/review linkage."""

from backend.evaluation.identity import identity_references
from backend.evaluation.records import canonical_digest
from backend.tests.evaluation.test_controlled_replay import case, replay
from backend.tests.versions.v3.test_validation import NOW


def requirements(value):
    return {
        "schema_version": "rtpeval_requirements_1",
        "spec_id": "synthetic-spec",
        "revision": "1",
        "group_id": value["case_id"],
        "input_sha256": canonical_digest(value["original_input"]),
        "review": {
            "status": "reviewed",
            "reviewer_ref": "synthetic-reviewer",
            "reviewed_at": NOW.isoformat(),
        },
        "subjects": [],
        "obligations": [],
        "soft_preferences": [],
        "unresolved_items": [],
    }


def test_controlled_preparation_has_only_real_v3_sources_and_identity_references():
    from backend.evaluation.controlled_preparation import prepare_controlled_case

    value = case()
    prepared = prepare_controlled_case(value, replay(value), requirements(value)).to_dict()
    assert prepared["status"] == "accepted"
    assert set(prepared["inventory"][0]["runs"]) == {"v3"}
    refs = identity_references(prepared)
    assert len(refs) == 3
    assert {r["projection"] for r in refs} == {"final", "draft", "final_primary"}
    assert {r["version"] for r in refs} == {"v3"}
