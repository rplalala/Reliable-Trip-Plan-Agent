"""Locally exposed, version-aware developer planning endpoint."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import SerializeAsAny

from backend.app.api.dependencies import get_developer_planning_service
from backend.app.api.schemas.planning import DeveloperPlanningRequest
from backend.app.api.streaming import planning_stream
from backend.app.policies.trip_dates import TripDatePolicyError
from backend.app.schemas.interpreted_requirements import ClarificationRequired
from backend.app.schemas.planning import PlanningResult, SystemVersion
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.app.services.planning import DeveloperPlanningService
from backend.app.services.preference_interpretation import validate_planning_request
from backend.app.versions.v0.graph import V0StageError
from backend.app.versions.v1.graph import V1StageError

router = APIRouter(prefix="/api/dev", tags=["developer-planning"])


@router.post("/planning/stream")
async def stream_developer_planning_result(
    body: DeveloperPlanningRequest,
    planning_service: Annotated[DeveloperPlanningService, Depends(get_developer_planning_service)],
):
    """Each connection is one independently cancellable research run."""
    reference_date = planning_service.reference_date(body.reference_date)
    try:
        validate_planning_request(body.request, reference_date)
    except TripDatePolicyError as exc:
        raise HTTPException(status_code=422, detail=exc.as_detail()) from exc
    snapshot = body.model_copy(update={"reference_date": reference_date})
    return planning_stream(
        lambda: create_developer_planning_result(snapshot, planning_service),
        developer=True, version=body.version,
    )


@router.post("/planning", response_model=SerializeAsAny[PlanningResult])
async def create_developer_planning_result(
    body: DeveloperPlanningRequest,
    planning_service: Annotated[
        DeveloperPlanningService,
        Depends(get_developer_planning_service),
    ],
) -> PlanningResult:
    """Run an explicitly selected implemented research planner version."""

    try:
        return await planning_service.plan(
            SystemVersion(body.version),
            body.request,
            reference_date=body.reference_date,
        )
    except RequirementBoundaryError as exc:
        raise HTTPException(status_code=502, detail=exc.as_dict()) from exc
    except ClarificationRequired as exc:
        raise HTTPException(status_code=422, detail=exc.as_dict()) from exc
    except TripDatePolicyError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                "system_version": body.version,
                **exc.as_detail(),
            },
        ) from exc
    except (V0StageError, V1StageError) as exc:
        cause = exc.__cause__
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "code": f"{body.version}_stage_failed",
                "system_version": body.version,
                "stage": exc.stage,
                "message": str(cause) if cause is not None else str(exc),
            },
        ) from exc
    except TimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail={"code": "planning_timeout", "system_version": body.version},
        ) from exc
    except Exception as exc:
        # Local research output is detailed; configuration secrets are still not public output.
        raise HTTPException(
            status_code=502,
            detail={"code": "planning_execution_failed", "system_version": body.version},
        ) from exc
