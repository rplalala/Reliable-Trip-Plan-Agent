"""Offline complete directed baseline routing and chunk-budget regressions."""

import asyncio
from datetime import UTC, date, datetime

import pytest

from backend.app.evidence.models import EvidenceAvailability, RouteElementEvidenceType
from backend.app.integrations.models import RouteMatrixDTO, RouteMatrixRequest
from backend.app.policies.route_matrix_chunking import partition_baseline_origins
from backend.app.policies.transport import select_transport_mode
from backend.app.runtime.budget import ToolBudgetKey, ToolBudgetLimits
from backend.tests.request_fixtures import make_request
from backend.tests.services.test_transport_evidence import (
    PolicyRoutesProvider,
    _place,
    _requirements,
    _service,
)


def _explicit_mode(text: str = "We will walk everywhere in Sydney."):
    return select_transport_mode(make_request(additional_preferences=text), _requirements())


def _places(count: int):
    return [_place(chr(ord("a") + index)) for index in range(count)]


@pytest.mark.parametrize("count", range(1, 17))
def test_every_supported_size_has_complete_stable_directed_grid(count: int) -> None:
    provider = PolicyRoutesProvider()
    service, budget = _service(provider)
    places = list(reversed(_places(count)))
    bundle = asyncio.run(
        service.acquire_routes(places=places, mode=_explicit_mode(), requirements=_requirements())
    )
    baseline = bundle.baseline
    ids = [item.place_id for item in places]
    assert len(baseline.elements) == count * count
    assert [(item.origin_place_id, item.destination_place_id) for item in baseline.elements] == [
        (origin, destination) for origin in ids for destination in ids
    ]
    assert baseline.availability is EvidenceAvailability.AVAILABLE
    assert all(
        item.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
        for item in baseline.elements
    )
    assert all(
        len(request.origins) * len(request.destinations) <= 64 for request in provider.requests
    )
    assert all(
        [item.place_id for item in request.destinations] == ids for request in provider.requests
    )
    assert (
        budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS.value]["used"]
        == count * count
    )
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS.value]["used"] == len(
        provider.requests
    )
    assert budget.summary()[ToolBudgetKey.ROUTE_MATRIX_ELEMENTS.value]["used"] == 0


@pytest.mark.parametrize(
    ("count", "expected_origins", "expected_elements"),
    [(8, [8], [64]), (9, [7, 2], [63, 18]), (16, [4, 4, 4, 4], [64, 64, 64, 64])],
)
def test_representative_chunk_shapes(
    count: int, expected_origins: list[int], expected_elements: list[int]
) -> None:
    provider = PolicyRoutesProvider()
    service, _ = _service(provider)
    asyncio.run(
        service.acquire_routes(
            places=_places(count), mode=_explicit_mode(), requirements=_requirements()
        )
    )
    assert [len(request.origins) for request in provider.requests] == expected_origins
    assert [
        len(request.origins) * len(request.destinations) for request in provider.requests
    ] == expected_elements
    assert [item.place_id for request in provider.requests for item in request.origins] == [
        item.place_id for item in _places(count)
    ]


def test_empty_input_returns_unavailable_without_dispatch() -> None:
    provider = PolicyRoutesProvider()
    service, budget = _service(provider)
    bundle = asyncio.run(
        service.acquire_routes(places=[], mode=_explicit_mode(), requirements=_requirements())
    )
    assert provider.requests == []
    assert bundle.baseline.availability is EvidenceAvailability.UNAVAILABLE
    assert bundle.baseline.elements == []
    assert bundle.alternatives == []
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS.value]["used"] == 0
    assert partition_baseline_origins([], per_request_element_limit=64) == ()


class ScrambledRoutesProvider(PolicyRoutesProvider):
    async def compute_route_matrix(self, request: RouteMatrixRequest) -> RouteMatrixDTO:
        result = await super().compute_route_matrix(request)
        return result.model_copy(update={"elements": list(reversed(result.elements))})


