"""Real runner wiring with fake-only providers and explicit phase ordering."""

import asyncio
from datetime import date
from uuid import uuid4

import pytest

from backend.app.observability.run_trace import NullRunTracer
from backend.app.policies.trip_dates import TripDatePolicyError
from backend.app.runtime.config_models import ReferenceDiscoveryConfig
from backend.app.schemas.itinerary_projection import V1Itinerary
from backend.app.versions.v1.graph import V1StageError
from backend.app.versions.v1.runner import run_v1
from backend.tests.request_fixtures import make_request
from backend.tests.services.test_reference_discovery import candidate, response
from backend.tests.versions.v0.fakes import FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    make_itinerary,
)


class Trace(NullRunTracer):
    def __init__(self):
        super().__init__(uuid4())
        self.events = []
        self.data = {}

    def event(self, name, data=None):
        self.events.append(name)
        self.data[name] = data


class NearbyFake(FakePlacesProvider):
    def __init__(self, tracer):
        super().__init__()
        self.tracer = tracer
        self.nearby_requests = []

    async def search_nearby(self, request):
        assert "itinerary_dates_validated" in self.tracer.events
        assert "generation_completed" in self.tracer.events
        self.nearby_requests.append(request)
        value = candidate().model_copy(update={"location": request.center})
        return response(value)


def main_output():
    data = make_itinerary().model_dump()
    data["output_version"] = "itinerary_2"
    data["days"][0]["activities"][0]["source_place_id"] = "poi-0-0"
    return V1Itinerary.model_validate(data)


def test_post_stage_runner_does_not_add_other_acquisition_or_model_calls():
    from backend.app.runtime.config_loader import load_runtime_config

    records = []
    original = main_output()
    for budget in (0, 3):
        tracer = Trace()
        places, weather, routes = NearbyFake(tracer), FakeWeatherProvider(), FakeRoutesProvider()
        llm = FakeStructuredLLMClient([original])
        result = asyncio.run(
            run_v1(
                make_request(),
                llm,
                places,
                weather,
                routes,
                reference_date=date(2026, 9, 11),
                tracer=tracer,
                runtime_config=load_runtime_config().model_copy(
                    update={"reference_discovery": ReferenceDiscoveryConfig(max_requests=budget)}
                ),
            )
        )
        records.append(
            (
                llm.calls,
                places.search_requests,
                places.details_requests,
                places.reviews_requests,
                weather.requests,
                routes.requests,
            )
        )
        assert len(llm.calls) == 1
        assert len(places.nearby_requests) == (1 if budget else 0)
        assert len(result.itinerary.reference_recommendations) == (1 if budget else 0)
        assert result.itinerary.model_dump(
            exclude={"reference_recommendations"}
        ) == original.model_dump(exclude={"reference_recommendations"})
        assert result.output_role_summary.scheduled_place_ids == ("poi-0-0",)
        assert result.output_role_summary.reference_place_ids == (("new",) if budget else ())
        assert tracer.data["reference_supply_relationship"]["references_outside_supply_ids"] == (
            ["new"] if budget else []
        )
        assert not any("semantic_evaluat" in event for event in tracer.events)
    assert records[0] == records[1]


@pytest.mark.parametrize("failure", ["generation", "identity", "dates", "model_reference"])
def test_primary_failure_prevents_nearby(failure):
    tracer = Trace()
    places = NearbyFake(tracer)
    output = main_output()
    if failure == "generation":
        output = RuntimeError("fake generation failure")
    elif failure == "identity":
        output.days[0].activities[0].source_place_id = "outside"
    elif failure == "dates":
        output = output.model_copy(update={"end_date": date(2026, 9, 14)})
    else:
        from backend.app.schemas.itinerary import ReferenceRecommendation

        output.reference_recommendations = [
            ReferenceRecommendation(
                place_name="Hidden model fallback", source_place_id="poi-0-1", reason="Not allowed"
            )
        ]
    with pytest.raises((V1StageError, TripDatePolicyError)):
        asyncio.run(
            run_v1(
                make_request(),
                FakeStructuredLLMClient([output]),
                places,
                FakeWeatherProvider(),
                FakeRoutesProvider(),
                reference_date=date(2026, 9, 11),
                tracer=tracer,
            )
        )
    assert places.nearby_requests == []
