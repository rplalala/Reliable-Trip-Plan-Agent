"""Opt-in, one-case V3 acceptance with normalized requirement-failure evidence."""

import argparse
import contextlib
import hashlib
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from unittest.mock import patch
from uuid import uuid4

import yaml

from backend.app.runtime.config_loader import DEFAULT_RUNTIME_CONFIG_PATH, load_runtime_config_file
from backend.app.schemas.interpreted_requirements import InterpretationDraft
from backend.app.services.preference_prompts import PREFERENCE_INTERPRETATION_SYSTEM_PROMPT
from backend.app.services.product_evidence import ProductEvidenceCollector
from backend.app.services.product_presentation import present_product
from backend.app.versions.v1 import runner
from backend.app.versions.v3.runner import main as v3_main
from backend.app.versions.v3.state import V3PlanningResult
from tools.validation.repair_replay import CapturedRepair
from tools.validation.requirement_capture import DevelopmentRequirementCapture


def write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=True, indent=2)


@contextlib.contextmanager
def case_logging():
    """Keep CLI-created handlers from retaining a closed per-case stderr stream."""
    root = logging.getLogger()
    handlers, level = root.handlers.copy(), root.level
    try:
        yield
    finally:
        for handler in root.handlers.copy():
            if handler not in handlers:
                root.removeHandler(handler)
                handler.close()
        root.handlers = handlers
        root.setLevel(level)


class CapturedRequirements:
    """Borrow a CLI-owned client; observe normalized drafts without changing decisions."""

    def __init__(self, client, directory, metadata, errors):
        self.client, self.metadata, self.errors = client, metadata, errors
        self.capture = None
        try:
            self.capture = DevelopmentRequirementCapture(
                directory,
                scenario_id=metadata["case_id"],
                secrets=getattr(client, "_capture_secrets", ()),
            )
        except Exception as exc:
            self.errors.append(type(exc).__name__)

    def __getattr__(self, name):
        return getattr(self.client, name)

    def record(self, call_id, stage, payload):
        if self.capture is None:
            return
        try:
            saved = self.capture.record(
                call_id,
                stage,
                {
                    **self.metadata,
                    "prompt_version": getattr(self.client, "last_call_metadata", {}).get(
                        "prompt_version"
                    ),
                    **payload,
                },
            )
            if saved is None:
                self.errors.append("artifact_write_failed")
        except Exception as exc:
            self.errors.append(type(exc).__name__)

    async def generate_structured(self, **kwargs):
        if kwargs["response_schema"] is not InterpretationDraft:
            return await self.client.generate_structured(**kwargs)
        try:
            draft = await self.client.generate_structured(**kwargs)
        except Exception as exc:
            metadata = getattr(self.client, "last_call_metadata", {})
            self.record(
                metadata.get("call_id") or uuid4().hex,
                "interpretation_error",
                {
                    "outcome": exc.as_dict()
                    if hasattr(exc, "as_dict")
                    else {
                        "error_type": type(exc).__name__,
                    },
                    "provider_diagnostics": metadata.get("provider_diagnostics"),
                },
            )
            raise
        self.record(
            draft._diagnostic_call_id,
            "draft_validated",
            {
                "draft": draft.model_dump(mode="json"),
            },
        )
        return draft

    def capture_requirement_outcome(self, draft, error=None):
        self.record(
            draft._diagnostic_call_id,
            "canonicalization",
            {
                "outcome": {"status": "validated"}
                if error is None
                else (
                    error.as_dict()
                    if hasattr(error, "as_dict")
                    else {
                        "error_type": type(error).__name__,
                    }
                ),
            },
        )
        self.client.capture_requirement_outcome(draft, error)


