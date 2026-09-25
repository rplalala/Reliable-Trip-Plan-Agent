"""Version-agnostic product planning endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.dependencies import get_date_provider, get_planning_service
from backend.app.api.schemas.planning import (
    CompletedPlanningResponse,
    NeedsClarificationResponse,
    ProductPlanningRequest,
    ProductPlanningResponse,
    ProviderBlockedResponse,
    SafetyBlockedResponse,
)
from backend.app.policies.trip_dates import (
    MAX_TRIP_DAYS,
    DateProvider,
    TripDatePolicyError,
    create_trip_date_window,
)
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.app.services.planning import (
    PlanningFailedError,
    PlanningNeedsClarificationError,
    PlanningService,
)

router = APIRouter(prefix="/api", tags=["product-planning"])


@router.post("/planning", response_model=ProductPlanningResponse)
async def create_planning_result(
    body: ProductPlanningRequest,
    planning_service: Annotated[PlanningService, Depends(get_planning_service)],
) -> ProductPlanningResponse:
    """Generate a product itinerary through the active research planner."""

    try:
        result = await planning_service.plan(body)
    except TripDatePolicyError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=exc.as_detail(),
        ) from exc
    except PlanningNeedsClarificationError as exc:
        if exc.issues.get("safety_disposition") == "SAFETY_BLOCK":
            from backend.app.policies.preference_input import MESSAGES

            types = {i["issue_type"] for i in exc.issues["issues"]}
            kind = "safety_self_harm" if "safety_self_harm" in types else "safety_serious_harm"
            message, action = MESSAGES[kind]
            return SafetyBlockedResponse(
                requirements=exc.requirements, message=message, action=action
            )
        return NeedsClarificationResponse(requirements=exc.requirements, issues=exc.issues)
    except PlanningFailedError as exc:
        cause = exc.__cause__
        if isinstance(cause, RequirementBoundaryError) and cause.provider_content_filtered:
            return ProviderBlockedResponse(**cause.public_provider_action())
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "code": "planning_failed",
                "message": "The itinerary could not be generated. Please try again.",
            },
        ) from exc

    from backend.app.schemas.generation_diagnostics import public_minimum_coverage

    return CompletedPlanningResponse(
        requirements=result.requirements,
        itinerary=result.itinerary,
        minimum_daily_coverage=public_minimum_coverage(result.generation_diagnostics),
    )


@router.get("/planning/date-window")
async def get_planning_date_window(
    date_provider: Annotated[DateProvider, Depends(get_date_provider)],
) -> dict[str, str | int]:
    """Publish the same trusted calendar boundaries used by request validation."""
    window = create_trip_date_window(date_provider.today())
    return {
        "allowedStart": window.allowed_start.isoformat(),
        "allowedEnd": window.allowed_end.isoformat(),
        "maxTripDays": MAX_TRIP_DAYS,
    }
