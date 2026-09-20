"""Pure revised V1-A POI selection policy regression tests."""

from datetime import UTC, date, datetime

import pytest

from backend.app.evidence.models import EvidenceAvailability, PlaceCandidate, PlaceEvidence
from backend.app.evidence.selection_models import (
    CoordinateState,
    PlaceOpeningDate,
    PlaceSelectionInput,
    QueryIntentHit,
    RatingAcquisitionState,
    SearchIntentKind,
)
from backend.app.policies.poi_selection import (
    DateRisk,
    evaluate_poi_eligibility,
)
from backend.app.policies.trip_dates import create_trip_date_window

START = date(2026, 9, 12)
END = date(2026, 9, 14)
WINDOW = create_trip_date_window(date(2026, 9, 11))


def hit(
    intent: str = "museum",
    *,
    rank: int = 0,
    count: int = 5,
    kind: SearchIntentKind = SearchIntentKind.EXPLICIT_REQUIREMENT,
) -> QueryIntentHit:
    return QueryIntentHit(
        intent_id=intent,
        source_query=f"{intent} in Sydney",
        provider_rank=rank,
        actual_result_count=count,
        intent_kind=kind,
    )


def place(
    place_id: str,
    *,
    hits: list[QueryIntentHit] | None = None,
    latitude: float = -33.87,
    longitude: float = 151.20,
    status: str | None = "OPERATIONAL",
    opening: PlaceOpeningDate | None = None,
    rating: float | None = 4.0,
    state: RatingAcquisitionState | None = None,
    coords: CoordinateState = CoordinateState.VALID,
) -> PlaceSelectionInput:
    candidate = PlaceCandidate(
        place_id=place_id,
        name=place_id,
        latitude=latitude,
        longitude=longitude,
        business_status=status,
        source_query="museum in Sydney",
        category="museum",
        provider_rank=0,
    )
    state = state or (
        RatingAcquisitionState.AVAILABLE if rating is not None else RatingAcquisitionState.MISSING
    )
    evidence = (
        None
        if state in {RatingAcquisitionState.NOT_ATTEMPTED, RatingAcquisitionState.DETAILS_FAILED}
        else PlaceEvidence(
            place_id=place_id,
            name=place_id,
            latitude=latitude,
            longitude=longitude,
            business_status=status,
            rating=rating,
            availability=EvidenceAvailability.AVAILABLE,
            retrieved_at=datetime(2026, 9, 11, tzinfo=UTC),
            source_ref=f"places:{place_id}",
        )
    )
    return PlaceSelectionInput(
        candidate=candidate,
        query_hits=hits or [hit()],
        search_opening_date=opening,
        structured_evidence=evidence,
        rating=rating if state is RatingAcquisitionState.AVAILABLE else None,
        rating_state=state,
        coordinate_state=coords,
    )


@pytest.mark.parametrize(
    ("status", "risk"),
    [
        ("OPERATIONAL", DateRisk.NONE),
        (None, DateRisk.UNKNOWN_STATUS),
        ("CLOSED_TEMPORARILY", DateRisk.TEMPORARILY_CLOSED_VERIFY),
        ("FUTURE_OPENING", DateRisk.FUTURE_OPENING_VERIFY),
    ],
)
def test_nonpermanent_status_retained_without_future_open_claim(
    status: str | None, risk: DateRisk
) -> None:
    result = evaluate_poi_eligibility(place("a", status=status), trip_end=END)
    assert result.eligible
    assert result.date_risk == risk


@pytest.mark.parametrize(
    ("opening", "eligible", "boundary"),
    [
        (PlaceOpeningDate(year=2026, month=9, day=11), True, date(2026, 9, 11)),
        (PlaceOpeningDate(year=2026, month=9, day=13), True, date(2026, 9, 13)),
        (PlaceOpeningDate(year=2026, month=9, day=15), False, date(2026, 9, 15)),
        (PlaceOpeningDate(year=2026, month=9), True, date(2026, 9, 1)),
        (PlaceOpeningDate(year=2026, month=10), False, date(2026, 10, 1)),
        (PlaceOpeningDate(year=2026), True, date(2026, 1, 1)),
        (PlaceOpeningDate(year=2027), False, date(2027, 1, 1)),
        (PlaceOpeningDate(month=9, day=15), True, None),
        (None, True, None),
    ],
)
def test_future_opening_uses_only_supported_date_precision(
    opening: PlaceOpeningDate | None, eligible: bool, boundary: date | None
) -> None:
    evaluation = evaluate_poi_eligibility(
        place("a", status="FUTURE_OPENING", opening=opening), trip_end=END
    )
    assert evaluation.eligible is eligible
    assert evaluation.date_risk == DateRisk.FUTURE_OPENING_VERIFY
    assert evaluation.not_visitable_before == boundary


def test_details_opening_date_takes_precedence_over_search_observation() -> None:
    candidate = place(
        "a",
        status="FUTURE_OPENING",
        opening=PlaceOpeningDate(year=2026, month=9, day=12),
    ).model_copy(update={"details_opening_date": PlaceOpeningDate(year=2026, month=9, day=16)})
    evaluation = evaluate_poi_eligibility(candidate, trip_end=END)
    assert evaluation.reason == "opening_definitely_after_trip"
    assert evaluation.not_visitable_before == date(2026, 9, 16)
