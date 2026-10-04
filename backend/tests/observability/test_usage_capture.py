"""Offline capture at real callback/HTTP seams; no model or network service."""

import asyncio
import hashlib
import json
from types import SimpleNamespace

import httpx
import pytest
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage

from backend.app.observability.usage import (
    UsageLedger,
    current_usage,
    install_http_hooks,
    observe_sdk,
    tokens,
    usage_stage,
)
from backend.app.observability.usage_capture import ModelUsageCallback, capture_attempt
from backend.app.runtime.cache import RequestCache
from backend.evaluation.usage_report import compare_usage, summarize


def capture(invoke, rows, **kwargs):
    return capture_attempt(
        invoke,
        group_id="g",
        run_id=kwargs.pop("run_id", "r"),
        version=kwargs.pop("version", "v0"),
        sink=rows.append,
        serialize=lambda value: json.dumps(value).encode(),
        **kwargs,
    )


def test_real_langchain_callback_usage_and_cleanup_scope():
    now, rows = [0.0], []
    ledger = UsageLedger(clock=lambda: now[0])
    model = FakeMessagesListChatModel(
        responses=[
            AIMessage(
                content="ok",
                usage_metadata={"input_tokens": 10, "output_tokens": 3, "total_tokens": 13},
            )
        ]
    )

    async def invoke():
        with usage_stage("primary_generation"):
            response = await model.ainvoke("private prompt")
            now[0] = 2
            return response.content

    async def cleanup():
        now[0] = 7

    assert (
        asyncio.run(
            capture(
                invoke, rows, cleanup=cleanup, ledger=ledger, adapter_coverage="default_adapters"
            )
        )
        == "ok"
    )
    assert rows[0]["timing"]["elapsed_seconds"] == 7
    assert rows[0]["model_calls"][0]["total_tokens"] == 13
    assert rows[0]["result_sha256"] == hashlib.sha256(b'"ok"').hexdigest()
    assert "private prompt" not in json.dumps(rows)
    assert current_usage.get() is None


def test_http_attempts_errors_elements_and_cache_are_distinct():
    rows = []
    seen = []

    def respond(request):
        seen.append(request)
        return httpx.Response(500 if len(seen) == 1 else 200, json={"ok": True})

    async def invoke():
        with usage_stage("acquisition"):
            async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
                install_http_hooks(client)
                install_http_hooks(client)
                for _ in range(2):
                    await client.post(
                        "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix",
                        headers={"Secret": "credential"},
                        json={"origins": [1, 2], "destinations": [3, 4, 5]},
                    )
            cache = RequestCache()

            async def factory():
                return 9

            await cache.get_or_create(("place_details", "private-id"), factory)
            await cache.get_or_create(("place_details", "private-id"), factory)
            assert cache.lookup(("place_details", "private-id")) == (9, True)
            return {"ok": True}

    asyncio.run(capture(invoke, rows, adapter_coverage="default_adapters"))
    events = rows[0]["provider_events"]
    assert len(events) == 2
    assert [e["outcome"] for e in events] == ["failed", "completed"]
    assert all(e["element_count"] == 6 for e in events)
    assert len(rows[0]["cache_events"]) == 2
    summary = summarize(rows[0])
    assert summary["metrics"]["cache_hits"] == 1
    assert summary["cache_lookup_hits"] == 1
    assert "credential" not in json.dumps(rows) and "private-id" not in json.dumps(rows)


def test_sdk_calls_missing_usage_and_repair_subset():
    rows = []
    calls = [
        SimpleNamespace(usage={"prompt_tokens": 4, "total_tokens": 4}),
        SimpleNamespace(usage=None),
    ]

    async def sdk(**kwargs):
        return calls.pop(0)

    async def invoke():
        with usage_stage("repair", 2):
            await observe_sdk(sdk, usage_operation="embedding", usage_provider="openai", model="m")
            await observe_sdk(sdk, usage_operation="official_reasoning", usage_provider="azure")
        return 1

    asyncio.run(capture(invoke, rows, adapter_coverage="default_adapters"))
    data = rows[0]
    assert len(data["model_calls"]) == 2
    assert len(data["repair_summary"]["model_event_ids"]) == 2
    assert all(r["round_id"] == 2 and r["repair"] for r in data["model_calls"])
    report = summarize(data)
    assert report["metrics"]["total_tokens"] is None
    assert report["observed_token_subtotal"] == 4


@pytest.mark.parametrize("error", [RuntimeError("private error"), asyncio.CancelledError()])
def test_primary_exception_and_cleanup_preserved(error):
    rows, cleanup = [], []

    async def invoke():
        raise error

    async def close():
        cleanup.append(True)
        raise ValueError("cleanup error")

    with pytest.raises(type(error)) as caught:
        asyncio.run(capture(invoke, rows, cleanup=close))
    assert caught.value is error
    assert cleanup and len(rows) == 1
    assert rows[0]["result_sha256"] is None
    assert "private error" not in json.dumps(rows)
    assert current_usage.get() is None


def test_concurrent_attempt_context_isolation():
    a, b = [], []

    async def work(amount):
        async def sdk(**kwargs):
            await asyncio.sleep(0)
            return {"usage": {"input_tokens": amount, "output_tokens": 1}}

        await observe_sdk(sdk, usage_operation="test", usage_provider="fixture")
        return amount

    async def run():
        return await asyncio.gather(
            capture(lambda: work(3), a, run_id="a"), capture(lambda: work(8), b, run_id="b")
        )

    assert asyncio.run(run()) == [3, 8]
    assert a[0]["model_calls"][0]["total_tokens"] == 4
    assert b[0]["model_calls"][0]["total_tokens"] == 9


