"""Offline V1-A Phase 3 acquisition-to-selection funnel tests."""

import asyncio
from datetime import date
from uuid import UUID

from backend.app.evidence.models import DestinationContext
from backend.app.evidence.selection_models import RatingAcquisitionState
from backend.app.integrations.google.places import PLACES_DETAILS_FIELD_MASK
from backend.app.integrations.models import (
    LatLng,
    PlaceCandidateDTO,
    PlaceDetailsDTO,
    PlaceDetailsRequest,
    PlaceOpeningDateDTO,
    PlaceReviewsRequest,
    PlaceSearchRequest,
    PlaceSearchResponse,
)
from backend.app.observability.run_trace import NullRunTracer
from backend.app.policies.poi_funnel import (
    NamedPlaceResolutionStatus,
    build_place_search_intents,
    merge_search_observations,
)
from backend.app.policies.poi_selection import DateRisk
from backend.app.policies.trip_dates import create_trip_date_window
from backend.app.runtime.budget import ToolBudget, ToolBudgetKey, ToolBudgetLimits
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.named_place_intent import NamedPlaceInclusion, NamedPlaceIntent
from backend.app.schemas.request import TravelRequirements
from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService
from backend.tests.versions.v1.fakes import FakeRoutesProvider, FakeWeatherProvider

WINDOW = create_trip_date_window(date(2026, 9, 11))
DESTINATION = DestinationContext(place_id="sydney", name="Sydney", latitude=-33.87, longitude=151.2)


def _candidate(
    place_id: str,
    name: str,
    rank: int,
    *,
    status: str = "OPERATIONAL",
    opening: PlaceOpeningDateDTO | None = None,
) -> PlaceCandidateDTO:
    return PlaceCandidateDTO(
        place_id=place_id,
        display_name=name,
        location=LatLng(latitude=-33.87, longitude=151.2),
        business_status=status,
        opening_date=opening,
        provider_rank=rank,
    )


class ScriptedPlacesProvider:
    def __init__(
        self,
        searches: dict[str, list[PlaceCandidateDTO]],
        *,
        ratings: dict[str, float | None] | None = None,
        detail_failures: set[str] | None = None,
        detail_openings: dict[str, PlaceOpeningDateDTO] | None = None,
        search_failures: set[str] | None = None,
    ) -> None:
        self.searches = searches
        self.ratings = ratings or {}
        self.detail_failures = detail_failures or set()
        self.detail_openings = detail_openings or {}
        self.search_failures = search_failures or set()
        self.search_requests: list[PlaceSearchRequest] = []
        self.details_requests: list[PlaceDetailsRequest] = []
        self.reviews_requests: list[PlaceReviewsRequest] = []
        self.by_id = {item.place_id: item for group in searches.values() for item in group}

    async def search_text(self, request: PlaceSearchRequest) -> PlaceSearchResponse:
        self.search_requests.append(request)
        if request.text_query in self.search_failures:
            raise RuntimeError("search unavailable")
        candidates = self.searches.get(request.text_query, [])
        return PlaceSearchResponse(
            candidates=candidates,
            actual_result_count=len(candidates),
            retrieved_at="2026-09-11T00:00:00+00:00",
        )

    async def get_place_details(self, request: PlaceDetailsRequest) -> PlaceDetailsDTO:
        self.details_requests.append(request)
        if request.place_id in self.detail_failures:
            raise RuntimeError("details unavailable")
        candidate = self.by_id[request.place_id]
        return PlaceDetailsDTO(
            place_id=request.place_id,
            display_name=candidate.display_name,
            location=candidate.location,
            business_status=candidate.business_status,
            opening_date=self.detail_openings.get(request.place_id, candidate.opening_date),
            rating=self.ratings.get(request.place_id, 4.0),
            website_uri=f"https://example.org/{request.place_id}",
            retrieved_at="2026-09-11T00:00:00+00:00",
        )

    async def get_place_reviews(self, request: PlaceReviewsRequest):
        self.reviews_requests.append(request)
        raise AssertionError("Phase 3 must never fetch reviews")


def _requirements(
    required: list[str] | None = None,
    preferences: list[str] | None = None,
    *,
    days: int = 1,
) -> TravelRequirements:
    return TravelRequirements(
        destination="Sydney",
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 11 + days),
        required_activities=required or [],
        preferences=preferences or [],
    )


