"""Offline contract tests for Google V1-A HTTP adapters."""

import asyncio
from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID

from backend.app.integrations.google.places import (
    PLACES_CANDIDATE_FIELD_MASK,
    PLACES_DETAILS_FIELD_MASK,
    GooglePlacesProvider,
)
from backend.app.integrations.google.routes import (
    ROUTE_MATRIX_FIELD_MASK,
    GoogleRoutesProvider,
)
from backend.app.integrations.google.weather import GoogleWeatherProvider
from backend.app.integrations.models import (
    LatLng,
    PlaceDetailsRequest,
    PlaceSearchRequest,
    RouteMatrixRequest,
    RouteWaypoint,
    WeatherRequest,
)
from backend.app.observability.run_trace import NullRunTracer


@dataclass
class FakeTransport:
    responses: list[object]
    calls: list[dict[str, object]] = field(default_factory=list)

    async def request_json(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, object] | None = None,
        json_body: object | None = None,
    ) -> object:
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": headers,
                "params": params,
                "json_body": json_body,
            }
        )
        return self.responses.pop(0)


TRACER = NullRunTracer(UUID("00000000-0000-0000-0000-000000000001"))


def test_places_candidate_and_details_field_masks_match_current_api_paths() -> None:
    transport = FakeTransport(
        responses=[
            {
                "places": [
                    {
                        "id": "poi-1",
                        "displayName": {"text": "Museum"},
                        "location": {"latitude": -33.8, "longitude": 151.2},
                        "formattedAddress": "Sydney",
                        "primaryType": "museum",
                        "businessStatus": "OPERATIONAL",
                    }
                ]
            },
            {
                "id": "poi-1",
                "displayName": {"text": "Museum"},
                "location": {"latitude": -33.8, "longitude": 151.2},
                "timeZone": {"id": "Australia/Sydney", "version": "2026a"},
            },
        ]
    )
    provider = GooglePlacesProvider(
        api_key="secret-key", transport=transport, tracer=TRACER
    )

    async def scenario():
        await provider.search_text(
            PlaceSearchRequest(
                text_query="museums in Sydney",
                page_size=5,
                field_mask=PLACES_CANDIDATE_FIELD_MASK,
            )
        )
        return await provider.get_place_details(
            PlaceDetailsRequest(place_id="poi-1", field_mask=PLACES_DETAILS_FIELD_MASK)
        )

    details = asyncio.run(scenario())

    assert PLACES_CANDIDATE_FIELD_MASK == (
        "places.id,places.displayName,places.location,places.formattedAddress,"
        "places.primaryType,places.businessStatus"
    )
    assert "places.displayName.text" not in PLACES_CANDIDATE_FIELD_MASK
    assert "reviews" not in PLACES_DETAILS_FIELD_MASK.casefold()
    assert details.time_zone == "Australia/Sydney"
    assert transport.calls[0]["headers"]["X-Goog-FieldMask"] == PLACES_CANDIDATE_FIELD_MASK
    assert transport.calls[1]["headers"]["X-Goog-FieldMask"] == PLACES_DETAILS_FIELD_MASK


def test_weather_adapter_requests_one_unpaginated_metric_daily_horizon() -> None:
    transport = FakeTransport(responses=[{"forecastDays": []}])
    provider = GoogleWeatherProvider(
        api_key="secret-key", transport=transport, tracer=TRACER
    )

    asyncio.run(
        provider.get_daily_forecast(
            WeatherRequest(
                location=LatLng(latitude=-33.8, longitude=151.2),
                horizon_days=4,
                requested_start=date(2026, 9, 12),
                requested_end=date(2026, 9, 14),
            )
        )
    )

    assert transport.calls[0]["url"].endswith("/forecast/days:lookup")
    assert transport.calls[0]["params"] == {
        "key": "secret-key",
        "location.latitude": -33.8,
        "location.longitude": 151.2,
        "days": 4,
        "pageSize": 4,
        "unitsSystem": "METRIC",
        "languageCode": "en",
    }


def test_routes_adapter_uses_minimal_fields_and_omits_invalid_preference() -> None:
    transport = FakeTransport(responses=[[]])
    provider = GoogleRoutesProvider(
        api_key="secret-key", transport=transport, tracer=TRACER
    )
    waypoint = RouteWaypoint(
        place_id="poi-1", location=LatLng(latitude=-33.8, longitude=151.2)
    )

    asyncio.run(
        provider.compute_route_matrix(
            RouteMatrixRequest(
                origins=[waypoint],
                destinations=[waypoint],
                travel_mode="WALK",
                field_mask=ROUTE_MATRIX_FIELD_MASK,
            )
        )
    )

    body = transport.calls[0]["json_body"]
    assert ROUTE_MATRIX_FIELD_MASK == (
        "originIndex,destinationIndex,duration,distanceMeters,status,condition"
    )
    assert body["travelMode"] == "WALK"
    assert "routingPreference" not in body
    assert "departureTime" not in body


def test_routes_adapter_serializes_transit_departure_time() -> None:
    transport = FakeTransport(responses=[[]])
    provider = GoogleRoutesProvider(
        api_key="secret-key", transport=transport, tracer=TRACER
    )
    waypoint = RouteWaypoint(
        place_id="poi-1", location=LatLng(latitude=-33.8, longitude=151.2)
    )

    asyncio.run(
        provider.compute_route_matrix(
            RouteMatrixRequest(
                origins=[waypoint],
                destinations=[waypoint],
                travel_mode="TRANSIT",
                departure_time=datetime.fromisoformat("2026-09-12T12:00:00+10:00"),
                field_mask=ROUTE_MATRIX_FIELD_MASK,
            )
        )
    )

    assert transport.calls[0]["json_body"]["departureTime"] == "2026-09-12T02:00:00Z"
