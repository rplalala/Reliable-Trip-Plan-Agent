"""Provider-independent structured itinerary schemas."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.schemas.request import Money


class Activity(BaseModel):
    """A scheduled itinerary activity."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    activity_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    place_name: str | None = Field(default=None, min_length=1)
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


class ItineraryDay(BaseModel):
    """An ordered collection of activities for one date."""

    model_config = ConfigDict(extra="forbid")

    date: date
    activities: list[Activity] = Field(default_factory=list)


class Itinerary(BaseModel):
    """A structured itinerary shared by all system versions."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

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

        activity_ids = [
            activity.activity_id for day in self.days for activity in day.activities
        ]
        if len(activity_ids) != len(set(activity_ids)):
            raise ValueError("activity_id values must be unique within an itinerary")

        return self
