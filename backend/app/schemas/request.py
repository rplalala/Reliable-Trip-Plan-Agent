"""Shared structured user input and internal trip facts."""

import hashlib
import json
from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Money(BaseModel):
    """A finite non-negative amount with an explicit three-letter currency code."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    amount: Decimal = Field(ge=0, allow_inf_nan=False)
    currency: str = Field(pattern=r"^[A-Z]{3}$")

    @field_validator("amount", mode="before")
    @classmethod
    def reject_boolean_amount(cls, value):
        if isinstance(value, bool):
            raise ValueError("amount must be a number, not a boolean")
        return value


class PlanningRequest(BaseModel):
    """Version-neutral user form; budget is for the entire trip."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    input_version: Literal["planning_request_2"] = "planning_request_2"
    destination: str = Field(min_length=1)
    start_date: date
    end_date: date
    traveler_count: int = Field(ge=1, strict=True)
    budget: Money
    additional_preferences: str = ""
    request_id: UUID | None = None

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def date_input(cls, value):
        if isinstance(value, datetime):
            raise ValueError("trip dates must not contain a time")
        if isinstance(value, date):
            return value
        if not isinstance(value, str):
            raise ValueError("trip dates must use YYYY-MM-DD")
        try:
            parsed = date.fromisoformat(value)
        except ValueError as exc:
            raise ValueError("trip dates must use YYYY-MM-DD") from exc
        if parsed.isoformat() != value:
            raise ValueError("trip dates must use YYYY-MM-DD")
        return parsed

    @field_validator("destination")
    @classmethod
    def nonblank_destination(cls, value):
        if not value.strip():
            raise ValueError("destination must not be blank")
        return value.strip()

    @field_validator("additional_preferences", mode="before")
    @classmethod
    def normalize_empty_preferences(cls, value):
        if value is None or isinstance(value, str) and not value.strip():
            return ""
        return value

    @model_validator(mode="after")
    def valid_boundary(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        if self.additional_preferences:
            from backend.app.runtime.token_counting import count_tokens

            if (
                len(self.additional_preferences) > 24000
                or count_tokens(self.additional_preferences) > 8000
            ):
                raise ValueError("preference_input_overflow")
        return self

    def trip_requirements(self) -> "TravelRequirements":
        return TravelRequirements(
            **self.model_dump(
                include={"destination", "start_date", "end_date", "traveler_count", "budget"}
            )
        )

    def structured_hash(self) -> str:
        fields = self.trip_requirements().model_dump(
            mode="json",
            exclude={
                "required_activities",
                "excluded_activities",
                "preferences",
                "unresolved_fields",
            },
        )
        amount = format(self.budget.amount, "f")
        fields["budget"]["amount"] = amount.rstrip("0").rstrip(".") if "." in amount else amount
        fields["input_version"] = self.input_version
        return hashlib.sha256(
            json.dumps(fields, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()


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
