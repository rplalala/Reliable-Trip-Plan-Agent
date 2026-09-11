"""Thin HTTP contracts for product and developer planning."""

from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import Money, TravelRequirements


class ProductPlanningRequest(BaseModel):
    """Validated structured input accepted by the product planner."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    destination: str = Field(min_length=1)
    start_date: date
    end_date: date
    traveler_count: int = Field(ge=1)
    budget: Money | None = None
    additional_preferences: str | None = Field(default=None, min_length=1)
    reference_date: date | None = None

    @model_validator(mode="after")
    def validate_date_range(self) -> "ProductPlanningRequest":
        """Reject a Product trip that ends before it starts."""

        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class CompletedPlanningResponse(BaseModel):
    """A completed product planning result without research metadata."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["completed"] = "completed"
    requirements: TravelRequirements
    itinerary: Itinerary


class NeedsClarificationResponse(BaseModel):
    """Extracted requirements that need the user to revise their request."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["needs_clarification"] = "needs_clarification"
    requirements: TravelRequirements


ProductPlanningResponse = Annotated[
    CompletedPlanningResponse | NeedsClarificationResponse,
    Field(discriminator="status"),
]


class DeveloperPlanningRequest(BaseModel):
    """Version-aware input accepted by the local developer planner."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    version: Literal["v0"]
    request_text: str = Field(min_length=1)
    reference_date: date | None = None
