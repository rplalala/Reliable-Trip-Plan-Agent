"""Accepted source facts through real version runners with offline providers."""

import asyncio
from datetime import date

import pytest

from backend.app.versions.v1.runner import run_v1
from backend.app.versions.v2.runner import run_v2
from backend.tests.request_fixtures import make_request
from backend.tests.services.test_tripworld_discovery import Retrieval
from backend.tests.versions.v0.fakes import FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import FakeRoutesProvider, FakeWeatherProvider
from backend.tests.versions.v2.test_v2_runner import Places
from backend.tests.versions.v3.test_wiring import ManyPlaces, Model, execute, primary


class RecordedPlaces(Places):
    def __init__(self):
        super().__init__()
        self.observations = {}

    async def get_place_details(self, request):
        response = await super().get_place_details(request)
        self.observations[response.place_id] = response
        return response


@pytest.mark.parametrize("runner", [run_v1, run_v2])
def test_runner_canonicalizes_primary_facts_without_editing_model(runner):
    raw = primary(False)
    for day in raw.days:
        for activity in day.activities:
            activity.place_name = "Model alias"
            activity.location = "Abbreviated model address"
    before = raw.model_dump()
    places = RecordedPlaces()
    kwargs = {"retrieval_factory": lambda: Retrieval([])} if runner == run_v2 else {}
    result = asyncio.run(
        runner(
            make_request(),
            FakeStructuredLLMClient([raw]),
            places,
            FakeWeatherProvider(),
            FakeRoutesProvider(),
            reference_date=date(2026, 9, 11),
            **kwargs,
        )
    )
    for day in result.itinerary.days:
        for activity in day.activities:
            evidence = places.observations[activity.source_place_id]
            assert activity.location == evidence.formatted_address
            assert activity.place_name == evidence.display_name
            original = next(
                a for d in raw.days for a in d.activities if a.activity_id == activity.activity_id
            )
            assert (activity.start_time, activity.end_time) == (
                original.start_time,
                original.end_time,
            )
    assert raw.model_dump() == before


@pytest.mark.parametrize(
    "behavior,overlap", [("complete", True), ("failure", True), ("complete", False)]
)
def test_v3_draft_and_final_keep_canonical_facts_across_repair(behavior, overlap):
    raw = primary(overlap)
    for day in raw.days:
        for activity in day.activities:
            activity.location = "Abbreviated model address"
    before = raw.model_dump()
    places = RecordedPlaces()
    result, model, _, _ = asyncio.run(execute(Model(raw, behavior), places=places))
    for itinerary in (result.v3.draft, result.v3.final_primary, result.itinerary):
        for day in itinerary.days:
            for activity in day.activities:
                assert (
                    activity.location
                    == places.observations[activity.source_place_id].formatted_address
                )
                assert (
                    activity.place_name
                    == places.observations[activity.source_place_id].display_name
                )
    assert raw.model_dump() == before
    if overlap:
        assert model.repair_calls > 0
        assert result.v3.repair.status == (
            "REJECTED" if behavior == "failure" else "ACCEPTED_COMPLETE"
        )
    else:
        assert model.repair_calls == 0


def test_v3_verified_addition_and_retained_visits_share_canonical_address_rule():
    class RecordedManyPlaces(ManyPlaces):
        def __init__(self):
            super().__init__()
            self.observations = {}

        async def get_place_details(self, request):
            response = await super().get_place_details(request)
            self.observations[response.place_id] = response
            return response

    places = RecordedManyPlaces()
    result, _, _, _ = asyncio.run(
        execute(
            Model(primary(False), "add"),
            places=places,
            quantity_review_enabled=True,
        )
    )
    added = set(result.v3.repair.final_place_ids) - set(result.planning_supply.selected_place_ids)
    assert len(added) == 1
    for day in result.itinerary.days:
        for activity in day.activities:
            assert (
                activity.location == places.observations[activity.source_place_id].formatted_address
            )
            assert activity.place_name == places.observations[activity.source_place_id].display_name
