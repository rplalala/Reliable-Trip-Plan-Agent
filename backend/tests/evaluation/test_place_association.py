"""Claim failures and independent physical evidence through evaluator public seams."""

import asyncio
import copy
import json

import pytest

from backend.evaluation.identity import identity_references, resolve_identities
from backend.evaluation.identity_cli import main as identity_main
from backend.evaluation.identity_program import resolve_versioned_identities
from backend.evaluation.opening import score_opening
from backend.evaluation.preparation import identity_ready
from backend.evaluation.routes import prepare_routes, score_routes
from backend.evaluation.snapshot import (
    AcquisitionPolicy,
    Response,
    acquire_snapshot,
    build_evidence_plan,
)
from backend.tests.evaluation.test_identity import details, evidence, prepared, search
from backend.tests.evaluation.test_identity_llm import model_material
from backend.tests.evaluation.test_identity_program import identified_batch
from backend.tests.evaluation.test_requirement_schedule import context
from backend.tests.evaluation.test_routes import reviews

pytest_plugins = ("backend.tests.evaluation.test_intake",)


@pytest.mark.parametrize("version", ["v1", "v2", "v3"])
def test_program_fail_checks_api_hours_and_original_drive_without_repair(
    batch, version, monkeypatch
):
    def change(_manifest, results, _save, _root):
        itinerary = results[version]["itinerary"]
        for a in itinerary["days"][0]["activities"]:
            if a["activity_kind"] == "main_poi":
                a.update(
                    source_place_id="venue-" + a["activity_id"],
                    location="10 Main St, Example City, Country",
                )
        itinerary["days"][0]["activities"][0]["location"] = "Wrong address"
        itinerary["transfers"] = [
            {
                "from_activity_id": "a",
                "to_activity_id": "b",
                "mode": "DRIVE",
                "departure_time": "2020-01-01T10:00:00Z",
            }
        ]
        return version

    intake = prepared(batch, change)
    original = intake.to_dict()
    refs = [r for r in identity_references(intake) if r["version"] == version]
    report = resolve_identities(
        intake, evidence(intake, [details(r, r["name"], r["claimed_place_id"]) for r in refs])
    ).to_dict()
    coords = {
        "schema_version": "rtpeval_route_coordinates_1",
        "batch_id": "batch",
        "revision": "1",
        "records": [
            {
                "place_id": r["claimed_place_id"],
                "latitude": 1,
                "longitude": 2,
                "evidence_sha256": "a" * 64,
                "source_ref": "independent-fixture",
                "reviewer_ref": "fixture",
                "reviewed_at": "2020-01-01T00:00:00Z",
            }
            for r in refs
        ],
    }
    route_review = reviews(intake)
    plan = prepare_routes(
        intake, report, context(intake), route_reviews=route_review, coordinate_evidence=coords
    ).to_dict()
    assert plan["status"] == "complete", plan["diagnostics"]
    monkeypatch.setattr("backend.evaluation.snapshot._now", lambda: "2020-01-01T00:00:00Z")

    async def transport(request):
        payload = (
            [
                {
                    "originIndex": 0,
                    "destinationIndex": 0,
                    "status": {"code": 0},
                    "condition": "ROUTE_EXISTS",
                    "duration": "300s",
                    "distanceMeters": 500,
                }
            ]
            if request["operation"] == "route_matrix"
            else {
                "id": request["parameters"]["place_id"],
                "timeZone": {"id": "Etc/UTC"},
                "regularOpeningHours": {
                    "periods": [
                        {
                            "open": {"day": 3, "hour": 9, "minute": 0},
                            "close": {"day": 3, "hour": 17, "minute": 0},
                        }
                    ]
                },
            }
        )
        return Response(200, json.dumps(payload).encode())

    directory = batch[4] / "downstream"
    asyncio.run(
        acquire_snapshot(
            plan["evidence_plan"], directory, transport, AcquisitionPolicy(20, max_attempts=1)
        )
    )
    opening = score_opening(intake, report, directory, context(intake)).to_dict()
    opened = next(r for r in opening["results"] if r["version"] == version)["opening"]["checks"][0]
    assert opened["state"] == "PASS"
    assert opened["identity_grounding_verdict"] == "FAIL"
    assert opened["canonical_place_id"] is None
    assert opened["associated_place_id"] == "venue-a"
    routes = score_routes(
        intake,
        report,
        directory,
        context(intake),
        route_reviews=route_review,
        coordinate_evidence=coords,
    ).to_dict()
    driven = next(r for r in routes["results"] if r["version"] == version)["routes"]["checks"][0]
    assert driven["state"] == "PASS"
    assert driven["mode"] == "DRIVE"
    assert driven["identity_grounding_verdicts"] == ["FAIL", "PASS"]
    assert driven["reserve_seconds"] == 600
    assert all("model_judgment" not in r for r in report["records"] if r["version"] == version)
    assert intake.to_dict() == original


