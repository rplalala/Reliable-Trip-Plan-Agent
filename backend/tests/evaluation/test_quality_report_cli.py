"""Real offline CLI replay with immutable inputs and exact file provenance."""

import hashlib
import json
import socket
from datetime import datetime

import pytest

from backend.evaluation.quality_report import quality_content_hash
from backend.evaluation.quality_report_cli import main
from backend.tests.evaluation import test_route_cli as route_cli_tests
from backend.tests.evaluation import test_routes as route_tests
from backend.tests.evaluation.test_daily_density import density_reviews

pytest_plugins = ("backend.tests.evaluation.test_intake",)
prepared_scenario = route_tests.prepared_scenario
route_case = route_tests.route_case


def arguments(case):
    return route_cli_tests.arguments(case)[1:] + ["--generated-at", "2026-10-02T00:00:00Z"]


def test_cli_is_deterministic_offline_and_preserves_exact_file_provenance(
    route_case, capsys, monkeypatch
):
    case = route_case()
    args = arguments(case)
    root = case[2].parent
    before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}

    def forbidden(*args, **kwargs):
        raise AssertionError("Quality replay must not construct a socket")

    monkeypatch.setattr(socket, "socket", forbidden)
    assert main(args) == 0
    output = capsys.readouterr().out
    report = json.loads(output)
    assert report["status"] == "complete"
    assert (
        report["preparation_file_sha256"]["identity"]
        == hashlib.sha256(before["identity.json"]).hexdigest()
    )
    assert report["content_hash"] == quality_content_hash(report)
    assert main(args) == 0
    assert capsys.readouterr().out == output
    assert {
        str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()
    } == before


@pytest.mark.parametrize(
    "fault",
    [
        "manifest",
        "identity",
        "context",
        "reviews",
        "coordinates",
        "occupancy",
        "expected_plan",
        "snapshot",
        "stale_identity",
        "timestamp",
    ],
)
def test_cli_invalid_preparation_emits_whole_batch_diagnostics(route_case, capsys, fault):
    case = route_case()
    args = arguments(case)
    absent = str(case[2].parent / "absent.json")
    if fault == "stale_identity":
        path = case[2].parent / "identity.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.pop("subject_scope_version")
        path.write_text(json.dumps(data), encoding="utf-8")
    elif fault in ("manifest", "identity", "snapshot"):
        args[{"manifest": 0, "identity": 1, "snapshot": 2}[fault]] = absent
    elif fault == "timestamp":
        args[-1] = "2026-10-02T00:00:00"
    elif fault in ("occupancy", "expected_plan"):
        args += [
            {"occupancy": "--occupancy-reviews", "expected_plan": "--expected-plan"}[fault],
            absent,
        ]
    else:
        flag = {
            "context": "--context",
            "reviews": "--route-reviews",
            "coordinates": "--coordinates",
        }[fault]
        args[args.index(flag) + 1] = absent
    assert main(args) == 2
    out = json.loads(capsys.readouterr().out)
    assert out["groups"] == []
    assert out["diagnostics"]
    assert out["status"] == (
        "identity_replay_required" if fault == "stale_identity" else "needs_material_correction"
    )
    assert out["content_hash"] == quality_content_hash(out)


def test_cli_creation_time_defaults_to_aware_utc(route_case, capsys):
    args = arguments(route_case())[:-2]
    assert main(args) == 0
    out = json.loads(capsys.readouterr().out)
    assert datetime.fromisoformat(out["generated_at"]).utcoffset().total_seconds() == 0


def test_cli_exact_file_hash_differs_from_object_hash_and_changes_content_hash(route_case, capsys):
    case = route_case()
    args = arguments(case)
    assert main(args) == 0
    original = json.loads(capsys.readouterr().out)
    path = case[2].parent / "identity.json"
    path.write_text(
        json.dumps(json.loads(path.read_text(encoding="utf-8")), indent=4), encoding="utf-8"
    )
    assert main(args) == 0
    replayed = json.loads(capsys.readouterr().out)
    assert original["groups"] == replayed["groups"]
    assert original["source_hashes"] == replayed["source_hashes"]
    assert (
        original["preparation_file_sha256"]["identity"]
        != replayed["preparation_file_sha256"]["identity"]
    )
    assert original["content_hash"] != replayed["content_hash"]


def test_cli_replays_density_reviews_with_exact_file_provenance(route_case, capsys):
    case = route_case()
    path = case[2].parent / "density.json"
    path.write_text(json.dumps(density_reviews(case[0], exact_count=1)), encoding="utf-8")
    assert main(arguments(case) + ["--density-reviews", str(path)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert (
        out["preparation_file_sha256"]["density_reviews"]
        == hashlib.sha256(path.read_bytes()).hexdigest()
    )
    v1 = out["groups"][0]["versions"]["v1"]
    assert v1["daily_density"]["mean_penalty_0_100"] == 100
    assert v1["overall_total"]["score_0_100"] == 0
    assert v1["auxiliary_total"]["score_0_100"] == 50
    assert out["content_hash"] == quality_content_hash(out)
