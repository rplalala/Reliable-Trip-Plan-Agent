"""Prepare and execute one explicitly approved development identity judgment."""

import argparse
import asyncio
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import httpx
from openai import AsyncOpenAI

from backend.app.runtime.token_counting import count_tokens
from backend.evaluation.identity import resolve_identities
from backend.evaluation.identity_adoption import load_v0_material
from backend.evaluation.identity_llm import (
    RESULT_VERSION,
    prepare_identity_judgment,
)
from backend.evaluation.records import canonical_digest, text, thaw

MODEL = "gpt-6-luna"
LIMITS = {
    "max_sends": 1,
    "max_retries": 0,
    "max_input_tokens": 18000,
    "input_token_reserve": 1024,
    "max_output_tokens": 3000,
    "http_timeout_seconds": 60,
    "retail_reference_allowance_usd": 0.0042,
}
PRICING = {
    "checked_on": "2026-10-06",
    "source": "https://developers.openai.com/api/docs/models/gpt-6-luna",
    "input_per_million_usd": 0.10,
    "cached_input_per_million_usd": 0.01,
    "cache_write_per_million_usd": 0.125,
    "output_per_million_usd": 0.50,
    "cache_source": "https://developers.openai.com/api/docs/guides/prompt-caching",
    "usage_categories": {
        "input": "input_tokens minus cached_tokens and cache_write_tokens",
        "cached_input": "input_tokens_details.cached_tokens",
        "cache_write": "input_tokens_details.cache_write_tokens",
        "output": "output_tokens, including reasoning; never add reasoning again",
    },
    "regional_multiplier_scenario": 1.10,
    "basis": "Standard retail reference; regional +10% scenario; Foundry invoice unavailable.",
}


def save(directory, name, value):
    (directory / name).write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _plan(bundle_path, endpoint, directory, protected_files):
    bundle_path, directory = Path(bundle_path).resolve(), Path(directory).resolve()
    url = httpx.URL(endpoint)
    if url.scheme != "https" or url.username or url.password or url.query or url.fragment:
        raise ValueError("An HTTPS endpoint without credentials/query/fragment is required")
    endpoint = str(url).rstrip("/") + "/"
    material = load_v0_material(None, bundle_path)
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    sources = {str(bundle_path): file_digest(bundle_path), **protected_files}
    root = (bundle_path.parent / bundle["artifact_root"]).resolve()
    for ref in bundle["artifacts"].values():
        if ref is not None:
            sources[str((root / ref["path"]).resolve())] = ref["sha256"]
    if any(file_digest(path) != sha for path, sha in sources.items()):
        raise ValueError("Frozen source hash mismatch")
    packet = prepare_identity_judgment(
        thaw(material.intake), thaw(material.evidence), model=MODEL
    ).to_dict()
    wire = {
        **packet["request"],
        "max_output_tokens": LIMITS["max_output_tokens"],
        "reasoning": {"effort": "low"},
        "store": False,
    }
    estimated = count_tokens(json.dumps(wire, ensure_ascii=False)) + LIMITS["input_token_reserve"]
    if estimated > LIMITS["max_input_tokens"]:
        raise ValueError("Estimated input exceeds smoke allowance")
    cases = json.loads(wire["input"])["cases"]
    maximum = (
        LIMITS["max_input_tokens"] * PRICING["cache_write_per_million_usd"]
        + LIMITS["max_output_tokens"] * PRICING["output_per_million_usd"]
    ) / 1000000
    repository = Path(__file__).resolve().parents[2]
    implementation = [
        Path(__file__).resolve(),
        repository / "backend/model_references.py",
        repository / "backend/app/runtime/token_counting.py",
        repository / "pyproject.toml",
        repository / "uv.lock",
        *sorted((repository / "backend/evaluation").glob("*.py")),
    ]
    return {
        "schema_version": "rtpeval_identity_smoke_preparation_2",
        "implementation_hashes": {str(path): file_digest(path) for path in implementation},
        "bundle_path": str(bundle_path),
        "endpoint": endpoint,
        "execution_directory": str(directory / "execution"),
        "protected_files": protected_files,
        "source_hashes": sources,
        "packet": packet,
        "wire_request": wire,
        "wire_request_sha256": canonical_digest(wire),
        "limits": dict(LIMITS),
        "pricing": dict(PRICING),
        "reference_count": len(cases),
        "data_scope": {
            "versions": sorted({c["version"] for c in cases}),
            "kinds": sorted({c["kind"] for c in cases}),
            "reference_count": len(cases),
            "candidate_count": sum(len(c["candidates"]) for c in cases),
            "original_addresses_missing": sum(not text(c["claim"]["location"]) for c in cases),
        },
        "request_counts": {"model": 1, "google": 0, "planner": 0, "routes": 0},
        "execution_gate": {
            "status": "awaiting_new_exact_plan_approval",
            "historical_allowance_reused": False,
            "current_session_child_required": True,
            "child_model": "gpt-6.1-sol",
            "child_reasoning_effort": "medium",
        },
        "estimated_input_tokens_with_reserve": estimated,
        "maximum_standard_retail_reference_usd": maximum,
        "maximum_regional_retail_reference_usd": maximum * PRICING["regional_multiplier_scenario"],
        "preparation": {"actual_sends": 0, "incremental_charges_usd": 0},
    }


