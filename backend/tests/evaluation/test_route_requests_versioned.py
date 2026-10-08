"""Current-policy V0 route preparation through public offline interfaces."""

import asyncio
import json
import socket
from datetime import UTC, datetime

import pytest

from backend.evaluation.identity import resolve_identities
from backend.evaluation.identity_adoption import load_v0_material
from backend.evaluation.identity_program import resolve_versioned_identities
from backend.evaluation.records import thaw
from backend.evaluation.snapshot import AcquisitionPolicy, Response, acquire_snapshot
from backend.evaluation.tools.route_requests import (
    preflight_v0_route_requests,
    prepare_v0_route_requests,
)
from backend.evaluation.tools.route_requests_cli import main
from backend.tests.evaluation.test_identity_llm import model_material
from backend.tests.evaluation.test_requirement_schedule import context
from backend.tests.evaluation.test_route_requests import reviewed_identity

pytest_plugins = (
    "backend.tests.evaluation.test_intake",
    "backend.tests.evaluation.test_identity_adoption",
)


def current_identity(case, decisions=None):
    intake, observed = case[:2]
    result = model_material(intake, observed, historical=False, decisions=decisions)
    return resolve_identities(intake, observed, model_result=result).to_dict()


@pytest.mark.parametrize("legacy", [False, True])
@pytest.mark.parametrize(
    "prepared_at, complete",
    [
        ("2026-10-06T08:59:59Z", False),
        ("2026-10-06T09:00:00Z", True),
        ("2026-10-06T09:00:01Z", True),
    ],
)
def test_snapshot_time_boundary_is_stable_for_current_and_legacy_routes(
    adoption_case, prepared_at, complete, legacy
):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = reviewed_identity(adoption_case) if legacy else current_identity(adoption_case)
    report = prepare_v0_route_requests(
        bundle, identity, prepared_at=prepared_at, schedule_context=context(intake), legacy=legacy
    ).to_dict()
    if complete:
        assert report["status"] == "complete", report["diagnostics"]
        assert report["counts"]["actual_sends"] == 0
    else:
        assert report["status"] == "needs_material_correction"
        assert report["requests"] == report["legs"] == []
        assert report["diagnostics"] == [
            {
                "reason": "artifact_integrity_error",
                "pointer": "snapshot/time",
                "explanation": "Identity evidence is later than preparation",
            }
        ]


@pytest.mark.parametrize("adoption_case", [{"coordinates_missing": True}], indirect=True)
@pytest.mark.parametrize("legacy", [False, True])
@pytest.mark.parametrize("second, complete", [(0, True), (1, False)])
def test_supplied_details_after_preparation_are_rejected_with_a_controlled_clock(
    adoption_case, snapshot_clock, tmp_path, legacy, second, complete
):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = reviewed_identity(adoption_case) if legacy else current_identity(adoption_case)
    before = prepare_v0_route_requests(
        bundle,
        identity,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        legacy=legacy,
    ).to_dict()
    assert before["counts"]["details_requests"] == 2
    snapshot_clock.instant = datetime(2026, 10, 6, 10, 0, second, tzinfo=UTC)

    async def respond(request):
        return Response(
            200,
            json.dumps(
                {
                    "id": request["parameters"]["place_id"],
                    "location": {"latitude": 10, "longitude": 20},
                }
            ).encode(),
        )

    directory = tmp_path / "timed-details"
    asyncio.run(
        acquire_snapshot(
            before["details_plan"], directory, respond, AcquisitionPolicy(2, max_attempts=1)
        )
    )
    report = prepare_v0_route_requests(
        bundle,
        identity,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        legacy=legacy,
        details_snapshot_directory=directory,
    ).to_dict()
    if complete:
        assert report["status"] == "complete", report["diagnostics"]
        assert report["counts"]["actual_sends"] == 0
        assert report["counts"]["supplied_details_observed_sends"] == 2
    else:
        assert report["status"] == "needs_material_correction"
        assert report["requests"] == report["legs"] == []
        assert report["diagnostics"] == [
            {
                "reason": "artifact_integrity_error",
                "pointer": "details/time",
                "explanation": "Details evidence is later than preparation",
            }
        ]


