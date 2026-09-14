"""Request-level limits for bounded V1 external information acquisition."""

from collections import Counter

from pydantic import BaseModel, ConfigDict, Field, StrictInt, model_validator

from backend.app.runtime.budget_limits import (
    ToolBudgetKey,
    validate_baseline_per_request_elements,
    validate_budget_values,
)


def _configured_default(key: ToolBudgetKey) -> int:
    from backend.app.runtime.config_loader import load_runtime_config

    return load_runtime_config().budget.as_key_limits()[key]


def _configured_baseline_per_request_default() -> int:
    from backend.app.runtime.config_loader import load_runtime_config

    return load_runtime_config().budget.routes.baseline_elements_per_request


class ToolBudgetLimits(BaseModel):
    """Small versioned default limits for one V1 request."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    max_candidates: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.CANDIDATES)
    )
    max_destination_search_calls: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.DESTINATION_SEARCH_CALLS)
    )
    max_candidate_search_calls: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.CANDIDATE_SEARCH_CALLS)
    )
    max_place_detail_calls: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.PLACE_DETAIL_CALLS)
    )
    max_review_detail_calls: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.REVIEW_DETAIL_CALLS)
    )
    max_review_enriched_places: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.REVIEW_ENRICHED_PLACES)
    )
    max_experience_profile_llm_calls: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS)
    )
    max_final_pois: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.FINAL_POIS)
    )
    max_web_evidence_tasks: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.WEB_EVIDENCE_TASKS)
    )
    max_page_fetches: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.PAGE_FETCHES)
    )
    max_route_matrix_elements: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.ROUTE_MATRIX_ELEMENTS)
    )
    max_baseline_route_matrix_elements_per_request: StrictInt = Field(
        default_factory=_configured_baseline_per_request_default
    )
    max_baseline_route_matrix_elements: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS)
    )
    max_baseline_route_matrix_calls: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS)
    )
    max_alternative_route_pairs: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS)
    )
    max_alternative_route_matrix_calls: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS)
    )
    max_weather_calls: StrictInt = Field(
        default_factory=lambda: _configured_default(ToolBudgetKey.WEATHER_CALLS)
    )

    @model_validator(mode="after")
    def within_hard_limits(self) -> "ToolBudgetLimits":
        validate_budget_values(self.as_key_limits())
        validate_baseline_per_request_elements(self.max_baseline_route_matrix_elements_per_request)
        if (
            self.max_baseline_route_matrix_elements_per_request
            > self.max_baseline_route_matrix_elements
        ):
            raise ValueError(
                "baseline_route_matrix_elements_per_request must not exceed the per-run limit"
            )
        if self.max_review_detail_calls < self.max_review_enriched_places:
            raise ValueError("review_detail_calls must cover review_enriched_places")
        if self.max_experience_profile_llm_calls < self.max_review_enriched_places:
            raise ValueError("experience_profile_llm_calls must cover review_enriched_places")
        return self

    def as_key_limits(self) -> dict[ToolBudgetKey, int]:
        """Map public setting names to runtime counter keys."""

        return {
            ToolBudgetKey.CANDIDATES: self.max_candidates,
            ToolBudgetKey.DESTINATION_SEARCH_CALLS: self.max_destination_search_calls,
            ToolBudgetKey.CANDIDATE_SEARCH_CALLS: self.max_candidate_search_calls,
            ToolBudgetKey.PLACE_DETAIL_CALLS: self.max_place_detail_calls,
            ToolBudgetKey.REVIEW_DETAIL_CALLS: self.max_review_detail_calls,
            ToolBudgetKey.REVIEW_ENRICHED_PLACES: self.max_review_enriched_places,
            ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS: self.max_experience_profile_llm_calls,
            ToolBudgetKey.FINAL_POIS: self.max_final_pois,
            ToolBudgetKey.WEB_EVIDENCE_TASKS: self.max_web_evidence_tasks,
            ToolBudgetKey.PAGE_FETCHES: self.max_page_fetches,
            ToolBudgetKey.ROUTE_MATRIX_ELEMENTS: self.max_route_matrix_elements,
            ToolBudgetKey.BASELINE_ROUTE_MATRIX_ELEMENTS: (self.max_baseline_route_matrix_elements),
            ToolBudgetKey.BASELINE_ROUTE_MATRIX_CALLS: self.max_baseline_route_matrix_calls,
            ToolBudgetKey.ALTERNATIVE_ROUTE_PAIRS: self.max_alternative_route_pairs,
            ToolBudgetKey.ALTERNATIVE_ROUTE_MATRIX_CALLS: (self.max_alternative_route_matrix_calls),
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

        self.consume_many(((key, amount),))

    def consume_many(self, charges: tuple[tuple[ToolBudgetKey, int], ...]) -> None:
        """Atomically reserve several related counters before provider work."""

        requested: Counter[ToolBudgetKey] = Counter()
        for key, amount in charges:
            if amount < 0:
                raise ValueError("Tool budget consumption cannot be negative")
            requested[key] += amount
        for key, amount in requested.items():
            used = self._usage[key]
            limit = self._limits[key]
            if used + amount > limit:
                raise ToolBudgetExceededError(key, amount, used, limit)
        self._usage.update(requested)

    def remaining(self, key: ToolBudgetKey) -> int:
        """Return unused capacity for one budget key."""

        return self._limits[key] - self._usage[key]

    def summary(self) -> dict[str, dict[str, int]]:
        """Return JSON-safe limits and usage for tracing."""

        return {
            key.value: {"used": self._usage[key], "limit": limit}
            for key, limit in self._limits.items()
        }
