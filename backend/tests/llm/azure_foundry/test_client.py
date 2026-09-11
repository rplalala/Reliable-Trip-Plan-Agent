"""Tests for the Microsoft Foundry structured-output client."""

import asyncio
from typing import Any

import pytest
from pydantic import BaseModel

from backend.app.llm.azure_foundry import client as client_module
from backend.app.llm.azure_foundry.client import AzureFoundryStructuredLLMClient
from backend.app.llm.azure_foundry.dto import (
    FoundryActivityDTO,
    FoundryDateTimeDTO,
    FoundryItineraryDayDTO,
    FoundryItineraryDTO,
    FoundryTravelRequirementsDTO,
)
from backend.app.llm.client import StructuredOutputError
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import TravelRequirements


class FakeStructuredModel:
    def __init__(self, response: object) -> None:
        self.response = response
        self.messages: list[object] = []
        self.invocation_count = 0

    async def ainvoke(self, messages: list[object]) -> object:
        self.messages = messages
        self.invocation_count += 1
        return self.response


class FakeChatOpenAI:
    response: object
    init_kwargs: dict[str, Any] = {}
    schema: object = None
    structured_kwargs: dict[str, Any] = {}
    structured_model: FakeStructuredModel
    structured_output_count = 0

    def __init__(self, **kwargs: Any) -> None:
        type(self).init_kwargs = kwargs

    def with_structured_output(
        self,
        schema: object,
        **kwargs: Any,
    ) -> FakeStructuredModel:
        type(self).schema = schema
        type(self).structured_kwargs = kwargs
        type(self).structured_output_count += 1
        type(self).structured_model = FakeStructuredModel(type(self).response)
        return type(self).structured_model


def make_activity(
    *,
    end_time: FoundryDateTimeDTO | None = None,
) -> FoundryActivityDTO:
    return FoundryActivityDTO(
        activity_id="activity-1",
        title="Visit Fushimi Inari Shrine",
        place_name="Fushimi Inari Taisha",
        location="Kyoto, Japan",
        start_time=FoundryDateTimeDTO(
            date="2026-10-01",
            time="09:00:00",
            utc_offset="+09:00",
        ),
        end_time=end_time
        or FoundryDateTimeDTO(
            date="2026-10-01",
            time="11:00:00",
            utc_offset="+09:00",
        ),
        estimated_cost=None,
        notes=None,
    )


def make_client(monkeypatch: pytest.MonkeyPatch) -> AzureFoundryStructuredLLMClient:
    FakeChatOpenAI.structured_output_count = 0
    monkeypatch.setattr(client_module, "ChatOpenAI", FakeChatOpenAI)
    return AzureFoundryStructuredLLMClient(
        endpoint="https://example.services.ai.azure.com/openai/v1",
        deployment="configured-deployment",
        api_key="test-key",
    )


def generate(client: AzureFoundryStructuredLLMClient, response_schema: type[BaseModel]):
    return asyncio.run(
        client.generate_structured(
            system_prompt="System prompt",
            user_prompt="User prompt",
            response_schema=response_schema,
        )
    )


def test_client_uses_requirements_dto_and_returns_domain_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    FakeChatOpenAI.response = FoundryTravelRequirementsDTO(
        destination="Kyoto",
        start_date="2026-10-01",
        end_date="2026-10-03",
        traveler_count=1,
        budget=None,
        required_activities=[],
        excluded_activities=[],
        preferences=[],
        unresolved_fields=[],
    )
    client = make_client(monkeypatch)

    result = generate(client, TravelRequirements)

    assert isinstance(result, TravelRequirements)
    assert FakeChatOpenAI.schema is FoundryTravelRequirementsDTO
    assert FakeChatOpenAI.init_kwargs == {
        "model": "configured-deployment",
        "base_url": "https://example.services.ai.azure.com/openai/v1",
        "api_key": "test-key",
        "use_responses_api": True,
        "max_retries": 0,
    }
    assert FakeChatOpenAI.structured_kwargs == {
        "method": "json_schema",
        "strict": True,
    }
    assert FakeChatOpenAI.structured_model.invocation_count == 1
    assert len(FakeChatOpenAI.structured_model.messages) == 2


def test_client_uses_itinerary_dto_and_returns_domain_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    FakeChatOpenAI.response = FoundryItineraryDTO(
        destination="Kyoto",
        start_date="2026-10-01",
        end_date="2026-10-01",
        days=[
            FoundryItineraryDayDTO(
                date="2026-10-01",
                activities=[make_activity()],
            )
        ],
    )
    client = make_client(monkeypatch)

    result = generate(client, Itinerary)

    assert isinstance(result, Itinerary)
    assert FakeChatOpenAI.schema is FoundryItineraryDTO
    assert result.days[0].activities[0].end_time.isoformat() == (
        "2026-10-01T11:00:00+09:00"
    )
    assert FakeChatOpenAI.structured_model.invocation_count == 1


def test_client_fails_without_retry_after_mapping_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    invalid_activity = make_activity(
        end_time=FoundryDateTimeDTO(
            date="2026-10-01",
            time="11:00",
            utc_offset="+09:00",
        )
    )
    FakeChatOpenAI.response = FoundryItineraryDTO(
        destination="Kyoto",
        start_date="2026-10-01",
        end_date="2026-10-01",
        days=[FoundryItineraryDayDTO(date="2026-10-01", activities=[invalid_activity])],
    )
    client = make_client(monkeypatch)

    with pytest.raises(StructuredOutputError, match="must use exactly HH:MM:SS"):
        generate(client, Itinerary)

    assert FakeChatOpenAI.structured_model.invocation_count == 1


def test_client_rejects_unregistered_domain_schema_before_invocation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class UnsupportedDomainModel(BaseModel):
        value: str

    FakeChatOpenAI.response = {"value": "unused"}
    client = make_client(monkeypatch)

    with pytest.raises(StructuredOutputError, match="no transport DTO"):
        generate(client, UnsupportedDomainModel)

    assert FakeChatOpenAI.structured_output_count == 0
