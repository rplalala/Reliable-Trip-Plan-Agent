"""Pure trip-duration capacities for the revised V1-A candidate funnel."""

from dataclasses import dataclass
from datetime import date

from backend.app.policies.trip_dates import (
    TRIP_DATE_WINDOW_DAYS,
    TripDateWindow,
    validate_requested_trip_dates,
)
from backend.app.runtime.budget import ToolBudgetLimits


@dataclass(frozen=True)
class POICapacities:
    trip_days: int
    c_raw: int
    r_pool: int
    k_final: int
    review_pool_cap: int


@dataclass(frozen=True)
class EffectivePOICapacities:
    """Preserve algorithmic maxima alongside explicit operating-budget reductions."""

    algorithmic: POICapacities
    c_raw: int
    r_pool: int
    k_final: int
    review_pool_cap: int
    limiting_budgets: tuple[str, ...]


def derive_poi_capacities(
    start_date: date, end_date: date, window: TripDateWindow
) -> POICapacities:
    """Derive maximum pool sizes only after shared date validation."""

    validate_requested_trip_dates(start_date, end_date, window)
    days = (end_date - start_date).days + 1
    if not 1 <= days <= TRIP_DATE_WINDOW_DAYS:
        raise ValueError("trip duration must be inside the supported 1-10 day horizon")
    k_final = min(16, 2 * days + 2)
    r_pool = max(10, k_final + 2)
    return POICapacities(
        trip_days=days,
        c_raw=max(20, 2 * r_pool),
        r_pool=r_pool,
        k_final=k_final,
        review_pool_cap=min(6, (k_final + 2) // 3),
    )


def apply_poi_operating_budgets(
    capacities: POICapacities, limits: ToolBudgetLimits
) -> EffectivePOICapacities:
    """Make deliberate runtime reductions visible without rewriting the formula."""

    c_raw = min(capacities.c_raw, limits.max_candidates)
    r_pool = min(capacities.r_pool, limits.max_place_detail_calls, c_raw)
    k_final = min(capacities.k_final, limits.max_final_pois, r_pool)
    review_pool_cap = min(
        capacities.review_pool_cap,
        limits.max_review_enriched_places,
        limits.max_review_detail_calls,
        limits.max_experience_profile_llm_calls,
        r_pool,
    )
    reductions = (
        ("c_raw", c_raw, capacities.c_raw),
        ("r_pool", r_pool, capacities.r_pool),
        ("k_final", k_final, capacities.k_final),
        ("review_pool_cap", review_pool_cap, capacities.review_pool_cap),
    )
    return EffectivePOICapacities(
        algorithmic=capacities,
        c_raw=c_raw,
        r_pool=r_pool,
        k_final=k_final,
        review_pool_cap=review_pool_cap,
        limiting_budgets=tuple(name for name, actual, maximum in reductions if actual < maximum),
    )