def test_out_of_order_chunk_local_indices_map_to_global_place_ids() -> None:
    provider = ScrambledRoutesProvider()
    service, _ = _service(provider)
    places = _places(9)
    baseline = asyncio.run(
        service.acquire_routes(places=places, mode=_explicit_mode(), requirements=_requirements())
    ).baseline
    assert len(provider.requests) == 2
    assert provider.requests[1].origins[0].place_id == "h"
    assert baseline.elements[7 * 9].origin_place_id == "h"
    assert baseline.elements[7 * 9].destination_place_id == "a"
    assert baseline.elements[7 * 9].availability is EvidenceAvailability.AVAILABLE


class FailedSecondChunkProvider(PolicyRoutesProvider):
    async def compute_route_matrix(self, request: RouteMatrixRequest) -> RouteMatrixDTO:
        if request.origins[0].place_id == "h":
            self.requests.append(request)
            raise RuntimeError("chunk unavailable")
        return await super().compute_route_matrix(request)


def test_failed_chunk_preserves_successes_and_consumes_dispatched_budget() -> None:
    provider = FailedSecondChunkProvider()
    service, budget = _service(provider)
    baseline = asyncio.run(
        service.acquire_routes(
            places=_places(9), mode=_explicit_mode(), requirements=_requirements()
        )
    ).baseline
    assert baseline.availability is EvidenceAvailability.PARTIAL
    assert len(baseline.elements) == 81
    assert (
        sum(item.availability is EvidenceAvailability.AVAILABLE for item in baseline.elements) == 63
    )
    failed = baseline.elements[7 * 9]
    assert failed.evidence_type is RouteElementEvidenceType.NOT_OBSERVED
    assert failed.duration_seconds is None
    assert "RuntimeError" in failed.unavailable_reason
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS.value]["used"] == 81
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS.value]["used"] == 2


def test_provider_route_not_found_differs_from_unobserved_retrieval_failure() -> None:
    provider = PolicyRoutesProvider(walk_values={("a", "b"): (None, None, "ROUTE_NOT_FOUND")})
    service, _ = _service(provider)
    baseline = asyncio.run(
        service.acquire_routes(
            places=_places(2), mode=_explicit_mode(), requirements=_requirements()
        )
    ).baseline
    pair = baseline.elements[1]
    assert pair.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
    assert pair.condition == "ROUTE_NOT_FOUND"
    assert pair.unavailable_reason == "ROUTE_NOT_FOUND"


class MalformedRoutesProvider(PolicyRoutesProvider):
    async def compute_route_matrix(self, request: RouteMatrixRequest) -> RouteMatrixDTO:
        self.requests.append(request)
        return RouteMatrixDTO(
            elements=[
                {
                    "originIndex": 1,
                    "destinationIndex": 0,
                    "condition": "ROUTE_EXISTS",
                    "duration": "600s",
                },
                {
                    "originIndex": 1,
                    "destinationIndex": 0,
                    "condition": "ROUTE_EXISTS",
                    "duration": "700s",
                },
                {
                    "originIndex": 0,
                    "destinationIndex": 1,
                    "condition": "ROUTE_EXISTS",
                    "duration": "500s",
                },
                {"originIndex": 99, "destinationIndex": 0, "condition": "ROUTE_EXISTS"},
                {"originIndex": True, "destinationIndex": 1, "condition": "ROUTE_EXISTS"},
            ],
            retrieved_at="2026-09-11T00:00:00+00:00",
        )


def test_missing_duplicate_out_of_range_and_bool_indices_are_isolated() -> None:
    provider = MalformedRoutesProvider()
    service, _ = _service(provider)
    baseline = asyncio.run(
        service.acquire_routes(
            places=_places(2), mode=_explicit_mode(), requirements=_requirements()
        )
    ).baseline
    pairs = {(item.origin_place_id, item.destination_place_id): item for item in baseline.elements}
    assert len(pairs) == 4
    assert pairs[("a", "b")].duration_seconds == 500
    assert pairs[("a", "b")].availability is EvidenceAvailability.AVAILABLE
    assert pairs[("b", "a")].unavailable_reason == "duplicate_provider_indices"
    assert pairs[("b", "a")].evidence_type is RouteElementEvidenceType.NOT_OBSERVED
    assert pairs[("a", "a")].unavailable_reason == "missing_provider_element"
    assert pairs[("b", "b")].duration_seconds is None


