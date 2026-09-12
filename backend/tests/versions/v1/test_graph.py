"""Offline integration tests for the explicit V1-A graph."""

import asyncio
from datetime import date
from uuid import UUID

import pytest

from backend.app.integrations.google.places import (
    PLACES_CANDIDATE_FIELD_MASK,
    PLACES_DETAILS_FIELD_MASK,
)
from backend.app.observability.run_trace import NullRunTracer
from backend.app.policies.transport import select_transport_mode
from backend.app.runtime.budget import ToolBudget, ToolBudgetLimits
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.planning import SystemVersion
from backend.app.schemas.request import TravelRequest
from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService
from backend.app.versions.v0.prompts import REQUIREMENT_EXTRACTION_SYSTEM_PROMPT
from backend.app.versions.v1.graph import build_v1_graph
from backend.app.versions.v1.runner import run_v1
from backend.tests.versions.v0.fakes import FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    make_itinerary,
    make_requirements,
)

RUN_ID = UUID("00000000-0000-0000-0000-000000000001")


def _dependencies():
    llm = FakeStructuredLLMClient([make_requirements(), make_itinerary()])
    places = FakePlacesProvider()
    weather = FakeWeatherProvider()
    routes = FakeRoutesProvider()
    tracer = NullRunTracer(RUN_ID)
    service = V1EvidenceAcquisitionService(
        places_provider=places,
        weather_provider=weather,
        routes_provider=routes,
        budget=ToolBudget(),
        cache=RequestCache(),
        tracer=tracer,
    )
    return llm, places, weather, routes, tracer, service


def test_v1_graph_has_explicit_non_agentic_topology() -> None:
    llm, _, _, _, tracer, service = _dependencies()
    graph = build_v1_graph(llm, service, tracer).get_graph()

    assert set(graph.nodes) == {
        "__start__",
        "extract_requirements",
        "validate_trip_dates",
        "resolve_destination",
        "search_place_candidates",
        "shortlist_places",
        "enrich_place_details",
        "acquire_weather",
        "acquire_routes",
        "generate_evidence_informed_itinerary",
        "validate_itinerary_dates",
        "__end__",
    }
    assert {(edge.source, edge.target) for edge in graph.edges} == {
        ("__start__", "extract_requirements"),
        ("acquire_routes", "generate_evidence_informed_itinerary"),
        ("acquire_weather", "acquire_routes"),
        ("enrich_place_details", "acquire_weather"),
        ("extract_requirements", "validate_trip_dates"),
        ("generate_evidence_informed_itinerary", "validate_itinerary_dates"),
        ("resolve_destination", "search_place_candidates"),
        ("search_place_candidates", "shortlist_places"),
        ("shortlist_places", "enrich_place_details"),
        ("validate_itinerary_dates", "__end__"),
        ("validate_trip_dates", "resolve_destination"),
    }


def test_v1_full_offline_run_uses_normalized_evidence_and_fixed_masks() -> None:
    llm, places, weather, routes, tracer, _ = _dependencies()

    result = asyncio.run(
        run_v1(
            TravelRequest(request_text="Plan two days in Sydney."),
            llm,
            places,
            weather,
            routes,
            reference_date=date(2026, 9, 11),
            tracer=tracer,
        )
    )

    assert result.system_version is SystemVersion.V1
    assert len(llm.calls) == 2
    assert llm.calls[0].system_prompt == REQUIREMENT_EXTRACTION_SYSTEM_PROMPT
    assert all(
        request.field_mask == PLACES_CANDIDATE_FIELD_MASK
        for request in places.search_requests
    )
    assert all(
        request.field_mask == PLACES_DETAILS_FIELD_MASK
        for request in places.details_requests
    )
    assert len(places.search_requests) == 4
    assert len(places.details_requests) == 8
    assert len(weather.requests) == 1
    assert weather.requests[0].horizon_days == 10
    assert len(routes.requests) == 1
    assert len(routes.requests[0].origins) == 8
    assert routes.requests[0].travel_mode == "WALK"
    assert routes.requests[0].routing_preference is None
    generation_prompt = llm.calls[1].user_prompt
    generation_system_prompt = llm.calls[1].system_prompt
    assert "place_evidence" not in generation_prompt
    assert '"places"' in generation_prompt
    assert '"precipitation_probability_percent": 70' in generation_prompt
    assert '"travel_mode": "WALK"' in generation_prompt
    assert '"baseline"' in generation_prompt
    assert '"non_walkable_pairs": []' in generation_prompt
    assert "provider_observed" in generation_system_prompt
    assert "mirrored_reverse_estimate" in generation_system_prompt
    assert "schedule the entire visit within them" in " ".join(
        generation_system_prompt.split()
    )
    assert "Never reuse another pair's measurement" in " ".join(
        generation_system_prompt.split()
    )
    assert "forecastDays" not in generation_prompt
    assert "currentOpeningHours" not in generation_prompt


def test_v1_weather_failure_is_explicit_and_does_not_block_generation() -> None:
    llm = FakeStructuredLLMClient([make_requirements(), make_itinerary()])
    places = FakePlacesProvider()
    weather = FakeWeatherProvider(failure=True)
    routes = FakeRoutesProvider()

    result = asyncio.run(
        run_v1(
            TravelRequest(request_text="Plan two days in Sydney."),
            llm,
            places,
            weather,
            routes,
            reference_date=date(2026, 9, 11),
            tracer=NullRunTracer(RUN_ID),
        )
    )

    assert result.system_version is SystemVersion.V1
    assert '"availability": "unavailable"' in llm.calls[1].user_prompt
    assert "Weather unavailable" in llm.calls[1].user_prompt


