"""Fresh offline V2 runs reuse main planning and preserve independent V1 behavior."""

import asyncio
from datetime import date

import pytest

from backend.app.integrations.models import LatLng, PlaceNearbySearchRequest, PlaceSearchResponse
from backend.app.schemas.planning import SystemVersion
from backend.app.versions.v1.runner import run_v1
from backend.app.versions.v2.runner import run_v2
from backend.tests.request_fixtures import make_request
from backend.tests.services.test_tripworld_discovery import Retrieval, details, hit
from backend.tests.versions.v0.fakes import FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    make_itinerary,
)


@pytest.fixture(autouse=True)
def query_tokens(monkeypatch):
    from types import SimpleNamespace

    monkeypatch.setattr(
        "backend.app.policies.tripworld_query_plan.tokenizer",
        lambda: SimpleNamespace(encode_ordinary=lambda text: list(text)),
    )


class Places(FakePlacesProvider):
    def __init__(self):
        super().__init__()
        self.nearby = []

    async def get_place_details(self, request):
        if request.place_id == "aaa-rag":
            self.details_requests.append(request)
            return details("aaa-rag", primary_type="museum")
        return await super().get_place_details(request)

    async def search_nearby(self, request: PlaceNearbySearchRequest):
        self.nearby.append(request)
        return PlaceSearchResponse(
            candidates=[], actual_result_count=0, retrieved_at="2026-09-19T00:00:00Z"
        )


def test_v2_new_identity_in_supply_and_schedule_nearby_uses_scheduled_anchor():
    itinerary = make_itinerary()
    itinerary.days[0].activities[0].source_place_id = "aaa-rag"
    itinerary.days[0].activities[0].place_name = "aaa-rag"
    llm, places = FakeStructuredLLMClient([itinerary]), Places()
    retrieval = Retrieval([hit("aaa-rag")])
    result = asyncio.run(
        run_v2(
            make_request(),
            llm,
            places,
            FakeWeatherProvider(),
            FakeRoutesProvider(),
            reference_date=date(2026, 9, 11),
            retrieval_factory=lambda: retrieval,
        )
    )
    assert result.system_version == SystemVersion.V2
    assert result.rag_discovery["config"]["sql_timeout"] == 60
    assert result.rag_discovery["config"]["deadline_seconds"] == 360
    assert len(llm.calls) == 1
    assert result.rag_discovery["fate"]["scheduled"] == ["aaa-rag"]
    assert result.rag_discovery["fate"]["supplied"] == ["aaa-rag"]
    assert len(result.planning_supply.selected_place_ids) == 10
    assert [r.place_id for r in places.details_requests].count("aaa-rag") == 1
    assert len(places.nearby) == 1
    assert places.nearby[0].center == LatLng(latitude=-33.86, longitude=151.2)
    assert result.itinerary.reference_recommendations == []


def test_v2_database_failure_has_v1_call_and_supply_parity_but_stays_v2():
    async def scenario():
        outputs, providers = [], []
        for runner in (run_v1, run_v2):
            places, llm = Places(), FakeStructuredLLMClient([make_itinerary()])
            kwargs = (
                {"retrieval_factory": lambda: Retrieval([], fail=True)} if runner == run_v2 else {}
            )
            outputs.append(
                await runner(
                    make_request(),
                    llm,
                    places,
                    FakeWeatherProvider(),
                    FakeRoutesProvider(),
                    reference_date=date(2026, 9, 11),
                    **kwargs,
                )
            )
            providers.append(places)
        assert outputs[0].system_version == SystemVersion.V1
        assert outputs[1].system_version == SystemVersion.V2
        assert outputs[1].rag_discovery["status"] == "unavailable"
        assert outputs[0].itinerary == outputs[1].itinerary
        assert (
            outputs[0].planning_supply.selected_place_ids
            == outputs[1].planning_supply.selected_place_ids
        )
        assert providers[0].search_requests == providers[1].search_requests
        assert providers[0].details_requests == providers[1].details_requests

    asyncio.run(scenario())


def test_v1_rejects_hidden_retrieval_injection():
    with pytest.raises(ValueError, match="Version dependencies"):
        asyncio.run(
            run_v1(make_request(), None, None, None, None, discovery_factory=lambda _: None)
        )


def test_unresolved_required_stops_before_rag_and_nearby():
    from backend.app.schemas.interpreted_requirements import ClarificationRequired
    from backend.app.schemas.named_place_intent import NamedPlaceIntent
    from backend.tests.versions.v1.fakes import make_revised_extraction

    text = "Visit Missing Place."
    extraction = make_revised_extraction(
        intents=(
            NamedPlaceIntent(place_text="Missing Place", inclusion="REQUIRED", source_text=text),
        )
    )
    places = Places()
    with pytest.raises(ClarificationRequired, match="unresolved_named_identity"):
        asyncio.run(
            run_v2(
                make_request(text),
                FakeStructuredLLMClient([extraction]),
                places,
                FakeWeatherProvider(),
                FakeRoutesProvider(),
                reference_date=date(2026, 9, 11),
                retrieval_factory=lambda: pytest.fail("RAG must not start"),
            )
        )
    assert not places.nearby


def test_default_quality_policy_rejects_conflicting_rag_override_before_acquisition():
    from backend.app.versions.v2.config import RAGConfig

    with pytest.raises(ValueError, match="Historical RAG override"):
        asyncio.run(
            run_v2(
                make_request(), None, None, None, None,
                rag_config=RAGConfig(sql_timeout=60, deadline_seconds=180),
            )
        )
