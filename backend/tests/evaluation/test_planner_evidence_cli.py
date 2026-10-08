"""Generation evidence through the confirmed public CLI; external HTTP is simulated."""

import hashlib
import json

import httpx
import pytest

from backend.app.observability.mechanism_observation import accepted_catalog
from backend.app.observability.usage import install_http_hooks
from backend.evaluation.tools.planner_usage_cli import main
from backend.tests.evaluation.test_planner_usage_cli import REFERENCE, arguments, result


def test_cli_binds_redacted_wire_and_mechanism_to_unchanged_result(tmp_path):
    seen = []

    class WireRuntime:
        async def run(self, version, request, *, reference_date, tracer=None):
            accepted_catalog([])

            def response(wire):
                seen.append(wire)
                return httpx.Response(
                    200,
                    json={
                        "name": "ordinary response",
                        "api_key": "fixture-wire-secret",
                        "echo": "fixture-wire-secret first-query-secret cookie-value-secret",
                        "usage": {"cached_tokens": 3},
                    },
                )

            async with httpx.AsyncClient(transport=httpx.MockTransport(response)) as client:
                install_http_hooks(client)
                value = await client.get(
                    "https://places.googleapis.com/v1/places/fixture"
                    "?key=first-query-secret&key=fixture-wire-secret",
                    headers={
                        "X-Goog-Api-Key": "fixture-wire-secret",
                        "X-Goog-FieldMask": "id",
                        "Cookie": "session=cookie-value-secret",
                    },
                )
                assert value.json()["api_key"] == "fixture-wire-secret"
            return result(version, request)

    assert (
        main(
            arguments(tmp_path) + ["--capture-evidence"],
            runtime=WireRuntime(),
            date_provider=REFERENCE,
        )
        == 0
    )
    output = tmp_path / "capture"
    mechanism = json.loads((output / "mechanism.json").read_bytes())
    usage = json.loads((output / "usage.json").read_bytes())
    index = json.loads((output / "evidence-index.json").read_bytes())
    sha = hashlib.sha256((output / "result.json").read_bytes()).hexdigest()
    assert mechanism["result_sha256"] == usage["result_sha256"] == index["result_sha256"] == sha
    assert mechanism["input_sha256"] == index["input_sha256"]
    assert len(seen) == len(index["http_events"]) == 1
    event = index["http_events"][0]
    assert event["event_id"] == usage["provider_events"][0]["event_id"]
    assert event["response_body_status"] == "complete"
    body = json.loads((output / event["response_body_ref"]).read_bytes())["body"]
    assert body["usage"]["cached_tokens"] == 3
    for ref in index["artifacts"]:
        path = output / ref["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == ref["sha256"]
    saved = "".join(p.read_text(encoding="utf-8") for p in output.rglob("*.json"))
    assert "fixture-wire-secret" not in saved
    assert "first-query-secret" not in saved
    assert "cookie-value-secret" not in saved
    assert "ordinary response" in saved
    assert index["adapter_coverage"] == "unverified"
    assert not index["qualified_four_version_batch"]


@pytest.mark.parametrize("outcome", ["completed", "failed", "cancelled"])
def test_cli_keeps_lazy_stream_and_trace_on_every_outcome(tmp_path, outcome):
    import asyncio

    from backend.app.observability.run_trace import TracePayloadMode

    consumed = []

    class Stream(httpx.AsyncByteStream):
        async def __aiter__(self):
            for chunk in (b'{"message":"', b'streamed fixture"}'):
                consumed.append(chunk)
                yield chunk

    class StreamRuntime:
        async def run(self, version, request, *, reference_date, tracer=None):
            assert tracer is not None
            async with httpx.AsyncClient(
                transport=httpx.MockTransport(lambda _: httpx.Response(200, stream=Stream()))
            ) as client:
                install_http_hooks(client)
                async with client.stream("GET", "https://example.org/stream") as response:
                    assert consumed == []
                    assert await response.aread() == b'{"message":"streamed fixture"}'
            tracer.payload(
                "llm", "fixture", {"text": "trace fixture"}, minimum_mode=TracePayloadMode.RAW
            )
            if outcome == "failed":
                raise RuntimeError("synthetic failure")
            if outcome == "cancelled":
                raise asyncio.CancelledError()
            return result(version, request)

    assert main(
        arguments(tmp_path) + ["--capture-evidence"],
        runtime=StreamRuntime(),
        date_provider=REFERENCE,
    ) == (0 if outcome == "completed" else 1)
    output = tmp_path / "capture"
    index = json.loads((output / "evidence-index.json").read_bytes())
    mechanism = json.loads((output / "mechanism.json").read_bytes())
    assert mechanism["outcome"] == outcome
    assert index["http_events"][0]["response_body_status"] == "complete"
    assert (
        index["result_sha256"] is not None
        if outcome == "completed"
        else index["result_sha256"] is None
    )
    assert any("trace" in ref["path"] for ref in index["artifacts"])
    assert "trace fixture" in "".join(p.read_text(encoding="utf-8") for p in output.rglob("*.json"))


def test_cli_captures_normally_decoded_compressed_response(tmp_path):
    import gzip

    class Stream(httpx.AsyncByteStream):
        async def __aiter__(self):
            yield gzip.compress(b'{"fixture":"compressed response"}')

    class Runtime:
        async def run(self, version, request, *, reference_date, tracer=None):
            async with httpx.AsyncClient(
                transport=httpx.MockTransport(
                    lambda _: httpx.Response(
                        200, headers={"content-encoding": "gzip"}, stream=Stream()
                    )
                )
            ) as client:
                install_http_hooks(client)
                value = await client.get("https://example.org/compressed")
                assert value.json() == {"fixture": "compressed response"}
            return result(version, request)

    assert (
        main(
            arguments(tmp_path) + ["--capture-evidence"], runtime=Runtime(), date_provider=REFERENCE
        )
        == 0
    )
    output = tmp_path / "capture"
    index = json.loads((output / "evidence-index.json").read_bytes())
    row = index["http_events"][0]
    assert row["response_body_status"] == "complete"
    assert json.loads((output / row["response_body_ref"]).read_bytes())["body"] == {
        "fixture": "compressed response"
    }


def test_cli_reports_unread_and_oversized_streams_without_extra_reads(tmp_path):
    from backend.app.observability.raw_capture import BODY_LIMIT

    reads = []

    class Stream(httpx.AsyncByteStream):
        async def __aiter__(self):
            reads.append(1)
            yield b"x" * (BODY_LIMIT + 1)

    class Runtime:
        async def run(self, version, request, *, reference_date, tracer=None):
            async with httpx.AsyncClient(
                transport=httpx.MockTransport(lambda _: httpx.Response(200, stream=Stream()))
            ) as client:
                install_http_hooks(client)
                async with client.stream("GET", "https://example.org/unread"):
                    assert reads == []
                async with client.stream("GET", "https://example.org/oversized") as response:
                    assert len(await response.aread()) == BODY_LIMIT + 1
            return result(version, request)

    assert (
        main(
            arguments(tmp_path) + ["--capture-evidence"], runtime=Runtime(), date_provider=REFERENCE
        )
        == 0
    )
    index = json.loads((tmp_path / "capture/evidence-index.json").read_bytes())
    assert reads == [1]
    assert [r["response_body_status"] for r in index["http_events"]] == [
        "incomplete",
        "omitted_size_limit",
    ]
    assert index["collection_status"] == "partial"


@pytest.mark.parametrize("vector_write_fails", [False, True])
def test_cli_captures_sdk_embedding_vectors_and_clears_ambient_scope(
    tmp_path, monkeypatch, vector_write_fails
):
    import httpx2
    import numpy as np
    from openai import AsyncOpenAI

    from backend.app.tripworld.retrieval.runtime import RuntimeRetrieval

    if vector_write_fails:
        from pathlib import Path

        original_open = Path.open

        def open_vector(path, mode="r", *args, **kwargs):
            if path.suffix == ".npz" and mode == "xb":
                raise OSError("synthetic vector write failure")
            return original_open(path, mode, *args, **kwargs)

        monkeypatch.setattr(Path, "open", open_vector)

    monkeypatch.setenv("OPENAI_API_KEY", "fixture-embedding-secret")
    sends = []

    def response(request):
        sends.append(request)
        return httpx2.Response(
            200,
            json={
                "object": "list",
                "model": "text-embedding-3-small",
                "data": [{"object": "embedding", "index": 0, "embedding": [1.0] * 1536}],
                "usage": {"prompt_tokens": 4, "total_tokens": 4},
            },
        )

    class Runtime:
        async def run(self, version, request, *, reference_date, tracer=None):
            from types import SimpleNamespace

            async with RuntimeRetrieval(
                SimpleNamespace(embedding_timeout=30),
                embedding_client_factory=lambda **kwargs: AsyncOpenAI(
                    **kwargs,
                    http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(response)),
                ),
            ) as rag:
                rag.artifact_hash = "a" * 64  # Synthetic corpus identity; no DB verification.
                vectors = await rag.embed(["fixture query"])
                assert np.linalg.norm(vectors[0]) == pytest.approx(1)
            return result(version, request)

    assert (
        main(
            arguments(tmp_path) + ["--capture-evidence"], runtime=Runtime(), date_provider=REFERENCE
        )
        == 0
    )
    output = tmp_path / "capture"
    index = json.loads((output / "evidence-index.json").read_bytes())
    vector_refs = [r for r in index["artifacts"] if r["path"].endswith(".npz")]
    assert len(sends) == len(index["http_events"]) == 1
    if vector_write_fails:
        assert not vector_refs
        assert "query_vectors" in index["missing_fields"]
        return
    assert len(vector_refs) == 1
    with np.load(output / vector_refs[0]["path"], allow_pickle=False) as bundle:
        metadata = json.loads(str(bundle["metadata"]))
        assert metadata["artifact_hash"] == "a" * 64
        assert metadata["text_sha256"] == [hashlib.sha256(b"fixture query").hexdigest()]
        assert metadata["vectors_sha256"] == hashlib.sha256(bundle["vectors"].tobytes()).hexdigest()
    other = tmp_path / "later"
    other.mkdir()
    assert main(arguments(other), runtime=Runtime(), date_provider=REFERENCE) == 0
    assert len(sends) == 2
    assert len(list(output.rglob("*.npz"))) == 1
    assert not list((other / "capture").rglob("*.npz"))


