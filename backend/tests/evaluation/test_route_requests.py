"""Offline V0 route acquisition preparation at its public boundaries."""

import asyncio
import json
import socket

import pytest

from backend.evaluation.identity_adoption import resolve_v0_identities
from backend.evaluation.route_requests import preflight_v0_route_requests, prepare_v0_route_requests
from backend.evaluation.snapshot import AcquisitionPolicy, Response, acquire_snapshot
from backend.tests.evaluation.test_identity import review_envelope
from backend.tests.evaluation.test_requirement_schedule import context

pytest_plugins = (
    "backend.tests.evaluation.test_intake",
    "backend.tests.evaluation.test_identity_adoption",
)


def reviewed_identity(case):
    intake, observed, bundle, _, _, _, refs, _ = case
    by_ref = {r["reference_id"]: r for r in observed["records"]}
    records = []
    for ref in refs:
        rid = ref["reference_id"]
        pid = by_ref[rid]["search"]["candidates"][0]["place_id"]
        records.extend(review_envelope(intake, by_ref[rid], rid, pid)["records"])
    reviews = {
        "schema_version": "rtpeval_identity_reviews_1",
        "batch_id": "batch",
        "batch_revision": "1",
        "records": records,
    }
    return resolve_v0_identities(intake, bundle, reviews)


