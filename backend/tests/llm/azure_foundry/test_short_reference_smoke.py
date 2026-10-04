"""Public smoke execution over real SDKs and an offline HTTP boundary."""

import asyncio
import json

import httpx
import pytest

from tools.validation.short_reference_cases import (
    introduction_case,
    mock_output,
    official_case,
    prepared_cases,
    repair_case,
)
from tools.validation.short_reference_smoke import SmokeCase, SmokeRunner

PLACE_ID = "ChIJsynthetic-canonical-place-0123456789abcdef"


def sdk_response(value, *, input_tokens=120, output_tokens=40):
    return {
        "id": "resp_fixture",
        "object": "response",
        "created_at": 1791150000,
        "status": "completed",
        "model": "gpt-6-luna",
        "output": [
            {
                "id": "msg_fixture",
                "type": "message",
                "role": "assistant",
                "status": "completed",
                "content": [{"type": "output_text", "text": json.dumps(value), "annotations": []}],
            }
        ],
        "usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "input_tokens_details": {"cached_tokens": 0},
            "output_tokens_details": {"reasoning_tokens": 0},
        },
    }


def profile_case():
    return SmokeCase(
        "review_profile",
        {
            "place_id": PLACE_ID,
            "reviews": [
                {"review_id": "review_1", "text": "A quiet museum with few visitors."},
                {"review_id": "review_2", "text": "Quiet galleries and a short visit."},
            ],
        },
    )


def profile_output(place_id="p01"):
    return {
        "place_id": place_id,
        "summary": "Quiet galleries.",
        "summary_review_refs": ["review_1", "review_2"],
        "signals": [],
        "review_count_used": 2,
    }


def test_profile_sdk_smoke_restores_identity_and_records_bounded_wire(tmp_path):
    requests = []

    def respond(request):
        body = json.loads(request.content)
        requests.append(body)
        assert PLACE_ID not in request.content.decode()
        assert body["max_output_tokens"] == 4000
        assert body["reasoning"]["effort"] == "low"
        assert body["text"]["format"]["schema"]["properties"]["place_id"]["enum"] == ["p01"]
        return httpx.Response(200, json=sdk_response(profile_output()))

    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(respond),
        directory=tmp_path,
    )
    report = asyncio.run(runner.run([profile_case()]))
    assert report["status"] == "completed"
    assert report["model_sends"] == len(requests) == 1
    assert report["cases"][0]["canonical_output"]["place_id"] == PLACE_ID
    assert report["cases"][0]["usage"]["input_tokens"] == 120
    assert report["cases"][0]["retail_estimate_usd"] == 0.000032


def test_invalid_alias_is_terminal_and_keeps_failed_attempt(tmp_path):
    requests = []

    def respond(request):
        requests.append(request)
        return httpx.Response(200, json=sdk_response(profile_output("p99")))

    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(respond),
        directory=tmp_path,
    )
    report = asyncio.run(runner.run([profile_case(), profile_case()]))
    assert report["status"] == "stopped"
    assert report["failed_case"] == "review_profile"
    assert report["model_sends"] == len(requests) == 1
    assert json.loads((tmp_path / "attempts.json").read_text())[0]["usage"]["input_tokens"] == 120


def test_primary_restores_both_place_ids_through_native_itinerary_checks(tmp_path):
    case = prepared_cases()[0]
    requests = []

    def respond(request):
        requests.append(json.loads(request.content))
        return httpx.Response(200, json=sdk_response(mock_output(case)))

    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(respond),
        directory=tmp_path,
    )
    report = asyncio.run(runner.run([case]))
    assert report["status"] == "completed"
    activities = report["cases"][0]["canonical_output"]["days"][0]["activities"]
    assert [a["source_place_id"] for a in activities] == [
        "ChIJsynthetic-museum-A-0123456789abcdef",
        "ChIJsynthetic-museum-B-0123456789abcdef",
    ]
    assert len(requests) == 1
    wire = json.dumps(requests[0])
    assert "ChIJsynthetic" not in wire and "p01" in wire and "p02" in wire


def test_repair_restores_all_namespaces_and_passes_actual_patch_permissions(tmp_path):
    case = repair_case()

    def respond(request):
        wire = request.content.decode()
        assert "ChIJsynthetic" not in wire and "0123456789abcdef" not in wire
        return httpx.Response(200, json=sdk_response(mock_output(case)))

    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(respond),
        directory=tmp_path,
    )
    report = asyncio.run(runner.run([case]))
    assert report["status"] == "completed"
    result = report["cases"][0]["canonical_output"]
    assert result["edits"][0]["activity_id"] == "activity-first-0123456789abcdef0123456789abcdef"
    assert result["edits"][0]["place_id"] == "ChIJsynthetic-museum-B-0123456789abcdef"
    assert (
        result["target_dispositions"][0]["target_id"]
        == "finding-replace-0123456789abcdef0123456789abcdef"
    )


