"""Opening acceptance through verified local snapshot replay; synthetic evidence only."""

import asyncio
import copy
import json

import pytest

from backend.evaluation.opening import score_opening
from backend.evaluation.snapshot import (
    AcquisitionPolicy,
    Response,
    acquire_snapshot,
    build_evidence_plan,
)
from backend.tests.evaluation import test_requirement_schedule as schedule_tests

pytest_plugins = ("backend.tests.evaluation.test_intake",)
prepared_scenario = schedule_tests.scenario


def point(day=3, hour=9, minute=0, **fields):
    return {"day": day, "hour": hour, "minute": minute, **fields}


def period(start=9, end=17, day=3, **fields):
    return {"open": point(day, start), "close": point(day, end), **fields}


@pytest.fixture
def opening_scenario(prepared_scenario, tmp_path, monkeypatch):  # noqa: F811
    counter = 0

    def build(
        payload=None,
        *,
        change=None,
        requested="2020-01-01T00:00:00+00:00",
        retrieved=None,
        unresolved_names=(),
        contexts=(),
        status_code=200,
        paired=False,
    ):
        nonlocal counter
        intake, identity, root = prepared_scenario(change=change, unresolved_names=unresolved_names)
        base_plan = build_evidence_plan(intake, identity, [], paired=paired)
        route_contexts = contexts(base_plan) if callable(contexts) else contexts
        plan = build_evidence_plan(intake, identity, list(route_contexts), paired=paired)
        payload = (
            payload
            if payload is not None
            else {"timeZone": {"id": "Etc/UTC"}, "regularOpeningHours": {"periods": [period()]}}
        )
        counter += 1
        directory = tmp_path / f"opening-{counter}"
        times = iter(
            [requested]
            + [t for _ in plan["requests"] for t in (requested, retrieved or requested)]
            + [retrieved or requested]
        )
        monkeypatch.setattr("backend.evaluation.snapshot._now", lambda: next(times))

        async def transport(request):
            if request["operation"] == "route_matrix":
                return Response(200, b"[]")
            data = {"id": request["parameters"]["place_id"], **payload}
            return Response(status_code, json.dumps(data).encode())

        asyncio.run(
            acquire_snapshot(
                plan, directory, transport, AcquisitionPolicy(max_sends=len(plan["requests"]) or 1)
            )
        )
        return intake, identity, directory, plan, root

    return build


def first(report):
    return report["results"][0]["opening"]


def test_end_at_close_passes_with_independent_regular_basis(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {"timeZone": {"id": "Etc/UTC"}, "regularOpeningHours": {"periods": [period(9, 10)]}}
    )
    report = score_opening(intake, identity, directory).to_dict()
    assert report["status"] == "complete"
    check = first(report)["checks"][0]
    assert check["state"] == "PASS"
    assert check["basis"] == "regular"
    assert check["outside_seconds"] == 0
    assert check["unknown_seconds"] == 0
    assert first(report)["counts"] == {"PASS": 1, "FAIL": 1, "UNKNOWN": 0, "N/A": 0}


def clocks(start, end):
    def change(results):
        item = results["v0"]["itinerary"]["days"][0]["activities"][0]
        item["start_time"], item["end_time"] = start, end

    return change


@pytest.mark.parametrize(
    ("hours", "state", "reason"),
    [
        ({"periods": []}, "FAIL", None),
        ({}, "UNKNOWN", "periods_missing"),
        ({"periods": None}, "UNKNOWN", "periods_invalid"),
        ({"periods": [None]}, "UNKNOWN", "period_invalid"),
        ({"periods": [{"open": point(0, 0)}]}, "PASS", None),
        ({"periods": [{"open": point(3, 9)}]}, "UNKNOWN", "close_missing"),
        (
            {"periods": [{"open": {"day": 3, "hour": 9}, "close": point(3, 17)}]},
            "UNKNOWN",
            "point_components_missing",
        ),
        (
            {"periods": [{"open": point(3, True), "close": point(3, 17)}]},
            "UNKNOWN",
            "point_components_invalid",
        ),
    ],
)
def test_original_presence_and_regular_encodings(opening_scenario, hours, state, reason):
    intake, identity, directory, _, _ = opening_scenario(
        {"timeZone": {"id": "Etc/UTC"}, "regularOpeningHours": hours}
    )
    report = score_opening(intake, identity, directory).to_dict()
    assert report["status"] == "complete"
    check = first(report)["checks"][0]
    assert check["state"] == state
    if reason:
        assert reason in check["reasons"]