def test_total_element_limit_does_not_dispatch_unaffordable_chunk() -> None:
    provider = PolicyRoutesProvider()
    service, budget = _service(
        provider,
        budget_limits=ToolBudgetLimits(max_baseline_route_matrix_elements=70),
    )
    baseline = asyncio.run(
        service.acquire_routes(
            places=_places(9), mode=_explicit_mode(), requirements=_requirements()
        )
    ).baseline
    assert len(provider.requests) == 1
    assert len(baseline.elements) == 81
    assert baseline.availability is EvidenceAvailability.PARTIAL
    assert baseline.elements[7 * 9].evidence_type is RouteElementEvidenceType.NOT_OBSERVED
    assert "not attempted" in baseline.elements[7 * 9].unavailable_reason
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS.value]["used"] == 63
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS.value]["used"] == 1


def test_unaffordable_first_chunk_does_not_block_smaller_later_chunk() -> None:
    provider = PolicyRoutesProvider()
    service, budget = _service(
        provider, budget_limits=ToolBudgetLimits(max_baseline_route_matrix_elements=80)
    )
    budget.consume(ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS, 30)
    baseline = asyncio.run(
        service.acquire_routes(
            places=_places(9), mode=_explicit_mode(), requirements=_requirements()
        )
    ).baseline
    assert len(baseline.elements) == 81
    assert len(provider.requests) == 1
    assert [item.place_id for item in provider.requests[0].origins] == ["h", "i"]
    assert baseline.elements[0].evidence_type is RouteElementEvidenceType.NOT_OBSERVED
    assert baseline.elements[7 * 9].availability is EvidenceAvailability.AVAILABLE
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS.value]["used"] == 48
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS.value]["used"] == 1


def test_call_limit_is_atomic_with_element_budget_and_retains_grid() -> None:
    provider = PolicyRoutesProvider()
    service, budget = _service(
        provider,
        budget_limits=ToolBudgetLimits(max_baseline_route_matrix_calls=1),
    )
    baseline = asyncio.run(
        service.acquire_routes(
            places=_places(9), mode=_explicit_mode(), requirements=_requirements()
        )
    ).baseline
    assert len(provider.requests) == 1
    assert len(baseline.elements) == 81
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS.value]["used"] == 63
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS.value]["used"] == 1


def test_per_request_limit_below_one_full_row_does_not_truncate_selected_pois() -> None:
    provider = PolicyRoutesProvider()
    service, budget = _service(
        provider,
        budget_limits=ToolBudgetLimits(max_baseline_route_matrix_elements_per_request=8),
    )
    baseline = asyncio.run(
        service.acquire_routes(
            places=_places(9), mode=_explicit_mode(), requirements=_requirements()
        )
    ).baseline
    assert len(baseline.elements) == 81
    assert baseline.availability is EvidenceAvailability.UNAVAILABLE
    assert all(
        item.evidence_type is RouteElementEvidenceType.NOT_OBSERVED for item in baseline.elements
    )
    assert provider.requests == []
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS.value]["used"] == 0


def test_budget_unattempted_not_cached_and_later_cached_key_still_works() -> None:
    provider = PolicyRoutesProvider()
    service, budget = _service(
        provider,
        budget_limits=ToolBudgetLimits(max_baseline_route_matrix_calls=1),
    )

    async def scenario():
        first = await service.acquire_routes(
            places=_places(2), mode=_explicit_mode(), requirements=_requirements()
        )
        reversed_places = list(reversed(_places(2)))
        failed = await service.acquire_routes(
            places=reversed_places, mode=_explicit_mode(), requirements=_requirements()
        )
        again_failed = await service.acquire_routes(
            places=reversed_places, mode=_explicit_mode(), requirements=_requirements()
        )
        cached = await service.acquire_routes(
            places=_places(2), mode=_explicit_mode(), requirements=_requirements()
        )
        return first, failed, again_failed, cached

    first, failed, again_failed, cached = asyncio.run(scenario())
    assert len(provider.requests) == 1
    assert first.baseline.availability is EvidenceAvailability.AVAILABLE
    assert failed.baseline.availability is EvidenceAvailability.UNAVAILABLE
    assert again_failed.baseline.availability is EvidenceAvailability.UNAVAILABLE
    assert cached.baseline.availability is EvidenceAvailability.AVAILABLE
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS.value]["used"] == 4
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS.value]["used"] == 1


