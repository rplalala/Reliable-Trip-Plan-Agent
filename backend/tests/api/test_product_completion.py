"""Product JSON and SSE retain current V3 completion semantics through presentation."""

import asyncio
import json
from datetime import date

import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.api.dependencies import get_planning_service
from backend.app.main import app
from backend.app.schemas.generation_diagnostics import GenerationDiagnostics
from backend.app.schemas.planning import PlanningResult
from backend.app.services.planning import PlanningService
from backend.tests.api.test_product_planning import make_product_payload
from backend.tests.fakes import FixedDateProvider
from backend.tests.versions.v0.fakes import make_itinerary


@pytest.mark.parametrize("stream", [False, True])
@pytest.mark.parametrize("completion", ["incomplete", "complete", "unassessed"])
def test_product_completion_survives_public_response(stream, completion):
    calls = []
    reasons = ["required_visit_obligation_unmet"] if completion == "incomplete" else []

    class Runtime:
        async def run(self, version, request, **kwargs):
            calls.append(version)
            return PlanningResult(
                system_version=version,
                requirements=request.trip_requirements(),
                itinerary=make_itinerary(),
                generation_diagnostics=GenerationDiagnostics(
                    policy_completion=completion,
                    policy_issues=tuple({"reason": r, "internal": "PRIVATE"} for r in reasons),
                    days=(),
                    days_meeting_default_target=0,
                    days_below_target=0,
                    days_above_target=0,
                    days_unassessable=0,
                    empty_days=0,
                    days_with_zero_main_pois=0,
                    scheduled_unique_supply=None,
                    unused_supply=None,
                    cross_day_repeated_visits=0,
                ),
            )

    class Introductions:
        async def generate(self, *args):
            return {}

    service = PlanningService(
        Runtime(), FixedDateProvider(date(2026, 9, 11)), introductions=Introductions()
    )

    async def send():
        app.dependency_overrides[get_planning_service] = lambda: service
        try:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
                return await c.post(
                    "/api/planning" + ("/stream" if stream else ""), json=make_product_payload()
                )
        finally:
            app.dependency_overrides.pop(get_planning_service, None)

    response = asyncio.run(send())
    assert response.status_code == 200
    if stream:
        events = [
            json.loads(line[6:]) for line in response.text.splitlines() if line.startswith("data: ")
        ]
        body = next(e["result"] for e in events if e["type"] == "result")
    else:
        body = response.json()
    assert calls == ["v3"]
    assert body["status"] == "completed"  # Request succeeded even if obligations remain unmet.
    assert body["policy_completion"] == completion
    assert body["policy_reasons"] == reasons
    assert body["itinerary"]["days"]
    assert "PRIVATE" not in response.text and "generation_diagnostics" not in body
