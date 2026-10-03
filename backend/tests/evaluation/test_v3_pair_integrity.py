"""Replay integrity, uncertainty and CLI regression at public paired boundaries."""

import copy
import json

from backend.evaluation.v3_correspondence import prepare_v3_correspondence, read_v3_result_sources
from backend.tests.evaluation import test_v3_pair_report as pair_tests

pytest_plugins = ("backend.tests.evaluation.test_intake",)
pair_case = pair_tests.pair_case
route_case = pair_tests.route_case
prepared_scenario = pair_tests.prepared_scenario


def test_cli_prepares_sources_and_replays_report_deterministically(pair_case, batch, capsys):
    from backend.evaluation.v3_pair_cli import main

    case = pair_case()
    root = batch[4]
    for name, value in (
        ("identity", case[1].to_dict()),
        ("context", case[3]),
        ("routes", case[4]),
        ("coordinates", case[5]),
    ):
        (root / (name + ".json")).write_text(json.dumps(value), encoding="utf-8")
    assert main(["prepare", str(root / "manifest.json"), str(root / "identity.json")]) == 0
    provenance = json.loads(capsys.readouterr().out)
    (root / "edit-provenance.json").write_text(json.dumps(provenance), encoding="utf-8")
    args = [
        "report",
        str(root / "manifest.json"),
        str(root / "identity.json"),
        str(case[2]),
        "--context",
        str(root / "context.json"),
        "--route-reviews",
        str(root / "routes.json"),
        "--coordinates",
        str(root / "coordinates.json"),
        "--edit-provenance",
        str(root / "edit-provenance.json"),
        "--generated-at",
        pair_tests.STAMP,
    ]
    assert main(args) == 0
    first = json.loads(capsys.readouterr().out)
    assert first["groups"][0]["pair_status"] == "available"
    assert first["preparation_file_sha256"]["edit_provenance"]
    assert main(args) == 0
    assert json.loads(capsys.readouterr().out) == first


def test_output_normalization_keeps_adopted_lineage_with_source_basis(pair_case, batch):
    def before(itinerary):
        itinerary["days"][0]["activities"][0]["source_place_id"] = "canonical-Museum A"

    def after(itinerary):
        itinerary["days"][0]["activities"][0]["place_name"] = "Museum A normalized"
        itinerary["days"][0]["activities"].reverse()
        itinerary["transfers"] = []

    def repair_change(repair):
        repair["status"] = "SKIPPED"
        repair["final"] = copy.deepcopy(repair["original"])
        repair["rounds"] = []

    case = pair_case(before=before, after=after, edits=[], repair_change=repair_change)
    # Normalization is backed by the producer's own selected output ledger, not venue truth.
    result = batch[1]["v3"]
    result["v3"]["final_places"] = [
        {"place_id": "canonical-Museum A", "name": "Museum A normalized"}
    ]

    # Rebuild through the fixture before accepting hashes/identity/snapshot.
    def change(results):
        original = copy.deepcopy(result)
        results["v3"] = original

    case = pair_case(source_change=change)
    sources = read_v3_result_sources(case[0], batch[4] / "manifest.json")
    row = prepare_v3_correspondence(case[0], case[1], sources).to_dict()["groups"][0]
    assert row["diagnostics"] == []
    assert row["unresolved"] == {"before": [], "after": []}
    assert "place_name_normalization" in [item["kind"] for item in row["normalizations"]]
    assert "transfer_refresh" in [item["kind"] for item in row["normalizations"]]
    assert all(r["basis"] == "validated_adopted_lineage" for r in row["relations"])


def test_removed_population_retains_subtotal_availability_and_exact_measurement_changes(
    pair_case, batch
):
    def after(itinerary):
        itinerary["days"][0]["activities"] = itinerary["days"][0]["activities"][1:]
        itinerary["transfers"] = []

    case = pair_case(after=after, edits=[pair_tests.edit("delete")])
    pair = pair_tests.report(
        case, result_sources=read_v3_result_sources(case[0], batch[4] / "manifest.json")
    )["groups"][0]
    assert pair["deltas"]["population"]["primary_visit_count"] == -1
    burden = pair["deltas"]["route_observed_burden"]
    assert burden["duration_nanoseconds"]["before"] == 1800000000000
    assert burden["duration_nanoseconds"]["after"] is None
    assert burden["duration_nanoseconds"]["delta"] is None
    assert burden["observed_leg_count"]["delta"] == -1
    assert (
        pair["stages"]["final_primary"]["primary_metrics"]["routes"]["observed_transfer_burden"][
            "full_scope_complete"
        ]
        is False
    )
