"""Public offline controlled commands and denominator-preserving report inventory."""

import json

from backend.tests.evaluation.test_controlled_preparation import requirements
from backend.tests.evaluation.test_controlled_replay import case


def write(root, name, value):
    path = root / name
    path.write_text(json.dumps(value), encoding="utf-8")
    return str(path)


def test_cli_replay_prepare_and_identity_reference_flow(tmp_path, capsys):
    from backend.evaluation.controlled_cli import main

    value = case()
    path = write(tmp_path, "case.json", value)
    assert main(["replay", path]) == 0
    execution = json.loads(capsys.readouterr().out)
    executed = write(tmp_path, "execution.json", execution)
    spec = write(tmp_path, "requirements.json", requirements(value))
    assert main(["prepare", path, executed, spec]) == 0
    preparation = json.loads(capsys.readouterr().out)
    saved = write(tmp_path, "prepared.json", preparation)
    assert main(["identity-references", saved]) == 0
    references = json.loads(capsys.readouterr().out)
    assert len(references["records"]) == 3
    assert {r["version"] for r in references["records"]} == {"v3"}
    assert main(["identity-plan", saved]) == 0
    plan = json.loads(capsys.readouterr().out)
    assert plan["schema_version"] == "rtpeval_snapshot_plan_1"
    assert plan["requests"]


def test_cli_duplicate_json_keys_fail_material_integrity(tmp_path, capsys):
    from backend.evaluation.controlled_cli import main

    path = tmp_path / "bad.json"
    path.write_text('{"case_id":"one","case_id":"two"}', encoding="utf-8")
    assert main(["replay", str(path)]) == 2
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "needs_material_correction"


def test_missing_batch_report_keeps_declared_case_and_expected_targets(tmp_path):
    from backend.evaluation.controlled_batch import build_controlled_batch

    manifest = {
        "schema_version": "rtpeval_controlled_batch_1",
        "batch_id": "synthetic",
        "revision": "one",
        "cases": [
            {
                "case_id": "missing-target",
                "role": "target",
                "expected_goal_ids": ["opening", "route"],
                "report": {
                    "path": "missing.json",
                    "sha256": "a" * 64,
                    "media_type": "application/json",
                    "availability": "available",
                    "schema_version": "rtpeval_controlled_report_1",
                },
            }
        ],
    }
    out = build_controlled_batch(manifest, tmp_path, generated_at="2026-10-04T00:00:00Z")
    assert out["status"] == "needs_material_correction"
    assert out["counts"]["expected_cases"] == 1
    assert out["counts"]["expected_targets"] == 2
    assert out["counts"]["resolved_targets"] == 0
    assert out["cases"][0]["status"] == "unavailable"
