"""Consecutive origin blocks for a complete, directed baseline Route Matrix."""

from collections.abc import Sequence

from backend.app.integrations.models import RouteWaypoint
from backend.app.runtime.budget_limits import TOOL_BUDGET_HARD_LIMITS, ToolBudgetKey


def partition_baseline_origins(
    waypoints: Sequence[RouteWaypoint], *, per_request_element_limit: int
) -> tuple[tuple[RouteWaypoint, ...], ...]:
    """Keep all destinations in every block; never truncate selected POIs."""

    count = len(waypoints)
    if count == 0:
        return ()
    if count > TOOL_BUDGET_HARD_LIMITS[ToolBudgetKey.FINAL_POIS].maximum:
        raise ValueError("Selected POIs exceed the project-wide final-POI hard limit")
    if len({item.place_id for item in waypoints}) != count:
        raise ValueError("Baseline Route Matrix requires unique selected Place IDs")
    if per_request_element_limit < count:
        raise ValueError("Per-request Route Matrix limit cannot fit one complete origin row")
    origins_per_block = per_request_element_limit // count
    return tuple(
        tuple(waypoints[offset : offset + origins_per_block])
        for offset in range(0, count, origins_per_block)
    )
