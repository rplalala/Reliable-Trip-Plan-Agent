"""Offline integration coverage for the active revised V1-A graph."""

import asyncio
import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from uuid import UUID

import pytest

from backend.app.evidence.experience_models import (
    ExperienceDimension,
    ExperienceProfileDraft,
    ExperienceSignalDraft,
    ExperienceValue,
)
from backend.app.evidence.models import RouteElementEvidenceType
from backend.app.integrations.models import (
    LatLng,
    PlaceCandidateDTO,
    PlaceReviewDTO,
    PlaceReviewsDTO,
    PlaceSearchResponse,
    RouteMatrixDTO,
)
from backend.app.observability.run_trace import (
    FileRunTracer,
    NullRunTracer,
    RunTraceContext,
    TracePayloadMode,
)
from backend.app.policies.trip_dates import create_trip_date_window
from backend.app.runtime.budget import ToolBudget, ToolBudgetLimits
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.interpreted_requirements import ClarificationRequired
from backend.app.schemas.interpreted_requirements import (
    InterpretationDraft as TripIntentExtractionResult,
)
from backend.app.schemas.itinerary import ItineraryDay
from backend.app.schemas.itinerary_projection import EstimatedCostProjectionDiagnostic, V1Itinerary
from backend.app.schemas.named_place_intent import (
    NamedPlaceInclusion,
    NamedPlaceIntent,
)
from backend.app.schemas.request import PlanningRequest, TravelRequirements
from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService
from backend.app.versions.v1.graph import build_v1_graph, project_selected_places
from backend.app.versions.v1.runner import run_v1
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v1.fakes import FakePlacesProvider, FakeWeatherProvider
from backend.tests.versions.v1.fakes import RevisedFakeLLM as FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import make_revised_extraction as make_extraction

REFERENCE_DATE = date(2026, 9, 11)
RUN_ID = UUID("00000000-0000-0000-0000-000000000016")
REVIEW_SENTINEL = "PRIVATE_RAW_REVIEW_TEXT_NEVER_TRACE"


class RecordingTracer(NullRunTracer):
    def __init__(self) -> None:
        super().__init__(RUN_ID)
        self.events: list[tuple[str, object | None]] = []
        self.payloads: list[tuple[str, str, object]] = []

    def event(self, event_type: str, payload: object | None = None) -> None:
        self.events.append((event_type, payload))

    def payload(self, category: str, name: str, value: object, *, minimum_mode) -> None:
        self.payloads.append((category, name, value))


class ManyPlacesProvider(FakePlacesProvider):
    def __init__(
        self,
        *,
        per_query: int,
        named_first: str | None = None,
        details_failure_ids: set[str] | None = None,
        with_reviews: bool = False,
    ) -> None:
        super().__init__(details_failure_ids=details_failure_ids)
        self.per_query = per_query
        self.named_first = named_first
        self.with_reviews = with_reviews

    async def search_text(self, request):
        if request.location_bias is None:
            return await super().search_text(request)
        self.search_requests.append(request)
        group = self._candidate_call
        self._candidate_call += 1
        candidates = [
            PlaceCandidateDTO(
                place_id=f"poi-{group}-{rank}",
                display_name=(
                    self.named_first
                    if group == 0 and rank == 0 and self.named_first is not None
                    else f"Place poi-{group}-{rank}"
                ),
                location=LatLng(
                    latitude=-33.86 - group * 0.01 - rank * 0.001,
                    longitude=151.20 + group * 0.01 + rank * 0.001,
                ),
                business_status="OPERATIONAL",
                provider_rank=rank,
            )
            for rank in range(self.per_query)
        ]
        return PlaceSearchResponse(
            candidates=candidates,
            actual_result_count=len(candidates),
            retrieved_at="2026-09-11T00:00:00+00:00",
        )

    async def get_place_reviews(self, request):
        self.reviews_requests.append(request)
        return PlaceReviewsDTO(
            place_id=request.place_id,
            reviews=[
                PlaceReviewDTO(text=REVIEW_SENTINEL),
                PlaceReviewDTO(text="Visitors report this location is crowded."),
            ]
            if self.with_reviews
            else [],
            retrieved_at="2026-09-11T00:00:00+00:00",
        )


