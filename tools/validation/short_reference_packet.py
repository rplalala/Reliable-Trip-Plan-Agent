"""Freeze, verify and launch the authorized six-case development smoke packet."""

import argparse
import asyncio
import hashlib
import json
import subprocess
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path
from time import monotonic

import httpx

from backend.app.llm.reference_transport import (
    primary_references,
    profile_references,
    repair_references,
)
from backend.evaluation.identity_assistance import IdentityAssistancePacket
from backend.model_references import ShortReferences
from tools.validation.short_reference_cases import (
    mock_output,
    prepared_cases,
    primary_prompt,
    repair_prompt,
)
from tools.validation.short_reference_smoke import SmokeCase, SmokeRunner, digest, save

ROOT = Path(__file__).resolve().parents[2]
LIMITS = {
    "model": "gpt-6-luna",
    "max_model_sends": 6,
    "retries": 0,
    "google_sends": 0,
    "tools": 0,
    "input_estimate_cap": 10000,
    "output_cap": 4000,
    "request_timeout_seconds": 60,
    "total_seconds": 600,
    "retail_estimate_budget_usd": 0.05,
}
PACKAGES = ("openai", "langchain-openai", "langchain-core", "httpx", "pydantic", "tiktoken")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_versions():
    return {name: version(name) for name in PACKAGES}


def case_references(case):
    if case.name == "shared_primary":
        return primary_references(primary_prompt(case.payload))[0]
    if case.name == "review_profile":
        return profile_references(json.dumps(case.payload))[0]
    if case.name == "v3_repair":
        return repair_references(repair_prompt(case.payload))[0]
    if case.name == "v0_identity":
        return IdentityAssistancePacket(case.payload["cases"]).references
    if case.name == "product_introduction":
        return ShortReferences(
            case.payload["original"]["days"][0]["activities"], {"activity_id": "a"}
        )
    from backend.app.evidence.official_models import EvidenceSourceBlock

    source = EvidenceSourceBlock.model_validate(case.payload["source"])
    return ShortReferences(
        {
            "place_id": case.payload["task"]["place_id"],
            "task_id": source.task_id,
            "source_key": source.source_key,
        },
        {"place_id": "p", "source_key": "s", "task_id": "t"},
    )


def mock_sdk_response(output):
    return {
        "id": "resp_preflight",
        "object": "response",
        "created_at": 1791150000,
        "status": "completed",
        "model": "gpt-6-luna",
        "output": [
            {
                "id": "msg_preflight",
                "type": "message",
                "role": "assistant",
                "status": "completed",
                "content": [{"type": "output_text", "text": json.dumps(output), "annotations": []}],
            }
        ],
        "usage": {
            "input_tokens": 120,
            "output_tokens": 40,
            "total_tokens": 160,
            "input_tokens_details": {"cached_tokens": 0},
            "output_tokens_details": {"reasoning_tokens": 0},
        },
    }


async def prepare_packet(directory, judge_input, *, source_hashes, revision, endpoint):
    directory = Path(directory)
    if directory.exists() and any(directory.iterdir()):
        raise ValueError("Packet directory must be new or empty")
    cases = prepared_cases(judge_input)
    index = 0

    def respond(request):
        nonlocal index
        output = mock_output(cases[index])
        index += 1
        return httpx.Response(200, json=mock_sdk_response(output))

    runner = SmokeRunner(
        endpoint=endpoint,
        api_key="unused-preflight-key",
        transport=httpx.MockTransport(respond),
        directory=directory / "mock",
    )
    report = await runner.run(cases)
    if report["status"] != "completed" or report["model_sends"] != 6:
        raise ValueError("Six-case SDK preflight failed: " + report.get("error_type", "coverage"))
    requests = {a["case"]: a["request"] for a in report["attempts"]}
    maps = {case.name: case_references(case).manifest for case in cases}
    result = {
        "status": "ready",
        "mock_sends": 6,
        "live_sends": 0,
        "request_hashes": {name: digest(body) for name, body in requests.items()},
        "mapping_hashes": {name: digest(mapping) for name, mapping in maps.items()},
        "input_estimates": {
            a["case"]: a["estimated_input_tokens_with_reserve"] for a in report["attempts"]
        },
        "retail_estimate_usd_at_caps": 0.018,
    }
    for name, data in [
        ("cases.json", [asdict(case) for case in cases]),
        ("requests.json", requests),
        ("reference-maps.json", maps),
        ("preflight.json", result),
    ]:
        save(directory, name, data)
    manifest = {
        "issue": 66,
        "code_revision": revision,
        "limits": LIMITS,
        "endpoint_sha256": hashlib.sha256(endpoint.rstrip("/").encode()).hexdigest(),
        "packages": package_versions(),
        "source_hashes": source_hashes,
        "file_hashes": {
            name: sha(directory / name)
            for name in ("cases.json", "requests.json", "reference-maps.json", "preflight.json")
        },
    }
    save(directory, "manifest.json", manifest)
    return result


