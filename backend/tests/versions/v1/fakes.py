"""Offline deterministic providers and fixtures for V1-A tests."""

from datetime import date, datetime

from backend.app.integrations.models import (
    LatLng,
    PlaceCandidateDTO,
    PlaceDetailsDTO,
    PlaceDetailsRequest,
    PlaceSearchRequest,
    PlaceSearchResponse,
    RouteMatrixDTO,
    RouteMatrixRequest,
    WeatherForecastDTO,
    WeatherRequest,
)
from backend.app.schemas.itinerary import Activity, Itinerary, ItineraryDay
from backend.app.schemas.request import TravelRequirements


def _candidate(place_id: str, rank: int, latitude: float, longitude: float) -> PlaceCandidateDTO:
    return PlaceCandidateDTO(
        place_id=place_id,
        display_name=f"Place {place_id}",
        location=LatLng(latitude=latitude, longitude=longitude),
        formatted_address=f"{rank} Sydney NSW, Australia",
        primary_type="tourist_attraction",
        business_status="OPERATIONAL",
        provider_rank=rank,
    )


class FakePlacesProvider:
    """Return one destination and three deterministic candidate groups."""

    def __init__(self, *, details_failure_ids: set[str] | None = None) -> None:
        self.search_requests: list[PlaceSearchRequest] = []
        self.details_requests: list[PlaceDetailsRequest] = []
        self.details_failure_ids = details_failure_ids or set()
        self._candidate_call = 0

    async def search_text(self, request: PlaceSearchRequest) -> PlaceSearchResponse:
        self.search_requests.append(request)
        if request.location_bias is None:
            candidates = [_candidate("destination-sydney", 0, -33.8688, 151.2093)]
        else:
            group = self._candidate_call
            self._candidate_call += 1
            candidates = [
                _candidate(
                    f"poi-{group}-{rank}",
                    rank,
                    -33.86 - group * 0.01 - rank * 0.001,
                    151.20 + group * 0.01 + rank * 0.001,
                )
                for rank in range(3)
            ]
        return PlaceSearchResponse(
            candidates=candidates,
            retrieved_at="2026-09-11T00:00:00+00:00",
        )

    async def get_place_details(self, request: PlaceDetailsRequest) -> PlaceDetailsDTO:
        self.details_requests.append(request)
        if request.place_id in self.details_failure_ids:
            raise RuntimeError("details unavailable")
        _, group, rank = request.place_id.split("-")
        return PlaceDetailsDTO(
            place_id=request.place_id,
            display_name=f"Place {request.place_id}",
            location=LatLng(
                latitude=-33.86 - int(group) * 0.01 - int(rank) * 0.001,
                longitude=151.20 + int(group) * 0.01 + int(rank) * 0.001,
            ),
            formatted_address=f"{rank} Sydney NSW, Australia",
            primary_type="tourist_attraction",
            business_status="OPERATIONAL",
            time_zone="Australia/Sydney",
            regular_opening_hours={
                "weekdayDescriptions": ["Monday: 9:00 AM - 5:00 PM"]
            },
            rating=4.5,
            user_rating_count=100,
            website_uri=f"https://example.test/{request.place_id}",
            price_level="PRICE_LEVEL_MODERATE",
            accessibility_options={"wheelchairAccessibleEntrance": True},
            retrieved_at="2026-09-11T00:00:00+00:00",
        )


class FakeWeatherProvider:
    def __init__(self, *, failure: bool = False) -> None:
        self.requests: list[WeatherRequest] = []
        self.failure = failure

    async def get_daily_forecast(self, request: WeatherRequest) -> WeatherForecastDTO:
        self.requests.append(request)
        if self.failure:
            raise RuntimeError("weather unavailable")
        return WeatherForecastDTO(
            forecast_days=[
                _weather_day(date(2026, 9, 11), 10),
                _weather_day(date(2026, 9, 12), 20),
                _weather_day(date(2026, 9, 13), 70),
                _weather_day(date(2026, 9, 14), 15),
            ],
            retrieved_at="2026-09-11T00:00:00+00:00",
        )


def _weather_day(value: date, precipitation: int) -> dict[str, object]:
    return {
        "displayDate": {"year": value.year, "month": value.month, "day": value.day},
        "minTemperature": {"degrees": 14},
        "maxTemperature": {"degrees": 22},
        "daytimeForecast": {
            "weatherCondition": {"type": "RAIN" if precipitation > 50 else "CLEAR"},
            "precipitation": {"probability": {"percent": precipitation}},
            "wind": {"speed": {"value": 18, "unit": "KILOMETERS_PER_HOUR"}},
        },
        "nighttimeForecast": {
            "precipitation": {"probability": {"percent": precipitation // 2}},
            "wind": {"speed": {"value": 10, "unit": "KILOMETERS_PER_HOUR"}},
        },
    }


class FakeRoutesProvider:
    def __init__(self, *, failure: bool = False) -> None:
        self.requests: list[RouteMatrixRequest] = []
        self.failure = failure

    async def compute_route_matrix(self, request: RouteMatrixRequest) -> RouteMatrixDTO:
        self.requests.append(request)
        if self.failure:
            raise RuntimeError("routes unavailable")
        elements = [
            {
                "originIndex": origin,
                "destinationIndex": destination,
                "status": {},
                "condition": "ROUTE_EXISTS",
                "distanceMeters": abs(origin - destination) * 1000,
                "duration": f"{abs(origin - destination) * 600}s",
            }
            for origin in range(len(request.origins))
            for destination in range(len(request.destinations))
        ]
        return RouteMatrixDTO(
            elements=elements,
            retrieved_at="2026-09-11T00:00:00+00:00",
        )


def make_requirements() -> TravelRequirements:
    return TravelRequirements(
        destination="Sydney",
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 13),
        traveler_count=2,
        required_activities=["museums", "coastal views", "local food"],
        preferences=["less crowded", "not too much walking"],
    )


def make_itinerary() -> Itinerary:
    return Itinerary(
        destination="Sydney",
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 13),
        days=[
            ItineraryDay(
                date=date(2026, 9, 12),
                activities=[
                    Activity(
                        activity_id="activity-1",
                        title="Visit a museum",
                        place_name="Place poi-0-0",
                        start_time=datetime.fromisoformat("2026-09-12T09:00:00+10:00"),
                        end_time=datetime.fromisoformat("2026-09-12T11:00:00+10:00"),
                    )
                ],
            ),
            ItineraryDay(date=date(2026, 9, 13), activities=[]),
        ],
    )