def test_v1_hard_route_matrix_budget_bounds_shortlist() -> None:
    llm = FakeStructuredLLMClient([make_requirements(), make_itinerary()])
    places = FakePlacesProvider()
    weather = FakeWeatherProvider()
    routes = FakeRoutesProvider()

    asyncio.run(
        run_v1(
            TravelRequest(request_text="Plan two days in Sydney."),
            llm,
            places,
            weather,
            routes,
            reference_date=date(2026, 9, 11),
            budget_limits=ToolBudgetLimits(max_route_matrix_elements=16),
            tracer=NullRunTracer(RUN_ID),
        )
    )

    assert len(places.details_requests) == 4
    assert len(routes.requests[0].origins) == 4
    assert len(routes.requests[0].origins) * len(routes.requests[0].destinations) == 16


def test_v1_captures_reference_date_once_across_midnight() -> None:
    class CrossingMidnightDateProvider:
        def __init__(self) -> None:
            self.calls = 0

        def today(self) -> date:
            self.calls += 1
            return date(2026, 9, 10 + self.calls)

    provider = CrossingMidnightDateProvider()
    llm, places, weather, routes, tracer, _ = _dependencies()

    asyncio.run(
        run_v1(
            TravelRequest(request_text="Plan two days in Sydney."),
            llm,
            places,
            weather,
            routes,
            date_provider=provider,
            tracer=tracer,
        )
    )

    assert provider.calls == 1
    assert "Reference date: 2026-09-11" in llm.calls[0].user_prompt
    assert "Reference date: 2026-09-11" in llm.calls[1].user_prompt


def test_v1_rejects_trip_outside_shared_window_before_any_provider_call() -> None:
    requirements = make_requirements().model_copy(
        update={"start_date": date(2026, 9, 21), "end_date": date(2026, 9, 21)}
    )
    llm = FakeStructuredLLMClient([requirements])
    places = FakePlacesProvider()

    with pytest.raises(ValueError):
        asyncio.run(
            run_v1(
                TravelRequest(request_text="Plan later."),
                llm,
                places,
                FakeWeatherProvider(),
                FakeRoutesProvider(),
                reference_date=date(2026, 9, 11),
                tracer=NullRunTracer(RUN_ID),
            )
        )

    assert places.search_requests == []


def test_v1_rejects_final_itinerary_dates_outside_requested_range() -> None:
    itinerary = make_itinerary().model_copy(update={"end_date": date(2026, 9, 14)})
    llm = FakeStructuredLLMClient([make_requirements(), itinerary])

    with pytest.raises(ValueError):
        asyncio.run(
            run_v1(
                TravelRequest(request_text="Plan two days in Sydney."),
                llm,
                FakePlacesProvider(),
                FakeWeatherProvider(),
                FakeRoutesProvider(),
                reference_date=date(2026, 9, 11),
                tracer=NullRunTracer(RUN_ID),
            )
        )

    assert len(llm.calls) == 2


def test_individual_place_details_failure_continues_with_partial_evidence() -> None:
    llm = FakeStructuredLLMClient([make_requirements(), make_itinerary()])
    places = FakePlacesProvider(details_failure_ids={"poi-0-0"})

    result = asyncio.run(
        run_v1(
            TravelRequest(request_text="Plan two days in Sydney."),
            llm,
            places,
            FakeWeatherProvider(),
            FakeRoutesProvider(),
            reference_date=date(2026, 9, 11),
            tracer=NullRunTracer(RUN_ID),
        )
    )

    assert result.system_version is SystemVersion.V1
    assert "Place Details unavailable" in llm.calls[1].user_prompt


def test_request_scoped_cache_deduplicates_details_weather_and_routes() -> None:
    places = FakePlacesProvider()
    weather = FakeWeatherProvider()
    routes = FakeRoutesProvider()
    budget = ToolBudget()
    service = V1EvidenceAcquisitionService(
        places_provider=places,
        weather_provider=weather,
        routes_provider=routes,
        budget=budget,
        cache=RequestCache(),
        tracer=NullRunTracer(RUN_ID),
    )
    requirements = make_requirements()

    async def scenario():
        destination = await service.resolve_destination("Sydney")
        repeated_destination = await service.resolve_destination("Sydney")
        candidates = await service.search_candidates(requirements, destination)
        shortlist = service.shortlist(candidates)[:2]
        first_places = await service.enrich_places(shortlist)
        second_places = await service.enrich_places(shortlist)
        first_weather = await service.acquire_weather(
            requirements=requirements,
            destination=destination,
            reference_date=date(2026, 9, 11),
        )
        second_weather = await service.acquire_weather(
            requirements=requirements,
            destination=destination,
            reference_date=date(2026, 9, 11),
        )
        mode = select_transport_mode(
            TravelRequest(request_text="Plan Sydney."), requirements
        )
        first_routes = await service.acquire_routes(
            places=first_places,
            mode=mode,
            requirements=requirements,
        )
        second_routes = await service.acquire_routes(
            places=first_places,
            mode=mode,
            requirements=requirements,
        )
        return (
            destination,
            repeated_destination,
            first_places,
            second_places,
            first_weather,
            second_weather,
            first_routes,
            second_routes,
        )

    results = asyncio.run(scenario())

    assert results[0] == results[1]
    assert results[2] == results[3]
    assert results[4] == results[5]
    assert results[6] == results[7]
    assert len(places.search_requests) == 4
    assert len(places.details_requests) == 2
    assert len(weather.requests) == 1
    assert len(routes.requests) == 1
    assert budget.summary()["place_detail_calls"]["used"] == 2
    assert budget.summary()["weather_calls"]["used"] == 1
    assert budget.summary()["route_matrix_elements"]["used"] == 4
    assert budget.summary()["alternative_route_pairs"]["used"] == 0
    assert budget.summary()["alternative_route_matrix_calls"]["used"] == 0