def test_callback_duplicate_end_is_not_extra_tokens():
    ledger = UsageLedger()
    callback = ModelUsageCallback(ledger)
    callback.on_chat_model_start({}, [], run_id="call")
    response = SimpleNamespace(
        generations=[
            [
                SimpleNamespace(
                    message=SimpleNamespace(
                        usage_metadata={"input_tokens": 2, "output_tokens": 1, "total_tokens": 3}
                    )
                )
            ]
        ]
    )
    callback.on_llm_end(response, run_id="call")
    callback.on_llm_end(response, run_id="call")
    assert len(ledger.models) == 1
    assert ledger.models["call"]["total_tokens"] == 3
    assert tokens({"input_tokens": 0, "output_tokens": 0})["total_tokens"] == 0
    assert tokens({"input_tokens": True})["input_tokens"] is None


def test_usage_comparisons_missing_zero_and_scope():
    rows = []

    async def invoke():
        return 1

    for version in ("v0", "v1", "v2", "v3"):
        asyncio.run(
            capture(
                invoke, rows, version=version, run_id=version, adapter_coverage="default_adapters"
            )
        )
    rows[2]["coverage"]["adapter_coverage"] = "unverified"
    rows[3]["timing"]["scope"] = "different"
    report = compare_usage(rows)
    pairs = report["groups"][0]["comparisons"]
    assert any(p["reason"] == "zero_baseline" for p in pairs)
    assert any(p["reason"] == "missing_measurement" for p in pairs)
    assert any(p["reason"] == "scope_mismatch" for p in pairs)
    assert report["quality_score_contribution"] is None
    with pytest.raises(ValueError):
        compare_usage([rows[0], rows[0]])
    with pytest.raises(ValueError):
        compare_usage([rows[0]])
    unavailable = dict(rows[0], collection_status="unavailable")
    assert summarize(unavailable)["metrics"]["total_tokens"] is None


def test_failed_http_send_is_counted_but_no_response_claimed():
    rows = []

    def transport(request):
        raise httpx.ConnectError("not connected")

    async def invoke():
        async with httpx.AsyncClient(transport=httpx.MockTransport(transport)) as client:
            install_http_hooks(client)
            await client.get("https://example.invalid")

    with pytest.raises(httpx.ConnectError):
        asyncio.run(capture(invoke, rows))
    assert len(rows[0]["provider_events"]) == 1
    assert rows[0]["provider_events"][0]["outcome"] == "incomplete"


def test_sink_failure_does_not_replace_planner_result():
    ledger = UsageLedger()

    async def invoke():
        return 42

    def sink(data):
        raise OSError("disk unavailable")

    result = asyncio.run(
        capture_attempt(invoke, group_id="g", run_id="r", version="v0", sink=sink, ledger=ledger)
    )
    assert result == 42
    assert ledger.diagnostics[-1]["reason"] == "usage_sink_failed"


def test_hooks_restore_owned_scope_and_shared_concurrent_client():
    a, b = [], []

    async def exercise():
        async with httpx.AsyncClient(
            transport=httpx.MockTransport(lambda request: httpx.Response(200, json={}))
        ) as client:
            entered, ended = asyncio.Event(), asyncio.Event()

            async def first():
                install_http_hooks(client)
                await client.get("https://example.invalid/one")
                entered.set()
                await ended.wait()
                await client.get("https://example.invalid/two")
                return 1

            async def second():
                await entered.wait()
                install_http_hooks(client)
                await client.get("https://example.invalid/three")
                return 2

            task = asyncio.create_task(capture(first, a, run_id="a"))
            await capture(second, b, run_id="b")
            assert len(client.event_hooks["request"]) == 1
            ended.set()
            await task
            assert client.event_hooks["request"] == []
            assert client.event_hooks["response"] == []
        assert len(a[0]["provider_events"]) == 2
        assert len(b[0]["provider_events"]) == 1

    asyncio.run(exercise())


def test_sdk_failure_then_explicit_retry_retains_missing_tokens():
    rows = []
    attempts = []

    async def sdk(**kwargs):
        attempts.append(True)
        if len(attempts) == 1:
            raise TimeoutError("sensitive endpoint details")
        return {"usage": {"input_tokens": 5, "output_tokens": 2}}

    async def invoke():
        try:
            await observe_sdk(sdk, usage_operation="test", usage_provider="fixture")
        except TimeoutError:
            pass
        return await observe_sdk(sdk, usage_operation="test", usage_provider="fixture")

    asyncio.run(capture(invoke, rows, adapter_coverage="default_adapters"))
    assert [e["outcome"] for e in rows[0]["model_calls"]] == ["failed", "completed"]
    summary = summarize(rows[0])
    assert summary["metrics"]["total_tokens"] is None
    assert summary["observed_token_subtotal"] == 7
    assert "sensitive" not in json.dumps(rows)


def test_existing_usage_callback_is_additive_not_double_counted():
    from langchain_core.callbacks import UsageMetadataCallbackHandler

    rows = []
    existing = UsageMetadataCallbackHandler()
    model = FakeMessagesListChatModel(
        responses=[
            AIMessage(
                content="ok",
                usage_metadata={"input_tokens": 2, "output_tokens": 1, "total_tokens": 3},
                response_metadata={"model_name": "fixture"},
            )
        ]
    )

    async def invoke():
        await model.ainvoke("private", config={"callbacks": [existing]})
        return True

    asyncio.run(capture(invoke, rows))
    assert len(rows[0]["model_calls"]) == 1
    assert rows[0]["model_calls"][0]["total_tokens"] == 3
    assert existing.usage_metadata["fixture"]["total_tokens"] == 3
