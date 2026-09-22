"""Offline tests for bounded two-stage V1-A route evidence acquisition."""

import asyncio
from datetime import UTC, date, datetime
from uuid import UUID

import pytest

from backend.app.evidence.models import (
    EvidenceAvailability,
    PlaceEvidence,
    RouteElementEvidenceType,
)
from backend.app.integrations.models import RouteMatrixDTO, RouteMatrixRequest
from backend.app.observability.run_trace import NullRunTracer
from backend.app.policies.transport import select_transport_mode
from backend.app.runtime.budget import ToolBudget, ToolBudgetLimits
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.request import TravelRequirements
from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v1.fakes import FakePlacesProvider, FakeWeatherProvider

RUN_ID = UUID("00000000-0000-0000-0000-000000000001")
RouteValue = tuple[int | None, int | None, str]


class RecordingTracer(NullRunTracer):
    def __init__(self) -> None:
        super().__init__(RUN_ID)
        self.events: list[tuple[str, object | None]] = []

    def event(self, event_type: str, payload: object | None = None) -> None:
        self.events.append((event_type, payload))


class PolicyRoutesProvider:
    def __init__(
        self,
        *,
        walk_values: dict[tuple[str, str], RouteValue] | None = None,
        transit_values: dict[tuple[str, str], RouteValue] | None = None,
        fail_walk: bool = False,
        fail_transit: bool = False,
    ) -> None:
        self.requests: list[RouteMatrixRequest] = []
        self.walk_values = walk_values or {}
        self.transit_values = transit_values or {}
        self.fail_walk = fail_walk
        self.fail_transit = fail_transit

    async def compute_route_matrix(self, request: RouteMatrixRequest) -> RouteMatrixDTO:
        self.requests.append(request)
        if request.travel_mode == "WALK" and self.fail_walk:
            raise RuntimeError("walk unavailable")
        if request.travel_mode == "TRANSIT" and self.fail_transit:
            raise RuntimeError("transit unavailable")
        values = self.walk_values if request.travel_mode == "WALK" else self.transit_values
        elements: list[dict[str, object]] = []
        for origin_index, origin in enumerate(request.origins):
            for destination_index, destination in enumerate(request.destinations):
                default = (
                    (0, 0, "ROUTE_EXISTS")
                    if origin.place_id == destination.place_id
                    else (1000, 600, "ROUTE_EXISTS")
                )
                distance, duration, condition = values.get(
                    (origin.place_id, destination.place_id), default
                )
                element: dict[str, object] = {
                    "originIndex": origin_index,
                    "destinationIndex": destination_index,
                    "condition": condition,
                    "status": {} if condition == "ROUTE_EXISTS" else {"code": 5},
                }
                if distance is not None:
                    element["distanceMeters"] = distance
                if duration is not None:
                    element["duration"] = f"{duration}s"
                elements.append(element)
        return RouteMatrixDTO(
            elements=elements,
            retrieved_at="2026-09-11T00:00:00+00:00",
        )


def _place(place_id: str, *, timezone_id: str | None = "Australia/Sydney") -> PlaceEvidence:
    index = ord(place_id[0]) - ord("a")
    return PlaceEvidence(
        place_id=place_id,
        name=f"Place {place_id}",
        latitude=-33.86 - index * 0.001,
        longitude=151.20 + index * 0.001,
        timezone_id=timezone_id,
        availability=EvidenceAvailability.AVAILABLE,
        retrieved_at=datetime(2026, 9, 11, tzinfo=UTC),
        source_ref=f"test:{place_id}",
    )


def _requirements(start_date: date = date(2026, 9, 12)) -> TravelRequirements:
    return TravelRequirements(
        destination="Sydney",
        start_date=start_date,
        end_date=start_date,
    )


def _service(
    routes: PolicyRoutesProvider,
    *,
    budget_limits: ToolBudgetLimits | None = None,
    tracer: RecordingTracer | None = None,
) -> tuple[V1EvidenceAcquisitionService, ToolBudget]:
    budget = ToolBudget(budget_limits)
    return (
        V1EvidenceAcquisitionService(
            places_provider=FakePlacesProvider(),
            weather_provider=FakeWeatherProvider(),
            routes_provider=routes,
            budget=budget,
            cache=RequestCache(),
            tracer=tracer or RecordingTracer(),
        ),
        budget,
    )


