"""Tests for shared itinerary and planning result schemas."""

from datetime import date, datetime

import pytest
from pydantic import ValidationError

from backend.app.schemas.itinerary import Activity, Itinerary, ItineraryDay
from backend.app.schemas.planning import PlanningResult, SystemVersion
from backend.app.schemas.request import TravelRequirements


def make_activity(activity_id: str = "activity-1") -> Activity:
    return Activity(
        activity_id=activity_id,
        title="Visit Fushimi Inari Shrine",
        place_name="Fushimi Inari Taisha",
        location="Kyoto, Japan",
        start_time=datetime.fromisoformat("2026-10-01T09:00:00+09:00"),
        end_time=datetime.fromisoformat("2026-10-01T11:00:00+09:00"),
    )


def make_itinerary() -> Itinerary:
    return Itinerary(
        destination="Kyoto",
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 1),
        days=[ItineraryDay(date=date(2026, 10, 1), activities=[make_activity()])],
    )


def test_planning_result_has_only_shared_output_fields() -> None:
    result = PlanningResult(
        system_version=SystemVersion.V0,
        requirements=TravelRequirements(
            destination="Kyoto",
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 1),
            traveler_count=1,
        ),
        itinerary=make_itinerary(),
    )

    assert set(result.model_dump(mode="json")) == {
        "generation_diagnostics",
        "system_version",
        "requirements",
        "itinerary",
    }


def test_planning_result_rejects_version_specific_fields() -> None:
    with pytest.raises(ValidationError):
        PlanningResult(
            system_version=SystemVersion.V1,
            requirements=TravelRequirements(destination="Kyoto"),
            itinerary=make_itinerary(),
            evidence=[],
        )


def test_activity_rejects_non_positive_duration() -> None:
    with pytest.raises(ValidationError, match="end_time must be after start_time"):
        Activity(
            activity_id="activity-1",
            title="Invalid activity",
            start_time=datetime.fromisoformat("2026-10-01T11:00:00+09:00"),
            end_time=datetime.fromisoformat("2026-10-01T11:00:00+09:00"),
        )


def test_itinerary_rejects_duplicate_activity_ids() -> None:
    with pytest.raises(ValidationError, match="activity_id values must be unique"):
        Itinerary(
            destination="Kyoto",
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 1),
            days=[
                ItineraryDay(
                    date=date(2026, 10, 1),
                    activities=[make_activity(), make_activity()],
                )
            ],
        )
