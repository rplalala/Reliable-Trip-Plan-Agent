"""Offline service-level V1-A review enrichment tests; no graph integration."""

import asyncio
from dataclasses import replace
from uuid import UUID

from backend.app.evidence.experience_models import (
    ExperienceDimension,
    ExperienceProfileDraft,
    ExperienceSignalDraft,
    ExperienceValue,
)
from backend.app.integrations.models import PlaceReviewDTO, PlaceReviewsDTO, PlaceReviewsRequest
from backend.app.observability.run_trace import NullRunTracer
from backend.app.policies.poi_capacity import apply_poi_operating_budgets, derive_poi_capacities
from backend.app.policies.poi_funnel import MergedSearchObservations
from backend.app.policies.poi_selection import select_pois
from backend.app.runtime.budget import ToolBudget, ToolBudgetKey, ToolBudgetLimits
from backend.app.runtime.cache import RequestCache
from backend.app.services.evidence_acquisition import CandidateFunnelResult
from backend.app.services.review_selection import ReviewSelectionService
from backend.tests.policies.test_experience_selection import (
    WINDOW,
    requirements,
    selection_place,
)


class FakeReviewsProvider:
    def __init__(self, values: dict[str, list[str] | Exception]) -> None:
        self.values = values
        self.requests: list[PlaceReviewsRequest] = []

    async def get_place_reviews(self, request: PlaceReviewsRequest) -> PlaceReviewsDTO:
        self.requests.append(request)
        value = self.values[request.place_id]
        if isinstance(value, Exception):
            raise value
        return PlaceReviewsDTO(
            place_id=request.place_id,
            reviews=[PlaceReviewDTO(text=text) for text in value],
            retrieved_at="2026-09-11T00:00:00+00:00",
        )


class FakeProfileLLM:
    def __init__(self, value: ExperienceProfileDraft | Exception) -> None:
        self.value = value
        self.calls: list[tuple[str, str, type]] = []

    async def generate_structured(
        self, *, system_prompt: str, user_prompt: str, response_schema: type
    ) -> ExperienceProfileDraft:
        self.calls.append((system_prompt, user_prompt, response_schema))
        if isinstance(self.value, Exception):
            raise self.value
        return self.value


class RecordingTracer(NullRunTracer):
    def __init__(self) -> None:
        super().__init__(UUID(int=2))
        self.events: list[tuple[str, object]] = []

    def event(self, event_type: str, payload: object | None = None) -> None:
        self.events.append((event_type, payload))


def draft(place_id: str = "a", *, refs: list[str] | None = None) -> ExperienceProfileDraft:
    refs = refs or ["review_1", "review_2"]
    return ExperienceProfileDraft(
        place_id=place_id,
        summary="Visitors report crowds.",
        summary_review_refs=refs,
        signals=[
            ExperienceSignalDraft(
                dimension=ExperienceDimension.CROWDING,
                value=ExperienceValue.HIGH,
                review_refs=refs,
            )
        ],
        review_count_used=2,
    )


def funnel(limits: ToolBudgetLimits) -> CandidateFunnelResult:
    req = requirements("avoid crowds")
    places = (selection_place("a", 4.0), selection_place("b", 3.8))
    capacities = apply_poi_operating_budgets(
        derive_poi_capacities(req.start_date, req.end_date, WINDOW), limits
    )
    baseline = select_pois(
        places,
        start_date=req.start_date,
        end_date=req.end_date,
        window=WINDOW,
        capacity=capacities.k_final,
    )
    return CandidateFunnelResult(
        capacities=capacities,
        search_intents=(),
        named_place_resolutions=(),
        observations=places,
        merged=MergedSearchObservations(places, 2),
        c_raw_selection=baseline,
        c_raw_candidates=places,
        r_pool_selection=baseline,
        rating_contenders=("a", "b"),
        enriched_candidates=places,
        details_failures=(),
        no_review_selection=baseline,
        conflicts=(),
        must_visit_place_ids=frozenset(),
        excluded_place_ids=frozenset(),
        unresolved_required_names=(),
    )


def setup(
    provider: FakeReviewsProvider,
    llm: FakeProfileLLM,
    *,
    limits: ToolBudgetLimits | None = None,
    tracer: NullRunTracer | None = None,
) -> tuple[ReviewSelectionService, ToolBudget, CandidateFunnelResult]:
    limits = limits or ToolBudgetLimits(
        max_final_pois=1,
        max_review_enriched_places=2,
        max_review_detail_calls=2,
        max_experience_profile_llm_calls=2,
    )
    budget = ToolBudget(limits)
    return (
        ReviewSelectionService(
            places_provider=provider,
            llm_client=llm,
            llm_config_identity="test-deployment",
            budget=budget,
            cache=RequestCache(),
            tracer=tracer or NullRunTracer(UUID(int=1)),
        ),
        budget,
        funnel(limits),
    )


