"""Synthetic provider contracts plus the saved 863-second WALK observation; offline only."""

import asyncio
import json
from datetime import timedelta
from pathlib import Path
from time import monotonic

import pytest

from backend.app.evidence.models import OpeningHoursEvidence, PlaceCandidate, RouteEvidence
from backend.app.evidence.normalization import normalize_place_details, normalize_routes
from backend.app.evidence.opening_hours import assess_opening, selected_hours
from backend.app.integrations.models import PlaceDetailsDTO, RouteMatrixDTO, RouteMatrixRequest
from backend.app.versions.v3.repair_acceptance import assess
from backend.app.versions.v3.repair_budget import RepairBudget
from backend.app.versions.v3.repair_candidates import prepare_candidates
from backend.app.versions.v3.repair_routes import bind_transitions, check_transitions
from backend.app.versions.v3.repair_spatial import check_addition_layout
from backend.app.versions.v3.wiring import operation_scope
from backend.tests.versions.v3.test_b_targets import edit, setup, visit
from backend.tests.versions.v3.test_c_obligations import execute
from backend.tests.versions.v3.test_validation import DAY, NOW, activity, draft, place


def period(start=9, end=17, weekday=6):
    return {"open": {"day": weekday, "hour": start}, "close": {"day": weekday, "hour": end}}


def normalized(current=None, regular=None, pid="a"):
    """Provider-shaped synthetic response; never represented as historical raw data."""
    dto = PlaceDetailsDTO(
        place_id=pid,
        display_name=pid,
        location={"latitude": 0, "longitude": 0},
        time_zone="UTC",
        requested_at=NOW.isoformat(),
        retrieved_at=NOW.isoformat(),
        current_opening_hours=current,
        regular_opening_hours=regular,
    )
    return normalize_place_details(
        dto,
        candidate=PlaceCandidate(
            place_id=pid,
            name=pid,
            latitude=0,
            longitude=0,
            source_query="fixture",
            category="fixture",
        ),
    )


def test_mapping_retains_presence_special_dates_and_truncation():
    raw = {"periods": [period()], "specialDays": [{"date": {"year": 2026, "month": 9, "day": 26}}]}
    raw["periods"][0]["open"]["truncated"] = True
    p = normalized(raw)
    assert p.current_opening_hours.periods == raw["periods"]
    assert p.current_opening_hours.special_days == [DAY]
    assert selected_hours(p, DAY)["known"]
    assert selected_hours(normalized({}), DAY)["reason"] == "structured_periods_missing"
    assert selected_hours(normalized({"periods": []}), DAY)["intervals"] == []
    assert selected_hours(normalized({"periods": []}), DAY)["known"]
    assert (
        selected_hours(
            place(
                current_opening_hours=OpeningHoursEvidence(
                    applicability="historical", weekday_descriptions=["Saturday: 09:00-17:00"]
                )
            ),
            DAY,
        )["reason"]
        == "structured_periods_legacy_unmapped"
    )


def test_current_window_regular_and_known_exception():
    p = normalized({"periods": [period(10, 16)]}, {"periods": [period(8, 20)]})
    assert selected_hours(p, DAY)["basis"] == "current_date_window"
    assert selected_hours(p, DAY + timedelta(days=7))["basis"] == "regular_weekly_baseline"
    special = {"specialDays": [{"date": {"year": 2026, "month": 9, "day": 26}}]}
    assert not selected_hours(normalized(special, {"periods": [period()]}), DAY)["known"]
    assert (
        selected_hours(normalized({"periods": []}, {"periods": [period()]}), DAY)["intervals"] == []
    )


def test_full_visit_multisegment_overnight_and_all_day():
    p = normalized(regular={"periods": [period(9, 12), period(14, 18)]})
    assert assess_opening(activity(start="11:00", end="15:00"), p)[3] == 7200
    overnight = {"open": {"day": 5, "hour": 22}, "close": {"day": 6, "hour": 2}}
    p = normalized(regular={"periods": [overnight]})
    assert assess_opening(activity(start="00:30", end="01:30"), p)[0] == "PASS"
    p = normalized(regular={"periods": [{"open": {"day": 0, "hour": 0, "minute": 0}}]})
    a = activity(start="23:00", end="23:59")
    a.end_time += timedelta(hours=2)
    assert assess_opening(a, p)[0] == "PASS"


