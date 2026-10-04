"""Offline opening CLI preparation integrity, deterministic replay and immutability."""

import json
import socket

import pytest

from backend.evaluation.opening_cli import main
from backend.tests.evaluation import test_opening as opening_tests
from backend.tests.evaluation import test_requirement_schedule as schedule_tests

pytest_plugins = ("backend.tests.evaluation.test_intake",)
prepared_scenario = schedule_tests.scenario
opening_scenario = opening_tests.opening_scenario


def test_cli_replays_without_socket_construction_or_source_mutation(
    opening_scenario, capsys, monkeypatch
):
    _, identity, directory, plan, root = opening_scenario()
    identity_path, plan_path = root / "identity.json", root / "expected-plan.json"
    identity_path.write_text(json.dumps(identity.to_dict()), encoding="utf-8")
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}

    def forbidden(*args, **kwargs):
        raise AssertionError("Offline opening replay must not construct a socket")

    monkeypatch.setattr(socket, "socket", forbidden)
    args = [
        str(root / "manifest.json"),
        str(identity_path),
        str(directory),
        "--expected-plan",
        str(plan_path),
    ]
    assert main(args) == 0
    report = json.loads(capsys.readouterr().out)
    assert main(args) == 0
    assert json.loads(capsys.readouterr().out) == report
    assert {
        str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()
    } == before
    assert all(
        len(report["preparation_file_sha256"][field]) == 64
        for field in ("identity", "expected_plan")
    )


@pytest.mark.parametrize(
    "fault", ["identity_file", "context_file", "manifest_file", "snapshot", "stale_identity"]
)
def test_cli_errors_are_structured_and_have_no_partial_cohort(opening_scenario, capsys, fault):
    _, identity, directory, _, root = opening_scenario()
    path = root / "identity.json"
    report = identity.to_dict()
    if fault == "stale_identity":
        report.pop("subject_scope_version")
    path.write_text(json.dumps(report), encoding="utf-8")
    args = [str(root / "manifest.json"), str(path), str(directory)]
    if fault == "identity_file":
        args[1] = str(root / "absent.json")
    elif fault == "context_file":
        args.extend(["--context", str(root / "absent.json")])
    elif fault == "manifest_file":
        args[0] = str(root / "absent.json")
    elif fault == "snapshot":
        args[2] = str(root / "absent-snapshot")
    assert main(args) == 2
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == (
        "identity_replay_required" if fault == "stale_identity" else "needs_material_correction"
    )
    assert output["results"] == []
    assert output["diagnostics"]
