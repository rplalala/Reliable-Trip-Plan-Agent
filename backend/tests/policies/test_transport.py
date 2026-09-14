"""Tests for deterministic bounded routing policy."""

from datetime import UTC, datetime

from backend.app.evidence.models import (
    EvidenceAvailability,
    NonWalkablePairEvidence,
    NonWalkableTrigger,
    RouteElementEvidence,
    RouteEvidence,
)
from backend.app.policies.transport import (
    TravelMode,
    find_non_walkable_pairs,
    select_alternative_route_pairs,
    select_transport_mode,
)
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


def test_non_walkable_policy_uses_strict_boundaries_and_excludes_same_place() -> None:
    evidence = _walk_evidence(
        [
            _element("a", "b", distance=3000, duration=2700),
            _element("a", "c", distance=3001, duration=1),
            _element("a", "d", distance=1, duration=2701),
            _element("a", "e", condition="ROUTE_NOT_FOUND"),
            _element("a", "a", distance=9000, duration=9000),
        ]
    )

    pairs = find_non_walkable_pairs(evidence)

    assert {(item.place_id_a, item.place_id_b) for item in pairs} == {
        ("a", "c"),
        ("a", "d"),
        ("a", "e"),
    }
    assert pairs[0].trigger_reasons == [NonWalkableTrigger.WALK_ROUTE_NOT_FOUND]


def test_non_walkable_pairs_have_stable_severity_order_and_bounded_selection() -> None:
    evidence = _walk_evidence(
        [
            _element("e", "z", distance=8000, duration=100),
            _element("a", "z", distance=7000, duration=100),
            _element("b", "z", distance=6000, duration=100),
            _element("c", "z", distance=5000, duration=100),
            _element("d", "z", distance=4000, duration=100),
            _element("a", "y", condition="ROUTE_NOT_FOUND"),
        ]
    )

    pairs = find_non_walkable_pairs(evidence)
    selected, truncated = select_alternative_route_pairs(
        pairs,
        max_pairs=8,
        max_calls=4,
    )

    assert [(item.place_id_a, item.place_id_b) for item in pairs] == [
        ("a", "y"),
        ("e", "z"),
        ("a", "z"),
        ("b", "z"),
        ("c", "z"),
        ("d", "z"),
    ]
    assert [(item.place_id_a, item.place_id_b) for item in selected] == [
        ("a", "y"),
        ("e", "z"),
        ("a", "z"),
        ("b", "z"),
        ("c", "z"),
    ]
    assert [(item.place_id_a, item.place_id_b) for item in truncated] == [
        ("d", "z"),
    ]


def test_logical_pair_ranking_uses_the_more_severe_directed_walk_result() -> None:
    forward = _walk_evidence(
        [
            _element("a", "b", distance=4000, duration=100),
            _element("b", "a", distance=1, duration=9000),
            _element("c", "d", distance=8000, duration=100),
        ]
    )
    reversed_input = _walk_evidence(list(reversed(forward.elements)))

    pairs = find_non_walkable_pairs(forward)

    assert pairs == find_non_walkable_pairs(reversed_input)
    assert [(item.place_id_a, item.place_id_b) for item in pairs] == [
        ("a", "b"),
        ("c", "d"),
    ]
    assert pairs[0].trigger_reasons == [
        NonWalkableTrigger.DISTANCE_THRESHOLD,
        NonWalkableTrigger.DURATION_THRESHOLD,
    ]


def test_alternative_pair_selection_caps_at_top_eight() -> None:
    pairs = [
        NonWalkablePairEvidence(
            place_id_a="a",
            place_id_b=f"destination-{index}",
            trigger_reasons=[NonWalkableTrigger.DISTANCE_THRESHOLD],
        )
        for index in range(10)
    ]

    selected, truncated = select_alternative_route_pairs(
        pairs,
        max_pairs=8,
        max_calls=4,
    )

    assert len(selected) == 8
    assert len(truncated) == 2


def test_alternative_pair_selection_has_no_hidden_cap_below_valid_runtime_budget() -> None:
    pairs = [
        NonWalkablePairEvidence(
            place_id_a="a",
            place_id_b=f"destination-{index}",
            trigger_reasons=[NonWalkableTrigger.DISTANCE_THRESHOLD],
        )
        for index in range(12)
    ]

    selected, truncated = select_alternative_route_pairs(
        pairs,
        max_pairs=12,
        max_calls=1,
    )

    assert len(selected) == 12
    assert truncated == []


def _element(
    origin: str,
    destination: str,
    *,
    distance: int | None = None,
    duration: int | None = None,
    condition: str = "ROUTE_EXISTS",
) -> RouteElementEvidence:
    return RouteElementEvidence(
        origin_place_id=origin,
        destination_place_id=destination,
        condition=condition,
        distance_meters=distance,
        duration_seconds=duration,
        availability=(
            EvidenceAvailability.UNAVAILABLE
            if condition == "ROUTE_NOT_FOUND"
            else EvidenceAvailability.AVAILABLE
        ),
    )


def _walk_evidence(elements: list[RouteElementEvidence]) -> RouteEvidence:
    return RouteEvidence(
        travel_mode="WALK",
        mode_reason="test",
        availability=EvidenceAvailability.AVAILABLE,
        elements=elements,
        retrieved_at=datetime(2026, 9, 11, tzinfo=UTC),
        source_ref="test:routes",
    )
