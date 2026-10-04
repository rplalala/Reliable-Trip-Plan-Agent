"""Offline CLI replay, input immutability and delivery error diagnostics."""

import json
import socket

from backend.evaluation.requirement_schedule_cli import main
from backend.tests.evaluation import test_requirement_schedule as schedule_tests

pytest_plugins = ("backend.tests.evaluation.test_intake",)
scenario = schedule_tests.scenario


def test_cli_replays_without_network_or_source_mutation(scenario, capsys, monkeypatch):
    intake, identity, root = scenario()
    identity_path = root / "identity.json"
    identity_path.write_text(json.dumps(identity.to_dict()), encoding="utf-8")
    before = {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()}

    def forbidden(*args, **kwargs):
        raise AssertionError("No network is allowed in offline scoring")

    monkeypatch.setattr(socket, "socket", forbidden)
    args = [str(root / "manifest.json"), str(identity_path)]
    assert main(args) == 0
    first = json.loads(capsys.readouterr().out)
    assert main(args) == 0
    assert json.loads(capsys.readouterr().out) == first
    assert {p.name: p.read_bytes() for p in root.iterdir() if p.is_file()} == before
    assert first["batch_id"] == intake.to_dict()["batch_id"]


def test_cli_missing_identity_file_returns_material_diagnostic(scenario, capsys):
    _, _, root = scenario()
    assert main([str(root / "manifest.json"), str(root / "absent.json")]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []
