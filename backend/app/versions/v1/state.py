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
from backend.app.schemas.generation_diagnostics import GenerationDiagnostics
from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import PlanningRequest, TravelRequirements
from backend.app.schemas.trip_intent import (
    RequestedPlaceInformation,
    TransportPreferenceIntent,
)
from backend.app.services.candidate_acquisition import CandidatePool
from backend.app.services.official_web_integration import OfficialWebIntegrationResult
from backend.app.services.planning_supply_pipeline import PlanningSupplySelection
from backend.app.services.reference_discovery import ReferenceDiscoveryResult


class V1State(TypedDict):
    """Typed normalized state for the explicit V1-A workflow."""

    request: PlanningRequest
    reference_date: date
    interpreted_requirements: NotRequired[InterpretedTripRequirements]
    requirements: NotRequired[TravelRequirements]
    requested_place_information: NotRequired[tuple[RequestedPlaceInformation, ...]]
    transport_preference: NotRequired[TransportPreferenceIntent | None]
    destination_context: NotRequired[DestinationContext]
    candidate_funnel: NotRequired[CandidatePool]
    review_selection: NotRequired[PlanningSupplySelection]
    selected_candidates: NotRequired[list[PlaceCandidate]]
    place_evidence: NotRequired[list[PlaceEvidence]]
    selection_conflicts: NotRequired[tuple[SelectionConflict, ...]]
    weather_evidence: NotRequired[WeatherEvidence]
    transport_mode: NotRequired[TransportModeDecision]
    route_evidence: NotRequired[RouteEvidenceBundle]
    official_web_result: NotRequired[OfficialWebIntegrationResult | None]
    official_planner_evidence: NotRequired[list[dict[str, object]]]
    generation_diagnostics: NotRequired[GenerationDiagnostics]
    itinerary: NotRequired[Itinerary]
    reference_discovery: NotRequired[ReferenceDiscoveryResult]
