"""Deployment-specific provider settings for the independently runnable V1 planner."""

from pydantic import Field, SecretStr

from backend.app.runtime.budget import ToolBudgetLimits
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.versions.v0.config import V0Settings


class V1Settings(V0Settings):
    """V0-compatible Foundry settings plus the V1 Google credential."""

    google_maps_api_key: SecretStr = Field(
        min_length=1,
        validation_alias="GOOGLE_MAPS_API_KEY",
    )

    def tool_budget_limits(self) -> ToolBudgetLimits:
        """Build request limits from the one validated global YAML policy."""

        runtime_budget = load_runtime_config().budget
        return ToolBudgetLimits.model_validate(
            {
                **{
                    f"max_{key.value}": value
                    for key, value in runtime_budget.as_key_limits().items()
                },
                "max_baseline_route_matrix_elements_per_request": (
                    runtime_budget.routes.baseline_elements_per_request
                ),
            }
        )
