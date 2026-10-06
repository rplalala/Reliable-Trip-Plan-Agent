"""Version dispatch through public evaluator seams using synthetic API evidence."""

import asyncio
import copy
import json
import socket

import pytest

from backend.evaluation.controlled_cli import main as controlled_main
from backend.evaluation.identity import identity_references, resolve_identities
from backend.evaluation.identity_cli import main as identity_main
from backend.evaluation.identity_llm import prepare_identity_judgment
from backend.evaluation.preparation import identity_ready
from backend.evaluation.quality_report import build_quality_report
from backend.evaluation.requirement_schedule import score_requirement_schedule
from backend.evaluation.routes import prepare_routes
from backend.evaluation.snapshot import (
    AcquisitionPolicy,
    Response,
    acquire_snapshot,
    build_evidence_plan,
    build_identity_plan,
    identity_evidence,
)
from backend.evaluation.snapshot_coordinates import prepare_snapshot_coordinates
from backend.evaluation.v3_pair_report import build_v3_pair_report
from backend.tests.evaluation.test_identity import details, evidence, prepared, search
from backend.tests.evaluation.test_identity_llm import model_material
from backend.tests.evaluation.test_requirement_schedule import context

pytest_plugins = ("backend.tests.evaluation.test_intake",)


def identified_batch(batch):
    def change(_manifest, results, _save, _root):
        for activity in results["v1"]["itinerary"]["days"][0]["activities"]:
            if activity["activity_kind"] == "main_poi":
                activity["source_place_id"] = "venue-" + activity["activity_id"]
                activity["location"] = "10 Main St, Example City, Country"
        return "v1"

    return prepared(batch, change)


def test_api_exact_match_without_model_and_wrong_address_is_fail(batch):
    intake = identified_batch(batch)
    refs = [r for r in identity_references(intake) if r["version"] == "v1"]
    observed = evidence(intake, [details(r, r["name"], r["claimed_place_id"]) for r in refs])
    original = intake.to_dict()
    report = resolve_identities(intake, observed).to_dict()
    records = [r for r in report["records"] if r["version"] == "v1"]
    assert [r["grounding_verdict"] for r in records] == ["PASS", "PASS"]
    assert all("model_judgment" not in r for r in records)
    assert identity_ready(original, report)
    wrong = copy.deepcopy(observed)
    wrong["records"][0]["details"]["place"]["formatted_address"] = "99 Other St"
    failed = resolve_identities(intake, wrong).to_dict()
    record = next(r for r in failed["records"] if r["reference_id"] == refs[0]["reference_id"])
    assert record["grounding_verdict"] == "FAIL"
    assert record["canonical_place_id"] is None
    assert record["original_claim"]["location"] == "10 Main St, Example City, Country"
    assert intake.to_dict() == original


def test_v0_packet_includes_own_subject_and_program_requirement_needs_no_model(batch):
    manifest, _results, _write, save, root = batch
    spec = json.loads((root / "requirements.json").read_text())
    spec["subjects"] = [
        {"subject_id": "museum", "place_name": "Museum A", "source_place_id": "venue-a"}
    ]
    spec["obligations"] = [
        {
            "obligation_id": "visit",
            "kind": "required_visit",
            "resolution": "resolved",
            "subject_ref": "museum",
            "count": {"mode": "exact", "value": 1},
            "source_refs": [{"field_path": "additional_preferences", "quote": "architecture"}],
        }
    ]
    manifest["groups"][0]["requirement_spec_ref"] = save(
        "requirements.json", spec, spec["schema_version"]
    )
    intake = identified_batch(batch)
    subject = next(r for r in identity_references(intake) if r["kind"] == "requirement_subject")
    observation = details({**subject, "claimed_place_id": "venue-a"}, "Museum A", "venue-a")
    observed = evidence(intake, [observation])
    packet = prepare_identity_judgment(intake, observed, model="fixture-model").to_dict()
    cases = json.loads(packet["request"]["input"])["cases"]
    assert {c["version"] for c in cases} == {"v0"}
    assert {c["kind"] for c in cases} == {"primary_visit", "requirement_subject"}
    record = next(
        r
        for r in resolve_identities(intake, observed).to_dict()["records"]
        if r["kind"] == "requirement_subject" and r["version"] == "v1"
    )
    assert record["grounding_verdict"] == "PASS"
    assert record["canonical_place_id"] == "venue-a"
    assert "model_judgment" not in record


