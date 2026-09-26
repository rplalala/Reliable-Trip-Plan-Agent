"""One bounded request to the fixed GeoDB public free HTTP endpoint."""

from collections.abc import Mapping

import httpx
from pydantic import BaseModel, ConfigDict, Field

GEODB_PLACES_URL = "http://geodb-free-service.wirefreethought.com/v1/geo/places"


class GeoDBUnavailable(RuntimeError):
    """The free service could not be reached or declined the request."""


class GeoDBThrottled(GeoDBUnavailable):
    """The provider declined the request because of a rate limit."""


class GeoDBTimeout(GeoDBUnavailable):
    """The single provider request exceeded its deadline."""


class GeoDBInvalidResponse(RuntimeError):
    """The provider returned an unusable result."""


class DestinationSuggestion(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(min_length=1, max_length=80)
    city: str = Field(min_length=1, max_length=120)
    region: str | None = Field(max_length=120)
    country: str = Field(min_length=1, max_length=120)
    country_code: str = Field(pattern=r"^[A-Z]{2}$")
    label: str = Field(min_length=1, max_length=400)


class GeoDBClient:
    """Normalize provider fields so the UI never consumes a raw provider object."""

    def __init__(self, *, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._transport = transport

    async def search(
        self, prefix: str, *, limit: int = 5, timeout_seconds: float = 3
    ) -> list[DestinationSuggestion]:
        try:
            async with httpx.AsyncClient(
                transport=self._transport, timeout=timeout_seconds, follow_redirects=False
            ) as client:
                response = await client.get(
                    GEODB_PLACES_URL,
                    params={
                        "namePrefix": prefix,
                        "sort": "-population",
                        "offset": 0,
                        "limit": limit,
                        "languageCode": "en",
                        "types": "CITY",
                    },
                )
            if response.status_code == 429:
                raise GeoDBThrottled()
            if response.status_code != 200:
                raise GeoDBUnavailable()
            payload = response.json()
        except httpx.TimeoutException as exc:
            raise GeoDBTimeout() from exc
        except httpx.RequestError as exc:
            raise GeoDBUnavailable() from exc
        except ValueError as exc:
            raise GeoDBInvalidResponse() from exc

        if not isinstance(payload, Mapping) or not isinstance(payload.get("data"), list):
            raise GeoDBInvalidResponse()
        rows = payload["data"]
        if len(rows) > limit:
            rows = rows[:limit]
        suggestions: list[DestinationSuggestion] = []
        for row in rows:
            if not isinstance(row, Mapping):
                raise GeoDBInvalidResponse()
            identifier = row.get("id")
            city = row.get("name")
            region = row.get("region")
            country = row.get("country")
            country_code = row.get("countryCode")
            if (
                not isinstance(identifier, (str, int))
                or isinstance(identifier, bool)
                or not isinstance(city, str)
                or not city.strip()
                or region is not None
                and not isinstance(region, str)
                or not isinstance(country, str)
                or not country.strip()
                or not isinstance(country_code, str)
            ):
                raise GeoDBInvalidResponse()
            parts = [city.strip(), region.strip() if region else None, country.strip()]
            try:
                suggestions.append(
                    DestinationSuggestion(
                        id=str(identifier),
                        city=city.strip(),
                        region=region.strip() if region and region.strip() else None,
                        country=country.strip(),
                        country_code=country_code,
                        label=", ".join(part for part in parts if part),
                    )
                )
            except ValueError as exc:
                raise GeoDBInvalidResponse() from exc
        return suggestions
