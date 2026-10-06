"""Frozen development smoke through the SDK and offline HTTP boundary."""

import asyncio
import hashlib
import json
from pathlib import Path

import httpx
import pytest

from backend.evaluation.records import canonical_digest
from backend.tests.llm.azure_foundry.test_short_reference_smoke import sdk_response
from tools.validation.identity_judgment_smoke import execute_smoke, prepare_smoke

pytest_plugins = (
    "backend.tests.evaluation.test_intake",
    "backend.tests.evaluation.test_identity_adoption",
)
ENDPOINT = "https://fixture.example/openai/v1/"


def prepared(adoption_case, tmp_path):
    return prepare_smoke(adoption_case[2], endpoint=ENDPOINT, directory=tmp_path / "prepared")


def run(plan, respond, *, approval=True, approved_digest=None):
    return asyncio.run(
        execute_smoke(
            plan,
            approved_manifest_sha256=(approved_digest or canonical_digest(plan))
            if approval
            else None,
            api_key="unused-test-secret",
            transport=httpx.MockTransport(respond),
        )
    )


def output(plan, *, failure=False, match=False):
    rows = []
    for case in json.loads(plan["wire_request"]["input"])["cases"]:
        rows.append(
            {
                "reference_id": case["reference_id"],
                "decision": "unknown",
                "candidate_id": None,
                "rationale": "Insufficient independent facts.",
                "evidence_fields": [],
                "address_assessment": "unknown" if case["claim"]["location"] else "not_supplied",
                "destination_assessment": "unknown",
            }
        )
        if match:
            rows[-1].update(
                decision="match",
                candidate_id=case["candidates"][0]["place_id"],
                rationale="Supplied independent fields establish this candidate.",
                evidence_fields=[
                    "claim.place_name",
                    "claim.destination",
                    "candidate.display_name",
                    "candidate.formatted_address",
                ],
                address_assessment="equivalent" if case["claim"]["location"] else "not_supplied",
                destination_assessment="consistent",
            )
            if case["claim"]["location"]:
                rows[-1]["evidence_fields"].append("claim.location")
    if failure:
        rows[0].update(
            decision="match",
            candidate_id=json.loads(plan["wire_request"]["input"])["cases"][0]["candidates"][0][
                "place_id"
            ],
            address_assessment="incorrect_claim",
            destination_assessment="consistent",
            rationale="The independent address contradicts the submitted address.",
            evidence_fields=[
                "claim.place_name",
                "claim.destination",
                "claim.location",
                "candidate.display_name",
                "candidate.formatted_address",
            ],
        )
    return {"decisions": rows}


def test_preparation_and_unapproved_execution_send_nothing(adoption_case, tmp_path):
    plan = prepared(adoption_case, tmp_path)
    assert plan["preparation"]["actual_sends"] == 0
    assert plan["preparation"]["incremental_charges_usd"] == 0
    with pytest.raises(ValueError, match="approval"):
        run(plan, lambda _: pytest.fail("Unexpected send"), approval=False)
    assert not (tmp_path / "prepared" / "execution").exists()


def test_offline_cli_preparation_needs_no_credentials(adoption_case, tmp_path, monkeypatch, capsys):
    from backend.app.versions.v0 import config
    from tools.validation.identity_judgment_smoke import main

    monkeypatch.setattr(
        config, "V0Settings", lambda: pytest.fail("Offline CLI must not load credentials")
    )
    assert (
        main(
            [
                "prepare",
                "--material",
                str(adoption_case[2]),
                "--directory",
                str(tmp_path / "cli-prepared"),
                "--endpoint",
                ENDPOINT,
            ]
        )
        == 0
    )
    summary = json.loads(capsys.readouterr().out)
    assert summary["reference_count"] == 2
    assert (tmp_path / "cli-prepared/handoff.md").is_file()