def test_route_cache_key_tracks_order_mode_departure_options_and_mask() -> None:
    from backend.app.integrations.models import LatLng, RouteWaypoint
    from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService

    a = RouteWaypoint(place_id="a", location=LatLng(latitude=-33.87, longitude=151.2))
    b = RouteWaypoint(place_id="b", location=LatLng(latitude=-33.86, longitude=151.21))
    base = RouteMatrixRequest(
        origins=[a, b], destinations=[a, b], travel_mode="WALK", field_mask="duration"
    )
    keys = {
        V1EvidenceAcquisitionService._route_cache_key(base),
        V1EvidenceAcquisitionService._route_cache_key(base.model_copy(update={"origins": [b, a]})),
        V1EvidenceAcquisitionService._route_cache_key(
            base.model_copy(update={"destinations": [b, a]})
        ),
        V1EvidenceAcquisitionService._route_cache_key(
            base.model_copy(update={"travel_mode": "DRIVE"})
        ),
        V1EvidenceAcquisitionService._route_cache_key(
            base.model_copy(update={"departure_time": datetime(2026, 9, 12, tzinfo=UTC)})
        ),
        V1EvidenceAcquisitionService._route_cache_key(
            base.model_copy(update={"field_mask": "distanceMeters"})
        ),
        V1EvidenceAcquisitionService._route_cache_key(
            base.model_copy(update={"routing_preference": "TRAFFIC_UNAWARE"})
        ),
    }
    assert len(keys) == 7


def test_default_walk_transit_trigger_runs_after_merged_chunks() -> None:
    provider = PolicyRoutesProvider(walk_values={("h", "a"): (4000, 3000, "ROUTE_EXISTS")})
    service, budget = _service(provider)
    default_mode = select_transport_mode(
        make_request(additional_preferences="Plan Sydney."), _requirements()
    )
    bundle = asyncio.run(
        service.acquire_routes(places=_places(9), mode=default_mode, requirements=_requirements())
    )
    assert [request.travel_mode for request in provider.requests] == ["WALK", "WALK", "TRANSIT"]
    assert [(item.place_id_a, item.place_id_b) for item in bundle.non_walkable_pairs] == [
        ("a", "h")
    ]
    assert len(bundle.baseline.elements) == 81
    observed, mirrored = bundle.alternatives[0].elements
    assert observed.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
    assert (observed.origin_place_id, observed.destination_place_id) == ("a", "h")
    assert mirrored.evidence_type is RouteElementEvidenceType.MIRRORED_REVERSE_ESTIMATE
    assert (mirrored.origin_place_id, mirrored.destination_place_id) == ("h", "a")
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS.value]["used"] == 81
    assert budget.summary()[ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS.value]["used"] == 2
    assert budget.summary()[ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS.value]["used"] == 1
    assert budget.summary()[ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS.value]["used"] == 1


def test_explicit_transit_uses_chunked_baseline_without_alternatives() -> None:
    provider = PolicyRoutesProvider()
    service, _ = _service(provider)
    mode = select_transport_mode(
        make_request(additional_preferences="We will use public transit in Sydney."),
        _requirements(),
    )
    bundle = asyncio.run(
        service.acquire_routes(
            places=_places(9), mode=mode, requirements=_requirements(date(2026, 9, 12))
        )
    )
    assert len(provider.requests) == 2
    assert all(request.travel_mode == "TRANSIT" for request in provider.requests)
    assert all(request.departure_time is not None for request in provider.requests)
    assert bundle.alternatives == []
    assert len(bundle.baseline.elements) == 81
