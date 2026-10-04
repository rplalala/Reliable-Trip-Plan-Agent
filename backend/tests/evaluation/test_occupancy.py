"""Source-selected commitments and protected blockers at the preparation interface."""

import copy

import pytest

from backend.evaluation.intake import load_batch
from backend.evaluation.occupancy import assess_occupancy, prepare_occupancy
from backend.tests.evaluation.test_intake import activity, transfer

pytest_plugins = ("backend.tests.evaluation.test_intake",)


def test_non_poi_free_time_retains_independently_reviewed_commitment(batch):
    _, results, write, _, _ = batch
    rest = activity("rest", "Coffee break", "10:00", "10:20", "free_time", place="Hotel Lounge")
    results["v1"]["itinerary"]["days"][0]["activities"].append(rest)
    projection = load_batch(write("v1")).to_dict()["inventory"][0]["runs"]["v1"]["final"]
    item = projection["activities"][-1]
    assert item["evaluation_role"] == "transition"
    unreviewed = prepare_occupancy(projection, [], timezone="Etc/UTC").to_dict()
    assert any(c["sources"] == [item["source"]] for c in unreviewed["candidates"])
    reviewed = prepare_occupancy(
        projection,
        [],
        timezone="Etc/UTC",
        reviews=[{"source": item["source"], "occupancy": "committed"}],
    ).to_dict()
    rest_unit = next(c for c in reviewed["commitments"] if c["kind"] == "fixed_generic")
    assert rest_unit["sources"] == [item["source"]]
    assert rest_unit["intervals"][0]["seconds"] == 1200


def test_overlapping_protections_union_without_adding_commitments(batch):
    _, _, write, _, _ = batch
    projection = load_batch(write()).to_dict()["inventory"][0]["runs"]["v0"]["final"]
    protections = [
        {
            "obligation_id": "p1",
            "kind": "protected_time",
            "resolution": "resolved",
            "date": "2020-01-01",
            "scope": "scheduled_commitments",
            "interval": {"kind": "clock", "start": "09:30", "end": "09:45"},
        },
        {
            "obligation_id": "p2",
            "kind": "protected_time",
            "resolution": "resolved",
            "date": "2020-01-01",
            "scope": "scheduled_commitments",
            "interval": {"kind": "clock", "start": "09:40", "end": "10:00"},
        },
    ]
    result = prepare_occupancy(projection, protections, timezone="Etc/UTC").to_dict()
    assert len(result["commitments"]) == 3
    assert len(result["blockers"]) == 1
    assert result["blockers"][0]["obligation_ids"] == ["p1", "p2"]
    assert result["blockers"][0]["interval"]["seconds"] == 1800
    assert result["denominator_unresolved"] is False


@pytest.mark.parametrize("version", ["v0", "v1", "v2", "v3"])
def test_transport_source_selection_has_no_fallback(batch, version):
    _, results, write, _, _ = batch
    results[version]["itinerary"]["transfers"] = [transfer("10:05", "10:25", mode=None)]
    projection = load_batch(write(version)).to_dict()["inventory"][0]["runs"][version]["final"]
    prepared = prepare_occupancy(projection, [])
    journey = next(unit for unit in prepared.commitments if unit.kind == "transport")
    assert journey.complete
    assert journey.guaranteed[0].seconds == 1200
    assert len(prepared.commitments) == 3
    assert journey.sources[0]["pointer"].endswith(
        "activities/1" if version == "v0" else "transfers/0"
    )