class CapturedSemantics:
    """Opt-in normalized semantic capture: 1 MiB per stage, 4 MiB per case."""

    def __init__(self, client, directory, metadata, errors):
        self.client, self.metadata, self.errors = client, metadata, errors
        self.remaining_bytes = 4 * 1024 * 1024
        self.capture = None
        try:
            self.capture = DevelopmentRequirementCapture(
                directory,
                scenario_id=metadata.get("case_id", "development"),
                secrets=getattr(client, "_capture_secrets", ()),
            )
        except Exception as exc:
            self.errors.append("semantic_capture_" + type(exc).__name__)

    def __getattr__(self, name):
        return getattr(self.client, name)

    def capture_poi_semantics(self, stage, payload):
        if self.capture is None:
            return
        limit = min(1024 * 1024, self.remaining_bytes)
        try:
            body = self.metadata | payload
            saved = self.capture.record(
                payload["call_id"],
                "semantic_" + stage,
                body,
                max_bytes=limit,
            )
            if saved is None:
                # A partial file may remain; conservatively charge the attempted maximum.
                self.remaining_bytes -= limit
                self.errors.append("semantic_artifact_write_failed")
            else:
                self.remaining_bytes -= saved.stat().st_size
        except OverflowError:
            self.errors.append("semantic_capture_limit")
        except Exception as exc:
            self.remaining_bytes -= limit
            self.errors.append("semantic_capture_" + type(exc).__name__)