def test_pending_identity_stays_visible_and_preparation_has_no_network(adoption_case, monkeypatch):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = resolve_v0_identities(intake, bundle)

    def forbidden(*args, **kwargs):
        raise AssertionError("Request preparation must send zero billable calls")

    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)
    report = prepare_v0_route_requests(
        bundle, identity, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()
    assert report["status"] == "complete"
    assert len(report["legs"]) == 1
    assert report["legs"][0]["identity_eligible"] is False
    assert report["legs"][0]["verdict"] == "UNKNOWN"
    assert report["counts"]["actual_sends"] == 0
    assert report["counts"]["details_requests"] == 0
    assert report["counts"]["ready_routes"] == 0
    assert report["counts"]["reused_coordinates"] == 1


@pytest.mark.parametrize("adoption_case", [{"coordinates_missing": True}], indirect=True)
def test_missing_coordinates_prepare_exact_details_and_conditional_routes(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        reviewed_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
    ).to_dict()
    assert report["counts"]["details_requests"] == 2
    assert report["counts"]["missing_coordinate_venues"] == 2
    details = [r for r in report["requests"] if r["operation"] == "places_details"]
    assert {r["parameters"]["place_id"] for r in details} == {
        "canonical-Museum A",
        "canonical-Museum B",
    }
    assert all(r["field_mask"] == "id,location" for r in details)
    leg = report["legs"][0]
    assert leg["request_state"] == "blocked"
    assert leg["request"]["body"] is None
    assert "independent_coordinates_missing" in leg["readiness_checks"]
    assert "regional_walk_unavailable_or_low_quality" in leg["readiness_checks"]
    assert report["budget"]["proposed_usd"] == "0.010000"
    assert report["budget"]["unready_routes_usd"] == "0.005000"


@pytest.mark.parametrize("adoption_case", [{"coordinates_missing": True}], indirect=True)
@pytest.mark.parametrize(
    "fault,ready",
    [(None, True), ("id", False), ("boolean", False), ("range", False), ("missing", False)],
)
def test_supplied_details_require_exact_identity_and_numeric_coordinates(
    adoption_case, tmp_path, fault, ready
):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = reviewed_identity(adoption_case)
    before = prepare_v0_route_requests(
        bundle, identity, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()

    async def fixture_response(request):
        pid = request["parameters"]["place_id"]
        body = {"id": pid, "location": {"latitude": 10, "longitude": 20}}
        if pid == "canonical-Museum A":
            if fault == "id":
                body["id"] = "foreign-id"
            elif fault == "boolean":
                body["location"]["latitude"] = True
            elif fault == "range":
                body["location"]["longitude"] = 181
            elif fault == "missing":
                body.pop("location")
        return Response(200, json.dumps(body).encode())

    snapshot = tmp_path / "extra-details"
    asyncio.run(
        acquire_snapshot(
            before["details_plan"], snapshot, fixture_response, AcquisitionPolicy(2, max_attempts=1)
        )
    )
    report = prepare_v0_route_requests(
        bundle,
        identity,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        details_snapshot_directory=snapshot,
    ).to_dict()
    assert report["status"] == "complete", report
    assert report["legs"][0]["coordinate_ready"] is ready
    assert report["counts"]["actual_sends"] == 0
    assert report["counts"]["details_requests"] == 0  # Never retry supplied bad evidence.
    assert report["counts"]["supplied_details_observed_sends"] == 2
    if ready:
        assert report["legs"][0]["request"]["body"]["travelMode"] == "WALK"
    else:
        assert report["legs"][0]["request"]["body"] is None
        assert report["coordinate_diagnostics"]


@pytest.mark.parametrize("fault", ["identity", "source", "policy", "review"])
def test_forged_handoff_fails_without_partial_request_inventory(adoption_case, fault):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = reviewed_identity(adoption_case).to_dict()
    if fault == "identity":
        identity["records"][0]["canonical_place_id"] = "foreign"
    elif fault == "source":
        identity["intake_hash"] = "0" * 64
    elif fault == "policy":
        identity["association_policy_version"] = "structural_claims_typed_addresses_3"
    else:
        identity["model_assistance_replay"]["reviews"]["records"][0]["decision"] = "reject"
    report = prepare_v0_route_requests(
        bundle, identity, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["requests"] == []
    assert report["legs"] == []


@pytest.mark.parametrize(
    "adoption_case", [{"coordinates_missing": True, "shared_venue": True}], indirect=True
)
def test_details_deduplicate_exact_canonical_venue_and_preserve_both_reference_links(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        reviewed_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
    ).to_dict()
    assert report["counts"]["details_requests"] == 1
    request = report["requests"][0]
    assert request["parameters"] == {"place_id": "shared-venue"}
    assert len(request["reference_ids"]) == 2
    assert report["legs"][0]["request"] is None
    assert report["legs"][0]["verdict"] == "N/A"


@pytest.mark.parametrize("adoption_case", [{"transport_mode": "TRANSIT"}], indirect=True)
def test_transit_keeps_original_departure_and_unverified_historical_context(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        reviewed_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
    ).to_dict()
    leg = report["legs"][0]
    assert leg["request_state"] == "conditional"
    assert leg["request"]["body"]["departureTime"] == "2020-01-01T10:00:00+00:00"
    assert leg["request"]["body"]["travelMode"] == "TRANSIT"
    assert "historical_matrix_transit_availability_unverified" in leg["readiness_checks"]
    assert report["counts"]["ready_routes"] == 0


def test_evidence_later_than_preparation_is_rejected(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        reviewed_identity(adoption_case),
        prepared_at="2020-01-01T00:00:00Z",
        schedule_context=context(intake),
    ).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["requests"] == []


@pytest.mark.parametrize("adoption_case", [{"coordinates_missing": True}], indirect=True)
@pytest.mark.parametrize(
    "fault,reason",
    [
        (None, None),
        ("deadline", "total_deadline_exhausted"),
        ("retry", "retries_forbidden"),
        ("search", "searches_forbidden"),
        ("model", "models_forbidden"),
        ("cost", "cost_limit_exceeded"),
        ("duplicate", "request_already_sent"),
        ("unknown", "request_not_ready"),
        ("package", "package_replay_mismatch"),
    ],
)
def test_preflight_counters_stop_without_granting_live_authorization(adoption_case, fault, reason):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = reviewed_identity(adoption_case)
    report = prepare_v0_route_requests(
        bundle, identity, prepared_at="2026-10-06T10:00:00Z", schedule_context=context(intake)
    ).to_dict()
    next_key = report["requests"][0]["key"]
    ledger = {
        "sent_request_keys": [],
        "elapsed_seconds": 0,
        "cost_usd": "0.000000",
        "retry_sends": 0,
        "search_sends": 0,
        "model_sends": 0,
    }
    if fault == "deadline":
        ledger["elapsed_seconds"] = 300
    elif fault in ("retry", "search", "model"):
        ledger[
            {"retry": "retry_sends", "search": "search_sends", "model": "model_sends"}[fault]
        ] = 1
    elif fault == "cost":
        ledger["cost_usd"] = "0.011000"
    elif fault == "duplicate":
        ledger.update(sent_request_keys=[next_key], cost_usd="0.005000")
    elif fault == "unknown":
        next_key = "foreign-request"
    elif fault == "package":
        report["limits"]["max_details_sends"] = 8
    result = preflight_v0_route_requests(
        bundle, identity, report, ledger=ledger, next_request_key=next_key
    )
    assert result["live_authorized"] is False
    if reason:
        assert result["status"] == "stopped"
        assert reason in result["reasons"]
    else:
        assert result["status"] == "within_prepared_limits"


@pytest.mark.parametrize("adoption_case", [{"shared_venue": True}], indirect=True)
def test_conflicting_saved_coordinates_block_reuse_and_do_not_propose_backfill(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        reviewed_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
    ).to_dict()
    assert report["counts"]["reused_coordinates"] == 0
    assert report["counts"]["details_requests"] == 0
    assert report["coordinate_diagnostics"][0]["reason"] == "coordinates_conflicting"


def test_cli_preserves_unknown_and_reports_invalid_input_without_network(adoption_case, capsys):
    from backend.evaluation.route_requests_cli import main

    intake, _, bundle, _, save, _, _, _ = adoption_case
    report_path = (
        bundle.parent
        / save("cli-identity.json", reviewed_identity(adoption_case).to_dict())["path"]
    )
    context_path = bundle.parent / save("cli-context.json", context(intake))["path"]
    assert (
        main(
            [
                str(bundle),
                str(report_path),
                "--context",
                str(context_path),
                "--prepared-at",
                "2026-10-06T10:00:00Z",
            ]
        )
        == 3
    )
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "complete"
    assert result["counts"]["actual_sends"] == 0
    assert result["legs"][0]["verdict"] == "UNKNOWN"
    assert main([str(bundle), str(report_path), "--prepared-at", "2026-10-06"]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "needs_material_correction"