@pytest.mark.parametrize(
    "field,value,expected",
    [
        ("display_name", "Museum a", "FAIL"),
        ("formatted_address", "10 Main St, Example City", "FAIL"),
        ("place_id", "foreign-id", "UNKNOWN"),
    ],
)
def test_exact_comparison_and_provider_id_uncertainty(batch, field, value, expected):
    intake = identified_batch(batch)
    ref = next(r for r in identity_references(intake) if r["version"] == "v1")
    observation = details(ref, ref["name"], ref["claimed_place_id"])
    observation["details"]["place"][field] = value
    record = next(
        r
        for r in resolve_identities(intake, evidence(intake, [observation])).to_dict()["records"]
        if r["reference_id"] == ref["reference_id"]
    )
    assert record["grounding_verdict"] == expected
    assert record["canonical_place_id"] is None


def test_mixed_cli_to_quality_and_pairs_preserves_failure_and_unknown(batch, capsys, monkeypatch):
    manifest, results, write, save, root = batch
    for version in ("v1", "v2", "v3"):
        for activity in results[version]["itinerary"]["days"][0]["activities"]:
            if activity["activity_kind"] == "main_poi":
                activity.update(
                    source_place_id="venue-" + activity["activity_id"],
                    location="10 Main St, Example City, Country",
                )
        write(version)
    results["v3"]["v3"] = {
        "draft": copy.deepcopy(results["v3"]["itinerary"]),
        "final_primary": copy.deepcopy(results["v3"]["itinerary"]),
    }
    results["v3"]["v3"]["draft"]["days"][0]["activities"][0]["location"] = "Wrong address"
    results["v2"]["itinerary"]["days"][0]["activities"][0]["source_place_id"] = "missing"
    results["v1"]["itinerary"]["days"][0]["activities"][2]["location"] = "Wrong address"
    write("v1")
    write("v3")
    write("v2")
    spec = json.loads((root / "requirements.json").read_text())
    spec["subjects"] = [
        {"subject_id": "museum", "place_name": "Museum A", "source_place_id": "venue-a"}
    ]
    spec["obligations"] = [
        {
            "obligation_id": "visit",
            "kind": "required_visit",
            "resolution": "resolved",
            "subject_ref": "museum",
            "count": {"mode": "exact", "value": 1},
            "source_refs": [{"field_path": "additional_preferences", "quote": "architecture"}],
        }
    ]
    manifest["groups"][0]["requirement_spec_ref"] = save(
        "requirements.json", spec, spec["schema_version"]
    )
    intake = prepared(batch)

    def forbidden(*_args, **_kwargs):
        raise AssertionError("Evaluation must remain offline")

    from openai import OpenAI

    monkeypatch.setattr(OpenAI, "__init__", forbidden)

    original_connect = socket.socket.connect

    def offline_connect(sock, address):
        if address[0] in ("127.0.0.1", "::1"):
            return original_connect(sock, address)
        return forbidden()

    monkeypatch.setattr(socket.socket, "connect", offline_connect)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)

    async def transport(request):
        params = request["parameters"]
        if params.get("place_id") == "missing":
            return Response(404, b"{}")
        name = params.get("query") or (
            "Museum A" if params["place_id"] == "venue-a" else "Museum B"
        )
        place = {
            "id": "venue-a" if name == "Museum A" else "venue-b",
            "displayName": {"text": name},
            "formattedAddress": "10 Main St, Example City, Country",
            "location": {"latitude": 1, "longitude": 2},
        }
        return Response(
            200, json.dumps({"places": [place]} if "query" in params else place).encode()
        )

    directory = root / "identity-snapshot"
    snapshot = asyncio.run(
        acquire_snapshot(
            build_identity_plan(intake, paired=True),
            directory,
            transport,
            AcquisitionPolicy(max_sends=20, max_attempts=1),
        )
    )
    observed = identity_evidence(snapshot)
    save("observed.json", observed)
    save("intake.json", intake.to_dict())
    args = [str(write()), str(root / "observed.json")]
    assert identity_main(args) == 3
    report = json.loads(capsys.readouterr().out)
    assert identity_ready(intake.to_dict(), report)
    assert (
        controlled_main(["identity", str(root / "intake.json"), str(root / "observed.json")]) == 3
    )
    assert json.loads(capsys.readouterr().out) == report
    assert identity_main(args + ["--prepare", "--model", "fixture-model"]) == 0
    assert {
        c["version"]
        for c in json.loads(json.loads(capsys.readouterr().out)["request"]["input"])["cases"]
    } == {"v0"}
    # Optional V0 model results do not change any programmatic record.
    judged = resolve_identities(
        intake, observed, model_result=model_material(intake, observed, historical=False)
    ).to_dict()
    assert [r for r in judged["records"] if r["version"] != "v0"] == [
        r for r in report["records"] if r["version"] != "v0"
    ]
    coordinates = prepare_snapshot_coordinates(intake, report, directory).to_dict()
    assert coordinates["status"] == "complete"
    assert {r["grounding_verdict"] for r in coordinates["unadopted_references"]} == {
        "FAIL",
        "UNKNOWN",
    }
    routes = prepare_routes(
        intake, report, context(intake), paired=True, identity_snapshot_directory=directory
    ).to_dict()
    assert routes["status"] == "complete", routes["diagnostics"]
    failed_leg = next(
        r for r in routes["results"] if r["version"] == "v3" and r["projection"] == "draft"
    )["legs"][0]
    assert failed_leg["canonical_endpoints"][0] is None
    assert failed_leg["identity_grounding_verdicts"] == ["FAIL", "PASS"]
    assert failed_leg["expected_context"] is None
    schedule = score_requirement_schedule(intake, report, context(intake), paired=True).to_dict()
    assert schedule["status"] == "complete"
    failed = next(
        r for r in schedule["results"] if r["version"] == "v3" and r["projection"] == "draft"
    )
    assert failed["descriptive"]["identity_checks"][0]["grounding_verdict"] == "FAIL"
    evidence_plan = build_evidence_plan(intake, report, [], paired=True)
    downstream = root / "downstream"
    asyncio.run(
        acquire_snapshot(
            evidence_plan, downstream, transport, AcquisitionPolicy(max_sends=20, max_attempts=1)
        )
    )
    final_directory = root / "downstream-final"
    asyncio.run(
        acquire_snapshot(
            build_evidence_plan(intake, report, []),
            final_directory,
            transport,
            AcquisitionPolicy(max_sends=20, max_attempts=1),
        )
    )
    quality = build_quality_report(
        intake, report, final_directory, context(intake), generated_at="2026-10-06T00:00:00Z"
    ).to_dict()
    assert quality["status"] == "complete", quality["diagnostics"]
    assert quality["groups"][0]["versions"]["v1"]["dimensions"]["grounding"]["counts"] == {
        "PASS": 1,
        "FAIL": 1,
        "UNKNOWN": 0,
    }
    assert quality["groups"][0]["versions"]["v2"]["dimensions"]["grounding"]["counts"] == {
        "PASS": 1,
        "FAIL": 0,
        "UNKNOWN": 1,
    }
    pairs = build_v3_pair_report(
        intake, report, downstream, context(intake), generated_at="2026-10-06T00:00:00Z"
    ).to_dict()
    assert pairs["status"] == "complete", pairs["diagnostics"]
    assert pairs["groups"][0]["stages"]["draft"]["dimensions"]["grounding"]["counts"] == {
        "PASS": 1,
        "FAIL": 1,
        "UNKNOWN": 0,
    }
    assert (
        pairs["groups"][0]["stages"]["draft"]["primary_metrics"]["opening"]["checks"][0][
            "identity_grounding_verdict"
        ]
        == "FAIL"
    )


