"""Known V0 transport occupancy does not require canonical POI endpoints."""

import pytest

from backend.evaluation.requirement_schedule import score_requirement_schedule

pytest_plugins = (
    "backend.tests.evaluation.test_intake",
    "backend.tests.evaluation.test_requirement_schedule",
)


def test_timed_v0_transport_to_generic_endpoint_is_a_commitment(scenario):
    def change(results):
        activities = results["v0"]["itinerary"]["days"][0]["activities"]
        activities[1]["transport"] = {
            "mode": "WALK",
            "from_activity_id": "a",
            "to_activity_id": "b",
        }
        activities[2].update(activity_kind="free_time", title="Lunch", place_name=None)

    intake, identity, _ = scenario(change=change)
    projection = intake.to_dict()["inventory"][0]["runs"]["v0"]["final"]
    assert len(projection["unbound_transport"]) == 1
    report = score_requirement_schedule(intake, identity).to_dict()
    v0 = next(r for r in report["results"] if r["version"] == "v0")
    assert v0["non_overlap"]["state"] == "PASS"
    assert v0["non_overlap"]["denominator"] == 2
    assert not v0["occupancy"]["denominator_unresolved"]
    assert {u["kind"] for u in v0["occupancy"]["commitments"]} == {"primary_visit", "transport"}


@pytest.mark.parametrize("fault", ["invalid_time", "overlap"])
def test_unbound_v0_occupancy_keeps_time_unknown_and_proven_conflict(scenario, fault):
    def change(results):
        activities = results["v0"]["itinerary"]["days"][0]["activities"]
        activities[2].update(activity_kind="free_time", title="Lunch", place_name=None)
        activities[1]["transport"] = {
            "mode": "WALK",
            "from_activity_id": "a",
            "to_activity_id": "b",
        }
        if fault == "invalid_time":
            activities[1]["end_time"] = "invalid"
        else:
            activities[1]["start_time"] = "2020-01-01T09:30:00+00:00"

    intake, identity, _ = scenario(change=change)
    report = score_requirement_schedule(intake, identity).to_dict()
    v0 = next(r for r in report["results"] if r["version"] == "v0")
    assert v0["non_overlap"]["denominator"] == 2
    assert v0["non_overlap"]["state"] == ("UNKNOWN" if fault == "invalid_time" else "FAIL")