class MappingRoutesProvider:
    def __init__(self, *, gaps: bool = False) -> None:
        self.requests = []
        self.gaps = gaps

    async def compute_route_matrix(self, request):
        self.requests.append(request)
        elements = []
        for origin_index, origin in enumerate(request.origins):
            for destination_index, destination in enumerate(request.destinations):
                if (
                    self.gaps
                    and origin_index == 0
                    and destination_index == 1
                    and origin.place_id != destination.place_id
                ):
                    continue
                not_found = (
                    self.gaps
                    and origin_index == 0
                    and destination_index == 2
                    and origin.place_id != destination.place_id
                )
                elements.append(
                    {
                        "originIndex": origin_index,
                        "destinationIndex": destination_index,
                        "status": {},
                        "condition": "ROUTE_NOT_FOUND" if not_found else "ROUTE_EXISTS",
                        **({} if not_found else {"distanceMeters": 400, "duration": "300s"}),
                    }
                )
        return RouteMatrixDTO(
            elements=elements,
            retrieved_at="2026-09-11T00:00:00+00:00",
        )


def requirements(
    days: int,
    *,
    required: list[str] | None = None,
    preferences: list[str] | None = None,
) -> TravelRequirements:
    return TravelRequirements(
        destination="Sydney",
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 12) + timedelta(days=days - 1),
        traveler_count=2,
        required_activities=required or ["museums", "beaches", "wildlife"],
        preferences=preferences or ["walking"],
    )


def itinerary_for(req: TravelRequirements) -> V1Itinerary:
    days = (req.end_date - req.start_date).days + 1
    return V1Itinerary(
        destination="Sydney",
        start_date=req.start_date,
        end_date=req.end_date,
        days=[
            ItineraryDay(date=req.start_date + timedelta(days=index), activities=[])
            for index in range(days)
        ],
    )


def run_graph(
    req: TravelRequirements,
    *,
    per_query: int,
    limits: ToolBudgetLimits | None = None,
    named_first: str | None = None,
    details_failure_ids: set[str] | None = None,
    gaps: bool = False,
    llm=None,
    with_reviews: bool = False,
    named_place_intents: tuple[NamedPlaceIntent, ...] = (),
):
    places = ManyPlacesProvider(
        per_query=per_query,
        named_first=named_first,
        details_failure_ids=details_failure_ids,
        with_reviews=with_reviews,
    )
    weather = FakeWeatherProvider()
    routes = MappingRoutesProvider(gaps=gaps)
    tracer = RecordingTracer()
    budget = ToolBudget(limits)
    client = llm or FakeStructuredLLMClient(
        [make_extraction(req, intents=named_place_intents), itinerary_for(req)]
    )
    service = V1EvidenceAcquisitionService(
        places_provider=places,
        weather_provider=weather,
        routes_provider=routes,
        budget=budget,
        cache=RequestCache(),
        tracer=tracer,
    )
    request = make_request(
        requirements=req,
        additional_preferences="Plan Sydney walking-only. "
        + " ".join(req.preferences)
        + " "
        + " ".join(item.source_text for item in named_place_intents),
    )
    graph = build_v1_graph(client, service, tracer)
    state = asyncio.run(graph.ainvoke({"request": request, "reference_date": REFERENCE_DATE}))
    return state, client, places, weather, routes, budget, tracer


def test_v1_planner_records_bounded_cost_projection_without_another_llm_call() -> None:
    req = requirements(1)
    itinerary = itinerary_for(req)
    itinerary.set_cost_projections(
        (
            EstimatedCostProjectionDiagnostic(
                field_path="days[0].activities[0].estimated_cost",
                projection="midpoint_from_range",
                currency="SGD",
                lower_bound="1.00",
                upper_bound="10.00",
                midpoint="5.50",
            ),
        )
    )
    llm = FakeStructuredLLMClient([make_extraction(req), itinerary])

    state, _, _, _, _, _, tracer = run_graph(req, per_query=1, llm=llm)

    assert state["itinerary"].start_date == req.start_date
    assert len(llm.calls) == 2
    diagnostics = [payload for name, payload in tracer.events if name == "estimated_cost_projected"]
    assert diagnostics == [itinerary.cost_projections[0].as_trace_payload()]
    assert "itinerary_dates_validated" in [name for name, _ in tracer.events]