def _default_mode():
    return select_transport_mode(
        make_request(additional_preferences="Plan Sydney."), _requirements()
    )


def test_default_walk_uses_sparse_transit_with_separate_bounded_budget_and_trace() -> None:
    walk_values = {
        ("a", "b"): (12000, 100, "ROUTE_EXISTS"),
        ("a", "c"): (11000, 100, "ROUTE_EXISTS"),
        ("b", "a"): (10000, 100, "ROUTE_EXISTS"),
        ("b", "c"): (9000, 100, "ROUTE_EXISTS"),
        ("c", "a"): (8000, 100, "ROUTE_EXISTS"),
        ("c", "b"): (7000, 100, "ROUTE_EXISTS"),
        ("d", "a"): (6000, 100, "ROUTE_EXISTS"),
        ("d", "b"): (5000, 100, "ROUTE_EXISTS"),
        ("e", "a"): (4000, 100, "ROUTE_EXISTS"),
    }
    routes = PolicyRoutesProvider(walk_values=walk_values)
    tracer = RecordingTracer()
    service, budget = _service(routes, tracer=tracer)

    bundle = asyncio.run(
        service.acquire_routes(
            places=[_place(item) for item in "abcde"],
            mode=_default_mode(),
            requirements=_requirements(),
        )
    )

    assert [request.travel_mode for request in routes.requests] == [
        "WALK",
        "TRANSIT",
        "TRANSIT",
    ]
    assert sum(len(request.destinations) for request in routes.requests[1:]) == 6
    assert len(bundle.non_walkable_pairs) == 6
    assert len(bundle.alternatives) == 2
    assert all(len(request.origins) == 1 for request in routes.requests[1:])
    assert all(
        request.departure_time == datetime.fromisoformat("2026-09-12T12:00:00+10:00")
        for request in routes.requests[1:]
    )
    summary = budget.summary()
    assert summary["baseline_route_matrix_elements"]["used"] == 25
    assert summary["baseline_route_matrix_calls"]["used"] == 1
    assert summary["route_matrix_elements"]["used"] == 0
    assert summary["alternative_route_pairs"]["used"] == 6
    assert summary["alternative_route_matrix_calls"]["used"] == 2
    trigger_payload = next(
        payload
        for event, payload in tracer.events
        if event == "route_alternative_trigger_evaluated"
    )
    assert isinstance(trigger_payload, dict)
    assert len(trigger_payload["detected_directed_walk_triggers"]) == 9
    assert len(trigger_payload["collapsed_logical_pairs"]) == 6
    assert len(trigger_payload["selected_logical_pairs"]) == 6
    assert len(trigger_payload["budget_truncated_logical_pairs"]) == 0
    assert trigger_payload["canonical_directions"] == [
        {"origin_place_id": "a", "destination_place_id": "b"},
        {"origin_place_id": "a", "destination_place_id": "c"},
        {"origin_place_id": "b", "destination_place_id": "c"},
        {"origin_place_id": "a", "destination_place_id": "d"},
        {"origin_place_id": "b", "destination_place_id": "d"},
        {"origin_place_id": "a", "destination_place_id": "e"},
    ]
    assert trigger_payload["representative_departure_time"] == datetime.fromisoformat(
        "2026-09-12T12:00:00+10:00"
    )


