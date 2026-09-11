"""Request-scoped state owned exclusively by the V1 graph."""

from datetime import date
from typing import NotRequired, TypedDict

from backend.app.evidence.models import (
    DestinationContext,
    PlaceCandidate,
    PlaceEvidence,
    RouteEvidence,
    WeatherEvidence,
)
from backend.app.policies.transport import TransportModeDecision
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import TravelRequest, TravelRequirements


class V1State(TypedDict):
    """Typed normalized state for the explicit V1-A workflow."""

    request: TravelRequest
    reference_date: date
    requirements: NotRequired[TravelRequirements]
    destination_context: NotRequired[DestinationContext]
    candidates: NotRequired[list[PlaceCandidate]]
    shortlist: NotRequired[list[PlaceCandidate]]
    place_evidence: NotRequired[list[PlaceEvidence]]
    weather_evidence: NotRequired[WeatherEvidence]
    transport_mode: NotRequired[TransportModeDecision]
    route_evidence: NotRequired[RouteEvidence]
    itinerary: NotRequired[Itinerary]
