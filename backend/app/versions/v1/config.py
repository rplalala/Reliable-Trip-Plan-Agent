"""Environment-backed configuration for the independently runnable V1 planner."""

from pathlib import Path

from pydantic import Field, SecretStr

from backend.app.observability.run_trace import TracePayloadMode
from backend.app.runtime.budget import ToolBudgetLimits
from backend.app.versions.v0.config import V0Settings


class V1Settings(V0Settings):
    """V0-compatible model settings plus bounded V1-A provider configuration."""

    google_maps_api_key: SecretStr = Field(
        min_length=1,
        validation_alias="GOOGLE_MAPS_API_KEY",
    )
    v1_trace_enabled: bool = Field(default=True, validation_alias="V1_TRACE_ENABLED")
    v1_trace_directory: Path = Field(
        default=Path("logs"), validation_alias="V1_TRACE_DIRECTORY"
    )
    v1_trace_payload_mode: TracePayloadMode = Field(
        default=TracePayloadMode.METADATA,
        validation_alias="V1_TRACE_PAYLOAD_MODE",
    )
    v1_trace_max_payload_bytes: int = Field(
        default=1_000_000,
        ge=1,
        validation_alias="V1_TRACE_MAX_PAYLOAD_BYTES",
    )
    v1_max_candidates: int = Field(default=20, ge=1, le=20)
    v1_max_place_search_calls: int = Field(default=4, ge=1)
    v1_max_place_detail_calls: int = Field(default=8, ge=1)
    v1_max_route_matrix_elements: int = Field(default=64, ge=1)
    v1_max_weather_calls: int = Field(default=1, ge=0)

    def tool_budget_limits(self) -> ToolBudgetLimits:
        """Build the request-level V1-A budget from validated settings."""

        return ToolBudgetLimits(
            max_candidates=self.v1_max_candidates,
            max_place_search_calls=self.v1_max_place_search_calls,
            max_place_detail_calls=self.v1_max_place_detail_calls,
            max_route_matrix_elements=self.v1_max_route_matrix_elements,
            max_weather_calls=self.v1_max_weather_calls,
        )