def test_api_hours_unbound_visit_automatic_c_retime_and_audit():
    original, ctx, _, policy = setup([[visit("a", "a", start="17:00", end="18:00")]], reviews=())
    p = normalized(regular={"periods": [period(9, 17)]})
    ctx = ctx.model_copy(update={"places": (p, *ctx.places[1:])})
    before = assess(original, ctx)
    finding = next(f for f in before.findings if f.check == "opening")
    assert finding.status == "CONFIRMED" and finding.magnitude == 3600
    assert finding.adopted_evidence["policy"] == "application_default"
    result, model = execute(
        (original, ctx, policy), [[edit("retime", "a", start="15:00", end="16:00")]]
    )
    assert model.calls == 1 and result.status == "ACCEPTED_COMPLETE"
    assert result.original == original
    assert next(f for f in result.adopted_report.findings if f.check == "opening").status == "PASS"
    assert (
        next(f for f in result.adopted_report.findings if f.check == "visitor_suitability").status
        == "UNKNOWN"
    )


def matrix(raw):
    request = RouteMatrixRequest(
        origins=[{"place_id": "a", "location": {"latitude": 0, "longitude": 0}}],
        destinations=[{"place_id": "b", "location": {"latitude": 0, "longitude": 1}}],
        travel_mode="WALK",
        field_mask="status,condition,duration",
    )
    return normalize_routes(
        RouteMatrixDTO(
            elements=[
                {"originIndex": 0, "destinationIndex": 0, "condition": "ROUTE_EXISTS", **raw}
            ],
            retrieved_at=NOW.isoformat(),
        ),
        request=request,
        mode_reason="fixture",
    )


@pytest.mark.parametrize(
    "status,success",
    [({}, True), ({"code": 0}, True), ({"code": 7}, False), (None, False), ("OK", False)],
)
def test_element_status_default_and_errors(status, success):
    element = matrix({"status": status, "duration": "0s"}).elements[0]
    assert (element.availability == "available") == success
    assert element.duration_seconds == 0


@pytest.mark.parametrize(
    "duration,expected",
    [("0.01s", 1), ("863s", 863), ("-1s", None), ("NaNs", None), (None, None), ("infs", None)],
)
def test_duration_never_rounds_down_or_coerces_invalid_to_zero(duration, expected):
    e = matrix({"status": {}, "duration": duration}).elements[0]
    assert e.duration_seconds == expected
    assert (e.availability == "available") == (expected is not None)


def test_missing_status_is_distinct_from_successful_empty_status():
    assert matrix({"duration": "1s"}).elements[0].status_state == "missing"
    assert matrix({"status": {}, "duration": "1s"}).elements[0].status_state == "success"


def test_saved_walk_estimate_and_synthetic_five_minute_conflict():
    path = Path("backend/tests/fixtures/v3/api_walk_observation.json")
    if not path.exists():
        pytest.skip("Local historical artifact is intentionally not a repository fixture")
    data = json.loads(path.read_text(encoding="utf-8"))
    evidence = RouteEvidence.model_validate(data["route"])
    e = evidence.elements[0]
    assert (e.duration_seconds, e.distance_meters) == (863, 1062)
    for gap, status, deficit in ((45, "PASS", 0), (5, "CONFIRMED", 563)):
        left = activity(pid=e.origin_place_id, start="11:00", end="12:30")
        right = activity("two", e.destination_place_id, "13:15", "14:30")
        right.start_time = left.end_time + timedelta(minutes=gap)
        itinerary = draft([left, right])
        row = list(check_transitions(itinerary, bind_transitions(itinerary, "WALK"), (evidence,)))[
            0
        ]
        assert row["status"] == status and row["magnitude"] == deficit
        assert row["adopted_evidence"]["selected_routes"][0]["element"]["duration_seconds"] == 863


