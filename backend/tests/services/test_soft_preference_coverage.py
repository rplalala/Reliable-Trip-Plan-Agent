"""Controlled planning inputs verify soft coverage mechanics, not model accuracy."""

import asyncio

import pytest

from backend.app.services.preference_interpretation import interpret_preferences
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v1.test_interpreted_requirements import draft_for


class PreferenceModel:
    def __init__(self, draft):
        self.draft = draft

    async def generate_structured(self, **kwargs):
        return self.draft


def test_ordinary_preference_gets_product_target_without_explicit_quantity():
    request = make_request("I like museums")
    draft = draft_for(request.additional_preferences)
    semantic = draft.semantic_requirements[0].model_dump()
    semantic["experience_goal"] = dict(
        frequency="continuing",
        count=None,
        target="category",
        distinct_dates=False,
        explicit_primary_exception=False,
        trip_scope="ordinary",
    )
    draft = type(draft).model_validate({**draft.model_dump(), "semantic_requirements": [semantic]})
    contract = asyncio.run(
        interpret_preferences(request, request.start_date, PreferenceModel(draft))
    )
    requirement = contract.semantic_requirements[0]
    assert requirement.experience_goal.count is None
    assert requirement.soft_coverage.target == 1
    assert requirement.soft_coverage.origin == "ordinary_preference"
    assert requirement.soft_coverage.focus_source is None


@pytest.mark.parametrize(
    "text,focus,target",
    [
        ("This trip is mainly about museums", True, 2),
        ("I especially like museums", False, 1),
        ("Maybe museums could be a focus", False, 1),
    ],
)
def test_focus_requires_a_separate_exact_source(text, focus, target):
    request = make_request(text)
    draft = draft_for(text)
    semantic = draft.semantic_requirements[0].model_dump()
    semantic["experience_goal"] = dict(
        frequency="continuing",
        count=None,
        target="category",
        distinct_dates=False,
        explicit_primary_exception=False,
        trip_scope="themed" if focus else "ordinary",
    )
    semantic["trip_focus_source"] = {"quote": text, "occurrence": 0} if focus else None
    draft = type(draft).model_validate({**draft.model_dump(), "semantic_requirements": [semantic]})
    contract = asyncio.run(
        interpret_preferences(request, request.start_date, PreferenceModel(draft))
    )
    requirement = contract.semantic_requirements[0]
    assert requirement.experience_goal.count is None
    assert requirement.soft_coverage.target == target
    if focus:
        source = requirement.soft_coverage.focus_source
        assert request.additional_preferences[source.start : source.end] == text
        assert requirement.soft_coverage.origin == "current_trip_focus"
    else:
        assert requirement.soft_coverage.focus_source is None


def test_unscheduled_candidates_leave_a_soft_gap_without_new_repair_authority():
    from backend.app.versions.v3.repair_acceptance import assess
    from backend.app.versions.v3.wiring import operation_scope
    from backend.tests.versions.v3.test_b_targets import setup, visit
    from backend.tests.versions.v3.test_semantic_repair import category_goal

    itinerary, context, _, policy = setup(
        [[visit("a", "a"), visit("b", "b", start="12:00", end="13:00")]],
        reviews=(),
    )
    context = category_goal(context, frequency="continuing", count=None, matched_ids=("c",))
    from backend.app.schemas.poi_semantics import RequirementMatch

    context = context.model_copy(
        update={
            "semantic_assessments": tuple(
                row.model_copy(
                    update={
                        "matches": row.matches
                        or [
                            RequirementMatch(
                                requirement_id="semantic_1",
                                relation="mismatch",
                                evidence_refs=row.evidence_refs,
                            )
                        ]
                    }
                )
                for row in context.semantic_assessments
            )
        }
    )
    report = assess(itinerary, context)
    progress = report.diagnostics.goal_progress[0]
    assert progress["matched"] == 0
    assert progress["remaining"] == 1
    assert progress["coverage_status"] == "gap"
    assert progress["target_origin"] == "ordinary_preference"
    assert progress["soft"] is True
    assert report.diagnostics.policy_completion == "complete"
    assert operation_scope(itinerary, report, context=context, policy=policy) is None