@pytest.mark.parametrize(
    ("start", "end", "outside"),
    [
        ("2020-01-01T08:30Z", "2020-01-01T09:30Z", 1800),
        ("2020-01-01T16:00Z", "2020-01-01T17:00:00.000001Z", 0.000001),
        ("2020-01-01T11:30Z", "2020-01-01T13:30Z", 3600),
    ],
)
def test_exact_early_fractional_and_lunch_conflicts(opening_scenario, start, end, outside):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "regularOpeningHours": {"periods": [period(9, 12), period(13, 17)]},
        },
        change=clocks(start, end),
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "FAIL"
    assert check["outside_seconds"] == outside


def test_malformed_period_does_not_invent_closure_but_valid_span_can_prove_pass(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "regularOpeningHours": {"periods": [period(9, 10), {"open": {"day": 3}}]},
        }
    )
    opening = first(score_opening(intake, identity, directory).to_dict())
    assert [c["state"] for c in opening["checks"]] == ["PASS", "UNKNOWN"]
    assert opening["checks"][1]["outside_seconds"] is None
    assert opening["checks"][1]["confirmed_outside_lower_bound_seconds"] == 0


def dated_point(day, hour, minute=0, **fields):
    from datetime import date

    value = date.fromisoformat(day)
    return point(
        (value.weekday() + 1) % 7,
        hour,
        minute,
        date={"year": value.year, "month": value.month, "day": value.day},
        **fields,
    )


def test_current_precedes_regular_and_uses_selected_request_date(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "regularOpeningHours": {"periods": [period()]},
            "currentOpeningHours": {"periods": []},
        },
        requested="2020-01-01T23:00Z",
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "FAIL"
    assert check["basis"] == "current"
    assert check["outside_seconds"] == 3600


def test_partial_closure_stays_fail_in_conditional_denominator(opening_scenario):
    # Jan 1 is the last day of the seven-day current scope. The next day lacks hours.
    intake, identity, directory, _, _ = opening_scenario(
        {"timeZone": {"id": "Etc/UTC"}, "currentOpeningHours": {"periods": []}},
        change=clocks("2020-01-01T23:00Z", "2020-01-02T01:00Z"),
        requested="2019-12-26T12:00Z",
    )
    opening = first(score_opening(intake, identity, directory).to_dict())
    check = opening["checks"][0]
    assert check["state"] == "FAIL"
    assert check["outside_seconds"] is None
    assert check["confirmed_outside_lower_bound_seconds"] == 3600
    assert check["unknown_seconds"] == 3600
    assert check["evidence_status"] == "partial"
    assert opening["conditional_compliance"] == {"numerator": 0, "denominator": 2, "rate": 0}
    assert opening["complete_evidence_count"] == 1


@pytest.mark.parametrize(
    ("hours", "reason"),
    [
        (None, "hours_missing"),
        ([], "hours_invalid"),
        ({}, "periods_missing"),
        ({"periods": None}, "periods_invalid"),
        ({"periods": [{"open": point(3, 0)}]}, "close_missing"),
    ],
)
def test_invalid_current_falls_back_to_regular_with_diagnostics(opening_scenario, hours, reason):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "regularOpeningHours": {"periods": [period()]},
            "currentOpeningHours": hours,
        }
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "PASS"
    assert check["basis"] == "regular"
    assert reason in check["reasons"]


@pytest.mark.parametrize("current", [None, {"periods": [period()]}])
def test_post_trip_current_does_not_become_historical(opening_scenario, current):
    payload = {"timeZone": {"id": "Etc/UTC"}, "regularOpeningHours": {"periods": [period(9, 10)]}}
    if current is not None:
        payload["currentOpeningHours"] = current
    intake, identity, directory, _, _ = opening_scenario(payload, requested="2020-01-02T00:00Z")
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "PASS"
    assert check["basis"] == "regular"


