"""Application services separating HTTP clients from research planners."""

from datetime import date

from backend.app.llm.client import StructuredLLMClient
from backend.app.policies.trip_dates import (
    DateProvider,
    SystemDateProvider,
    create_trip_date_window,
    validate_requested_trip_dates,
)
from backend.app.schemas.planning import PlanningResult
from backend.app.schemas.request import Money, TravelRequest, TravelRequirements
from backend.app.versions.v0.graph import MissingRequiredFieldsError, V0StageError
from backend.app.versions.v0.runner import run_v0


class PlanningNeedsClarificationError(RuntimeError):
    """Signal that the product request lacks requirements needed for planning."""

    def __init__(self, requirements: TravelRequirements) -> None:
        self.requirements = requirements
        super().__init__("The travel request needs clarification")


class PlanningFailedError(RuntimeError):
    """Hide active planner implementation details from the product API."""


def build_canonical_request_text(
    *,
    destination: str,
    start_date: date,
    end_date: date,
    traveler_count: int,
    budget: Money | None,
    additional_preferences: str | None,
) -> str:
    """Build deterministic V0 input using only validated, user-supplied values."""

    traveler_label = "traveler" if traveler_count == 1 else "travelers"
    request_text = (
        f"Plan a trip to {destination} from {start_date.isoformat()} to {end_date.isoformat()} "
        f"for {traveler_count} {traveler_label}"
    )
    if budget is not None:
        request_text += f" with a total budget of {budget.amount} {budget.currency}"
    request_text += "."
    if additional_preferences is not None:
        request_text += f" Additional preferences: {additional_preferences}"
    return request_text


class PlanningService:
    """Run the active planner behind a version-agnostic product boundary."""

    def __init__(
        self,
        llm_client: StructuredLLMClient,
        date_provider: DateProvider | None = None,
    ) -> None:
        self._llm_client = llm_client
        self._date_provider = date_provider or SystemDateProvider()

    async def plan(
        self,
        *,
        destination: str,
        start_date: date,
        end_date: date,
        traveler_count: int,
        budget: Money | None,
        additional_preferences: str | None,
    ) -> PlanningResult:
        """Run the current product planner using its programmatic entry point."""

        reference_date = self._date_provider.today()
        validate_requested_trip_dates(
            start_date,
            end_date,
            create_trip_date_window(reference_date),
        )
        request_text = build_canonical_request_text(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            traveler_count=traveler_count,
            budget=budget,
            additional_preferences=additional_preferences,
        )
        try:
            return await run_v0(
                TravelRequest(request_text=request_text),
                self._llm_client,
                reference_date=reference_date,
            )
        except MissingRequiredFieldsError as exc:
            raise PlanningNeedsClarificationError(exc.requirements) from exc
        except V0StageError as exc:
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
        request: TravelRequest,
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
