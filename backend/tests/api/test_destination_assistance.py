"""Offline contract checks for GeoDB destination suggestions."""

import asyncio
from datetime import UTC, datetime

import httpx
import pytest

from backend.app.api.input_assistance import get_destination_service
from backend.app.integrations.geodb.client import GeoDBClient
from backend.app.main import app
from backend.app.runtime.config_models import DestinationAssistanceConfig
from backend.app.services.destination_suggestions import DestinationSuggestionService


async def request(service, q):
    app.dependency_overrides[get_destination_service] = lambda: service
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            return await client.get("/api/input-assistance/destinations", params={"q": q})
    finally:
        app.dependency_overrides.pop(get_destination_service, None)


def test_same_name_cities_keep_region_and_country_and_use_fixed_free_host():
    seen = []

    def respond(request):
        seen.append(request)
        return httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": 1,
                        "name": "London",
                        "region": "England",
                        "country": "United Kingdom",
                        "countryCode": "GB",
                    },
                    {
                        "id": 2,
                        "name": "London",
                        "region": "Ontario",
                        "country": "Canada",
                        "countryCode": "CA",
                    },
                ]
            },
        )

    service = DestinationSuggestionService(GeoDBClient(transport=httpx.MockTransport(respond)))
    response = asyncio.run(request(service, " Lon "))
    assert response.status_code == 200
    assert response.json() == {
        "source": "geodb",
        "suggestions": [
            {
                "id": "1",
                "city": "London",
                "region": "England",
                "country": "United Kingdom",
                "country_code": "GB",
                "label": "London, England, United Kingdom",
            },
            {
                "id": "2",
                "city": "London",
                "region": "Ontario",
                "country": "Canada",
                "country_code": "CA",
                "label": "London, Ontario, Canada",
            },
        ],
    }
    assert len(seen) == 1
    assert str(seen[0].url).startswith(
        "http://geodb-free-service.wirefreethought.com/v1/geo/places?"
    )
    assert dict(seen[0].url.params) == {
        "namePrefix": "Lon",
        "sort": "-population",
        "offset": "0",
        "limit": "5",
        "languageCode": "en",
        "types": "CITY",
    }
    assert "x-rapidapi-key" not in seen[0].headers


def test_short_or_long_prefix_is_rejected_before_provider_send():
    sends = []

    def respond(request):
        sends.append(request)
        return httpx.Response(200, json={"data": []})

    service = DestinationSuggestionService(GeoDBClient(transport=httpx.MockTransport(respond)))
    assert asyncio.run(request(service, "x")).status_code == 422
    assert asyncio.run(request(service, "x" * 101)).status_code == 422
    assert sends == []


def test_rate_and_daily_guards_count_sent_attempts_even_after_failure():
    clock = [10.0]
    sends = []

    def respond(request):
        sends.append(request)
        return httpx.Response(503)

    service = DestinationSuggestionService(
        GeoDBClient(transport=httpx.MockTransport(respond)),
        DestinationAssistanceConfig(daily_attempts_per_process=2),
        now=lambda: clock[0],
        utc_now=lambda: datetime(2026, 9, 26, tzinfo=UTC),
    )
    assert asyncio.run(request(service, "Lon")).status_code == 503
    assert asyncio.run(request(service, "Par")).status_code == 429
    clock[0] += 1.1
    assert asyncio.run(request(service, "Par")).status_code == 503
    clock[0] += 1.1
    assert asyncio.run(request(service, "Rom")).status_code == 429
    assert len(sends) == 2


@pytest.mark.parametrize(
    "status,payload,expected",
    [
        (429, None, 429),
        (302, None, 503),
        (200, {"data": "invalid"}, 502),
        (200, {"data": [{"id": 1, "name": "London"}]}, 502),
    ],
)
def test_provider_errors_are_sanitized_without_following_redirects(status, payload, expected):
    def respond(request):
        return httpx.Response(status, json=payload, headers={"Location": "https://example.com/"})

    service = DestinationSuggestionService(GeoDBClient(transport=httpx.MockTransport(respond)))
    result = asyncio.run(request(service, "Lon"))
    assert result.status_code == expected
    assert set(result.json()) == {"error"}
    assert "example.com" not in str(result.json())


def test_missing_region_and_empty_results_have_safe_public_shapes():
    def respond(request):
        return httpx.Response(
            200,
            json={
                "data": [
                    {
                        "id": "q1",
                        "name": "Québec",
                        "region": None,
                        "country": "Canada",
                        "countryCode": "CA",
                    }
                ]
            },
        )

    service = DestinationSuggestionService(GeoDBClient(transport=httpx.MockTransport(respond)))
    result = asyncio.run(request(service, "Qu"))
    assert result.json()["suggestions"][0]["label"] == "Québec, Canada"
