"""Offline safeguards for the bounded SELECT diagnostic entry point."""

import asyncio
import hashlib
import json

import numpy as np
import pytest

from tools.diagnostics.retrieval_performance import (
    TimedConnection,
    error_chain,
    reserve,
    saved_vector,
)


def test_diagnostic_attempts_are_reserved_before_execution(tmp_path):
    for number in range(1, 9):
        assert reserve(tmp_path, "analyze15") == number
    with pytest.raises(ValueError, match="limit"):
        reserve(tmp_path, "normal15")


def test_saved_vector_rejects_checksum_and_normalization(tmp_path):
    vector = np.zeros((1, 1536), dtype=np.float32)
    vector[0, 0] = 1
    metadata = {
        "response_model": "text-embedding-3-small",
        "vectors_sha256": hashlib.sha256(vector.tobytes()).hexdigest(),
    }
    path = tmp_path / "query.npz"
    np.savez(path, vectors=vector, metadata=json.dumps(metadata))
    assert saved_vector(path)[0].shape == (1536,)
    vector[0, 0] = 2
    np.savez(path, vectors=vector, metadata=json.dumps(metadata))
    with pytest.raises(ValueError, match="checksum"):
        saved_vector(path)
    metadata["vectors_sha256"] = hashlib.sha256(vector.tobytes()).hexdigest()
    np.savez(path, vectors=vector, metadata=json.dumps(metadata))
    with pytest.raises(ValueError, match="normalized"):
        saved_vector(path)


def test_timeout_preserves_structured_cause():
    class ServerCancellation(Exception):
        sqlstate = "57014"

    outer = TimeoutError()
    outer.__cause__ = ServerCancellation()
    assert error_chain(outer) == [
        {"type": "TimeoutError", "sqlstate": None},
        {"type": "ServerCancellation", "sqlstate": "57014"},
    ]


def test_execute_timeout_does_not_invent_fetch_timing():
    class Connection:
        async def execute(self, *_):
            raise TimeoutError()

    timings = {}
    with pytest.raises(TimeoutError):
        asyncio.run(TimedConnection(Connection(), timings).execute("SELECT 1"))
    assert "execute_seconds" in timings
    assert "fetch_decode_seconds" not in timings


def test_default_embedding_transport_hooks_observe_mock_send(monkeypatch):
    import httpx
    import httpx2
    from openai import AsyncOpenAI, DefaultAsyncHttpxClient

    async def wrong_transport(*args, **kwargs):
        raise AssertionError("The SDK default must not use this patched httpx method")

    monkeypatch.setattr(httpx.AsyncClient, "send", wrong_transport)
    sends = []

    async def hook(request):
        sends.append(request.url.path)

    def handler(request):
        return httpx2.Response(
            200,
            json={
                "object": "list",
                "model": "text-embedding-3-small",
                "data": [{"object": "embedding", "index": 0, "embedding": [1.0]}],
                "usage": {"prompt_tokens": 1, "total_tokens": 1},
            },
        )

    async def run():
        async with AsyncOpenAI(
            api_key="fake-offline-key",
            max_retries=0,
            http_client=DefaultAsyncHttpxClient(
                transport=httpx2.MockTransport(handler), event_hooks={"request": [hook]}
            ),
        ) as client:
            result = await client.embeddings.create(model="text-embedding-3-small", input=["test"])
            assert result.usage.total_tokens == 1

    asyncio.run(run())
    assert sends == ["/v1/embeddings"]
