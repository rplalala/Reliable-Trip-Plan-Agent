"""Deterministic V1-A search-intent and observation-merge policies."""

import json
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from backend.app.evidence.selection_models import (
    PlaceOpeningDate,
    PlaceSearchIntent,
    PlaceSelectionInput,
    SearchIntentKind,
)
from backend.app.schemas.named_place_intent import NamedPlaceInclusion, NamedPlaceIntent
from backend.app.schemas.request import TravelRequirements

GENERIC_SEARCH_TERMS = (
    "top attractions",
    "local food",
    "museums and cultural attractions",
)
EXPERIENCE_PREFERENCE_MARKERS = (
    "accessib",
    "crowd",
    "family",
    "quiet",
    "queue",
    "visit duration",
    "walking",
)
_CATEGORY_TERMS = frozenset(
    {
        "attraction",
        "attractions",
        "beach",
        "beaches",
        "food",
        "local food",
        "museum",
        "museums",
        "park",
        "parks",
        "wildlife",
        "coastal views",
        "harbour views",
    }
)
_OTHER_GENERIC_CATEGORIES = frozenset(
    {"viewpoint", "viewpoints", "cultural attraction", "cultural attractions"}
)


def normalize_exact_name(value: str) -> str:
    """Conservative Unicode/case/spacing normalization, not alias inference."""

    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def is_generic_category_surface(value: str) -> bool:
    """Guard only controlled complete category surfaces, not words inside names."""

    return normalize_exact_name(value) in _CATEGORY_TERMS | _OTHER_GENERIC_CATEGORIES


def _clean_term(value: str) -> str:
    return " ".join(value.split())[:80]


def _duplicates_named_activity(activity: str, named_surfaces: frozenset[str]) -> bool:
    """Recognize only a whole name or a bounded Visit/Visit the wrapper."""

    normalized = normalize_exact_name(activity)
    return any(
        normalized in (surface, f"visit {surface}", f"visit the {surface}")
        for surface in named_surfaces
    )


def build_place_search_intents(
    requirements: TravelRequirements,
    *,
    max_queries: int | None = None,
    named_place_intents: Sequence[NamedPlaceIntent] = (),
) -> tuple[PlaceSearchIntent, ...]:
    """Prioritize typed names while retaining distinct activity/category queries."""

    if not requirements.destination:
        raise ValueError("A destination is required for candidate search")
    if max_queries is not None and max_queries < 0:
        raise ValueError("max_queries cannot be negative")
    named_surfaces = frozenset(
        normalize_exact_name(item.place_text) for item in named_place_intents
    )
    if any(is_generic_category_surface(item.place_text) for item in named_place_intents):
        raise ValueError("Generic categories cannot be named-place search intents")
    required = [
        cleaned
        for value in requirements.required_activities
        if (cleaned := _clean_term(value)) and not _duplicates_named_activity(value, named_surfaces)
    ]

    terms: list[tuple[str, SearchIntentKind, NamedPlaceIntent | None]] = []
    seen: set[str] = set()

    def add(value: str, kind: SearchIntentKind, named: NamedPlaceIntent | None = None) -> None:
        cleaned = value if named is not None else _clean_term(value)
        key = normalize_exact_name(cleaned)
        if not cleaned or key in seen:
            return
        seen.add(key)
        terms.append((cleaned, kind, named))

    for named in named_place_intents:
        if named.inclusion is NamedPlaceInclusion.REQUIRED:
            add(named.place_text, SearchIntentKind.EXPLICIT_REQUIREMENT, named)
    for value in required:
        add(value, SearchIntentKind.EXPLICIT_REQUIREMENT)
    for named in named_place_intents:
        if named.inclusion is NamedPlaceInclusion.OPTIONAL:
            add(named.place_text, SearchIntentKind.NORMAL_PREFERENCE, named)
    for value in requirements.preferences:
        if not any(marker in value.casefold() for marker in EXPERIENCE_PREFERENCE_MARKERS):
            add(value, SearchIntentKind.NORMAL_PREFERENCE)
    for value in GENERIC_SEARCH_TERMS:
        if len(terms) >= max(3, max_queries or 0):
            break
        add(value, SearchIntentKind.FALLBACK)

    counts: dict[SearchIntentKind, int] = {}
    intents: list[PlaceSearchIntent] = []
    for term, kind, named in terms if max_queries is None else terms[:max_queries]:
        counts[kind] = counts.get(kind, 0) + 1
        intents.append(
            PlaceSearchIntent(
                intent_id=f"{kind.value}_{counts[kind]}",
                term=term,
                query=f"{term} in {requirements.destination}",
                kind=kind,
                named_place_intent=named,
            )
        )
    return tuple(intents)


def opening_dates_compatible(a: PlaceOpeningDate, b: PlaceOpeningDate) -> bool:
    return all(
        left is None or right is None or left == right
        for left, right in ((a.year, b.year), (a.month, b.month), (a.day, b.day))
    )


def opening_date_precision(value: PlaceOpeningDate) -> int:
    return sum(part is not None for part in (value.year, value.month, value.day))