def _named(
    name: str, inclusion: NamedPlaceInclusion = NamedPlaceInclusion.REQUIRED
) -> NamedPlaceIntent:
    return NamedPlaceIntent(
        place_text=name,
        inclusion=inclusion,
        source_text=f"Visit {name}",
    )


class RecordingTracer(NullRunTracer):
    def __init__(self) -> None:
        super().__init__(UUID("00000000-0000-0000-0000-000000000027"))
        self.events: list[tuple[str, object | None]] = []

    def event(self, event_type: str, payload: object | None = None) -> None:
        self.events.append((event_type, payload))


def _service(
    provider: ScriptedPlacesProvider,
    *,
    limits: ToolBudgetLimits | None = None,
    tracer: NullRunTracer | None = None,
) -> tuple[V1EvidenceAcquisitionService, ToolBudget]:
    budget = ToolBudget(limits or ToolBudgetLimits())
    service = V1EvidenceAcquisitionService(
        places_provider=provider,
        weather_provider=FakeWeatherProvider(),
        routes_provider=FakeRoutesProvider(),
        budget=budget,
        cache=RequestCache(),
        tracer=tracer or NullRunTracer(UUID("00000000-0000-0000-0000-000000000001")),
    )
    return service, budget


def test_full_no_review_funnel_preserves_multi_intent_hits_and_actual_rating() -> None:
    provider = ScriptedPlacesProvider(
        {
            "Australian Museum in Sydney": [
                _candidate("other", "Other", 0),
                _candidate("museum", "Australian Museum", 1),
            ],
            "museums in Sydney": [
                _candidate("museum", "Australian Museum", 0),
                _candidate("gallery", "Gallery", 1),
            ],
            "harbour views in Sydney": [_candidate("harbour", "Harbour Lookout", 0)],
        },
        ratings={"museum": 4.8, "other": None},
    )
    service, budget = _service(provider)
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["Australian Museum", "museums"], ["harbour views"]),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(_named("Australian Museum"),),
        )
    )
    assert result.finality == "pending_review_enrichment"
    assert result.capacities.algorithmic.c_raw == 20
    assert result.merged.raw_observation_count == 5
    assert len(result.merged.places) == 4
    museum = next(item for item in result.merged.places if item.candidate.place_id == "museum")
    assert [(hit.provider_rank, hit.actual_result_count) for hit in museum.query_hits] == [
        (1, 2),
        (0, 2),
    ]
    assert result.search_intents[0].named_place_intent.place_text == "Australian Museum"
    assert result.c_raw_selection.selected_place_ids[0] == "museum"
    assert result.r_pool_selection.selected_place_ids[0] == "museum"
    assert result.no_review_selection.selected_place_ids[0] == "museum"
    assert result.no_review_selection.selected[0].must_visit
    enriched = {item.candidate.place_id: item for item in result.enriched_candidates}
    assert enriched["museum"].rating == 4.8
    assert enriched["other"].rating_state is RatingAcquisitionState.MISSING
    assert all(
        request.field_mask == PLACES_DETAILS_FIELD_MASK for request in provider.details_requests
    )
    assert "reviews" not in PLACES_DETAILS_FIELD_MASK
    assert not provider.reviews_requests
    assert budget.summary()[ToolBudgetKey.CANDIDATES.value]["used"] == 4
    assert budget.summary()[ToolBudgetKey.PLACE_DETAIL_CALLS.value]["used"] == 4
    assert budget.summary()[ToolBudgetKey.REVIEW_DETAIL_CALLS.value]["used"] == 0
    assert budget.summary()[ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS.value]["used"] == 0
    assert all(
        selected.score is None or selected.score.e_exp == 0
        for selected in result.no_review_selection.selected
    )


def test_raw_unique_cap_protects_low_rank_must_visit_and_deduplicates() -> None:
    provider = ScriptedPlacesProvider(
        {
            "Australian Museum in Sydney": [
                _candidate("a", "A", 0),
                _candidate("b", "B", 1),
                _candidate("must", "Australian Museum", 2),
            ],
            "museums in Sydney": [_candidate("a", "A", 0), _candidate("c", "C", 1)],
        }
    )
    service, budget = _service(provider, limits=ToolBudgetLimits(max_candidates=2))
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["Australian Museum", "museums"]),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(_named("Australian Museum"),),
        )
    )
    assert len(result.observations) == 5
    assert len(result.merged.places) == 4
    assert len(result.c_raw_candidates) == 2
    assert result.c_raw_candidates[0].candidate.place_id == "must"
    assert budget.summary()[ToolBudgetKey.CANDIDATES.value]["used"] == 2
    assert result.capacities.limiting_budgets == ("c_raw", "r_pool", "k_final")


