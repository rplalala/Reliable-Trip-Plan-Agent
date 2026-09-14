"""Pure, reusable V1-A POI eligibility and greedy selection policy."""

import calendar
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum

from backend.app.evidence.selection_models import (
    CoordinateState,
    PlaceOpeningDate,
    PlaceSelectionInput,
    QueryIntentHit,
    RatingAcquisitionState,
)
from backend.app.policies.trip_dates import TripDateWindow, validate_requested_trip_dates


class DateRisk(StrEnum):
    NONE = "none"
    UNKNOWN_STATUS = "unknown_status"
    TEMPORARILY_CLOSED_VERIFY = "temporarily_closed_verify"
    FUTURE_OPENING_VERIFY = "future_opening_verify"


@dataclass(frozen=True)
class Eligibility:
    place_id: str
    eligible: bool
    reason: str | None
    date_risk: DateRisk
    earliest_possible_opening: date | None
    not_visitable_before: date | None
    opening_date_conflict: bool = False


@dataclass(frozen=True)
class Score:
    q_rel: Decimal
    c_cov: Decimal
    g_geo: Decimal
    r_rating: Decimal
    e_exp: Decimal

    @property
    def total(self) -> Decimal:
        return self.q_rel + self.c_cov + self.g_geo + self.r_rating + self.e_exp


@dataclass(frozen=True)
class SelectedPOI:
    place_id: str
    must_visit: bool
    score: Score | None
    covered_intent_ids: tuple[str, ...]
    date_risk: DateRisk
    not_visitable_before: date | None


@dataclass(frozen=True)
class SelectionConflict:
    place_id_or_name: str
    reason: str


@dataclass(frozen=True)
class POISelectionResult:
    selected: tuple[SelectedPOI, ...]
    eligibility: tuple[Eligibility, ...]
    conflicts: tuple[SelectionConflict, ...]

    @property
    def selected_place_ids(self) -> tuple[str, ...]:
        return tuple(item.place_id for item in self.selected)


def _opening_bounds(opening: PlaceOpeningDate | None) -> tuple[date, date] | None:
    if opening is None or opening.year is None:
        return None
    if opening.month is None:
        if opening.day is not None:
            return None
        return date(opening.year, 1, 1), date(opening.year, 12, 31)
    last_day = calendar.monthrange(opening.year, opening.month)[1]
    if opening.day is None:
        return date(opening.year, opening.month, 1), date(opening.year, opening.month, last_day)
    exact = date(opening.year, opening.month, opening.day)
    return exact, exact


def _coordinates_valid(place: PlaceSelectionInput) -> bool:
    candidate = place.candidate
    return (
        place.coordinate_state is CoordinateState.VALID
        and math.isfinite(candidate.latitude)
        and math.isfinite(candidate.longitude)
        and -90 <= candidate.latitude <= 90
        and -180 <= candidate.longitude <= 180
    )