def test_review_aware_selection_changes_membership_without_changing_places() -> None:
    provider = FakeReviewsProvider({"a": ["Crowded.", "Very busy."], "b": []})
    llm = FakeProfileLLM(draft())
    service, budget, baseline = setup(provider, llm)
    before = baseline.enriched_candidates[0].structured_evidence

    result = asyncio.run(
        service.run(funnel=baseline, requirements=requirements("avoid crowds"), window=WINDOW)
    )

    assert baseline.no_review_selection.selected_place_ids == ("a",)
    assert result.selected_place_ids == ("b",)
    assert dict(result.experience_scores)["a"].total == -10
    assert {item.place_id: item for item in result.profiles}["a"].signals[0].review_refs == (
        "review_1",
        "review_2",
    )
    assert baseline.enriched_candidates[0].structured_evidence == before
    assert all("reviews" in request.field_mask for request in provider.requests)
    assert all("rating" not in request.field_mask for request in provider.requests)
    assert len(llm.calls) == 1
    assert budget.summary()[ToolBudgetKey.REVIEW_ENRICHED_PLACES.value]["used"] == len(
        result.attempts
    )
    assert budget.summary()[ToolBudgetKey.REVIEW_DETAIL_CALLS.value]["used"] == len(
        provider.requests
    )
    assert budget.summary()[ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS.value]["used"] == 1


def test_no_explicit_need_or_guaranteed_must_visit_avoids_review_calls() -> None:
    provider = FakeReviewsProvider({"a": ["Crowded."], "b": ["Quiet."]})
    llm = FakeProfileLLM(draft())
    service, _, baseline = setup(provider, llm)
    no_need = asyncio.run(
        service.run(funnel=baseline, requirements=requirements("beaches"), window=WINDOW)
    )
    assert no_need.attempts == ()
    assert no_need.selected_place_ids == baseline.no_review_selection.selected_place_ids
    assert provider.requests == []
    must = replace(baseline, must_visit_place_ids=frozenset({"a"}))
    must_result = asyncio.run(
        service.run(funnel=must, requirements=requirements("avoid crowds"), window=WINDOW)
    )
    assert must_result.attempts == ()


def test_provider_and_profile_failures_are_explicit_and_not_retried() -> None:
    provider = FakeReviewsProvider({"a": RuntimeError("offline"), "b": []})
    llm = FakeProfileLLM(draft())
    service, budget, baseline = setup(provider, llm)
    result = asyncio.run(
        service.run(funnel=baseline, requirements=requirements("avoid crowds"), window=WINDOW)
    )
    assert result.stop_reason == "insufficient_review_evidence"
    assert result.selected_place_ids == baseline.no_review_selection.selected_place_ids
    assert len(provider.requests) == 2
    assert len(llm.calls) == 0
    assert all(item.availability.value == "unavailable" for item in result.profiles)
    assert budget.summary()[ToolBudgetKey.REVIEW_DETAIL_CALLS.value]["used"] == 2


def test_profile_invalid_refs_fail_without_repair() -> None:
    provider = FakeReviewsProvider({"a": ["Crowded.", "Very busy."], "b": []})
    llm = FakeProfileLLM(draft(refs=["missing"]))
    service, budget, baseline = setup(provider, llm)
    result = asyncio.run(
        service.run(funnel=baseline, requirements=requirements("avoid crowds"), window=WINDOW)
    )
    assert all(item.availability.value == "unavailable" for item in result.profiles)
    assert all(item.total == 0 for _, item in result.experience_scores)
    assert len(llm.calls) == 1
    assert budget.summary()[ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS.value]["used"] == 1


def test_review_and_profile_cache_hits_do_not_consume_http_or_llm_budget() -> None:
    provider = FakeReviewsProvider({"a": ["Crowded.", "Very busy."]})
    llm = FakeProfileLLM(draft())
    service, budget, _ = setup(provider, llm)
    first, _ = asyncio.run(service._reviews("a"))
    second, _ = asyncio.run(service._reviews("a"))
    assert first == second
    assert len(provider.requests) == 1
    from backend.app.policies.experience_profile import preprocess_reviews

    reviews = preprocess_reviews(first, place_id="a")
    first_profile = asyncio.run(service._profile("a", reviews, first.retrieved_at))
    second_profile = asyncio.run(service._profile("a", reviews, first.retrieved_at))
    assert first_profile == second_profile
    assert len(llm.calls) == 1
    assert budget.summary()[ToolBudgetKey.REVIEW_DETAIL_CALLS.value]["used"] == 1
    assert budget.summary()[ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS.value]["used"] == 1


