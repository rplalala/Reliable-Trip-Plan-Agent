"""State contract owned exclusively by the V0 graph."""

from datetime import date
from typing import NotRequired, TypedDict

from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import TravelRequest, TravelRequirements


class V0State(TypedDict):
    """Minimal state for the two-stage V0 workflow."""

    request: TravelRequest
    reference_date: date
    requirements: NotRequired[TravelRequirements]
    itinerary: NotRequired[Itinerary]