@pytest.mark.parametrize(
    "relation,matched,status",
    [
        ("supported", 1, "covered"),
        ("related_alternative", 0, "gap"),
        ("mismatch", 0, "gap"),
        ("unresolved", 0, "unassessed"),
    ],
)
def test_distinct_scheduled_identity_can_cover_two_interests_only_with_support(
    relation, matched, status
):
    from backend.app.versions.v3.repair_acceptance import assess
    from backend.tests.versions.v3.test_b_targets import setup, visit
    from backend.tests.versions.v3.test_semantic_repair import category_goal

    itinerary, context, _, _ = setup(
        [[visit("a1", "a"), visit("a2", "a", start="12:00", end="13:00")]], reviews=()
    )
    context = category_goal(context, frequency="continuing", count=None, matched_ids=("a", "c"))
    first = context.contract.semantic_requirements[0]
    second = first.model_copy(
        update={"requirement_id": "semantic_2", "normalized_text": "Architecture"}
    )
    rows = tuple(
        row.model_copy(
            update={
                "matches": [
                    match.model_copy(update={"relation": relation, "requirement_id": ref})
                    for match in row.matches
                    for ref in ("semantic_1", "semantic_2")
                ]
            }
        )
        for row in context.semantic_assessments
    )
    context = context.model_copy(
        update={
            "contract": context.contract.model_copy(
                update={"semantic_requirements": (first, second)}
            ),
            "semantic_assessments": rows,
        }
    )
    report = assess(itinerary, context)
    assert len(report.diagnostics.goal_progress) == 2
    for progress in report.diagnostics.goal_progress:
        assert progress["matched"] == matched
        assert progress["coverage_status"] == status


def test_generation_boundary_expresses_saturation_without_new_v0_stages():
    from backend.app.versions.v0.prompts import ITINERARY_GENERATION_SYSTEM_PROMPT
    from backend.app.versions.v1.prompts import ITINERARY_GENERATION_SYSTEM_PROMPT as GROUNDED

    for prompt in (ITINERARY_GENERATION_SYSTEM_PROMPT, GROUNDED):
        assert "one distinct qualifying scheduled POI" in prompt
        assert "stop adding priority" in prompt
        assert "classic-landmark value" in prompt
        assert "Allow and explain remaining soft gaps" in prompt


@pytest.mark.parametrize(
    "frequency,count,polarity,scope,goal_present",
    [
        ("exact", 3, "favor", "selected_poi_set", True),
        ("minimum", 2, "favor", "selected_poi_set", True),
        ("continuing", None, "avoid", "selected_poi_set", True),
        ("continuing", None, "favor", "whole_trip", False),
        ("continuing", None, "favor", "itinerary_style", False),
    ],
)
def test_explicit_quantities_restrictions_and_broad_goals_do_not_acquire_soft_counts(
    frequency,
    count,
    polarity,
    scope,
    goal_present,
):
    request = make_request("Synthetic sourced requirement")
    data = draft_for(request.additional_preferences).model_dump()
    row = data["semantic_requirements"][0]
    row.update(
        polarity=polarity,
        scope=scope,
        experience_goal=dict(
            frequency=frequency,
            count=count,
            target="category",
            distinct_dates=False,
            explicit_primary_exception=False,
            trip_scope="exclusive",
        )
        if goal_present
        else None,
    )
    contract = asyncio.run(
        interpret_preferences(
            request,
            request.start_date,
            PreferenceModel(type(draft_for()).model_validate(data)),
        )
    )
    requirement = contract.semantic_requirements[0]
    assert requirement.soft_coverage is None
    assert requirement.polarity == polarity and requirement.scope == scope
    if goal_present:
        assert requirement.experience_goal.count == count
        assert requirement.experience_goal.trip_scope == "exclusive"


@pytest.mark.parametrize("version", ["v0", "v1"])
def test_planning_entry_points_keep_version_boundaries_and_send_coverage_guidance(version):
    import json
    from datetime import date

    from backend.app.versions.v0.runner import run_v0
    from backend.app.versions.v1.runner import run_v1
    from backend.tests.versions.v0.fakes import FakeStructuredLLMClient
    from backend.tests.versions.v0.fakes import make_itinerary as plain_trip
    from backend.tests.versions.v1.fakes import (
        FakePlacesProvider,
        FakeRoutesProvider,
        FakeWeatherProvider,
        make_itinerary,
    )

    request = make_request("I like museums")
    data = draft_for(request.additional_preferences).model_dump()
    data["semantic_requirements"][0]["experience_goal"] = dict(
        frequency="continuing",
        count=None,
        target="category",
        distinct_dates=False,
        explicit_primary_exception=False,
        trip_scope="ordinary",
    )
    data.update(visit_requirements=[], time_protections=[])
    preference = type(draft_for()).model_validate(data)

    class Model(FakeStructuredLLMClient):
        async def generate_poi_semantics_structured(self, **kwargs):
            output = await super().generate_poi_semantics_structured(**kwargs)
            payload = json.loads(kwargs["user_prompt"])
            for row in output["assessments"]:
                row["matches"] = [
                    dict(
                        requirement_id=req["requirement_id"],
                        relation="supported",
                        evidence_refs=row["evidence_refs"],
                    )
                    for req in payload["requirements"]
                ]
            return output

    if version == "v0":
        trip = plain_trip()
        request = make_request(
            "I like museums",
            destination=trip.destination,
            start_date=trip.start_date,
            end_date=trip.end_date,
        )
        model = Model([preference, trip])
        result = asyncio.run(run_v0(request, model, reference_date=date(2026, 9, 11)))
        assert not model.semantic_calls
        assert result.generation_diagnostics.goal_progress == ()
    else:
        trip = make_itinerary()
        trip.days[0].activities[0].source_place_id = "poi-0-0"
        trip.days[0].activities[0].activity_kind = "main_poi"
        model = Model([preference, trip])
        result = asyncio.run(
            run_v1(
                request,
                model,
                FakePlacesProvider(),
                FakeWeatherProvider(),
                FakeRoutesProvider(),
                reference_date=date(2026, 9, 11),
            )
        )
        progress = result.generation_diagnostics.goal_progress[0]
        assert progress["matched"] >= 1 and progress["satisfied"] is True
        assert progress["expected"] == 1 and progress["remaining"] == 0
        assert (
            result.interpreted_requirements.semantic_requirements[0].experience_goal.count is None
        )
        assert '"soft_coverage"' in model.calls[-1].user_prompt
    assert len(model.calls) == 2
    assert "stop adding priority" in model.calls[-1].system_prompt