def test_special_date_marker_without_schedule_uses_regular(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "regularOpeningHours": {"periods": [period()]},
            "currentOpeningHours": {
                "specialDays": [{"date": {"year": 2020, "month": 1, "day": 1}}]
            },
        },
        requested="2020-01-02T00:00Z",
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "PASS"
    assert check["basis"] == "regular"
    assert "special_date_marker" in check["reasons"]
    assert "full visit" in check["explanation"]


def test_partial_current_fallback_preserves_interval_provenance(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "currentOpeningHours": {"periods": [period(9, 10), {"open": point(3, 11)}]},
            "regularOpeningHours": {"periods": [period(9, 12)]},
        },
        change=clocks("2020-01-01T09:00Z", "2020-01-01T11:00Z"),
    )
    report = score_opening(intake, identity, directory).to_dict()
    check = first(report)["checks"][0]
    assert check["state"] == "PASS"
    assert check["basis"] == "mixed"
    segment = check["basis_segments"][0]
    assert segment["hours_fields"] == ["currentOpeningHours", "regularOpeningHours"]
    assert segment["hours_field"] is None
    assert segment["regular_fallback"]["known_open"] == [
        {
            "start": "2020-01-01T10:00:00+00:00",
            "end": "2020-01-01T11:00:00+00:00",
            "seconds": 3600.0,
        }
    ]
    assert segment["regular_fallback"]["known_closed"] == []
    assert "close_missing" in segment["reasons"]
    assert report["rules"]["version"] == "rtpeval_opening_rules_2"


@pytest.mark.parametrize("special", [None, {}, [{"date": {"year": 2020}}]])
def test_invalid_special_markers_are_diagnostics_not_regular_vetoes(opening_scenario, special):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "currentOpeningHours": {"specialDays": special},
            "regularOpeningHours": {"periods": [period()]},
        }
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "PASS"
    assert "special_dates_invalid" in check["reasons"]
    assert "periods_missing" in check["reasons"]


def test_regular_fallback_can_prove_visit_outside_hours(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "currentOpeningHours": None,
            "regularOpeningHours": {"periods": [period()]},
        },
        change=clocks("2020-01-01T08:30Z", "2020-01-01T09:30Z"),
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "FAIL"
    assert check["basis"] == "regular"
    assert check["outside_seconds"] == 1800
    assert check["basis_segments"][0]["regular_fallback"]["known_closed"][0]["seconds"] == 1800


def test_known_current_closure_survives_regular_cross_date_fallback(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "currentOpeningHours": {
                "periods": [
                    {
                        "open": dated_point("2020-01-01", 22),
                        "close": dated_point("2020-01-01", 23, 59, truncated=True),
                    }
                ]
            },
            "regularOpeningHours": {"periods": [{"open": point(3, 21), "close": point(4, 2)}]},
        },
        requested="2019-12-26T12:00Z",
        change=clocks("2020-01-01T21:00Z", "2020-01-02T01:00Z"),
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "FAIL"
    assert check["basis"] == "mixed"
    assert check["unknown_seconds"] == 0
    assert check["outside_seconds"] == 3600
    assert check["basis_segments"][0]["regular_fallback"]["known_closed"] == []


def test_partial_current_without_regular_retains_unknown_interval(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "currentOpeningHours": {"periods": [period(9, 10), {"open": point(3, 11)}]},
        },
        change=clocks("2020-01-01T09:00Z", "2020-01-01T11:00Z"),
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "UNKNOWN"
    assert check["basis"] == "current"
    assert check["known_open_seconds"] == 3600
    assert check["unknown_seconds"] == 3600
    assert check["basis_segments"][0]["regular_fallback"]["known_open"] == []


