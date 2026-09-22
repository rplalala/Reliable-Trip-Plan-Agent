"""Acquisition limits expand for must-visits only, never by changing tool budgets."""

from datetime import date
from types import SimpleNamespace

import pytest

from backend.app.policies.poi_capacity import apply_poi_operating_budgets, derive_poi_capacities
from backend.app.policies.trip_dates import create_trip_date_window
from backend.app.runtime.budget import ToolBudget, ToolBudgetLimits
from backend.app.schemas.interpreted_requirements import ClarificationRequired
from backend.app.services.planning_supply_pipeline import PlanningCandidateSupplyPipeline


def test_required_expansion_preserves_normal_capacity_and_hard_limits():
    limits = ToolBudgetLimits()
    budget = ToolBudget(limits)
    pipeline = object.__new__(PlanningCandidateSupplyPipeline)
    pipeline.acquisition = SimpleNamespace(_budget=budget)
    capacities = apply_poi_operating_budgets(
        derive_poi_capacities(
            date(2026, 9, 21),
            date(2026, 9, 23),
            create_trip_date_window(date(2026, 9, 19)),
        ),
        limits,
    )
    expanded = pipeline.required_capacities(capacities, 12)
    assert capacities.k_final == expanded.k_final == 8
    assert expanded.r_pool == 12
    assert expanded.c_raw == capacities.c_raw
    assert budget.limits == limits
    with pytest.raises(ClarificationRequired, match="required_capacity_conflict"):
        pipeline.required_capacities(capacities, limits.max_final_pois + 1)