def prepare_smoke(bundle_path, *, endpoint, directory, protected_files=None):
    """Freeze verified sources and an exact SDK request without credentials or sends."""
    protected = {str(Path(p).resolve()): sha for p, sha in (protected_files or {}).items()}
    plan = _plan(bundle_path, endpoint, directory, protected)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    save(directory, "preparation.json", plan)
    material = load_v0_material(None, bundle_path)
    pending = resolve_identities(thaw(material.intake), thaw(material.evidence)).to_dict()
    save(directory, "pending-identity-report.json", pending)
    (directory / "handoff.md").write_text(_handoff(plan), encoding="utf-8")
    return plan


def _handoff(plan):
    """Private, reviewable instructions; the frozen manifest never grants execution."""
    directory = Path(plan["execution_directory"]).parent
    command = (
        ".venv/Scripts/python.exe -m tools.validation.identity_judgment_smoke execute "
        f'--preparation "{directory / "preparation.json"}" '
        f"--approved-manifest-sha256 {canonical_digest(plan)}"
    )
    return f"""# V0 identity development smoke preparation

No live execution is authorized by this preparation. A future user must approve this
new exact manifest and its limits; the historical one-call allowance is not reused.

Manifest SHA-256: `{canonical_digest(plan)}`
Wire request SHA-256: `{plan["wire_request_sha256"]}`
Destination: `{plan["endpoint"]}responses`
Data scope: `{json.dumps(plan["data_scope"], sort_keys=True)}`
Planned requests: `{json.dumps(plan["request_counts"], sort_keys=True)}`
Model: `{plan["wire_request"]["model"]}`.
Reasoning: `{plan["wire_request"]["reasoning"]["effort"]}`.
Limits: `{json.dumps(plan["limits"], sort_keys=True)}`
Price reference: `{json.dumps(plan["pricing"], sort_keys=True)}`
Maximum standard retail reference: USD {plan["maximum_standard_retail_reference_usd"]:.6f}.
Regional +10% reference scenario: USD {plan["maximum_regional_retail_reference_usd"]:.6f}.
Provider invoice is unavailable. Token sizing is an offline surrogate, not an invoice ceiling.
Missing cache categories use an explicitly labelled conservative reference upper bound.

Private originals and independent facts are linked by `source_hashes` in `preparation.json`.
The packet contains original claims and supplied candidates with request-local references.
The current pending report is `pending-identity-report.json`; V0 has no new model evidence.
Model/Google/planner/Routes sends during preparation: 0. Incremental charges: USD 0.

Only a current-session execution child using `gpt-6.1-sol` with `medium` reasoning may
perform a subsequently approved live execution. Provide source revision, frozen hashes,
credentials/configuration prerequisites and the exact command without copying secrets:

```powershell
{command}
```

The bound execution directory is `{plan["execution_directory"]}`. One attempt consumes it,
including errors; do not delete or regenerate it to retry. HTTP success does not establish
import success. Invalid/partial/foreign/citation/usage/source results stop without acceptance.
Preserve `response.bin`, `execution.json`, `model-result.json` and, only if import succeeds,
`identity-report.json`. FAIL and legitimate UNKNOWN are valid imported outcomes. They keep
original claims and null canonical endpoints; no all-match or all-PASS target is imposed.
"""