@pytest.mark.parametrize(
    ("timezone", "reason"),
    [
        (None, "timezone_missing"),
        ({"id": "Unknown/Zone"}, "timezone_invalid"),
        ({"id": 0}, "timezone_invalid"),
        ([], "timezone_invalid"),
    ],
)
def test_provider_timezone_errors_are_visit_unknown(opening_scenario, timezone, reason):
    intake, identity, directory, _, _ = opening_scenario(
        {"timeZone": timezone, "regularOpeningHours": {"periods": [period()]}}
    )
    report = score_opening(intake, identity, directory).to_dict()
    assert report["status"] == "complete"
    check = first(report)["checks"][0]
    assert check["state"] == "UNKNOWN"
    assert reason in check["reasons"]


def context(intake, zone="Etc/UTC"):
    return {
        "schema_version": "rtpeval_schedule_context_1",
        "batch_id": "batch",
        "revision": "1",
        "groups": [
            {
                "group_id": "g",
                "input_sha256": intake.to_dict()["inventory"][0]["input_sha256"],
                "timezone": zone,
                "source_ref": "independent-local-zone",
                "reviewer_ref": "reviewer",
                "reviewed_at": "2020-01-01T00:00Z",
            }
        ],
    }


def test_reviewed_context_fallback_and_place_conflict_are_explicit(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {"regularOpeningHours": {"periods": [period()]}}
    )
    check = first(score_opening(intake, identity, directory, context(intake)).to_dict())["checks"][
        0
    ]
    assert check["state"] == "PASS"
    assert check["timezone"]["origin"] == "reviewed_group_context"
    intake, identity, directory, _, _ = opening_scenario()
    check = first(
        score_opening(intake, identity, directory, context(intake, "Europe/Berlin")).to_dict()
    )["checks"][0]
    assert check["state"] == "UNKNOWN"
    assert "timezone_evidence_conflict" in check["reasons"]


def test_unresolved_role_suppresses_full_scope_rates(opening_scenario):
    def change(results):
        item = results["v0"]["itinerary"]["days"][0]["activities"][1]
        item.update(activity_kind="unknown", title="Unclear commitment")

    intake, identity, directory, _, _ = opening_scenario(change=change)
    opening = first(score_opening(intake, identity, directory).to_dict())
    assert opening["unresolved_role_count"] == 1
    assert opening["complete_evidence_coverage"]["rate"] is None
    assert opening["verdict_decidable_coverage"]["rate"] is None
    assert opening["conditional_compliance"]["rate"] is None
    assert len(opening["nonapplicable_records"]) == 1


