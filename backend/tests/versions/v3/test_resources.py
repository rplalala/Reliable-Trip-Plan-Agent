"""Request lifecycle, shared failures and phase-state separation without real services."""

import asyncio
from time import monotonic

import httpx
import pytest

from backend.app.tripworld.database.vectors import SPACE
from backend.app.tripworld.retrieval.geography import GeographicScope
from backend.app.versions.v3.resources import RequestRetrieval
from backend.tests.tripworld.test_runtime_retrieval import configured
from backend.tests.versions.v3.test_wiring import OwnedRetrieval


@pytest.mark.parametrize("stage", ["factory", "enter", "prepare"])
def test_initialization_failure_is_request_terminal_and_cleanup_is_owned(stage):
    class Runtime(OwnedRetrieval):
        async def __aenter__(self):
            await super().__aenter__()
            if stage == "enter":
                raise RuntimeError("enter failure")
            return self

        async def prepare(self):
            await super().prepare()
            if stage == "prepare":
                raise RuntimeError("prepare failure")

    async def scenario():
        runtime, factories = Runtime(), []

        def factory():
            factories.append(1)
            if stage == "factory":
                raise RuntimeError("factory failure")
            return runtime

        owner = RequestRetrieval(factory, monotonic() + 60)
        for _ in range(2):
            with pytest.raises(RuntimeError):
                async with owner:
                    await owner.prepare()
        assert len(factories) == 1
        assert not owner.allows_embedding(["museum"])
        await owner.close()
        await owner.close()
        assert runtime.closes == (0 if stage == "factory" else 1)

    asyncio.run(scenario())


def test_search_failure_cannot_retry_by_changing_top_k():
    class Runtime(OwnedRetrieval):
        async def search(self, *args):
            self.searches += 1
            raise TimeoutError("mock SQL failure")

    async def scenario():
        runtime = Runtime()
        owner = RequestRetrieval(lambda: runtime, monotonic() + 60)
        scope = GeographicScope(latitude=0, longitude=0, radius_km=15)
        async with owner:
            await owner.prepare()
            with pytest.raises(TimeoutError):
                await owner.search([1], scope, 20)
        assert not runtime.closed
        with pytest.raises(RuntimeError, match="Previous"):
            await owner.search([1], scope, 10)
        assert runtime.searches == 1
        await owner.close()
        assert runtime.closes == 1

    asyncio.run(scenario())


def test_real_runtime_reuses_embedding_sdk_client_and_removes_hooks(tmp_path, monkeypatch):
    def handler(request):
        return httpx.Response(
            200,
            json={
                "object": "list",
                "model": SPACE["model"],
                "data": [{"object": "embedding", "index": 0, "embedding": [1.0] + [0.0] * 1535}],
                "usage": {"prompt_tokens": 1, "total_tokens": 1},
            },
        )

    runtime, conn, _ = configured(tmp_path, monkeypatch, handler)

    async def scenario():
        async with runtime:
            await runtime.prepare()
            await runtime.embed(["first"])
            client = runtime.client
            await runtime.embed(["second"])
            assert runtime.client is client
            assert len(runtime.http_attempts) == runtime.embedding_sends == 2
            http, request_hook, response_hook = runtime._http_hooks
            assert http.event_hooks["request"].count(request_hook) == 1
        assert client.is_closed() and conn.closed
        assert request_hook not in http.event_hooks["request"]
        assert response_hook not in http.event_hooks["response"]

    asyncio.run(scenario())


def test_cleanup_failure_does_not_replace_cancellation():
    class Runtime(OwnedRetrieval):
        async def __aexit__(self, *_):
            await super().__aexit__()
            raise RuntimeError("cleanup failure")

    async def scenario():
        runtime = Runtime()
        owner = RequestRetrieval(lambda: runtime, monotonic() + 60)
        try:
            async with owner:
                await owner.prepare()
                raise asyncio.CancelledError()
        finally:
            await owner.close()
            assert runtime.closes == 1
            assert owner.operations[-1]["operation"] == "close"

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(scenario())


