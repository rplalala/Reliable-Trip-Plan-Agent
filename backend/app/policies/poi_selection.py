"""Canonical POI factual eligibility and downstream selection records."""

import calendar
import math
from dataclasses import dataclass
from datetime import date
from enum import StrEnum

from backend.app.evidence.selection_models import (
    CoordinateState,
    PlaceOpeningDate,
    PlaceSelectionInput,
    RatingAcquisitionState,
)


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
class SelectedPOI:
    place_id: str
    must_visit: bool
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
