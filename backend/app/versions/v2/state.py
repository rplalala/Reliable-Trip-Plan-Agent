"""V2 keeps the shared itinerary shape and exposes separate RAG diagnostics."""

from pydantic import Field

from backend.app.schemas.planning_supply_result import PlanningSupplyPlanningResult


class V2PlanningResult(PlanningSupplyPlanningResult):
    rag_discovery: dict = Field(default_factory=dict)
