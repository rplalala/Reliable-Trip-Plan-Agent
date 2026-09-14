"""Counterfactual review triggers using the unchanged Phase-2 POI selector."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from backend.app.evidence.selection_models import PlaceSelectionInput
from backend.app.policies.experience_selection import (
    ExplicitExperienceNeed,
    reachable_experience_values,
)
from backend.app.policies.poi_selection import POISelectionResult, select_pois
from backend.app.policies.trip_dates import TripDateWindow


@dataclass(frozen=True)
class ReviewSelectionContext:
    start_date: date
    end_date: date
    window: TripDateWindow
    capacity: int
    must_visit_place_ids: frozenset[str]
    excluded_place_ids: frozenset[str]
    unresolved_required_names: tuple[str, ...]


@dataclass(frozen=True)
class ReviewSensitiveCandidate:
    place_id: str
    minimum_flip_magnitude: Decimal
    triggering_values: tuple[Decimal, ...]
    preference_importance: Decimal
    best_provider_rank: int


def select_with_experience(
    places: Sequence[PlaceSelectionInput],
    context: ReviewSelectionContext,
    scores: Mapping[str, Decimal],
) -> POISelectionResult:
    return select_pois(
        places,
        start_date=context.start_date,
        end_date=context.end_date,
        window=context.window,
        capacity=context.capacity,
        must_visit_place_ids=context.must_visit_place_ids,
        excluded_place_ids=context.excluded_place_ids,
        unresolved_required_names=context.unresolved_required_names,
        experience_scores=scores,
        require_details=True,
    )


def find_review_sensitive_candidates(
    places: Sequence[PlaceSelectionInput],
    *,
    context: ReviewSelectionContext,
    needs: Sequence[ExplicitExperienceNeed],
    current_scores: Mapping[str, Decimal],
    attempted_ids: frozenset[str] = frozenset(),
) -> tuple[ReviewSensitiveCandidate, ...]:
    """Vary only one candidate's reachable E while holding all others fixed."""

    if not needs:
        return ()
    baseline = select_with_experience(places, context, current_scores)
    baseline_ids = set(baseline.selected_place_ids)
    eligible_ids = {item.place_id for item in baseline.eligibility if item.eligible}
    reachable = reachable_experience_values(needs)
    importance = max(need.importance for need in needs)
    result: list[ReviewSensitiveCandidate] = []
    for place in places:
        place_id = place.candidate.place_id
        if (
            place_id not in eligible_ids
            or place_id in attempted_ids
            or place_id in context.must_visit_place_ids
        ):
            continue
        original = current_scores.get(place_id, Decimal(0))
        flipping: list[Decimal] = []
        for value in reachable:
            if value == original or value == 0:
                continue
            changed = select_with_experience(
                places,
                context,
                {**current_scores, place_id: value},
            )
            if (place_id in changed.selected_place_ids) != (place_id in baseline_ids):
                flipping.append(value)
        if flipping:
            result.append(
                ReviewSensitiveCandidate(
                    place_id=place_id,
                    minimum_flip_magnitude=min(abs(value) for value in flipping),
                    triggering_values=tuple(flipping),
                    preference_importance=importance,
                    best_provider_rank=min(hit.provider_rank for hit in place.query_hits),
                )
            )
    return tuple(
        sorted(
            result,
            key=lambda item: (
                item.minimum_flip_magnitude,
                -item.preference_importance,
                item.best_provider_rank,
                item.place_id,
            ),
        )
    )
