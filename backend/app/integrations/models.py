"""Provider-bound request and response DTOs for V1-A integrations."""

from datetime import date
from typing import Literal, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator


class IntegrationModel(BaseModel):
    """Strict immutable integration DTO base."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class LatLng(IntegrationModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class PlaceOpeningDateDTO(IntegrationModel):
    """Google Places calendar parts without inventing missing precision."""

    year: int | None = Field(default=None, ge=1, le=9999)
    month: int | None = Field(default=None, ge=1, le=12)
    day: int | None = Field(default=None, ge=1, le=31)

    @model_validator(mode="after")
    def valid_full_date(self) -> "PlaceOpeningDateDTO":
        if self.year is not None and self.month is not None and self.day is not None:
            date(self.year, self.month, self.day)
        return self


class PlaceSearchRequest(IntegrationModel):
    text_query: str = Field(min_length=1)
    page_size: int = Field(ge=1, le=20)
    field_mask: str = Field(min_length=1)
    location_bias: LatLng | None = None
    language_code: str = "en"
    include_future_opening_businesses: bool = False


class PlaceNearbySearchRequest(IntegrationModel):
    center: LatLng
    radius_metres: float = Field(gt=0, le=50000)
    max_result_count: int = Field(ge=1, le=20)
    included_types: tuple[str, ...]
    rank_preference: Literal["DISTANCE"] = "DISTANCE"
    language_code: str = "en"
    field_mask: str = Field(min_length=1)
    include_future_opening_businesses: Literal[False] = False


class PlaceCandidateDTO(IntegrationModel):
    place_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    location: LatLng
    formatted_address: str | None = None
    primary_type: str | None = None
    types: tuple[str, ...] = ()
    attributions: tuple[dict[str, object], ...] = ()
    business_status: str | None = None
    opening_date: PlaceOpeningDateDTO | None = None
    provider_rank: int = Field(ge=0)


class PlaceSearchResponse(IntegrationModel):
    candidates: list[PlaceCandidateDTO] = Field(default_factory=list)
    actual_result_count: int = Field(ge=0)
    retrieved_at: str

    @model_validator(mode="after")
    def ranks_match_raw_count(self) -> Self:
        if any(item.provider_rank >= self.actual_result_count for item in self.candidates):
            raise ValueError("Candidate provider rank exceeds raw result count")
        return self


class PlaceDetailsRequest(IntegrationModel):
    place_id: str = Field(min_length=1)
    field_mask: str = Field(min_length=1)
    language_code: str = "en"


class PlaceDetailsDTO(IntegrationModel):
    place_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    location: LatLng
    formatted_address: str | None = None
    primary_type: str | None = None
    business_status: str | None = None
    opening_date: PlaceOpeningDateDTO | None = None
    time_zone: str | None = None
    current_opening_hours: dict[str, object] | None = None
    regular_opening_hours: dict[str, object] | None = None
    rating: float | None = Field(default=None, ge=0, le=5)
    website_uri: str | None = None
    price_level: str | None = None
    price_range: dict[str, object] | None = None
    accessibility_options: dict[str, bool] | None = None
    requested_at: str | None = None
    retrieved_at: str


class PlaceReviewsRequest(IntegrationModel):
    place_id: str = Field(min_length=1)
    field_mask: str = Field(min_length=1)
    language_code: str = "en"


class PlaceReviewDTO(IntegrationModel):
    """Provider review fields retained for later bounded evidence processing."""

    resource_name: str | None = None
    text: str | None = None
    publish_time: AwareDatetime | None = None
    google_maps_uri: str | None = None


class PlaceReviewsDTO(IntegrationModel):
    place_id: str = Field(min_length=1)
    reviews: list[PlaceReviewDTO] = Field(default_factory=list)
    retrieved_at: str


class WeatherRequest(IntegrationModel):
    location: LatLng
    requested_start: date
    requested_end: date
    timezone: str = "auto"
    provider: Literal["open_meteo"] = "open_meteo"


class WeatherDayDTO(IntegrationModel):
    """Provider-independent metric daily aggregates; null means unknown."""

    date: date
    condition: str | None = None
    min_temperature_c: float | None = None
    max_temperature_c: float | None = None
    precipitation_probability_percent: int | None = Field(default=None, ge=0, le=100)
    max_wind_speed_kph: float | None = Field(default=None, ge=0)


class WeatherForecastDTO(IntegrationModel):
    forecast_days: list[WeatherDayDTO] = Field(default_factory=list)
    retrieved_at: str
    timezone: str | None = None
    source_ref: str = "open_meteo:daily_forecast"
    attribution: str = "Weather data by Open-Meteo (CC BY 4.0): https://open-meteo.com/"


class RouteWaypoint(IntegrationModel):
    place_id: str = Field(min_length=1)
    location: LatLng


class RouteMatrixRequest(IntegrationModel):
    origins: list[RouteWaypoint] = Field(min_length=1)
    destinations: list[RouteWaypoint] = Field(min_length=1)
    travel_mode: str = Field(min_length=1)
    routing_preference: str | None = None
    departure_time: AwareDatetime | None = None
    field_mask: str = Field(min_length=1)


class RouteMatrixDTO(IntegrationModel):
    requested_at: str | None = None
    elements: list[dict[str, object]] = Field(default_factory=list)
    retrieved_at: str