@pytest.mark.parametrize(
    "mutation", ["verdict", "policy", "version", "claim", "evidence", "stripped"]
)
def test_consumers_reject_forged_and_stale_program_reports(batch, mutation):
    intake = identified_batch(batch)
    ref = next(r for r in identity_references(intake) if r["version"] == "v1")
    report = resolve_identities(
        intake, evidence(intake, [details(ref, ref["name"], ref["claimed_place_id"])])
    ).to_dict()
    assert identity_ready(intake.to_dict(), report)
    target = next(r for r in report["records"] if r["reference_id"] == ref["reference_id"])
    if mutation == "policy":
        report["association_policy_version"] = "structural_claims_typed_addresses_3"
    elif mutation == "stripped":
        del report["identity_versioned_replay"]
        del report["model_judgment_provenance"]
        report["association_policy_version"] = "structural_claims_typed_addresses_3"
        report["status"] = "complete"
    elif mutation == "version":
        target["version"] = "v0"
    elif mutation == "claim":
        target["original_claim"]["location"] = "Repaired"
    elif mutation == "evidence":
        report["identity_versioned_replay"]["evidence"]["records"][0]["details"][
            "requested_place_id"
        ] = "stale"
    else:
        target["grounding_verdict"] = "FAIL"
    assert not identity_ready(intake.to_dict(), report)
    with pytest.raises(ValueError):
        build_evidence_plan(intake, report, [])


