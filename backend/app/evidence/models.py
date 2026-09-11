"""Small normalized evidence contracts consumed by the V1 planner."""

from datetime import date, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class EvidenceModel(BaseModel):
    """Strict immutable base for normalized external evidence."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class EvidenceAvailability(StrEnum):
    """Explicit provider/evidence completeness states."""

    AVAILABLE = "available"
    PARTIAL = "partial"
    UNAVAILABLE = "unavailable"


class DestinationContext(EvidenceModel):
    """Resolved destination coordinate used to bias external requests."""

    place_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    formatted_address: str | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class PlaceCandidate(EvidenceModel):
    """Minimal candidate-stage data plus deterministic shortlist metadata."""

    place_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    formatted_address: str | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    primary_type: str | None = None
    business_status: str | None = None
    source_query: str = Field(min_length=1)
    category: str = Field(min_length=1)
    provider_rank: int = Field(ge=0)


class OpeningHoursEvidence(EvidenceModel):
    """Compact opening information with explicit temporal applicability."""

    applicability: str = Field(min_length=1)
    weekday_descriptions: list[str] = Field(default_factory=list)
    open_now: bool | None = None
    next_open_time: datetime | None = None
    next_close_time: datetime | None = None


class PlaceEvidence(EvidenceModel):
    """Planning-relevant normalized information for one shortlisted POI."""

    place_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    formatted_address: str | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    primary_type: str | None = None
    business_status: str | None = None
    timezone_id: str | None = None
    opening_hours: OpeningHoursEvidence | None = None
    rating: float | None = Field(default=None, ge=0, le=5)
    user_rating_count: int | None = Field(default=None, ge=0)
    price_level: str | None = None
    price_range: str | None = None
    accessibility_options: dict[str, bool] | None = None
    website_uri: str | None = None
    availability: EvidenceAvailability
    unavailable_reason: str | None = None
    retrieved_at: datetime
    source_ref: str = Field(min_length=1)


class WeatherDayEvidence(EvidenceModel):
    """Minimal daily weather facts for one requested trip date."""

    date: date
    condition: str | None = None
    min_temperature_c: float | None = None
    max_temperature_c: float | None = None
    precipitation_probability_percent: int | None = Field(default=None, ge=0, le=100)
    max_wind_speed_kph: float | None = Field(default=None, ge=0)


class WeatherEvidence(EvidenceModel):
    """Destination weather containing only requested trip dates."""

    destination: str = Field(min_length=1)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    availability: EvidenceAvailability
    days: list[WeatherDayEvidence] = Field(default_factory=list)
    unavailable_reason: str | None = None
    retrieved_at: datetime
    source_ref: str = Field(min_length=1)


class RouteElementEvidence(EvidenceModel):
    """One origin/destination result from a bounded route matrix."""

    origin_place_id: str = Field(min_length=1)
    destination_place_id: str = Field(min_length=1)
    status: str | None = None
    condition: str | None = None
    distance_meters: int | None = Field(default=None, ge=0)
    duration_seconds: int | None = Field(default=None, ge=0)
    availability: EvidenceAvailability


class RouteEvidence(EvidenceModel):
    """Normalized bounded route matrix and its deterministic mode decision."""

    travel_mode: str = Field(min_length=1)
    mode_reason: str = Field(min_length=1)
    routing_preference: str | None = None
    availability: EvidenceAvailability
    elements: list[RouteElementEvidence] = Field(default_factory=list)
    unavailable_reason: str | None = None
    retrieved_at: datetime
    source_ref: str = Field(min_length=1)
