"""Trip-derived candidate capacity and explicit runtime reduction tests."""

from datetime import date, timedelta

import pytest

from backend.app.policies.poi_capacity import (
    apply_poi_operating_budgets,
    derive_poi_capacities,
)
from backend.app.policies.trip_dates import (
    TripDatePolicyError,
    create_trip_date_window,
)
from backend.app.runtime.budget import ToolBudgetLimits

REFERENCE = date(2026, 9, 11)
WINDOW = create_trip_date_window(REFERENCE)


@pytest.mark.parametrize(
    ("days", "expected"),
    [
        (1, (20, 10, 4, 2)),
        (3, (20, 10, 8, 3)),
        (4, (24, 12, 10, 4)),
        (7, (36, 18, 16, 6)),
        (10, (36, 18, 16, 6)),
    ],
)
def test_approved_duration_capacities(days: int, expected: tuple[int, ...]) -> None:
    result = derive_poi_capacities(REFERENCE, REFERENCE + timedelta(days=days - 1), WINDOW)
    assert (result.c_raw, result.r_pool, result.k_final, result.review_pool_cap) == expected


@pytest.mark.parametrize(
    ("start", "end"),
    [
        (REFERENCE - timedelta(days=1), REFERENCE),
        (REFERENCE, REFERENCE + timedelta(days=10)),
        (REFERENCE + timedelta(days=1), REFERENCE),
    ],
)
def test_invalid_dates_cannot_derive_capacity(start: date, end: date) -> None:
    with pytest.raises(TripDatePolicyError):
        derive_poi_capacities(start, end, WINDOW)


def test_runtime_limits_do_not_redefine_algorithmic_capacity() -> None:
    original = derive_poi_capacities(REFERENCE, REFERENCE + timedelta(days=9), WINDOW)
    effective = apply_poi_operating_budgets(
        original,
        ToolBudgetLimits(
            max_candidates=24,
            max_place_detail_calls=12,
            max_final_pois=10,
            max_review_enriched_places=3,
            max_review_detail_calls=3,
            max_experience_profile_llm_calls=3,
        ),
    )
    assert effective.algorithmic == original
    assert (effective.c_raw, effective.r_pool, effective.k_final, effective.review_pool_cap) == (
        24,
        12,
        10,
        3,
    )
    assert effective.limiting_budgets == ("c_raw", "r_pool", "k_final", "review_pool_cap")


def test_default_runtime_covers_algorithmic_maxima() -> None:
    maximum = derive_poi_capacities(REFERENCE, REFERENCE + timedelta(days=9), WINDOW)
    effective = apply_poi_operating_budgets(maximum, ToolBudgetLimits())
    assert effective.limiting_budgets == ()
    assert (effective.c_raw, effective.r_pool, effective.k_final, effective.review_pool_cap) == (
        36,
        18,
        16,
        6,
    )


@pytest.mark.parametrize("days", range(1, 11))
def test_departure_offset_does_not_increase_quality_capacity(days):
    from backend.app.policies.poi_capacity import quality_capacities

    base = quality_capacities(REFERENCE, REFERENCE + timedelta(days=days - 1), WINDOW)
    delayed = quality_capacities(
        REFERENCE + timedelta(days=4), REFERENCE + timedelta(days=days + 3), WINDOW
    )
    assert delayed == base
    assert delayed.k_final <= 20