def test_walk_conflict_flows_through_automatic_scope_and_repair():
    original, ctx, _, policy = setup(
        [[visit("a", "a", end="11:00"), visit("b", "b", start="11:05", end="12:05")]], reviews=()
    )
    ctx = ctx.model_copy(
        update={
            "route_evidence": (matrix({"status": {}, "duration": "863s"}),),
            "transitions": bind_transitions(original, "WALK"),
        }
    )
    assert next(f for f in assess(original, ctx).findings if f.check == "route").magnitude == 563
    result, _ = execute(
        (original, ctx, policy), [[edit("retime", "b", start="11:20", end="12:20")]]
    )
    assert result.status == "ACCEPTED_COMPLETE"
    assert result.counters.get("routes", 0) == 0


def test_existing_api_route_bypasses_radius_in_preparation_and_acceptance():
    original, ctx, _, policy = setup([[visit("a", "a")]], reviews=("coverage",))
    places = (place(), place("b", longitude=0.05))
    evidence = matrix({"status": {}, "duration": "1200s", "distanceMeters": 2800})
    ctx = ctx.model_copy(
        update={"places": places, "original_supply_ids": ("a", "b"), "route_evidence": (evidence,)}
    )
    scope = operation_scope(
        original, assess(original, ctx), mode="WALK", context=ctx, policy=policy
    )
    prep = asyncio.run(
        prepare_candidates(ctx, scope, RepairBudget(monotonic() + 300), original=original)
    )
    assert any(r.place_id == "b" for r in prep.authorizations)
    from backend.app.versions.v3.repair_projection import build_repair_input

    _, text, _ = build_repair_input(original, assess(original, ctx), scope, ctx, prep, (evidence,))
    assert json.loads(text)["routes"][0]["elements"][0]["destination_place_id"] == "b"
    proposed = original.model_copy(deep=True)
    proposed.days[0].activities.append(visit("new", "b", start="11:00", end="12:00"))
    layout = check_addition_layout(original, proposed, places, (evidence,), "WALK", policy.spatial)
    assert layout["accepted"] and layout["legs"][0]["basis"] == "walk_provider_estimate"
    proposed.days[0].activities[1].start_time = original.days[0].activities[0].end_time + timedelta(
        minutes=5
    )
    layout = check_addition_layout(original, proposed, places, (evidence,), "WALK", policy.spatial)
    assert not layout["accepted"]
    assert "insufficient_layout_transfer_window" in layout["reasons"]
    assert layout["legs"][0]["basis"] == "walk_provider_estimate"


def test_same_activity_identity_replacement_receives_only_comparable_baseline_credit():
    original, ctx, _, policy = setup(
        [[visit("a", "a"), visit("b", "b", start="12:00", end="13:00")]]
    )
    old = matrix({"status": {}, "duration": "1200s"})
    new = old.model_copy(
        update={
            "elements": [
                old.elements[0].model_copy(update={"origin_place_id": "c", "duration_seconds": 600})
            ]
        }
    )
    proposed = original.model_copy(deep=True)
    proposed.days[0].activities[0].source_place_id = "c"
    result = check_addition_layout(
        original, proposed, ctx.places, (old, new), "WALK", policy.spatial
    )
    assert result["accepted"] and result["daily"][0]["added_minutes"] == 0
    assert result["daily"][0]["baseline_credits"][0]["minutes"] == 20
    missing = check_addition_layout(original, proposed, ctx.places, (new,), "WALK", policy.spatial)
    assert missing["daily"][0]["added_minutes"] == 10


def test_truncated_current_end_covers_last_minute_only_inside_saved_window():
    p = normalized(
        {
            "periods": [
                {
                    "open": {
                        "date": {"year": 2026, "month": 9, "day": 25},
                        "hour": 0,
                        "truncated": True,
                    },
                    "close": {
                        "date": {"year": 2026, "month": 10, "day": 1},
                        "hour": 23,
                        "minute": 59,
                        "truncated": True,
                    },
                }
            ]
        }
    )
    last = DAY + timedelta(days=5)
    view = selected_hours(p, last)
    assert view["intervals"][0][1] == "2026-10-02T00:00:00"
    assert not selected_hours(p, last + timedelta(days=1))["known"]