def test_unknown_identity_preserves_visit_and_missing_magnitude(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(unresolved_names=("Museum A",))
    opening = first(score_opening(intake, identity, directory).to_dict())
    assert opening["applicable_count"] == 2
    assert opening["checks"][0]["state"] == "UNKNOWN"
    assert opening["checks"][0]["outside_seconds"] is None
    assert opening["identity_available_count"] == 1


@pytest.mark.parametrize(
    ("start", "end", "hours", "basis", "state"),
    [
        (
            "2020-01-01T23:30Z",
            "2020-01-02T00:30Z",
            [{"open": point(3, 22), "close": point(4, 2)}],
            "regular",
            "PASS",
        ),
        (
            "2020-01-01T00:30Z",
            "2020-01-01T01:30Z",
            [{"open": point(2, 22), "close": point(3, 2)}],
            "regular",
            "PASS",
        ),
        ("2020-01-01T10:00Z", "2020-01-01T09:00Z", [period()], "unavailable", "UNKNOWN"),
    ],
)
def test_explicit_cross_date_and_previous_day_periods(
    opening_scenario, start, end, hours, basis, state
):
    intake, identity, directory, _, _ = opening_scenario(
        {"timeZone": {"id": "Etc/UTC"}, "regularOpeningHours": {"periods": hours}},
        change=clocks(start, end),
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == state
    assert check["basis"] == basis


def test_cross_date_truncation_falls_back_without_losing_basis_segments(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "currentOpeningHours": {
                "periods": [
                    {
                        "open": dated_point("2020-01-01", 22),
                        "close": dated_point("2020-01-01", 23, 59, truncated=True),
                    }
                ]
            },
            "regularOpeningHours": {"periods": [{"open": point(3, 22), "close": point(4, 2)}]},
        },
        requested="2019-12-26T12:00Z",
        change=clocks("2020-01-01T23:00Z", "2020-01-02T01:00Z"),
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "PASS"
    assert check["basis"] == "mixed"
    assert check["unknown_seconds"] == 0
    assert check["confirmed_outside_lower_bound_seconds"] == 0
    assert [s["basis"] for s in check["basis_segments"]] == ["mixed", "regular"]
    assert check["basis_segments"][0]["regular_fallback"]["known_open"][0]["seconds"] == 60


@pytest.mark.parametrize(("dated", "basis"), [(False, "regular"), (True, "current")])
def test_collection_crossing_midnight_uses_regular_when_current_dates_are_uncertain(
    opening_scenario, dated, basis
):
    p = {"open": dated_point("2020-01-01", 9), "close": dated_point("2020-01-01", 17)}
    if not dated:
        p = period()
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "currentOpeningHours": {"periods": [p]},
            "regularOpeningHours": {"periods": [period()]},
        },
        requested="2020-01-01T23:59Z",
        retrieved="2020-01-02T00:01Z",
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "PASS"
    assert check["basis"] == basis
    assert "current_collection_date_uncertain" in check["reasons"]


@pytest.mark.parametrize(
    ("day", "hours", "start", "end", "state", "magnitude", "reason"),
    [
        ("2020-03-29", [{"open": point(0, 0)}], "00:00", "next", "PASS", 82800, None),
        ("2020-10-25", [{"open": point(0, 0)}], "00:00", "next", "PASS", 90000, None),
        ("2020-03-29", [period(1, 4, 0)], "02:15", "03:30", "UNKNOWN", None, "dst_gap"),
        ("2020-10-25", [period(1, 4, 0)], "02:15", "03:30", "UNKNOWN", None, "dst_fold"),
        ("2020-03-29", [period(2, 4, 0)], "03:00", "03:30", "UNKNOWN", None, "dst_gap"),
    ],
)
def test_place_local_dst_days_and_provider_endpoint_uncertainty(
    opening_scenario, day, hours, start, end, state, magnitude, reason
):
    from datetime import date, timedelta

    end_stamp = (
        (date.fromisoformat(day) + timedelta(days=1)).isoformat() + "T00:00"
        if end == "next"
        else day + "T" + end
    )

    def change(results):
        item = results["v0"]["itinerary"]["days"][0]
        item["date"] = day
        item["activities"][0].update(start_time=day + "T" + start, end_time=end_stamp)

    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Europe/Berlin", "version": "provider-test-version"},
            "regularOpeningHours": {"periods": hours},
        },
        change=change,
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == state
    if magnitude is not None:
        assert check["known_open_seconds"] == magnitude
    if reason:
        assert reason in check["reasons"]
    assert check["timezone"]["provider"]["version"] == "provider-test-version"
    assert len(check["timezone"]["zone_data"]["zone_file_sha256"]) == 64


@pytest.mark.parametrize(
    "fault", ["scope", "reference", "source", "policy", "resolution", "high_impact"]
)
def test_stale_or_invalid_identity_requires_replay_without_partial_results(opening_scenario, fault):
    intake, identity, directory, _, _ = opening_scenario()
    report = identity.to_dict()
    if fault == "scope":
        report.pop("subject_scope_version")
    elif fault == "reference":
        report["records"].pop()
    elif fault == "source":
        report["records"][0]["source"]["pointer"] = "/wrong"
    elif fault == "policy":
        report["audit_plan_hash"] = "unverified"
    elif fault == "resolution":
        report["records"][0]["resolution"] = "unsupported"
    else:
        report["records"][0].update(high_impact=True, decision_route="automatic")
    output = score_opening(intake, report, directory).to_dict()
    assert output["status"] == "identity_replay_required"
    assert output["results"] == []


def revise_snapshot(directory, change):
    from backend.evaluation.records import canonical_digest

    path = directory / "manifest.json"
    manifest = json.loads(path.read_text())
    change(manifest)
    manifest["plan_hash"] = canonical_digest(manifest["plan"])
    path.write_text(json.dumps(manifest), encoding="utf-8")


