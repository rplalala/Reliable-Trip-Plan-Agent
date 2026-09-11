"""Schemas for raw requests and extracted travel requirements."""

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Money(BaseModel):
    """A non-negative monetary amount in an ISO 4217 currency."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    amount: Decimal = Field(ge=0)
    currency: str = Field(pattern=r"^[A-Z]{3}$")


class TravelRequest(BaseModel):
    """The raw user request accepted by every system version."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    request_text: str = Field(min_length=1)
    request_id: UUID | None = None


class TravelRequirements(BaseModel):
    """Provider-independent requirements extracted from a user request."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    destination: str | None = Field(default=None, min_length=1)
    start_date: date | None = None
    end_date: date | None = None
    traveler_count: int | None = Field(default=None, ge=1)
    budget: Money | None = None
    required_activities: list[str] = Field(default_factory=list)
    excluded_activities: list[str] = Field(default_factory=list)
    preferences: list[str] = Field(default_factory=list)
    unresolved_fields: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_date_range(self) -> "TravelRequirements":
        """Reject an end date that precedes the start date."""

        if self.start_date is not None and self.end_date is not None:
            if self.end_date < self.start_date:
                raise ValueError("end_date must be on or after start_date")
        return self