@pytest.mark.parametrize(
    ("days", "final_pois", "per_query", "expected_calls"),
    [(4, 9, 5, 2), (7, 16, 7, 4)],
)
def test_active_selection_routes_and_planner_preserve_final_order(
    days: int, final_pois: int, per_query: int, expected_calls: int
) -> None:
    req = requirements(days)
    limits = ToolBudgetLimits(max_final_pois=final_pois, max_route_matrix_elements=16)
    state, llm, places, weather, routes, budget, tracer = run_graph(
        req, per_query=per_query, limits=limits
    )

    funnel = state["candidate_funnel"]
    selection = state["review_selection"]
    expected_ids = selection.selected_place_ids
    assert len(expected_ids) == final_pois
    assert not selection.profiles
    assert set(expected_ids) <= {p.candidate.place_id for p in funnel.enriched_candidates}
    assert [item.place_id for item in state["selected_candidates"]] == list(expected_ids)
    assert [item.place_id for item in state["place_evidence"]] == list(expected_ids)
    assert project_selected_places(funnel, selection) == (
        state["selected_candidates"],
        state["place_evidence"],
    )
    assert len(places.details_requests) == funnel.capacities.r_pool
    assert len(weather.requests) == 1
    assert len(routes.requests) == expected_calls
    assert all(
        [item.place_id for item in request.destinations] == list(expected_ids)
        for request in routes.requests
    )
    assert [item.place_id for request in routes.requests for item in request.origins] == list(
        expected_ids
    )
    baseline = state["route_evidence"].baseline
    assert len(baseline.elements) == final_pois**2
    assert [(item.origin_place_id, item.destination_place_id) for item in baseline.elements] == [
        (origin, destination) for origin in expected_ids for destination in expected_ids
    ]
    assert len(llm.calls) == 2
    prompt = llm.calls[-1].user_prompt
    assert prompt.index(expected_ids[0]) < prompt.index(expected_ids[1])
    assert "PRIVATE_RAW_REVIEW_TEXT" not in prompt
    assert "<requirement_conflicts>\n[]\n</requirement_conflicts>" in prompt
    summary = budget.summary()
    assert summary["final_pois"]["used"] == final_pois
    assert summary["baseline_route_matrix_elements"]["used"] == final_pois**2
    assert summary["baseline_route_matrix_calls"]["used"] == expected_calls
    assert summary["route_matrix_elements"]["used"] == 0
    assert summary["review_detail_calls"]["used"] == 0
    assert not places.reviews_requests
    names = [name for name, _ in tracer.events]
    assert names.index("interpreted_requirements_validated") < names.index("date_window_validated")
    assert names.index("date_window_validated") < names.index("destination_resolved")
    assert names.index("destination_resolved") < names.index("planning_supply_completed")
    assert names.index("planning_supply_completed") < names.index("weather_completed")
    assert names.index("weather_completed") < names.index("route_matrix_completed")
    assert names.index("route_matrix_completed") < names.index("generation_completed")
    assert names.index("generation_completed") < names.index("itinerary_dates_validated")
    assert names.count("route_baseline_chunk_completed") == expected_calls
    assert "semantic_candidate_admission" in names
    hours_events = [
        payload for name, payload in tracer.events if name == "opening_hours_planning_views_created"
    ]
    assert len(hours_events) == 1
    assert [item["place_id"] for item in hours_events[0]["places"]] == list(expected_ids)
    assert all(len(item["date_bases"]) == days for item in hours_events[0]["places"])
    chunk_events = [
        payload for name, payload in tracer.events if name == "route_baseline_chunk_completed"
    ]
    assert sum(event["requested_elements"] for event in chunk_events) == final_pois**2
    assert all(event["requested_elements"] <= 64 for event in chunk_events)
    route_lookups = [
        payload
        for name, payload in tracer.events
        if name == "request_cache_lookup" and payload["operation"] == "route_matrix"
    ]
    assert len(route_lookups) == expected_calls
    assert all(item["outcome"] == "success" and not item["cache_hit"] for item in route_lookups)


def test_unresolved_and_unsatisfied_named_must_visits_block_generation() -> None:
    req = requirements(1, required=["Australian Museum", "museums"])
    named = NamedPlaceIntent(
        place_text="Australian Museum",
        inclusion=NamedPlaceInclusion.REQUIRED,
        source_text="Visit Australian Museum",
    )
    with pytest.raises(ClarificationRequired, match="unresolved_named_identity"):
        run_graph(req, per_query=3, named_place_intents=(named,))
    with pytest.raises(ClarificationRequired, match="required_place_details_unusable"):
        run_graph(
            req,
            per_query=3,
            named_first="Australian Museum",
            details_failure_ids={"poi-0-0"},
            named_place_intents=(named,),
        )


