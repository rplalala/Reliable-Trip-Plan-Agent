"""Repeated operations through the real adapter with offline provider HTTP responses."""

import asyncio
import json

import httpx2
import pytest

from backend.app.llm.azure_foundry.polishing import (
    FoundryPolishingClient,
    PolishProviderUnavailable,
)
from backend.app.schemas.input_assistance import PolishRequest
from backend.app.services.preference_polishing import PreferencePolishingService
from backend.app.versions.v0.config import V0Settings


@pytest.mark.parametrize("first_fails", [False, True])
def test_two_polish_operations_in_one_loop_keep_independent_connections(monkeypatch, first_fails):
    sends = []

    async def respond(transport, request):
        body = json.loads(request.content)
        sends.append(body)
        if first_fails and len(sends) == 1:
            return httpx2.Response(503, request=request, json={"error": {"message": "Unavailable"}})
        output = {"status": "suggested", "suggested_text": "I like climbing mountains.",
                  "explanation": "Corrected grammar.", "questions": []}
        return httpx2.Response(200, request=request, json={
            "id": "resp_offline", "object": "response", "created_at": 0,
            "model": "offline", "status": "completed",
            "output": [{"id": "msg_offline", "type": "message", "role": "assistant",
                        "status": "completed", "content": [{"type": "output_text",
                        "text": json.dumps(output), "annotations": []}]}],
        })

    monkeypatch.setattr(httpx2.AsyncHTTPTransport, "handle_async_request", respond)
    clients = []

    def factory():
        client = FoundryPolishingClient(V0Settings(
            azure_openai_endpoint="https://polish-lifecycle.invalid/v1/",
            azure_openai_deployment="offline", azure_openai_api_key="offline-placeholder",
        ))
        clients.append(client)
        return client

    async def run():
        service = PreferencePolishingService(factory)
        request = PolishRequest(original_text="I like climbing mountain.", client_revision="one")
        for operation in range(2):
            if first_fails and operation == 0:
                with pytest.raises(PolishProviderUnavailable):
                    await service.polish(request)
            else:
                result = await service.polish(request)
                assert result.status == "suggested"
                assert result.suggested_text == "I like climbing mountains."
            assert clients[-1]._chat.root_async_client.is_closed()
            assert clients[-1]._chat.root_client.is_closed()

    asyncio.run(run())
    assert len(sends) == 2
    expected_budgets = [2000, 2000]
    assert [body["max_output_tokens"] for body in sends] == expected_budgets