def test_r_pool_is_a_maximum_and_details_attempts_follow_neutral_priority() -> None:
    provider = ScriptedPlacesProvider(
        {
            "museums in Sydney": [
                _candidate(f"poi-{rank}", f"POI {rank}", rank) for rank in range(12)
            ]
        }
    )
    service, budget = _service(provider, limits=ToolBudgetLimits(max_place_detail_calls=3))
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["museums"]), destination=DESTINATION, window=WINDOW
        )
    )
    assert len(result.c_raw_candidates) == 12
    assert result.rating_contenders == ("poi-0", "poi-1", "poi-2")
    assert [request.place_id for request in provider.details_requests] == list(
        result.rating_contenders
    )
    assert budget.summary()["place_detail_calls"]["used"] == 3
    assert result.capacities.limiting_budgets == ("r_pool", "k_final")


def test_more_valid_named_must_visits_than_r_pool_reports_capacity_conflict() -> None:
    names = ("Named A", "Named B", "Named C")
    provider = ScriptedPlacesProvider(
        {
            f"{name} in Sydney": [_candidate(f"id-{index}", name, 0)]
            for index, name in enumerate(names)
        }
    )
    service, _ = _service(provider, limits=ToolBudgetLimits(max_place_detail_calls=2))
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(list(names)),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=tuple(_named(name) for name in names),
        )
    )
    assert len(result.rating_contenders) == 2
    assert len(provider.details_requests) == 2
    assert any(item.reason == "must_visits_exceed_capacity" for item in result.conflicts)
    assert all(item.must_visit for item in result.no_review_selection.selected)


def test_neutral_provisional_selection_reruns_after_rating_details() -> None:
    provider = ScriptedPlacesProvider(
        {
            "museums in Sydney": [_candidate("first", "First", 0)],
            "beaches in Sydney": [_candidate("second", "Second", 0)],
        },
        ratings={"first": 1.0, "second": 5.0},
    )
    service, _ = _service(provider, limits=ToolBudgetLimits(max_final_pois=1))
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["museums", "beaches"]),
            destination=DESTINATION,
            window=WINDOW,
        )
    )
    assert result.r_pool_selection.selected_place_ids[0] == "first"
    assert result.r_pool_selection.selected[0].score.r_rating == 0
    assert result.no_review_selection.selected_place_ids == ("second",)
    assert result.no_review_selection.selected[0].score.r_rating == 10
    assert result.no_review_selection.selected[0].score.e_exp == 0


def test_details_failure_does_not_reserve_failed_must_visit_slot() -> None:
    provider = ScriptedPlacesProvider(
        {
            "Australian Museum in Sydney": [
                _candidate("must", "Australian Museum", 0),
                _candidate("normal-a", "Normal A", 1),
                _candidate("normal-b", "Normal B", 2),
            ]
        },
        detail_failures={"must"},
    )
    service, _ = _service(provider, limits=ToolBudgetLimits(max_final_pois=2))
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["Australian Museum"]),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(_named("Australian Museum"),),
        )
    )
    assert result.details_failures == (("must", "RuntimeError"),)
    assert result.no_review_selection.selected_place_ids == ("normal-a", "normal-b")
    assert all(not item.must_visit for item in result.no_review_selection.selected)
    assert ("must", "structured_details_failed") in [
        (item.place_id_or_name, item.reason) for item in result.conflicts
    ]


def test_permanently_closed_named_requirement_is_not_substituted_or_slot_reserved() -> None:
    provider = ScriptedPlacesProvider(
        {
            "Australian Museum in Sydney": [
                _candidate("must", "Australian Museum", 0, status="CLOSED_PERMANENTLY"),
                _candidate("normal-a", "Normal A", 1),
                _candidate("normal-b", "Normal B", 2),
            ]
        }
    )
    service, _ = _service(provider, limits=ToolBudgetLimits(max_final_pois=2))
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["Australian Museum"]),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(_named("Australian Museum"),),
        )
    )
    assert result.no_review_selection.selected_place_ids == ("normal-a", "normal-b")
    assert all(not item.must_visit for item in result.no_review_selection.selected)
    assert ("must", "permanently_closed") in [
        (item.place_id_or_name, item.reason) for item in result.conflicts
    ]
    assert {request.place_id for request in provider.details_requests} == {
        "normal-a",
        "normal-b",
    }


