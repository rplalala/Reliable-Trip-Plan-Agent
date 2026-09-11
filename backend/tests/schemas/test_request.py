"""Tests for travel request and requirement schemas."""

from datetime import date

import pytest
from pydantic import ValidationError

from backend.app.schemas.request import Money, TravelRequest, TravelRequirements


def test_travel_request_strips_surrounding_whitespace() -> None:
    request = TravelRequest(request_text="  Plan a trip to Kyoto.  ")

    assert request.request_text == "Plan a trip to Kyoto."
    assert request.request_id is None


def test_travel_request_rejects_blank_text() -> None:
    with pytest.raises(ValidationError):
        TravelRequest(request_text="   ")


def test_requirements_accept_partial_information() -> None:
    requirements = TravelRequirements(
        destination="Kyoto",
        traveler_count=2,
        budget=Money(amount="1500.00", currency="AUD"),
        unresolved_fields=["start_date", "end_date"],
    )

    assert requirements.destination == "Kyoto"
    assert requirements.start_date is None
    assert requirements.budget is not None
    assert requirements.budget.currency == "AUD"


def test_requirements_reject_reversed_date_range() -> None:
    with pytest.raises(ValidationError, match="end_date must be on or after start_date"):
        TravelRequirements(
            destination="Kyoto",
            start_date=date(2026, 10, 5),
            end_date=date(2026, 10, 1),
        )


def test_shared_request_schema_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        TravelRequest(request_text="Plan a trip.", provider_payload={})
