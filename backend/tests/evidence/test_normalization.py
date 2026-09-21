"""Tests that raw provider data is reduced to bounded typed evidence."""

from datetime import date

from backend.app.evidence.models import EvidenceAvailability
from backend.app.evidence.normalization import normalize_routes, normalize_weather
from backend.app.integrations.models import (
    LatLng,
    RouteMatrixDTO,
    RouteMatrixRequest,
    RouteWaypoint,
    WeatherForecastDTO,
    WeatherRequest,
)
from backend.tests.versions.v1.fakes import _weather_day


def test_weather_normalization_exposes_only_requested_dates() -> None:
    request = WeatherRequest(
        location=LatLng(latitude=-33.8, longitude=151.2),
        requested_start=date(2026, 9, 12),
        requested_end=date(2026, 9, 13),
    )
    raw = WeatherForecastDTO(
        forecast_days=[
            _weather_day(date(2026, 9, 11), 5),
            _weather_day(date(2026, 9, 12), 20),
            _weather_day(date(2026, 9, 13), 70),
            _weather_day(date(2026, 9, 14), 10),
        ],
        retrieved_at="2026-09-11T00:00:00+00:00",
    )

    evidence = normalize_weather(raw, request=request, destination="Sydney")

    assert [item.date for item in evidence.days] == [
        date(2026, 9, 12),
        date(2026, 9, 13),
    ]
    assert evidence.days[1].precipitation_probability_percent == 70
    assert evidence.availability is EvidenceAvailability.AVAILABLE


def test_route_normalization_preserves_partial_matrix_failure() -> None:
    waypoints = [
        RouteWaypoint(place_id="a", location=LatLng(latitude=0, longitude=0)),
        RouteWaypoint(place_id="b", location=LatLng(latitude=1, longitude=1)),
    ]
    request = RouteMatrixRequest(
        origins=waypoints,
        destinations=waypoints,
        travel_mode="WALK",
        field_mask="originIndex,destinationIndex,status,condition,distanceMeters,duration",
    )
    raw = RouteMatrixDTO(
        elements=[
            {
                "originIndex": 0,
                "destinationIndex": 1,
                "status": {},
                "condition": "ROUTE_EXISTS",
                "distanceMeters": 100,
                "duration": "60s",
            },
            {
                "originIndex": 1,
                "destinationIndex": 0,
                "status": {"code": 5, "message": "not found"},
                "condition": "ROUTE_NOT_FOUND",
            },
        ],
        retrieved_at="2026-09-11T00:00:00+00:00",
    )

    evidence = normalize_routes(raw, request=request, mode_reason="test")

    assert evidence.availability is EvidenceAvailability.PARTIAL
    assert evidence.elements[0].duration_seconds == 60
    assert evidence.elements[1].availability is EvidenceAvailability.UNAVAILABLE