def test_cache_hits_do_not_reconsume_search_details_or_candidate_budget() -> None:
    provider = ScriptedPlacesProvider({"museums in Sydney": [_candidate("one", "One", 0)]})
    service, budget = _service(provider, limits=ToolBudgetLimits(max_candidate_search_calls=12))
    kwargs = {
        "requirements": _requirements(["museums"]),
        "destination": DESTINATION,
        "window": WINDOW,
    }
    first = asyncio.run(service.run_candidate_funnel(**kwargs))
    first_usage = budget.summary()
    second = asyncio.run(service.run_candidate_funnel(**kwargs))
    assert first.no_review_selection == second.no_review_selection
    assert len(provider.search_requests) == 3
    assert len(provider.details_requests) == 1
    assert budget.summary() == first_usage


def test_smoke_b_intents_all_execute_with_separate_default_search_budgets() -> None:
    terms = [
        "Sydney Opera House",
        "Australian Museum",
        "museums",
        "harbour attractions",
        "beaches",
        "parks",
        "viewpoints",
        "cultural attractions",
        "major Sydney landmarks",
    ]
    searches = {
        f"{term} in Sydney": [
            _candidate(f"place-{index}", term if index < 2 else f"POI {index}", 0)
        ]
        for index, term in enumerate(terms)
    }
    searches["Sydney"] = [_candidate("sydney", "Sydney", 0)]
    provider = ScriptedPlacesProvider(searches)
    tracer = RecordingTracer()
    service, budget = _service(provider, tracer=tracer)
    requirements = _requirements(terms[:3], terms[3:])
    destination = asyncio.run(service.resolve_destination("Sydney"))
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=requirements,
            destination=destination,
            window=WINDOW,
            named_place_intents=(_named(terms[0]), _named(terms[1])),
        )
    )

    assert [intent.term for intent in result.search_intents] == terms
    assert [intent.kind.value for intent in result.search_intents] == [
        "explicit_requirement",
        "explicit_requirement",
        "explicit_requirement",
        *(["normal_preference"] * 6),
    ]
    assert [item.status for item in result.search_executions] == ["provider_success"] * 9
    assert [request.text_query for request in provider.search_requests] == [
        "Sydney",
        *(f"{term} in Sydney" for term in terms),
    ]
    assert budget.summary()[ToolBudgetKey.DESTINATION_SEARCH_CALLS.value] == {
        "used": 1,
        "limit": 1,
    }
    assert budget.summary()[ToolBudgetKey.CANDIDATE_SEARCH_CALLS.value] == {
        "used": 9,
        "limit": 12,
    }
    assert [item.status for item in result.named_place_resolutions] == [
        NamedPlaceResolutionStatus.RESOLVED,
        NamedPlaceResolutionStatus.RESOLVED,
    ]
    generated = [
        payload for name, payload in tracer.events if name == "candidate_search_intents_generated"
    ]
    assert generated[0]["deduplicated_count"] == 9
    assert (
        len([name for name, _ in tracer.events if name == "candidate_search_intent_completed"]) == 9
    )


def test_reduced_search_budget_marks_skips_but_later_cache_hit_still_works() -> None:
    requirements = _requirements([], ["beaches", "parks", "viewpoints"])
    intents = build_place_search_intents(requirements)
    assert len(intents) == 3
    assert all(item.kind.value == "normal_preference" for item in intents)
    duplicate = intents[0].model_copy(update={"intent_id": "duplicate_beaches"})
    provider = ScriptedPlacesProvider(
        {
            intents[0].query: [_candidate("beach", "Beach", 0)],
            intents[1].query: [_candidate("park", "Park", 0)],
        }
    )
    tracer = RecordingTracer()
    service, budget = _service(
        provider,
        limits=ToolBudgetLimits(max_candidate_search_calls=2),
        tracer=tracer,
    )
    executions = []
    observations = asyncio.run(
        service.search_candidate_observations(
            requirements,
            DESTINATION,
            intents=(*intents, duplicate),
            intent_executions=executions,
        )
    )
    assert [(item.status, item.cache_hit) for item in executions] == [
        ("provider_success", False),
        ("provider_success", False),
        ("budget_not_attempted", False),
        ("provider_success", True),
    ]
    assert len(provider.search_requests) == 2
    assert budget.summary()[ToolBudgetKey.CANDIDATE_SEARCH_CALLS.value]["used"] == 2
    assert [hit.intent_id for item in observations for hit in item.query_hits] == [
        intents[0].intent_id,
        intents[1].intent_id,
        duplicate.intent_id,
    ]
    assert all(
        hit.intent_id != intents[2].intent_id
        for item in merge_search_observations(observations).places
        for hit in item.query_hits
    )
    assert any(
        name == "candidate_search_intent_completed"
        and payload["intent_id"] == intents[2].intent_id
        and payload["status"] == "budget_not_attempted"
        for name, payload in tracer.events
    )


