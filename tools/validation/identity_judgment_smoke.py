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
from backend.evaluation.records import canonical_digest, thaw

MODEL = "gpt-6-luna"
LIMITS = {
    "max_sends": 1,
    "max_retries": 0,
    "max_input_tokens": 20000,
    "input_token_reserve": 1024,
    "max_output_tokens": 4000,
    "http_timeout_seconds": 60,
    "retail_reference_allowance_usd": 0.005,
}
PRICING = {
    "checked_on": "2026-10-06",
    "source": "https://developers.openai.com/api/docs/models/gpt-6-luna",
    "input_per_million_usd": 0.10,
    "output_per_million_usd": 0.50,
    "basis": "Standard uncached retail reference; Foundry invoice unavailable.",
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
    root = Path(bundle["artifact_root"])
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
    return {
        "schema_version": "rtpeval_identity_smoke_preparation_1",
        "implementation_hashes": {
            str(path): file_digest(path)
            for path in (
                Path(__file__).resolve(),
                Path(__file__).resolve().parents[2] / "backend/evaluation/identity_llm.py",
            )
        },
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
        "reference_count": len(json.loads(wire["input"])["cases"]),
        "estimated_input_tokens_with_reserve": estimated,
        "maximum_standard_retail_reference_usd": (
            LIMITS["max_input_tokens"] * PRICING["input_per_million_usd"]
            + LIMITS["max_output_tokens"] * PRICING["output_per_million_usd"]
        )
        / 1000000,
        "preparation": {"actual_sends": 0, "incremental_charges_usd": 0},
    }


def prepare_smoke(bundle_path, *, endpoint, directory, protected_files=None):
    """Freeze verified sources and an exact SDK request without credentials or sends."""
    protected = {str(Path(p).resolve()): sha for p, sha in (protected_files or {}).items()}
    plan = _plan(bundle_path, endpoint, directory, protected)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    save(directory, "preparation.json", plan)
    return plan


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
    # Deliberately do not assume cached-input discounts or provider invoice equivalence.
    cost = (
        usage["input_tokens"] * PRICING["input_per_million_usd"]
        + usage["output_tokens"] * PRICING["output_per_million_usd"]
    ) / 1000000
    if cost > LIMITS["retail_reference_allowance_usd"]:
        raise ValueError("Retail reference allowance exceeded")
    return cost


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
        self.receipt["retail_reference_usd"] = _usage_cost(value)
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
    prepare.add_argument("--protected-hashes", help="JSON file containing a file_hashes map")
    execute = commands.add_parser("execute")
    execute.add_argument("--preparation", required=True)
    execute.add_argument("--approved-manifest-sha256", required=True)
    args = parser.parse_args(argv)
    from backend.app.versions.v0.config import V0Settings

    settings = V0Settings()
    if args.command == "prepare":
        protected = None
        if args.protected_hashes:
            protected = json.loads(Path(args.protected_hashes).read_text(encoding="utf-8"))[
                "file_hashes"
            ]
        plan = prepare_smoke(
            args.material,
            endpoint=str(settings.azure_openai_endpoint),
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
