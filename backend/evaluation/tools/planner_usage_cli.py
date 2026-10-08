"""Opt-in development execution/capture; preparation is offline unless --execute is supplied."""

import argparse
import asyncio
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv

from backend.app.observability.mechanism_capture import capture_attempt as capture_mechanism
from backend.app.observability.raw_capture import capture_raw
from backend.app.observability.run_trace import FileRunTracer, RunTraceContext, TracePayloadMode
from backend.app.observability.usage import usage_stage
from backend.app.observability.usage_capture import capture_attempt
from backend.app.policies.trip_dates import SystemDateProvider, create_trip_date_window
from backend.app.runtime.config_loader import load_runtime_config_file, runtime_config_snapshot
from backend.app.services.planner_runtime import RequestPlannerRuntime
from backend.app.services.preference_interpretation import (
    read_planning_request,
    validate_planning_request,
)
from backend.app.versions.v1.runner import serialize_planning_result
from backend.evaluation.cost_report import build_cost_report, read_source
from backend.evaluation.usage_report import summarize

from .generation_evidence import build_evidence_index, finish_trace_if_running
from .reference_prices import build_reference_prices, reference_basis

ROOT = Path(__file__).resolve().parents[3]


def _save(directory, name, value):
    (directory / name).write_bytes(
        (json.dumps(value, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
    )


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None, *, runtime=None, date_provider=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, choices=["v0", "v1", "v2", "v3"])
    parser.add_argument("--input-json", required=True, type=Path)
    parser.add_argument("--runtime-config", type=Path, default=ROOT / "config/runtime.yaml")
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env")
    parser.add_argument("--rag-env-file", type=Path)
    parser.add_argument("--output-directory", required=True, type=Path)
    parser.add_argument("--group-id", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument(
        "--capture-evidence",
        action="store_true",
        help="Capture credential-filtered HTTP and mechanism evidence locally",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Invoke the real selected planner; requires separately authorized live execution",
    )
    args = parser.parse_args(argv)
    reference_date = (date_provider or SystemDateProvider()).today()
    request = validate_planning_request(read_planning_request(args.input_json), reference_date)
    config = load_runtime_config_file(args.runtime_config)
    snapshot, policy_hash = runtime_config_snapshot(config)
    output = args.output_directory.resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "input.json").write_bytes(args.input_json.read_bytes())
    (output / "runtime.yaml").write_bytes(args.runtime_config.read_bytes())
    _save(output, "runtime-policy.json", {"configuration": snapshot, "sha256": policy_hash})
    _save(output, "price-basis.json", reference_basis())
    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = None
    manifest = {
        "kind": "development_planner_usage_capture",
        "version": args.version,
        "group_id": args.group_id,
        "run_id": args.run_id,
        "source_revision": revision,
        "input_sha256": _sha(output / "input.json"),
        "runtime_config_sha256": _sha(output / "runtime.yaml"),
        "runtime_policy_sha256": policy_hash,
        "reference_date": str(reference_date),
        "prepared_at": datetime.now(UTC).isoformat(),
        "execution_requested": args.execute,
        "evidence_requested": args.capture_evidence,
        "status": "prepared",
        "qualified_four_version_batch": False,
        "scope": (
            "One original selected-version generation; "
            "no independent evaluator requests or hard spend guard."
        ),
    }
    _save(output, "manifest.json", manifest)
    if not args.execute:
        print(
            json.dumps({"status": "prepared", "output_directory": str(output), "provider_sends": 0})
        )
        return 0
    if args.rag_env_file:
        load_dotenv(args.rag_env_file, override=False)
    load_dotenv(args.env_file, override=False)
    selected = runtime or RequestPlannerRuntime(config=config)
    captured = []
    failure = None
    tracer = None

    def sink(usage):
        captured.append(usage)
        _save(output, "usage.json", usage)

    async def invoke():
        with usage_stage("planner"):
            trace_options = {"tracer": tracer} if tracer is not None else {}
            value = await selected.run(
                args.version, request, reference_date=reference_date, **trace_options
            )
        if str(value.system_version) != args.version:
            raise ValueError("Selected planner returned a different version")
        for field in ("destination", "start_date", "end_date", "traveler_count", "budget"):
            if getattr(value.requirements, field) != getattr(request, field):
                raise ValueError("Selected planner returned different structured trip facts")
        return value

    raw = None

    async def captured_invoke():
        return await capture_attempt(
            invoke,
            group_id=args.group_id,
            run_id=args.run_id,
            version=args.version,
            sink=sink,
            serialize=serialize_planning_result,
            adapter_coverage="default_adapters" if runtime is None else "unverified",
        )

    async def execute():
        nonlocal raw, tracer
        if not args.capture_evidence:
            return await captured_invoke()
        with capture_raw(output) as raw:
            tracer = FileRunTracer(
                RunTraceContext(
                    run_id=uuid4(),
                    system_version=args.version,
                    reference_date=reference_date,
                    date_window=create_trip_date_window(reference_date),
                    request=request,
                    started_at=datetime.now(UTC),
                    runtime_config=snapshot,
                    runtime_config_sha256=policy_hash,
                ),
                root=output / "evidence/trace",
                payload_mode=TracePayloadMode.RAW,
                max_payload_bytes=config.trace.max_payload_bytes,
            )
            try:
                return await capture_mechanism(
                    captured_invoke,
                    group_id=args.group_id,
                    run_id=args.run_id,
                    version=args.version,
                    input_sha256=manifest["input_sha256"],
                    serialize=serialize_planning_result,
                    sink=lambda value: _save(output, "mechanism.json", value),
                )
            finally:
                # V1-V3 own normal trace completion; retain their tool usage and outcome.
                finish_trace_if_running(tracer, captured[-1] if captured else None)

    try:
        value = asyncio.run(
            execute(),
            loop_factory=asyncio.SelectorEventLoop if sys.platform == "win32" else None,
        )
        (output / "result.json").write_bytes(serialize_planning_result(value).encode("utf-8"))
    except (Exception, asyncio.CancelledError, KeyboardInterrupt) as exc:
        failure = type(exc).__name__
        _save(output, "failure.json", {"error_type": failure})
    if not captured or not (output / "usage.json").is_file():
        manifest.update(status="capture_failed", failure_type=failure)
        if args.capture_evidence:
            _save(
                output,
                "evidence-index.json",
                build_evidence_index(
                    output,
                    manifest,
                    raw,
                    captured[-1] if captured else {"outcome": "incomplete"},
                    adapter_coverage="default_adapters" if runtime is None else "unverified",
                ),
            )
        _save(output, "manifest.json", manifest)
        return 1
    source = read_source(output / "usage.json")
    prices = build_reference_prices([source])
    _save(output, "prices.json", prices)
    _save(output, "usage-summary.json", summarize(source["usage"]))
    _save(output, "cost-report.json", build_cost_report([source], prices))
    manifest.update(
        status="failed" if failure else "completed",
        failure_type=failure,
        usage_sha256=_sha(output / "usage.json"),
    )
    if args.capture_evidence:
        _save(
            output,
            "evidence-index.json",
            build_evidence_index(
                output,
                manifest,
                raw,
                captured[-1],
                adapter_coverage="default_adapters" if runtime is None else "unverified",
            ),
        )
    if (output / "result.json").is_file():
        result_sha = _sha(output / "result.json")
        _save(
            output,
            "provenance.json",
            {
                "schema_version": "rtpeval_provenance_1",
                "group_id": args.group_id,
                "run_id": args.run_id,
                "version": args.version,
                "input_sha256": manifest["input_sha256"],
                "result_sha256": result_sha,
                "source_revision": revision,
                "configuration_ref": {
                    "path": "runtime-policy.json",
                    "sha256": _sha(output / "runtime-policy.json"),
                    "media_type": "application/json",
                    "availability": "available",
                },
                **(
                    {
                        "evidence_index_ref": {
                            "path": "evidence-index.json",
                            "sha256": _sha(output / "evidence-index.json"),
                        },
                        "mechanism_ref": {
                            "path": "mechanism.json",
                            "sha256": _sha(output / "mechanism.json"),
                        }
                        if (output / "mechanism.json").is_file()
                        else None,
                    }
                    if args.capture_evidence
                    else {}
                ),
                "scope": (
                    "Development capture only; "
                    "producer completion and batch qualification are separate."
                ),
            },
        )
        manifest["result_sha256"] = result_sha
    _save(output, "manifest.json", manifest)
    print(json.dumps({"status": manifest["status"], "output_directory": str(output)}))
    return 1 if failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