@pytest.mark.parametrize("scheduled,remaining", [(1, 1), (3, 0)])
def test_focus_target_counts_final_visits_and_is_not_a_category_maximum(scheduled, remaining):
    from backend.app.schemas.interpreted_requirements import SemanticRequirement
    from backend.app.versions.v3.repair_acceptance import assess
    from backend.tests.versions.v3.test_b_targets import setup, visit
    from backend.tests.versions.v3.test_semantic_repair import category_goal

    visits = [visit("a", "a")]
    if scheduled == 3:
        visits += [
            visit("b", "b", start="12:00", end="13:00"),
            visit("c", "c", start="15:00", end="16:00"),
        ]
    itinerary, context, _, _ = setup([visits], reviews=())
    context = category_goal(context, frequency="continuing", count=None)
    requirement = context.contract.semantic_requirements[0]
    requirement = SemanticRequirement.model_validate(
        {
            **requirement.model_dump(),
            "soft_coverage": {
                "target": 2,
                "origin": "current_trip_focus",
                "focus_source": {
                    "quote": "This trip focuses on zoos",
                    "occurrence": 0,
                    "start": 0,
                    "end": 25,
                },
            },
        }
    )
    context = context.model_copy(
        update={
            "contract": context.contract.model_copy(
                update={
                    "semantic_requirements": (requirement,),
                }
            )
        }
    )
    report = assess(itinerary, context)
    progress = report.diagnostics.goal_progress[0]
    assert progress["expected"] == 2 and progress["matched"] == scheduled
    assert progress["remaining"] == remaining
    assert not any(
        r["reason"].startswith("experience_goal") for r in report.diagnostics.policy_issues
    )


@pytest.mark.parametrize(
    "focus_quote", ["Fabricated trip focus", "this trip is mainly about museums"]
)
def test_fabricated_or_casefold_only_focus_cannot_raise_target(focus_quote):
    from backend.app.schemas.requirement_boundary import RequirementBoundaryError

    request = make_request("This trip is mainly about museums")
    data = draft_for(request.additional_preferences).model_dump()
    data["semantic_requirements"][0].update(
        experience_goal=dict(
            frequency="continuing",
            count=None,
            target="category",
            distinct_dates=False,
            explicit_primary_exception=False,
            trip_scope="themed",
        ),
        trip_focus_source={"quote": focus_quote, "occurrence": 0},
    )
    with pytest.raises(RequirementBoundaryError):
        asyncio.run(
            interpret_preferences(
                request, request.start_date, PreferenceModel(type(draft_for()).model_validate(data))
            )
        )


@pytest.mark.parametrize("other_requirement", [False, True])
def test_absent_match_remains_unassessed(other_requirement):
    from backend.app.schemas.poi_semantics import RequirementMatch
    from backend.app.versions.v3.repair_acceptance import assess
    from backend.tests.versions.v3.test_b_targets import setup, visit
    from backend.tests.versions.v3.test_semantic_repair import category_goal

    itinerary, context, _, _ = setup([[visit("a", "a")]], reviews=())
    context = category_goal(context, frequency="continuing", count=None, matched_ids=())
    if other_requirement:
        context = context.model_copy(
            update={
                "semantic_assessments": tuple(
                    row.model_copy(
                        update={
                            "matches": [
                                RequirementMatch(
                                    requirement_id="semantic_2",
                                    relation="supported",
                                    evidence_refs=row.evidence_refs,
                                )
                            ]
                        }
                    )
                    for row in context.semantic_assessments
                )
            }
        )
    progress = assess(itinerary, context).diagnostics.goal_progress[0]
    assert progress["matched"] == 0
    assert progress["coverage_status"] == "unassessed"
