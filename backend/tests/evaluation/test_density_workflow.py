"""Density rules survive actual paired CLI and downstream independent channels."""

import hashlib
import json

from backend.evaluation.mechanism_preparation import read_batch_sources
from backend.evaluation.records import canonical_digest
from backend.evaluation.v3_pair_cli import main
from backend.tests.evaluation import test_route_cli as route_commands
from backend.tests.evaluation import test_v3_pair_report as pairs
from backend.tests.evaluation.test_daily_density import density_reviews

pytest_plugins = ("backend.tests.evaluation.test_intake",)
pair_case = pairs.pair_case
route_case = pairs.route_case
prepared_scenario = pairs.prepared_scenario


def test_paired_cli_density_policy_preserves_provenance_and_read_only_sources(pair_case, capsys):
    case = pair_case()
    root = case[2].parent
    path = root / "density.json"
    path.write_text(json.dumps(density_reviews(case[0], exact_count=1)), encoding="utf-8")
    args = ["report", *route_commands.arguments(case)[1:], "--density-reviews", str(path)]
    originals = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
    assert main(args) == 0
    out = json.loads(capsys.readouterr().out)
    assert (
        out["preparation_file_sha256"]["density_reviews"]
        == hashlib.sha256(path.read_bytes()).hexdigest()
    )
    pair = out["groups"][0]
    assert pair["stages"]["draft"]["daily_density"]["days"][0]["known_primary_count"] == 2
    assert pair["stages"]["draft"]["overall_total"]["score_0_100"] == 0
    assert pair["deltas"]["overall_total"]["percentage_points"] == 0
    assert {p: p.read_bytes() for p in root.rglob("*") if p.is_file()} == originals


def test_new_pair_report_can_be_linked_into_independent_mechanism_channel(pair_case, batch):
    case = pair_case()
    out = pairs.report(case, density_reviews=density_reviews(case[0]))
    prepared = case[0].to_dict()
    group = prepared["inventory"][0]
    context = group["runs"]["v3"]["final"]["context"]
    observation = {
        "group_id": group["group_id"],
        "run_id": context["run_id"],
        "version": "v3",
        "input_sha256": group["input_sha256"],
        "result_sha256": context["artifact_sha256"],
        "channel": "independent",
        "content": out,
        "content_sha256": canonical_digest(out),
    }
    mechanism = read_batch_sources(batch[4] / "manifest.json", observations=[observation]).to_dict()
    v3 = next(run for run in mechanism["runs"] if run["version"] == "v3")
    assert v3["channels"]["independent"]["status"] == "available"
