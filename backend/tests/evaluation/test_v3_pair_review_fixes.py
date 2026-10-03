"""Public regressions for independently reviewed structural loss attribution."""

import copy

import pytest

from backend.evaluation.v3_correspondence import read_v3_result_sources
from backend.tests.evaluation import test_v3_pair_report as pairs

pytest_plugins = ("backend.tests.evaluation.test_intake",)
pair_case = pairs.pair_case
route_case = pairs.route_case
prepared_scenario = pairs.prepared_scenario


@pytest.mark.parametrize("relation", ["removed", "added"])
def test_review_counts_each_confirmed_primary_occurrence(pair_case, relation):
    def before(itinerary):
        duplicate = copy.deepcopy(itinerary["days"][0]["activities"][0])
        duplicate["activity_id"] = "a2"
        itinerary["days"][0]["activities"].append(duplicate)

    def after(itinerary):
        itinerary["days"][0]["activities"] = [
            a for a in itinerary["days"][0]["activities"] if a["activity_id"] == "b"
        ]
        itinerary["transfers"] = []

    def change(results):
        pairs.no_departure(results)
        full = copy.deepcopy(results["v3"]["itinerary"])
        before(full)
        reduced = copy.deepcopy(full)
        after(reduced)
        draft, final = (full, reduced) if relation == "removed" else (reduced, full)
        results["v3"]["v3"] = {"draft": draft, "final_primary": final}

    case = pair_case(source_change=change)
    review = pairs.correspondence_review(case, relation)
    run = case[0].to_dict()["inventory"][0]["runs"]["v3"]
    for side, stage in (("before", "draft"), ("after", "final_primary")):
        review["records"][0][side] = [
            a["source"]
            for a in run["optional"][stage]["activities"]
            if a["original"]["activity_id"] != "b"
        ]
    review["records"][0]["rationale"] = "Original editing evidence confirms two visit changes."
    out = pairs.report(case, correspondence_reviews=review)
    assert out["status"] == "complete", out["diagnostics"]
    assert out["groups"][0]["visit_changes"][relation + "_count"] == 2


@pytest.mark.parametrize("operation", ["delete", "add"])
def test_transport_protection_attribution_uses_confirmed_endpoint_changes(
    pair_case, batch, operation
):
    def before(itinerary):
        if operation == "delete":
            itinerary["transfers"][0].update(
                departure_time="2020-01-01T10:00:00Z", arrival_time="2020-01-01T10:30:00Z"
            )
        else:
            itinerary["days"][0]["activities"].pop(0)
            itinerary["transfers"] = []

    def after(itinerary):
        if operation == "delete":
            itinerary["days"][0]["activities"].pop(0)
            itinerary["transfers"] = []
        else:
            visit = copy.deepcopy(itinerary["days"][0]["activities"][0])
            visit.update(
                activity_id="repair_r1_1",
                title="Museum A",
                place_name="Museum A",
                source_place_id="canonical-Museum A",
                start_time="2020-01-01T09:00:00Z",
                end_time="2020-01-01T10:00:00Z",
            )
            itinerary["days"][0]["activities"].insert(0, visit)
            itinerary["transfers"] = [
                {
                    "from_activity_id": "repair_r1_1",
                    "to_activity_id": "b",
                    "mode": "WALK",
                    "departure_time": "2020-01-01T10:00:00Z",
                    "arrival_time": "2020-01-01T10:30:00Z",
                }
            ]

    proposal = (
        pairs.edit("delete")
        if operation == "delete"
        else pairs.edit(
            "add",
            None,
            place_id="canonical-Museum A",
            start_time="2020-01-01T09:00:00Z",
            end_time="2020-01-01T10:00:00Z",
        )
    )
    case = pair_case(
        before=before,
        after=after,
        edits=[proposal],
        obligations=[pairs.protection("10:10", "10:20")],
    )
    out = pairs.report(
        case, result_sources=read_v3_result_sources(case[0], batch[4] / "manifest.json")
    )
    assert out["status"] == "complete", out["diagnostics"]
    pair = out["groups"][0]
    stage = "draft" if operation == "delete" else "final_primary"
    ids = {
        u["commitment_id"]
        for u in pair["stages"][stage]["occupancy"]["commitments"]
        if u["kind"] == "transport"
    }
    conflicts = [
        c
        for c in pair["continuity"]["protection_conflicts"]
        if c["before" if operation == "delete" else "after"]
        and c["before" if operation == "delete" else "after"]["commitment_id"] in ids
    ]
    assert len(conflicts) == 1
    assert conflicts[0]["transition"] == (
        "removed_participant" if operation == "delete" else "introduced_conflict"
    )


@pytest.mark.parametrize("venue_change", [False, True])
def test_complex_visit_sets_do_not_prove_new_transport_participants(pair_case, venue_change):
    def before(itinerary):
        duplicate = copy.deepcopy(itinerary["days"][0]["activities"][0])
        duplicate["activity_id"] = "a2"
        itinerary["days"][0]["activities"].insert(1, duplicate)
        itinerary["transfers"][0].update(
            from_activity_id="a2",
            departure_time="2020-01-01T10:00:00Z",
            arrival_time="2020-01-01T10:05:00Z",
        )

    def after(itinerary):
        for activity in itinerary["days"][0]["activities"]:
            if activity["activity_id"] != "b":
                activity.update(start_time="2020-01-01T08:00:00Z", end_time="2020-01-01T09:00:00Z")
        if venue_change:
            itinerary["days"][0]["activities"][1].update(
                title="Gallery C", place_name="Gallery C", source_place_id="canonical-Gallery C"
            )
        itinerary["transfers"][0].update(
            departure_time="2020-01-01T10:00:00Z",
            arrival_time="2020-01-01T10:30:00Z",
        )

    case = pair_case(before=before, after=after, obligations=[pairs.protection("10:10", "10:20")])
    review = pairs.correspondence_review(case, "complex")
    run = case[0].to_dict()["inventory"][0]["runs"]["v3"]
    for side, stage in (("before", "draft"), ("after", "final_primary")):
        review["records"][0][side] = [
            a["source"]
            for a in run["optional"][stage]["activities"]
            if a["original"]["activity_id"] != "b"
        ]
    out = pairs.report(case, correspondence_reviews=review)
    assert out["status"] == "complete", out["diagnostics"]
    continuity = out["groups"][0]["continuity"]
    assert continuity["protection_conflicts"][0]["transition"] == "unresolved_attribution"
    assert all(row["transition"] == "unresolved_correspondence" for row in continuity["routes"])
    assert out["groups"][0]["visit_changes"]["confirmed_venue_loss_count"] == 0