def test_dispatched_failed_search_consumes_candidate_call_and_is_observable() -> None:
    requirements = _requirements([], ["beaches", "parks"])
    intents = build_place_search_intents(requirements)
    provider = ScriptedPlacesProvider(
        {intents[1].query: [_candidate("park", "Park", 0)]},
        search_failures={intents[0].query},
    )
    service, budget = _service(provider, limits=ToolBudgetLimits(max_candidate_search_calls=2))
    executions = []
    observations = asyncio.run(
        service.search_candidate_observations(
            requirements, DESTINATION, intents=intents, intent_executions=executions
        )
    )
    assert [item.status for item in executions] == [
        "provider_failed",
        "provider_success",
        "budget_not_attempted",
    ]
    assert len(provider.search_requests) == 2
    assert budget.summary()[ToolBudgetKey.CANDIDATE_SEARCH_CALLS.value]["used"] == 2
    assert [hit.intent_id for item in observations for hit in item.query_hits] == [
        intents[1].intent_id
    ]


def test_status_and_partial_opening_flow_into_phase2_without_early_exclusion() -> None:
    provider = ScriptedPlacesProvider(
        {
            "top attractions in Sydney": [
                _candidate("temp", "Temp", 0, status="CLOSED_TEMPORARILY"),
                _candidate(
                    "future",
                    "Future",
                    1,
                    status="FUTURE_OPENING",
                    opening=PlaceOpeningDateDTO(year=2026, month=9),
                ),
                _candidate("closed", "Closed", 2, status="CLOSED_PERMANENTLY"),
            ]
        },
        detail_openings={"future": PlaceOpeningDateDTO(year=2026, month=9, day=12)},
    )
    service, _ = _service(provider)
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(), destination=DESTINATION, window=WINDOW
        )
    )
    assert set(result.rating_contenders) == {"temp", "future"}
    assert "closed" not in result.c_raw_selection.selected_place_ids
    enriched = {item.candidate.place_id: item for item in result.enriched_candidates}
    assert enriched["future"].search_opening_date.day is None
    assert enriched["future"].details_opening_date.day == 12
    selected = {item.place_id: item for item in result.no_review_selection.selected}
    assert selected["temp"].date_risk is DateRisk.TEMPORARILY_CLOSED_VERIFY
    assert selected["future"].not_visitable_before == date(2026, 9, 12)


def test_legacy_graph_search_uses_phase2_status_policy_not_old_closed_set() -> None:
    provider = ScriptedPlacesProvider(
        {
            "top attractions in Sydney": [
                _candidate("temp", "Temp", 0, status="CLOSED_TEMPORARILY"),
                _candidate(
                    "future",
                    "Future",
                    1,
                    status="FUTURE_OPENING",
                    opening=PlaceOpeningDateDTO(year=2026, month=9, day=12),
                ),
                _candidate("permanent", "Permanent", 2, status="CLOSED_PERMANENTLY"),
            ]
        }
    )
    service, _ = _service(provider)
    candidates = asyncio.run(service.search_candidates(_requirements(), DESTINATION))
    assert {item.place_id for item in candidates} == {"temp", "future"}


