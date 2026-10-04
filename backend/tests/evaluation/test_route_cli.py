"""Local route CLI behavior over frozen synthetic batches; no network access."""

import json
import socket

import pytest

from backend.evaluation.route_cli import main
from backend.tests.evaluation import test_requirement_schedule as schedule_tests
from backend.tests.evaluation import test_routes as route_tests

pytest_plugins = ("backend.tests.evaluation.test_intake",)
prepared_scenario = schedule_tests.scenario
route_case = route_tests.route_case


def arguments(case, command="score"):
    intake, identity, directory, ctx, reviews, coords, _ = case
    root = directory.parent
    for name, data in (
        ("identity", identity.to_dict()),
        ("context", ctx),
        ("reviews", reviews),
        ("coordinates", coords),
    ):
        (root / (name + ".json")).write_text(json.dumps(data), encoding="utf-8")
    args = [command, str(root / "manifest.json"), str(root / "identity.json")]
    if command == "score":
        args.append(str(directory))
    return args + [
        "--context",
        str(root / "context.json"),
        "--route-reviews",
        str(root / "reviews.json"),
        "--coordinates",
        str(root / "coordinates.json"),
    ]


def test_local_cli_prepares_and_scores_deterministic_reports(route_case, capsys):
    case = route_case()
    assert main(arguments(case, "prepare")) == 0
    prepared = json.loads(capsys.readouterr().out)
    assert prepared["status"] == "complete"
    assert len(prepared["route_contexts"]) == 3
    assert main(arguments(case)) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "complete"
    assert report["results"][1]["routes"]["counts"]["PASS"] == 1


def test_cli_replay_never_constructs_socket_or_mutates_supplied_material(
    route_case, capsys, monkeypatch
):
    case = route_case()
    args = arguments(case)
    root = case[2].parent
    before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}

    def forbidden(*args, **kwargs):
        raise AssertionError("Offline route replay must not construct a socket")

    monkeypatch.setattr(socket, "socket", forbidden)
    assert main(args) == 0
    report = json.loads(capsys.readouterr().out)
    assert main(args) == 0
    assert json.loads(capsys.readouterr().out) == report
    assert {
        str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()
    } == before


@pytest.mark.parametrize(
    "fault",
    ["manifest", "identity", "context", "reviews", "coordinates", "snapshot", "stale_identity"],
)
def test_cli_invalid_preparation_has_structured_error_and_no_partial_cohort(
    route_case, capsys, fault
):
    case = route_case()
    args = arguments(case)
    if fault == "stale_identity":
        path = case[2].parent / "identity.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.pop("subject_scope_version")
        path.write_text(json.dumps(data), encoding="utf-8")
    elif fault in ("manifest", "identity", "snapshot"):
        args[{"manifest": 1, "identity": 2, "snapshot": 3}[fault]] = str(case[2].parent / "absent")
    else:
        flag = {
            "context": "--context",
            "reviews": "--route-reviews",
            "coordinates": "--coordinates",
        }[fault]
        args[args.index(flag) + 1] = str(case[2].parent / "absent.json")
    assert main(args) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == (
        "identity_replay_required" if fault == "stale_identity" else "needs_material_correction"
    )
    assert report["results"] == []
    assert report["diagnostics"]


def test_quality_failure_is_complete_replay_exit_zero(route_case, capsys):
    case = route_case({"status": {}, "condition": "ROUTE_NOT_FOUND"})
    assert main(arguments(case)) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["results"][1]["routes"]["counts"]["FAIL"] == 1
