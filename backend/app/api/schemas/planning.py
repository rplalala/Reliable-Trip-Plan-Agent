"""Thin HTTP contracts for product and developer planning."""

from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import PlanningRequest, TravelRequirements

ProductPlanningRequest = PlanningRequest


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
    issues: dict[str, object] = Field(default_factory=dict)


ProductPlanningResponse = Annotated[
    CompletedPlanningResponse | NeedsClarificationResponse,
    Field(discriminator="status"),
]


class DeveloperPlanningRequest(BaseModel):
    """Engine selection is separate from the shared user form."""

    model_config = ConfigDict(extra="forbid")
    version: Literal["v0"]
    request: PlanningRequest
    reference_date: date | None = None
