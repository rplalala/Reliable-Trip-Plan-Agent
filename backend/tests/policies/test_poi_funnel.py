"""Pure search-intent and multi-intent observation funnel policies."""

from datetime import date
from decimal import Decimal

import pytest

from backend.app.evidence.selection_models import SearchIntentKind
from backend.app.evidence.selection_normalization import normalize_place_search_hit
from backend.app.integrations.models import LatLng, PlaceCandidateDTO, PlaceOpeningDateDTO
from backend.app.policies.poi_funnel import (
    NamedPlaceResolutionStatus,
    build_place_search_intents,
    merge_search_observations,
    resolve_named_place_intents,
)
from backend.app.schemas.named_place_intent import NamedPlaceInclusion, NamedPlaceIntent
from backend.app.schemas.request import TravelRequirements


def _requirements(required: list[str], preferences: list[str] | None = None) -> TravelRequirements:
    return TravelRequirements(
        destination="Sydney",
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 14),
        required_activities=required,
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


def _observation(
    place_id: str,
    name: str,
    *,
    intent: str,
    rank: int,
    count: int,
    opening: PlaceOpeningDateDTO | None = None,
):
    return normalize_place_search_hit(
        PlaceCandidateDTO(
            place_id=place_id,
            display_name=name,
            location=LatLng(latitude=-33.8, longitude=151.2),
            provider_rank=rank,
            opening_date=opening,
        ),
        intent_id=intent,
        source_query=f"{intent} in Sydney",
        actual_result_count=count,
        intent_kind=SearchIntentKind.EXPLICIT_REQUIREMENT,
    )


def test_intents_have_stable_class_weights_and_named_vs_category_semantics() -> None:
    requirements = _requirements(
        ["museums", "Australian Museum"],
        ["harbour views", "less crowded"],
    )
    intents = build_place_search_intents(
        requirements,
        max_queries=3,
        named_place_intents=(_named("Australian Museum"),),
    )
    assert [(item.intent_id, item.term, item.weight) for item in intents] == [
        ("explicit_requirement_1", "Australian Museum", 1),
        ("explicit_requirement_2", "museums", 1),
        ("normal_preference_1", "harbour views", Decimal("0.8")),
    ]
    assert intents[0].named_place_intent.place_text == "Australian Museum"
    assert intents[1].named_place_intent is None
    assert build_place_search_intents(requirements, max_queries=3) == build_place_search_intents(
        requirements, max_queries=3
    )


def test_generic_category_cannot_be_marked_as_named_must_visit() -> None:
    with pytest.raises(ValueError, match="Generic categories"):
        build_place_search_intents(
            _requirements(["museums"]),
            max_queries=3,
            named_place_intents=(_named("museums"),),
        )


def test_fallback_intent_is_bounded_and_weighted() -> None:
    intents = build_place_search_intents(_requirements([]), max_queries=2)
    assert len(intents) == 2
    assert [item.kind for item in intents] == [SearchIntentKind.FALLBACK] * 2
    assert [item.weight for item in intents] == [Decimal("0.4")] * 2


def test_intent_generation_keeps_more_than_provider_budget_without_reordering() -> None:
    preferences = [f"interest {index}" for index in range(15)]
    intents = build_place_search_intents(
        _requirements([], preferences), named_place_intents=(_named("Sydney Opera House"),)
    )
    assert len(intents) == 16
    assert [item.term for item in intents] == ["Sydney Opera House", *preferences]
    assert intents[0].weight == 1
    assert all(item.weight == Decimal("0.8") for item in intents[1:])


def test_duplicate_preferences_collapse_before_priority_order_and_fallback() -> None:
    intents = build_place_search_intents(_requirements([], ["museums", " Museums ", "beaches"]))
    assert [item.term for item in intents] == ["museums", "beaches", "top attractions"]
    assert [item.kind for item in intents] == [
        SearchIntentKind.NORMAL_PREFERENCE,
        SearchIntentKind.NORMAL_PREFERENCE,
        SearchIntentKind.FALLBACK,
    ]


def test_required_name_not_claimed_satisfied_when_own_query_skipped_by_budget() -> None:
    named = _named("Sydney Opera House")
    intents = build_place_search_intents(
        _requirements([], ["harbour attractions"]), named_place_intents=(named,)
    )
    places = merge_search_observations(
        [
            _observation(
                "opera",
                "Sydney Opera House",
                intent=intents[1].intent_id,
                rank=0,
                count=1,
            )
        ]
    ).places
    (resolution,) = resolve_named_place_intents(
        (named,),
        intents,
        places,
        budget_not_attempted_intent_ids=frozenset({intents[0].intent_id}),
    )
    assert resolution.status is NamedPlaceResolutionStatus.SEARCH_NOT_ISSUED_BUDGET
    assert resolution.matching_place_ids == ("opera",)
    assert resolution.resolved_place_id is None


