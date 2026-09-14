"""HTTP contract tests for the local developer planner."""

import asyncio
from datetime import date

from httpx import ASGITransport, AsyncClient

from backend.app.api.dependencies import get_developer_planning_service
from backend.app.main import app
from backend.app.schemas.request import TravelRequirements
from backend.app.services.planning import DeveloperPlanningService
from backend.tests.versions.v0.fakes import (
    FakeStructuredLLMClient,
    make_itinerary,
    make_requirements,
)


def post_developer_planning(
    service: DeveloperPlanningService,
    payload: dict[str, object],
) -> tuple[int, dict[str, object]]:
    async def send_request() -> tuple[int, dict[str, object]]:
        app.dependency_overrides[get_developer_planning_service] = lambda: service
        try:
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.post("/api/dev/planning", json=payload)
            return response.status_code, response.json()
        finally:
            app.dependency_overrides.pop(get_developer_planning_service, None)

    return asyncio.run(send_request())


def test_developer_planning_returns_raw_v0_result() -> None:
    service = DeveloperPlanningService(
        FakeStructuredLLMClient([make_requirements(), make_itinerary()])
    )

    status_code, body = post_developer_planning(
        service,
        {
            "version": "v0",
            "request_text": "Plan one day in Kyoto.",
            "reference_date": "2026-09-11",
        },
    )

    assert status_code == 200
    assert body["system_version"] == "v0"
    assert set(body) == {"system_version", "requirements", "itinerary"}


def test_developer_planning_rejects_unimplemented_version() -> None:
    service = DeveloperPlanningService(FakeStructuredLLMClient([]))

    status_code, body = post_developer_planning(
        service,
        {"version": "v1", "request_text": "Plan one day in Kyoto."},
    )

    assert status_code == 422
    assert body["detail"][0]["type"] == "literal_error"


def test_developer_planning_returns_missing_requirements_debug_details() -> None:
    service = DeveloperPlanningService(
        FakeStructuredLLMClient([TravelRequirements(destination="Kyoto")])
    )

    status_code, body = post_developer_planning(
        service,
        {"version": "v0", "request_text": "Plan a trip to Kyoto."},
    )

    assert status_code == 422
    assert body["detail"]["code"] == "missing_required_fields"
    assert body["detail"]["system_version"] == "v0"
    assert body["detail"]["requirements"]["unresolved_fields"] == [
        "start_date",
        "end_date",
    ]


def test_developer_planning_exposes_v0_stage_for_debugging() -> None:
    service = DeveloperPlanningService(
        FakeStructuredLLMClient([RuntimeError("provider unavailable")])
    )

    status_code, body = post_developer_planning(
        service,
        {"version": "v0", "request_text": "Plan one day in Kyoto."},
    )

    assert status_code == 502
    assert body == {
        "detail": {
            "code": "v0_stage_failed",
            "system_version": "v0",
            "stage": "extract_requirements",
            "message": "provider unavailable",
        }
    }


def test_developer_planning_uses_trusted_reference_date_for_window_validation() -> None:
    requirements = make_requirements().model_copy(
        update={
            "start_date": date(2026, 9, 21),
            "end_date": date(2026, 9, 21),
        }
    )
    client = FakeStructuredLLMClient([requirements])
    service = DeveloperPlanningService(client)

    status_code, body = post_developer_planning(
        service,
        {
            "version": "v0",
            "request_text": "Plan one day in Kyoto.",
            "reference_date": "2026-09-11",
        },
    )

    assert status_code == 422
    assert body["detail"]["system_version"] == "v0"
    assert body["detail"]["code"] == "trip_date_after_window"
    assert len(client.calls) == 1
