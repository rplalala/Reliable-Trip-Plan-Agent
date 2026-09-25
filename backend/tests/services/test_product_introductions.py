"""Product decoration makes at most one call and cannot replan or invalidate an itinerary."""

import asyncio
from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest

from backend.app.services.product_introductions import (
    Introduction,
    IntroductionBatch,
    IntroductionClient,
    ProductIntroductions,
)
from backend.tests.services.test_product_presentation import example


@pytest.mark.parametrize("outcome", ["success", "failure", "timeout", "unknown_id", "cancel"])
def test_one_batch_is_optional_and_closes_resources(outcome):
    result, evidence = example()
    evidence.deadline = 100
    evidence.summaries["left-place"] = "Existing summary."
    calls, closed = [], []

    class Client:
        async def generate(self, places):
            calls.append(places)
            if outcome == "failure":
                raise RuntimeError("PRIVATE")
            if outcome == "timeout":
                await asyncio.Event().wait()
            if outcome == "cancel":
                raise asyncio.CancelledError()
            return IntroductionBatch(
                introductions=[
                    Introduction(
                        activity_id="invented"
                        if outcome == "unknown_id"
                        else places[0]["activity_id"],
                        text="A short introduction.",
                    )
                ]
            )

    @asynccontextmanager
    async def factory():
        try:
            yield Client()
        finally:
            closed.append(True)

    original = result.itinerary.model_dump()
    service = ProductIntroductions(factory, timeout_seconds=0.02, clock=lambda: 90)
    if outcome == "cancel":
        with pytest.raises(asyncio.CancelledError):
            asyncio.run(service.generate(result.itinerary, evidence))
    else:
        output = asyncio.run(service.generate(result.itinerary, evidence))
        assert bool(output) == (outcome == "success")
    assert len(calls) == 1 and closed == [True]
    assert calls[0][0]["summary"] == "Existing summary."
    assert result.itinerary.model_dump() == original


def test_insufficient_remaining_time_never_constructs_client():
    result, evidence = example()
    evidence.deadline = 90

    def forbidden():
        pytest.fail("No remaining request time")

    assert (
        asyncio.run(
            ProductIntroductions(forbidden, clock=lambda: 90).generate(result.itinerary, evidence)
        )
        == {}
    )


def test_presentation_adapter_uses_one_structured_response_call():
    calls = []

    class Responses:
        async def create(self, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(output_text='{"introductions": []}')

    client = IntroductionClient(SimpleNamespace(responses=Responses()), "test-deployment")
    output = asyncio.run(client.generate([{"activity_id": "a", "summary": None}]))
    assert not output.introductions and len(calls) == 1
    assert calls[0]["text"]["format"]["strict"] is True
    assert "tools" not in calls[0]


def test_only_main_places_are_sent_and_timeout_uses_remaining_allowance(monkeypatch):
    result, evidence = example()
    evidence.deadline = 93
    result.itinerary.days[0].activities[1].activity_kind = "free_time"
    received = []
    service = ProductIntroductions(clock=lambda: 90)

    async def generate(places, timeout):
        received.append((places, timeout))
        return {}

    monkeypatch.setattr(service, "_generate", generate)
    asyncio.run(service.generate(result.itinerary, evidence))
    assert len(received) == 1 and len(received[0][0]) == 1
    assert received[0][1] == 3  # No fresh 30/600-second allowance after planning.
    assert received[0][0][0]["summary"] is None  # Missing context is not invented.