def run_case(
    input_json,
    output,
    *,
    runtime_config=DEFAULT_RUNTIME_CONFIG_PATH,
    capture_requirements=False,
    capture_semantics=False,
    capture_repair=False,
    repair_quantity_review=None,
    reference_date=None,
):
    """Run once in a fresh directory. Application exit status is never rewritten."""
    output = Path(output)
    config_path = Path(runtime_config)
    config = load_runtime_config_file(config_path)
    request = runner.read_planning_request(str(input_json))
    output.mkdir(parents=True, exist_ok=False)
    case_id = uuid4().hex
    write_json(
        output / "started.json",
        {
            "case_id": case_id,
            "started_at": datetime.now(UTC).isoformat(),
        },
    )
    write_json(output / "request.json", request.model_dump(mode="json"))
    metadata = {
        "case_id": case_id,
        "request_budget_seconds": config.development_timeout_seconds,
        "prompt_sha256": hashlib.sha256(
            PREFERENCE_INTERPRETATION_SYSTEM_PROMPT.encode("utf-8")
        ).hexdigest(),
        "runtime_config_sha256": hashlib.sha256(config_path.read_bytes()).hexdigest(),
        "input_sha256": hashlib.sha256(request.model_dump_json().encode("utf-8")).hexdigest(),
    }
    write_json(
        output / "manifest.json",
        metadata
        | {
            "capture_requirements": capture_requirements,
            "capture_semantics": capture_semantics,
            "capture_repair": capture_repair,
            "repair_quantity_review": repair_quantity_review,
            "quantity_review_source": "runtime.yaml"
            if repair_quantity_review is None
            else "explicit_override",
            "reference_date": reference_date,
            "development_timeout_seconds": config.development_timeout_seconds,
        },
    )
    effective = config.model_dump(mode="json")
    effective["trace"]["directory"] = str(output.resolve() / "trace")
    effective_path = output / "runtime.yaml"
    effective_path.write_text(yaml.safe_dump(effective, sort_keys=False), encoding="utf-8")
    errors, semantic_errors, collectors = [], [], []
    repair_errors, repair_captures = [], []
    create_client, create_trace = runner.create_foundry_client, runner.create_run_tracer

    def captured_client(settings):
        client = create_client(settings)
        if capture_repair:
            client = CapturedRepair(client, output / "repair", metadata, repair_errors)
            repair_captures.append(client)
        if capture_semantics:
            client = CapturedSemantics(client, output / "semantics", metadata, semantic_errors)
        return (
            CapturedRequirements(client, output / "requirements", metadata, errors)
            if capture_requirements
            else client
        )

    def captured_trace(*args, **kwargs):
        collector = ProductEvidenceCollector(create_trace(*args, **kwargs))
        collectors.append(collector)
        return collector

    argv = [
        "--input-json",
        str(output / "request.json"),
        "--runtime-config",
        str(effective_path),
        "--development-timeout-seconds",
        str(config.development_timeout_seconds),
    ]
    if reference_date:
        argv.extend(["--reference-date", str(reference_date)])
    if repair_quantity_review is not None:
        argv.append(
            "--repair-quantity-review" if repair_quantity_review else "--no-repair-quantity-review"
        )
    started = monotonic()
    with (
        (output / "result.json").open("x", encoding="utf-8") as stdout,
        (output / "stderr.log").open("x", encoding="utf-8") as stderr,
        contextlib.redirect_stdout(stdout),
        contextlib.redirect_stderr(stderr),
        patch.object(runner, "create_foundry_client", captured_client),
        patch.object(runner, "create_run_tracer", captured_trace),
        case_logging(),
    ):
        code = v3_main(argv)
    trace_directories = [
        str(directory)
        for collector in collectors
        if (directory := getattr(collector.tracer, "run_directory", None)) is not None
    ]
    trace_available = (
        bool(collectors)
        and len(trace_directories) == len(collectors)
        and not any(getattr(collector.tracer, "_failed", False) for collector in collectors)
    )
    if config.trace.enabled and not trace_available:
        errors.append("trace_unavailable")
    if capture_repair and not any(c.attempted for c in repair_captures):
        repair_errors.append("repair_snapshot_not_reached")
    status = {
        "application_exit_code": code,
        "elapsed_seconds": monotonic() - started,
        "capture_status": "disabled"
        if not capture_requirements
        else ("incomplete" if errors else "complete"),
        "capture_errors": errors,
        "semantic_capture_status": "disabled"
        if not capture_semantics
        else ("incomplete" if semantic_errors else "complete"),
        "semantic_capture_errors": semantic_errors,
        "repair_capture_status": "disabled"
        if not capture_repair
        else ("incomplete" if repair_errors else "complete"),
        "repair_capture_errors": repair_errors,
        "acceptance_status": "execution_failed" if code else "completed_pending_review",
        "trace_directories": trace_directories,
        "trace_status": "disabled"
        if not config.trace.enabled
        else ("available" if trace_available else "unavailable"),
    }
    if code == 0:
        result = V3PlanningResult.model_validate_json(
            (output / "result.json").read_text(encoding="utf-8")
        )
        write_json(
            output / "product.json", present_product(result, collectors[0]).model_dump(mode="json")
        )
    if errors or semantic_errors or repair_errors:
        status["acceptance_status"] = "evidence_incomplete"
    write_json(output / "execution.json", status)
    return status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-json", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--runtime-config", type=Path, default=DEFAULT_RUNTIME_CONFIG_PATH)
    parser.add_argument("--rag-env-file", type=Path)
    parser.add_argument("--capture-requirements", action="store_true")
    parser.add_argument("--capture-semantics", action="store_true")
    parser.add_argument("--capture-repair", action="store_true")
    parser.add_argument(
        "--repair-quantity-review", action=argparse.BooleanOptionalAction, default=None
    )
    parser.add_argument("--execute", action="store_true", help="Explicitly run one live case")
    args = parser.parse_args()
    if not args.execute:
        parser.error("Execution requires --execute and separate user authorization")
    if args.rag_env_file:
        from dotenv import load_dotenv

        load_dotenv(args.rag_env_file, override=False)
    result = run_case(
        args.input_json,
        args.output,
        runtime_config=args.runtime_config,
        capture_requirements=args.capture_requirements,
        capture_semantics=args.capture_semantics,
        capture_repair=args.capture_repair,
        repair_quantity_review=args.repair_quantity_review,
    )
    print(json.dumps(result))
    return result["application_exit_code"] or (
        3
        if result["capture_errors"]
        or result["semantic_capture_errors"]
        or result["repair_capture_errors"]
        else 0
    )


if __name__ == "__main__":
    sys.exit(main())
