"""Shared parsing and trace helpers for Google provider adapters."""

from collections.abc import Mapping

from backend.app.observability.run_trace import RunTracer, TracePayloadMode


class ProviderResponseError(RuntimeError):
    """A provider returned JSON that lacks fields required by its DTO."""


def require_mapping(value: object, *, context: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise ProviderResponseError(f"{context} must be a JSON object")
    return value


def trace_exchange(
    tracer: RunTracer,
    *,
    name: str,
    request: object,
    response: object,
) -> None:
    """Write an opt-in raw provider exchange through central redaction."""

    tracer.payload(
        "tools",
        name,
        {"request": request, "response": response},
        minimum_mode=TracePayloadMode.RAW,
    )
