"""V1 itinerary output selector and bounded cost-projection diagnostics."""

from dataclasses import dataclass
from typing import Literal

from pydantic import PrivateAttr

from backend.app.schemas.itinerary import Itinerary

CostProjectionType = Literal[
    "exact_point", "midpoint_from_range", "explicit_null", "invalid_set_null"
]


@dataclass(frozen=True)
class EstimatedCostProjectionDiagnostic:
    field_path: str
    projection: CostProjectionType
    currency: str | None = None
    lower_bound: str | None = None
    upper_bound: str | None = None
    midpoint: str | None = None
    error_category: str | None = None

    def as_trace_payload(self) -> dict[str, str | None]:
        """Expose only bounded metadata, never the planner response."""

        return {
            "stage": "itinerary_cost_projection",
            "field_path": self.field_path,
            "estimated_cost_projection": self.projection,
            "currency": self.currency,
            "lower_bound": self.lower_bound,
            "upper_bound": self.upper_bound,
            "midpoint": self.midpoint,
            "error_category": self.error_category,
        }


class V1Itinerary(Itinerary):
    """The unchanged Itinerary domain contract with V1-only projection metadata."""

    _cost_projections: tuple[EstimatedCostProjectionDiagnostic, ...] = PrivateAttr(default=())

    @property
    def cost_projections(self) -> tuple[EstimatedCostProjectionDiagnostic, ...]:
        return self._cost_projections

    def set_cost_projections(
        self, projections: tuple[EstimatedCostProjectionDiagnostic, ...]
    ) -> None:
        self._cost_projections = projections