@pytest.mark.parametrize("adoption_case", [{"high_impact": True}], indirect=True)
def test_fresh_preparation_delivers_v0_scope_and_pending_report_without_sends(
    adoption_case, tmp_path, monkeypatch
):
    import socket

    from openai import AsyncOpenAI

    def forbidden(*_args, **_kwargs):
        pytest.fail("Offline preparation must not create clients or network connections")

    monkeypatch.setattr(AsyncOpenAI, "__init__", forbidden)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    before = {
        str(p): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in adoption_case[2].parent.rglob("*")
        if p.is_file()
    }
    plan = prepared(adoption_case, tmp_path)
    assert plan["schema_version"] == "rtpeval_identity_smoke_preparation_2"
    assert plan["data_scope"] == {
        "versions": ["v0"],
        "kinds": ["primary_visit", "requirement_subject"],
        "reference_count": 3,
        "candidate_count": 3,
        "original_addresses_missing": 3,
    }
    assert plan["request_counts"] == {"model": 1, "google": 0, "planner": 0, "routes": 0}
    assert plan["execution_gate"]["status"] == "awaiting_new_exact_plan_approval"
    assert plan["execution_gate"]["historical_allowance_reused"] is False
    assert plan["execution_gate"]["child_model"] == "gpt-6.1-sol"
    assert plan["execution_gate"]["child_reasoning_effort"] == "medium"
    assert plan["packet"]["association_policy_version"] == "v0_identity_correspondence_3"
    pending = json.loads((tmp_path / "prepared/pending-identity-report.json").read_text())
    assert all(
        r["grounding_verdict"] == "UNKNOWN" for r in pending["records"] if r["version"] == "v0"
    )
    assert all("model_judgment" not in r for r in pending["records"] if r["version"] != "v0")
    handoff = (tmp_path / "prepared/handoff.md").read_text()
    assert ENDPOINT in handoff and canonical_digest(plan) in handoff
    assert "No live execution is authorized" in handoff
    assert "gpt-6.1-sol" in handoff and "pending-identity-report.json" in handoff
    assert {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in before} == before


@pytest.mark.parametrize("change", ["source", "request", "endpoint", "limits"])
def test_changed_preparation_is_rejected_before_send(adoption_case, tmp_path, change):
    plan = prepared(adoption_case, tmp_path)
    approved_digest = canonical_digest(plan)
    if change == "source":
        adoption_case[2].write_text("{}", encoding="utf-8")
    elif change == "request":
        plan["wire_request"]["tools"] = [{"type": "web_search"}]
    elif change == "endpoint":
        plan["endpoint"] += "other"
    else:
        plan["limits"]["max_sends"] = 2
    with pytest.raises(ValueError):
        run(plan, lambda _: pytest.fail("Unexpected send"), approved_digest=approved_digest)


def test_new_allowance_covers_supported_price_categories(adoption_case, tmp_path):
    plan = prepared(adoption_case, tmp_path)
    assert plan["limits"]["max_input_tokens"] == 18000
    assert plan["limits"]["max_output_tokens"] == 3000
    assert plan["limits"]["retail_reference_allowance_usd"] == 0.0042
    assert plan["pricing"]["cached_input_per_million_usd"] == 0.01
    assert plan["pricing"]["cache_write_per_million_usd"] == 0.125
    assert plan["maximum_standard_retail_reference_usd"] == pytest.approx(0.00375)
    assert plan["maximum_regional_retail_reference_usd"] == pytest.approx(0.004125)


@pytest.mark.parametrize(
    "adoption_case, accepted",
    [({"claimed_location": "x" * 56000}, True), ({"claimed_location": "x" * 64000}, False)],
    indirect=["adoption_case"],
)
def test_preparation_keeps_full_claim_within_new_input_cap_and_rejects_overflow(
    adoption_case, tmp_path, monkeypatch, accepted
):
    from openai import AsyncOpenAI

    monkeypatch.setattr(
        AsyncOpenAI, "__init__", lambda *a, **kw: pytest.fail("Preparation created a live client")
    )
    if not accepted:
        with pytest.raises(ValueError, match="Estimated input exceeds smoke allowance"):
            prepared(adoption_case, tmp_path)
        assert not (tmp_path / "prepared").exists()
        return
    plan = prepared(adoption_case, tmp_path)
    assert 16000 < plan["estimated_input_tokens_with_reserve"] <= 18000
    cases = json.loads(plan["wire_request"]["input"])["cases"]
    assert cases[0]["claim"]["location"] == "x" * 56000
    assert plan["preparation"]["actual_sends"] == 0
    assert not (tmp_path / "prepared/execution").exists()


