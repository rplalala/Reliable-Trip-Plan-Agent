"""Explicit non-agentic LangGraph workflow for V1-A external evidence."""

from collections.abc import Sequence

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from backend.app.llm.client import StructuredLLMClient
from backend.app.observability.run_trace import RunTracer, TracePayloadMode
from backend.app.policies.transport import select_transport_mode
from backend.app.policies.trip_dates import (
    create_trip_date_window,
    validate_itinerary_dates,
    validate_requested_trip_dates,
)
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import TravelRequirements
from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService
from backend.app.versions.v0.graph import MissingRequiredFieldsError
from backend.app.versions.v0.prompts import (
    REQUIREMENT_EXTRACTION_SYSTEM_PROMPT,
    build_requirement_extraction_prompt,
)
from backend.app.versions.v1.prompts import (
    ITINERARY_GENERATION_SYSTEM_PROMPT,
    build_itinerary_generation_prompt,
)
from backend.app.versions.v1.state import V1State

REQUIRED_REQUIREMENT_FIELDS = ("destination", "start_date", "end_date")


class V1StageError(RuntimeError):
    """Identify the V1 stage in which a provider, schema, or graph failure occurred."""

    def __init__(self, stage: str) -> None:
        self.stage = stage
        super().__init__(f"V1 stage failed: {stage}")


def _missing_fields(requirements: TravelRequirements) -> Sequence[str]:
    return [
        field_name
        for field_name in REQUIRED_REQUIREMENT_FIELDS
        if getattr(requirements, field_name) is None
    ]


