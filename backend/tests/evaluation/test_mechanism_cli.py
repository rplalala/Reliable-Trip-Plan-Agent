"""Offline researcher workflow through persisted public CLI artifacts."""

import json

from backend.evaluation.mechanism_cli import main
from backend.tests.evaluation.test_intake import batch as selected_batch
from backend.tests.evaluation.test_official_audit import preparation, review

batch = selected_batch


def test_public_four_version_workflow(batch, tmp_path):
    _, _, write, _, _ = batch
    prepared, report, queue, audit = [
        tmp_path / name for name in ("prepared.json", "report.json", "queue.json", "audit.json")
    ]
    assert main(["prepare", "--manifest", str(write()), "--output", str(prepared)]) == 0
    assert main(["report", str(prepared), "--output", str(report)]) == 0
    assert main(["audit-queue", str(prepared), "--output", str(queue)]) == 0
    assert main(["audit-report", str(queue), "--output", str(audit)]) == 0
    assert len(json.loads(report.read_text())["runs"]) == 4
    assert json.loads(audit.read_text())["counts"]["qualifying"] is None
    assert json.loads(audit.read_text())["counts"]["observed_qualifying"] == 0


def test_persisted_review_workflow_and_failed_review_exit_code(tmp_path):
    prepared, queue, reviews = [
        tmp_path / name for name in ("prepared.json", "queue.json", "reviews.json")
    ]
    prepared.write_text(json.dumps(preparation()), encoding="utf-8")
    assert main(["audit-queue", str(prepared), "--output", str(queue)]) == 0
    value = json.loads(queue.read_text())
    reviews.write_text(json.dumps(review(value)), encoding="utf-8")
    assert main(["audit-report", str(queue), "--reviews", str(reviews)]) == 0
    stale = review(value)
    stale["queue_sha256"] = "f" * 64
    reviews.write_text(json.dumps(stale), encoding="utf-8")
    assert main(["audit-report", str(queue), "--reviews", str(reviews)]) == 2


def test_genuine_ticket11_v3_only_selection_does_not_invent_other_versions(tmp_path):
    from backend.evaluation.controlled_preparation import prepare_controlled_case
    from backend.tests.evaluation.test_controlled_preparation import requirements
    from backend.tests.evaluation.test_controlled_replay import case, replay

    value = case()
    selection = prepare_controlled_case(value, replay(value), requirements(value)).to_dict()
    source, prepared, report = [
        tmp_path / name for name in ("selection.json", "prepared.json", "report.json")
    ]
    source.write_text(json.dumps(selection), encoding="utf-8")
    assert main(["prepare", "--selection", str(source), "--output", str(prepared)]) == 0
    assert main(["report", str(prepared), "--output", str(report)]) == 0
    runs = json.loads(report.read_text())["runs"]
    assert len(runs) == 1 and runs[0]["version"] == "v3"
    assert runs[0]["coverage"] == "available"
    assert runs[0]["triggered"] is False and runs[0]["model_attempts"] == 0
