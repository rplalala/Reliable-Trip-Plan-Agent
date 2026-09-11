"""Request-level limits for bounded V1 external information acquisition."""

from collections import Counter
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ToolBudgetKey(StrEnum):
    """Provider operations and bounded result dimensions tracked per run."""

    CANDIDATES = "candidates"
    PLACE_SEARCH_CALLS = "place_search_calls"
    PLACE_DETAIL_CALLS = "place_detail_calls"
    REVIEW_ENRICHED_PLACES = "review_enriched_places"
    WEB_SEARCH_QUERIES = "web_search_queries"
    PAGE_FETCHES = "page_fetches"
    ROUTE_MATRIX_ELEMENTS = "route_matrix_elements"
    WEATHER_CALLS = "weather_calls"


class ToolBudgetLimits(BaseModel):
    """Small versioned default limits for one V1 request."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    max_candidates: int = Field(default=20, ge=1, le=20)
    max_place_search_calls: int = Field(default=4, ge=1)
    max_place_detail_calls: int = Field(default=8, ge=1)
    max_review_enriched_places: int = Field(default=3, ge=0)
    max_web_search_queries: int = Field(default=6, ge=0)
    max_page_fetches: int = Field(default=6, ge=0)
    max_route_matrix_elements: int = Field(default=64, ge=1)
    max_weather_calls: int = Field(default=1, ge=0)

    def as_key_limits(self) -> dict[ToolBudgetKey, int]:
        """Map public setting names to runtime counter keys."""

        return {
            ToolBudgetKey.CANDIDATES: self.max_candidates,
            ToolBudgetKey.PLACE_SEARCH_CALLS: self.max_place_search_calls,
            ToolBudgetKey.PLACE_DETAIL_CALLS: self.max_place_detail_calls,
            ToolBudgetKey.REVIEW_ENRICHED_PLACES: self.max_review_enriched_places,
            ToolBudgetKey.WEB_SEARCH_QUERIES: self.max_web_search_queries,
            ToolBudgetKey.PAGE_FETCHES: self.max_page_fetches,
            ToolBudgetKey.ROUTE_MATRIX_ELEMENTS: self.max_route_matrix_elements,
            ToolBudgetKey.WEATHER_CALLS: self.max_weather_calls,
        }


class ToolBudgetExceededError(RuntimeError):
    """Raised before a provider call or result would exceed its hard limit."""

    def __init__(self, key: ToolBudgetKey, requested: int, used: int, limit: int) -> None:
        self.key = key
        self.requested = requested
        self.used = used
        self.limit = limit
        super().__init__(
            f"Tool budget exceeded for {key.value}: used={used}, "
            f"requested={requested}, limit={limit}"
        )


class ToolBudget:
    """Mutable usage counters owned by exactly one V1 run."""

    def __init__(self, limits: ToolBudgetLimits | None = None) -> None:
        self.limits = limits or ToolBudgetLimits()
        self._limits = self.limits.as_key_limits()
        self._usage: Counter[ToolBudgetKey] = Counter()

    def consume(self, key: ToolBudgetKey, amount: int = 1) -> None:
        """Reserve capacity deterministically before performing work."""

        if amount < 0:
            raise ValueError("Tool budget consumption cannot be negative")
        used = self._usage[key]
        limit = self._limits[key]
        if used + amount > limit:
            raise ToolBudgetExceededError(key, amount, used, limit)
        self._usage[key] += amount

    def remaining(self, key: ToolBudgetKey) -> int:
        """Return unused capacity for one budget key."""

        return self._limits[key] - self._usage[key]

    def summary(self) -> dict[str, dict[str, int]]:
        """Return JSON-safe limits and usage for tracing."""

        return {
            key.value: {"used": self._usage[key], "limit": limit}
            for key, limit in self._limits.items()
        }
