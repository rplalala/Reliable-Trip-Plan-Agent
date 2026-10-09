"""Explicit region selection through public offline preparation and CLI seams."""

import json

import pytest

from backend.evaluation.tools.route_requests import (
    preflight_v0_route_requests,
    prepare_v0_route_requests,
)
from backend.evaluation.tools.route_requests_cli import main
from backend.tests.evaluation.test_requirement_schedule import context
from backend.tests.evaluation.test_route_requests_versioned import current_identity

pytest_plugins = (
    "backend.tests.evaluation.test_intake",
    "backend.tests.evaluation.test_identity_adoption",
)


@pytest.mark.parametrize("adoption_case", [{"destination": "Sydney, Australia"}], indirect=True)
def test_au_walk_is_ready_for_approval_but_stays_unknown_and_never_authorized(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = current_identity(adoption_case)
    report = prepare_v0_route_requests(
        bundle,
        identity,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        region_code="AU",
    ).to_dict()
    assert report["status"] == "complete", report["diagnostics"]
    leg = report["legs"][0]
    assert leg["provider"]["region_code"] == "AU"
    assert leg["provider"]["checked_on"] == "2026-10-07"
    assert leg["request_state"] == "ready_for_approval"
    assert leg["verdict"] == "UNKNOWN"
    assert leg["request"]["body"]["travelMode"] == "WALK"
    assert "departureTime" not in leg["request"]["body"]
    assert report["counts"]["ready_routes"] == 1
    assert report["counts"]["actual_sends"] == report["counts"]["details_requests"] == 0
    assert report["budget"]["proposed_usd"] == "0.005000"
    ledger = {
        "sent_request_keys": [],
        "elapsed_seconds": 0,
        "cost_usd": "0.000000",
        "retry_sends": 0,
        "search_sends": 0,
        "model_sends": 0,
    }
    assert preflight_v0_route_requests(
        bundle, identity, report, ledger=ledger, next_request_key=leg["request"]["key"]
    ) == {"status": "within_prepared_limits", "live_authorized": False, "reasons": []}


@pytest.mark.parametrize("adoption_case", [{"destination": "Sydney, Australia"}], indirect=True)
def test_cli_explicit_au_matches_library_without_changing_default_kr(adoption_case, capsys):
    intake, _, bundle, _, save, _, _, _ = adoption_case
    identity = current_identity(adoption_case)
    identity_path = bundle.parent / save("current-identity.json", identity)["path"]
    ctx = context(intake)
    context_path = bundle.parent / save("context.json", ctx)["path"]
    args = [
        str(bundle),
        str(identity_path),
        "--context",
        str(context_path),
        "--prepared-at",
        "2026-10-06T10:00:00Z",
    ]
    assert main([*args, "--region", "AU"]) == 0
    actual = json.loads(capsys.readouterr().out)
    assert (
        actual
        == prepare_v0_route_requests(
            bundle,
            identity,
            prepared_at="2026-10-06T10:00:00Z",
            schedule_context=ctx,
            region_code="AU",
        ).to_dict()
    )
    assert main(args) == 3
    default = json.loads(capsys.readouterr().out)
    explicit_kr = prepare_v0_route_requests(
        bundle,
        identity,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=ctx,
        region_code="KR",
    ).to_dict()
    assert default == explicit_kr
    assert "region_code" not in default["replay_inputs"]
    assert default["legs"][0]["request_state"] == "blocked"


@pytest.mark.parametrize(
    "adoption_case", [{"destination": "Sydney, Australia", "repeat_visits": True}], indirect=True
)
def test_au_duplicate_queries_budget_sends_not_leg_occurrences(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        current_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        region_code="AU",
    ).to_dict()
    assert report["status"] == "complete", report["diagnostics"]
    assert len(report["legs"]) == 3
    assert report["counts"]["eligible_endpoint_occurrences"] == 6
    assert report["counts"]["directed_route_requests"] == 2
    assert report["counts"]["ready_routes"] == report["limits"]["max_routes_sends"] == 2
    assert report["budget"]["proposed_usd"] == "0.010000"
    assert sorted(len(r["leg_ids"]) for r in report["requests"]) == [1, 2]
    assert all(leg["verdict"] == "UNKNOWN" for leg in report["legs"])


@pytest.mark.parametrize("region", [None, True, "au", "US", "", [], {}])
def test_invalid_region_never_silently_falls_back_to_a_supported_profile(adoption_case, region):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        current_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        region_code=region,
    ).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["legs"] == report["requests"] == []
    assert report["diagnostics"][0]["pointer"] == "provider/region_code"


