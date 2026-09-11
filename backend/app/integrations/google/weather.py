"""Google Weather Daily Forecast adapter."""

from datetime import UTC, datetime

from backend.app.integrations.google.common import require_mapping, trace_exchange
from backend.app.integrations.http import AsyncJSONTransport
from backend.app.integrations.models import WeatherForecastDTO, WeatherRequest
from backend.app.observability.run_trace import RunTracer


class GoogleWeatherProvider:
    """Retrieve one metric daily forecast response without pagination."""

    def __init__(
        self,
        *,
        api_key: str,
        transport: AsyncJSONTransport,
        tracer: RunTracer,
        base_url: str = "https://weather.googleapis.com/v1",
    ) -> None:
        self._api_key = api_key
        self._transport = transport
        self._tracer = tracer
        self._base_url = base_url.rstrip("/")

    async def get_daily_forecast(self, request: WeatherRequest) -> WeatherForecastDTO:
        params: dict[str, object] = {
            "key": self._api_key,
            "location.latitude": request.location.latitude,
            "location.longitude": request.location.longitude,
            "days": request.horizon_days,
            "pageSize": request.horizon_days,
            "unitsSystem": "METRIC",
            "languageCode": request.language_code,
        }
        response = await self._transport.request_json(
            "GET",
            f"{self._base_url}/forecast/days:lookup",
            params=params,
        )
        trace_exchange(
            self._tracer,
            name="google_weather_daily_forecast",
            request={"params": params},
            response=response,
        )
        payload = require_mapping(response, context="Weather Daily Forecast response")
        raw_days = payload.get("forecastDays", [])
        if not isinstance(raw_days, list):
            raw_days = []
        return WeatherForecastDTO(
            forecast_days=[dict(item) for item in raw_days if isinstance(item, dict)],
            retrieved_at=datetime.now(UTC).isoformat(),
        )