@pytest.mark.parametrize(
    "input_tokens, output_tokens, completed",
    [(18000, 3000, True), (18001, 3000, False), (18000, 3001, False)],
)
def test_reported_usage_at_new_caps_prices_full_cache_writes_and_stops_overflow(
    adoption_case, tmp_path, input_tokens, output_tokens, completed
):
    plan = prepared(adoption_case, tmp_path)
    response = sdk_response(output(plan), input_tokens=input_tokens, output_tokens=output_tokens)
    response["usage"]["input_tokens_details"] = {
        "cached_tokens": 0,
        "cache_write_tokens": input_tokens,
    }
    receipt = run(plan, lambda _: httpx.Response(200, json=response))
    assert receipt["model_sends"] == 1
    directory = tmp_path / "prepared/execution"
    assert (directory / "response.bin").is_file()
    if completed:
        assert receipt["status"] == "completed"
        assert receipt["retail_reference_usd"] == pytest.approx(0.00375)
        assert receipt["regional_retail_reference_usd"] == pytest.approx(0.004125)
        assert receipt["retail_reference_basis"] == "reported_categories"
        assert (directory / "identity-report.json").is_file()
    else:
        assert receipt["status"] == "stopped"
        assert not (directory / "identity-report.json").exists()
    with pytest.raises(FileExistsError):
        run(plan, lambda _: pytest.fail("Consumed usage-boundary attempt repeated"))


def test_relative_material_root_and_critical_implementation_are_frozen(adoption_case, tmp_path):
    bundle = json.loads(adoption_case[2].read_text())
    bundle["artifact_root"] = "."
    adoption_case[2].write_text(json.dumps(bundle), encoding="utf-8")
    plan = prepared(adoption_case, tmp_path)
    frozen = {Path(p).relative_to(Path.cwd()).as_posix() for p in plan["implementation_hashes"]}
    assert {
        "tools/validation/identity_judgment_smoke.py",
        "backend/evaluation/identity.py",
        "backend/evaluation/identity_adoption.py",
        "backend/evaluation/identity_llm.py",
        "backend/evaluation/records.py",
        "backend/model_references.py",
        "backend/app/runtime/token_counting.py",
    } <= frozen
    receipt = run(plan, lambda _: httpx.Response(200, json=sdk_response(output(plan))))
    assert receipt["status"] == "completed"


@pytest.mark.parametrize("writes", [200, None])
def test_sdk_usage_prices_categories_or_explicit_upper_bound(adoption_case, tmp_path, writes):
    plan = prepared(adoption_case, tmp_path)
    response = sdk_response(output(plan), input_tokens=1000, output_tokens=100)
    response["usage"]["input_tokens_details"] = {"cached_tokens": 600}
    if writes is not None:
        response["usage"]["input_tokens_details"]["cache_write_tokens"] = writes
    receipt = run(plan, lambda _: httpx.Response(200, json=response))
    assert receipt["status"] == "completed"
    assert receipt["usage"] == response["usage"]
    assert receipt["provider_invoice_usd"] is None
    assert receipt["retail_reference_usd"] == pytest.approx(0.000101 if writes == 200 else 0.000106)
    assert receipt["retail_reference_basis"] == (
        "reported_categories" if writes == 200 else "missing_category_upper_bound"
    )


@pytest.mark.parametrize(
    "details",
    [
        {"cached_tokens": True},
        {"cache_write_tokens": -1},
        {"cached_tokens": 80, "cache_write_tokens": 50},
        "invalid",
    ],
)
def test_invalid_usage_categories_stop_and_consume_attempt(adoption_case, tmp_path, details):
    plan = prepared(adoption_case, tmp_path)
    response = sdk_response(output(plan), input_tokens=120)
    response["usage"]["input_tokens_details"] = details
    receipt = run(plan, lambda _: httpx.Response(200, json=response))
    assert receipt["status"] == "stopped" and receipt["model_sends"] == 1
    assert (tmp_path / "prepared/execution/response.bin").is_file()
    assert not (tmp_path / "prepared/execution/identity-report.json").exists()
    with pytest.raises(FileExistsError):
        run(plan, lambda _: pytest.fail("Repeated failed execution"))


