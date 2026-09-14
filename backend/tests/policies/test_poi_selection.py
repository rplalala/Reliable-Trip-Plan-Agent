"""Pure revised V1-A POI selection policy regression tests."""

from datetime import UTC, date, datetime
from decimal import Decimal

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
    c_cov,
    evaluate_poi_eligibility,
    g_geo,
    q_rel,
    r_rating,
    select_pois,
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


def choose(
    places: list[PlaceSelectionInput],
    *,
    capacity: int = 2,
    **kwargs: object,
):
    return select_pois(
        places,
        start_date=START,
        end_date=END,
        window=WINDOW,
        capacity=capacity,
        **kwargs,
    )


@pytest.mark.parametrize(
    ("rank", "count", "kind", "expected"),
    [
        (0, 1, SearchIntentKind.EXPLICIT_REQUIREMENT, Decimal(30)),
        (0, 5, SearchIntentKind.EXPLICIT_REQUIREMENT, Decimal(30)),
        (2, 5, SearchIntentKind.EXPLICIT_REQUIREMENT, Decimal(15)),
        (4, 5, SearchIntentKind.EXPLICIT_REQUIREMENT, Decimal(0)),
        (0, 5, SearchIntentKind.NORMAL_PREFERENCE, Decimal(24)),
        (0, 5, SearchIntentKind.FALLBACK, Decimal(12)),
    ],
)
def test_q_uses_original_rank_result_count_and_intent_weight(
    rank: int, count: int, kind: SearchIntentKind, expected: Decimal
) -> None:
    assert q_rel([hit(rank=rank, count=count, kind=kind)]) == expected


def test_q_takes_maximum_of_preserved_multi_intent_hits() -> None:
    assert q_rel(
        [
            hit("first", rank=4, count=5),
            hit("second", rank=1, count=5, kind=SearchIntentKind.NORMAL_PREFERENCE),
        ]
    ) == Decimal(18)


def test_c_uses_maximum_uncovered_weight_and_recomputes() -> None:
    hits = [
        hit("museum", kind=SearchIntentKind.EXPLICIT_REQUIREMENT),
        hit("food", kind=SearchIntentKind.NORMAL_PREFERENCE),
    ]
    assert c_cov(hits, frozenset()) == Decimal(25)
    assert c_cov(hits, frozenset({"museum"})) == Decimal(20)
    assert c_cov(hits, frozenset({"museum", "food"})) == 0


def test_g_uses_spherical_thresholds() -> None:
    anchor = place("anchor")
    assert g_geo(place("empty"), []) == 5
    assert g_geo(place("near", latitude=-33.88), [anchor]) == 10
    assert g_geo(place("middle", latitude=-33.92), [anchor]) == 5
    assert g_geo(place("far", latitude=-34.00), [anchor]) == 0


@pytest.mark.parametrize(
    ("rating", "expected"),
    [
        (None, Decimal(0)),
        (1.0, Decimal(-10)),
        (3.5, Decimal(0)),
        (4.25, Decimal(5)),
        (5.0, Decimal(10)),
        (float("nan"), Decimal(0)),
    ],
)
def test_r_rating_neutral_missing_and_clamped(rating: float | None, expected: Decimal) -> None:
    assert r_rating(rating) == expected


@pytest.mark.parametrize("value", [-15, 0, 10])
def test_e_exp_accepts_neutral_and_bounds(value: int) -> None:
    result = choose([place("a")], capacity=1, experience_scores={"a": value})
    assert result.selected[0].score is not None
    assert result.selected[0].score.e_exp == value
    assert choose([place("a")], capacity=1).selected[0].score.e_exp == 0


@pytest.mark.parametrize("value", [-16, 11, float("nan")])
def test_e_exp_rejects_invalid_values(value: float) -> None:
    with pytest.raises(ValueError, match="E_exp"):
        choose([place("a")], experience_scores={"a": value})


def test_explicit_exclusion_and_permanent_closure_precede_scoring() -> None:
    result = choose(
        [place("excluded", rating=5), place("closed", status="CLOSED_PERMANENTLY"), place("ok")],
        excluded_place_ids=frozenset({"excluded"}),
    )
    assert result.selected_place_ids == ("ok",)
    assert {item.place_id: item.reason for item in result.eligibility} == {
        "closed": "permanently_closed",
        "excluded": "explicitly_excluded",
        "ok": None,
    }


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
    result = choose([place("a", status=status)])
    assert result.selected_place_ids == ("a",)
    assert result.selected[0].date_risk == risk


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


