"""Candidate options are not a minimum semantic cover or mandatory itinerary."""

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from backend.app.evidence.experience_models import ExperienceProfile, ExperienceSignal
from backend.app.policies.interpreted_requirements import canonicalize_requirements
from backend.app.policies.planning_supply import SupplyCandidate, select_planning_supply
from backend.app.schemas.interpreted_requirements import (
    ClarificationRequired,
    ExperienceEvidenceRequest,
)
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v1.test_interpreted_requirements import draft_for


def candidate(pid, category="museum", intents=(), rating=4.5):
    return SupplyCandidate(
        place_id=pid,
        primary_type=category,
        rating=rating,
        latitude=-33.86,
        longitude=151.2,
        intent_ids=intents,
    )


def contract():
    return canonicalize_requirements(draft_for(), make_request("Prefer local places"))


def select(candidates, req=None, **kwargs):
    args = dict(
        required_ids=(),
        excluded_ids=(),
        capacity=8,
        hard_capacity=16,
        destination_coordinates=(-33.86, 151.2),
    )
    args.update(kwargs)
    return select_planning_supply(candidates, req or contract(), **args)


@pytest.mark.parametrize("count,expected,shortfall", [(12, 8, 0), (3, 3, 5), (0, 0, 8)])
def test_fills_capacity_without_semantic_coverage(count, expected, shortfall):
    result = select([candidate(str(i)) for i in range(count)])
    assert len(result.selected_place_ids) == expected
    assert result.shortfall == shortfall
    assert result.evaluator_calls == result.subset_enumerator_calls == 0


@pytest.mark.parametrize("required_count", [1, 7, 8, 9, 12])
def test_required_near_and_over_normal_capacity(required_count):
    places = [candidate(f"p{i:02}") for i in range(12)]
    required = {p.place_id for p in places[:required_count]}
    result = select(places, required_ids=required)
    assert required <= set(result.selected_place_ids)
    assert len(result.selected_place_ids) == max(8, required_count)
    assert result.normal_capacity == 8


def test_required_hard_budget_and_excluded_conflicts_are_explicit():
    places = [candidate(str(i)) for i in range(10)]
    with pytest.raises(ClarificationRequired, match="required_capacity_conflict"):
        select(places, required_ids={p.place_id for p in places}, hard_capacity=9)
    with pytest.raises(ClarificationRequired, match="required_place_ineligible"):
        select(places, required_ids={"0"}, excluded_ids={"0"})
    assert "0" not in select(places, excluded_ids={"0"}).selected_place_ids


def linked_contract():
    req = contract()
    semantic = req.semantic_requirements[0]
    return req.model_copy(
        update={
            "semantic_requirements": (
                semantic.model_copy(
                    update={"requirement_id": "father", "subject_refs": ("father",)}
                ),
                semantic.model_copy(
                    update={"requirement_id": "mother", "subject_refs": ("mother",)}
                ),
            ),
            "discovery_intents": tuple(
                SimpleNamespace(intent_id=i, requirement_refs=(s,))
                for i, s in [("d1", "father"), ("d2", "father"), ("d3", "mother")]
            ),
        }
    )


def test_multiple_interests_of_one_subject_cannot_take_the_first_round():
    candidates = [
        candidate("a", intents=("d1",)),
        candidate("b", intents=("d2",)),
        candidate("c", intents=("d3",)),
    ]
    assert select(candidates, linked_contract(), capacity=2).selected_place_ids == ("a", "c")


def test_library_preference_keeps_landmarks_and_other_credible_options():
    req = contract().model_copy(
        update={
            "discovery_intents": (
                SimpleNamespace(intent_id="libraries", requirement_refs=("semantic_1",)),
            )
        }
    )
    places = [candidate("z", "library", ("libraries",))] + [
        candidate(str(i), kind)
        for i, kind in enumerate(
            ["landmark", "park", "museum", "gallery", "historic_area", "cultural_site"]
        )
    ]
    result = select(places, req)
    assert result.selected_place_ids[0] == "z"
    assert len(result.selected_place_ids) == 7


def walking_contract():
    return contract().model_copy(
        update={
            "experience_evidence_requests": (
                ExperienceEvidenceRequest(
                    requirement_id="semantic_1",
                    dimension="walking_intensity",
                    preferred_values=("LIGHT",),
                    avoided_values=("HIGH",),
                ),
            )
        }
    )


def profile(pid, value):
    return ExperienceProfile(
        place_id=pid,
        availability="available",
        signals=(
            ExperienceSignal(
                dimension="walking_intensity",
                value=value,
                confidence="medium",
                review_refs=("review_1",),
            ),
        ),
    )


def test_unknown_neutral_soft_conflict_and_required():
    places = [candidate(x) for x in "abcd"]
    profiles = {
        "a": profile("a", "HIGH"),
        "c": profile("c", "LIGHT"),
        "d": profile("d", "MODERATE"),
    }
    result = select(places, walking_contract(), profiles=profiles, capacity=4)
    assert result.selected_place_ids == ("c", "b", "d", "a")
    assert result.profile_relations["b"][0].relation == "unknown"
    assert result.profile_relations["d"][0].relation == "neutral"
    assert select(
        places, walking_contract(), profiles=profiles, required_ids={"a"}, capacity=2
    ).selected_place_ids == ("a", "c")


def test_old_dimension_only_snapshot_does_not_invent_preference_direction():
    req = contract().model_copy(
        update={
            "experience_evidence_requests": (
                ExperienceEvidenceRequest(
                    requirement_id="semantic_1", dimension="walking_intensity"
                ),
            )
        }
    )
    result = select([candidate("a")], req, profiles={"a": profile("a", "HIGH")})
    assert result.profile_relations["a"][0].relation == "unknown"


def test_type_diversity_before_rating_without_claiming_experience_diversity():
    places = [candidate("a", rating=5), candidate("b", rating=5), candidate("c", "park", rating=4)]
    assert select(places, capacity=2).selected_place_ids == ("a", "c")


def test_missing_rating_abstains_and_source_rank_is_not_an_input():
    places = [candidate("a", rating=None), candidate("b", rating=5)]
    assert select(places, capacity=1).selected_place_ids == ("a",)
    assert "provider_rank" not in SupplyCandidate.model_fields
    assert "source" not in SupplyCandidate.model_fields
    with pytest.raises(ValidationError):
        SupplyCandidate(**places[0].model_dump(), provider_rank=0)


def test_shuffle_and_repeat_are_identical_apart_from_timings():
    places = [candidate(str(i), str(i % 3)) for i in range(10)]
    first = select(places)
    exclude = {"elapsed_seconds", "cpu_seconds"}
    assert first.model_dump(exclude=exclude) == select(list(reversed(places))).model_dump(
        exclude=exclude
    )
    assert first.model_dump(exclude=exclude) == select(places).model_dump(exclude=exclude)
