"""Benchmark-owned attempt capture; quality evaluation never invokes this runner."""

import asyncio
import hashlib
from contextvars import ContextVar
from datetime import UTC, datetime

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.tracers.context import register_configure_hook

from backend.app.observability.usage import UsageLedger, current_usage, finish_attempt

_callback = ContextVar("rtpeval_model_callback", default=None)
register_configure_hook(_callback, inheritable=True)


class ModelUsageCallback(BaseCallbackHandler):
    run_inline = True

    def __init__(self, ledger):
        self.ledger = ledger

    def on_chat_model_start(self, serialized, messages, *, run_id, **kwargs):
        params = kwargs.get("invocation_params") or {}
        self.ledger.begin(
            "model",
            "langchain",
            "chat_model",
            event_id=str(run_id),
            model=params.get("model") or params.get("model_name"),
            source="langchain_message_usage",
        )

    def on_llm_end(self, response, *, run_id, **kwargs):
        usage = None
        for group in response.generations:
            for generation in group:
                message = getattr(generation, "message", None)
                if getattr(message, "usage_metadata", None) is not None:
                    usage = message.usage_metadata
                    break
        self.ledger.finish("model", str(run_id), usage=usage)

    def on_llm_error(self, error, *, run_id, **kwargs):
        self.ledger.finish(
            "model",
            str(run_id),
            outcome="cancelled" if isinstance(error, asyncio.CancelledError) else "failed",
            error_type=type(error).__name__,
        )


async def capture_attempt(
    invoke,
    *,
    group_id,
    run_id,
    version,
    sink,
    cleanup=None,
    serialize=None,
    ledger=None,
    namespace="planner",
    adapter_coverage="unverified",
):
    """Preserve return/exception, including cleanup; emit an envelope to a caller-owned sink.

    invoke is a zero-argument async callable owned by the benchmark producer. Include all
    client ownership in invoke, or provide an async cleanup. Do not pass an already-started
    task. The serializer must be the exact function used to save the result bytes.
    """
    if current_usage.get() is not None:
        raise ValueError("Nested attempt capture would double count usage")
    if version not in ("v0", "v1", "v2", "v3") or namespace not in ("planner", "oracle"):
        raise ValueError("Invalid usage identity")
    if not group_id or not run_id:
        raise ValueError("Usage linkage requires group and run IDs")
    ledger = ledger or UsageLedger()
    token = current_usage.set(ledger)
    callback_token = _callback.set(ModelUsageCallback(ledger))
    started_at = datetime.now(UTC).isoformat()
    started = ledger.clock()
    result = None
    outcome = "failed"
    primary_error = None
    try:
        try:
            result = await invoke()
            outcome = "completed"
        except BaseException as exc:
            primary_error = exc
            outcome = "cancelled" if isinstance(exc, asyncio.CancelledError) else "failed"
            raise
        finally:
            if cleanup is not None:
                try:
                    await cleanup()
                except BaseException as exc:
                    ledger.diagnostics.append(
                        {"reason": "cleanup_failed", "error_type": type(exc).__name__}
                    )
                    if primary_error is None:
                        outcome = (
                            "cancelled" if isinstance(exc, asyncio.CancelledError) else "failed"
                        )
                        raise
    finally:
        # Stop the common clock before serialization, file output and sink work.
        data = finish_attempt(ledger, started, started_at, outcome)
        current_usage.reset(token)
        _callback.reset(callback_token)
        digest = None
        if result is not None and outcome == "completed" and serialize is not None:
            try:
                raw = serialize(result)
                if isinstance(raw, str):
                    raw = raw.encode("utf-8")
                digest = hashlib.sha256(raw).hexdigest()
            except Exception as exc:
                data["diagnostics"].append(
                    {"reason": "result_hash_unavailable", "error_type": type(exc).__name__}
                )
        if adapter_coverage not in ("default_adapters", "unverified"):
            adapter_coverage = "unverified"
        if adapter_coverage == "unverified":
            data["missing_fields"].append("adapter_coverage")
        if digest is None:
            data["missing_fields"].append("result_sha256")
        data.update(
            schema_version="rtpeval_usage_1",
            group_id=group_id,
            run_id=run_id,
            version=version,
            namespace=namespace,
            result_sha256=digest,
            collection_status="partial" if data["missing_fields"] else "available",
            coverage={
                "scope": "instrumented_adapters_only",
                "adapter_coverage": adapter_coverage,
                "unobserved_injected_clients": "not_inferred",
                "http_sends": "transport_entry_not_billing",
                "model_calls": "provider_invocations_not_internal_reasoning",
            },
        )
        try:
            sink(data)
        except Exception as exc:
            # A failed artifact sink must not replace the planner result or primary exception.
            ledger.diagnostics.append(
                {"reason": "usage_sink_failed", "error_type": type(exc).__name__}
            )
    return result