def test_missing_rating_is_neutral_but_details_failure_is_ineligible() -> None:
    result = choose(
        [
            place("missing", rating=None),
            place("failed", rating=None, state=RatingAcquisitionState.DETAILS_FAILED),
        ]
    )
    assert result.selected_place_ids == ("missing",)
    assert result.selected[0].score.r_rating == 0
    assert {item.place_id: item.reason for item in result.eligibility}["failed"] == (
        "structured_details_failed"
    )


@pytest.mark.parametrize(
    ("bad_place", "reason"),
    [
        (
            place("failed", rating=None, state=RatingAcquisitionState.DETAILS_FAILED),
            "structured_details_failed",
        ),
        (place("closed", status="CLOSED_PERMANENTLY"), "permanently_closed"),
        (
            place("future", status="FUTURE_OPENING", opening=PlaceOpeningDate(year=2027)),
            "opening_definitely_after_trip",
        ),
        (place("unrouteable", coords=CoordinateState.INVALID), "invalid_or_missing_coordinates"),
    ],
)
def test_bad_must_visit_reports_conflict_without_substituting(
    bad_place: PlaceSelectionInput, reason: str
) -> None:
    result = choose(
        [bad_place, place("normal")], must_visit_place_ids=frozenset({bad_place.candidate.place_id})
    )
    assert (bad_place.candidate.place_id, reason) in [
        (item.place_id_or_name, item.reason) for item in result.conflicts
    ]
    assert result.selected_place_ids == ("normal",)


def test_must_visits_are_pinned_despite_low_rank_rating_or_missing_rating() -> None:
    must = place("must", hits=[hit(rank=4)], rating=None)
    result = choose(
        [place("top", rating=5), must], capacity=1, must_visit_place_ids=frozenset({"must"})
    )
    assert result.selected_place_ids == ("must",)
    assert result.selected[0].must_visit is True


def test_too_many_and_unresolved_must_visits_report_conflicts() -> None:
    result = choose(
        [place("a"), place("b")],
        capacity=1,
        must_visit_place_ids=frozenset({"a", "b", "missing"}),
        unresolved_required_names=("Named attraction",),
    )
    reasons = {item.reason for item in result.conflicts}
    assert {"must_visits_exceed_capacity", "required_place_unresolved"} <= reasons


def test_provisional_and_final_use_same_engine_with_details_eligibility_switch() -> None:
    candidate = place("a", rating=None, state=RatingAcquisitionState.NOT_ATTEMPTED)
    assert choose([candidate], require_details=False).selected_place_ids == ("a",)
    assert choose([candidate], require_details=True).selected_place_ids == ()


def test_coordinate_state_prevents_nonrouteable_selection() -> None:
    assert choose([place("a", coords=CoordinateState.MISSING)]).selected_place_ids == ()


def test_greedy_recomputes_coverage_after_each_choice() -> None:
    first = place("first", hits=[hit("museum", rank=0)])
    redundant = place("redundant", hits=[hit("museum", rank=1)])
    other = place("other", hits=[hit("beach", rank=2)])
    result = choose([other, redundant, first], capacity=2)
    assert result.selected_place_ids == ("first", "other")
    assert result.selected[1].score.c_cov == 25


def test_tie_breaks_by_best_original_rank_then_place_id_not_input_order() -> None:
    best = place(
        "z",
        hits=[
            hit("museum", rank=1, count=3),
            hit("food", rank=0, kind=SearchIntentKind.FALLBACK),
        ],
    )
    later = place("a", hits=[hit("museum", rank=1, count=3)])
    assert choose([later, best], capacity=1).selected_place_ids == ("z",)
    a = place("a", hits=[hit(rank=0)])
    b = place("b", hits=[hit(rank=0)])
    assert choose([b, a], capacity=2).selected_place_ids[0] == "a"
    assert choose([a, b], capacity=2).selected_place_ids[0] == "a"


def test_repeated_identical_runs_are_equal_and_duplicate_ids_rejected() -> None:
    inputs = [place("b"), place("a")]
    assert choose(inputs) == choose(inputs)
    with pytest.raises(ValueError, match="unique Place IDs"):
        choose([inputs[0], inputs[0]])
