"""Offline contract tests for V1's single-call named-place extraction."""

import asyncio
from datetime import date
from uuid import UUID

import pytest

from backend.app.evidence.web_models import RequestedFacet
from backend.app.observability.run_trace import NullRunTracer
from backend.app.runtime.budget import ToolBudget
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.named_place_intent import NamedPlaceInclusion, NamedPlaceIntent
from backend.app.schemas.request import TravelRequest
from backend.app.schemas.trip_intent import RequestedPlaceInformation, TripIntentExtractionResult
from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService
from backend.app.versions.v1.graph import V1StageError, build_v1_graph
from backend.tests.versions.v0.fakes import FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    make_extraction,
    make_itinerary,
    make_requirements,
)

RUN_ID = UUID("00000000-0000-0000-0000-000000000026")


class RecordingTracer(NullRunTracer):
    def __init__(self) -> None:
        super().__init__(RUN_ID)
        self.events: list[tuple[str, object | None]] = []

    def event(self, event_type: str, payload: object | None = None) -> None:
        self.events.append((event_type, payload))


def _run(request_text: str, extraction: TripIntentExtractionResult):
    llm = FakeStructuredLLMClient([extraction, make_itinerary()])
    places = FakePlacesProvider()
    tracer = RecordingTracer()
    service = V1EvidenceAcquisitionService(
        places_provider=places,
        weather_provider=FakeWeatherProvider(),
        routes_provider=FakeRoutesProvider(),
        budget=ToolBudget(),
        cache=RequestCache(),
        tracer=tracer,
    )
    graph = build_v1_graph(llm, service, tracer)
    return (
        asyncio.run(
            graph.ainvoke(
                {
                    "request": TravelRequest(request_text=request_text),
                    "reference_date": date(2026, 9, 11),
                }
            )
        ),
        llm,
        places,
        tracer,
    )


@pytest.mark.parametrize(
    ("source_text", "inclusion"),
    [
        ("Sydney Opera House is a must-visit", NamedPlaceInclusion.REQUIRED),
        ("I want to visit Sydney Opera House", NamedPlaceInclusion.REQUIRED),
        ("I'd like to visit Sydney Opera House", NamedPlaceInclusion.REQUIRED),
        ("I hope to visit Sydney Opera House", NamedPlaceInclusion.REQUIRED),
        ("I heard Sydney Opera House is good", NamedPlaceInclusion.OPTIONAL),
        ("I'm interested in Sydney Opera House", NamedPlaceInclusion.OPTIONAL),
        ("Maybe visit Sydney Opera House", NamedPlaceInclusion.OPTIONAL),
        ("Visit Sydney Opera House if there is time", NamedPlaceInclusion.OPTIONAL),
        ("Sydney Opera House would be nice if convenient", NamedPlaceInclusion.OPTIONAL),
        ("I want to visit Sydney Opera House if there is time", NamedPlaceInclusion.OPTIONAL),
    ],
)
def test_mocked_named_place_inclusion_is_retained_separately(
    source_text: str, inclusion: NamedPlaceInclusion
) -> None:
    base = make_requirements()
    intent = NamedPlaceIntent(
        place_text="Sydney Opera House",
        inclusion=inclusion,
        source_text=source_text,
    )

    state, llm, places, tracer = _run(source_text, make_extraction(base, intents=(intent,)))

    assert state["requirements"] == base
    assert state["named_place_intents"] == (intent,)
    assert llm.calls[0].response_schema is TripIntentExtractionResult
    assert len(llm.calls) == 2
    assert len(places.search_requests) == 4
    assert any(name == "named_place_intents_validated" for name, _ in tracer.events)


@pytest.mark.parametrize("category", ["museums", "parks", "beaches"])
def test_generic_category_remains_base_requirement_without_named_intent(category: str) -> None:
    base = make_requirements().model_copy(update={"required_activities": [category]})

    state, _, _, _ = _run(f"I want to visit {category}.", make_extraction(base))

    assert state["requirements"].required_activities == [category]
    assert state["named_place_intents"] == ()


