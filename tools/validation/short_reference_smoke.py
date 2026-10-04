"""Development-only, bounded execution at actual short-reference model boundaries."""

import asyncio
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from typing import Literal

import httpx
from openai import AsyncOpenAI
from pydantic import BaseModel, ConfigDict

from backend.app.evidence.experience_models import ExperienceProfileDraft, ReviewEvidence
from backend.app.llm.azure_foundry.client import AzureFoundryStructuredLLMClient
from backend.app.observability.usage import UsageLedger
from backend.app.policies.experience_profile import validate_profile_draft
from backend.app.runtime.token_counting import count_tokens
from backend.app.services import preference_interpretation as _bootstrap  # noqa: F401


def save(directory, name, value):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class SmokeCase:
    name: str
    payload: dict


class SmokeLimitError(ValueError):
    """A preparation, request or response violates the authorized smoke limits."""


class IdentityDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reference_id: str
    decision: Literal["match", "unknown", "no_supported_match"]
    candidate_id: str | None
    rationale: str
    evidence_fields: list[str]


class IdentityProposals(BaseModel):
    model_config = ConfigDict(extra="forbid")
    decisions: list[IdentityDecision]


def retail_cost(usage):
    if usage is None:
        return None
    values = [usage.get("input_tokens"), usage.get("output_tokens")]
    if not all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in values):
        raise SmokeLimitError("Invalid provider usage counts")
    cached = (usage.get("input_tokens_details") or {}).get("cached_tokens", 0)
    if not isinstance(cached, int) or isinstance(cached, bool) or not 0 <= cached <= values[0]:
        raise SmokeLimitError("Invalid cached token count")
    return ((values[0] - cached) * 0.10 + cached * 0.01 + values[1] * 0.50) / 1000000


