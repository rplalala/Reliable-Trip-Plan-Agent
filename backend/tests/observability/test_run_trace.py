"""Tests for local best-effort Run Trace output and secret redaction."""

import json
from datetime import UTC, date, datetime
from uuid import UUID

from backend.app.observability.run_trace import (
    FileRunTracer,
    NullRunTracer,
    RunTraceContext,
    TracePayloadMode,
    create_run_tracer,
)
from backend.app.policies.trip_dates import create_trip_date_window
from backend.app.schemas.request import TravelRequest

RUN_ID = UUID("00000000-0000-0000-0000-000000000001")


def _context() -> RunTraceContext:
    reference_date = date(2026, 9, 11)
    return RunTraceContext(
        run_id=RUN_ID,
        system_version="v1",
        reference_date=reference_date,
        date_window=create_trip_date_window(reference_date),
        request=TravelRequest(request_text="Plan Sydney."),
        started_at=datetime(2026, 9, 11, tzinfo=UTC),
    )


def test_raw_run_trace_writes_structure_and_redacts_secrets(tmp_path) -> None:
    tracer = FileRunTracer(
        _context(), root=tmp_path, payload_mode=TracePayloadMode.RAW
    )
    tracer.event("run_started", {"Authorization": "Bearer top-secret"})
    tracer.payload(
        "tools",
        "provider",
        {
            "headers": {"X-Goog-Api-Key": "google-secret"},
            "url": "https://example.test/data?key=query-secret",
        },
        minimum_mode=TracePayloadMode.RAW,
    )
    tracer.finish(
        status="failed",
        requirements=None,
        tool_usage={"weather_calls": {"used": 1, "limit": 1}},
        outcome=None,
        error={"credential": "azure-secret", "message": "failed"},
    )

    assert (tracer.run_directory / "run.json").is_file()
    assert (tracer.run_directory / "events.jsonl").is_file()
    assert (tracer.run_directory / "llm").is_dir()
    assert (tracer.run_directory / "tools").is_dir()
    assert (tracer.run_directory / "evidence").is_dir()
    assert (tracer.run_directory / "error.json").is_file()
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in tracer.run_directory.rglob("*.json*")
    )
    assert "top-secret" not in combined
    assert "google-secret" not in combined
    assert "query-secret" not in combined
    assert "azure-secret" not in combined
    assert "[REDACTED]" in combined
    event_lines = (tracer.run_directory / "events.jsonl").read_text(
        encoding="utf-8"
    ).splitlines()
    assert len(event_lines) == 1
    assert json.loads(event_lines[0])["event"] == "run_started"


def test_metadata_mode_does_not_write_optional_payloads(tmp_path) -> None:
    tracer = FileRunTracer(
        _context(), root=tmp_path, payload_mode=TracePayloadMode.METADATA
    )

    tracer.payload(
        "tools", "raw", {"value": "hidden"}, minimum_mode=TracePayloadMode.RAW
    )

    assert list((tracer.run_directory / "tools").iterdir()) == []



def test_disabled_or_failed_trace_creation_returns_null_tracer(tmp_path) -> None:
    disabled = create_run_tracer(
        _context(),
        enabled=False,
        root=tmp_path,
        payload_mode=TracePayloadMode.RAW,
    )
    blocking_file = tmp_path / "not-a-directory"
    blocking_file.write_text("block", encoding="utf-8")
    failed = create_run_tracer(
        _context(),
        enabled=True,
        root=blocking_file,
        payload_mode=TracePayloadMode.RAW,
    )

    assert isinstance(disabled, NullRunTracer)
    assert isinstance(failed, NullRunTracer)
