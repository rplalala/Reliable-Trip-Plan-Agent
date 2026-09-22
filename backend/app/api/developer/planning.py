"""Locally exposed, version-aware developer planning endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.api.dependencies import get_developer_planning_service
from backend.app.api.schemas.planning import DeveloperPlanningRequest
from backend.app.policies.trip_dates import TripDatePolicyError
from backend.app.schemas.interpreted_requirements import ClarificationRequired
from backend.app.schemas.planning import PlanningResult
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.app.services.planning import DeveloperPlanningService
from backend.app.versions.v0.graph import V0StageError

router = APIRouter(prefix="/api/dev", tags=["developer-planning"])


@router.post("/planning", response_model=PlanningResult)
async def create_developer_planning_result(
    body: DeveloperPlanningRequest,
    planning_service: Annotated[
        DeveloperPlanningService,
        Depends(get_developer_planning_service),
    ],
) -> PlanningResult:
    """Run an explicitly selected implemented research planner version."""

    try:
        return await planning_service.plan_v0(
            body.request,
            reference_date=body.reference_date,
        )
    except (ClarificationRequired, RequirementBoundaryError) as exc:
        raise HTTPException(status_code=422, detail=exc.as_dict()) from exc
    except TripDatePolicyError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                "system_version": body.version,
                **exc.as_detail(),
            },
        ) from exc
    except V0StageError as exc:
        cause = exc.__cause__
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "code": "v0_stage_failed",
                "system_version": body.version,
                "stage": exc.stage,
                "message": str(cause) if cause is not None else str(exc),
            },
        ) from exc
