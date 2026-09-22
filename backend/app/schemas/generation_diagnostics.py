"""Read-only first-draft measurements; no feasibility or repair decisions."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict


class DayGenerationDiagnostics(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    date: date
    day_present: bool
    applicability: Literal["default_full_day", "same_day_remaining_hours_unsupported"]
    count_basis: Literal["canonical_id", "name_proxy"]
    main_activity_count: int
    distinct_main_poi_count: int
    repeated_main_poi_count: int
    generic_activity_count: int
    transport_activity_count: int
    free_time_activity_count: int
    unclassified_activity_count: int
    target_status: Literal["within_target", "below_target", "above_target", "not_assessable"]
    empty_day: bool


class GenerationDiagnostics(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    days: tuple[DayGenerationDiagnostics, ...]
    days_meeting_default_target: int
    days_below_target: int
    days_above_target: int
    days_unassessable: int
    empty_days: int
    days_with_zero_main_pois: int
    scheduled_unique_supply: int | None
    unused_supply: int | None
    cross_day_repeated_visits: int
    related_requirement_ids: tuple[str, ...] = ()
    assessment_basis: Literal["default_target_observation_not_feasibility"] = (
        "default_target_observation_not_feasibility"
    )