def test_review_pool_cap_stops_without_filling_provider_budget() -> None:
    provider = FakeReviewsProvider({"a": ["Crowded."], "b": []})
    llm = FakeProfileLLM(draft())
    limits = ToolBudgetLimits(
        max_final_pois=1,
        max_review_enriched_places=1,
        max_review_detail_calls=2,
        max_experience_profile_llm_calls=2,
    )
    service, budget, baseline = setup(provider, llm, limits=limits)
    result = asyncio.run(
        service.run(funnel=baseline, requirements=requirements("avoid crowds"), window=WINDOW)
    )
    assert result.stop_reason == "review_pool_cap_exhausted"
    assert len(result.attempts) == len(provider.requests) == 1
    assert budget.summary()[ToolBudgetKey.REVIEW_ENRICHED_PLACES.value]["used"] == 1
    assert budget.summary()[ToolBudgetKey.REVIEW_DETAIL_CALLS.value]["used"] == 1


def test_profile_llm_failure_is_unavailable_with_no_retry() -> None:
    provider = FakeReviewsProvider({"a": ["Crowded.", "Very busy."], "b": []})
    llm = FakeProfileLLM(RuntimeError("model unavailable"))
    service, budget, baseline = setup(provider, llm)
    before = tuple(item.structured_evidence for item in baseline.enriched_candidates)
    result = asyncio.run(
        service.run(funnel=baseline, requirements=requirements("avoid crowds"), window=WINDOW)
    )
    assert len(llm.calls) == 1
    assert all(item.availability.value == "unavailable" for item in result.profiles)
    assert all(item.total == 0 for _, item in result.experience_scores)
    assert tuple(item.structured_evidence for item in baseline.enriched_candidates) == before
    assert budget.summary()[ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS.value]["used"] == 1


def test_profile_cache_identity_changes_with_review_content() -> None:
    provider = FakeReviewsProvider({"a": ["Crowded.", "Very busy."]})
    llm = FakeProfileLLM(draft())
    service, budget, _ = setup(provider, llm)
    from backend.app.policies.experience_profile import preprocess_reviews

    first = preprocess_reviews(
        PlaceReviewsDTO(
            place_id="a",
            reviews=[PlaceReviewDTO(text="Crowded."), PlaceReviewDTO(text="Busy.")],
            retrieved_at="now",
        ),
        place_id="a",
    )
    second = preprocess_reviews(
        PlaceReviewsDTO(
            place_id="a",
            reviews=[PlaceReviewDTO(text="Quiet."), PlaceReviewDTO(text="Calm.")],
            retrieved_at="now",
        ),
        place_id="a",
    )
    asyncio.run(service._profile("a", first, "now"))
    asyncio.run(service._profile("a", second, "now"))
    assert len(llm.calls) == 2
    assert budget.summary()[ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS.value]["used"] == 2


def test_review_trace_records_sensitivity_attempt_and_final_reason_without_raw_text() -> None:
    provider = FakeReviewsProvider({"a": ["Crowded.", "Very busy."], "b": []})
    llm = FakeProfileLLM(draft())
    tracer = RecordingTracer()
    service, _, baseline = setup(provider, llm, tracer=tracer)
    asyncio.run(
        service.run(funnel=baseline, requirements=requirements("avoid crowds"), window=WINDOW)
    )
    kinds = [kind for kind, _ in tracer.events]
    assert "v1_review_sensitivity_evaluated" in kinds
    assert "v1_review_attempt_started" in kinds
    assert "v1_review_selection_completed" in kinds
    assert "Crowded." not in repr(tracer.events)


def test_review_http_budget_exhaustion_stops_before_provider_call() -> None:
    provider = FakeReviewsProvider({"a": ["Crowded."], "b": []})
    llm = FakeProfileLLM(draft())
    service, budget, baseline = setup(provider, llm)
    budget.consume(ToolBudgetKey.REVIEW_DETAIL_CALLS, 2)
    result = asyncio.run(
        service.run(funnel=baseline, requirements=requirements("avoid crowds"), window=WINDOW)
    )
    assert result.stop_reason == "safety_budget_exhausted"
    assert len(result.attempts) == 1
    assert len(provider.requests) == 0
    assert budget.summary()[ToolBudgetKey.REVIEW_ENRICHED_PLACES.value]["used"] == 1


def test_cached_review_still_consumes_distinct_poi_pool_slot() -> None:
    provider = FakeReviewsProvider({"a": ["Crowded.", "Very busy."], "b": []})
    llm = FakeProfileLLM(draft())
    service, budget, baseline = setup(provider, llm)
    asyncio.run(service._reviews("b"))
    assert len(provider.requests) == 1
    result = asyncio.run(
        service.run(funnel=baseline, requirements=requirements("avoid crowds"), window=WINDOW)
    )
    assert len(result.attempts) == 2
    assert [request.place_id for request in provider.requests] == ["b", "a"]
    assert budget.summary()[ToolBudgetKey.REVIEW_ENRICHED_PLACES.value]["used"] == 2
    assert budget.summary()[ToolBudgetKey.REVIEW_DETAIL_CALLS.value]["used"] == 2
