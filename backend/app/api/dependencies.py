"""FastAPI dependencies for planning services."""

from functools import lru_cache

from backend.app.llm.client import StructuredLLMClient
from backend.app.policies.trip_dates import DateProvider, SystemDateProvider
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.runtime.logging_config import configure_logging
from backend.app.services.planning import DeveloperPlanningService, PlanningService
from backend.app.versions.v0.config import V0Settings
from backend.app.versions.v0.runner import create_foundry_client


@lru_cache
def get_v0_llm_client() -> StructuredLLMClient:
    """Create the shared V0 LLM client lazily from environment settings."""

    return create_foundry_client(V0Settings())


@lru_cache
def get_date_provider() -> DateProvider:
    """Provide the trusted configured-zone date source for production requests."""

    runtime_config = load_runtime_config()
    configure_logging(runtime_config.logging)
    return SystemDateProvider(runtime_config.app.time_zone)


@lru_cache
def get_planning_service() -> PlanningService:
    """Provide the version-agnostic product planning service."""

    return PlanningService(get_v0_llm_client(), get_date_provider())


@lru_cache
def get_developer_planning_service() -> DeveloperPlanningService:
    """Provide the locally exposed developer planning service."""

    return DeveloperPlanningService(get_v0_llm_client(), get_date_provider())