@pytest.mark.parametrize("target", ["wire", "usage"])
def test_cli_records_capture_write_failure_without_losing_result(tmp_path, monkeypatch, target):
    from pathlib import Path

    original_write = Path.write_bytes

    def write(path, data):
        if (target == "wire" and "wire" in path.parts) or (
            target == "usage" and path.name == "usage.json"
        ):
            raise OSError("synthetic filesystem failure")
        return original_write(path, data)

    monkeypatch.setattr(Path, "write_bytes", write)

    class Runtime:
        async def run(self, version, request, *, reference_date, tracer=None):
            async with httpx.AsyncClient(
                transport=httpx.MockTransport(
                    lambda _: httpx.Response(200, json={"fixture": "response"})
                )
            ) as client:
                install_http_hooks(client)
                await client.get("https://example.org/fixture")
            return result(version, request)

    assert main(
        arguments(tmp_path) + ["--capture-evidence"], runtime=Runtime(), date_provider=REFERENCE
    ) == (1 if target == "usage" else 0)
    output = tmp_path / "capture"
    assert (output / "result.json").is_file()
    index = json.loads((output / "evidence-index.json").read_bytes())
    assert index["collection_status"] == "partial"
    assert (
        ("usage" in index["missing_fields"])
        if target == "usage"
        else (index["http_events"][0]["response_body_status"] == "write_failed")
    )