class BoundedTransport(httpx.AsyncBaseTransport):
    """Enforce limits on the actual outgoing SDK request and journal every attempt."""

    def __init__(self, inner, endpoint, directory, *, clock=monotonic, frozen_requests=None):
        self.inner, self.directory, self.clock = inner, directory, clock
        self.url = httpx.URL(endpoint.rstrip("/") + "/responses")
        self.started = clock()
        self.case = None
        self.attempts = []
        self.frozen_requests = frozen_requests
        self.blocked_reason = None
        self.ledger = UsageLedger(clock=clock)

    async def handle_async_request(self, request):
        try:
            return await self.send_bounded(request)
        except Exception as exc:
            self.blocked_reason = (
                str(exc) if isinstance(exc, SmokeLimitError) else type(exc).__name__
            )
            raise

    async def send_bounded(self, request):
        if request.method != "POST" or request.url != self.url:
            raise SmokeLimitError("Unexpected request destination or method")
        if not self.case or len(self.attempts) >= 6:
            raise SmokeLimitError("Model request allowance exhausted")
        if any(attempt["case"] == self.case for attempt in self.attempts):
            raise SmokeLimitError("Retries and repeated cases are prohibited")
        remaining = 600 - (self.clock() - self.started)
        if remaining <= 0:
            raise SmokeLimitError("Total deadline exhausted")
        body = json.loads(request.content)
        if body.get("model") != "gpt-6-luna" or body.get("tools"):
            raise SmokeLimitError("Unexpected model or tools")
        body["max_output_tokens"] = min(body.get("max_output_tokens", 4000), 4000)
        body["reasoning"] = {"effort": "low"}
        body["store"] = False
        estimated = count_tokens(json.dumps(body)) + 1024
        if estimated > 10000:
            raise SmokeLimitError("Input token allowance exceeded")
        if self.frozen_requests is not None and self.frozen_requests.get(self.case) != digest(body):
            raise SmokeLimitError("Frozen request changed")
        reserved = sum(
            a.get("retail_estimate_usd") if a.get("retail_estimate_usd") is not None else 0.003
            for a in self.attempts
        )
        if reserved + 0.003 > 0.05:
            raise SmokeLimitError("Retail estimate budget exhausted")
        headers = dict(request.headers)
        headers.pop("content-length", None)
        bounded = httpx.Request(
            "POST", request.url, headers=headers, json=body, extensions=request.extensions
        )
        attempt = {
            "case": self.case,
            "request": body,
            "request_sha256": digest(body),
            "estimated_input_tokens_with_reserve": estimated,
        }
        self.attempts.append(attempt)
        event_id = self.ledger.begin(
            "model",
            "azure_foundry",
            self.case,
            model="gpt-6-luna",
            stage=self.case,
            repair=self.case == "v3_repair",
        )
        http_id = self.ledger.begin(
            "provider",
            "azure_foundry",
            "model_http",
            stage=self.case,
            repair=self.case == "v3_repair",
            source="http_transport",
            model_event_id=event_id,
            model_provider="azure_foundry",
        )
        attempt["model_event_id"], attempt["http_event_id"] = event_id, http_id
        attempt["started_at"] = datetime.now(UTC).isoformat()
        started = self.clock()
        save(self.directory, "attempts.json", self.attempts)
        try:
            async with asyncio.timeout(min(60, remaining)):
                response = await self.inner.handle_async_request(bounded)
                raw_bytes = await response.aread()
            attempt["http_status"] = response.status_code
            attempt["response_sha256"] = hashlib.sha256(raw_bytes).hexdigest()
            (self.directory / f"{self.case}-response.bin").write_bytes(raw_bytes)
            if response.status_code != 200:
                raise SmokeLimitError("HTTP response was not successful")
            raw = json.loads(raw_bytes)
            attempt["response_id"] = raw.get("id")
            attempt["usage"] = raw.get("usage")
            attempt["retail_estimate_usd"] = retail_cost(raw.get("usage"))
            if raw.get("status") != "completed" or any(
                item.get("type") not in ("message", "reasoning") for item in raw.get("output", [])
            ):
                raise SmokeLimitError("Incomplete response or unexpected tool output")
            usage = raw.get("usage")
            if usage and (usage["input_tokens"] > 10000 or usage["output_tokens"] > 4000):
                raise SmokeLimitError("Reported token allowance exceeded")
            return response
        except BaseException as exc:
            attempt["error_type"] = type(exc).__name__
            raise
        finally:
            attempt["elapsed_seconds"] = max(0, self.clock() - started)
            outcome = "failed" if attempt.get("error_type") else "completed"
            self.ledger.finish(
                "model",
                event_id,
                outcome=outcome,
                usage=attempt.get("usage"),
                response_id=attempt.get("response_id"),
            )
            self.ledger.finish(
                "provider", http_id, outcome=outcome, http_status=attempt.get("http_status")
            )
            save(self.directory, "attempts.json", self.attempts)

    async def aclose(self):
        await self.inner.aclose()


