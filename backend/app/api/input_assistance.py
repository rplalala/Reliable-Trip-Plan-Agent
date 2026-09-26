"""Separate application endpoints for optional planning input assistance."""

from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from backend.app.integrations.geodb.client import (
    DestinationSuggestion,
    GeoDBClient,
    GeoDBInvalidResponse,
    GeoDBThrottled,
    GeoDBTimeout,
    GeoDBUnavailable,
)
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.services.destination_suggestions import (
    DestinationRateLimited,
    DestinationSuggestionService,
)

router = APIRouter(prefix="/api/input-assistance", tags=["input-assistance"])


class DestinationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source: str = "geodb"
    suggestions: list[DestinationSuggestion]


def assistance_error(
    status_code: int,
    code: str,
    message: str,
    *,
    retry_after: int | None = None,
):
    headers = {"Retry-After": str(retry_after)} if retry_after is not None else None
    content = {"error": {"code": code, "message": message}}
    return JSONResponse(
        status_code=status_code,
        content=content,
        headers=headers,
    )


@lru_cache
def get_destination_service() -> DestinationSuggestionService:
    config = load_runtime_config().input_assistance.destination
    return DestinationSuggestionService(GeoDBClient(), config)


@router.get("/destinations", response_model=DestinationResponse)
async def get_destinations(
    service: Annotated[DestinationSuggestionService, Depends(get_destination_service)],
    q: Annotated[str | None, Query()] = None,
):
    prefix = q.strip() if q is not None else ""
    if not service.accepts(prefix):
        return assistance_error(422, "invalid_prefix", "Enter 2 to 100 destination characters.")
    try:
        choices = await service.suggest(prefix)
    except DestinationRateLimited:
        return assistance_error(
            429,
            "destination_rate_limited",
            "Destination suggestions are temporarily limited.",
            retry_after=2,
        )
    except GeoDBThrottled:
        return assistance_error(
            429, "destination_provider_limited", "Destination suggestions are temporarily limited."
        )
    except GeoDBTimeout:
        return assistance_error(504, "destination_timeout", "Destination suggestions timed out.")
    except GeoDBInvalidResponse:
        return assistance_error(
            502, "destination_invalid_response", "Destination suggestions are unavailable."
        )
    except GeoDBUnavailable:
        return assistance_error(
            503, "destination_unavailable", "Destination suggestions are unavailable."
        )
    return DestinationResponse(suggestions=choices)