def evaluate_poi_eligibility(
    place: PlaceSelectionInput,
    *,
    trip_end: date,
    excluded: bool = False,
    require_details: bool = True,
) -> Eligibility:
    """Use structured Places facts only; never infer trip-date opening hours."""

    place_id = place.candidate.place_id
    supported_dates = [
        value
        for value in (place.details_opening_date, place.search_opening_date)
        if value is not None
    ]
    opening = (
        None
        if place.opening_date_conflict or not supported_dates
        else max(
            supported_dates,
            key=lambda value: (
                value.year is not None,
                sum(part is not None for part in (value.year, value.month, value.day)),
            ),
        )
    )
    bounds = _opening_bounds(opening)
    earliest = bounds[0] if bounds else None
    status = (
        place.structured_evidence.business_status
        if place.structured_evidence is not None
        else place.candidate.business_status
    )
    risk = DateRisk.NONE
    reason: str | None = None
    if excluded:
        reason = "explicitly_excluded"
    elif status == "CLOSED_PERMANENTLY":
        reason = "permanently_closed"
    elif status == "FUTURE_OPENING":
        risk = DateRisk.FUTURE_OPENING_VERIFY
        if earliest is not None and earliest > trip_end:
            reason = "opening_definitely_after_trip"
    elif status == "CLOSED_TEMPORARILY":
        risk = DateRisk.TEMPORARILY_CLOSED_VERIFY
    elif status != "OPERATIONAL":
        risk = DateRisk.UNKNOWN_STATUS

    if reason is None and not _coordinates_valid(place):
        reason = "invalid_or_missing_coordinates"
    if reason is None and place.rating_state is RatingAcquisitionState.DETAILS_FAILED:
        reason = "structured_details_failed"
    if (
        reason is None
        and require_details
        and (
            place.rating_state is RatingAcquisitionState.NOT_ATTEMPTED
            or place.structured_evidence is None
        )
    ):
        reason = "structured_details_unavailable"
    return Eligibility(
        place_id=place_id,
        eligible=reason is None,
        reason=reason,
        date_risk=risk,
        earliest_possible_opening=earliest,
        not_visitable_before=earliest if status == "FUTURE_OPENING" else None,
        opening_date_conflict=place.opening_date_conflict,
    )


def q_rel(hits: Sequence[QueryIntentHit]) -> Decimal:
    """Highest original, unfiltered provider-hit relevance across all intents."""

    values: list[Decimal] = []
    for hit in hits:
        weight = hit.intent_kind.weight
        if hit.actual_result_count == 1:
            values.append(Decimal(30) * weight)
        else:
            values.append(
                Decimal(30)
                * weight
                * Decimal(hit.actual_result_count - 1 - hit.provider_rank)
                / Decimal(hit.actual_result_count - 1)
            )
    return max(values, default=Decimal(0))


def c_cov(hits: Sequence[QueryIntentHit], covered: frozenset[str]) -> Decimal:
    return max(
        (Decimal(25) * hit.intent_kind.weight for hit in hits if hit.intent_id not in covered),
        default=Decimal(0),
    )


def _distance_km(a: PlaceSelectionInput, b: PlaceSelectionInput) -> float:
    lat_a, lon_a = math.radians(a.candidate.latitude), math.radians(a.candidate.longitude)
    lat_b, lon_b = math.radians(b.candidate.latitude), math.radians(b.candidate.longitude)
    central = 2 * math.asin(
        min(
            1.0,
            math.sqrt(
                math.sin((lat_b - lat_a) / 2) ** 2
                + math.cos(lat_a) * math.cos(lat_b) * math.sin((lon_b - lon_a) / 2) ** 2
            ),
        )
    )
    return 6371.0088 * central


def g_geo(place: PlaceSelectionInput, selected: Sequence[PlaceSelectionInput]) -> Decimal:
    if not selected:
        return Decimal(5)
    distance = min(_distance_km(place, other) for other in selected)
    if distance <= 3:
        return Decimal(10)
    if distance <= 10:
        return Decimal(5)
    return Decimal(0)


def r_rating(rating: float | None) -> Decimal:
    if rating is None or not math.isfinite(rating) or not 0 <= rating <= 5:
        return Decimal(0)
    raw = Decimal(10) * (Decimal(str(rating)) - Decimal("3.5")) / Decimal("1.5")
    return max(Decimal(-10), min(Decimal(10), raw))


def _experience_value(value: Decimal | int | float) -> Decimal:
    result = Decimal(str(value))
    if not result.is_finite() or not Decimal(-15) <= result <= Decimal(10):
        raise ValueError("E_exp must be finite and within [-15, 10]")
    return result


