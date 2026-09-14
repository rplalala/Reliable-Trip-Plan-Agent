"""Date-scoped Places hours must not leak a seven-day view into later trip dates."""

import json
from datetime import UTC, date, datetime

from backend.app.evidence.models import (
    EvidenceAvailability,
    PlaceCandidate,
    RouteEvidence,
    RouteEvidenceBundle,
    WeatherEvidence,
)
from backend.app.evidence.normalization import normalize_place_details
from backend.app.evidence.opening_hours import opening_hours_for_date, planning_opening_hours
from backend.app.integrations.models import LatLng, PlaceDetailsDTO
from backend.app.schemas.request import TravelRequest, TravelRequirements
from backend.app.versions.v1.prompts import build_itinerary_generation_prompt


def _place(
    place_id: str = "museum",
    *,
    current: dict[str, object] | None = None,
    regular: dict[str, object] | None = None,
    time_zone: str | None = "Australia/Sydney",
    requested_at: str | None = None,
):
    candidate = PlaceCandidate(
        place_id=place_id,
        name=place_id,
        latitude=-33.8,
        longitude=151.2,
        source_query="museums in Sydney",
        category="museums",
        provider_rank=0,
    )
    details = PlaceDetailsDTO(
        place_id=place_id,
        display_name=place_id,
        location=LatLng(latitude=-33.8, longitude=151.2),
        time_zone=time_zone,
        current_opening_hours=current,
        regular_opening_hours=regular,
        requested_at=requested_at,
        retrieved_at="2026-09-14T01:00:00+00:00",
    )
    return normalize_place_details(details, candidate=candidate)


CURRENT = {
    "weekdayDescriptions": [
        "Monday: 10:00 AM – 5:00 PM",
        "Tuesday: Closed",
        "Wednesday: 10:00 AM – 5:00 PM",
    ],
    "periods": [
        {
            "open": {"date": {"year": 2026, "month": 9, "day": 14}},
            "close": {"date": {"year": 2026, "month": 9, "day": 14}},
        }
    ],
    "specialDays": [{"date": {"year": 2026, "month": 9, "day": 15}}],
}
REGULAR = {
    "weekdayDescriptions": [
        "Monday: 9:00 AM – 6:00 PM",
        "Tuesday: 9:00 AM – 6:00 PM",
        "Wednesday: Closed",
    ]
}


def test_current_date_window_overrides_regular_but_not_after_day_seven() -> None:
    place = _place(current=CURRENT, regular=REGULAR)
    assert place.current_opening_hours is not None
    assert place.regular_opening_hours is not None
    assert place.current_opening_hours.applicability == "provider_current_window"
    assert place.current_opening_hours.valid_from == date(2026, 9, 14)
    assert place.current_opening_hours.valid_through == date(2026, 9, 20)
    assert place.current_opening_hours.source_dated_days == [
        date(2026, 9, 14),
        date(2026, 9, 15),
    ]
    assert place.regular_opening_hours.applicability == "regular_weekly_pattern"

    inside = opening_hours_for_date(place, date(2026, 9, 15))
    assert inside.basis == "current_date_window"
    assert inside.weekday_description == "Tuesday: Closed"
    assert inside.source_window_start == date(2026, 9, 14)
    assert inside.source_window_end == date(2026, 9, 20)

    for day in (date(2026, 9, 21), date(2026, 9, 22), date(2026, 9, 23)):
        later = opening_hours_for_date(place, day)
        assert later.basis == "regular_weekly_baseline"
        assert later.source_window_start is None
        assert later.source_window_end is None
    assert opening_hours_for_date(place, date(2026, 9, 22)).weekday_description == (
        "Tuesday: 9:00 AM – 6:00 PM"
    )
    regular_closure = opening_hours_for_date(place, date(2026, 9, 23))
    assert regular_closure.weekday_description == "Wednesday: Closed"


def test_missing_sources_and_missing_timezone_keep_uncertainty_explicit() -> None:
    regular_only = _place(current=None, regular=REGULAR)
    assert opening_hours_for_date(regular_only, date(2026, 9, 15)).basis == (
        "regular_weekly_baseline"
    )

    current_only = _place(current=CURRENT, regular=None)
    assert opening_hours_for_date(current_only, date(2026, 9, 15)).basis == ("current_date_window")
    assert opening_hours_for_date(current_only, date(2026, 9, 22)).basis == "unknown"

    neither = _place(current=None, regular=None)
    assert opening_hours_for_date(neither, date(2026, 9, 15)).basis == "unknown"

    no_local_window = _place(current=CURRENT, regular=REGULAR, time_zone=None)
    assert no_local_window.current_opening_hours is not None
    assert no_local_window.current_opening_hours.valid_from is None
    assert opening_hours_for_date(no_local_window, date(2026, 9, 15)).basis == (
        "regular_weekly_baseline"
    )


def test_current_window_uses_request_date_when_response_crosses_local_midnight() -> None:
    place = _place(
        current=CURRENT,
        regular=REGULAR,
        requested_at="2026-09-13T13:59:00+00:00",
    )
    assert place.current_opening_hours is not None
    assert place.current_opening_hours.valid_from == date(2026, 9, 13)
    assert place.current_opening_hours.valid_through == date(2026, 9, 19)
    assert opening_hours_for_date(place, date(2026, 9, 20)).basis != "current_date_window"


def test_planner_prompt_attaches_date_view_to_correct_place_id() -> None:
    museum = _place("museum", current=CURRENT, regular=REGULAR)
    beach = _place("beach", current=None, regular=None)
    requirements = TravelRequirements(
        destination="Sydney",
        start_date=date(2026, 9, 22),
        end_date=date(2026, 9, 23),
    )
    prompt = build_itinerary_generation_prompt(
        TravelRequest(request_text="Plan two days in Sydney"),
        requirements,
        date(2026, 9, 14),
        places=[museum, beach],
        weather=WeatherEvidence(
            destination="Sydney",
            latitude=-33.8,
            longitude=151.2,
            availability=EvidenceAvailability.UNAVAILABLE,
            retrieved_at=datetime(2026, 9, 14, tzinfo=UTC),
            source_ref="google_weather",
        ),
        routes=RouteEvidenceBundle(
            baseline=RouteEvidence(
                travel_mode="WALK",
                mode_reason="test",
                availability=EvidenceAvailability.UNAVAILABLE,
                retrieved_at=datetime(2026, 9, 14, tzinfo=UTC),
                source_ref="google_routes",
            )
        ),
    )
    payload = prompt.split("<external_evidence>\n", 1)[1].split("\n</external_evidence>", 1)[0]
    places = {item["place_id"]: item for item in json.loads(payload)["places"]}
    assert "opening_hours" not in places["museum"]
    assert "current_opening_hours" not in places["museum"]
    assert "regular_opening_hours" not in places["museum"]
    assert [item["basis"] for item in places["museum"]["opening_hours_by_date"]] == [
        "regular_weekly_baseline",
        "regular_weekly_baseline",
    ]
    assert places["museum"]["opening_hours_by_date"][0]["weekday_description"] == (
        "Tuesday: 9:00 AM – 6:00 PM"
    )
    assert [item["basis"] for item in places["beach"]["opening_hours_by_date"]] == [
        "unknown",
        "unknown",
    ]
    days = planning_opening_hours(museum, date(2026, 9, 22), date(2026, 9, 23))
    assert [item.date for item in days] == [
        date(2026, 9, 22),
        date(2026, 9, 23),
    ]