def test_malformed_and_missing_endpoint_are_not_closed_or_all_day():
    for row in ({"open": {}}, {"open": {"day": 8}, "close": {"day": 1}}, {"close": {"day": 1}}):
        view = selected_hours(normalized(regular={"periods": [row]}), DAY)
        assert not view["known"] and view["reason"] == "invalid_structured_period"


def test_selected_timezone_ignores_unrelated_candidate_and_keeps_local_conflict():
    from backend.app.versions.v3.repair_schedule import build_schedule

    original, ctx, _, _ = setup([[visit("a", "a")]])
    protection = {
        "dates": (DAY,),
        "start_time": "12:00",
        "end_time": "13:00",
        "status": "fixed",
        "reason": None,
        "source_refs": ({"quote": "rest", "start": 0, "end": 4, "occurrence": 0},),
    }
    from backend.app.schemas.interpreted_requirements import TimeProtection

    c = ctx.contract.model_copy(update={"time_protections": (TimeProtection(**protection),)})
    state = build_schedule(
        original, c, (place(), place("foreign", timezone_id="Asia/Tokyo")), primary_generated=True
    )
    assert not state.unresolved_dates and state.fixed
    original.days[0].activities.append(visit("b", "foreign", start="14:00", end="15:00"))
    state = build_schedule(
        original, c, (place(), place("foreign", timezone_id="Asia/Tokyo")), primary_generated=True
    )
    assert str(DAY) in state.unresolved_dates


def test_unresolved_named_binding_blocks_only_its_bounded_identity():
    from backend.tests.versions.v3.test_validation import binding, contract

    original, ctx, _, policy = setup([[visit("a", "a", start="17:00", end="18:00")]], reviews=())
    named = contract("OPTIONAL").named_places
    c = ctx.contract.model_copy(update={"named_places": named, "visit_requirements": ()})
    from dataclasses import replace

    unresolved = replace(
        binding("b"), status="ambiguous", resolved_place_id=None, matching_place_ids=("b", "c")
    )
    ctx = ctx.model_copy(
        update={
            "contract": c,
            "named_resolutions": (unresolved,),
            "places": (normalized(regular={"periods": [period()]}), *ctx.places[1:]),
        }
    )
    # REQUIRED provenance remains independent of the concrete, unrelated opening target.
    c = c.model_copy(
        update={"named_places": (named[0].model_copy(update={"inclusion": "REQUIRED"}),)}
    )
    ctx = ctx.model_copy(update={"contract": c})
    scope = operation_scope(original, assess(original, ctx), context=ctx, policy=policy)
    assert "delete" in next(p for p in scope.permissions if p.activity_id == "a").operations
    ctx = ctx.model_copy(
        update={"named_resolutions": (replace(unresolved, matching_place_ids=()),)}
    )
    scope = operation_scope(original, assess(original, ctx), context=ctx, policy=policy)
    assert next(p for p in scope.permissions if p.activity_id == "a").operations == {"retime"}


def test_basic_drive_fallback_and_time_sensitive_route_rules():
    from backend.app.versions.v3.repair_routes import route_rows

    base = matrix(
        {
            "status": {},
            "duration": "600s",
            "staticDuration": "550s",
            "fallbackInfo": {"routingMode": "FALLBACK_TRAFFIC_UNAWARE", "reason": "SERVER_ERROR"},
        }
    )
    base = base.model_copy(update={"travel_mode": "DRIVE", "routing_preference": "TRAFFIC_AWARE"})
    rows = route_rows("a", "b", "DRIVE", "TRAFFIC_AWARE", NOW, (base,))
    assert rows[0]["basis"] == "basic_drive_estimate"
    assert rows[0]["element"]["static_duration_seconds"] == 550
    sensitive = base.model_copy(
        update={"elements": [base.elements[0].model_copy(update={"fallback_info": None})]}
    )
    assert not route_rows("a", "b", "DRIVE", "TRAFFIC_AWARE", NOW, (sensitive,))
    assert not route_rows("b", "a", "DRIVE", "TRAFFIC_AWARE", NOW, (base,))
    assert not route_rows("a", "b", "TRANSIT", None, NOW, (base,))