def test_official_sdk_smoke_keeps_exact_source_and_canonical_keys(tmp_path):
    case = official_case()

    def respond(request):
        body = json.loads(request.content)
        assert body["max_output_tokens"] == 1200
        assert "ChIJsynthetic" not in request.content.decode()
        return httpx.Response(200, json=sdk_response(mock_output(case)))

    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(respond),
        directory=tmp_path,
    )
    report = asyncio.run(runner.run([case]))
    assert report["status"] == "completed"
    candidate = report["cases"][0]["canonical_output"]["assessments"][0]["candidate"]
    assert candidate["place_id"] == "ChIJsynthetic-museum-A-0123456789abcdef"
    assert candidate["source_url"] == "https://museum.example.org/admission"
    assert candidate["supporting_excerpt"] == "Synthetic Museum A offers free general admission."
    assert len(candidate["source_key"]) == 24


def test_product_sdk_smoke_restores_both_activity_ids_and_checks_ownership(tmp_path):
    case = introduction_case()

    def respond(request):
        body = json.loads(request.content)
        assert body["max_output_tokens"] == 4000
        assert "0123456789abcdef" not in request.content.decode()
        return httpx.Response(200, json=sdk_response(mock_output(case)))

    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(respond),
        directory=tmp_path,
    )
    report = asyncio.run(runner.run([case]))
    assert report["status"] == "completed"
    result = report["cases"][0]["canonical_output"]
    assert set(result) == {
        "activity-first-0123456789abcdef0123456789abcdef",
        "activity-second-0123456789abcdef0123456789abcdef",
    }


def identity_case():
    return SmokeCase(
        "v0_identity",
        {
            "instructions": "Match only supplied independent candidates.",
            "cases": [
                {
                    "reference_id": "reference-" + "a" * 64,
                    "claim": {"place_name": "Museum A"},
                    "candidates": [{"place_id": PLACE_ID, "display_name": "Museum A"}],
                }
            ],
        },
    )


@pytest.mark.parametrize("decision,candidate", [("match", "p01"), ("unknown", None)])
def test_identity_sdk_keeps_judging_instructions_and_restores_only_proposals(
    tmp_path, decision, candidate
):
    case = identity_case()

    def respond(request):
        body = json.loads(request.content)
        assert "Match only supplied independent candidates." in body["instructions"]
        assert PLACE_ID not in request.content.decode() and "a" * 64 not in request.content.decode()
        return httpx.Response(
            200,
            json=sdk_response(
                {
                    "decisions": [
                        {
                            "reference_id": "r01",
                            "decision": decision,
                            "candidate_id": candidate,
                            "rationale": "Supplied candidate evidence.",
                            "evidence_fields": ["display_name"],
                        }
                    ]
                }
            ),
        )

    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(respond),
        directory=tmp_path,
    )
    report = asyncio.run(runner.run([case]))
    assert report["status"] == "completed"
    output = report["cases"][0]["canonical_output"]
    assert output["decisions"][0]["reference_id"] == "reference-" + "a" * 64
    assert output["decisions"][0]["candidate_id"] == (PLACE_ID if decision == "match" else None)
    assert report["native_identity_adoptions"] == 0


@pytest.mark.parametrize(
    "status,usage", [(500, None), (302, None), (200, (10001, 40)), (200, (120, 4001))]
)
def test_http_or_reported_token_failure_never_retries_or_starts_next_case(tmp_path, status, usage):
    requests = []

    def respond(request):
        requests.append(request)
        raw = (
            sdk_response(profile_output(), input_tokens=usage[0], output_tokens=usage[1])
            if usage
            else {}
        )
        return httpx.Response(status, json=raw, headers={"location": "https://unplanned.example/"})

    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(respond),
        directory=tmp_path,
    )
    report = asyncio.run(runner.run([profile_case(), identity_case()]))
    assert report["status"] == "stopped" and report["model_sends"] == len(requests) == 1
    assert report["attempts"][0]["case"] == "review_profile"
    assert report["stop_reason"]


def test_modified_frozen_wire_is_blocked_before_any_send(tmp_path):
    requests = []
    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(lambda r: requests.append(r)),
        directory=tmp_path,
        frozen_requests={"review_profile": "frozen-original-hash"},
    )
    report = asyncio.run(runner.run([profile_case()]))
    assert report["status"] == "stopped" and report["model_sends"] == 0
    assert not requests
    assert report["stop_reason"] == "Frozen request changed"


