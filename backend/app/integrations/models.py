"""Provider-bound request and response DTOs for V1-A integrations."""

from datetime import date

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


class IntegrationModel(BaseModel):
    """Strict immutable integration DTO base."""

    model_config = ConfigDict(extra="forbid", frozen=True)


class LatLng(IntegrationModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class PlaceSearchRequest(IntegrationModel):
    text_query: str = Field(min_length=1)
    page_size: int = Field(ge=1, le=20)
    field_mask: str = Field(min_length=1)
    location_bias: LatLng | None = None
    language_code: str = "en"


class PlaceCandidateDTO(IntegrationModel):
    place_id: str = Field(min_length=1)
    display_name: str = Field(min_length=1)
    location: LatLng
    formatted_address: str | None = None
    primary_type: str | None = None
    business_status: str | None = None
    provider_rank: int = Field(ge=0)


class PlaceSearchResponse(IntegrationModel):
    candidates: list[PlaceCandidateDTO] = Field(default_factory=list)
    retrieved_at: str


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
    time_zone: str | None = None
    current_opening_hours: dict[str, object] | None = None
    regular_opening_hours: dict[str, object] | None = None
    rating: float | None = None
    user_rating_count: int | None = None
    website_uri: str | None = None
    price_level: str | None = None
    price_range: dict[str, object] | None = None
    accessibility_options: dict[str, bool] | None = None
    retrieved_at: str


class WeatherRequest(IntegrationModel):
    location: LatLng
    horizon_days: int = Field(ge=1, le=10)
    requested_start: date
    requested_end: date
    language_code: str = "en"


class WeatherForecastDTO(IntegrationModel):
    forecast_days: list[dict[str, object]] = Field(default_factory=list)
    retrieved_at: str


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
    elements: list[dict[str, object]] = Field(default_factory=list)
    retrieved_at: str