def _usage_cost(raw):
    usage = raw.get("usage")
    if not isinstance(usage, dict):
        raise ValueError("Missing provider usage")
    for key, limit in (
        ("input_tokens", LIMITS["max_input_tokens"]),
        ("output_tokens", LIMITS["max_output_tokens"]),
    ):
        value = usage.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= limit:
            raise ValueError("Invalid or excessive reported token usage")
    details = usage.get("input_tokens_details")
    if details is None:
        details = {}
    if not isinstance(details, dict):
        raise ValueError("Invalid input token categories")
    counts = {}
    for key in ("cached_tokens", "cache_write_tokens"):
        value = details.get(key)
        if value is not None and (
            not isinstance(value, int) or isinstance(value, bool) or value < 0
        ):
            raise ValueError("Invalid input token categories")
        counts[key] = value
    cached, writes = counts["cached_tokens"], counts["cache_write_tokens"]
    if (cached or 0) + (writes or 0) > usage["input_tokens"]:
        raise ValueError("Input token categories exceed total")
    # Unknown cached tokens earn no assumed discount; unknown writes use the highest rate.
    priced_cached = cached or 0
    priced_writes = usage["input_tokens"] - priced_cached if writes is None else writes
    ordinary = usage["input_tokens"] - priced_cached - priced_writes
    cost = (
        ordinary * PRICING["input_per_million_usd"]
        + priced_cached * PRICING["cached_input_per_million_usd"]
        + priced_writes * PRICING["cache_write_per_million_usd"]
        + usage["output_tokens"] * PRICING["output_per_million_usd"]
    ) / 1000000
    regional = cost * PRICING["regional_multiplier_scenario"]
    if regional > LIMITS["retail_reference_allowance_usd"]:
        raise ValueError("Retail reference allowance exceeded")
    return {
        "retail_reference_usd": cost,
        "regional_retail_reference_usd": regional,
        "retail_reference_basis": "reported_categories"
        if cached is not None and writes is not None
        else "missing_category_upper_bound",
    }


class _SingleRequest(httpx.AsyncBaseTransport):
    def __init__(self, inner, plan, directory, receipt):
        self.inner, self.plan, self.directory, self.receipt = inner, plan, directory, receipt

    async def handle_async_request(self, request):
        if self.receipt["model_sends"]:
            raise ValueError("Additional sends and retries are prohibited")
        if request.method != "POST" or request.url != self.plan["endpoint"] + "responses":
            raise ValueError("Unexpected method or endpoint")
        if json.loads(request.content) != self.plan["wire_request"]:
            raise ValueError("Frozen SDK request mismatch")
        # Revalidate originals at the actual send boundary, after the SDK has built its request.
        if any(file_digest(p) != sha for p, sha in self.plan["source_hashes"].items()):
            raise ValueError("Frozen source changed before send")
        self.receipt.update(model_sends=1, requested_at=datetime.now(UTC).isoformat())
        save(self.directory, "execution.json", self.receipt)
        async with asyncio.timeout(LIMITS["http_timeout_seconds"]):
            response = await self.inner.handle_async_request(request)
            raw = await response.aread()
        self.receipt.update(
            retrieved_at=datetime.now(UTC).isoformat(),
            http_status=response.status_code,
            raw_response_sha256=hashlib.sha256(raw).hexdigest(),
        )
        (self.directory / "response.bin").write_bytes(raw)
        if response.status_code != 200:
            raise ValueError("Unsuccessful HTTP response")
        value = json.loads(raw)
        self.receipt["usage"] = value.get("usage")
        self.receipt.update(_usage_cost(value))
        self.receipt["response_id"] = value.get("id")
        return response

    async def aclose(self):
        await self.inner.aclose()