def test_missing_current_model_evidence_retains_original_blocked_leg(adoption_case, monkeypatch):
    intake, _, bundle, _, _, _, _, _ = adoption_case

    def forbidden(*args, **kwargs):
        raise AssertionError("Offline route preparation cannot connect or resolve hosts")

    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)
    report = prepare_v0_route_requests(
        bundle, None, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()
    assert report["status"] == "complete", report
    assert len(report["legs"]) == 1
    leg = report["legs"][0]
    assert leg["canonical_endpoints"] == [None, None]
    assert leg["identity_eligible"] is False
    assert leg["verdict"] == "UNKNOWN"
    assert {r["reason"] for r in leg["identity_blockers"]} == {"model_judgment_missing"}
    assert report["requests"] == []
    assert report["counts"]["actual_sends"] == report["counts"]["ready_routes"] == 0
    assert report["counts"]["reused_coordinates"] == 0
    assert report["budget"]["proposed_usd"] == "0.000000"


def test_historical_adoption_requires_explicit_legacy_replay(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    historical = reviewed_identity(adoption_case)
    rejected = prepare_v0_route_requests(
        bundle, historical, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()
    assert rejected["status"] == "needs_material_correction"
    assert rejected["requests"] == []
    legacy = prepare_v0_route_requests(
        bundle,
        historical,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        legacy=True,
    ).to_dict()
    assert legacy["status"] == "complete"
    assert legacy["replay_inputs"]["legacy"] is True


@pytest.mark.parametrize("adoption_case", [{"pagination": True}], indirect=True)
def test_historical_paginated_v0_bundle_replays_without_changing_current_evidence(adoption_case):
    intake, observed, bundle, _, _, _, _, _ = adoption_case
    historical = reviewed_identity(adoption_case)
    assert load_v0_material(intake, bundle, historical=True).evidence is not None
    current = load_v0_material(intake, bundle)
    assert all(
        r["search"]["next_page_token"] == "remaining-page"
        for r in thaw(current.evidence)["records"]
    )
    assert all("next_page_token" not in r["search"] for r in observed["records"])
    replay = prepare_v0_route_requests(
        bundle,
        historical,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        legacy=True,
    ).to_dict()
    assert replay["status"] == "complete", replay["diagnostics"]
    assert replay["counts"]["reused_coordinates"] == 2


@pytest.mark.parametrize("adoption_case", [{"pagination": True}], indirect=True)
def test_policy_two_route_replay_retains_its_current_pagination_wire(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    observed = thaw(load_v0_material(intake, bundle).evidence)
    material = model_material(intake, observed, historical=False)
    identity = resolve_versioned_identities(
        intake, observed, model_result=material, previous=True
    ).to_dict()
    report = prepare_v0_route_requests(
        bundle,
        identity,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        legacy=True,
    ).to_dict()
    assert report["status"] == "complete", report["diagnostics"]
    assert report["counts"]["reused_coordinates"] == 2


@pytest.mark.parametrize("adoption_case", [{"high_impact": True}], indirect=True)
def test_current_matches_need_no_human_identity_gate_and_reuse_independent_points(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = current_identity(adoption_case)
    assert identity["review_queue"] == [] and identity["review_hash"] is None
    report = prepare_v0_route_requests(
        bundle, identity, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()
    assert report["status"] == "complete"
    assert report["identity_policy"] == {
        "association_policy_version": "versioned_api_identity_3",
        "legacy": False,
        "current_v0_model_result_present": True,
        "report_origin": "supplied",
    }
    assert report["counts"]["eligible_endpoint_occurrences"] == 2
    assert report["counts"]["eligible_endpoint_venues"] == 2
    assert report["counts"]["reused_coordinates"] == 2
    assert report["legs"][0]["identity_eligible"] is True
    assert report["legs"][0]["identity_grounding_verdicts"] == ["PASS", "PASS"]
    assert report["legs"][0]["request"]["body"]["travelMode"] == "WALK"
    assert report["legs"][0]["verdict"] == "UNKNOWN"
    assert report["counts"]["ready_routes"] == 0


@pytest.mark.parametrize(
    "adoption_case", [{"claimed_location": "Wrong original address"}], indirect=True
)
@pytest.mark.parametrize("verdict", ["FAIL", "UNKNOWN"])
def test_trusted_failed_claim_can_use_physical_evidence_but_unknown_cannot(adoption_case, verdict):
    intake, _, bundle, _, _, _, _, _ = adoption_case

    def choose(row, case):
        if case["claim"]["location"]:
            if verdict == "FAIL":
                row.update(address_assessment="incorrect_claim")
                row["evidence_fields"].append("claim.location")
            else:
                row.update(
                    decision="unknown",
                    candidate_id=None,
                    evidence_fields=[],
                    address_assessment="unknown",
                    destination_assessment="unknown",
                )

    identity = current_identity(adoption_case, choose)
    report = prepare_v0_route_requests(
        bundle, identity, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()
    assert report["status"] == "complete"
    leg = report["legs"][0]
    associated = verdict == "FAIL"
    assert leg["canonical_endpoints"] == [
        "canonical-Museum A" if associated else None,
        "canonical-Museum B",
    ]
    assert leg["identity_grounding_verdicts"] == [verdict, "PASS"]
    assert leg["identity_blockers"] == (
        []
        if associated
        else [
            {
                "reference_id": identity["records"][0]["reference_id"],
                "reason": identity["records"][0]["reason"],
                "grounding_verdict": verdict,
            }
        ]
    )
    assert leg["identity_endpoints"][0]["original_claim"]["location"] == "Wrong original address"
    assert leg["verdict"] == "UNKNOWN"
    assert (leg["request"] is not None) == associated
    assert report["counts"]["eligible_endpoint_occurrences"] == (2 if associated else 1)
    assert report["counts"]["reused_coordinates"] == (2 if associated else 1)
    assert {p["place_id"] for p in report["coordinates"]} == (
        {"canonical-Museum A", "canonical-Museum B"} if associated else {"canonical-Museum B"}
    )


def test_cli_without_current_report_retains_blockers_and_rejects_implicit_legacy(
    adoption_case, capsys
):
    _, _, bundle, _, save, _, _, _ = adoption_case
    assert main([str(bundle), "--prepared-at", "2026-10-06T10:00:00Z"]) == 3
    report = json.loads(capsys.readouterr().out)
    assert len(report["legs"]) == 1 and report["counts"]["actual_sends"] == 0
    assert report["identity_policy"]["report_origin"] == "derived_without_model_result"
    path = (
        bundle.parent
        / save("historical-identity.json", reviewed_identity(adoption_case).to_dict())["path"]
    )
    args = [str(bundle), str(path), "--prepared-at", "2026-10-06T10:00:00Z"]
    assert main(args) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "needs_material_correction"
    assert main([*args, "--legacy"]) == 3
    assert json.loads(capsys.readouterr().out)["identity_policy"]["legacy"] is True


@pytest.mark.parametrize("fault", ["verdict", "evidence", "source", "snapshot"])
def test_current_replay_rejects_changed_report_or_source_without_partial_inventory(
    adoption_case, fault
):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = current_identity(adoption_case)
    if fault == "verdict":
        identity["records"][0]["grounding_verdict"] = "FAIL"
    elif fault == "evidence":
        identity["identity_versioned_replay"]["evidence"]["records"][0]["observation_id"] = (
            "foreign"
        )
    elif fault == "source":
        (bundle.parent / "v0.json").write_text("{}", encoding="utf-8")
    else:
        next((bundle.parent / "identity-snapshot/raw").glob("*")).write_bytes(b"corrupt")
    report = prepare_v0_route_requests(
        bundle, identity, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["legs"] == report["requests"] == []


@pytest.mark.parametrize(
    "adoption_case", [{"shared_venue": True, "coordinates_missing": True}], indirect=True
)
def test_current_details_deduplicate_venue_without_losing_endpoint_occurrences(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        current_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
    ).to_dict()
    assert report["status"] == "complete"
    assert report["counts"]["eligible_endpoint_occurrences"] == 2
    assert report["counts"]["eligible_endpoint_venues"] == report["counts"]["details_requests"] == 1
    assert len(report["requests"][0]["reference_ids"]) == 2
    assert report["requests"][0]["field_mask"] == "id,location"
    assert report["legs"][0]["verdict"] == "N/A"


@pytest.mark.parametrize(
    "adoption_case", [{"transport_mode": "TRANSIT"}, {"transport_mode": "DRIVE"}], indirect=True
)
def test_current_provider_time_blockers_keep_original_mode_and_departure(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        current_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
    ).to_dict()
    assert report["status"] == "complete"
    leg = report["legs"][0]
    assert leg["submitted_departure"] == "2020-01-01T10:00:00+00:00"
    assert leg["verdict"] == "UNKNOWN" and report["counts"]["ready_routes"] == 0
    if leg["mode"] == "TRANSIT":
        assert leg["request_state"] == "conditional"
        assert leg["request"]["body"]["departureTime"] == "2020-01-01T10:00:00+00:00"
        assert "historical_matrix_transit_availability_unverified" in leg["readiness_checks"]
    else:
        assert leg["mode"] == "DRIVE" and leg["request_state"] == "blocked"
        assert leg["request"]["body"] is None
        assert "regional_drive_unavailable_or_low_quality" in leg["readiness_checks"]


@pytest.mark.parametrize("adoption_case", [{"coordinates_missing": True}], indirect=True)
@pytest.mark.parametrize("fault", ["wrong_id", "invalid_coordinate", "missing_coordinate"])
def test_current_supplied_details_block_bad_coordinates_without_backfill(
    adoption_case, tmp_path, fault
):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = current_identity(adoption_case)
    before = prepare_v0_route_requests(
        bundle, identity, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()
    assert before["counts"]["details_requests"] == 2

    async def respond(request):
        pid = request["parameters"]["place_id"]
        body = {"id": pid, "location": {"latitude": 10, "longitude": 20}}
        if pid == "canonical-Museum A":
            if fault == "wrong_id":
                body["id"] = "foreign"
            elif fault == "invalid_coordinate":
                body["location"]["latitude"] = True
            else:
                body.pop("location")
        return Response(200, json.dumps(body).encode())

    snapshot = tmp_path / "current-details"
    asyncio.run(
        acquire_snapshot(
            before["details_plan"], snapshot, respond, AcquisitionPolicy(2, max_attempts=1)
        )
    )
    report = prepare_v0_route_requests(
        bundle,
        identity,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        details_snapshot_directory=snapshot,
    ).to_dict()
    assert report["status"] == "complete"
    assert {p["place_id"] for p in report["coordinates"]} == {"canonical-Museum B"}
    assert report["legs"][0]["coordinate_ready"] is False
    assert report["legs"][0]["request"]["body"] is None
    assert report["counts"]["details_requests"] == report["counts"]["actual_sends"] == 0


@pytest.mark.parametrize("adoption_case", [{"shared_venue": True}], indirect=True)
def test_current_conflicting_coordinates_block_reuse_without_new_details(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        current_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
    ).to_dict()
    assert report["status"] == "complete"
    assert report["counts"]["reused_coordinates"] == report["counts"]["details_requests"] == 0
    assert report["coordinate_diagnostics"][0]["reason"] == "coordinates_conflicting"


@pytest.mark.parametrize("adoption_case", [{"repeat_visits": True}], indirect=True)
def test_current_duplicate_matrix_query_retains_every_original_directed_leg(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        current_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
    ).to_dict()
    assert report["status"] == "complete"
    assert len(report["legs"]) == 3
    assert report["counts"]["eligible_endpoint_occurrences"] == 6
    assert report["counts"]["eligible_endpoint_venues"] == 2
    assert report["counts"]["directed_route_requests"] == 2
    assert sorted(len(r["leg_ids"]) for r in report["requests"]) == [1, 2]
    assert report["budget"]["unready_routes_usd"] == "0.010000"
    assert report["budget"]["proposed_usd"] == "0.000000"


@pytest.mark.parametrize("adoption_case", [{"coordinates_missing": True}], indirect=True)
def test_current_preflight_replays_exact_inventory_without_authorizing_sends(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = current_identity(adoption_case)
    report = prepare_v0_route_requests(
        bundle, identity, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()
    ledger = {
        "sent_request_keys": [],
        "elapsed_seconds": 0,
        "cost_usd": "0.000000",
        "retry_sends": 0,
        "search_sends": 0,
        "model_sends": 0,
    }
    result = preflight_v0_route_requests(
        bundle, identity, report, ledger=ledger, next_request_key=report["requests"][0]["key"]
    )
    assert result == {"status": "within_prepared_limits", "live_authorized": False, "reasons": []}
    report["identity_policy"]["legacy"] = True
    result = preflight_v0_route_requests(
        bundle, identity, report, ledger=ledger, next_request_key=report["requests"][0]["key"]
    )
    assert result["status"] == "stopped" and result["live_authorized"] is False
    assert result["reasons"] == ["package_replay_mismatch"]
