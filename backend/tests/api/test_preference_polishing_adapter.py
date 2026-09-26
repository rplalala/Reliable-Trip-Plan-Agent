"""Offline checks for the bounded strict Foundry polishing transport."""

import asyncio

import pytest

from backend.app.llm.azure_foundry.polishing import (
    FoundryPolishingClient,
    PolishProviderInvalidResponse,
)


class FakeChat:
    def __init__(self, payload):
        self.payload = payload
        self.schema = None
        self.options = None

    def with_structured_output(self, schema, **options):
        self.schema = schema
        self.options = options
        return self

    async def ainvoke(self, messages):
        assert len(messages) == 2
        return self.schema.model_validate(self.payload)


def adapter(payload):
    client = object.__new__(FoundryPolishingClient)
    fake = FakeChat(payload)
    client._chat = fake
    return client, fake


def test_draft_uses_required_only_transport_and_enforces_domain_contract():
    client, fake = adapter({"status": "suggested", "suggested_text": "Visit a zoo.",
                            "explanation": "Clearer.", "questions": []})
    result = asyncio.run(client.draft("system", "input", 2000))
    assert result.suggested_text == "Visit a zoo."
    assert fake.options == {"method": "json_schema", "strict": True, "max_output_tokens": 2000}
    schema = fake.schema.model_json_schema()
    assert set(schema["required"]) == set(schema["properties"])
    assert "default" not in str(schema)
    assert "maxLength" not in str(schema)


def test_malformed_draft_is_rejected_after_transport_validation():
    client, _ = adapter({"status": "needs_input", "suggested_text": None,
                         "explanation": "Clarify.", "questions": []})
    with pytest.raises(PolishProviderInvalidResponse):
        asyncio.run(client.draft("system", "input", 2000))
