"""Provider-independent structured itinerary schemas."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.schemas.request import Money

ActivityKind = Literal["main_poi", "generic_activity", "transport", "free_time", "unknown"]


class Activity(BaseModel):
    """A scheduled itinerary activity."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    activity_kind: ActivityKind = "unknown"
    activity_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    place_name: str | None = Field(default=None, min_length=1)
    source_place_id: str | None = Field(default=None, min_length=1, max_length=256)
    location: str | None = Field(default=None, min_length=1)
    start_time: datetime
    end_time: datetime
    estimated_cost: Money | None = None
    notes: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_time_range(self) -> "Activity":
        """Require an activity to finish after it starts."""

        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class ReferenceRecommendation(BaseModel):
    """An optional unscheduled place, never a booking or committed expense."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    place_name: str = Field(min_length=1, max_length=200)
    source_place_id: str | None = Field(default=None, min_length=1, max_length=256)
    reason: str = Field(min_length=1, max_length=240)
    associated_day: date | None = None
    area: str | None = Field(default=None, min_length=1, max_length=160)
    uncertainty: str | None = Field(default=None, min_length=1, max_length=240)
    source_ref: str | None = Field(default=None, min_length=1, max_length=256)


class ItineraryDay(BaseModel):
    """An ordered collection of activities for one date."""

    model_config = ConfigDict(extra="forbid")

    date: date
    activities: list[Activity] = Field(default_factory=list)


class Transfer(BaseModel):
    """Application-owned adopted transfer; absent for historical or unbound results."""

    model_config = ConfigDict(extra="forbid", frozen=True)
    from_activity_id: str
    to_activity_id: str
    origin_place_id: str
    destination_place_id: str
    mode: Literal["WALK", "TRANSIT", "DRIVE"]
    mode_source: str
    departure_time: datetime
    arrival_time: datetime | None = None
    provider_duration_seconds: float | None = Field(default=None, ge=0)
    distance_meters: int | None = Field(default=None, ge=0)
    reserve_seconds: float = Field(default=0, ge=0)
    routing_preference: str | None = None
    evidence_refs: tuple[str, ...] = ()
    calculation_basis: str
    validation_state: Literal["PASS", "CONFIRMED", "UNKNOWN"]
    unknowns: tuple[str, ...] = ()


class Itinerary(BaseModel):
    """A structured itinerary shared by all system versions."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    # Missing version marks historical input, not newly generated wire output.
    output_version: Literal["itinerary_1", "itinerary_2"] = "itinerary_1"
    transfers: list[Transfer] = Field(default_factory=list)
    route_diagnostics: list[dict] = Field(default_factory=list)
    reference_recommendations: list[ReferenceRecommendation] = Field(
        default_factory=list, max_length=3
    )
    destination: str = Field(min_length=1)
    start_date: date
    end_date: date
    days: list[ItineraryDay] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_schedule(self) -> "Itinerary":
        """Require unique, ordered itinerary days within the trip range."""

        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")

        day_dates = [day.date for day in self.days]
        if day_dates != sorted(day_dates):
            raise ValueError("itinerary days must be ordered by date")
        if len(day_dates) != len(set(day_dates)):
            raise ValueError("itinerary days must have unique dates")
        if any(day_date < self.start_date or day_date > self.end_date for day_date in day_dates):
            raise ValueError("itinerary days must be within the trip date range")

        activity_ids = [activity.activity_id for day in self.days for activity in day.activities]
        if len(activity_ids) != len(set(activity_ids)):
            raise ValueError("activity_id values must be unique within an itinerary")

        references = self.reference_recommendations
        if any(
            r.associated_day is not None
            and not self.start_date <= r.associated_day <= self.end_date
            for r in references
        ):
            raise ValueError("Recommendation associated_day must be within the trip")
        keys = [r.source_place_id or r.place_name.casefold() for r in references]
        if len(keys) != len(set(keys)):
            raise ValueError("Duplicate reference recommendations")
        scheduled_ids = {
            a.source_place_id
            for d in self.days
            for a in d.activities
            if a.source_place_id is not None
        }
        scheduled_names = {
            a.place_name.casefold()
            for d in self.days
            for a in d.activities
            if a.place_name is not None
        }
        if any(
            (
                r.source_place_id in scheduled_ids
                if r.source_place_id
                else r.place_name.casefold() in scheduled_names
            )
            for r in references
        ):
            raise ValueError("Scheduled venues cannot also be reference recommendations")

        return self