def test_repair_cannot_retry_reserved_pre_send_failure_or_claim_it_as_sent():
    from backend.app.runtime.cache import RequestCache
    from backend.app.versions.v3.repair_budget import RepairBudget

    async def scenario():
        cache = RequestCache()
        cache.attempts[("places_details", "failed")] = "reserved_not_sent"
        budget = RepairBudget(monotonic() + 180, cache=cache)
        value = await budget.call(
            ("places_details", "failed"),
            lambda: pytest.fail("No cross-phase retry"),
            charges={"details": 1},
        )
        assert value is None and budget.used["details"] == 0
        assert budget.stops == ["previous_attempt"]
        assert cache.attempts[("places_details", "failed")] == "reserved_not_sent"

    asyncio.run(scenario())


def test_expired_borrowed_port_does_not_invoke_client():
    from backend.app.versions.v3.resources import DeadlinePort

    class Client:
        async def search_text(self, request):
            pytest.fail("Expired request must not send")

    async def scenario():
        port = DeadlinePort(Client(), monotonic() - 1)
        with pytest.raises(TimeoutError):
            await port.search_text(None)

    asyncio.run(scenario())


def test_cli_owned_cleanup_preserves_error_and_closes_each_client_once():
    from backend.app.versions.v1.runner import _run_with_owned_clients

    class Client:
        closes = 0

        async def aclose(self):
            self.closes += 1

    async def scenario():
        owned, borrowed = Client(), Client()

        async def fail():
            raise asyncio.CancelledError()

        with pytest.raises(asyncio.CancelledError):
            await _run_with_owned_clients(fail(), [owned])
        assert owned.closes == 1 and borrowed.closes == 0

    asyncio.run(scenario())


def test_official_factory_registers_resources_before_later_assembly_failure(monkeypatch):
    from types import SimpleNamespace

    from backend.app.runtime.config_loader import load_runtime_config
    from backend.app.versions.v1 import runner

    class Client:
        closes = 0

        async def aclose(self):
            self.closes += 1

    created = Client()
    settings = SimpleNamespace(
        azure_openai_endpoint="https://unit.example",
        azure_openai_deployment="fixture",
        azure_openai_api_key=SimpleNamespace(get_secret_value=lambda: "unit-key"),
    )
    monkeypatch.setattr(runner, "AzureFoundryWebEvidenceProvider", lambda **kwargs: created)

    def fail(**kwargs):
        raise RuntimeError("reasoner construction failed")

    monkeypatch.setattr(runner, "AzureFoundryEvidenceReasoner", fail)
    owners = []
    with pytest.raises(RuntimeError):
        runner._create_official_web_providers(
            settings, load_runtime_config().web_evidence, owned_clients=owners
        )
    assert owners == [created]
    asyncio.run(runner._close_owned_clients(owners))
    assert created.closes == 1


def test_official_factory_does_not_recreate_or_close_injected_clients(monkeypatch):
    from types import SimpleNamespace

    from backend.app.runtime.config_loader import load_runtime_config
    from backend.app.versions.v1 import runner

    settings = SimpleNamespace(
        azure_openai_endpoint="https://unit.example",
        azure_openai_deployment="fixture",
        azure_openai_api_key=SimpleNamespace(get_secret_value=lambda: "unit-key"),
    )

    def forbidden(**kwargs):
        pytest.fail("Injected clients must not be recreated")

    monkeypatch.setattr(runner, "AzureFoundryWebEvidenceProvider", forbidden)
    monkeypatch.setattr(runner, "AzureFoundryEvidenceReasoner", forbidden)
    supplied, owners = (object(), object(), object()), []
    assert (
        runner._create_official_web_providers(
            settings, load_runtime_config().web_evidence, existing=supplied, owned_clients=owners
        )
        == supplied
    )
    assert owners == []
