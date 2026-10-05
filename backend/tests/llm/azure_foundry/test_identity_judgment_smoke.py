"""Frozen development smoke through the SDK and offline HTTP boundary."""

import asyncio
import json

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


def output(plan, *, failure=False):
    rows = []
    for case in json.loads(plan["wire_request"]["input"])["cases"]:
        rows.append(
            {
                "reference_id": case["reference_id"],
                "decision": "unknown",
                "candidate_id": None,
                "rationale": "Insufficient independent facts.",
                "evidence_fields": [],
                "address_assessment": "unknown",
                "destination_assessment": "unknown",
            }
        )
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
    assert all(r["grounding_verdict"] == "UNKNOWN" for r in report["records"][1:])
    assert report["review_queue"] == []
    with pytest.raises(FileExistsError):
        run(plan, lambda _: pytest.fail("Repeated execution"))


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