def test_conflicting_opening_date_preserves_uncertainty_without_fabrication() -> None:
    provider = ScriptedPlacesProvider(
        {
            "top attractions in Sydney": [
                _candidate(
                    "future",
                    "Future",
                    0,
                    status="FUTURE_OPENING",
                    opening=PlaceOpeningDateDTO(year=2026, month=9),
                )
            ]
        },
        detail_openings={"future": PlaceOpeningDateDTO(year=2026, month=10)},
    )
    service, _ = _service(provider)
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(), destination=DESTINATION, window=WINDOW
        )
    )
    enriched = result.enriched_candidates[0]
    assert enriched.opening_date_conflict
    assert enriched.search_opening_date.month == 9
    assert enriched.details_opening_date.month == 10
    assert result.no_review_selection.eligibility[0].opening_date_conflict
    assert result.no_review_selection.eligibility[0].not_visitable_before is None
    assert result.no_review_selection.selected_place_ids == ("future",)


def test_smoke_a_shape_reconciles_typed_required_place_once_across_intents() -> None:
    provider = ScriptedPlacesProvider(
        {
            "Sydney Opera House in Sydney": [
                _candidate("opera", "Sydney Opera House", 0),
            ],
            "harbour views in Sydney": [
                _candidate("opera", "Sydney Opera House", 0),
                _candidate("harbour", "Harbour Lookout", 1),
            ],
        }
    )
    tracer = RecordingTracer()
    service, budget = _service(provider, tracer=tracer)
    named = _named("Sydney Opera House")
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["Visit the Sydney Opera House", "harbour views"]),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(named,),
        )
    )

    assert [item.term for item in result.search_intents][:2] == [
        "Sydney Opera House",
        "harbour views",
    ]
    assert "Visit the Sydney Opera House in Sydney" not in [
        item.text_query for item in provider.search_requests
    ]
    assert len([item for item in result.search_intents if item.named_place_intent]) == 1
    assert result.named_place_resolutions[0].status is NamedPlaceResolutionStatus.RESOLVED
    assert result.named_place_resolutions[0].resolved_place_id == "opera"
    assert len(result.observations) == 3
    assert len(result.merged.places) == 2
    opera = next(item for item in result.merged.places if item.candidate.place_id == "opera")
    assert {hit.intent_id for hit in opera.query_hits} == {
        result.search_intents[0].intent_id,
        result.search_intents[1].intent_id,
    }
    assert result.must_visit_place_ids == frozenset({"opera"})
    assert result.unresolved_required_names == ()
    assert result.c_raw_selection.selected_place_ids[0] == "opera"
    assert result.r_pool_selection.selected_place_ids[0] == "opera"
    assert result.no_review_selection.selected_place_ids[0] == "opera"
    assert result.no_review_selection.selected[0].must_visit
    assert [request.place_id for request in provider.details_requests].count("opera") == 1
    assert budget.summary()[ToolBudgetKey.PLACE_DETAIL_CALLS.value]["used"] == 2
    search_event = next(
        payload for name, payload in tracer.events if name == "named_place_search_intents_created"
    )
    assert search_event["intents"][0]["source_text"] == "Visit Sydney Opera House"
    assert search_event["intents"][0]["query"] == "Sydney Opera House in Sydney"
    assert search_event["intents"][0]["weight"] == "1.0"
    reconciliation = next(
        payload for name, payload in tracer.events if name == "named_place_identities_reconciled"
    )
    assert reconciliation["resolutions"][0]["resolved_place_id"] == "opera"
    assert reconciliation["resolutions"][0]["must_visit"] is True
    propagation = next(
        payload for name, payload in tracer.events if name == "named_place_must_visit_propagated"
    )
    assert propagation["places"][0]["c_raw"] is True
    assert propagation["places"][0]["r_pool"] is True
    assert propagation["places"][0]["no_review_final"] is True


def test_optional_named_place_uses_preference_weight_without_must_visit() -> None:
    provider = ScriptedPlacesProvider(
        {"Sydney Opera House in Sydney": [_candidate("opera", "Sydney Opera House", 0)]}
    )
    service, _ = _service(provider)
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["Visit the Sydney Opera House"]),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(_named("Sydney Opera House", NamedPlaceInclusion.OPTIONAL),),
        )
    )
    assert result.search_intents[0].kind.value == "normal_preference"
    assert str(result.search_intents[0].weight) == "0.8"
    assert result.named_place_resolutions[0].resolved_place_id == "opera"
    assert result.must_visit_place_ids == frozenset()
    assert result.no_review_selection.selected[0].must_visit is False