def build_v1_graph(
    llm_client: StructuredLLMClient,
    evidence_service: V1EvidenceAcquisitionService,
    tracer: RunTracer,
) -> CompiledStateGraph:
    """Build the fixed V1-A graph with no free-form tool loop."""

    async def extract_requirements(state: V1State) -> dict[str, TravelRequirements]:
        tracer.event("requirement_extraction_started")
        user_prompt = build_requirement_extraction_prompt(
            state["request"], state["reference_date"]
        )
        tracer.payload(
            "llm",
            "requirement_extraction_request",
            {
                "system_prompt": REQUIREMENT_EXTRACTION_SYSTEM_PROMPT,
                "user_prompt": user_prompt,
                "response_schema": "TravelRequirements",
            },
            minimum_mode=TracePayloadMode.RAW,
        )
        try:
            requirements = await llm_client.generate_structured(
                system_prompt=REQUIREMENT_EXTRACTION_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_schema=TravelRequirements,
            )
        except Exception as exc:
            tracer.event("requirement_extraction_failed", {"error": type(exc).__name__})
            raise V1StageError("extract_requirements") from exc

        missing_fields = _missing_fields(requirements)
        if missing_fields:
            unresolved_fields = list(
                dict.fromkeys([*requirements.unresolved_fields, *missing_fields])
            )
            requirements = requirements.model_copy(
                update={"unresolved_fields": unresolved_fields}
            )
            tracer.event("requirements_incomplete", {"fields": list(missing_fields)})
            raise MissingRequiredFieldsError(
                unresolved_fields=missing_fields,
                requirements=requirements,
            )
        tracer.payload(
            "llm",
            "requirement_extraction_response",
            requirements,
            minimum_mode=TracePayloadMode.RAW,
        )
        tracer.set_requirements(requirements)
        tracer.event("requirements_extracted", requirements.model_dump(mode="json"))
        return {"requirements": requirements}

    async def validate_trip_dates(state: V1State) -> dict[str, object]:
        requirements = state["requirements"]
        validate_requested_trip_dates(
            requirements.start_date,
            requirements.end_date,
            create_trip_date_window(state["reference_date"]),
        )
        tracer.event(
            "date_window_validated",
            {
                "start_date": requirements.start_date,
                "end_date": requirements.end_date,
            },
        )
        return {}

    async def resolve_destination(state: V1State) -> dict[str, object]:
        tracer.event("destination_resolution_started")
        destination = await evidence_service.resolve_destination(
            state["requirements"].destination
        )
        tracer.event("destination_resolved", destination.model_dump(mode="json"))
        return {"destination_context": destination}

    async def search_place_candidates(state: V1State) -> dict[str, object]:
        tracer.event("places_search_started")
        candidates = await evidence_service.search_candidates(
            state["requirements"], state["destination_context"]
        )
        tracer.event("places_search_completed", {"candidate_count": len(candidates)})
        return {"candidates": candidates}

    async def shortlist_places(state: V1State) -> dict[str, object]:
        shortlist = evidence_service.shortlist(state["candidates"])
        tracer.event(
            "shortlist_created",
            {
                "place_ids": [item.place_id for item in shortlist],
                "count": len(shortlist),
            },
        )
        return {"shortlist": shortlist}

    async def enrich_place_details(state: V1State) -> dict[str, object]:
        tracer.event("place_details_started", {"count": len(state["shortlist"])})
        places = await evidence_service.enrich_places(state["shortlist"])
        tracer.event(
            "place_details_completed",
            {
                "count": len(places),
                "partial_count": sum(
                    item.unavailable_reason is not None for item in places
                ),
            },
        )
        return {"place_evidence": places}

    async def acquire_weather(state: V1State) -> dict[str, object]:
        tracer.event("weather_started")
        weather = await evidence_service.acquire_weather(
            requirements=state["requirements"],
            destination=state["destination_context"],
            reference_date=state["reference_date"],
        )
        tracer.event("weather_completed", {"availability": weather.availability.value})
        return {"weather_evidence": weather}

    async def acquire_routes(state: V1State) -> dict[str, object]:
        mode = select_transport_mode(state["request"], state["requirements"])
        tracer.event("route_matrix_started", mode.model_dump(mode="json"))
        routes = await evidence_service.acquire_routes(
            places=state["place_evidence"], mode=mode
        )
        tracer.event(
            "route_matrix_completed",
            {
                "availability": routes.availability.value,
                "element_count": len(routes.elements),
            },
        )
        return {"transport_mode": mode, "route_evidence": routes}

    async def generate_evidence_informed_itinerary(
        state: V1State,
    ) -> dict[str, Itinerary]:
        tracer.event("generation_started")
        user_prompt = build_itinerary_generation_prompt(
            state["request"],
            state["requirements"],
            state["reference_date"],
            places=state["place_evidence"],
            weather=state["weather_evidence"],
            routes=state["route_evidence"],
        )
        tracer.payload(
            "llm",
            "itinerary_generation_request",
            {
                "system_prompt": ITINERARY_GENERATION_SYSTEM_PROMPT,
                "user_prompt": user_prompt,
                "response_schema": "Itinerary",
            },
            minimum_mode=TracePayloadMode.RAW,
        )
        try:
            itinerary = await llm_client.generate_structured(
                system_prompt=ITINERARY_GENERATION_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_schema=Itinerary,
            )
        except Exception as exc:
            tracer.event("generation_failed", {"error": type(exc).__name__})
            raise V1StageError("generate_itinerary") from exc
        tracer.payload(
            "llm",
            "itinerary_generation_response",
            itinerary,
            minimum_mode=TracePayloadMode.RAW,
        )
        tracer.event("generation_completed")
        return {"itinerary": itinerary}

    async def validate_itinerary_date_node(state: V1State) -> dict[str, object]:
        validate_itinerary_dates(
            state["requirements"],
            state["itinerary"],
            create_trip_date_window(state["reference_date"]),
        )
        tracer.event("itinerary_dates_validated")
        return {}

    graph_builder = StateGraph(V1State)
    graph_builder.add_node("extract_requirements", extract_requirements)
    graph_builder.add_node("validate_trip_dates", validate_trip_dates)
    graph_builder.add_node("resolve_destination", resolve_destination)
    graph_builder.add_node("search_place_candidates", search_place_candidates)
    graph_builder.add_node("shortlist_places", shortlist_places)
    graph_builder.add_node("enrich_place_details", enrich_place_details)
    graph_builder.add_node("acquire_weather", acquire_weather)
    graph_builder.add_node("acquire_routes", acquire_routes)
    graph_builder.add_node(
        "generate_evidence_informed_itinerary", generate_evidence_informed_itinerary
    )
    graph_builder.add_node("validate_itinerary_dates", validate_itinerary_date_node)
    graph_builder.add_edge(START, "extract_requirements")
    graph_builder.add_edge("extract_requirements", "validate_trip_dates")
    graph_builder.add_edge("validate_trip_dates", "resolve_destination")
    graph_builder.add_edge("resolve_destination", "search_place_candidates")
    graph_builder.add_edge("search_place_candidates", "shortlist_places")
    graph_builder.add_edge("shortlist_places", "enrich_place_details")
    graph_builder.add_edge("enrich_place_details", "acquire_weather")
    graph_builder.add_edge("acquire_weather", "acquire_routes")
    graph_builder.add_edge("acquire_routes", "generate_evidence_informed_itinerary")
    graph_builder.add_edge("generate_evidence_informed_itinerary", "validate_itinerary_dates")
    graph_builder.add_edge("validate_itinerary_dates", END)
    return graph_builder.compile(name="v1")
