"""Shared planning state and result contracts."""

from enum import StrEnum
from typing import NotRequired, TypedDict

from pydantic import BaseModel, ConfigDict

from backend.app.schemas.generation_diagnostics import GenerationDiagnostics
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import PlanningRequest, TravelRequirements


class SystemVersion(StrEnum):
    """Independently runnable system versions."""

    V0 = "v0"
    V1 = "v1"
    V2 = "v2"
    V3 = "v3"


class SharedPlanningState(TypedDict):
    """Minimum evolving state shared by every planning version."""

    request: PlanningRequest
    requirements: NotRequired[TravelRequirements]
    itinerary: NotRequired[Itinerary]


class PlanningResult(BaseModel):
    """Stable output fields that are common to every system version."""

    model_config = ConfigDict(extra="forbid")

    generation_diagnostics: GenerationDiagnostics | None = None
    system_version: SystemVersion
    requirements: TravelRequirements
    itinerary: Itinerary