def test_place_id_merge_preserves_every_raw_n_r_and_partial_opening_observation() -> None:
    a = _observation(
        "shared",
        "Australian Museum",
        intent="museum",
        rank=2,
        count=5,
        opening=PlaceOpeningDateDTO(year=2026, month=9),
    )
    b = _observation(
        "shared",
        "Australian Museum",
        intent="culture",
        rank=0,
        count=3,
        opening=PlaceOpeningDateDTO(year=2026, month=9, day=13),
    )
    c = _observation("other", "Other", intent="museum", rank=1, count=5)
    forward = merge_search_observations([a, b, c])
    reverse = merge_search_observations([c, b, a])
    assert forward == reverse
    assert forward.raw_observation_count == 3
    shared = next(item for item in forward.places if item.candidate.place_id == "shared")
    assert [
        (hit.intent_id, hit.provider_rank, hit.actual_result_count) for hit in shared.query_hits
    ] == [
        ("culture", 0, 3),
        ("museum", 2, 5),
    ]
    assert shared.search_opening_date.day == 13
    assert len(shared.search_opening_date_observations) == 2
    assert not shared.opening_date_conflict


def test_conflicting_search_opening_dates_are_preserved_as_uncertain() -> None:
    first = _observation(
        "same",
        "Same",
        intent="first",
        rank=0,
        count=1,
        opening=PlaceOpeningDateDTO(year=2026, month=9),
    )
    second = _observation(
        "same",
        "Same",
        intent="second",
        rank=0,
        count=1,
        opening=PlaceOpeningDateDTO(year=2026, month=10),
    )
    merged = merge_search_observations([second, first]).places[0]
    assert merged.opening_date_conflict
    assert len(merged.search_opening_date_observations) == 2


def test_only_exact_name_resolves_explicit_place_not_category() -> None:
    named = _named("Australian Museum")
    intents = build_place_search_intents(
        _requirements(["Australian Museum", "museums"]),
        max_queries=2,
        named_place_intents=(named,),
    )
    places = merge_search_observations(
        [
            _observation("museum", "Australian Museum", intent="required", rank=0, count=1),
            _observation("category", "Museum of Sydney", intent="required", rank=0, count=1),
        ]
    ).places
    (resolution,) = resolve_named_place_intents((named,), intents, places)
    assert resolution.status is NamedPlaceResolutionStatus.RESOLVED
    assert resolution.resolved_place_id == "museum"
    assert intents[0].named_place_intent == named
    assert intents[1].named_place_intent is None


@pytest.mark.parametrize(
    "activity",
    ["Sydney Opera House", "Visit Sydney Opera House", "Visit the Sydney Opera House"],
)
def test_typed_intent_replaces_only_mechanically_equivalent_activity(activity: str) -> None:
    named = _named("Sydney Opera House", NamedPlaceInclusion.OPTIONAL)
    intents = build_place_search_intents(
        _requirements([activity]), max_queries=3, named_place_intents=(named,)
    )
    matching = [item for item in intents if "Sydney Opera House" in item.term]
    assert len(matching) == 1
    assert matching[0].term == "Sydney Opera House"
    assert matching[0].kind is SearchIntentKind.NORMAL_PREFERENCE
    assert matching[0].weight == Decimal("0.8")
    assert matching[0].named_place_intent == named


def test_compound_activity_is_not_suppressed_by_narrow_named_dedup() -> None:
    intents = build_place_search_intents(
        _requirements(["Visit Sydney Opera House and harbour attractions"]),
        max_queries=3,
        named_place_intents=(_named("Sydney Opera House"),),
    )
    assert [item.term for item in intents[:2]] == [
        "Sydney Opera House",
        "Visit Sydney Opera House and harbour attractions",
    ]


def test_without_typed_intent_free_text_does_not_create_named_resolution() -> None:
    intents = build_place_search_intents(_requirements(["Sydney Opera House"]), max_queries=2)
    places = merge_search_observations(
        [_observation("opera", "Sydney Opera House", intent=intents[0].intent_id, rank=0, count=1)]
    ).places
    assert intents[0].named_place_intent is None
    assert resolve_named_place_intents((), intents, places) == ()


def test_ambiguous_exact_name_and_alias_remain_unresolved() -> None:
    named = (_named("Australian Museum"), _named("MCA"))
    intents = build_place_search_intents(
        _requirements([]), max_queries=2, named_place_intents=named
    )
    places = merge_search_observations(
        [
            _observation(
                "museum-a", "Australian Museum", intent=intents[0].intent_id, rank=0, count=2
            ),
            _observation(
                "museum-b", "Australian Museum", intent=intents[0].intent_id, rank=1, count=2
            ),
            _observation(
                "mca", "Museum of Contemporary Art", intent=intents[1].intent_id, rank=0, count=1
            ),
        ]
    ).places
    ambiguous, alias = resolve_named_place_intents(named, intents, places)
    assert ambiguous.status is NamedPlaceResolutionStatus.AMBIGUOUS_EXACT_NAME
    assert ambiguous.matching_place_ids == ("museum-a", "museum-b")
    assert ambiguous.resolved_place_id is None
    assert alias.status is NamedPlaceResolutionStatus.NO_EXACT_CANDIDATE_MATCH
    assert alias.resolved_place_id is None


def test_name_can_resolve_from_another_query_when_own_query_is_budget_truncated() -> None:
    named = _named("Australian Museum", NamedPlaceInclusion.OPTIONAL)
    intents = build_place_search_intents(
        _requirements(["museums"]), max_queries=1, named_place_intents=(named,)
    )
    assert intents[0].term == "museums"
    places = merge_search_observations(
        [_observation("museum", "Australian Museum", intent=intents[0].intent_id, rank=0, count=1)]
    ).places
    (resolution,) = resolve_named_place_intents((named,), intents, places)
    assert resolution.status is NamedPlaceResolutionStatus.RESOLVED
    assert resolution.search_intent_id is None
    assert resolution.resolved_place_id == "museum"
