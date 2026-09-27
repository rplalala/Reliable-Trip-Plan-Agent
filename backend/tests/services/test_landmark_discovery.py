"""Offline planning entry tests observe real search sends and final supply metadata."""

import asyncio
from datetime import date, timedelta

import pytest

from backend.app.integrations.models import PlaceSearchResponse
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.schemas.interpreted_requirements import InterpretationDraft
from backend.app.services.preference_interpretation import empty_preference_draft
from backend.app.versions.v1.runner import run_v1
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    RevisedFakeLLM,
    _candidate,
    make_itinerary,
)


def run_case(
    names,
    *,
    named=(),
    interests=0,
    pools=None,
    search_limit=12,
    rejected=(),
    exclusive=False,
    scheduled_id=None,
    supported_interests=None,
    closed=(),
    destination="Sydney",
    days=2,
    focus=False,
    combined_intent=False,
):
    text = (
        "; ".join(
            [
                *(name for name, inclusion in named),
                *(f"Interest {i}" for i in range(interests)),
                *(["This trip focuses on Interest 0"] if focus else []),
            ]
        )
        or "Plan a trip"
    )
    data = empty_preference_draft().model_dump()
    data["named_places"] = [
        dict(place_text=name, inclusion=inclusion, source_refs=[dict(quote=name, occurrence=0)])
        for name, inclusion in named
    ]
    data["semantic_requirements"] = [
        dict(
            local_key=f"r{i}",
            normalized_text=f"Interest {i}",
            kind="preference",
            polarity="favor",
            strength="medium",
            scope="selected_poi_set",
            subject_target={"kind": "party"},
            source_refs=[dict(quote=f"Interest {i}", occurrence=0)],
            experience_goal=dict(
                frequency="continuing",
                count=None,
                target="category",
                distinct_dates=False,
                explicit_primary_exception=False,
                trip_scope="exclusive" if exclusive else "ordinary",
            ),
        )
        for i in range(interests)
    ]
    data["discovery_intents"] = [
        dict(requirement_refs=[f"r{i}"], purpose="activity_or_category", query_text=f"Interest {i}")
        for i in range(interests)
    ]
    if combined_intent:
        data["discovery_intents"] = [
            dict(
                requirement_refs=[f"r{i}" for i in range(interests)],
                purpose="activity_or_category",
                query_text="Interest 0",
            )
        ]
    if focus:
        data["semantic_requirements"][0]["kind"] = "goal"
        data["semantic_requirements"][0]["scope"] = "whole_trip"
        data["semantic_requirements"][0]["trip_focus_source"] = dict(
            quote="This trip focuses on Interest 0", occurrence=0
        )
        data["semantic_requirements"][0]["source_refs"].append(
            dict(quote="This trip focuses on Interest 0", occurrence=0)
        )
        data["semantic_requirements"][0]["experience_goal"]["trip_scope"] = "ordinary"
    draft = InterpretationDraft.model_validate(data)

    class Model(RevisedFakeLLM):
        nominations = 0

        async def generate_landmark_nomination_structured(self, **kwargs):
            self.nominations += 1
            assert "Interest" not in kwargs["user_prompt"]
            if isinstance(names, Exception):
                raise names
            return {"names": names}

        async def generate_poi_semantics_structured(self, **kwargs):
            output = await super().generate_poi_semantics_structured(**kwargs)
            if supported_interests is not None:
                import json

                payload = json.loads(kwargs["user_prompt"])
                for row in output["assessments"]:
                    row["matches"] = [
                        dict(
                            requirement_id=r["requirement_id"],
                            relation="supported"
                            if i in supported_interests.get(row["visit_object"], ())
                            else "mismatch",
                            evidence_refs=row["evidence_refs"],
                        )
                        for i, r in enumerate(payload["requirements"])
                    ]
            for row in output["assessments"]:
                if row["visit_object"] in rejected:
                    row["role"] = "non_main"
            return output

    class Places(FakePlacesProvider):
        async def search_text(self, request):
            if request.location_bias is None:
                return await super().search_text(request)
            self.search_requests.append(request)
            rows = (pools or {}).get(
                request.text_query, [("poi-0-0", "Old Tower"), ("poi-0-1", "City Museum")]
            )
            candidates = [
                _candidate(pid, rank, -33.86, 151.20).model_copy(update={"display_name": name})
                for rank, (pid, name) in enumerate(rows)
            ]
            return PlaceSearchResponse(
                candidates=candidates,
                actual_result_count=len(candidates),
                retrieved_at="2026-09-11T00:00:00+00:00",
            )

        async def get_place_details(self, request):
            details = await super().get_place_details(request)
            if request.place_id in closed:
                return details.model_copy(update={"business_status": "CLOSED_PERMANENTLY"})
            for search in self.search_requests:
                if search.location_bias is None:
                    continue
                for pid, name in (pools or {}).get(
                    search.text_query, [("poi-0-0", "Old Tower"), ("poi-0-1", "City Museum")]
                ):
                    if pid == request.place_id:
                        return details.model_copy(update={"display_name": name})
            return details

    config = load_runtime_config()
    config = config.model_copy(
        update={
            "budget": config.budget.model_copy(
                update={
                    "places": config.budget.places.model_copy(
                        update={"candidate_search_calls": search_limit}
                    )
                }
            )
        }
    )
    trip = make_itinerary()
    trip.destination = destination
    trip.end_date = trip.start_date + timedelta(days=days - 1)
    template = trip.days[0]
    trip.days = []
    for i in range(days):
        day = template.model_copy(deep=True)
        day.date = trip.start_date + timedelta(days=i)
        for activity in day.activities:
            activity.activity_id = f"activity-{i}"
            activity.start_time += timedelta(days=i)
            activity.end_time += timedelta(days=i)
        trip.days.append(day)
    if scheduled_id:
        trip.days[0].activities[0].source_place_id = scheduled_id
        trip.days[0].activities[0].activity_kind = "main_poi"
        for rows in (pools or {}).values():
            for pid, name in rows:
                if pid == scheduled_id:
                    trip.days[0].activities[0].place_name = name
    model, places = Model([draft, trip]), Places()
    result = asyncio.run(
        run_v1(
            make_request(text, destination=destination, end_date=trip.end_date),
            model,
            places,
            FakeWeatherProvider(),
            FakeRoutesProvider(),
            reference_date=date(2026, 9, 11),
            runtime_config=config,
        )
    )
    return result, model, places