@pytest.mark.parametrize(
    "adoption_case", [{"claimed_location": "Wrong submitted address"}], indirect=True
)
def test_single_sdk_call_imports_failure_and_unknown_without_repair(adoption_case, tmp_path):
    plan = prepared(adoption_case, tmp_path)
    requests = []

    def respond(request):
        requests.append(request)
        assert json.loads(request.content) == plan["wire_request"]
        assert request.url == ENDPOINT + "responses"
        return httpx.Response(200, json=sdk_response(output(plan, failure=True)))

    receipt = run(plan, respond)
    assert receipt["status"] == "completed"
    assert receipt["model_sends"] == len(requests) == 1
    report = json.loads((tmp_path / "prepared/execution/identity-report.json").read_text())
    assert report["records"][0]["grounding_verdict"] == "FAIL"
    assert report["records"][0]["canonical_place_id"] is None
    assert report["records"][0]["original_claim"]["location"] == "Wrong submitted address"
    assert all(
        r["grounding_verdict"] == "UNKNOWN" for r in report["records"][1:] if r["version"] == "v0"
    )
    assert all("model_judgment" not in r for r in report["records"] if r["version"] != "v0")
    assert report["review_queue"] == []
    with pytest.raises(FileExistsError):
        run(plan, lambda _: pytest.fail("Repeated execution"))


def test_supported_match_with_null_original_address_imports_without_repair(adoption_case, tmp_path):
    plan = prepared(adoption_case, tmp_path)
    receipt = run(plan, lambda _: httpx.Response(200, json=sdk_response(output(plan, match=True))))
    assert receipt["status"] == "completed"
    report = json.loads((tmp_path / "prepared/execution/identity-report.json").read_text())
    v0 = [r for r in report["records"] if r["version"] == "v0"]
    assert all(r["grounding_verdict"] == "PASS" for r in v0)
    assert all(r["original_claim"]["location"] is None for r in v0)
    assert all(r["canonical_place_id"] is not None for r in v0)
    assert all("model_judgment" not in r for r in report["records"] if r["version"] != "v0")


@pytest.mark.parametrize(
    "problem",
    [
        "http",
        "redirect",
        "timeout",
        "json",
        "decision",
        "usage",
        "missing_usage",
        "tools",
        "incomplete",
        "partial",
        "unsupported_citation",
        "null_address_contract",
    ],
)
def test_terminal_errors_keep_one_attempt_without_import(adoption_case, tmp_path, problem):
    plan = prepared(adoption_case, tmp_path)
    requests = []

    def respond(request):
        requests.append(request)
        if problem == "timeout":
            raise httpx.ReadTimeout("unused-test-secret", request=request)
        if problem == "http":
            return httpx.Response(429, json={"error": "rate limited"})
        if problem == "redirect":
            return httpx.Response(307, headers={"location": "https://other.example/"})
        if problem == "json":
            return httpx.Response(200, content=b"invalid JSON")
        value = output(plan)
        if problem == "decision":
            value["decisions"][0]["reference_id"] = "foreign-reference"
        if problem == "partial":
            value["decisions"].pop()
        if problem == "unsupported_citation":
            value["decisions"][0]["evidence_fields"] = ["candidate.website"]
        if problem == "null_address_contract":
            value["decisions"][0]["address_assessment"] = "equivalent"
        response = sdk_response(value, input_tokens=20001 if problem == "usage" else 120)
        if problem == "missing_usage":
            response.pop("usage")
        if problem == "incomplete":
            response["status"] = "incomplete"
        if problem == "tools":
            response["output"].append(
                {"type": "web_search_call", "id": "tool", "status": "completed"}
            )
        return httpx.Response(200, json=response)

    receipt = run(plan, respond)
    assert receipt["status"] == "stopped"
    assert receipt["model_sends"] == len(requests) == 1
    directory = tmp_path / "prepared/execution"
    assert (directory / "execution.json").is_file()
    assert not (directory / "identity-report.json").exists()
    assert "unused-test-secret" not in (directory / "execution.json").read_text()
    if problem != "timeout":
        assert (directory / "response.bin").is_file()
    with pytest.raises(FileExistsError):
        run(plan, lambda _: pytest.fail("Repeated failed execution"))


def test_extra_protected_source_changed_during_call_prevents_import(adoption_case, tmp_path):
    from tools.validation.identity_judgment_smoke import file_digest

    source = tmp_path / "protected-original.json"
    source.write_text("original", encoding="utf-8")
    plan = prepare_smoke(
        adoption_case[2],
        endpoint=ENDPOINT,
        directory=tmp_path / "prepared",
        protected_files={str(source): file_digest(source)},
    )

    def respond(_request):
        source.write_text("changed", encoding="utf-8")
        return httpx.Response(200, json=sdk_response(output(plan)))

    receipt = run(plan, respond)
    assert receipt["status"] == "stopped"
    assert receipt["model_sends"] == 1
    assert not (tmp_path / "prepared/execution/identity-report.json").exists()
