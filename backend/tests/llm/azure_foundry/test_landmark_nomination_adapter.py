"""Actual SDK nomination transport with bounded fake HTTP responses."""

import asyncio
import json

import httpx2 as httpx
import pytest

from backend.app.llm.azure_foundry.client import AzureFoundryStructuredLLMClient
from backend.app.runtime.config_models import LandmarkNominationConfig
from backend.app.services.landmark_nomination import LandmarkNominationService
from backend.tests.llm.azure_foundry.test_requirement_acceptance_harness import response


@pytest.mark.parametrize("mode", ["success", "malformed", "provider_error"])
def test_nomination_adapter_wire_usage_and_cleanup(mode):
    sends = []

    def handler(request):
        sends.append(json.loads(request.content))
        if mode == "provider_error":
            return httpx.Response(500, json={"error": {"message": "fixture failure"}})
        names = ["Old Tower"] if mode == "success" else ["Tower"] * 13
        return httpx.Response(200, json=response(json.dumps({"names": names}), 1))

    sync = httpx.Client(transport=httpx.MockTransport(handler))
    asynchronous = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AzureFoundryStructuredLLMClient(
        endpoint="https://fixture.invalid/openai/v1",
        deployment="fixture-model",
        api_key="fixture-key",
        http_client=sync,
        http_async_client=asynchronous,
    )
    service = LandmarkNominationService(client, LandmarkNominationConfig(), 256)

    async def run():
        try:
            return await service.nominate({"name": "Example City"})
        finally:
            await client.aclose()

    result = asyncio.run(run())
    assert len(sends) == 1
    assert sends[0]["max_output_tokens"] == 2000
    assert sends[0]["text"]["format"]["strict"] is True
    assert sync.is_closed and asynchronous.is_closed
    assert result == (("Old Tower",) if mode == "success" else ())
    if mode == "success":
        assert next(iter(service.snapshot()["usage"].values()))["total_tokens"] == 40