def test_verified_original_id_enables_details_without_repairing_address(batch):
    intake = identified_batch(batch)
    original = intake.to_dict()
    ref = next(r for r in identity_references(intake) if r["version"] == "v1")
    observation = details(ref, ref["name"], ref["claimed_place_id"])
    observation["details"]["place"]["formatted_address"] = "99 Other St"
    report = resolve_identities(intake, evidence(intake, [observation])).to_dict()
    record = next(r for r in report["records"] if r["reference_id"] == ref["reference_id"])
    assert record["grounding_verdict"] == "FAIL"
    assert record["canonical_place_id"] is None
    assert record["place_association"] == {
        "state": "verified",
        "place_id": ref["claimed_place_id"],
        "reason": "independent_api_id_verified",
    }
    assert identity_ready(original, report)
    plan = build_evidence_plan(intake, report, [])
    request = next(r for r in plan["references"] if r["reference_id"] == ref["reference_id"])
    assert request["requests"]["details"]
    assert request["canonical_place_id"] is None
    assert request["associated_place_id"] == ref["claimed_place_id"]
    assert intake.to_dict() == original
    forged = copy.deepcopy(report)
    next(r for r in forged["records"] if r["reference_id"] == ref["reference_id"])[
        "place_association"
    ]["place_id"] = "foreign"
    assert not identity_ready(original, forged)


@pytest.mark.parametrize("version", ["v1", "v2", "v3"])
@pytest.mark.parametrize("field", ["place_name", "location"])
def test_missing_original_claim_field_does_not_prevent_independent_id_check(batch, version, field):
    def change(_manifest, results, _save, _root):
        activity = results[version]["itinerary"]["days"][0]["activities"][0]
        activity.update(source_place_id="venue-a", location="Wrong address")
        activity[field] = None
        return version

    intake = prepared(batch, change)
    ref = next(r for r in identity_references(intake) if r["version"] == version)
    observation = details(ref, "Museum A", "venue-a")
    report = resolve_identities(intake, evidence(intake, [observation])).to_dict()
    record = next(r for r in report["records"] if r["reference_id"] == ref["reference_id"])
    assert record["grounding_verdict"] == "FAIL"
    assert record["place_association"]["place_id"] == "venue-a"
    assert "model_judgment" not in record


@pytest.mark.parametrize("fault", ["missing", "requested_id", "returned_id", "time", "search_only"])
def test_unverified_id_never_uses_search_as_repair(batch, fault):
    intake = identified_batch(batch)
    ref = next(r for r in identity_references(intake) if r["version"] == "v1")
    observation = details(ref, ref["name"], ref["claimed_place_id"])
    if fault == "missing":
        observation["details"] = {"status": "unavailable"}
    elif fault == "requested_id":
        observation["details"]["requested_place_id"] = "foreign"
    elif fault == "returned_id":
        observation["details"]["place"]["place_id"] = "foreign"
    elif fault == "time":
        observation["details"]["retrieved_at"] = "not-a-timestamp"
    else:
        observation = search(ref, ref["name"], place_id=ref["claimed_place_id"])
    report = resolve_identities(intake, evidence(intake, [observation])).to_dict()
    record = next(r for r in report["records"] if r["reference_id"] == ref["reference_id"])
    assert record["place_association"]["state"] == "UNKNOWN"
    assert record["place_association"]["place_id"] is None
    reference = next(
        r
        for r in build_evidence_plan(intake, report, [])["references"]
        if r["reference_id"] == ref["reference_id"]
    )
    assert reference["requests"] == {}


@pytest.mark.parametrize("decision", ["unknown", "no_supported_match"])
def test_candidate_presence_never_substitutes_for_v0_correspondence(batch, decision):
    intake = prepared(batch)
    refs = [r for r in identity_references(intake) if r["version"] == "v0"]
    observed = evidence(intake, [search(r, r["name"]) for r in refs])

    def choose(row, _case):
        row.update(decision=decision, candidate_id=None, evidence_fields=["case.candidates"])

    material = model_material(intake, observed, historical=False, decisions=choose)
    report = resolve_identities(intake, observed, model_result=material).to_dict()
    assert all(
        r["place_association"]["state"] == "UNKNOWN"
        for r in report["records"]
        if r["version"] == "v0"
    )


def test_previous_policy_cli_and_consumers_retain_fail_blocker(batch, capsys):
    intake = identified_batch(batch)
    ref = next(r for r in identity_references(intake) if r["version"] == "v1")
    observation = details(ref, ref["name"], ref["claimed_place_id"])
    observation["details"]["place"]["formatted_address"] = "Wrong address"
    observed = evidence(intake, [observation])
    old = resolve_versioned_identities(intake, observed, previous=True).to_dict()
    assert old["association_policy_version"] == "versioned_api_identity_2"
    assert identity_ready(intake.to_dict(), old)
    assert all("place_association" not in r for r in old["records"])
    old_plan = build_evidence_plan(intake, old, [])
    assert (
        next(r for r in old_plan["references"] if r["reference_id"] == ref["reference_id"])[
            "requests"
        ]
        == {}
    )
    root = batch[4]
    (root / "evidence.json").write_text(json.dumps(observed), encoding="utf-8")
    assert (
        identity_main(
            [str(root / "manifest.json"), str(root / "evidence.json"), "--historical-association"]
        )
        == 3
    )
    assert json.loads(capsys.readouterr().out) == old


def test_association_marker_cannot_bypass_replay_by_claiming_legacy_policy(batch):
    intake = identified_batch(batch)
    report = resolve_identities(intake, evidence(intake, [])).to_dict()
    report.update(
        association_policy_version="structural_claims_typed_addresses_3",
        status="complete",
        audit_plan_hash="a" * 64,
    )
    del report["identity_versioned_replay"]
    del report["model_judgment_provenance"]
    for record in report["records"]:
        for key in ("programmatic_judgment", "model_judgment", "candidate_correspondence"):
            record.pop(key, None)
        record["high_impact"] = False
    report["records"][0]["place_association"] = {
        "state": "verified",
        "place_id": "forged",
        "reason": "forged",
    }
    assert not identity_ready(intake.to_dict(), report)
