"""Explicit non-agentic LangGraph workflow for V1 external evidence."""

from collections.abc import Sequence

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from backend.app.evidence.models import (
    PlaceCandidate,
    PlaceEvidence,
    RouteElementEvidenceType,
)
from backend.app.evidence.opening_hours import planning_opening_hours
from backend.app.llm.client import StructuredLLMClient
from backend.app.observability.run_trace import RunTracer, TracePayloadMode
from backend.app.policies.named_place_intent import (
    NamedPlaceIntentContractError,
    validate_named_place_intents,
)
from backend.app.policies.poi_selection import SelectionConflict
from backend.app.policies.transport import select_transport_mode
from backend.app.policies.trip_dates import (
    create_trip_date_window,
    validate_itinerary_dates,
    validate_requested_trip_dates,
)
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.named_place_intent import RequirementsWithNamedPlaceIntents
from backend.app.schemas.request import TravelRequirements
from backend.app.services.evidence_acquisition import (
    CandidateFunnelResult,
    NoViableCandidatesError,
    V1EvidenceAcquisitionService,
)
from backend.app.services.official_web_integration import OfficialWebIntegrationService
from backend.app.services.review_selection import ReviewAwareSelectionResult
from backend.app.versions.v0.graph import MissingRequiredFieldsError
from backend.app.versions.v0.prompts import build_requirement_extraction_prompt
from backend.app.versions.v1.official_planner import build_official_planner_evidence
from backend.app.versions.v1.official_web import project_official_web_inputs
from backend.app.versions.v1.prompts import (
    ITINERARY_GENERATION_SYSTEM_PROMPT,
    V1_REQUIREMENT_EXTRACTION_SYSTEM_PROMPT,
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


def project_selected_places(
    funnel: CandidateFunnelResult,
    selection: ReviewAwareSelectionResult,
) -> tuple[list[PlaceCandidate], list[PlaceEvidence]]:
    """Project the stable selected order into aligned downstream Places contracts."""

    by_id = {item.candidate.place_id: item for item in funnel.enriched_candidates}
    candidates: list[PlaceCandidate] = []
    evidence: list[PlaceEvidence] = []
    for place_id in selection.selected_place_ids:
        item = by_id.get(place_id)
        if item is None or item.structured_evidence is None:
            raise ValueError(f"Selected Place {place_id} lacks structured Details evidence")
        if item.structured_evidence.place_id != place_id:
            raise ValueError("Selected candidate and Place evidence IDs do not align")
        candidates.append(item.candidate)
        evidence.append(item.structured_evidence)
    if not candidates:
        raise NoViableCandidatesError("No viable POIs remained after review-aware selection")
    if len({item.place_id for item in candidates}) != len(candidates):
        raise ValueError("Selected POI Place IDs must be unique")
    return candidates, evidence


def build_v1_graph(
    llm_client: StructuredLLMClient,
    evidence_service: V1EvidenceAcquisitionService,
    tracer: RunTracer,
    *,
    llm_config_identity: str = "run_scoped_llm",
    official_web_service: OfficialWebIntegrationService | None = None,
) -> CompiledStateGraph:
    """Build the fixed V1 graph with one bounded official-Web step."""

    async def extract_requirements(state: V1State) -> dict[str, object]:
        tracer.event("requirement_extraction_started")
        user_prompt = build_requirement_extraction_prompt(state["request"], state["reference_date"])
        tracer.payload(
            "llm",
            "requirement_extraction_request",
            {
                "system_prompt": V1_REQUIREMENT_EXTRACTION_SYSTEM_PROMPT,
                "user_prompt": user_prompt,
                "response_schema": "RequirementsWithNamedPlaceIntents",
            },
            minimum_mode=TracePayloadMode.RAW,
        )
        try:
            extraction = await llm_client.generate_structured(
                system_prompt=V1_REQUIREMENT_EXTRACTION_SYSTEM_PROMPT,
                user_prompt=user_prompt,
                response_schema=RequirementsWithNamedPlaceIntents,
            )
        except Exception as exc:
            tracer.event("requirement_extraction_failed", {"error": type(exc).__name__})
            raise V1StageError("extract_requirements") from exc

        requirements = extraction.requirements
        try:
            named_place_intents = validate_named_place_intents(
                extraction.named_place_intents, state["request"].request_text
            )
        except NamedPlaceIntentContractError as exc:
            tracer.event("named_place_intents_validation_failed", {"reason": exc.code})
            raise V1StageError("extract_requirements") from exc
        tracer.event(
            "named_place_intents_validated",
            {
                "count": len(named_place_intents),
                "duplicate_count": len(extraction.named_place_intents) - len(named_place_intents),
                "intents": [
                    {
                        "place_text": item.place_text,
                        "inclusion": item.inclusion.value,
                        "source_text": item.source_text,
                        "additional_source_texts": item.additional_source_texts,
                    }
                    for item in named_place_intents
                ],
            },
        )

        missing_fields = _missing_fields(requirements)
        if missing_fields:
            unresolved_fields = list(
                dict.fromkeys([*requirements.unresolved_fields, *missing_fields])
            )
            requirements = requirements.model_copy(update={"unresolved_fields": unresolved_fields})
            tracer.event("requirements_incomplete", {"fields": list(missing_fields)})
            raise MissingRequiredFieldsError(
                unresolved_fields=missing_fields,
                requirements=requirements,
            )
        tracer.payload(
            "llm",
            "requirement_extraction_response",
            extraction,
            minimum_mode=TracePayloadMode.RAW,
        )
        tracer.set_requirements(requirements)
        tracer.event("requirements_extracted", requirements.model_dump(mode="json"))
        return {"requirements": requirements, "named_place_intents": named_place_intents}

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
        destination = await evidence_service.resolve_destination(state["requirements"].destination)
        tracer.event("destination_resolved", destination.model_dump(mode="json"))
        return {"destination_context": destination}

    async def acquire_candidate_funnel(state: V1State) -> dict[str, CandidateFunnelResult]:
        requirements = state["requirements"]
        named_place_intents = state["named_place_intents"]
        tracer.event(
            "candidate_funnel_started",
            {
                "named_place_intents": [
                    {"place_text": item.place_text, "inclusion": item.inclusion.value}
                    for item in named_place_intents
                ]
            },
        )
        funnel = await evidence_service.run_candidate_funnel(
            requirements=requirements,
            destination=state["destination_context"],
            window=create_trip_date_window(state["reference_date"]),
            named_place_intents=named_place_intents,
        )
        tracer.event(
            "candidate_funnel_completed",
            {
                "search_intents": [
                    {"intent_id": item.intent_id, "kind": item.kind.value}
                    for item in funnel.search_intents
                ],
                "raw_observation_count": len(funnel.observations),
                "merged_place_ids": [item.candidate.place_id for item in funnel.merged.places],
                "c_raw": funnel.capacities.c_raw,
                "r_pool": funnel.capacities.r_pool,
                "k_final": funnel.capacities.k_final,
                "c_raw_place_ids": funnel.c_raw_selection.selected_place_ids,
                "r_pool_place_ids": funnel.r_pool_selection.selected_place_ids,
                "unresolved_required_names": funnel.unresolved_required_names,
            },
        )
        eligibility = {item.place_id: item for item in funnel.no_review_selection.eligibility}
        attempted = set(funnel.rating_contenders)
        tracer.event(
            "candidate_details_rating_recorded",
            {
                "places": [
                    {
                        "place_id": item.candidate.place_id,
                        "attempted": item.candidate.place_id in attempted,
                        "rating_state": item.rating_state.value,
                        "rating_present": item.rating is not None,
                        "structured_available": item.structured_evidence is not None,
                        "business_status": item.candidate.business_status,
                        "date_risk": eligibility[item.candidate.place_id].date_risk.value,
                    }
                    for item in funnel.enriched_candidates
                ],
                "details_failures": funnel.details_failures,
            },
        )
        return {"candidate_funnel": funnel}

    async def select_review_aware_pois(state: V1State) -> dict[str, object]:
        funnel = state["candidate_funnel"]
        selection = await evidence_service.run_review_aware_selection(
            funnel=funnel,
            requirements=state["requirements"],
            window=create_trip_date_window(state["reference_date"]),
            llm_client=llm_client,
            llm_config_identity=llm_config_identity,
        )
        candidates, places = project_selected_places(funnel, selection)
        conflicts: tuple[SelectionConflict, ...] = tuple(
            dict.fromkeys((*funnel.conflicts, *selection.final_selection.conflicts))
        )
        tracer.event(
            "final_poi_selection_completed",
            {
                "selected_place_ids": selection.selected_place_ids,
                "selected_count": len(candidates),
                "unresolved_required_names": funnel.unresolved_required_names,
                "conflicts": [
                    {"place_id_or_name": item.place_id_or_name, "reason": item.reason}
                    for item in conflicts
                ],
                "selected_scores": [
                    {
                        "place_id": item.place_id,
                        "must_visit": item.must_visit,
                        "q_rel": str(item.score.q_rel) if item.score else None,
                        "c_cov": str(item.score.c_cov) if item.score else None,
                        "g_geo": str(item.score.g_geo) if item.score else None,
                        "r_rating": str(item.score.r_rating) if item.score else None,
                        "e_exp": str(item.score.e_exp) if item.score else None,
                        "total": str(item.score.total) if item.score else None,
                    }
                    for item in selection.final_selection.selected
                ],
                "review_attempts": [
                    {
                        "place_id": item.place_id,
                        "status": item.status,
                        "profile_availability": item.profile_availability,
                    }
                    for item in selection.attempts
                ],
                "experience_scores": [
                    {"place_id": place_id, "e_exp": str(score.total)}
                    for place_id, score in selection.experience_scores
                ],
                "review_stop_reason": selection.stop_reason,
            },
        )
        tracer.event(
            "named_place_final_selection_completed",
            {
                "places": [
                    {
                        "place_text": item.named_place_intent.place_text,
                        "inclusion": item.named_place_intent.inclusion.value,
                        "resolved_place_id": item.resolved_place_id,
                        "final_selected": item.resolved_place_id in selection.selected_place_ids,
                        "must_visit": item.resolved_place_id in funnel.must_visit_place_ids
                        if item.resolved_place_id is not None
                        else False,
                    }
                    for item in funnel.named_place_resolutions
                ]
            },
        )
        tracer.payload(
            "evidence",
            "selected_place_evidence",
            places,
            minimum_mode=TracePayloadMode.NORMALIZED,
        )
        return {
            "review_selection": selection,
            "selected_candidates": candidates,
            "place_evidence": places,
            "selection_conflicts": conflicts,
        }

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
            places=state["place_evidence"],
            mode=mode,
            requirements=state["requirements"],
        )
        tracer.event(
            "route_matrix_completed",
            {
                "baseline_availability": routes.baseline.availability.value,
                "baseline_element_count": len(routes.baseline.elements),
                "not_observed_reasons": {
                    reason: sum(
                        item.evidence_type is RouteElementEvidenceType.NOT_OBSERVED
                        and (item.unavailable_reason or "unspecified") == reason
                        for item in routes.baseline.elements
                    )
                    for reason in sorted(
                        {
                            item.unavailable_reason or "unspecified"
                            for item in routes.baseline.elements
                            if item.evidence_type is RouteElementEvidenceType.NOT_OBSERVED
                        }
                    )
                },
                "provider_route_not_found_count": sum(
                    item.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
                    and item.condition == "ROUTE_NOT_FOUND"
                    for item in routes.baseline.elements
                ),
                "alternative_count": len(routes.alternatives),
                "non_walkable_pair_count": len(routes.non_walkable_pairs),
            },
        )
        return {"transport_mode": mode, "route_evidence": routes}

    async def acquire_and_resolve_official_web(state: V1State) -> dict[str, object]:
        if official_web_service is None:
            tracer.event("official_web_disabled")
            return {"official_web_result": None}
        try:
            projection = project_official_web_inputs(
                funnel=state["candidate_funnel"],
                selection=state["review_selection"],
                candidates=state["selected_candidates"],
                places=state["place_evidence"],
            )
            result = await official_web_service.run(
                request=state["request"],
                requirements=state["requirements"],
                projection=projection,
            )
        except Exception as exc:
            tracer.event("official_web_integration_failed", {"error_type": type(exc).__name__})
            raise V1StageError("official_web") from exc
        planner_evidence = build_official_planner_evidence(result)
        tracer.event(
            "official_planner_evidence_prepared",
            {
                "places": [
                    {
                        "place_id": item["place_id"],
                        "accepted_facts": [
                            {
                                key: fact[key]
                                for key in (
                                    "dimension",
                                    "subject_scope",
                                    "scope_text",
                                    "date",
                                    "applicable_start_date",
                                    "applicable_end_date",
                                    "value_kind",
                                    "value_text",
                                    "relation",
                                    "source_refs",
                                )
                            }
                            for fact in item["accepted_effective_facts"]
                        ],
                        "operational_days": item["operational_days"],
                        "need_statuses": item["need_statuses"],
                        "conflict_source_refs": item["unresolved_conflict_source_refs"],
                        "task_statuses": [
                            {
                                "information_need": task["information_need"],
                                "acquisition_status": task["acquisition_status"],
                                "evidence_status": task["evidence_status"],
                                "facet_statuses": task["facet_statuses"],
                            }
                            for task in item["tasks"]
                        ],
                    }
                    for item in planner_evidence
                ],
            },
        )
        return {
            "official_web_result": result,
            "official_planner_evidence": planner_evidence,
        }

    async def generate_evidence_informed_itinerary(
        state: V1State,
    ) -> dict[str, Itinerary]:
        tracer.event("generation_started")
        trip_start = state["requirements"].start_date
        trip_end = state["requirements"].end_date
        if trip_start is None or trip_end is None:
            raise ValueError("Complete trip dates are required for opening-hours planning evidence")
        tracer.event(
            "opening_hours_planning_views_created",
            {
                "places": [
                    {
                        "place_id": place.place_id,
                        "current_present": place.current_opening_hours is not None,
                        "regular_present": place.regular_opening_hours is not None,
                        "current_window_start": (
                            place.current_opening_hours.valid_from
                            if place.current_opening_hours is not None
                            else None
                        ),
                        "current_window_end": (
                            place.current_opening_hours.valid_through
                            if place.current_opening_hours is not None
                            else None
                        ),
                        "date_bases": [
                            {"date": day.date, "basis": day.basis}
                            for day in planning_opening_hours(place, trip_start, trip_end)
                        ],
                    }
                    for place in state["place_evidence"]
                ]
            },
        )
        user_prompt = build_itinerary_generation_prompt(
            state["request"],
            state["requirements"],
            state["reference_date"],
            places=state["place_evidence"],
            weather=state["weather_evidence"],
            routes=state["route_evidence"],
            requirement_conflicts=state["selection_conflicts"],
            official_evidence=state.get("official_planner_evidence"),
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
    graph_builder.add_node("acquire_candidate_funnel", acquire_candidate_funnel)
    graph_builder.add_node("select_review_aware_pois", select_review_aware_pois)
    graph_builder.add_node("acquire_weather", acquire_weather)
    graph_builder.add_node("acquire_routes", acquire_routes)
    graph_builder.add_node("acquire_and_resolve_official_web", acquire_and_resolve_official_web)
    graph_builder.add_node(
        "generate_evidence_informed_itinerary", generate_evidence_informed_itinerary
    )
    graph_builder.add_node("validate_itinerary_dates", validate_itinerary_date_node)
    graph_builder.add_edge(START, "extract_requirements")
    graph_builder.add_edge("extract_requirements", "validate_trip_dates")
    graph_builder.add_edge("validate_trip_dates", "resolve_destination")
    graph_builder.add_edge("resolve_destination", "acquire_candidate_funnel")
    graph_builder.add_edge("acquire_candidate_funnel", "select_review_aware_pois")
    graph_builder.add_edge("select_review_aware_pois", "acquire_weather")
    graph_builder.add_edge("acquire_weather", "acquire_routes")
    graph_builder.add_edge("acquire_routes", "acquire_and_resolve_official_web")
    graph_builder.add_edge(
        "acquire_and_resolve_official_web", "generate_evidence_informed_itinerary"
    )
    graph_builder.add_edge("generate_evidence_informed_itinerary", "validate_itinerary_dates")
    graph_builder.add_edge("validate_itinerary_dates", END)
    return graph_builder.compile(name="v1")