def test_many_interests_keep_general_discovery_and_four_supplements_inside_twelve():
    result, model, places = run_case(
        [f"Landmark {i}" for i in range(12)],
        named=(("Old Tower", "REQUIRED"), ("City Museum", "OPTIONAL")),
        interests=8,
    )
    queries = [r.text_query for r in places.search_requests[1:]]
    assert queries[:3] == [
        "Old Tower in Sydney",
        "City Museum in Sydney",
        "top attractions in Sydney",
    ]
    assert len(queries) == 12
    assert sum(q.startswith("Landmark") for q in queries) == 4
    assert model.nominations == 1
    assert result.planning_supply.nomination_diagnostics["supplementary_sends"] == 4


def test_unspent_supplements_return_to_preference_discovery():
    result, _, places = run_case(["Old Tower"], interests=8)
    queries = [r.text_query for r in places.search_requests[1:]]
    assert len(queries) == 9
    assert all(f"Interest {i} in Sydney" in queries for i in range(8))
    assert result.planning_supply.nomination_diagnostics["supplementary_sends"] == 0


def test_named_budget_exhaustion_reports_skipped_general_without_overrun():
    result, _, places = run_case(["Old Tower"], named=(("Old Tower", "REQUIRED"),), search_limit=1)
    assert len(places.search_requests) == 2  # Separate destination + one candidate send.
    assert result.planning_supply.nomination_diagnostics["general_status"] == "budget_not_attempted"


@pytest.mark.parametrize(
    "names,pools",
    [
        (
            ["Old Tower"],
            {"top attractions in Sydney": [("poi-0-0", "Old Tower"), ("poi-0-1", "Old Tower")]},
        ),
        (["Tower alias"], {}),
    ],
)
def test_ambiguous_and_alias_names_do_not_acquire_landmark_identity(names, pools):
    result, _, _ = run_case(names, pools=pools)
    assert result.planning_supply.landmarks == {}
    assert result.planning_supply.nomination_diagnostics["status"] == "degraded"


@pytest.mark.parametrize("failure", [RuntimeError("fixture failure"), []])
def test_auxiliary_failure_keeps_existing_qualified_supply(failure):
    result, model, _ = run_case(failure)
    assert result.planning_supply.selected_place_ids
    assert not result.planning_supply.landmarks
    assert model.nominations == 1


def test_named_exclusion_and_non_primary_role_override_nomination():
    result, _, _ = run_case(["Old Tower"], named=(("Old Tower", "EXCLUDED"),))
    assert "poi-0-0" not in result.planning_supply.selected_place_ids
    result, _, _ = run_case(["Old Tower"], rejected=("Old Tower",))
    assert "poi-0-0" not in result.planning_supply.selected_place_ids


def test_exclusive_scope_does_not_admit_an_unsupported_nomination():
    result, _, _ = run_case(["Old Tower"], interests=1, exclusive=True)
    assert "poi-0-0" not in result.planning_supply.selected_place_ids


def test_supplementary_exact_name_is_usable_in_final_schedule():
    result, _, places = run_case(
        ["Third Monument"],
        pools={
            "Third Monument in Sydney": [("poi-0-2", "Third Monument")],
        },
        scheduled_id="poi-0-2",
    )
    assert result.itinerary.days[0].activities[0].source_place_id == "poi-0-2"
    assert result.planning_supply.landmarks["poi-0-2"].name == "Third Monument"
    assert result.planning_supply.nomination_diagnostics["supplementary_sends"] == 1
    assert (
        len([q for q in places.search_requests if q.text_query == "Third Monument in Sydney"]) == 1
    )


def test_duplicate_supplement_queries_reuse_cache_and_do_not_spend_extra_sends():
    result, _, places = run_case(["Unknown Place"] * 12)
    assert result.planning_supply.nomination_diagnostics["supplementary_sends"] == 1
    assert (
        len([q for q in places.search_requests if q.text_query == "Unknown Place in Sydney"]) == 1
    )


def test_failed_auxiliary_does_not_swallow_required_identity_failure():
    from backend.app.schemas.interpreted_requirements import ClarificationRequired

    with pytest.raises(ClarificationRequired, match="unresolved_named_identity"):
        run_case(RuntimeError("auxiliary failed"), named=(("Absent Required", "REQUIRED"),))
