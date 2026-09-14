"""Provider-independent integration interfaces used by V1 services."""

from typing import Protocol, runtime_checkable

from backend.app.integrations.models import (
    PlaceDetailsDTO,
    PlaceDetailsRequest,
    PlaceReviewsDTO,
    PlaceReviewsRequest,
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
        """Return structured details and rating for one Place ID."""

        ...

    async def get_place_reviews(self, request: PlaceReviewsRequest) -> PlaceReviewsDTO:
        """Return bounded provider reviews without unrelated structured details."""

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
