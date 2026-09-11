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
        result = await planning_service.plan(
            destination=body.destination,
            start_date=body.start_date,
            end_date=body.end_date,
            traveler_count=body.traveler_count,
            budget=body.budget,
            additional_preferences=body.additional_preferences,
            reference_date=body.reference_date,
        )
    except PlanningNeedsClarificationError as exc:
        return NeedsClarificationResponse(requirements=exc.requirements)
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