def test_symmetric_walk_triggers_use_one_canonical_element_and_mirrored_reverse() -> None:
    routes = PolicyRoutesProvider(
        walk_values={
            ("a", "b"): (4000, 3000, "ROUTE_EXISTS"),
            ("b", "a"): (5000, 3600, "ROUTE_EXISTS"),
        }
    )
    tracer = RecordingTracer()
    service, budget = _service(routes, tracer=tracer)

    bundle = asyncio.run(
        service.acquire_routes(
            places=[_place("b"), _place("a")],
            mode=_default_mode(),
            requirements=_requirements(),
        )
    )

    assert len(bundle.non_walkable_pairs) == 1
    assert bundle.non_walkable_pairs[0].place_id_a == "a"
    assert bundle.non_walkable_pairs[0].place_id_b == "b"
    assert len(routes.requests) == 2
    assert [item.place_id for item in routes.requests[1].origins] == ["a"]
    assert [item.place_id for item in routes.requests[1].destinations] == ["b"]
    observed, mirrored = bundle.alternatives[0].elements
    assert observed.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
    assert (observed.origin_place_id, observed.destination_place_id) == ("a", "b")
    assert mirrored.evidence_type is RouteElementEvidenceType.MIRRORED_REVERSE_ESTIMATE
    assert (mirrored.origin_place_id, mirrored.destination_place_id) == ("b", "a")
    assert mirrored.duration_seconds == observed.duration_seconds
    assert mirrored.distance_meters is None
    assert mirrored.status is None
    assert mirrored.condition is None
    assert mirrored.derived_from_origin_place_id == "a"
    assert mirrored.derived_from_destination_place_id == "b"
    assert budget.summary()["alternative_route_pairs"]["used"] == 1
    assert budget.summary()["alternative_route_matrix_calls"]["used"] == 1
    completed = next(
        payload for event, payload in tracer.events if event == "route_alternative_completed"
    )
    assert completed["provider_observed_element_count"] == 1
    assert completed["mirrored_reverse_estimate_count"] == 1
    assert completed["billable_matrix_element_count"] == 1


@pytest.mark.parametrize(
    ("request_text", "expected_mode"),
    [
        ("We will walk everywhere in Sydney.", "WALK"),
        ("We prefer to drive in Sydney.", "DRIVE"),
        ("We will travel by public transit in Sydney.", "TRANSIT"),
        ("We will get around by bicycle in Sydney.", "BICYCLE"),
    ],
)
def test_explicit_supported_mode_uses_one_matrix_without_fan_out(
    request_text: str, expected_mode: str
) -> None:
    routes = PolicyRoutesProvider(walk_values={("a", "b"): (9000, 9000, "ROUTE_EXISTS")})
    service, budget = _service(routes)
    mode = select_transport_mode(make_request(additional_preferences=request_text), _requirements())

    bundle = asyncio.run(
        service.acquire_routes(
            places=[_place("a"), _place("b")],
            mode=mode,
            requirements=_requirements(),
        )
    )

    assert len(routes.requests) == 1
    assert routes.requests[0].travel_mode == expected_mode
    assert bundle.alternatives == []
    assert bundle.non_walkable_pairs == []
    assert budget.summary()["alternative_route_pairs"]["used"] == 0
    assert budget.summary()["alternative_route_matrix_calls"]["used"] == 0
    if expected_mode == "TRANSIT":
        assert routes.requests[0].departure_time == datetime.fromisoformat(
            "2026-09-12T12:00:00+10:00"
        )
    if expected_mode == "DRIVE":
        assert routes.requests[0].routing_preference == "TRAFFIC_UNAWARE"


def test_alternative_element_budget_reduces_sparse_transit_selection() -> None:
    routes = PolicyRoutesProvider(
        walk_values={
            ("a", "b"): (6000, 100, "ROUTE_EXISTS"),
            ("a", "c"): (5000, 100, "ROUTE_EXISTS"),
            ("a", "d"): (4000, 100, "ROUTE_EXISTS"),
        }
    )
    service, budget = _service(
        routes,
        budget_limits=ToolBudgetLimits(max_alternative_route_pairs=2),
    )

    bundle = asyncio.run(
        service.acquire_routes(
            places=[_place(item) for item in "abcd"],
            mode=_default_mode(),
            requirements=_requirements(),
        )
    )

    assert len(bundle.non_walkable_pairs) == 3
    assert len(routes.requests) == 2
    assert len(routes.requests[1].destinations) == 2
    assert budget.summary()["alternative_route_pairs"]["used"] == 2