def test_v0_segments_and_duplicates_keep_one_journey_and_do_not_fill_gaps(batch):
    _, results, write, _, _ = batch
    activities = results["v0"]["itinerary"]["days"][0]["activities"]
    activities[1]["end_time"] = "2020-01-01T10:05:00+00:00"
    activities.append(activity("t2", "Walking", "10:15", "10:20", "transport"))
    duplicate = copy.deepcopy(activities[1])
    duplicate["activity_id"] = "t3"
    activities.append(duplicate)
    projection = load_batch(write("v0")).to_dict()["inventory"][0]["runs"]["v0"]["final"]
    prepared = prepare_occupancy(projection, [])
    journey = next(unit for unit in prepared.commitments if unit.kind == "transport")
    assert len(journey.guaranteed) == 2
    assert sum(span.seconds for span in journey.guaranteed) == 600
    assert len(journey.sources) == 3
    assert len(prepared.commitments) == 3


def test_transfer_alternatives_are_not_simultaneous_and_missing_claim_stays_unknown(batch):
    _, results, write, _, _ = batch
    results["v1"]["itinerary"]["transfers"] = [transfer(), transfer("09:45", "10:05")]
    projection = load_batch(write("v1")).to_dict()["inventory"][0]["runs"]["v1"]["final"]
    prepared = prepare_occupancy(projection, [])
    checks, _, _ = assess_occupancy(prepared)
    assert len(prepared.commitments) == 3
    assert [item["state"] for item in checks] == ["UNKNOWN", "PASS", "UNKNOWN"]
    results["v1"]["itinerary"]["transfers"] = [transfer(end=None)]
    projection = load_batch(write("v1")).to_dict()["inventory"][0]["runs"]["v1"]["final"]
    prepared = prepare_occupancy(projection, [])
    checks, _, _ = assess_occupancy(prepared)
    assert len(prepared.commitments) == 3
    assert all(item["state"] == "UNKNOWN" for item in checks)


def test_unbound_claim_preserves_denominator_uncertainty_and_no_claim_adds_no_unit(batch):
    _, results, write, _, _ = batch
    results["v1"]["itinerary"]["transfers"] = [{**transfer(), "from_activity_id": "missing"}]
    projection = load_batch(write("v1")).to_dict()["inventory"][0]["runs"]["v1"]["final"]
    prepared = prepare_occupancy(projection, [])
    assert len(prepared.commitments) == 2
    assert prepared.to_dict()["denominator_unresolved"] is True
    assert len(prepared.candidates) == 1
    results["v1"]["itinerary"]["transfers"] = []
    projection = load_batch(write("v1")).to_dict()["inventory"][0]["runs"]["v1"]["final"]
    prepared = prepare_occupancy(projection, [])
    assert len(prepared.commitments) == 2
    assert prepared.to_dict()["transport_coverage"][0]["claims_present"] is False


def test_all_journey_alternatives_proving_conflict_can_fail_with_only_common_lower_bound(batch):
    _, results, write, _, _ = batch
    results["v1"]["itinerary"]["transfers"] = [
        transfer("09:20", "09:40"),
        transfer("09:45", "10:05"),
    ]
    projection = load_batch(write("v1")).to_dict()["inventory"][0]["runs"]["v1"]["final"]
    checks, _, measures = assess_occupancy(prepare_occupancy(projection, []))
    assert [item["state"] for item in checks] == ["FAIL", "PASS", "FAIL"]
    assert len(measures["commitment_pairs"]) == 1
    assert measures["commitment_conflict"]["status"] == "lower_bound"
    assert measures["commitment_conflict"]["seconds"] is None


def test_unbound_claim_explicit_disjoint_time_does_not_make_known_visits_unknown(batch):
    _, results, write, _, _ = batch
    results["v1"]["itinerary"]["transfers"] = [
        {**transfer("15:00", "16:00"), "from_activity_id": "missing"}
    ]
    projection = load_batch(write("v1")).to_dict()["inventory"][0]["runs"]["v1"]["final"]
    prepared = prepare_occupancy(projection, [])
    checks, _, _ = assess_occupancy(prepared)
    assert [item["state"] for item in checks] == ["PASS", "PASS"]
    assert prepared.to_dict()["denominator_unresolved"] is True
    assert prepared.to_dict()["candidates"][0]["interval"]["seconds"] == 3600
