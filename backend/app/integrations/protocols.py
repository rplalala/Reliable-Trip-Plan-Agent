"""Provider-independent integration interfaces used by V1 services."""

from typing import Protocol, runtime_checkable

from backend.app.integrations.models import (
    PlaceDetailsDTO,
    PlaceDetailsRequest,
    PlaceSearchRequest,
    PlaceSearchResponse,
    RouteMatrixDTO,
    RouteMatrixRequest,
    WeatherForecastDTO,
    WeatherRequest,
)


@runtime_checkable
class PlacesProvider(Protocol):
    async def search_text(self, request: PlaceSearchRequest) -> PlaceSearchResponse:
        """Return minimal candidates for one bounded text search."""

        ...

    async def get_place_details(self, request: PlaceDetailsRequest) -> PlaceDetailsDTO:
        """Return rich details for one shortlisted Place ID."""

        ...


@runtime_checkable
class WeatherProvider(Protocol):
    async def get_daily_forecast(self, request: WeatherRequest) -> WeatherForecastDTO:
        """Return one daily forecast response for a destination."""

        ...


@runtime_checkable
class RoutesProvider(Protocol):
    async def compute_route_matrix(self, request: RouteMatrixRequest) -> RouteMatrixDTO:
        """Return one bounded route matrix response."""

        ...