def test_resolved_optional_place_can_lose_normal_final_selection() -> None:
    provider = ScriptedPlacesProvider(
        {
            "museums in Sydney": [_candidate("museum", "Museum of Sydney", 0)],
            "Sydney Opera House in Sydney": [_candidate("opera", "Sydney Opera House", 0)],
        },
        ratings={"museum": 5.0, "opera": 1.0},
    )
    service, _ = _service(provider, limits=ToolBudgetLimits(max_final_pois=1))
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["museums"]),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(_named("Sydney Opera House", NamedPlaceInclusion.OPTIONAL),),
        )
    )
    assert result.named_place_resolutions[0].resolved_place_id == "opera"
    assert result.no_review_selection.selected_place_ids == ("museum",)
    assert result.must_visit_place_ids == frozenset()
    assert not result.conflicts


def test_unresolved_optional_does_not_create_required_conflict() -> None:
    provider = ScriptedPlacesProvider(
        {"top attractions in Sydney": [_candidate("other", "Other Attraction", 0)]}
    )
    service, _ = _service(provider)
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(_named("MCA", NamedPlaceInclusion.OPTIONAL),),
        )
    )
    assert (
        result.named_place_resolutions[0].status
        is NamedPlaceResolutionStatus.NO_EXACT_CANDIDATE_MATCH
    )
    assert result.unresolved_required_names == ()
    assert not result.conflicts
    assert result.no_review_selection.selected_place_ids == ("other",)


def test_required_alias_unresolved_and_ambiguous_exact_name_never_guess_ids() -> None:
    provider = ScriptedPlacesProvider(
        {
            "MCA in Sydney": [_candidate("mca", "Museum of Contemporary Art", 0)],
            "Australian Museum in Sydney": [
                _candidate("museum-a", "Australian Museum", 0),
                _candidate("museum-b", "Australian Museum", 1),
            ],
        }
    )
    service, _ = _service(provider)
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(_named("MCA"), _named("Australian Museum")),
        )
    )
    assert [item.status for item in result.named_place_resolutions] == [
        NamedPlaceResolutionStatus.NO_EXACT_CANDIDATE_MATCH,
        NamedPlaceResolutionStatus.AMBIGUOUS_EXACT_NAME,
    ]
    assert result.must_visit_place_ids == frozenset()
    assert result.unresolved_required_names == ("MCA", "Australian Museum")
    assert {(item.place_id_or_name, item.reason) for item in result.conflicts} >= {
        ("MCA", "required_place_unresolved"),
        ("Australian Museum", "required_place_unresolved"),
    }


def test_base_required_activity_alone_never_creates_named_must_visit() -> None:
    provider = ScriptedPlacesProvider(
        {"Sydney Opera House in Sydney": [_candidate("opera", "Sydney Opera House", 0)]}
    )
    service, _ = _service(provider)
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["Sydney Opera House"]),
            destination=DESTINATION,
            window=WINDOW,
        )
    )
    assert result.named_place_resolutions == ()
    assert result.must_visit_place_ids == frozenset()
    assert result.no_review_selection.selected[0].must_visit is False


def test_required_name_resolves_from_category_query_even_when_own_query_misses() -> None:
    provider = ScriptedPlacesProvider(
        {"museums in Sydney": [_candidate("museum", "Australian Museum", 0)]}
    )
    service, _ = _service(provider)
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["museums"]),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(_named("Australian Museum"),),
        )
    )
    assert result.named_place_resolutions[0].status is NamedPlaceResolutionStatus.RESOLVED
    assert result.must_visit_place_ids == frozenset({"museum"})
    assert result.no_review_selection.selected[0].must_visit is True


def test_failed_named_search_is_distinct_from_no_exact_candidate_match() -> None:
    provider = ScriptedPlacesProvider(
        {"museums in Sydney": [_candidate("other", "Other Museum", 0)]},
        search_failures={"Australian Museum in Sydney"},
    )
    service, _ = _service(provider)
    result = asyncio.run(
        service.run_candidate_funnel(
            requirements=_requirements(["museums"]),
            destination=DESTINATION,
            window=WINDOW,
            named_place_intents=(_named("Australian Museum"),),
        )
    )
    assert result.named_place_resolutions[0].status is NamedPlaceResolutionStatus.SEARCH_FAILED
    assert result.unresolved_required_names == ("Australian Museum",)
    assert ("Australian Museum", "required_place_unresolved") in [
        (item.place_id_or_name, item.reason) for item in result.conflicts
    ]