def test_missing_timezone_marks_alternative_unavailable_without_provider_now() -> None:
    routes = PolicyRoutesProvider(walk_values={("a", "b"): (4000, 100, "ROUTE_EXISTS")})
    tracer = RecordingTracer()
    service, budget = _service(routes, tracer=tracer)

    bundle = asyncio.run(
        service.acquire_routes(
            places=[_place("a", timezone_id=None), _place("b", timezone_id="Invalid/Zone")],
            mode=_default_mode(),
            requirements=_requirements(),
        )
    )

    assert len(routes.requests) == 1
    assert len(bundle.alternatives) == 1
    assert bundle.alternatives[0].availability is EvidenceAvailability.UNAVAILABLE
    assert bundle.alternatives[0].representative_departure_time is None
    assert "no valid destination timezone" in bundle.alternatives[0].unavailable_reason
    assert budget.summary()["alternative_route_pairs"]["used"] == 0
    assert budget.summary()["alternative_route_matrix_calls"]["used"] == 0
    completed = [
        payload for event, payload in tracer.events if event == "route_alternative_completed"
    ]
    assert completed[0]["availability"] == "unavailable"


def test_provider_wide_walk_failure_does_not_fan_out() -> None:
    routes = PolicyRoutesProvider(fail_walk=True)
    service, _ = _service(routes)

    bundle = asyncio.run(
        service.acquire_routes(
            places=[_place("a"), _place("b")],
            mode=_default_mode(),
            requirements=_requirements(),
        )
    )

    assert len(routes.requests) == 1
    assert bundle.baseline.availability is EvidenceAvailability.UNAVAILABLE
    assert bundle.alternatives == []


@pytest.mark.parametrize("fail_transit", [False, True])
def test_partial_or_unavailable_transit_is_preserved(fail_transit: bool) -> None:
    routes = PolicyRoutesProvider(
        walk_values={
            ("a", "b"): (5000, 100, "ROUTE_EXISTS"),
            ("a", "c"): (4000, 100, "ROUTE_EXISTS"),
        },
        transit_values={("a", "c"): (None, None, "ROUTE_NOT_FOUND")},
        fail_transit=fail_transit,
    )
    service, _ = _service(routes)

    bundle = asyncio.run(
        service.acquire_routes(
            places=[_place(item) for item in "abc"],
            mode=_default_mode(),
            requirements=_requirements(),
        )
    )

    expected = EvidenceAvailability.UNAVAILABLE if fail_transit else EvidenceAvailability.PARTIAL
    assert bundle.alternatives[0].availability is expected
    if fail_transit:
        assert bundle.alternatives[0].elements == []
    else:
        elements = bundle.alternatives[0].elements
        assert len(elements) == 3
        observed = [
            item
            for item in elements
            if item.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
        ]
        mirrored = [
            item
            for item in elements
            if item.evidence_type is RouteElementEvidenceType.MIRRORED_REVERSE_ESTIMATE
        ]
        assert len(observed) == 2
        assert len(mirrored) == 1
        assert mirrored[0].origin_place_id == "b"
        assert mirrored[0].destination_place_id == "a"
        assert mirrored[0].duration_seconds == observed[0].duration_seconds
        assert mirrored[0].distance_meters is None
        assert mirrored[0].status is None
        assert mirrored[0].condition is None
        assert mirrored[0].derived_from_origin_place_id == "a"
        assert mirrored[0].derived_from_destination_place_id == "b"


def test_route_cache_deduplicates_same_departure_time_and_separates_new_date() -> None:
    routes = PolicyRoutesProvider(walk_values={("a", "b"): (4000, 100, "ROUTE_EXISTS")})
    service, budget = _service(routes)

    async def scenario() -> None:
        for start_date in (date(2026, 9, 12), date(2026, 9, 12), date(2026, 9, 13)):
            await service.acquire_routes(
                places=[_place("a"), _place("b")],
                mode=_default_mode(),
                requirements=_requirements(start_date),
            )

    asyncio.run(scenario())

    assert [request.travel_mode for request in routes.requests] == [
        "WALK",
        "TRANSIT",
        "TRANSIT",
    ]
    assert routes.requests[1].departure_time != routes.requests[2].departure_time
    assert budget.summary()["baseline_route_matrix_elements"]["used"] == 4
    assert budget.summary()["baseline_route_matrix_calls"]["used"] == 1
    assert budget.summary()["alternative_route_pairs"]["used"] == 2
    assert budget.summary()["alternative_route_matrix_calls"]["used"] == 2
