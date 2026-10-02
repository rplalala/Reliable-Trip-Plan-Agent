"""Revision-aware import and mapped human outcomes through public interfaces."""

import copy

import pytest

from backend.evaluation.human_answers import validate_answers
from backend.evaluation.records import MaterialError
from backend.tests.evaluation.test_human_tasks import package

pytest_plugins = ("backend.tests.evaluation.test_intake",)


def answer(public, revision=1, state="submitted", groups=None, task=0):
    return {
        "answer_schema_version": "rtpeval_human_answer_1",
        **{
            k: public[k]
            for k in (
                "batch_id",
                "batch_revision",
                "presentation_id",
                "presentation_hash",
                "rater_ref",
            )
        },
        "task_id": public["tasks"][task]["task_id"],
        "answer_revision": revision,
        "updated_at": "2026-10-02T10:00:00+10:00",
        "state": state,
        "responses": {
            d: {"status": "ranked", "tie_groups": groups or [["A", "B"], ["C"], ["D"]]}
            for d in public["dimensions"]
        },
    }


def bundle(*records):
    return {"schema_version": "rtpeval_human_answers_1", "answers": list(records)}


def test_newest_complete_submission_overrides_old_answer_without_counting_draft(batch):
    material = package(batch)
    public, private = material["public"], material["private"]
    old, new = answer(public), answer(public, 2, groups=[["D"], ["C"], ["B"], ["A"]])
    draft = answer(public, 3, "draft")
    result = validate_answers(public, private, [bundle(new, old, draft), bundle(new)])
    assert len(result["records"]) == 3
    assert result["effective"][0]["answer_revision"] == 2
    assert result["effective"][0]["responses"]["pace"]["tie_groups"] == [["D"], ["C"], ["B"], ["A"]]
    assert result == validate_answers(public, private, [bundle(old, draft), bundle(new)])


@pytest.mark.parametrize(
    "change",
    [
        {"presentation_hash": "0" * 64},
        {"answer_revision": True},
        {"updated_at": "2026-10-02T10:00:00"},
        {"task_id": "missing"},
        {
            "responses": {
                "preference": {"status": "ranked", "tie_groups": [["A"], ["A", "B", "C", "D"]]}
            }
        },
        {"responses": {"preference": {"status": "pending"}}},
        {"private_mapping": {}},
    ],
)
def test_invalid_bundle_is_rejected_atomically(batch, change):
    material = package(batch)
    original = answer(material["public"])
    invalid = {**original, **change}
    with pytest.raises(MaterialError):
        validate_answers(material["public"], material["private"], [bundle(original, invalid)])


def test_conflict_is_not_overwritten_and_unassessable_is_not_a_tie(batch):
    material = package(batch)
    original = answer(material["public"])
    conflict = copy.deepcopy(original)
    conflict["responses"]["pace"] = {"status": "unable_to_judge", "reason": "Missing times"}
    with pytest.raises(MaterialError, match="Conflicting"):
        validate_answers(
            material["public"], material["private"], [bundle(original), bundle(conflict)]
        )
    conflict["answer_revision"] = 2
    conflict["responses"]["usefulness"] = {"status": "not_applicable"}
    selected = validate_answers(
        material["public"], material["private"], [bundle(original, conflict)]
    )
    assert selected["effective"][0]["responses"]["pace"]["status"] == "unable_to_judge"
    assert selected["effective"][0]["responses"]["usefulness"]["status"] == "not_applicable"