@pytest.mark.parametrize(
    "fault",
    [
        "phase",
        "paired",
        "intake",
        "identity",
        "source",
        "missing_record",
        "raw",
        "attempt_time",
        "trusted_plan",
    ],
)
def test_corrupt_or_unlinked_snapshot_is_batch_correction(opening_scenario, fault):
    intake, identity, directory, plan, _ = opening_scenario()
    trusted = None
    if fault == "raw":
        raw = next(directory.glob("raw/*"))
        raw.write_bytes(b"corrupt")
    elif fault == "trusted_plan":
        trusted = copy.deepcopy(plan)
        trusted["paired"] = True
    else:

        def change(snapshot):
            if fault == "phase":
                snapshot["plan"]["phase"] = "identity"
            elif fault == "paired":
                snapshot["plan"]["paired"] = True
            elif fault in ("intake", "identity"):
                snapshot["plan"][fault + ("_hash" if fault == "intake" else "_report_hash")] = (
                    "0" * 64
                )
            elif fault == "source":
                snapshot["plan"]["references"][0]["source"]["pointer"] = "/wrong"
            elif fault == "missing_record":
                snapshot["records"].pop()
            else:
                snapshot["records"][0]["attempts"][0]["requested_at"] = "2020-01-01T00:00+02:00"

        revise_snapshot(directory, change)
    report = score_opening(intake, identity, directory, expected_plan=trusted).to_dict()
    assert report["status"] == "needs_material_correction"
    assert report["results"] == []


def mixed_routes(plan):
    from backend.tests.evaluation.test_snapshot import route_context

    leg = plan["legs"][0]
    value = route_context(leg)
    refs = {r["reference_id"]: r for r in plan["references"]}
    for side, field in (("origin", "origin_reference"), ("destination", "destination_reference")):
        value[side]["place_id"] = refs[leg[field]]["canonical_place_id"]
    return [value]


@pytest.mark.parametrize("corrupt_route", [False, True])
def test_mixed_purpose_snapshot_retains_valid_routes_and_checks_linkage(
    opening_scenario, corrupt_route
):
    intake, identity, directory, plan, _ = opening_scenario(contexts=mixed_routes)
    if corrupt_route:
        revise_snapshot(
            directory,
            lambda snapshot: snapshot["plan"]["legs"][0].update(
                origin_reference="unlinked-reference"
            ),
        )
    report = score_opening(intake, identity, directory).to_dict()
    assert report["status"] == ("needs_material_correction" if corrupt_route else "complete")
    if not corrupt_route:
        assert first(report)["checks"][0]["state"] == "PASS"
        assert score_opening(intake, identity, directory, expected_plan=plan).status == "complete"


def test_returned_wrong_canonical_place_is_unknown_not_rebound(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "id": "wrong-place",
            "timeZone": {"id": "Etc/UTC"},
            "regularOpeningHours": {"periods": [period()]},
        }
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "UNKNOWN"
    assert "canonical_id_mismatch" in check["reasons"]


def test_two_passes_and_partial_fail_use_two_over_three_compliance(opening_scenario):
    def change(results):
        activities = results["v0"]["itinerary"]["days"][0]["activities"]
        item = copy.deepcopy(activities[0])
        item.update(
            activity_id="repeat-a", start_time="2020-01-01T23:00Z", end_time="2020-01-02T01:00Z"
        )
        activities.append(item)

    intake, identity, directory, plan, _ = opening_scenario(
        {"timeZone": {"id": "Etc/UTC"}, "currentOpeningHours": {"periods": [period()]}},
        change=change,
        requested="2019-12-26T12:00Z",
    )
    opening = first(score_opening(intake, identity, directory).to_dict())
    assert opening["counts"] == {"PASS": 2, "FAIL": 1, "UNKNOWN": 0, "N/A": 0}
    assert opening["conditional_compliance"]["rate"] == 2 / 3
    assert opening["complete_evidence_coverage"]["rate"] == 2 / 3
    assert opening["verdict_decidable_coverage"]["rate"] == 1
    assert opening["duration_subtotals"]["outside_seconds"]["observed_visit_count"] == 2
    assert opening["duration_subtotals"]["confirmed_outside_lower_bound_seconds"]["seconds"] == 3600
    assert len(plan["requests"]) == 2
    assert len({c["source"]["record_id"] for c in opening["checks"]}) == 3


