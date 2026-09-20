"""Offline service-level V1-A review enrichment tests; no graph integration."""

import asyncio
from uuid import UUID

from backend.app.evidence.experience_models import (
    ExperienceDimension,
    ExperienceProfileDraft,
    ExperienceSignalDraft,
    ExperienceValue,
)
from backend.app.integrations.models import PlaceReviewDTO, PlaceReviewsDTO, PlaceReviewsRequest
from backend.app.observability.run_trace import NullRunTracer
from backend.app.runtime.budget import ToolBudget, ToolBudgetLimits
from backend.app.runtime.cache import RequestCache
from backend.app.services.review_selection import ReviewSelectionService


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


def setup(provider, llm, limits=None):
    budget = ToolBudget(limits or ToolBudgetLimits())
    return ReviewSelectionService(
        places_provider=provider,
        llm_client=llm,
        llm_config_identity="test",
        budget=budget,
        cache=RequestCache(),
        tracer=NullRunTracer(UUID(int=1)),
    ), budget


def test_profile_cache_preserves_budget_and_signal():
    provider = FakeReviewsProvider({"a": ["Crowded venue.", "Queues and crowds."]})
    llm = FakeProfileLLM(draft())
    service, budget = setup(provider, llm)

    async def run():
        first = await service.acquire_profile("a")
        before = budget.summary()
        second = await service.acquire_profile("a")
        assert first == second
        assert budget.summary() == before
        assert first.signals[0].value == "HIGH"

    asyncio.run(run())
    assert len(provider.requests) == len(llm.calls) == 1


def test_failed_provider_does_not_retry_or_call_profile():
    provider = FakeReviewsProvider({"a": RuntimeError("offline")})
    llm = FakeProfileLLM(draft())
    service, _ = setup(provider, llm)
    profile = asyncio.run(service.acquire_profile("a"))
    assert profile.availability == "unavailable"
    assert len(provider.requests) == 1 and llm.calls == []


def test_invalid_profile_refs_fail_without_repair():
    provider = FakeReviewsProvider({"a": ["Crowds here.", "Long queues."]})
    llm = FakeProfileLLM(draft(refs=["invented"]))
    service, _ = setup(provider, llm)
    assert asyncio.run(service.acquire_profile("a")).availability == "unavailable"
    assert len(llm.calls) == 1


def test_profile_budget_exhaustion_stays_bounded():
    provider = FakeReviewsProvider({"a": ["Crowds here."], "b": ["Crowds here."]})
    service, budget = setup(
        provider, FakeProfileLLM(draft()), ToolBudgetLimits(max_review_enriched_places=1)
    )
    asyncio.run(service.acquire_profile("a"))
    assert asyncio.run(service.acquire_profile("b")).availability == "unavailable"
    assert len(provider.requests) == 1
