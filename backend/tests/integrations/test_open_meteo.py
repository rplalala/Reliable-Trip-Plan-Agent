"""Offline provider/date/source regression checks; no external network."""

import asyncio
from datetime import date
from uuid import UUID

import httpx
import pytest

from backend.app.evidence.models import EvidenceAvailability
from backend.app.evidence.normalization import normalize_weather
from backend.app.integrations.http import HttpxJSONTransport, ProviderHTTPError
from backend.app.integrations.models import LatLng, WeatherRequest
from backend.app.integrations.open_meteo import OpenMeteoWeatherProvider
from backend.app.observability.run_trace import NullRunTracer


def request():
    return WeatherRequest(
        location=LatLng(latitude=51.5, longitude=-0.1),
        requested_start=date(2026, 10, 4),
        requested_end=date(2026, 10, 6),
    )


def payload():
    return {
        "timezone": "Europe/London",
        "utc_offset_seconds": 3600,
        "daily_units": {
            "time": "iso8601",
            "weather_code": "wmo code",
            "temperature_2m_max": "°C",
            "temperature_2m_min": "°C",
            "precipitation_probability_max": "%",
            "wind_speed_10m_max": "km/h",
        },
        "daily": {
            "time": ["2026-10-04", "2026-10-05", "2026-10-06"],
            "weather_code": [0, 63, 95],
            "temperature_2m_max": [20, 19, 18],
            "temperature_2m_min": [10, 9, 8],
            "precipitation_probability_max": [0, 80, 90],
            "wind_speed_10m_max": [0, 20, 30],
        },
    }


