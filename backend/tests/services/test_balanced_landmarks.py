"""Integrated supply behavior with controlled external collaborators, not live quality."""

import pytest

from backend.tests.services.test_landmark_discovery import run_case


@pytest.mark.parametrize("destination", ["Harbour City", "Hill City", "River City"])
def test_preference_dense_pool_keeps_landmarks_and_replacement_options(destination):
    museums = [(f"poi-0-{i:02}", f"Museum {i}") for i in range(60)]
    landmarks = [(f"poi-9-{i}", f"Classic {i}") for i in range(3)]
    all_rows = museums + landmarks
    pools = {f"Interest {i} in {destination}": all_rows for i in range(3)}
    pools[f"top attractions in {destination}"] = all_rows
    matches = {name: (0, 1, 2) for _, name in all_rows}
    result, model, places = run_case(
        [name for _, name in landmarks],
        interests=3,
        pools=pools,
        supported_interests=matches,
        destination=destination,
    )
    selected = set(result.planning_supply.selected_place_ids)
    assert {pid for pid, _ in landmarks} <= selected
    assert len(selected - {pid for pid, _ in landmarks}) >= 2
    assert model.nominations == 1
    assert len(places.search_requests) <= 13
    assert all(pid in model.calls[-1].user_prompt for pid, _ in landmarks)


def test_saturated_preference_keeps_alternatives_without_monopolizing_fallback():
    museums = [(f"poi-0-{i:02}", f"Museum {i}") for i in range(30)]
    other = [(f"poi-9-{i}", f"Other {i}") for i in range(8)]
    result, _, _ = run_case(
        [],
        interests=1,
        pools={"Interest 0 in Sydney": museums, "top attractions in Sydney": other},
        supported_interests={name: (0,) for _, name in museums},
    )
    selected = set(result.planning_supply.selected_place_ids)
    assert len(selected & {pid for pid, _ in museums}) >= 2
    assert len(selected & {pid for pid, _ in other}) >= 4


def test_whole_trip_focus_saturates_and_retains_independent_landmarks():
    museums = [(f"poi-0-{i:02}", f"Museum {i}") for i in range(30)]
    classics = [(f"poi-9-{i}", f"Classic {i}") for i in range(8)]
    result, model, _ = run_case(
        [name for _, name in classics],
        interests=1,
        focus=True,
        pools={"Interest 0 in Sydney": museums, "top attractions in Sydney": classics},
        supported_interests={name: (0,) for _, name in museums},
        scheduled_id="poi-0-07",
    )
    selected = set(result.planning_supply.selected_place_ids)
    assert len(selected & {pid for pid, _ in museums}) >= 3
    assert len(selected & {pid for pid, _ in classics}) >= 4
    progress = result.generation_diagnostics.goal_progress[0]
    assert progress["expected"] == 2
    assert progress["matched"] == 1
    assert progress["remaining"] == 1
    assert model.nominations == 1


def test_closed_landmark_leaves_preference_replacements_and_never_enters_supply():
    rows = [(f"poi-0-{i}", f"Museum {i}") for i in range(8)]
    result, model, _ = run_case(
        ["Museum 0", "Museum 1", "Museum 2"],
        interests=2,
        pools={
            "top attractions in Sydney": rows,
            "Interest 0 in Sydney": rows,
            "Interest 1 in Sydney": rows,
        },
        supported_interests={name: (0, 1) for _, name in rows},
        closed=("poi-0-0",),
        scheduled_id="poi-0-1",
    )
    assert "poi-0-0" not in result.planning_supply.selected_place_ids
    assert {"poi-0-1", "poi-0-2"} <= set(result.planning_supply.selected_place_ids)
    assert result.itinerary.days[0].activities[0].source_place_id == "poi-0-1"
    assert model.nominations == 1


@pytest.mark.parametrize("days,focus", [(1, False), (6, True)])
def test_short_and_long_trips_keep_options_separate_from_scheduled_coverage(days, focus):
    museums = [(f"poi-0-{i}", f"Museum {i}") for i in range(8)]
    other = [(f"poi-9-{i}", f"Classic {i}") for i in range(8)]
    result, model, places = run_case(
        [name for _, name in other],
        interests=2,
        days=days,
        focus=focus,
        pools={
            "Interest 0 in Sydney": museums,
            "Interest 1 in Sydney": museums,
            "top attractions in Sydney": other,
        },
        supported_interests={name: (0, 1) for _, name in museums},
        scheduled_id="poi-0-7",
    )
    selected = set(result.planning_supply.selected_place_ids)
    assert len(selected & {pid for pid, _ in museums}) >= (3 if focus else 2)
    assert selected & {pid for pid, _ in other}
    progress = result.generation_diagnostics.goal_progress
    assert [p["matched"] for p in progress] == [1, 1]
    assert progress[0]["remaining"] == (1 if focus else 0)
    assert model.nominations == 1 and len(model.calls) == 2
    assert len(places.search_requests) <= 13
    assert len(places.details_requests) <= 60


def test_many_interests_on_one_day_report_real_gaps_without_extra_generation():
    rows = [(f"poi-0-{i}", f"Shared Museum {i}") for i in range(8)]
    pools = {f"Interest {i} in Sydney": rows for i in range(8)}
    pools["top attractions in Sydney"] = rows
    result, model, places = run_case(
        ["Shared Museum 7"],
        interests=8,
        days=1,
        pools=pools,
        supported_interests={name: (0, 1) for _, name in rows},
        scheduled_id="poi-0-7",
    )
    progress = result.generation_diagnostics.goal_progress
    assert [p["matched"] for p in progress] == [1, 1, 0, 0, 0, 0, 0, 0]
    assert [p["coverage_status"] for p in progress] == ["covered"] * 2 + ["gap"] * 6
    assert len(model.calls) == 2 and model.nominations == 1
    assert len(places.search_requests) <= 13


def test_multi_interest_query_cannot_keep_rewarding_only_its_saturated_match():
    museums = [(f"poi-0-{i:02}", f"Museum {i}") for i in range(30)]
    landmarks = [(f"poi-9-{i}", f"Classic {i}") for i in range(3)]
    result, _, _ = run_case(
        [name for _, name in landmarks],
        interests=2,
        focus=True,
        combined_intent=True,
        pools={"Interest 0 in Sydney": museums, "top attractions in Sydney": landmarks},
        supported_interests={name: (0,) for _, name in museums},
    )
    assert {pid for pid, _ in landmarks} <= set(result.planning_supply.selected_place_ids)