@dataclass(frozen=True)
class MergedSearchObservations:
    """All unique Place IDs, with every original query hit retained."""

    places: tuple[PlaceSelectionInput, ...]
    raw_observation_count: int


def merge_search_observations(
    observations: Sequence[PlaceSelectionInput],
) -> MergedSearchObservations:
    """Merge identity by Place ID without losing any raw hit or opening-date fact."""

    groups: dict[str, list[PlaceSelectionInput]] = {}
    for observation in observations:
        groups.setdefault(observation.candidate.place_id, []).append(observation)
    merged: list[PlaceSelectionInput] = []
    for place_id in sorted(groups):
        group = groups[place_id]
        canonical = min(
            group,
            key=lambda item: (
                min(hit.provider_rank for hit in item.query_hits),
                min(hit.intent_id for hit in item.query_hits),
                json.dumps(item.candidate.model_dump(mode="json"), sort_keys=True),
            ),
        )
        hits = tuple(
            sorted(
                (hit for item in group for hit in item.query_hits),
                key=lambda hit: (
                    hit.intent_id,
                    hit.provider_rank,
                    hit.actual_result_count,
                    hit.source_query,
                ),
            )
        )
        dates = tuple(
            sorted(
                {
                    observed
                    for item in group
                    for observed in (
                        item.search_opening_date,
                        *item.search_opening_date_observations,
                    )
                    if observed is not None
                },
                key=lambda value: (
                    value.year is None,
                    -opening_date_precision(value),
                    value.year or 0,
                    value.month or 0,
                    value.day or 0,
                ),
            )
        )
        conflict = any(
            not opening_dates_compatible(a, b)
            for index, a in enumerate(dates)
            for b in dates[index + 1 :]
        )
        merged.append(
            canonical.model_copy(
                update={
                    "query_hits": list(hits),
                    "search_opening_date": dates[0] if dates else None,
                    "search_opening_date_observations": dates,
                    "opening_date_conflict": conflict,
                }
            )
        )
    return MergedSearchObservations(tuple(merged), len(observations))


class NamedPlaceResolutionStatus(StrEnum):
    RESOLVED = "resolved"
    NO_EXACT_CANDIDATE_MATCH = "no_exact_candidate_match"
    AMBIGUOUS_EXACT_NAME = "ambiguous_exact_name"
    SEARCH_NOT_ISSUED_BUDGET = "search_not_issued_budget"
    SEARCH_FAILED = "search_failed"


@dataclass(frozen=True)
class NamedPlaceResolution:
    """One typed user intent reconciled against all merged provider identities."""

    named_place_intent: NamedPlaceIntent
    search_intent_id: str | None
    status: NamedPlaceResolutionStatus
    matching_place_ids: tuple[str, ...]
    resolved_place_id: str | None


def resolve_named_place_intents(
    named_place_intents: Sequence[NamedPlaceIntent],
    search_intents: Sequence[PlaceSearchIntent],
    places: Sequence[PlaceSelectionInput],
    *,
    failed_search_intent_ids: frozenset[str] = frozenset(),
    budget_not_attempted_intent_ids: frozenset[str] = frozenset(),
) -> tuple[NamedPlaceResolution, ...]:
    """Reconcile each typed surface by exact normalized provider display name."""

    by_name: dict[str, set[str]] = {}
    for place in places:
        by_name.setdefault(normalize_exact_name(place.candidate.name), set()).add(
            place.candidate.place_id
        )
    search_by_name = {
        normalize_exact_name(intent.named_place_intent.place_text): intent.intent_id
        for intent in search_intents
        if intent.named_place_intent is not None
    }
    resolutions: list[NamedPlaceResolution] = []
    for named in named_place_intents:
        key = normalize_exact_name(named.place_text)
        matching_ids = tuple(sorted(by_name.get(key, ())))
        search_intent_id = search_by_name.get(key)
        if named.inclusion is NamedPlaceInclusion.REQUIRED and (
            search_intent_id is None or search_intent_id in budget_not_attempted_intent_ids
        ):
            status = NamedPlaceResolutionStatus.SEARCH_NOT_ISSUED_BUDGET
        elif len(matching_ids) == 1:
            status = NamedPlaceResolutionStatus.RESOLVED
        elif len(matching_ids) > 1:
            status = NamedPlaceResolutionStatus.AMBIGUOUS_EXACT_NAME
        elif search_intent_id is None or search_intent_id in budget_not_attempted_intent_ids:
            status = NamedPlaceResolutionStatus.SEARCH_NOT_ISSUED_BUDGET
        elif search_intent_id in failed_search_intent_ids:
            status = NamedPlaceResolutionStatus.SEARCH_FAILED
        else:
            status = NamedPlaceResolutionStatus.NO_EXACT_CANDIDATE_MATCH
        resolutions.append(
            NamedPlaceResolution(
                named_place_intent=named,
                search_intent_id=search_intent_id,
                status=status,
                matching_place_ids=matching_ids,
                resolved_place_id=matching_ids[0]
                if status is NamedPlaceResolutionStatus.RESOLVED
                else None,
            )
        )
    return tuple(resolutions)
