"""Open-Meteo daily forecasts normalized at the provider boundary."""

from datetime import UTC, date, datetime
from math import isfinite
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from backend.app.integrations.http import AsyncJSONTransport, ProviderHTTPError
from backend.app.integrations.models import WeatherDayDTO, WeatherForecastDTO, WeatherRequest
from backend.app.observability.run_trace import RunTracer, TracePayloadMode

DAILY_FIELDS = (
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_probability_max",
    "wind_speed_10m_max",
)
WMO_CONDITIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


class OpenMeteoWeatherProvider:
    """One exact-date request, with no geocoding, retries or fallback provider.

    Free endpoint: non-commercial use, CC BY 4.0 attribution required.
    Daily precipitation probability and wind are daily maxima, not guarantees.
    """

    def __init__(self, *, transport: AsyncJSONTransport, tracer: RunTracer) -> None:
        self._transport = transport
        self._tracer = tracer

    async def get_daily_forecast(self, request: WeatherRequest) -> WeatherForecastDTO:
        params = {
            "latitude": request.location.latitude,
            "longitude": request.location.longitude,
            "start_date": request.requested_start.isoformat(),
            "end_date": request.requested_end.isoformat(),
            "daily": ",".join(DAILY_FIELDS),
            "timezone": request.timezone,
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
        }
        response = await self._transport.request_json(
            "GET",
            "https://api.open-meteo.com/v1/forecast",
            params=params,
        )
        self._tracer.payload(
            "tools",
            "open_meteo_daily_forecast",
            {"request": params, "response": response},
            minimum_mode=TracePayloadMode.RAW,
        )
        if not isinstance(response, dict) or response.get("error"):
            raise ProviderHTTPError("Invalid Open-Meteo forecast response")
        daily, units = response.get("daily"), response.get("daily_units")
        if not isinstance(daily, dict) or not isinstance(units, dict):
            raise ProviderHTTPError("Open-Meteo daily data or units missing")
        timezone = response.get("timezone")
        try:
            if not isinstance(timezone, str):
                raise ValueError("Missing forecast time zone")
            ZoneInfo(timezone)
        except (ValueError, ZoneInfoNotFoundError) as exc:
            raise ProviderHTTPError("Invalid Open-Meteo time zone") from exc
        times = daily.get("time")
        if not isinstance(times, list) or units.get("time") != "iso8601":
            raise ProviderHTTPError("Invalid Open-Meteo daily dates")

        def number(field: str, index: int, unit: str) -> float | None:
            values = daily.get(field)
            if units.get(field) != unit or not isinstance(values, list) or index >= len(values):
                return None
            value = values[index]
            if isinstance(value, bool) or not isinstance(value, int | float) or not isfinite(value):
                return None
            return float(value)

        days = []
        seen = set()
        for i, value in enumerate(times):
            try:
                day = date.fromisoformat(value)
            except (TypeError, ValueError):
                continue
            if day in seen or not request.requested_start <= day <= request.requested_end:
                continue
            seen.add(day)
            code = number("weather_code", i, "wmo code")
            probability = number("precipitation_probability_max", i, "%")
            # The current contract stores integer percent; fractional values remain unknown.
            probability = (
                int(probability)
                if probability is not None and probability.is_integer() and 0 <= probability <= 100
                else None
            )
            wind = number("wind_speed_10m_max", i, "km/h")
            days.append(
                WeatherDayDTO(
                    date=day,
                    condition=WMO_CONDITIONS.get(code),
                    min_temperature_c=number("temperature_2m_min", i, "°C"),
                    max_temperature_c=number("temperature_2m_max", i, "°C"),
                    precipitation_probability_percent=probability,
                    max_wind_speed_kph=wind if wind is not None and wind >= 0 else None,
                )
            )
        return WeatherForecastDTO(
            forecast_days=days,
            retrieved_at=datetime.now(UTC).isoformat(),
            timezone=timezone,
        )