@pytest.mark.parametrize(
    ("item", "reason"),
    [
        ({"open": point(7, 9), "close": point(3, 17)}, "point_components_invalid"),
        ({"open": point(3, 24), "close": point(3, 17)}, "point_components_invalid"),
        ({"open": point(3, 9, -1), "close": point(3, 17)}, "point_components_invalid"),
        ({"open": point(3, 9.0), "close": point(3, 17)}, "point_components_invalid"),
        ({"open": point(3, 9, truncated="false"), "close": point(3, 17)}, "truncation_invalid"),
        (
            {
                "open": dated_point("2020-01-02", 9) | {"day": 3},
                "close": dated_point("2020-01-02", 17),
            },
            "point_date_weekday_conflict",
        ),
        (
            {"open": point(3, 9, date={"year": 2020, "month": 1}), "close": point(3, 17)},
            "point_date_invalid",
        ),
    ],
)
def test_invalid_provider_components_remain_semantic_unknown(opening_scenario, item, reason):
    intake, identity, directory, _, _ = opening_scenario(
        {"timeZone": {"id": "Etc/UTC"}, "currentOpeningHours": {"periods": [item]}}
    )
    opening = first(score_opening(intake, identity, directory).to_dict())
    assert opening["checks"][0]["state"] == "UNKNOWN"
    assert reason in opening["checks"][0]["reasons"]


def test_request_window_is_place_local_not_utc_or_host_local(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Pacific/Kiritimati"},
            "currentOpeningHours": {"periods": []},
            "regularOpeningHours": {"periods": [{"open": point(0, 0)}]},
        },
        requested="2019-12-31T12:00Z",
        change=clocks("2020-01-01T09:00+14:00", "2020-01-01T10:00+14:00"),
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "FAIL"
    assert check["basis_segments"][0]["current_window_start"] == "2020-01-01"


def test_current_truncated_open_does_not_invent_pre_window_hours(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Etc/UTC"},
            "currentOpeningHours": {
                "periods": [
                    {
                        "open": dated_point("2020-01-01", 0, truncated=True),
                        "close": dated_point("2020-01-01", 6),
                    }
                ]
            },
        },
        change=clocks("2020-01-01T00:30Z", "2020-01-01T01:30Z"),
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "PASS"
    assert check["basis"] == "current"


def test_non_hours_fields_and_planner_findings_do_not_supply_evidence(opening_scenario):
    def change(results):
        for result in results.values():
            result["validation_report"] = {"opening": "PASS"}
            result["repair_status"] = "successful"
            result["itinerary"]["nearby_references"] = [{"place_name": "Museum A"}]
            for item in result["itinerary"]["days"][0]["activities"]:
                item["opening_hours"] = {"periods": [period()]}

    payload = {
        "timeZone": {"id": "Etc/UTC"},
        "openNow": True,
        "businessStatus": "OPERATIONAL",
        "weekdayDescriptions": ["Always open"],
        "regularSecondaryOpeningHours": [{"periods": [{"open": point(0, 0)}]}],
    }
    intake, identity, directory, _, _ = opening_scenario(payload)
    before = first(score_opening(intake, identity, directory).to_dict())
    intake, identity, directory, _, _ = opening_scenario(payload, change=change)
    after = first(score_opening(intake, identity, directory).to_dict())
    assert before["counts"] == after["counts"] == {"PASS": 0, "FAIL": 0, "UNKNOWN": 2, "N/A": 0}
    assert before["basis_counts"] == after["basis_counts"]
    assert [c["outside_seconds"] for c in before["checks"]] == [
        c["outside_seconds"] for c in after["checks"]
    ]


