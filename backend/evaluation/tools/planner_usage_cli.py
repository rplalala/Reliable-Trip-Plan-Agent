"""Opt-in development execution/capture; preparation is offline unless --execute is supplied."""

import argparse
import asyncio
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from dotenv import load_dotenv

from backend.app.observability.usage import usage_stage
from backend.app.observability.usage_capture import capture_attempt
from backend.app.policies.trip_dates import SystemDateProvider
from backend.app.runtime.config_loader import load_runtime_config_file, runtime_config_snapshot
from backend.app.services.planner_runtime import RequestPlannerRuntime
from backend.app.services.preference_interpretation import (
    read_planning_request,
    validate_planning_request,
)
from backend.app.versions.v1.runner import serialize_planning_result
from backend.evaluation.cost_report import build_cost_report, read_source
from backend.evaluation.usage_report import summarize

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

    def sink(usage):
        captured.append(usage)
        _save(output, "usage.json", usage)

    async def invoke():
        with usage_stage("planner"):
            value = await selected.run(args.version, request, reference_date=reference_date)
        if str(value.system_version) != args.version:
            raise ValueError("Selected planner returned a different version")
        for field in ("destination", "start_date", "end_date", "traveler_count", "budget"):
            if getattr(value.requirements, field) != getattr(request, field):
                raise ValueError("Selected planner returned different structured trip facts")
        return value

    try:
        value = asyncio.run(
            capture_attempt(
                invoke,
                group_id=args.group_id,
                run_id=args.run_id,
                version=args.version,
                sink=sink,
                serialize=serialize_planning_result,
                adapter_coverage="default_adapters" if runtime is None else "unverified",
            ),
            loop_factory=asyncio.SelectorEventLoop if sys.platform == "win32" else None,
        )
        (output / "result.json").write_bytes(serialize_planning_result(value).encode("utf-8"))
    except (Exception, asyncio.CancelledError, KeyboardInterrupt) as exc:
        failure = type(exc).__name__
        _save(output, "failure.json", {"error_type": failure})
    if not captured or not (output / "usage.json").is_file():
        manifest.update(status="capture_failed", failure_type=failure)
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
