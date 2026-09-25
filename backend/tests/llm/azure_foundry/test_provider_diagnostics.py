"""Provider facts pass through the real SDK, adapter and smoke; no live services."""

import json
from types import SimpleNamespace

import httpx
import pytest

from backend.app.llm.azure_foundry.provider_diagnostics import normalize
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.tests.llm.azure_foundry.test_preference_smoke_harness import execute, matrix
from backend.tests.llm.azure_foundry.test_requirement_acceptance_harness import response
from backend.tests.services.test_preference_input_gate import draft, issue


@pytest.mark.parametrize(
    "status,code,category",
    [
        (400, "invalid_json_schema", "configuration_failure"),
        (400, "content_filter", "provider_request_rejected"),
        (400, None, "provider_request_rejected"),
        (429, "rate_limit_exceeded", "transport_failure"),
        (503, "service_unavailable", "transport_failure"),
    ],
)
def test_http_failure_facts_survive_boundary(tmp_path, status, code, category):
    def handler(request):
        return httpx.Response(
            status,
            headers={"x-request-id": "provider-fixture"},
            json={
                "error": {"code": code, "type": "fixture_type", "message": "fixture message"},
            },
        )

    result, sends, clients = execute(
        tmp_path,
        [draft(disposition="VALID")],
        handler_override=handler,
    )
    row = result["cases"][0]
    d = row["provider_diagnostics"]
    assert row["application_outcome"]["status"] == category
    assert d["http_status"] == status and d["provider_error_code"] == code
    assert d["provider_error_type"] == "fixture_type"
    assert d["provider_error_message"] == "fixture message"
    assert d["provider_request_id"] == "provider-fixture"
    assert d["usage_availability"] == "unavailable" and d["usage"] is None
    assert "provider_diagnostics" not in row["application_outcome"]
    assert len(sends) == 1 and clients[0].last_call_metadata["provider_diagnostics"] == d


@pytest.mark.parametrize("mode", ["plain", "refusal", "incomplete", "no_reason"])
def test_response_failure_is_never_gate_safety(tmp_path, mode):
    def handler(request):
        payload = response("I'm sorry, but I cannot assist with that request.", 1)
        if mode == "refusal":
            payload["output"][0]["content"] = [{"type": "refusal", "refusal": "fixture"}]
        if mode in ("incomplete", "no_reason"):
            payload["status"] = "incomplete"
            payload["incomplete_details"] = (
                {"reason": "max_output_tokens"} if mode == "incomplete" else None
            )
        return httpx.Response(200, json=payload)

    result, sends, _ = execute(
        tmp_path,
        [draft(disposition="VALID")],
        handler_override=handler,
    )
    row = result["cases"][0]
    assert row["state"] == "provider_failure"
    assert row["domain_parsed_dto"] is None
    assert row["application_outcome"]["status"] == (
        "provider_refusal" if mode == "refusal" else "provider_incomplete"
    )
    d = row["provider_diagnostics"]
    assert d["structured_refusal"] == (mode == "refusal")
    assert d["incomplete_reason"] == ("max_output_tokens" if mode == "incomplete" else None)
    assert d["usage"] == {"input_tokens": 30, "output_tokens": 10, "total_tokens": 40}
    assert d["provider_response_id"] == "resp_1"
    assert len(sends) == 1


@pytest.mark.parametrize("safety", [False, True])
def test_valid_domain_outputs_unchanged(tmp_path, safety):
    value = (
        draft(issue("safety_self_harm"), disposition="VALID", safety="SAFETY_BLOCK")
        if safety
        else draft(disposition="VALID")
    )
    result, _, _ = execute(tmp_path, [value])
    assert result["stop_reason"] is None
    assert result["cases"][0]["frozen_expectation_match"]


def test_allowlist_redaction_and_truncation():
    error = SimpleNamespace(
        status_code=400,
        request_id="safe-id",
        body={
            "code": "content_filter",
            "type": "fixture",
            "message": ("fixture-secret Bearer private-token\n"
                        "Authorization: Basic private\napi-key: hidden\n") + "x" * 3000,
            "headers": {"Authorization": "secret"},
            "reasoning": "PRIVATE REASONING",
        },
    )
    d = normalize(error=error, secrets=("fixture-secret",))
    text = json.dumps(d)
    assert all(
        x not in text
        for x in ("fixture-secret", "private-token", "Basic private", "hidden", "PRIVATE REASONING")
    )
    assert len(d["provider_error_message"]) == 1024
    assert d["truncated_fields"] == ["provider_error_message"]
    assert RequirementBoundaryError("failed", provider_diagnostics=d).as_dict() == {
        "code": "failed",
        "stage": "canonicalization",
        "status": "invalid_model_contract",
        "errors": (),
    }


def test_no_response_has_no_invented_facts():
    d = normalize(error=RuntimeError("private detail"))
    assert all(
        d[k] is None
        for k in (
            "http_status",
            "provider_error_code",
            "provider_request_id",
            "provider_error_message",
            "usage",
        )
    )


def test_capture_and_cleanup_cannot_replace_provider_failure(tmp_path):
    def attach(client, observer):
        from tools.validation.preference_gate_smoke import attach_observer

        attach_observer(client, observer)

        class BrokenCapture:
            def record(self, *args, **kwargs):
                raise OSError("private capture error")

        client.requirement_capture = BrokenCapture()

    result, _, _ = execute(
        tmp_path,
        ["ordinary non-JSON response"],
        manifest=matrix(tmp_path, [draft(disposition="VALID")]),
        attach=attach,
        close_failure=True,
    )
    assert result["stop_reason"] == "provider_failure:case_0"
    assert "cleanup_failure:RuntimeError" in result["secondary_errors"]
    row = result["cases"][0]
    assert row["application_outcome"]["status"] == "provider_incomplete"
    assert row["provider_diagnostics"]["usage_availability"] == "available"
    assert "capture_failure:OSError" in row["secondary_errors"]


def test_failure_usage_and_missing_body_over_real_sdk(tmp_path):
    def handler(request):
        return httpx.Response(
            400,
            json={
                "error": {"message": "bounded", "code": "content_filter"},
                "usage": {"input_tokens": 8, "output_tokens": 0, "reasoning": "not retained"},
            },
        )

    result, _, _ = execute(tmp_path, [draft(disposition="VALID")], handler_override=handler)
    d = result["cases"][0]["provider_diagnostics"]
    assert d["usage"] == {"input_tokens": 8, "output_tokens": 0}
    assert "provider_request_id" in d["unavailable_fields"]
    assert "reasoning" not in json.dumps(d)


def test_sdk_connection_failure_without_response(tmp_path):
    def handler(request):
        raise httpx.ConnectError("fixture failure", request=request)

    result, sends, _ = execute(tmp_path, [draft(disposition="VALID")], handler_override=handler)
    d = result["cases"][0]["provider_diagnostics"]
    assert len(sends) == 1
    assert d["http_status"] is None and d["provider_error_code"] is None
    assert d["usage_availability"] == "unavailable"
    assert result["cases"][0]["application_outcome"]["status"] == "transport_failure"