@pytest.mark.parametrize(
    "adoption_case",
    [{}, {"destination": "Sydney"}, {"destination": "Seoul, South Korea"}],
    indirect=True,
)
def test_au_cannot_relabel_an_unresolved_or_foreign_source_destination(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        current_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        region_code="AU",
    ).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["legs"] == report["requests"] == []
    assert report["diagnostics"][0]["pointer"] == "provider/region_code"


@pytest.mark.parametrize(
    "adoption_case",
    [
        {"destination": "Sydney, Australia", "transport_mode": "TRANSIT"},
        {"destination": "Sydney, Australia", "transport_mode": "DRIVE"},
    ],
    indirect=True,
)
def test_au_does_not_promote_transit_or_add_a_drive_path(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        current_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        region_code="AU",
    ).to_dict()
    assert report["status"] == "complete", report["diagnostics"]
    leg = report["legs"][0]
    assert leg["verdict"] == "UNKNOWN"
    assert report["counts"]["ready_routes"] == 0
    if leg["mode"] == "TRANSIT":
        assert leg["request_state"] == "conditional"
        assert leg["request"]["body"]["departureTime"] == leg["evaluation_departure"]
        assert "regional_transit_coverage_unverified" in leg["readiness_checks"]
        assert "historical_matrix_transit_availability_unverified" in leg["readiness_checks"]
    else:
        assert leg["request_state"] == "blocked"
        assert leg["request"]["body"] is None
        assert "provider_mode_unsupported" in leg["readiness_checks"]


@pytest.mark.parametrize(
    "adoption_case",
    [{"destination": "Sydney, Australia", "coordinates_missing": True}],
    indirect=True,
)
def test_au_missing_independent_points_only_prepares_details_and_keeps_route_conditional(
    adoption_case,
):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        current_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        region_code="AU",
    ).to_dict()
    assert report["status"] == "complete"
    assert report["legs"][0]["request_state"] == "conditional"
    assert report["legs"][0]["request"]["body"] is None
    assert report["counts"]["details_requests"] == 2
    assert report["budget"]["proposed_usd"] == "0.010000"
    assert report["budget"]["unready_routes_usd"] == "0.005000"


@pytest.mark.parametrize("adoption_case", [{"destination": "Sydney, Australia"}], indirect=True)
def test_au_missing_model_result_keeps_identity_blockers_and_original_output(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    original_bytes = (bundle.parent / "v0.json").read_bytes()
    report = prepare_v0_route_requests(
        bundle,
        None,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        region_code="AU",
    ).to_dict()
    assert report["status"] == "complete"
    assert report["legs"][0]["request_state"] == "blocked"
    assert report["legs"][0]["canonical_endpoints"] == [None, None]
    assert report["requests"] == []
    assert report["budget"]["proposed_usd"] == "0.000000"
    assert (bundle.parent / "v0.json").read_bytes() == original_bytes


@pytest.mark.parametrize(
    "adoption_case",
    [{"destination": "Sydney, Australia", "shared_venue": True}],
    indirect=True,
)
def test_au_same_canonical_leg_never_consumes_a_route_allowance(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    report = prepare_v0_route_requests(
        bundle,
        current_identity(adoption_case),
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        region_code="AU",
    ).to_dict()
    assert report["status"] == "complete"
    assert report["legs"][0]["verdict"] == "N/A"
    assert report["requests"] == []
    assert report["counts"]["ready_routes"] == report["limits"]["max_routes_sends"] == 0


@pytest.mark.parametrize("adoption_case", [{"destination": "Sydney, Australia"}], indirect=True)
def test_preflight_rejects_a_changed_region_profile(adoption_case):
    intake, _, bundle, _, _, _, _, _ = adoption_case
    identity = current_identity(adoption_case)
    report = prepare_v0_route_requests(
        bundle,
        identity,
        prepared_at="2026-10-06T10:00:00Z",
        schedule_context=context(intake),
        region_code="AU",
    ).to_dict()
    report["replay_inputs"]["region_code"] = "KR"
    ledger = {
        "sent_request_keys": [],
        "elapsed_seconds": 0,
        "cost_usd": "0.000000",
        "retry_sends": 0,
        "search_sends": 0,
        "model_sends": 0,
    }
    result = preflight_v0_route_requests(
        bundle,
        identity,
        report,
        ledger=ledger,
        next_request_key=report["requests"][0]["key"],
    )
    assert result["reasons"] == ["package_replay_mismatch"]
    assert result["live_authorized"] is False