def test_typed_required_place_survives_active_final_selection_and_trace() -> None:
    req = requirements(1, required=["Visit the Sydney Opera House", "harbour views"])
    named = NamedPlaceIntent(
        place_text="Sydney Opera House",
        inclusion=NamedPlaceInclusion.REQUIRED,
        source_text="I want to visit Sydney Opera House",
    )
    state, _, places, _, _, _, tracer = run_graph(
        req,
        per_query=4,
        named_first="Sydney Opera House",
        named_place_intents=(named,),
    )
    funnel = state["candidate_funnel"]
    assert funnel.named_place_resolutions[0].resolved_place_id == "poi-0-0"
    assert funnel.must_visit_place_ids == frozenset({"poi-0-0"})
    assert state["review_selection"].selected_place_ids[0] == "poi-0-0"
    assert state["review_selection"].final_selection.selected[0].must_visit
    assert [item.term for item in funnel.search_intents].count("Sydney Opera House") == 1
    assert not any(
        request.text_query == "Visit the Sydney Opera House in Sydney"
        for request in places.search_requests
    )
    completed = next(
        payload for name, payload in tracer.events if name == "planning_supply_completed"
    )
    assert "poi-0-0" in completed["selected_ids"]
    from backend.app.services.planning_supply_pipeline import planner_supply_projection

    view = planner_supply_projection(state["review_selection"], state["interpreted_requirements"])
    assert view["required_canonical_ids"] == ("poi-0-0",)
    assert "poi-0-0" not in view["optional_canonical_ids"]
    assert view["optional_canonical_ids"]
    assert "suitable subset" in view["instructions"]
    # The fake itinerary deliberately schedules no options; V1 does not repair it.
    assert all(not day.activities for day in state["itinerary"].days)


class ReviewProfileLLM:
    def __init__(self, req: TravelRequirements) -> None:
        self.req = req
        self.calls: list[tuple[type, str]] = []

    async def generate_structured(self, *, system_prompt, user_prompt, response_schema):
        self.calls.append((response_schema, user_prompt))
        if response_schema is TripIntentExtractionResult:
            return make_extraction(
                self.req,
                experience=(("avoid crowds", "crowding"),),
            )
        if response_schema is ExperienceProfileDraft:
            place_id = json.loads(user_prompt)["place_id"]
            crowded = place_id == "poi-0-0"
            return ExperienceProfileDraft(
                place_id=place_id,
                summary=(
                    "Visitors report crowds." if crowded else "Visitors report calm conditions."
                ),
                summary_review_refs=["review_1", "review_2"],
                signals=[
                    ExperienceSignalDraft(
                        dimension=ExperienceDimension.CROWDING,
                        value=ExperienceValue.HIGH if crowded else ExperienceValue.LOW,
                        review_refs=["review_1", "review_2"],
                    )
                ],
                review_count_used=2,
            )
        if response_schema is V1Itinerary:
            return itinerary_for(self.req)
        raise AssertionError("Unexpected response schema")


def test_review_relations_are_available_but_raw_reviews_stay_out_of_planner() -> None:
    req = requirements(1, required=["museums", "beaches"], preferences=["avoid crowds"])
    llm = ReviewProfileLLM(req)
    limits = ToolBudgetLimits(
        max_final_pois=1,
        max_review_enriched_places=1,
        max_review_detail_calls=1,
        max_experience_profile_llm_calls=1,
    )
    state, _, places, _, _, budget, tracer = run_graph(
        req, per_query=1, limits=limits, llm=llm, with_reviews=True
    )
    assert state["review_selection"].evaluator_calls == 0
    assert {schema for schema, _ in llm.calls} <= {
        TripIntentExtractionResult, ExperienceProfileDraft, V1Itinerary
    }
    assert len(places.reviews_requests) == 1
    assert len(state["review_selection"].profiles) == 1
    assert budget.summary()["review_enriched_places"]["used"] == 1
    assert budget.summary()["review_detail_calls"]["used"] == 1
    assert budget.summary()["experience_profile_llm_calls"]["used"] == 1
    generation_prompt = next(prompt for schema, prompt in llm.calls if schema is V1Itinerary)
    for forbidden in (
        REVIEW_SENTINEL,
        "Visitors report crowds.",
        "Visitors report calm conditions.",
        "summary_review_refs",
        "minimum_flip_magnitude",
        "q_rel",
        "c_cov",
        "g_geo",
        "r_rating",
        "e_exp",
    ):
        assert forbidden not in generation_prompt
    assert REVIEW_SENTINEL not in repr(tracer.events)
    assert REVIEW_SENTINEL not in repr(tracer.payloads)
    assert any(name == "planning_supply_completed" for name, _ in tracer.events)


def test_active_supply_has_no_additional_selection_model_call():
    req = requirements(3)
    state, llm, *_ = run_graph(req, per_query=4)
    selection = state["review_selection"]
    assert len(selection.selected_place_ids) == 8
    assert selection.subset_enumerator_calls == selection.evaluator_calls == 0
    assert len(llm.calls) == 2


