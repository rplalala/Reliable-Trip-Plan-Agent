"""Mocked API retries, response checks, budgets, and paid-batch resume semantics."""

import base64
import json
from types import SimpleNamespace

import httpx
import numpy as np
import pytest
from openai import OpenAI

from tools.data.tripworld.embedding_build import encode_resumable
from tools.data.tripworld.embedding_config import EmbeddingConfig, EncodedBatch
from tools.data.tripworld.openai_adapter import (
    OpenAIEmbeddingAdapter,
    OpenAIEmbeddingError,
)


@pytest.fixture(autouse=True)
def fake_tokenizer(monkeypatch):
    # Network-independent unit test tokenizer; real cl100k is used in the live spike.
    monkeypatch.setattr(
        "tools.data.tripworld.estimation.tokenizer",
        lambda: SimpleNamespace(encode_ordinary=lambda text: list(text.encode())),
    )


def response_payload(count, *, dimensions=1536):
    return {
        "object": "list",
        "model": "text-embedding-3-small",
        "usage": {"prompt_tokens": 12, "total_tokens": 12},
        "data": [
            {"object": "embedding", "index": i, "embedding": [1.0] + [0.0] * (dimensions - 1)}
            for i in reversed(range(count))
        ],
    }


def test_api_adapter_default_dimensions_retry_and_response_order():
    requests = []
    sleeps = []

    def handler(request):
        requests.append(json.loads(request.content))
        if len(requests) == 1:
            return httpx.Response(
                429, json={"error": {"message": "rate limited"}}, headers={"retry-after": "0"}
            )
        return httpx.Response(200, json=response_payload(2), headers={"x-request-id": "test"})

    client = OpenAI(
        api_key="test-only",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    adapter = OpenAIEmbeddingAdapter(EmbeddingConfig(), client=client, sleep=sleeps.append)
    result = adapter.encode(["museum", "gallery"])
    assert len(requests) == 2 and len(sleeps) == 1
    assert result.attempts == 2 and result.total_tokens == 12
    assert result.vectors.shape == (2, 1536)
    assert requests[0]["input"] == ["museum", "gallery"]
    assert "dimensions" not in requests[0]
    assert requests[0]["model"] == "text-embedding-3-small"
    adapter.close()


def test_base64_transport_preserves_float32_vectors():
    expected = np.zeros((1, 1536), dtype=np.float32)
    expected[0, 0] = 1

    def handler(request):
        assert json.loads(request.content)["encoding_format"] == "base64"
        payload = response_payload(1)
        payload["data"][0]["embedding"] = base64.b64encode(expected.tobytes()).decode()
        return httpx.Response(200, json=payload)

    client = OpenAI(
        api_key="test-only",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    adapter = OpenAIEmbeddingAdapter(EmbeddingConfig(), client=client)
    assert np.array_equal(adapter.encode(["museum"]).vectors, expected)
    adapter.close()


def test_authentication_failure_not_retried_and_no_secret_in_error():
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(401, json={"error": {"message": "secret must not leak"}})

    client = OpenAI(
        api_key="test-only",
        max_retries=0,
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    adapter = OpenAIEmbeddingAdapter(EmbeddingConfig(), client=client)
    with pytest.raises(OpenAIEmbeddingError) as failure:
        adapter.encode(["museum"])
    assert len(calls) == 1
    assert "secret" not in str(failure.value) and "401" in str(failure.value)
    adapter.close()


def test_missing_key_has_no_provider_fallback(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(OpenAIEmbeddingError, match="Set OPENAI_API_KEY"):
        OpenAIEmbeddingAdapter(EmbeddingConfig())


def test_adapter_response_dimension_validation():
    client = OpenAI(
        api_key="test-only",
        max_retries=0,
        http_client=httpx.Client(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(
                    200,
                    json=response_payload(1, dimensions=3),
                )
            ),
        ),
    )
    adapter = OpenAIEmbeddingAdapter(EmbeddingConfig(), client=client)
    with pytest.raises(ValueError, match="shape"):
        adapter.encode(["museum"])
    adapter.close()


class InterruptedProvider:
    config = EmbeddingConfig()

    def __init__(self, fail_on=None):
        self.calls = 0
        self.fail_on = fail_on

    def encode(self, texts, *, query=False):
        self.calls += 1
        if self.calls == self.fail_on:
            raise RuntimeError("simulated interruption")
        vectors = np.zeros((len(texts), 1536), dtype=np.float32)
        vectors[:, 0] = 1
        return EncodedBatch(vectors, len(texts), len(texts), "text-embedding-3-small")


def test_resume_does_not_pay_for_completed_batches(tmp_path):
    texts = ["a", "b", "c", "d", "e"]
    provider = InterruptedProvider(fail_on=2)
    with pytest.raises(RuntimeError):
        encode_resumable(texts, provider, tmp_path, token_counts=[1] * 5, batch_size=2)
    assert len(list(tmp_path.glob("*.npz"))) == 1
    resumed = InterruptedProvider()
    vectors, report = encode_resumable(
        texts,
        resumed,
        tmp_path,
        token_counts=[1] * 5,
        batch_size=2,
    )
    assert vectors.shape == (5, 1536)
    assert resumed.calls == 2
    assert report["reused_batches"] == 1 and report["new_api_batches"] == 2
    again = InterruptedProvider()
    _, reused = encode_resumable(texts, again, tmp_path, token_counts=[1] * 5, batch_size=2)
    assert again.calls == 0 and reused["new_usage_tokens"] == 0


def test_cost_limit_empty_overlong_inputs_rejected_before_api(tmp_path):
    provider = InterruptedProvider()
    for texts, counts in [([""], [1]), (["text"], [9000])]:
        with pytest.raises(ValueError):
            encode_resumable(texts, provider, tmp_path, token_counts=counts)
    provider.config = EmbeddingConfig(max_run_usd=0.00000001)
    with pytest.raises(ValueError, match="cost budget"):
        encode_resumable(["text"], provider, tmp_path, token_counts=[5])
    assert provider.calls == 0


def test_batch_token_limit_controls_partitioning(tmp_path):
    provider = InterruptedProvider()
    provider.config = EmbeddingConfig(max_batch_tokens=3)
    _, report = encode_resumable(
        ["aa", "bb", "cc"],
        provider,
        tmp_path,
        token_counts=[2, 2, 2],
    )
    assert provider.calls == report["new_api_batches"] == 3