class SmokeRunner:
    """Run sequential cases, retaining a terminal failure without further sends."""

    def __init__(
        self, *, endpoint, api_key, transport, directory, frozen_requests=None, clock=monotonic
    ):
        self.endpoint, self.api_key = endpoint, api_key
        self.directory = Path(directory)
        self.transport = BoundedTransport(
            transport, endpoint, self.directory, frozen_requests=frozen_requests, clock=clock
        )

    async def run(self, cases):
        from backend.app.services.review_selection import _PROFILE_SYSTEM_PROMPT

        report = {
            "status": "completed",
            "cases": [],
            "model_sends": 0,
            "native_identity_adoptions": 0,
        }
        async with httpx.AsyncClient(
            transport=self.transport, follow_redirects=False, timeout=60
        ) as http:
            client = AzureFoundryStructuredLLMClient(
                endpoint=self.endpoint,
                deployment="gpt-6-luna",
                api_key=self.api_key,
                http_async_client=http,
                http_client=httpx.Client(transport=httpx.MockTransport(self.reject_sync)),
            )
            sdk = AsyncOpenAI(
                base_url=self.endpoint,
                api_key=self.api_key,
                max_retries=0,
                timeout=60,
                http_client=http,
            )
            try:
                for case in cases:
                    self.transport.case = case.name
                    if case.name == "shared_primary":
                        from datetime import date

                        from backend.app.policies.itinerary_output import validate_output_sources
                        from backend.app.policies.trip_dates import (
                            create_trip_date_window,
                            validate_itinerary_dates,
                        )
                        from backend.app.schemas.itinerary_projection import V1Itinerary
                        from backend.app.versions.v1.prompts import (
                            ITINERARY_GENERATION_SYSTEM_PROMPT,
                        )
                        from tools.validation.short_reference_cases import (
                            fixture_places,
                            fixture_request,
                            primary_prompt,
                        )

                        value = await client.generate_structured(
                            system_prompt=ITINERARY_GENERATION_SYSTEM_PROMPT,
                            user_prompt=primary_prompt(case.payload),
                            response_schema=V1Itinerary,
                        )
                        value = validate_output_sources(
                            value,
                            places=fixture_places(),
                            supplied_ids=[p["place_id"] for p in case.payload["places"]],
                        )
                        validate_itinerary_dates(
                            fixture_request().trip_requirements(),
                            value,
                            create_trip_date_window(date(2026, 10, 5)),
                        )
                        visits = [a for d in value.days for a in d.activities]
                        expected = {p["place_id"] for p in case.payload["places"]}
                        if (
                            len(visits) != 2
                            or {a.source_place_id for a in visits} != expected
                            or any(a.activity_kind != "main_poi" for a in visits)
                        ):
                            raise SmokeLimitError("Primary fixture ownership or coverage failed")
                    elif case.name == "review_profile":
                        value = await client.generate_structured(
                            system_prompt=_PROFILE_SYSTEM_PROMPT,
                            user_prompt=json.dumps(case.payload),
                            response_schema=ExperienceProfileDraft,
                        )
                        reviews = [
                            ReviewEvidence(place_id=case.payload["place_id"], **r)
                            for r in case.payload["reviews"]
                        ]
                        validate_profile_draft(
                            value,
                            place_id=case.payload["place_id"],
                            reviews=reviews,
                            retrieved_at="2026-10-05T00:00:00Z",
                        )
                    elif case.name == "v3_repair":
                        from backend.app.schemas.itinerary import Itinerary
                        from backend.app.versions.v3.repair_acceptance import apply_patch
                        from backend.app.versions.v3.repair_models import (
                            CandidatePreparation,
                            RepairScope,
                        )
                        from backend.app.versions.v3.repair_projection import REPAIR_SYSTEM_PROMPT
                        from tools.validation.short_reference_cases import repair_prompt

                        value = await client.generate_repair_structured(
                            system_prompt=REPAIR_SYSTEM_PROMPT,
                            user_prompt=repair_prompt(case.payload),
                            output_tokens=4000,
                        )
                        scope = RepairScope.model_validate(case.payload["scope"])
                        if {d.target_id for d in value.target_dispositions} != set(
                            scope.target_ids
                        ) or len(value.edits) != 1:
                            raise SmokeLimitError("Repair fixture target coverage failed")
                        apply_patch(
                            Itinerary.model_validate(case.payload["original"]),
                            value,
                            scope,
                            CandidatePreparation.model_validate(case.payload["preparation"]),
                        )
                    elif case.name == "official_reasoning":
                        from backend.app.evidence.models import PlaceEvidence
                        from backend.app.evidence.official_models import EvidenceSourceBlock
                        from backend.app.evidence.web_models import WebEvidenceTask
                        from backend.app.integrations.azure_foundry.evidence_reasoner import (
                            AzureFoundryEvidenceReasoner,
                        )
                        from backend.app.runtime.config_loader import load_runtime_config

                        reasoner = AzureFoundryEvidenceReasoner(
                            endpoint=self.endpoint,
                            deployment="gpt-6-luna",
                            api_key=self.api_key,
                            config=load_runtime_config().web_evidence,
                            responses_client=sdk.responses,
                        )
                        rows = await reasoner.reason(
                            WebEvidenceTask.model_validate(case.payload["task"]),
                            (EvidenceSourceBlock.model_validate(case.payload["source"]),),
                            PlaceEvidence.model_validate(case.payload["baseline"]),
                        )
                        if len(rows) != 1 or rows[0].candidate is None:
                            raise SmokeLimitError("Official fixture source alignment failed")
                        value = {"assessments": [row.model_dump(mode="json") for row in rows]}
                    elif case.name == "product_introduction":
                        from contextlib import asynccontextmanager
                        from types import SimpleNamespace

                        from backend.app.schemas.itinerary import Itinerary
                        from backend.app.services.product_introductions import (
                            IntroductionClient,
                            ProductIntroductions,
                        )

                        @asynccontextmanager
                        async def introduction_factory():
                            yield IntroductionClient(sdk, "gpt-6-luna")

                        itinerary = Itinerary.model_validate(case.payload["original"])
                        value = await ProductIntroductions(
                            factory=introduction_factory, timeout_seconds=60
                        ).generate(
                            itinerary,
                            SimpleNamespace(deadline=monotonic() + 60, summaries={}),
                        )
                        expected = {a.activity_id for d in itinerary.days for a in d.activities}
                        if set(value) != expected:
                            raise SmokeLimitError(
                                "Introduction fixture ownership or coverage failed"
                            )
                    elif case.name == "v0_identity":
                        from backend.evaluation.identity_assistance import IdentityAssistancePacket

                        packet = IdentityAssistancePacket(case.payload["cases"])
                        raw = await sdk.responses.create(
                            model="gpt-6-luna",
                            instructions=case.payload["instructions"]
                            + "\n"
                            + packet.payload["instructions"],
                            input=json.dumps({"cases": packet.payload["cases"]}),
                            max_output_tokens=4000,
                            tools=[],
                            text={
                                "format": {
                                    "type": "json_schema",
                                    "name": "V0IdentityProposals",
                                    "strict": True,
                                    "schema": packet.constrain_schema(
                                        IdentityProposals.model_json_schema()
                                    ),
                                }
                            },
                        )
                        value = packet.resolve(
                            IdentityProposals.model_validate_json(raw.output_text).model_dump()
                        )
                    else:
                        raise SmokeLimitError("Unknown smoke case")
                    usage = self.transport.attempts[-1].get("usage")
                    cost = retail_cost(usage)
                    report["cases"].append(
                        {
                            "case": case.name,
                            "canonical_output": value.model_dump(mode="json")
                            if hasattr(value, "model_dump")
                            else value,
                            "usage": usage,
                            "retail_estimate_usd": cost,
                        }
                    )
            except (Exception, asyncio.CancelledError) as exc:
                report.update(
                    status="stopped",
                    failed_case=self.transport.case,
                    error_type=type(exc).__name__,
                    stop_reason=self.transport.blocked_reason or "adapter_or_domain_failure",
                )
            finally:
                await client.aclose()
                await sdk.close()
                report["model_sends"] = len(self.transport.attempts)
                report["attempts"] = self.transport.attempts
                report["known_retail_estimate_usd"] = sum(
                    a.get("retail_estimate_usd") or 0 for a in self.transport.attempts
                )
                report["cost_missing_cases"] = [
                    a["case"]
                    for a in self.transport.attempts
                    if a.get("retail_estimate_usd") is None
                ]
                report["retail_estimate_usd"] = (
                    report["known_retail_estimate_usd"]
                    if not report["cost_missing_cases"]
                    else None
                )
                report["price_source"] = "https://developers.openai.com/api/docs/models/gpt-6-luna"
                report["price_date"] = "2026-10-05"
                report["price_assumptions"] = (
                    "Standard token rates; cache-write, regional "
                    "and invoice adjustments unavailable"
                )
                report["invoice_amount"] = None
                usage = self.transport.ledger.snapshot()
                usage.update(
                    schema_version="rtpeval_usage_1",
                    namespace="development_adapter_smoke",
                    outcome=report["status"],
                    collection_status="partial",
                    missing_fields=[v for v in usage["missing_fields"] if v]
                    + ["planner_pipeline_coverage", "invoice_amount"],
                    coverage={
                        "adapter_coverage": "unverified",
                        "scope": "selected_frozen_adapter_cases_only",
                    },
                )
                save(self.directory, "usage.json", usage)
                save(self.directory, "execution.json", report)
        return report

    @staticmethod
    def reject_sync(request):
        raise SmokeLimitError("Synchronous model requests are prohibited")
