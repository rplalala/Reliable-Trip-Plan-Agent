"""HTTP contract tests for the version-agnostic product planner."""

import asyncio
from datetime import date

from httpx import ASGITransport, AsyncClient

from backend.app.api.dependencies import get_planning_service
from backend.app.main import app
from backend.app.services.planning import PlanningService
from backend.tests.fakes import FixedDateProvider, V0TestRuntime
from backend.tests.versions.v0.fakes import (
    FakeStructuredLLMClient,
    make_itinerary,
)


def post_product_planning(
    service: PlanningService,
    payload: dict[str, object],
) -> tuple[int, dict[str, object]]:
    async def send_request() -> tuple[int, dict[str, object]]:
        app.dependency_overrides[get_planning_service] = lambda: service
        try:
            transport = ASGITransport(app=app)
            async with AsyncClient(transport=transport, base_url="http://test") as client:
                response = await client.post("/api/planning", json=payload)
            return response.status_code, response.json()
        finally:
            app.dependency_overrides.pop(get_planning_service, None)

    return asyncio.run(send_request())


def make_product_payload() -> dict[str, object]:
    """Create a valid structured Product request payload."""

    return {
        "destination": "Kyoto",
        "start_date": "2026-09-12",
        "end_date": "2026-09-12",
        "traveler_count": 1,
        "budget": {"amount": "1800", "currency": "AUD"},
    }


def make_planning_service(client: FakeStructuredLLMClient) -> PlanningService:
    return PlanningService(V0TestRuntime(client, "v3"), FixedDateProvider(date(2026, 9, 11)))


def test_product_planning_returns_completed_contract_without_version() -> None:
    service = make_planning_service(FakeStructuredLLMClient([make_itinerary()]))

    status_code, body = post_product_planning(
        service,
        make_product_payload(),
    )

    assert status_code == 200
    assert body["status"] == "completed"
    assert body["requirements"]["destination"] == "Kyoto"
    assert body["itinerary"]["destination"] == "Kyoto"
    assert "system_version" not in body


def test_product_planning_missing_budget_is_input_failure():
    client = FakeStructuredLLMClient([])
    payload = make_product_payload()
    del payload["budget"]
    status_code, body = post_product_planning(make_planning_service(client), payload)
    assert status_code == 422
    assert not client.calls


def test_product_planning_rejects_version_field() -> None:
    service = make_planning_service(FakeStructuredLLMClient([]))
    payload = {**make_product_payload(), "version": "v0"}

    status_code, body = post_product_planning(service, payload)

    assert status_code == 422
    assert body["detail"][0]["type"] == "extra_forbidden"


def test_product_planning_rejects_raw_request_text() -> None:
    service = make_planning_service(FakeStructuredLLMClient([]))
    payload = {**make_product_payload(), "request_text": "Plan one day in Kyoto."}

    status_code, body = post_product_planning(service, payload)

    assert status_code == 422
    assert body["detail"][0]["type"] == "extra_forbidden"


def test_product_planning_requires_all_structured_fields() -> None:
    service = make_planning_service(FakeStructuredLLMClient([]))
    payload = make_product_payload()
    payload.pop("start_date")

    status_code, body = post_product_planning(service, payload)

    assert status_code == 422
    assert body["detail"][0]["loc"] == ["body", "start_date"]


def test_product_planning_rejects_invalid_date_range() -> None:
    service = make_planning_service(FakeStructuredLLMClient([]))
    payload = {
        **make_product_payload(),
        "start_date": "2026-09-14",
        "end_date": "2026-09-12",
    }

    status_code, body = post_product_planning(service, payload)

    assert status_code == 422
    assert body["detail"][0]["type"] == "value_error"


def test_product_planning_rejects_non_positive_traveler_count() -> None:
    service = make_planning_service(FakeStructuredLLMClient([]))
    payload = {**make_product_payload(), "traveler_count": 0}

    status_code, body = post_product_planning(service, payload)

    assert status_code == 422
    assert body["detail"][0]["type"] == "greater_than_equal"


def test_product_planning_rejects_incomplete_budget() -> None:
    service = make_planning_service(FakeStructuredLLMClient([]))
    payload = {**make_product_payload(), "budget": {"amount": "2000"}}

    status_code, body = post_product_planning(service, payload)

    assert status_code == 422
    assert body["detail"][0]["loc"] == ["body", "budget", "currency"]


def test_product_planning_rejects_invalid_currency() -> None:
    service = make_planning_service(FakeStructuredLLMClient([]))
    payload = {
        **make_product_payload(),
        "budget": {"amount": "2000", "currency": "aud"},
    }

    status_code, body = post_product_planning(service, payload)

    assert status_code == 422
    assert body["detail"][0]["type"] == "string_pattern_mismatch"


def test_product_planning_rejects_negative_budget() -> None:
    service = make_planning_service(FakeStructuredLLMClient([]))
    payload = {
        **make_product_payload(),
        "budget": {"amount": "-1", "currency": "AUD"},
    }

    status_code, body = post_product_planning(service, payload)

    assert status_code == 422
    assert body["detail"][0]["type"] == "greater_than_equal"


def test_product_planning_hides_provider_failure_details() -> None:
    service = make_planning_service(FakeStructuredLLMClient([RuntimeError("provider secret")]))

    status_code, body = post_product_planning(
        service,
        make_product_payload(),
    )

    assert status_code == 502
    assert body == {
        "detail": {
            "code": "planning_failed",
            "message": "The itinerary could not be generated. Please try again.",
        }
    }
    assert "provider secret" not in str(body)


def test_product_planning_rejects_client_controlled_reference_date() -> None:
    service = make_planning_service(FakeStructuredLLMClient([]))
    payload = {**make_product_payload(), "reference_date": "2027-01-01"}

    status_code, body = post_product_planning(service, payload)

    assert status_code == 422
    assert body["detail"][0]["type"] == "extra_forbidden"


def test_product_planning_rejects_direct_api_date_window_bypass() -> None:
    client = FakeStructuredLLMClient([])
    service = make_planning_service(client)
    payload = {
        **make_product_payload(),
        "start_date": "2027-01-01",
        "end_date": "2027-01-03",
    }

    status_code, body = post_product_planning(service, payload)

    assert status_code == 422
    assert body["detail"]["code"] == "trip_date_after_window"
    assert body["detail"]["allowed_start"] == "2026-09-11"
    assert body["detail"]["allowed_end"] == "2026-09-24"
    assert client.calls == []


def test_date_window_uses_backend_date_without_model_initialization():
    from backend.app.api.dependencies import get_date_provider

    async def check():
        app.dependency_overrides[get_date_provider] = lambda: FixedDateProvider(date(2026, 9, 20))
        try:
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as client:
                response = await client.get("/api/planning/date-window")
            assert response.status_code == 200
            assert response.json() == {
                "allowedStart": "2026-09-20",
                "allowedEnd": "2026-10-03",
                "maxTripDays": 10,
            }
        finally:
            app.dependency_overrides.pop(get_date_provider, None)

    asyncio.run(check())