def test_missing_route_observation_is_not_provider_confirmed_route_not_found() -> None:
    state, llm, _, _, _, _, tracer = run_graph(requirements(4), per_query=5, gaps=True)
    elements = state["route_evidence"].baseline.elements
    missing = [
        item for item in elements if item.evidence_type is RouteElementEvidenceType.NOT_OBSERVED
    ]
    confirmed = [
        item
        for item in elements
        if item.evidence_type is RouteElementEvidenceType.PROVIDER_OBSERVED
        and item.condition == "ROUTE_NOT_FOUND"
    ]
    assert missing and confirmed
    assert all(item.duration_seconds is None for item in missing + confirmed)
    assert all(item.condition is None for item in missing)
    assert "not_observed means no usable measurement" in llm.calls[-1].system_prompt
    route_event = next(
        payload for name, payload in tracer.events if name == "route_matrix_completed"
    )
    assert sum(route_event["not_observed_reasons"].values()) == len(missing)
    assert route_event["provider_route_not_found_count"] == len(confirmed)


def _file_tracer(root: Path, request: PlanningRequest) -> FileRunTracer:
    return FileRunTracer(
        RunTraceContext(
            run_id=RUN_ID,
            system_version="v1",
            reference_date=REFERENCE_DATE,
            date_window=create_trip_date_window(REFERENCE_DATE),
            request=request,
            started_at=datetime(2026, 9, 11, tzinfo=UTC),
        ),
        root=root,
        payload_mode=TracePayloadMode.RAW,
        raw_provider_payloads=True,
    )


def test_active_file_trace_excludes_review_inputs_and_redacts_secrets(tmp_path: Path) -> None:
    from backend.app.runtime.config_loader import load_runtime_config
    from backend.app.runtime.config_models import AcquisitionConfig

    req = requirements(1, required=["museums", "beaches"], preferences=["avoid crowds"])
    request = make_request(
        requirements=req,
        additional_preferences=(
            "Plan Sydney walking-only. avoid crowds. api_key=hidden-example-secret"
        ),
    )
    tracer = _file_tracer(tmp_path, request)
    llm = ReviewProfileLLM(req)
    places = ManyPlacesProvider(per_query=1, with_reviews=True)
    limits = ToolBudgetLimits(
        max_final_pois=1,
        max_review_enriched_places=1,
        max_review_detail_calls=1,
        max_experience_profile_llm_calls=1,
    )
    result = asyncio.run(
        run_v1(
            request,
            llm,
            places,
            FakeWeatherProvider(),
            MappingRoutesProvider(),
            reference_date=REFERENCE_DATE,
            runtime_config=load_runtime_config().model_copy(
                update={"acquisition": AcquisitionConfig(policy_id="conservative_1")}
            ),
            budget_limits=limits,
            tracer=tracer,
        )
    )
    trace_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in tracer.run_directory.rglob("*")
        if path.is_file()
    )
    assert result.itinerary == itinerary_for(req)
    assert len(places.reviews_requests) == 1
    assert "semantic_candidate_admission" in trace_text
    assert "planning_supply_completed" in trace_text
    assert "route_baseline_chunk_completed" in trace_text
    assert REVIEW_SENTINEL not in trace_text
    assert "hidden-example-secret" not in trace_text
    assert "[REDACTED]" in trace_text


def test_trace_write_failure_does_not_change_active_planning_result(tmp_path: Path) -> None:
    req = requirements(1)
    request = make_request(additional_preferences="Plan Sydney walking-only.", requirements=req)
    baseline = asyncio.run(
        run_v1(
            request,
            FakeStructuredLLMClient([make_extraction(req), itinerary_for(req)]),
            ManyPlacesProvider(per_query=2),
            FakeWeatherProvider(),
            MappingRoutesProvider(),
            reference_date=REFERENCE_DATE,
            tracer=NullRunTracer(RUN_ID),
        )
    )
    tracer = _file_tracer(tmp_path, request)
    tracer._events_path = tmp_path / "missing" / "events.jsonl"
    with_failed_trace = asyncio.run(
        run_v1(
            request,
            FakeStructuredLLMClient([make_extraction(req), itinerary_for(req)]),
            ManyPlacesProvider(per_query=2),
            FakeWeatherProvider(),
            MappingRoutesProvider(),
            reference_date=REFERENCE_DATE,
            tracer=tracer,
        )
    )
    # Wall-clock telemetry is not part of the deterministic planning result.
    exclude = {
        "planning_supply": {
            "elapsed_seconds": True,
            "cpu_seconds": True,
            "acquisition_diagnostics": {"elapsed_seconds"},
        }
    }
    assert with_failed_trace.model_dump(exclude=exclude) == baseline.model_dump(exclude=exclude)