def test_candidate_catalog_groups_preserve_authorization_and_object_uniqueness():
    from backend.app.versions.v3.repair_projection import build_repair_input
    from tools.diagnostics.repair_payload import fixture

    args = list(fixture(1, 28))
    prep = args[-1]
    auth = prep.authorizations[3].model_copy(update={"operation": "add"})
    args[-1] = prep.model_copy(update={"authorizations": (*prep.authorizations, auth)})
    _, text, counts = build_repair_input(*args)
    payload = json.loads(text)
    assert len(payload["candidate_catalog"]) == 28
    assert payload["addition_candidates"][0]["place_id"] == auth.place_id
    assert payload["addition_candidates"][0]["target_authorizations"] == [
        auth.model_dump(
            mode="json",
            exclude={
                "opportunity_signature",
                "opportunity_status",
                "opportunity_reason",
                "opportunity_windows",
            },
        )
    ]
    assert all("place" not in row for row in payload["other_operation_candidates"])
    assert counts["input_identity_union"] == 28


def test_actual_graph_uses_provider_periods_default_policy_and_final_report():
    from backend.tests.versions.v3.test_wiring import Model, Places, primary
    from backend.tests.versions.v3.test_wiring import execute as run_graph

    class HoursPlaces(Places):
        async def get_place_details(self, request):
            dto = await super().get_place_details(request)
            return dto.model_copy(
                update={
                    "regular_opening_hours": {"periods": [period(12, 18), period(12, 18, 0)]},
                    "current_opening_hours": None,
                }
            )

    original = primary(False)
    # Keep the unrelated second visit within the same provider opening window.
    second = original.days[1].activities[0]
    second.start_time += timedelta(hours=3)
    second.end_time += timedelta(hours=3)
    aid = original.days[0].activities[0].activity_id

    class Retime(Model):
        async def generate_repair_structured(self, **kwargs):
            self.repair_calls += 1
            return {
                "edits": [
                    {
                        "operation": "retime",
                        "activity_id": aid,
                        "date": "2026-09-12",
                        "place_id": None,
                        "start_time": "2026-09-12T12:00:00+10:00",
                        "end_time": "2026-09-12T14:00:00+10:00",
                    }
                ]
            }

    result, model, places, owner = asyncio.run(run_graph(Retime(original), HoursPlaces()))
    assert result.v3.repair.status == "ACCEPTED_COMPLETE", [
        (f.check, f.status, f.dates, f.reason) for f in result.v3.final_report.findings
    ]
    assert model.repair_calls == 1 and len(places.nearby) == 1
    assert owner.closes == 1
    assert (
        next(f for f in result.v3.original_report.findings if f.check == "opening").status
        == "CONFIRMED"
    )
    final = next(f for f in result.v3.final_report.findings if f.check == "opening")
    assert final.status == "PASS" and final.adopted_evidence["policy"] == "application_default"
    assert result.v3.draft == original


def test_success_and_applicable_no_route_remain_an_explicit_conflict():
    from backend.app.versions.v3.repair_routes import route_rows

    success = matrix({"status": {}, "duration": "600s"})
    missing = matrix({"status": {}, "condition": "ROUTE_NOT_FOUND"})
    assert not route_rows("a", "b", "WALK", None, NOW, (success, missing))
    error = matrix({"status": {"code": 13}, "condition": "ROUTE_NOT_FOUND"})
    assert route_rows("a", "b", "WALK", None, NOW, (success, error))


def test_special_gap_cannot_reappear_as_regular_open_in_generation_projection():
    from backend.app.evidence.opening_hours import opening_hours_for_date

    current = {"specialDays": [{"date": {"year": 2026, "month": 9, "day": 26}}]}
    p = normalized(
        current, {"periods": [period()], "weekdayDescriptions": ["Saturday: 09:00-17:00"]}
    )
    view = opening_hours_for_date(p, DAY)
    assert not view.structured_known
    assert view.basis == "current_date_window" and view.weekday_description is None