def test_failed_send_is_visit_unknown_with_attempt_provenance(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(status_code=400)
    report = score_opening(intake, identity, directory).to_dict()
    assert report["status"] == "complete"
    check = first(report)["checks"][0]
    assert check["state"] == "UNKNOWN"
    assert "details_unavailable" in check["reasons"]
    assert check["evidence_reference"]["attempts"][0]["status_code"] == 400


def test_unusable_hours_are_unavailable_basis_even_with_candidate_field(opening_scenario):
    intake, identity, directory, _, _ = opening_scenario(
        {"timeZone": {"id": "Etc/UTC"}, "currentOpeningHours": {"periods": None}}
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["basis"] == "unavailable"
    assert check["basis_segments"][0]["selected_basis"] == "current"


def test_paired_scope_is_explicit_and_optional_checks_remain_independent(opening_scenario):
    def change(results):
        itinerary = results["v3"]["itinerary"]
        results["v3"]["v3"] = {
            "draft": copy.deepcopy(itinerary),
            "final_primary": copy.deepcopy(itinerary),
        }

    intake, identity, directory, plan, _ = opening_scenario(change=change, paired=True)
    paired = score_opening(intake, identity, directory, paired=True, expected_plan=plan).to_dict()
    assert paired["status"] == "complete"
    assert [(r["version"], r["projection"]) for r in paired["results"]][-3:] == [
        ("v3", "final"),
        ("v3", "draft"),
        ("v3", "final_primary"),
    ]
    assert sum(len(r["opening"]["checks"]) for r in paired["results"]) == 12
    assert score_opening(intake, identity, directory).status == "needs_material_correction"


def test_empty_applicable_scope_is_na_with_unavailable_rates(opening_scenario):
    def change(results):
        for result in results.values():
            result["itinerary"]["days"][0]["activities"] = []

    intake, identity, directory, _, _ = opening_scenario(change=change)
    opening = first(score_opening(intake, identity, directory).to_dict())
    assert opening["applicable_count"] == 0
    assert opening["state"] == "N/A"
    assert opening["conditional_compliance"]["rate"] is None
    assert opening["duration_subtotals"]["outside_seconds"]["seconds"] is None


@pytest.mark.parametrize(
    ("start", "end", "reason"),
    [
        ("2020-01-01T09:00+01:00", "2020-01-01T10:00+01:00", "timezone_offset_conflict"),
        ("2020-01-02T09:00Z", "2020-01-02T10:00Z", "declared_date_mismatch"),
        (None, "2020-01-01T10:00Z", "invalid_timestamp"),
        ("2020-01-01T09:00:00.0000001Z", "2020-01-01T10:00Z", "unsupported_timestamp_precision"),
    ],
)
def test_bad_visit_time_preserves_unknown_and_null_duration(opening_scenario, start, end, reason):
    intake, identity, directory, _, _ = opening_scenario(change=clocks(start, end))
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "UNKNOWN"
    assert reason in check["reasons"]
    assert check["unknown_seconds"] is None
    assert check["confirmed_outside_lower_bound_seconds"] is None


@pytest.mark.parametrize(
    ("day", "start", "end"),
    [
        ("2020-04-01", "2020-04-01T10:00", "2020-04-01T11:00"),
        ("2020-03-28", "2020-03-28T23:00", "2020-03-29T00:00"),
    ],
)
def test_previous_week_dst_endpoint_defect_does_not_erase_unrelated_closed_day(
    opening_scenario, day, start, end
):
    def change(results):
        item = results["v0"]["itinerary"]["days"][0]
        item["date"] = day
        item["activities"][0].update(start_time=start, end_time=end)

    intake, identity, directory, _, _ = opening_scenario(
        {
            "timeZone": {"id": "Europe/Berlin"},
            "regularOpeningHours": {"periods": [period(2, 4, 0)]},
        },
        change=change,
    )
    check = first(score_opening(intake, identity, directory).to_dict())["checks"][0]
    assert check["state"] == "FAIL"
    assert check["outside_seconds"] == 3600
    assert "dst_gap" not in check["reasons"]
