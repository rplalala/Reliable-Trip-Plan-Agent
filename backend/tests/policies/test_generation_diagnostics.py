"""Read-only role-aware coverage observations, including historical uncertainty."""

from datetime import date, datetime, timedelta
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from backend.app.llm.azure_foundry.dto import FoundryActivityDTO
from backend.app.policies.generation_diagnostics import observe_generation
from backend.app.policies.generation_policy import FIRST_GENERATION_POLICY
from backend.app.schemas.itinerary import Activity, Itinerary

START = date(2026, 9, 21)


def activity(index, kind="main_poi", pid="a", name="Museum", day=START):
    return Activity(
        activity_id=str(index), activity_kind=kind, title="Declared activity",
        source_place_id=pid, place_name=name,
        start_time=datetime.fromisoformat(f"{day}T10:00:00+01:00"),
        end_time=datetime.fromisoformat(f"{day}T11:00:00+01:00"),
    )


def observe(activities, *, supply=("a", "b", "c"), reference=START-timedelta(days=1)):
    itinerary = Itinerary(
        destination="Fixture city", start_date=START, end_date=START+timedelta(days=2),
        days=[{"date": START, "activities": activities}],
        reference_recommendations=[{"place_name": "Cafe", "reason": "Optional"}],
    )
    before = itinerary.model_dump_json()
    result = observe_generation(
        itinerary, SimpleNamespace(start_date=itinerary.start_date, end_date=itinerary.end_date),
        reference_date=reference, supplied_ids=supply,
    )
    assert itinerary.model_dump_json() == before
    return result


def test_roles_duplicates_missing_dates_and_references_do_not_inflate_counts():
    result = observe([
        activity(1), activity(2), activity(3, pid="b"),
        activity(4, "transport"), activity(5, "free_time"), activity(6, "generic_activity"),
    ])
    row = result.days[0]
    assert (row.main_activity_count, row.distinct_main_poi_count, row.repeated_main_poi_count) == (
        3, 2, 1,
    )
    assert row.target_status == "within_target"
    assert (row.transport_activity_count, row.free_time_activity_count,
            row.generic_activity_count) == (1, 1, 1)
    assert result.empty_days == result.days_with_zero_main_pois == 2
    assert not result.days[1].day_present
    assert result.days_below_target == 2
    assert (result.scheduled_unique_supply, result.unused_supply) == (2, 1)


@pytest.mark.parametrize("role,pid", [("unknown", "a"), ("main_poi", None),
                                     ("main_poi", "outside")])
def test_unknown_or_unlinked_main_is_not_claimed_verified(role, pid):
    row = observe([activity(1, role, pid)]).days[0]
    assert row.target_status == "not_assessable"
    assert row.unclassified_activity_count == 1
    assert row.distinct_main_poi_count == 0


def test_v0_name_proxy_normalizes_only_unicode_whitespace_case():
    result = observe([
        activity(1, pid=None, name="Ｍuseum  A"),
        activity(2, pid=None, name="museum\tA"),
        activity(3, pid=None, name="Museum A annex"),
    ], supply=None)
    row = result.days[0]
    assert row.count_basis == "name_proxy"
    assert row.distinct_main_poi_count == 2 and row.repeated_main_poi_count == 1
    assert result.scheduled_unique_supply is None and result.unused_supply is None


def test_same_day_does_not_claim_remaining_hours_supported():
    row = observe([activity(1)], reference=START).days[0]
    assert row.applicability == "same_day_remaining_hours_unsupported"
    assert row.target_status == "not_assessable"


def test_above_target_is_observation_not_schema_failure():
    result = observe([activity(i, pid=str(i)) for i in range(6)], supply=tuple(map(str, range(6))))
    assert result.days_above_target == 1


def test_cross_day_repeated_visits_remain_unmodified():
    end = START + timedelta(days=1)
    itinerary = Itinerary(destination="Fixture", start_date=START, end_date=end, days=[
        {"date": START, "activities": [activity(1)]},
        {"date": end, "activities": [activity(2, day=end)]},
    ])
    result = observe_generation(itinerary, itinerary, reference_date=START-timedelta(days=1),
                                supplied_ids=("a",))
    assert result.cross_day_repeated_visits == 1
    assert result.scheduled_unique_supply == 1
    assert len(itinerary.days[1].activities) == 1


def test_historical_missing_role_is_unknown_but_new_dto_requires_role():
    raw = activity(1).model_dump()
    del raw["activity_kind"]
    assert Activity.model_validate(raw).activity_kind == "unknown"
    assert "activity_kind" in FoundryActivityDTO.model_json_schema()["required"]
    with pytest.raises(ValidationError):
        Activity.model_validate({**raw, "activity_kind": "inferred_from_keyword"})


def test_generation_policy_is_shared_without_repair_instructions():
    from backend.app.versions.v0.prompts import ITINERARY_GENERATION_SYSTEM_PROMPT as v0
    from backend.app.versions.v1.prompts import ITINERARY_GENERATION_SYSTEM_PROMPT as v1

    assert FIRST_GENERATION_POLICY in v0 and FIRST_GENERATION_POLICY in v1
    assert "not an unconditional" in FIRST_GENERATION_POLICY