def test_full_six_case_packet_is_frozen_and_tampering_is_rejected(tmp_path):
    from tools.validation.short_reference_packet import prepare_packet, validate_packet

    packet = tmp_path / "packet"
    result = asyncio.run(
        prepare_packet(
            packet,
            identity_case().payload,
            source_hashes={},
            revision="revision-fixture",
            endpoint="https://fixture.example/openai/v1/",
        )
    )
    assert result["status"] == "ready" and result["mock_sends"] == 6
    assert result["live_sends"] == 0
    assert len(result["request_hashes"]) == 6 and len(result["mapping_hashes"]) == 6
    validate_packet(
        packet, revision="revision-fixture", endpoint="https://fixture.example/openai/v1/"
    )
    requests = packet / "requests.json"
    requests.write_text(requests.read_text() + " ")
    with pytest.raises(ValueError, match="Frozen file changed"):
        validate_packet(
            packet, revision="revision-fixture", endpoint="https://fixture.example/openai/v1/"
        )


def test_packet_executes_once_and_exports_accounting_without_double_counting(tmp_path):
    from backend.evaluation.usage_report import summarize
    from tools.validation.short_reference_packet import (
        LIMITS,
        execute_packet,
        prepare_packet,
        sha,
    )

    folder = tmp_path / "packet"
    endpoint = "https://fixture.example/openai/v1/"
    asyncio.run(
        prepare_packet(
            folder,
            identity_case().payload,
            source_hashes={},
            revision="revision-fixture",
            endpoint=endpoint,
        )
    )
    (folder / "execution-authorization.json").write_text(
        json.dumps(
            {
                "status": "user_authorized",
                "issue": 66,
                "limits": LIMITS,
                "manifest_sha256": sha(folder / "manifest.json"),
            }
        )
    )
    cases = prepared_cases(identity_case().payload)
    requests = []

    def respond(request):
        output = mock_output(cases[len(requests)])
        requests.append(request)
        return httpx.Response(200, json=sdk_response(output))

    result = asyncio.run(
        execute_packet(
            folder,
            revision="revision-fixture",
            endpoint=endpoint,
            api_key="unused-test-key",
            transport=httpx.MockTransport(respond),
        )
    )
    assert result["status"] == "completed" and len(requests) == 6
    usage = json.loads((folder / "live" / "usage.json").read_text())
    summary = summarize(usage)
    assert summary["observed_model_calls"] == 6 and summary["observed_http_sends"] == 6
    assert summary["observed_token_subtotal"] == 960
    assert summary["repair_model_calls"] == 1
    with pytest.raises(FileExistsError):
        asyncio.run(
            execute_packet(
                folder,
                revision="revision-fixture",
                endpoint=endpoint,
                api_key="unused-test-key",
                transport=httpx.MockTransport(respond),
            )
        )
    assert len(requests) == 6


def test_oversized_input_stops_before_dispatch(tmp_path):
    case = profile_case()
    case.payload["reviews"][0]["text"] = "Large fixture text. " * 12000
    requests = []
    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(lambda r: requests.append(r)),
        directory=tmp_path,
    )
    result = asyncio.run(runner.run([case]))
    assert result["status"] == "stopped" and result["model_sends"] == 0
    assert result["stop_reason"] == "Input token allowance exceeded"
    assert not requests


def test_total_deadline_blocks_first_send(tmp_path):
    ticks = iter([0, 601])
    requests = []
    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(lambda r: requests.append(r)),
        directory=tmp_path,
        clock=lambda: next(ticks),
    )
    result = asyncio.run(runner.run([profile_case()]))
    assert result["status"] == "stopped" and result["model_sends"] == 0
    assert result["stop_reason"] == "Total deadline exhausted"
    assert not requests


def test_read_timeout_is_terminal_with_unknown_fee_preserved(tmp_path):
    requests = []

    def respond(request):
        requests.append(request)
        raise httpx.ReadTimeout("Sensitive provider detail must not enter the summary")

    runner = SmokeRunner(
        endpoint="https://fixture.example/openai/v1/",
        api_key="unused-test-key",
        transport=httpx.MockTransport(respond),
        directory=tmp_path,
    )
    result = asyncio.run(runner.run([profile_case(), identity_case()]))
    assert result["status"] == "stopped" and len(requests) == 1
    assert result["retail_estimate_usd"] is None
    assert result["cost_missing_cases"] == ["review_profile"]
    assert "Sensitive provider detail" not in json.dumps(result)