def select_pois(
    places: Sequence[PlaceSelectionInput],
    *,
    start_date: date,
    end_date: date,
    window: TripDateWindow,
    capacity: int,
    must_visit_place_ids: frozenset[str] = frozenset(),
    excluded_place_ids: frozenset[str] = frozenset(),
    unresolved_required_names: tuple[str, ...] = (),
    experience_scores: Mapping[str, Decimal | int | float] | None = None,
    require_details: bool = True,
) -> POISelectionResult:
    """Select POIs without provider, cache, budget, LLM, or graph side effects.

    Resolved IDs and explicit exclusions are inputs from controlled upstream matching.
    This policy never interprets free text or category names as must-visit IDs.
    """

    validate_requested_trip_dates(start_date, end_date, window)
    if capacity < 1:
        raise ValueError("final POI capacity must be positive")
    by_id = {place.candidate.place_id: place for place in places}
    if len(by_id) != len(places):
        raise ValueError("selection inputs must have unique Place IDs")
    scores = {key: _experience_value(value) for key, value in (experience_scores or {}).items()}
    unknown_score_ids = scores.keys() - by_id.keys()
    if unknown_score_ids:
        raise ValueError("experience scores must reference provided Place IDs")
    eligibility = {
        place_id: evaluate_poi_eligibility(
            place,
            trip_end=end_date,
            excluded=place_id in excluded_place_ids,
            require_details=require_details,
        )
        for place_id, place in by_id.items()
    }
    conflicts = [
        SelectionConflict(name, "required_place_unresolved")
        for name in sorted(set(unresolved_required_names))
    ]
    if len(must_visit_place_ids) > capacity:
        conflicts.append(SelectionConflict("must_visits", "must_visits_exceed_capacity"))
    for place_id in sorted(must_visit_place_ids):
        if place_id not in by_id:
            conflicts.append(SelectionConflict(place_id, "required_place_unresolved"))
        elif not eligibility[place_id].eligible:
            conflicts.append(
                SelectionConflict(place_id, eligibility[place_id].reason or "ineligible")
            )

    def best_rank(place: PlaceSelectionInput) -> int:
        return min(hit.provider_rank for hit in place.query_hits)

    selected_inputs: list[PlaceSelectionInput] = []
    selected: list[SelectedPOI] = []
    covered: frozenset[str] = frozenset()
    for place_id in sorted(
        (pid for pid in must_visit_place_ids if pid in by_id and eligibility[pid].eligible),
        key=lambda pid: (best_rank(by_id[pid]), pid),
    ):
        if len(selected) >= capacity:
            break
        place = by_id[place_id]
        selected_inputs.append(place)
        place_intents = frozenset(hit.intent_id for hit in place.query_hits)
        covered = covered.union(place_intents)
        selected.append(
            SelectedPOI(
                place_id=place_id,
                must_visit=True,
                score=None,
                covered_intent_ids=tuple(sorted(place_intents)),
                date_risk=eligibility[place_id].date_risk,
                not_visitable_before=eligibility[place_id].not_visitable_before,
            )
        )
    # Conflicts remain unsatisfied, but unusable required POIs do not reserve slots.
    while len(selected) < capacity:
        options = []
        for place_id, place in by_id.items():
            if not eligibility[place_id].eligible or place_id in {p.place_id for p in selected}:
                continue
            score = Score(
                q_rel=q_rel(place.query_hits),
                c_cov=c_cov(place.query_hits, covered),
                g_geo=g_geo(place, selected_inputs),
                r_rating=r_rating(place.rating),
                e_exp=scores.get(place_id, Decimal(0)),
            )
            options.append((place_id, place, score))
        if not options:
            break
        place_id, place, score = min(
            options,
            key=lambda item: (-item[2].total, best_rank(item[1]), item[0]),
        )
        selected_inputs.append(place)
        place_intents = frozenset(hit.intent_id for hit in place.query_hits)
        covered = covered.union(place_intents)
        selected.append(
            SelectedPOI(
                place_id=place_id,
                must_visit=False,
                score=score,
                covered_intent_ids=tuple(sorted(place_intents)),
                date_risk=eligibility[place_id].date_risk,
                not_visitable_before=eligibility[place_id].not_visitable_before,
            )
        )
    return POISelectionResult(
        selected=tuple(selected),
        eligibility=tuple(eligibility[pid] for pid in sorted(eligibility)),
        conflicts=tuple(conflicts),
    )
