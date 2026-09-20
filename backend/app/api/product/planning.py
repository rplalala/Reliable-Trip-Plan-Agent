"""Version-agnostic product planning endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.dependencies import get_planning_service
from backend.app.api.schemas.planning import (
    CompletedPlanningResponse,
    NeedsClarificationResponse,
    ProductPlanningRequest,
    ProductPlanningResponse,
)
from backend.app.policies.trip_dates import TripDatePolicyError
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
        return NeedsClarificationResponse(requirements=exc.requirements, issues=exc.issues)
    except PlanningFailedError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "code": "planning_failed",
                "message": "The itinerary could not be generated. Please try again.",
            },
        ) from exc

    return CompletedPlanningResponse(
        requirements=result.requirements,
        itinerary=result.itinerary,
    )