def validate_packet(directory, *, revision, endpoint):
    directory = Path(directory).resolve()
    manifest = read(directory / "manifest.json")
    if manifest["code_revision"] != revision or manifest["limits"] != LIMITS:
        raise ValueError("Frozen revision or limits changed")
    if manifest["endpoint_sha256"] != hashlib.sha256(endpoint.rstrip("/").encode()).hexdigest():
        raise ValueError("Model endpoint changed")
    if manifest["packages"] != package_versions():
        raise ValueError("SDK dependency versions changed")
    for owner, hashes in [(directory, manifest["file_hashes"]), (ROOT, manifest["source_hashes"])]:
        for name, expected in hashes.items():
            path = (owner / name).resolve()
            if not path.is_relative_to(owner) or not path.is_file() or sha(path) != expected:
                raise ValueError("Frozen file changed: " + name)
    cases = [SmokeCase(**data) for data in read(directory / "cases.json")]
    if [c.name for c in cases] != [c.name for c in prepared_cases({"cases": []})]:
        raise ValueError("Frozen case coverage changed")
    maps = read(directory / "reference-maps.json")
    if maps != {case.name: case_references(case).manifest for case in cases}:
        raise ValueError("Frozen reference map changed")
    return cases, read(directory / "preflight.json")


async def execute_packet(directory, *, revision, endpoint, api_key, transport=None):
    started = monotonic()
    directory = Path(directory)
    cases, preflight = validate_packet(directory, revision=revision, endpoint=endpoint)
    authorization = read(directory / "execution-authorization.json")
    if (
        authorization.get("status") != "user_authorized"
        or authorization.get("issue") != 66
        or authorization.get("limits") != LIMITS
        or authorization.get("manifest_sha256") != sha(directory / "manifest.json")
    ):
        raise ValueError("Explicit execution authorization is missing or changed")
    with (directory / "launch.json").open("x", encoding="utf-8") as launch:
        json.dump({"issue": 66, "code_revision": revision, "retries": 0}, launch)
    runner = SmokeRunner(
        endpoint=endpoint,
        api_key=api_key,
        transport=transport if transport is not None else httpx.AsyncHTTPTransport(retries=0),
        directory=directory / "live",
        frozen_requests=preflight["request_hashes"],
    )
    report = await asyncio.wait_for(
        runner.run(cases), timeout=max(0.001, 600 - (monotonic() - started))
    )
    report["mode"] = "live" if transport is None else "injected_http_boundary"
    report["elapsed_seconds"] = monotonic() - started
    report["original_sources_unchanged"] = True
    try:
        validate_packet(directory, revision=revision, endpoint=endpoint)
    except ValueError:
        report.update(
            status="stopped",
            original_sources_unchanged=False,
            stop_reason="Frozen source changed during execution",
        )
    save(directory / "live", "execution.json", report)
    return report


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def main():
    from backend.app.versions.v0.config import V0Settings

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "preflight", "execute"))
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--judge-input", type=Path)
    parser.add_argument("--source-authorization", type=Path)
    args = parser.parse_args()
    directory = args.directory.resolve()
    if not directory.is_relative_to(ROOT / "artifacts"):
        raise ValueError("Execution packet must be under repository artifacts")
    if git("status", "--porcelain"):
        raise ValueError("Tracked worktree must be clean before packet preparation or execution")
    settings = V0Settings()
    endpoint = str(settings.azure_openai_endpoint)
    url = httpx.URL(endpoint)
    if (
        settings.azure_openai_deployment != "gpt-6-luna"
        or url.scheme != "https"
        or url.path.rstrip("/") != "/openai/v1"
        or url.query
        or url.userinfo
    ):
        raise ValueError("Expected the configured GPT-6 Luna Foundry v1 deployment")
    revision = git("rev-parse", "HEAD")
    if args.operation == "prepare":
        if args.judge_input is None or args.source_authorization is None:
            raise ValueError("Preparation requires original judge input and source authorization")
        hashes = read(args.source_authorization)["file_hashes"].copy()
        for name, expected in hashes.items():
            if sha(ROOT / name) != expected:
                raise ValueError("Original frozen source changed: " + name)
        for name in git("ls-files").splitlines():
            if name.endswith(".py") or name in ("config/runtime.yaml", "pyproject.toml", "uv.lock"):
                hashes[name] = sha(ROOT / name)
        for path in (args.judge_input.resolve(), args.source_authorization.resolve()):
            hashes[path.relative_to(ROOT).as_posix()] = sha(path)
        result = asyncio.run(
            prepare_packet(
                directory,
                read(args.judge_input),
                source_hashes=hashes,
                revision=revision,
                endpoint=endpoint,
            )
        )
    elif args.operation == "preflight":
        _, result = validate_packet(directory, revision=revision, endpoint=endpoint)
    else:
        result = asyncio.run(
            execute_packet(
                directory,
                revision=revision,
                endpoint=endpoint,
                api_key=settings.azure_openai_api_key.get_secret_value(),
            )
        )
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "mock_sends",
                    "live_sends",
                    "model_sends",
                    "elapsed_seconds",
                    "stop_reason",
                )
                if key in result
            }
        )
    )
    if result["status"] not in ("ready", "completed"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
