"""Structured product/service migration; old prose extraction is intentionally replaced."""

import asyncio
from datetime import date
from decimal import Decimal

import pytest

from backend.app.services.planning import (
    DeveloperPlanningService,
    PlanningFailedError,
    PlanningNeedsClarificationError,
    PlanningService,
)
from backend.app.services.preference_interpretation import empty_preference_draft
from backend.tests.fakes import FixedDateProvider
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v0.fakes import (
    FakeStructuredLLMClient,
    make_itinerary,
    make_requirements,
)


def test_product_default_remains_v0_and_budget_is_total():
    request = make_request(
        requirements=make_requirements(), budget={"amount": "1234.50", "currency": "NZD"}
    )
    client = FakeStructuredLLMClient([make_itinerary()])
    result = asyncio.run(
        PlanningService(client, FixedDateProvider(date(2026, 9, 11))).plan(request)
    )
    assert result.system_version == "v0"
    assert result.requirements.budget.amount == Decimal("1234.50")
    assert result.requirements.budget.currency == "NZD"
    assert len(client.calls) == 1
    assert "1234.50" in client.calls[0].user_prompt


def test_product_service_hides_provider_failure():
    client = FakeStructuredLLMClient([RuntimeError("provider secret")])
    with pytest.raises(PlanningFailedError) as exc:
        asyncio.run(
            PlanningService(client, FixedDateProvider(date(2026, 9, 11))).plan(make_request())
        )
    assert "provider secret" not in str(exc.value)


def test_product_service_preserves_form_on_semantic_issue():
    request = make_request("Unclear preference")
    draft = empty_preference_draft().model_copy(update={"extraction_issues": ("ambiguous",)})
    client = FakeStructuredLLMClient([draft])
    with pytest.raises(PlanningNeedsClarificationError) as exc:
        asyncio.run(PlanningService(client, FixedDateProvider(date(2026, 9, 11))).plan(request))
    assert exc.value.requirements == request.trip_requirements()
    assert exc.value.issues["code"] == "extraction_ambiguity"
    assert len(client.calls) == 1


def test_developer_service_reuses_shared_v0_contract():
    request = make_request(requirements=make_requirements())
    client = FakeStructuredLLMClient([make_itinerary()])
    result = asyncio.run(
        DeveloperPlanningService(client).plan_v0(request, reference_date=date(2026, 9, 11))
    )
    assert result.requirements == request.trip_requirements()
    assert len(client.calls) == 1


def test_product_service_rejects_future_dates_before_model():
    request = make_request(start_date="2027-01-01", end_date="2027-01-03")
    client = FakeStructuredLLMClient([])
    with pytest.raises(ValueError, match="end_date must be on or before"):
        asyncio.run(PlanningService(client, FixedDateProvider(date(2026, 9, 11))).plan(request))
    assert not client.calls