def test_typed_intent_replaces_free_text_named_place_identity_in_funnel() -> None:
    base = make_requirements().model_copy(
        update={"required_activities": ["Visit the Sydney Opera House"]}
    )
    intent = NamedPlaceIntent(
        place_text="Sydney Opera House",
        inclusion=NamedPlaceInclusion.REQUIRED,
        source_text="Sydney Opera House is a must-visit",
    )

    state, _, places, _ = _run(
        "Sydney Opera House is a must-visit", make_extraction(base, intents=(intent,))
    )

    assert state["named_place_intents"] == (intent,)
    assert state["candidate_funnel"].unresolved_required_names == ("Sydney Opera House",)
    assert [item.term for item in state["candidate_funnel"].search_intents].count(
        "Sydney Opera House"
    ) == 1
    assert "Visit the Sydney Opera House in Sydney" not in [
        request.text_query for request in places.search_requests
    ]


def test_invalid_intent_fails_extraction_before_provider_calls() -> None:
    extraction = make_extraction(
        intents=(
            NamedPlaceIntent(
                place_text="Sydney Opera House",
                inclusion=NamedPlaceInclusion.REQUIRED,
                source_text="unsupported source",
            ),
        )
    )
    llm = FakeStructuredLLMClient([extraction])
    places = FakePlacesProvider()
    tracer = RecordingTracer()
    graph = build_v1_graph(
        llm,
        V1EvidenceAcquisitionService(
            places_provider=places,
            weather_provider=FakeWeatherProvider(),
            routes_provider=FakeRoutesProvider(),
            budget=ToolBudget(),
            cache=RequestCache(),
            tracer=tracer,
        ),
        tracer,
    )

    with pytest.raises(V1StageError, match="extract_requirements"):
        asyncio.run(
            graph.ainvoke(
                {
                    "request": TravelRequest(request_text="Plan Sydney."),
                    "reference_date": date(2026, 9, 11),
                }
            )
        )
    assert places.search_requests == []
    assert (
        "named_place_intents_validation_failed",
        {"reason": "source_not_in_request"},
    ) in tracer.events


def test_typed_information_is_kept_in_v1_state_without_another_extraction_call() -> None:
    text = "Sydney Opera House. How much is admission?"
    intent = NamedPlaceIntent(
        place_text="Sydney Opera House",
        inclusion=NamedPlaceInclusion.OPTIONAL,
        source_text="Sydney Opera House",
    )
    information = RequestedPlaceInformation(
        target_surface="Sydney Opera House",
        target_source_text="Sydney Opera House",
        source_text="How much is admission?",
        requested_facet=RequestedFacet.ADMISSION_FEE,
        operational_need=None,
    )

    state, llm, _, tracer = _run(
        text,
        make_extraction(intents=(intent,), information=(information,)),
    )

    assert state["requested_place_information"] == (information,)
    assert llm.calls[0].response_schema is TripIntentExtractionResult
    assert len(llm.calls) == 2  # Requirements extraction and itinerary generation only.
    validated = next(payload for name, payload in tracer.events if name == "trip_intents_validated")
    assert validated["requested_information"][0]["facet"] == "admission_fee"


def test_invalid_information_provenance_stops_before_provider_calls() -> None:
    intent = NamedPlaceIntent(
        place_text="Sydney Opera House",
        inclusion=NamedPlaceInclusion.OPTIONAL,
        source_text="Sydney Opera House",
    )
    information = RequestedPlaceInformation(
        target_surface="Sydney Opera House",
        target_source_text="Sydney Opera House",
        source_text="Unsupported admission question",
        requested_facet=RequestedFacet.ADMISSION_FEE,
        operational_need=None,
    )
    llm = FakeStructuredLLMClient([make_extraction(intents=(intent,), information=(information,))])
    places = FakePlacesProvider()
    tracer = RecordingTracer()
    graph = build_v1_graph(
        llm,
        V1EvidenceAcquisitionService(
            places_provider=places,
            weather_provider=FakeWeatherProvider(),
            routes_provider=FakeRoutesProvider(),
            budget=ToolBudget(),
            cache=RequestCache(),
            tracer=tracer,
        ),
        tracer,
    )

    with pytest.raises(V1StageError, match="extract_requirements"):
        asyncio.run(
            graph.ainvoke(
                {
                    "request": TravelRequest(request_text="Sydney Opera House."),
                    "reference_date": date(2026, 9, 11),
                }
            )
        )
    assert places.search_requests == []
    assert (
        "trip_intents_validation_failed",
        {"reason": "information_source_not_in_request"},
    ) in tracer.events
