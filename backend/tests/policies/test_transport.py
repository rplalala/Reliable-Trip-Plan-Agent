"""Tests for deterministic single-mode routing policy."""

from backend.app.policies.transport import TravelMode, select_transport_mode
from backend.app.schemas.request import TravelRequest, TravelRequirements


def test_transport_policy_defaults_to_walking_for_poi_transfer_grouping() -> None:
    decision = select_transport_mode(
        TravelRequest(request_text="Plan Sydney with not too much walking."),
        TravelRequirements(preferences=["not too much walking"]),
    )

    assert decision.travel_mode is TravelMode.WALK
    assert decision.reason == "default_pedestrian_transfer_for_poi_grouping"
    assert decision.routing_preference is None


def test_transport_policy_honors_explicit_drive_and_uses_stable_preference() -> None:
    decision = select_transport_mode(
        TravelRequest(request_text="We plan to drive around Sydney."),
        TravelRequirements(),
    )

    assert decision.travel_mode is TravelMode.DRIVE
    assert decision.routing_preference == "TRAFFIC_UNAWARE"


def test_transport_policy_uses_exact_extracted_public_transport_preference() -> None:
    decision = select_transport_mode(
        TravelRequest(request_text="Plan Sydney."),
        TravelRequirements(preferences=["public transport"]),
    )

    assert decision.travel_mode is TravelMode.TRANSIT
    assert decision.routing_preference is None
