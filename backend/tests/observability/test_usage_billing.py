"""Billing metadata at the existing opt-in SDK and HTTP boundaries."""

import asyncio

import httpx
import pytest

from backend.app.observability.usage import install_http_hooks, observe_sdk
from backend.app.observability.usage_capture import capture_attempt
from backend.evaluation.usage_report import summarize


def test_sdk_capture_retains_cache_and_reasoning_without_changing_totals():
    rows = []

    async def invoke():
        async def response(**kwargs):
            return {
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 20,
                    "input_tokens_details": {"cached_tokens": 40},
                    "output_tokens_details": {"reasoning_tokens": 10},
                }
            }

        await observe_sdk(response, usage_operation="test", usage_provider="fixture")
        return "ok"

    asyncio.run(capture_attempt(invoke, group_id="g", run_id="r", version="v0", sink=rows.append))
    call = rows[0]["model_calls"][0]
    assert call["cached_input_tokens"] == 40
    assert call["reasoning_tokens"] == 10
    assert call["total_tokens"] == 120


def test_capture_preserves_reported_cache_writes_and_numeric_usage_for_pricing():
    rows = []

    async def invoke():
        async def response(**kwargs):
            return {
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 20,
                    "input_tokens_details": {"cached_tokens": 40, "cache_write_tokens": 25},
                    "output_tokens_details": {"reasoning_tokens": 10},
                    "private_field": "SECRET",
                }
            }

        await observe_sdk(response, usage_operation="test", usage_provider="fixture")

    asyncio.run(capture_attempt(invoke, group_id="g", run_id="r", version="v1", sink=rows.append))
    call = rows[0]["model_calls"][0]
    assert call["cache_write_input_tokens"] == 25
    assert call["usage_details"]["input_tokens_details"] == {
        "cached_tokens": 40,
        "cache_write_tokens": 25,
    }
    assert call["total_tokens"] == 120
    assert "SECRET" not in str(rows)


def test_http_capture_retains_only_bounded_billing_parameters():
    rows = []

    async def invoke():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(lambda r: httpx.Response(200, json={}))
        ) as client:
            install_http_hooks(client)
            await client.post(
                "https://places.googleapis.com/v1/places:searchText",
                headers={"X-Goog-FieldMask": "places.id,places.displayName"},
                json={"textQuery": "PRIVATE", "key": "SECRET"},
            )
            await client.post(
                "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix",
                json={"origins": [1, 2], "destinations": [3], "travelMode": "WALK"},
            )
        return "ok"

    asyncio.run(capture_attempt(invoke, group_id="g", run_id="r", version="v1", sink=rows.append))
    search, matrix = rows[0]["provider_events"]
    assert search["billing_context"] == {
        "endpoint": "searchText",
        "field_mask": "places.displayName,places.id",
    }
    assert matrix["billing_context"] == {"travel_mode": "WALK"}
    assert matrix["element_count"] == 2
    assert "PRIVATE" not in str(rows) and "SECRET" not in str(rows)


def test_sdk_search_output_records_tool_units_separately_from_model_tokens():
    rows = []

    async def invoke():
        async def response(**kwargs):
            return {
                "usage": {"input_tokens": 10, "output_tokens": 2},
                "output": [{"type": "web_search_call"}, {"type": "message"}],
            }

        await observe_sdk(
            response,
            usage_operation="official_search",
            usage_provider="fixture",
            tools=[{"type": "web_search"}],
        )

    asyncio.run(capture_attempt(invoke, group_id="g", run_id="r", version="v1", sink=rows.append))
    assert rows[0]["provider_events"][0]["operation"] == "web_search_tool"
    assert rows[0]["provider_events"][0]["tool_calls"] == 1
    assert rows[0]["model_calls"][0]["total_tokens"] == 12


@pytest.mark.parametrize("http_sends", [0, 1])
def test_sdk_tool_billing_does_not_inflate_physical_http_metrics(http_sends):
    rows, dispatched = [], []

    async def invoke():
        def transport(request):
            dispatched.append(request)
            return httpx.Response(200, json={})

        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as client:
            install_http_hooks(client, "fixture", "model_http")

            async def response(**kwargs):
                if http_sends:
                    await client.post("https://example.test/model", json={})
                return {
                    "usage": {"input_tokens": 10, "output_tokens": 2},
                    "output": [{"type": "web_search_call"}],
                }

            await observe_sdk(
                response,
                usage_operation="official_search",
                usage_provider="fixture",
                tools=[{"type": "web_search"}],
            )

    asyncio.run(
        capture_attempt(
            invoke,
            group_id="g",
            run_id="r",
            version="v1",
            sink=rows.append,
            adapter_coverage="default_adapters",
        )
    )
    report = summarize(rows[0])
    assert len(dispatched) == http_sends
    assert report["metrics"]["http_sends"] == http_sends
    assert report["observed_http_sends"] == http_sends
    assert report["observed_tool_http_sends"] == 0
    assert report["failed_http_responses"] == 0
    assert report["incomplete_http_sends"] == 0
    assert report["metrics"]["total_tokens"] == 12
    assert rows[0]["provider_events"][-1]["tool_calls"] == 1


@pytest.mark.parametrize("tools", [None, object()])
def test_optional_sdk_tools_metadata_does_not_change_success(tools):
    rows = []

    async def invoke():
        async def response(**kwargs):
            return {"usage": {"input_tokens": 10, "output_tokens": 2}}

        return await observe_sdk(
            response, usage_operation="test", usage_provider="fixture", tools=tools
        )

    result = asyncio.run(
        capture_attempt(invoke, group_id="g", run_id="r", version="v0", sink=rows.append)
    )
    assert result["usage"]["output_tokens"] == 2
    assert rows[0]["outcome"] == "completed"


def test_http_backing_send_links_to_its_active_sdk_invocation():
    rows = []

    async def invoke():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(lambda r: httpx.Response(200, json={}))
        ) as client:
            install_http_hooks(client, "fixture", "model_http")

            async def response(**kwargs):
                await client.post("https://example.test/model", json={})
                return {"usage": {"input_tokens": 10, "output_tokens": 2}}

            await observe_sdk(response, usage_operation="chat", usage_provider="fixture")

    asyncio.run(capture_attempt(invoke, group_id="g", run_id="r", version="v0", sink=rows.append))
    assert rows[0]["provider_events"][0]["model_event_id"] == rows[0]["model_calls"][0]["event_id"]