async def execute_smoke(plan, *, approved_manifest_sha256=None, api_key, transport=None):
    """Consume the approved directory once; any failed attempt remains terminal."""
    if approved_manifest_sha256 is None or canonical_digest(plan) != approved_manifest_sha256:
        raise ValueError("Explicit approval of this manifest digest is required")
    directory = Path(plan["execution_directory"])
    expected = _plan(
        plan["bundle_path"], plan["endpoint"], directory.parent, plan["protected_files"]
    )
    if plan != expected:
        raise ValueError("Frozen preparation differs from verified sources or execution policy")
    if not api_key:
        raise ValueError("Model credentials are required")
    directory.mkdir(exist_ok=False)
    receipt = {
        "status": "running",
        "manifest_sha256": approved_manifest_sha256,
        "model_sends": 0,
        "provider_invoice_usd": None,
        "wire_request_sha256": plan["wire_request_sha256"],
    }
    save(directory, "execution.json", receipt)
    bounded = _SingleRequest(
        transport or httpx.AsyncHTTPTransport(retries=0), plan, directory, receipt
    )
    try:
        async with httpx.AsyncClient(transport=bounded, follow_redirects=False) as http:
            async with AsyncOpenAI(
                base_url=plan["endpoint"],
                api_key=api_key,
                max_retries=0,
                timeout=LIMITS["http_timeout_seconds"],
                http_client=http,
            ) as client:
                await client.responses.create(**plan["wire_request"])
        raw = json.loads((directory / "response.bin").read_bytes())
        if any(file_digest(p) != sha for p, sha in plan["source_hashes"].items()):
            raise ValueError("Frozen source changed during execution")
        result = {
            "schema_version": RESULT_VERSION,
            "packet": plan["packet"],
            "requested_at": receipt["requested_at"],
            "retrieved_at": receipt["retrieved_at"],
            "response": raw,
            "response_sha256": canonical_digest(raw),
        }
        save(directory, "model-result.json", result)
        material = load_v0_material(None, plan["bundle_path"])
        report = resolve_identities(
            thaw(material.intake), thaw(material.evidence), model_result=result
        ).to_dict()
        save(directory, "identity-report.json", report)
        receipt.update(status="completed", identity_status=report["status"])
    except (Exception, asyncio.CancelledError) as exc:
        # Persist the type only: SDK exception strings can contain credentials/provider bodies.
        receipt.update(status="stopped", error_type=type(exc).__name__)
        if isinstance(exc, asyncio.CancelledError):
            raise
    finally:
        save(directory, "execution.json", receipt)
    return receipt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare = commands.add_parser("prepare")
    prepare.add_argument("--material", required=True)
    prepare.add_argument("--directory", required=True)
    prepare.add_argument(
        "--endpoint", help="Explicit HTTPS destination for credential-free preparation"
    )
    prepare.add_argument("--protected-hashes", help="JSON file containing a file_hashes map")
    execute = commands.add_parser("execute")
    execute.add_argument("--preparation", required=True)
    execute.add_argument("--approved-manifest-sha256", required=True)
    args = parser.parse_args(argv)
    from backend.app.versions.v0.config import V0Settings

    if args.command == "prepare":
        protected = None
        if args.protected_hashes:
            protected = json.loads(Path(args.protected_hashes).read_text(encoding="utf-8"))[
                "file_hashes"
            ]
        plan = prepare_smoke(
            args.material,
            endpoint=args.endpoint or str(V0Settings().azure_openai_endpoint),
            directory=args.directory,
            protected_files=protected,
        )
        print(
            json.dumps(
                {
                    "manifest_sha256": canonical_digest(plan),
                    "reference_count": plan["reference_count"],
                }
            )
        )
        return 0
    settings = V0Settings()
    plan = json.loads(Path(args.preparation).read_text(encoding="utf-8"))
    if str(settings.azure_openai_endpoint).rstrip("/") + "/" != plan["endpoint"]:
        raise ValueError("Configured endpoint differs from approved preparation")
    receipt = asyncio.run(
        execute_smoke(
            plan,
            approved_manifest_sha256=args.approved_manifest_sha256,
            api_key=settings.azure_openai_api_key.get_secret_value(),
        )
    )
    print(json.dumps(receipt))
    return 0 if receipt["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
