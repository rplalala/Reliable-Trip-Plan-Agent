"""Request-scoped state owned exclusively by the V1 graph."""

from datetime import date
from typing import NotRequired, TypedDict

from backend.app.evidence.models import (
    DestinationContext,
    PlaceCandidate,
    PlaceEvidence,
    RouteEvidenceBundle,
    WeatherEvidence,
)
from backend.app.policies.poi_selection import SelectionConflict
from backend.app.policies.transport import TransportModeDecision
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.named_place_intent import NamedPlaceIntent
from backend.app.schemas.request import TravelRequest, TravelRequirements
from backend.app.schemas.trip_intent import (
    ExperiencePreferenceIntent,
    PoiInterest,
    RequestedPlaceInformation,
    TransportPreferenceIntent,
)
from backend.app.services.evidence_acquisition import CandidateFunnelResult
from backend.app.services.official_web_integration import OfficialWebIntegrationResult
from backend.app.services.review_selection import ReviewAwareSelectionResult


class V1State(TypedDict):
    """Typed normalized state for the explicit V1-A workflow."""

    request: TravelRequest
    reference_date: date
    requirements: NotRequired[TravelRequirements]
    named_place_intents: NotRequired[tuple[NamedPlaceIntent, ...]]
    requested_place_information: NotRequired[tuple[RequestedPlaceInformation, ...]]
    experience_preferences: NotRequired[tuple[ExperiencePreferenceIntent, ...]]
    transport_preference: NotRequired[TransportPreferenceIntent | None]
    poi_interests: NotRequired[tuple[PoiInterest, ...]]
    destination_context: NotRequired[DestinationContext]
    candidate_funnel: NotRequired[CandidateFunnelResult]
    review_selection: NotRequired[ReviewAwareSelectionResult]
    selected_candidates: NotRequired[list[PlaceCandidate]]
    place_evidence: NotRequired[list[PlaceEvidence]]
    selection_conflicts: NotRequired[tuple[SelectionConflict, ...]]
    weather_evidence: NotRequired[WeatherEvidence]
    transport_mode: NotRequired[TransportModeDecision]
    route_evidence: NotRequired[RouteEvidenceBundle]
    official_web_result: NotRequired[OfficialWebIntegrationResult | None]
    official_planner_evidence: NotRequired[list[dict[str, object]]]
    itinerary: NotRequired[Itinerary]
