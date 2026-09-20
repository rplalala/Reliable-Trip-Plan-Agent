"""Application services separating HTTP clients from research planners."""

from datetime import date

from backend.app.llm.client import StructuredLLMClient
from backend.app.policies.trip_dates import (
    DateProvider,
    SystemDateProvider,
)
from backend.app.schemas.interpreted_requirements import ClarificationRequired
from backend.app.schemas.planning import PlanningResult
from backend.app.schemas.request import PlanningRequest, TravelRequirements
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.app.versions.v0.graph import V0StageError
from backend.app.versions.v0.runner import run_v0


class PlanningNeedsClarificationError(RuntimeError):
    """Signal that the product request lacks requirements needed for planning."""

    def __init__(self, requirements: TravelRequirements, issues: dict | None = None) -> None:
        self.issues = issues or {}
        self.requirements = requirements
        super().__init__("The travel request needs clarification")


class PlanningFailedError(RuntimeError):
    """Hide active planner implementation details from the product API."""


class PlanningService:
    """Run the active planner behind a version-agnostic product boundary."""

    def __init__(
        self,
        llm_client: StructuredLLMClient,
        date_provider: DateProvider | None = None,
    ) -> None:
        self._llm_client = llm_client
        self._date_provider = date_provider or SystemDateProvider()

    async def plan(self, request: PlanningRequest) -> PlanningResult:
        """The product engine remains V0; input semantics do not select an engine."""
        try:
            return await run_v0(request, self._llm_client, date_provider=self._date_provider)
        except ClarificationRequired as exc:
            raise PlanningNeedsClarificationError(
                request.trip_requirements(), exc.as_dict()
            ) from exc
        except (V0StageError, RequirementBoundaryError) as exc:
            raise PlanningFailedError("The active planner failed") from exc


class DeveloperPlanningService:
    """Run currently implemented research planners for local inspection."""

    def __init__(
        self,
        llm_client: StructuredLLMClient,
        date_provider: DateProvider | None = None,
    ) -> None:
        self._llm_client = llm_client
        self._date_provider = date_provider or SystemDateProvider()

    async def plan_v0(
        self,
        request: PlanningRequest,
        *,
        reference_date: date | None = None,
    ) -> PlanningResult:
        """Run V0 directly while preserving its research-facing behavior."""

        effective_reference_date = reference_date or self._date_provider.today()
        return await run_v0(
            request,
            self._llm_client,
            reference_date=effective_reference_date,
        )