class Transport:
    def __init__(self, response):
        self.response = response
        self.calls = []

    async def request_json(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        return self.response


def convert(raw):
    transport = Transport(raw)
    provider = OpenMeteoWeatherProvider(transport=transport, tracer=NullRunTracer(UUID(int=1)))
    dto = asyncio.run(provider.get_daily_forecast(request()))
    return normalize_weather(dto, request=request(), destination="London"), transport


def test_exact_delayed_dates_units_source_and_code():
    evidence, transport = convert(payload())
    params = transport.calls[0][2]["params"]
    assert params["start_date"] == "2026-10-04"
    assert params["end_date"] == "2026-10-06"
    assert params["timezone"] == "auto"
    assert "forecast_days" not in params and "key" not in params
    assert len(transport.calls) == 1
    assert evidence.availability is EvidenceAvailability.AVAILABLE
    assert evidence.timezone == "Europe/London"
    assert evidence.source_ref == "open_meteo:daily_forecast"
    assert "CC BY 4.0" in evidence.attribution
    assert evidence.days[0].precipitation_probability_percent == 0
    assert evidence.days[1].condition == "Moderate rain"
    assert evidence.days[2].max_wind_speed_kph == 30


def test_null_last_date_is_partial_not_clear_weather():
    raw = payload()
    for key in raw["daily"]:
        if key != "time":
            raw["daily"][key][-1] = None
    evidence, _ = convert(raw)
    assert evidence.availability is EvidenceAvailability.PARTIAL
    assert evidence.missing_dates == [date(2026, 10, 6)]
    assert evidence.days[-1].condition is None
    assert evidence.days[-1].min_temperature_c is None


def test_missing_date_and_short_field_keep_other_data():
    raw = payload()
    raw["daily"]["time"] = raw["daily"]["time"][:2]
    raw["daily"]["temperature_2m_max"] = [20]
    evidence, _ = convert(raw)
    assert len(evidence.days) == 2
    assert evidence.days[1].max_temperature_c is None
    assert evidence.missing_dates == [date(2026, 10, 6)]
    assert evidence.availability is EvidenceAvailability.PARTIAL


@pytest.mark.parametrize(
    "field,unit",
    [
        ("temperature_2m_max", "°F"),
        ("wind_speed_10m_max", "mph"),
        ("precipitation_probability_max", "fraction"),
        ("weather_code", "unknown"),
    ],
)
def test_unexpected_units_remain_unknown(field, unit):
    raw = payload()
    raw["daily_units"][field] = unit
    evidence, _ = convert(raw)
    assert evidence.availability is EvidenceAvailability.PARTIAL


@pytest.mark.parametrize("raw", [[], {"error": True}, {}, {"daily": {}, "daily_units": {}}])
def test_invalid_envelope_raises_provider_error(raw):
    with pytest.raises(ProviderHTTPError):
        convert(raw)


def test_no_dates_is_unavailable():
    raw = payload()
    raw["daily"]["time"] = []
    evidence, _ = convert(raw)
    assert evidence.availability is EvidenceAvailability.UNAVAILABLE
    assert len(evidence.missing_dates) == 3


def test_http_transport_no_retry_on_error(monkeypatch):
    calls = []

    def handler(req):
        calls.append(req)
        return httpx.Response(400, json={"error": True, "reason": "invalid dates"})

    original = httpx.AsyncClient
    monkeypatch.setattr(
        httpx, "AsyncClient", lambda **kw: original(**kw, transport=httpx.MockTransport(handler))
    )
    provider = OpenMeteoWeatherProvider(
        transport=HttpxJSONTransport(), tracer=NullRunTracer(UUID(int=1))
    )
    with pytest.raises(ProviderHTTPError):
        asyncio.run(provider.get_daily_forecast(request()))
    assert len(calls) == 1


def test_shared_factory_keeps_google_places_routes_and_replaces_only_weather():
    from pydantic import SecretStr

    from backend.app.integrations.google import GooglePlacesProvider, GoogleRoutesProvider
    from backend.app.versions.v1 import runner as v1
    from backend.app.versions.v1.config import V1Settings
    from backend.app.versions.v1.runner import _create_tool_providers
    from backend.app.versions.v2 import runner as v2

    settings = V1Settings.model_construct(google_maps_api_key=SecretStr("fake"))
    places, weather, routes = _create_tool_providers(settings, NullRunTracer(UUID(int=1)))
    assert isinstance(places, GooglePlacesProvider)
    assert isinstance(routes, GoogleRoutesProvider)
    assert isinstance(weather, OpenMeteoWeatherProvider)
    assert v2.run_tools_planner is v1.run_tools_planner


def test_weather_cache_dates_provider_and_failure_semantics():
    from backend.app.runtime.budget import ToolBudget
    from backend.app.runtime.cache import RequestCache
    from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService
    from backend.tests.versions.v1.fakes import (
        FakePlacesProvider,
        FakeRoutesProvider,
        FakeWeatherProvider,
        make_requirements,
    )

    async def scenario():
        cache = RequestCache()
        weather = FakeWeatherProvider()
        service = V1EvidenceAcquisitionService(
            places_provider=FakePlacesProvider(),
            weather_provider=weather,
            routes_provider=FakeRoutesProvider(),
            budget=ToolBudget(),
            cache=cache,
            tracer=NullRunTracer(UUID(int=1)),
        )
        destination = await service.resolve_destination("Sydney")
        requirements = make_requirements()
        kwargs = dict(
            requirements=requirements, destination=destination, reference_date=date(2026, 9, 11)
        )
        await service.acquire_weather(**kwargs)
        await service.acquire_weather(**kwargs)
        assert len(weather.requests) == 1
        keys = [key for key in cache.attempts if key[0] == "weather_daily"]
        assert len(keys) == 1 and "open_meteo" in keys[0] and "auto" in keys[0]
        weather.failure = True
        kwargs["requirements"] = requirements.model_copy(update={"end_date": date(2026, 9, 14)})
        evidence = await service.acquire_weather(**kwargs)
        assert evidence.availability is EvidenceAvailability.UNAVAILABLE
        assert len(evidence.missing_dates) == 3
        assert evidence.source_ref == "open_meteo:daily_forecast"
        await service.acquire_weather(**kwargs)
        assert len(weather.requests) == 2

    asyncio.run(scenario())


def test_provider_cancellation_propagates():
    class CancelTransport:
        async def request_json(self, *args, **kwargs):
            raise asyncio.CancelledError()

    provider = OpenMeteoWeatherProvider(
        transport=CancelTransport(), tracer=NullRunTracer(UUID(int=1))
    )
    with pytest.raises(asyncio.CancelledError):
        asyncio.run(provider.get_daily_forecast(request()))
