"""V1-only supply result; scheduled itinerary remains a separate output."""

from typing import Literal

from backend.app.policies.itinerary_output import OutputRoleSummary
from backend.app.policies.planning_supply import PlanningSupplyResult
from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements
from backend.app.schemas.planning import PlanningResult


class PlanningSupplyPlanningResult(PlanningResult):
    interpreted_requirements: InterpretedTripRequirements
    selection_status: Literal["selected", "degraded_selection"]
    selection_contract_version: Literal["planning_supply_1"] = "planning_supply_1"
    output_role_summary: OutputRoleSummary | None = None
    planning_supply: PlanningSupplyResult