def test_current_resolver_rejects_historical_and_foreign_v0_material(batch):
    intake = identified_batch(batch)
    observed = evidence(intake, [])
    with pytest.raises(ValueError, match="packet/source mismatch"):
        resolve_identities(intake, observed, model_result=model_material(intake, observed))
    foreign = model_material(intake, observed, historical=False)
    foreign["packet"]["association_policy_version"] = "llm_identity_judgment_2"
    with pytest.raises(ValueError, match="packet/source mismatch"):
        resolve_identities(intake, observed, model_result=foreign)


@pytest.mark.parametrize(
    "field,value", [("source_place_id", None), ("location", None), ("place_name", None)]
)
def test_proven_missing_output_fields_fail_even_without_api_evidence(batch, field, value):
    def change(_manifest, results, _save, _root):
        results["v1"]["itinerary"]["days"][0]["activities"][0].update(
            source_place_id="venue-a", location="10 Main St, Example City, Country"
        )
        results["v1"]["itinerary"]["days"][0]["activities"][0][field] = value
        return "v1"

    intake = prepared(batch, change)
    record = next(
        r
        for r in resolve_identities(intake, evidence(intake, [])).to_dict()["records"]
        if r["version"] == "v1"
    )
    assert record["grounding_verdict"] == "FAIL"


@pytest.mark.parametrize("fault", ["missing", "provider_error", "requested_id", "planner"])
def test_api_provenance_and_acquisition_failures_do_not_become_pass(batch, fault):
    intake = identified_batch(batch)
    ref = next(r for r in identity_references(intake) if r["version"] == "v1")
    observation = details(ref, ref["name"], ref["claimed_place_id"])
    if fault == "provider_error":
        observation["details"] = {"status": "provider_error"}
    elif fault == "requested_id":
        observation["details"]["requested_place_id"] = "another-request"
    elif fault == "planner":
        observation["source_kind"] = "planner_cache"
    observed = evidence(intake, [] if fault == "missing" else [observation])
    if fault == "planner":
        with pytest.raises(ValueError, match="independent source"):
            resolve_identities(intake, observed)
    else:
        record = next(
            r
            for r in resolve_identities(intake, observed).to_dict()["records"]
            if r["reference_id"] == ref["reference_id"]
        )
        assert record["grounding_verdict"] == "UNKNOWN"
        assert record["canonical_place_id"] is None


@pytest.mark.parametrize(
    "variant",
    [
        "exact",
        "ambiguous",
        "null_components",
        "wrong_components",
        "conflicting_components",
        "wrong_query",
    ],
)
def test_unbound_requirement_uncertainty_is_local_and_cli_continues(batch, capsys, variant):
    manifest, _results, write, save, root = batch
    spec = json.loads((root / "requirements.json").read_text())
    spec["subjects"] = [{"subject_id": "museum", "place_name": "Museum A"}]
    spec["obligations"] = [
        {
            "obligation_id": "visit",
            "kind": "required_visit",
            "resolution": "resolved",
            "subject_ref": "museum",
            "count": {"mode": "exact", "value": 1},
            "source_refs": [{"field_path": "additional_preferences", "quote": "architecture"}],
        }
    ]
    manifest["groups"][0]["requirement_spec_ref"] = save(
        "requirements.json", spec, spec["schema_version"]
    )
    intake = identified_batch(batch)
    refs = identity_references(intake)
    subject = next(r for r in refs if r["kind"] == "requirement_subject")
    observation = search(subject, "Museum A", place_id="venue-a")
    candidate = observation["search"]["candidates"][0]
    if variant == "ambiguous":
        observation["search"]["actual_result_count"] = 2
    elif variant == "null_components":
        candidate["address_components"] = None
    elif variant == "wrong_components":
        candidate["address_components"] = "bad"
    elif variant == "conflicting_components":
        candidate["address_components"] = [
            {"longText": "Example City", "types": ["locality"]},
            {"longText": "Other City", "types": ["locality"]},
        ]
    elif variant == "wrong_query":
        observation["search"]["query"] = "another search"
    observed = evidence(
        intake,
        [observation]
        + [details(r, r["name"], r["claimed_place_id"]) for r in refs if r["version"] == "v1"],
    )
    save("observed.json", observed)
    code = identity_main([str(write()), str(root / "observed.json")])
    out = json.loads(capsys.readouterr().out)
    assert code == 3, out
    assert identity_ready(intake.to_dict(), out)
    record = next(
        r for r in out["records"] if r["kind"] == "requirement_subject" and r["version"] == "v1"
    )
    assert record["grounding_verdict"] == ("PASS" if variant == "exact" else "UNKNOWN")
    assert [
        r["grounding_verdict"]
        for r in out["records"]
        if r["version"] == "v1" and r["kind"] == "primary_visit"
    ] == [
        "PASS",
        "PASS",
    ]
