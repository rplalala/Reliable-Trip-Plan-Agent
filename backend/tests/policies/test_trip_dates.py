"""Tests for the shared project-wide trip-date policy."""

from datetime import UTC, date, datetime

import pytest

from backend.app.policies.trip_dates import (
    SystemDateProvider,
    TripDateErrorCode,
    TripDatePolicyError,
    create_trip_date_window,
    validate_itinerary_dates,
    validate_requested_trip_dates,
)
from backend.app.runtime.settings import RuntimeSettings
from backend.app.schemas.itinerary import Activity, Itinerary, ItineraryDay
from backend.app.schemas.request import TravelRequirements

REFERENCE_DATE = date(2026, 9, 11)


def test_system_date_provider_uses_explicit_iana_time_zone() -> None:
    observed_zones: list[str] = []

    def fixed_now(time_zone):
        observed_zones.append(time_zone.key)
        return datetime(2026, 9, 11, 14, 30, tzinfo=UTC).astimezone(time_zone)

    provider = SystemDateProvider("Australia/Sydney", now=fixed_now)

    assert provider.today() == date(2026, 9, 12)
    assert observed_zones == ["Australia/Sydney"]


def test_runtime_settings_ignore_env_time_zone_override(monkeypatch) -> None:
    monkeypatch.setenv("APP_TIME_ZONE", "Pacific/Auckland")

    settings = RuntimeSettings(_env_file=None)

    assert settings.app_time_zone == "Australia/Sydney"


def make_itinerary(
    *,
    start_date: date = date(2026, 9, 12),
    end_date: date = date(2026, 9, 13),
    day_date: date = date(2026, 9, 12),
    activity_start: str = "2026-09-12T09:00:00+10:00",
    activity_end: str = "2026-09-12T11:00:00+10:00",
) -> Itinerary:
    return Itinerary(
        destination="Sydney",
        start_date=start_date,
        end_date=end_date,
        days=[
            ItineraryDay(
                date=day_date,
                activities=[
                    Activity(
                        activity_id="activity-1",
                        title="Visit a museum",
                        start_time=datetime.fromisoformat(activity_start),
                        end_time=datetime.fromisoformat(activity_end),
                    )
                ],
            )
        ],
    )


def test_window_includes_reference_date_through_reference_date_plus_nine() -> None:
    window = create_trip_date_window(REFERENCE_DATE)

    assert window.allowed_start == date(2026, 9, 11)
    assert window.allowed_end == date(2026, 9, 20)


@pytest.mark.parametrize(
    ("start_date", "end_date"),
    [
        (date(2026, 9, 11), date(2026, 9, 11)),
        (date(2026, 9, 20), date(2026, 9, 20)),
        (date(2026, 9, 12), date(2026, 9, 14)),
    ],
)
def test_requested_dates_accept_every_valid_boundary(
    start_date: date,
    end_date: date,
) -> None:
    validate_requested_trip_dates(
        start_date,
        end_date,
        create_trip_date_window(REFERENCE_DATE),
    )


@pytest.mark.parametrize(
    ("start_date", "end_date", "code"),
    [
        (
            date(2026, 9, 10),
            date(2026, 9, 11),
            TripDateErrorCode.BEFORE_WINDOW,
        ),
        (
            date(2026, 9, 20),
            date(2026, 9, 21),
            TripDateErrorCode.AFTER_WINDOW,
        ),
        (
            date(2027, 1, 1),
            date(2027, 1, 3),
            TripDateErrorCode.AFTER_WINDOW,
        ),
        (
            date(2026, 9, 13),
            date(2026, 9, 12),
            TripDateErrorCode.RANGE_REVERSED,
        ),
    ],
)
def test_requested_dates_reject_invalid_ranges(
    start_date: date,
    end_date: date,
    code: TripDateErrorCode,
) -> None:
    with pytest.raises(TripDatePolicyError) as captured:
        validate_requested_trip_dates(
            start_date,
            end_date,
            create_trip_date_window(REFERENCE_DATE),
        )

    assert captured.value.code is code


def test_itinerary_dates_accept_values_inside_requested_dates() -> None:
    requirements = TravelRequirements(
        destination="Sydney",
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 13),
    )

    validate_itinerary_dates(
        requirements,
        make_itinerary(),
        create_trip_date_window(REFERENCE_DATE),
    )


def test_itinerary_rejects_a_day_outside_requested_dates() -> None:
    requirements = TravelRequirements(
        destination="Sydney",
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 13),
    )

    with pytest.raises(TripDatePolicyError) as captured:
        validate_itinerary_dates(
            requirements,
            make_itinerary(
                start_date=date(2026, 9, 12),
                end_date=date(2026, 9, 14),
                day_date=date(2026, 9, 14),
                activity_start="2026-09-14T09:00:00+10:00",
                activity_end="2026-09-14T11:00:00+10:00",
            ),
            create_trip_date_window(REFERENCE_DATE),
        )

    assert captured.value.code is TripDateErrorCode.ITINERARY_OUTSIDE_REQUEST
    assert "itinerary.days[0].date" in captured.value.offending_fields


def test_itinerary_rejects_an_activity_end_outside_requested_dates() -> None:
    requirements = TravelRequirements(
        destination="Sydney",
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 13),
    )

    with pytest.raises(TripDatePolicyError) as captured:
        validate_itinerary_dates(
            requirements,
            make_itinerary(
                day_date=date(2026, 9, 13),
                activity_start="2026-09-13T23:00:00+10:00",
                activity_end="2026-09-14T01:00:00+10:00",
            ),
            create_trip_date_window(REFERENCE_DATE),
        )

    assert captured.value.offending_fields == (
        "itinerary.days[0].activities[0].end_time",
    )
