"""Tests for product and developer planning service boundaries."""

import asyncio
from datetime import date

import pytest

from backend.app.schemas.planning import SystemVersion
from backend.app.schemas.request import Money, TravelRequest, TravelRequirements
from backend.app.services.planning import (
    DeveloperPlanningService,
    PlanningFailedError,
    PlanningNeedsClarificationError,
    PlanningService,
    build_canonical_request_text,
)
from backend.tests.versions.v0.fakes import (
    FakeStructuredLLMClient,
    make_itinerary,
    make_requirements,
)


def test_canonical_request_contains_only_required_values() -> None:
    request_text = build_canonical_request_text(
        destination="Beijing",
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 3),
        traveler_count=2,
        budget=None,
        additional_preferences=None,
    )

    assert request_text == (
        "Plan a trip to Beijing from 2026-10-01 to 2026-10-03 for 2 travelers."
    )


def test_canonical_request_preserves_explicit_budget_without_conversion() -> None:
    request_text = build_canonical_request_text(
        destination="Wellington",
        start_date=date(2026, 11, 4),
        end_date=date(2026, 11, 4),
        traveler_count=1,
        budget=Money(amount="1234.50", currency="NZD"),
        additional_preferences=None,
    )

    assert request_text == (
        "Plan a trip to Wellington from 2026-11-04 to 2026-11-04 for 1 traveler "
        "with a total budget of 1234.50 NZD."
    )


def test_canonical_request_preserves_preference_text_exactly() -> None:
    preference = "Keep Museum names AS entered; no nightlife, please!"

    request_text = build_canonical_request_text(
        destination="Berlin",
        start_date=date(2027, 1, 8),
        end_date=date(2027, 1, 10),
        traveler_count=3,
        budget=None,
        additional_preferences=preference,
    )

    assert request_text == (
        "Plan a trip to Berlin from 2027-01-08 to 2027-01-10 for 3 travelers. "
        "Additional preferences: Keep Museum names AS entered; no nightlife, please!"
    )


def test_canonical_request_is_deterministic_for_the_same_validated_values() -> None:
    values = {
        "destination": "Beijing",
        "start_date": date(2026, 10, 1),
        "end_date": date(2026, 10, 3),
        "traveler_count": 2,
        "budget": Money(amount="2000", currency="AUD"),
        "additional_preferences": "Local food and quiet mornings.",
    }

    first = build_canonical_request_text(**values)
    second = build_canonical_request_text(**values)

    assert first == second
    assert first == (
        "Plan a trip to Beijing from 2026-10-01 to 2026-10-03 for 2 travelers "
        "with a total budget of 2000 AUD. Additional preferences: Local food and quiet mornings."
    )


def test_product_service_returns_programmatic_v0_result_from_canonical_request() -> None:
    client = FakeStructuredLLMClient([make_requirements(), make_itinerary()])
    service = PlanningService(client)

    result = asyncio.run(
        service.plan(
            destination="Kyoto",
            start_date=date(2026, 10, 1),
            end_date=date(2026, 10, 1),
            traveler_count=1,
            budget=None,
            additional_preferences=None,
            reference_date=date(2026, 9, 11),
        )
    )

    assert result.system_version is SystemVersion.V0
    assert result.itinerary.destination == "Kyoto"
    assert len(client.calls) == 2
    assert (
        "Plan a trip to Kyoto from 2026-10-01 to 2026-10-01 for 1 traveler."
        in client.calls[0].user_prompt
    )


def test_product_service_maps_missing_requirements_without_generation() -> None:
    requirements = TravelRequirements(destination="Kyoto")
    client = FakeStructuredLLMClient([requirements])
    service = PlanningService(client)

    with pytest.raises(PlanningNeedsClarificationError) as captured:
        asyncio.run(
            service.plan(
                destination="Kyoto",
                start_date=date(2026, 10, 1),
                end_date=date(2026, 10, 3),
                traveler_count=1,
                budget=None,
                additional_preferences=None,
                reference_date=date(2026, 9, 11),
            )
        )

    assert captured.value.requirements.unresolved_fields == ["start_date", "end_date"]
    assert len(client.calls) == 1


def test_product_service_hides_v0_stage_failure() -> None:
    client = FakeStructuredLLMClient([RuntimeError("provider secret")])
    service = PlanningService(client)

    with pytest.raises(PlanningFailedError, match="active planner failed") as captured:
        asyncio.run(
            service.plan(
                destination="Kyoto",
                start_date=date(2026, 10, 1),
                end_date=date(2026, 10, 1),
                traveler_count=1,
                budget=None,
                additional_preferences=None,
                reference_date=date(2026, 9, 11),
            )
        )

    assert "provider secret" not in str(captured.value)


def test_developer_service_preserves_v0_programmatic_result() -> None:
    client = FakeStructuredLLMClient([make_requirements(), make_itinerary()])
    service = DeveloperPlanningService(client)

    result = asyncio.run(
        service.plan_v0(
            TravelRequest(request_text="Plan one day in Kyoto."),
            reference_date=date(2026, 9, 11),
        )
    )

    assert result.system_version is SystemVersion.V0
    assert len(client.calls) == 2
