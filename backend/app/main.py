"""FastAPI application entry point."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Response returned by the health endpoint."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"]


app = FastAPI(
    title="Reliable Trip Plan Agent",
    description="Backend API for reliable itinerary generation.",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def get_health() -> HealthResponse:
    """Report whether the API process is responsive."""

    return HealthResponse(status="ok")
