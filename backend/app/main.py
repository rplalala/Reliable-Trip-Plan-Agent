"""FastAPI application entry point."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

from backend.app.api.developer.planning import router as developer_planning_router
from backend.app.api.input_assistance import router as input_assistance_router
from backend.app.api.product.planning import router as product_planning_router


class HealthResponse(BaseModel):
    """Response returned by the health endpoint."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"]


app = FastAPI(
    title="Reliable Trip Plan Agent",
    description="Backend API for reliable itinerary generation.",
    version="0.1.0",
)

app.include_router(product_planning_router)
app.include_router(developer_planning_router)
app.include_router(input_assistance_router)


@app.get("/health", response_model=HealthResponse, tags=["system"])
def get_health() -> HealthResponse:
    """Report whether the API process is responsive."""

    return HealthResponse(status="ok")
