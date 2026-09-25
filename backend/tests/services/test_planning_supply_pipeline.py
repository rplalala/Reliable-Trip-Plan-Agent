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


def test_quality_primary_details_uses_yaml_allowance_without_expanding_success_target():
    from backend.app.runtime.config_loader import load_runtime_config

    config = load_runtime_config()
    pipeline = object.__new__(PlanningCandidateSupplyPipeline)
    pipeline.acquisition = SimpleNamespace(
        _budget=ToolBudget(ToolBudgetLimits()), runtime_config=config
    )
    pipeline.tracer = SimpleNamespace(event=lambda *args: None)
    requirements = SimpleNamespace(start_date=date(2026, 9, 26), end_date=date(2026, 10, 2))
    caps = pipeline.capacities(requirements, create_trip_date_window(date(2026, 9, 25)))
    effective = pipeline.required_capacities(caps, 0)
    assert pipeline.acquisition._budget.limits.max_place_detail_calls == 60
    assert effective.r_pool == 32
    assert config.tripworld_discovery.details_calls == 30
    assert config.v3_repair.acquisition.details == 30
