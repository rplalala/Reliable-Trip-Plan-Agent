"""State contract owned exclusively by the V0 graph."""

from datetime import date
from typing import NotRequired, TypedDict

from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import PlanningRequest, TravelRequirements


class V0State(TypedDict):
    """Minimal state for the two-stage V0 workflow."""

    request: PlanningRequest
    reference_date: date
    requirements: NotRequired[TravelRequirements]
    itinerary: NotRequired[Itinerary]
    interpreted_requirements: NotRequired[InterpretedTripRequirements]
