"""One project-wide source of hard safety ceilings for tool usage."""

from dataclasses import dataclass
from enum import StrEnum


class ToolBudgetKey(StrEnum):
    """Provider operations and bounded result dimensions tracked per run."""

    CANDIDATES = "candidates"
    PLACE_SEARCH_CALLS = "place_search_calls"
    PLACE_DETAIL_CALLS = "place_detail_calls"
    REVIEW_ENRICHED_PLACES = "review_enriched_places"
    WEB_EVIDENCE_TASKS = "web_evidence_tasks"
    PAGE_FETCHES = "page_fetches"
    ROUTE_MATRIX_ELEMENTS = "route_matrix_elements"
    ALTERNATIVE_ROUTE_PAIRS = "alternative_route_pairs"
    ALTERNATIVE_ROUTE_MATRIX_CALLS = "alternative_route_matrix_calls"
    WEATHER_CALLS = "weather_calls"


@dataclass(frozen=True)
class BudgetHardLimit:
    minimum: int
    maximum: int


TOOL_BUDGET_HARD_LIMITS: dict[ToolBudgetKey, BudgetHardLimit] = {
    ToolBudgetKey.CANDIDATES: BudgetHardLimit(1, 40),
    ToolBudgetKey.PLACE_SEARCH_CALLS: BudgetHardLimit(1, 12),
    ToolBudgetKey.PLACE_DETAIL_CALLS: BudgetHardLimit(1, 20),
    ToolBudgetKey.REVIEW_ENRICHED_PLACES: BudgetHardLimit(0, 8),
    ToolBudgetKey.WEB_EVIDENCE_TASKS: BudgetHardLimit(0, 20),
    ToolBudgetKey.PAGE_FETCHES: BudgetHardLimit(0, 20),
    ToolBudgetKey.ROUTE_MATRIX_ELEMENTS: BudgetHardLimit(1, 100),
    ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS: BudgetHardLimit(0, 16),
    ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS: BudgetHardLimit(0, 8),
    ToolBudgetKey.WEATHER_CALLS: BudgetHardLimit(0, 3),
}


def validate_budget_values(values: dict[ToolBudgetKey, int]) -> None:
    """Reject runtime budgets outside the single project-wide safety envelope."""

    for key in ToolBudgetKey:
        value = values[key]
        limit = TOOL_BUDGET_HARD_LIMITS[key]
        if not limit.minimum <= value <= limit.maximum:
            raise ValueError(
                f"{key.value} must be between {limit.minimum} and {limit.maximum}; got {value}"
            )
