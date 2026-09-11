"""FastAPI dependencies for planning services."""

from functools import lru_cache

from backend.app.llm.client import StructuredLLMClient
from backend.app.services.planning import DeveloperPlanningService, PlanningService
from backend.app.versions.v0.config import V0Settings
from backend.app.versions.v0.runner import create_foundry_client


@lru_cache
def get_v0_llm_client() -> StructuredLLMClient:
    """Create the shared V0 LLM client lazily from environment settings."""

    return create_foundry_client(V0Settings())


@lru_cache
def get_planning_service() -> PlanningService:
    """Provide the version-agnostic product planning service."""

    return PlanningService(get_v0_llm_client())


@lru_cache
def get_developer_planning_service() -> DeveloperPlanningService:
    """Provide the locally exposed developer planning service."""

    return DeveloperPlanningService(get_v0_llm_client())
