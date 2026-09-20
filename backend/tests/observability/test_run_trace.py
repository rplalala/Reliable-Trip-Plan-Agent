"""Tests for local best-effort Run Trace output and secret redaction."""

import asyncio
import json
from datetime import UTC, date, datetime
from pathlib import Path
from uuid import UUID

from backend.app.observability.run_trace import (
    FileRunTracer,
    NullRunTracer,
    RunTraceContext,
    TracePayloadMode,
    create_run_tracer,
)
from backend.app.policies.trip_dates import create_trip_date_window
from backend.app.runtime.config_loader import load_runtime_config, runtime_config_snapshot
from backend.app.versions.v1.runner import run_v1
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    make_itinerary,
)
from backend.tests.versions.v1.fakes import RevisedFakeLLM as FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import (
    make_revised_extraction as make_extraction,
)

RUN_ID = UUID("00000000-0000-0000-0000-000000000001")


def _context() -> RunTraceContext:
    reference_date = date(2026, 9, 11)
    return RunTraceContext(
        run_id=RUN_ID,
        system_version="v1",
        reference_date=reference_date,
        date_window=create_trip_date_window(reference_date),
        request=make_request(additional_preferences="Plan Sydney."),
        started_at=datetime(2026, 9, 11, tzinfo=UTC),
    )


def test_raw_run_trace_writes_structure_and_redacts_secrets(tmp_path) -> None:
    tracer = FileRunTracer(_context(), root=tmp_path, payload_mode=TracePayloadMode.RAW)
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
        path.read_text(encoding="utf-8") for path in tracer.run_directory.rglob("*.json*")
    )
    assert "top-secret" not in combined
    assert "google-secret" not in combined
    assert "query-secret" not in combined
    assert "azure-secret" not in combined
    assert "[REDACTED]" in combined
    event_lines = (tracer.run_directory / "events.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(event_lines) == 1
    assert json.loads(event_lines[0])["event"] == "run_started"


def test_trace_records_effective_config_and_gates_optional_categories(tmp_path) -> None:
    snapshot, digest = runtime_config_snapshot(load_runtime_config())
    context = _context()
    context = RunTraceContext(
        **{
            **context.__dict__,
            "runtime_config": snapshot,
            "runtime_config_sha256": digest,
        }
    )
    tracer = FileRunTracer(
        context,
        root=tmp_path,
        payload_mode=TracePayloadMode.RAW,
        capture_llm=False,
        capture_tools=True,
        capture_evidence=False,
        raw_provider_payloads=False,
    )
    tracer.payload("llm", "request", {"value": 1}, minimum_mode=TracePayloadMode.RAW)
    tracer.payload("tools", "raw", {"value": 2}, minimum_mode=TracePayloadMode.RAW)
    tracer.payload("evidence", "normalized", {"value": 3}, minimum_mode=TracePayloadMode.NORMALIZED)
    metadata = json.loads((tracer.run_directory / "run.json").read_text(encoding="utf-8"))

    assert metadata["runtime_config"] == snapshot
    assert metadata["runtime_config_sha256"] == digest
    assert list((tracer.run_directory / "llm").iterdir()) == []
    assert list((tracer.run_directory / "tools").iterdir()) == []
    assert list((tracer.run_directory / "evidence").iterdir()) == []


def test_metadata_mode_does_not_write_optional_payloads(tmp_path) -> None:
    tracer = FileRunTracer(_context(), root=tmp_path, payload_mode=TracePayloadMode.METADATA)

    tracer.payload("tools", "raw", {"value": "hidden"}, minimum_mode=TracePayloadMode.RAW)

    assert list((tracer.run_directory / "tools").iterdir()) == []


def test_completed_v1_run_finalizes_trace_metadata_and_normalized_evidence(tmp_path) -> None:
    tracer = FileRunTracer(_context(), root=tmp_path, payload_mode=TracePayloadMode.NORMALIZED)

    result = asyncio.run(
        run_v1(
            make_request(additional_preferences="Plan Sydney."),
            FakeStructuredLLMClient([make_extraction(), make_itinerary()]),
            FakePlacesProvider(),
            FakeWeatherProvider(),
            FakeRoutesProvider(),
            reference_date=date(2026, 9, 11),
            tracer=tracer,
        )
    )
    run_metadata = json.loads((tracer.run_directory / "run.json").read_text(encoding="utf-8"))

    assert result.system_version.value == "v1"
    assert run_metadata["run_id"] == str(RUN_ID)
    assert run_metadata["system_stage"] == "v1-a"
    assert run_metadata["status"] == "completed"
    assert run_metadata["requested_trip_dates"] == {
        "start": "2026-09-12",
        "end": "2026-09-13",
    }
    assert run_metadata["tool_usage"]["destination_search_calls"]["used"] == 1
    assert run_metadata["tool_usage"]["candidate_search_calls"]["used"] == 3
    assert run_metadata["final_outcome"]["system_version"] == "v1"
    assert len(list((tracer.run_directory / "evidence").glob("*.json"))) == 4
    assert list((tracer.run_directory / "evidence").glob("*nearby_reference_ledger.json"))
    assert not (tracer.run_directory / "error.json").exists()


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


def test_trace_write_failure_does_not_change_planning_semantics(tmp_path, monkeypatch) -> None:
    tracer = FileRunTracer(_context(), root=tmp_path, payload_mode=TracePayloadMode.METADATA)

    def fail_open(self, *args, **kwargs):
        raise OSError("simulated trace failure")

    monkeypatch.setattr(Path, "open", fail_open)

    result = asyncio.run(
        run_v1(
            make_request(additional_preferences="Plan two days in Sydney."),
            FakeStructuredLLMClient([make_extraction(), make_itinerary()]),
            FakePlacesProvider(),
            FakeWeatherProvider(),
            FakeRoutesProvider(),
            reference_date=date(2026, 9, 11),
            tracer=tracer,
        )
    )

    assert result.system_version.value == "v1"


def test_quality_token_counters_remain_numeric_but_credentials_stay_redacted():
    from backend.app.observability.run_trace import redact_secrets

    fields = (
        "framing_tokens",
        "total_query_tokens",
        "system_tokens",
        "user_tokens",
        "schema_tokens",
    )
    assert redact_secrets(dict.fromkeys(fields, 2048)) == dict.fromkeys(fields, 2048)
    assert redact_secrets(dict.fromkeys(fields, "credential")) == dict.fromkeys(
        fields, "[REDACTED]"
    )
    assert redact_secrets({"api_key": "secret", "access_token": 123}) == {
        "api_key": "[REDACTED]",
        "access_token": "[REDACTED]",
    }
