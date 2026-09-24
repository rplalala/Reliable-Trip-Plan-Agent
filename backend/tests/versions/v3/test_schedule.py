"""A-only time/adjacency integration, using exclusively offline fixtures."""

import asyncio
import json
from datetime import timedelta
from pathlib import Path
from time import monotonic

import pytest

from backend.app.evidence.models import PlaceEvidence
from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements, TimeProtection
from backend.app.schemas.itinerary import Itinerary
from backend.app.versions.v3.repair_routes import bind_transitions
from backend.app.versions.v3.repair_schedule import (
    build_schedule,
    ordered_activities,
    window_projection,
)
from backend.app.versions.v3.repair_service import run_repair_once, run_repair_stage
from backend.app.versions.v3.wiring import operation_scope
from backend.tests.versions.v3.test_repair import Model, context, edit
from backend.tests.versions.v3.test_validation import DAY, activity, draft


def setup(activities=None, protections=()):
    original = draft(
        activities
        if activities is not None
        else [
            activity(start="09:00", end="10:00"),
            activity(
                "free",
                None,
                "10:00",
                "17:00",
                activity_kind="free_time",
                place_name=None,
                location=None,
            ),
        ]
    )
    ctx = context()
    ctx = ctx.model_copy(
        update={"contract": ctx.contract.model_copy(update={"time_protections": protections})}
    )
    state = build_schedule(original, ctx.contract, ctx.places, primary_generated=True)
    ctx = ctx.model_copy(update={"schedule": state})
    from backend.app.versions.v3.repair_acceptance import assess

    scope = operation_scope(original, assess(original, ctx), mode="WALK")
    scope = scope.model_copy(
        update={"window_roots": tuple(w.root_activity_id for w in state.windows)}
    )
    return original, ctx, scope


def addition(pid="b", start="12:00", end="13:00"):
    return edit(start, end, operation="add", activity_id=None, place_id=pid)


def execute(original, ctx, scope, edits):
    return asyncio.run(
        run_repair_once(
            original, ctx, scope, model=Model(edits), request_deadline=monotonic() + 300
        )
    )


def test_elastic_addition_atomically_splits_and_preserves_original():
    original, ctx, scope = setup()
    saved = original.model_dump()
    result = execute(original, ctx, scope, [addition()])
    assert result.status == "ACCEPTED_COMPLETE", result.reason
    assert original.model_dump() == saved
    assert result.comparison.business_values[0]["after_distinct_main"] == 2
    assert result.window_adjustments and result.schedule.lineage
    assert not any(
        f.check == "overlap" and f.status == "CONFIRMED" for f in result.proposed_report.findings
    )
    assert all(a.activity_id != "free" for a in result.final.days[0].activities)
    assert all(
        b.from_activity_id != "free" and b.to_activity_id != "free"
        for b in bind_transitions(result.final, "WALK", schedule=result.schedule)
    )
    assert len(window_projection(result.final, result.schedule, scope.window_roots)) == 2


def test_legacy_unassessed_does_not_gain_placeholder_permission():
    original, ctx, scope = setup(protections=None)
    assert not ctx.schedule.windows and not scope.window_roots
    result = execute(original, ctx, scope, [addition()])
    assert result.status == "REJECTED"
    assert result.final == original


def protection(status="fixed", dates=(DAY,)):
    return TimeProtection(
        dates=dates,
        start_time="12:00",
        end_time="14:00",
        status=status,
        reason="Ambiguous local time" if status == "unresolved" else None,
        source_refs=({"quote": "rest", "start": 0, "end": 4, "occurrence": 0},),
    )


@pytest.mark.parametrize("status", ["fixed", "unresolved"])
def test_explicit_rest_and_unresolved_scope_block_consumption(status):
    original, ctx, scope = setup(protections=(protection(status),))
    result = execute(original, ctx, scope, [addition()])
    assert result.status == "REJECTED" and result.final == original
    assert "time" in result.reason.lower()


def test_fixed_rest_can_preserve_only_its_interval_not_whole_afternoon():
    original, ctx, scope = setup(protections=(protection(),))
    result = execute(original, ctx, scope, [addition(start="15:00", end="16:00")])
    assert result.status == "ACCEPTED_COMPLETE", result.reason
    fixed = ctx.schedule.fixed[0]
    assert any(
        a.start_time <= fixed.start and a.end_time >= fixed.end
        for a in result.final.days[0].activities
        if a.activity_kind == "free_time"
    )


def test_two_rounds_use_residual_window_and_later_failure_retains_adoption():
    original, ctx, scope = setup(
        [
            activity(
                "free",
                None,
                "09:00",
                "17:00",
                activity_kind="free_time",
                place_name=None,
                location=None,
            )
        ]
    )

    class Sequence(Model):
        async def generate_repair_structured(self, **kwargs):
            self.calls += 1
            if self.calls == 1:
                return {"edits": [addition("a", "10:00", "11:00")]}
            return {"edits": [addition("b", "12:00", "13:00")]}

    result = asyncio.run(
        run_repair_stage(original, ctx, scope, model=Sequence(), request_deadline=monotonic() + 600)
    )
    assert result.status == "ACCEPTED_COMPLETE", result.reason
    assert len(result.rounds) == 2
    assert result.rounds[0].result.status == "ACCEPTED_PARTIAL"
    assert result.rounds[1].input_itinerary == result.rounds[0].adopted
    assert len({a.activity_id for d in result.final.days for a in d.activities}) == sum(
        len(d.activities) for d in result.final.days
    )

    class Failing(Sequence):
        async def generate_repair_structured(self, **kwargs):
            if self.calls:
                raise RuntimeError("fixture failure")
            return await super().generate_repair_structured(**kwargs)

    failed = asyncio.run(
        run_repair_stage(original, ctx, scope, model=Failing(), request_deadline=monotonic() + 600)
    )
    assert failed.status == "ACCEPTED_PARTIAL"
    assert failed.final == failed.rounds[0].adopted
    assert failed.schedule == failed.rounds[0].result.schedule


@pytest.mark.parametrize("edits", [[addition("invented")], [addition(start="09:30", end="10:30")]])
def test_invalid_proposal_rolls_back_visits_and_placeholders(edits):
    original, ctx, scope = setup()
    saved = original.model_dump()
    result = execute(original, ctx, scope, edits)
    assert result.status == "REJECTED"
    assert result.final.model_dump() == saved == original.model_dump()
    assert result.schedule == ctx.schedule


def test_real_unknown_activity_remains_a_route_barrier():
    original, ctx, scope = setup(
        [
            activity(start="09:00", end="10:00"),
            activity("unknown", None, "11:00", "11:30", activity_kind="generic_activity"),
            activity(
                "free",
                None,
                "11:30",
                "17:00",
                activity_kind="free_time",
                place_name=None,
                location=None,
            ),
        ]
    )
    assert "unknown" in [a.activity_id for a in ordered_activities(original.days[0], ctx.schedule)]
    result = execute(original, ctx, scope, [addition()])
    assert result.status == "REJECTED" and result.final == original


def test_real_far_candidate_is_not_accepted_by_window_consumption():
    original, ctx, scope = setup()
    ctx = ctx.model_copy(
        update={
            "places": tuple(
                p.model_copy(update={"latitude": 40}) if p.place_id == "b" else p
                for p in ctx.places
            )
        }
    )
    result = execute(original, ctx, scope, [addition()])
    assert not result.status.startswith("ACCEPTED")


def test_cost_obligation_and_original_role_are_protected():
    original, ctx, scope = setup(
        [
            activity(start="09:00", end="10:00"),
            activity(
                "free",
                None,
                "10:00",
                "17:00",
                activity_kind="free_time",
                place_name=None,
                location=None,
                estimated_cost={"amount": 10, "currency": "GBP"},
            ),
        ]
    )
    assert not ctx.schedule.windows
    assert execute(original, ctx, scope, [addition()]).status == "REJECTED"


def historical_case(index):
    data = json.loads(
        (Path(__file__).parents[2] / "fixtures/v3/historical_free_time.json").read_text(
            encoding="utf-8"
        )
    )
    original = Itinerary.model_validate(data["draft"])
    # Explicit synthetic new-contract assessment; NOT observed in the historical run.
    contract = InterpretedTripRequirements.model_validate(data["contract"]).model_copy(
        update={"time_protections": ()}
    )
    places = tuple(PlaceEvidence.model_validate(p) for p in data["places"])
    from datetime import date

    from backend.app.policies.trip_dates import create_trip_date_window

    ctx = context(
        contract,
        places=places,
        original_supply_ids=tuple(p.place_id for p in places),
        window=create_trip_date_window(date(2026, 9, 23)),
    )
    ctx = ctx.model_copy(
        update={"schedule": build_schedule(original, contract, places, primary_generated=True)}
    )
    from backend.app.versions.v3.repair_acceptance import assess

    scope = operation_scope(original, assess(original, ctx), mode="WALK")
    scope = scope.model_copy(
        update={"window_roots": tuple(w.root_activity_id for w in ctx.schedule.windows)}
    )
    return original, ctx, scope, data["patches"][index]["edits"]


@pytest.mark.parametrize("index", range(3))
def test_historical_patches_no_longer_use_free_time_as_geographic_endpoints(index):
    original, ctx, scope, edits = historical_case(index)
    result = execute(original, ctx, scope, edits)
    assert result.parsed_patch is not None
    assert all(
        "free" not in b.from_activity_id
        and "rest" not in b.from_activity_id
        and "afternoon" not in b.from_activity_id
        for b in bind_transitions(original, "WALK", schedule=ctx.schedule)
    )
    if result.proposed_report:
        assert not any(
            f.check == "overlap" and f.status == "CONFIRMED"
            for f in result.proposed_report.findings
        )
    assert "coordinates_required_for_automatic_addition" not in result.reason
    assert original == result.original
    expected = (
        "Insufficient unoccupied transfer window" if index == 0 else "no_route_fallback_distance"
    )
    assert result.status == "REJECTED" and expected in result.reason


def test_actual_graph_consumes_placeholder_and_nearby_uses_adopted_visits():
    from backend.tests.versions.v3.test_wiring import Model as GraphModel
    from backend.tests.versions.v3.test_wiring import execute as graph_execute
    from backend.tests.versions.v3.test_wiring import primary

    original = primary(False)
    a = original.days[0].activities[0]
    original.days[0].activities.append(
        a.model_copy(
            update={
                "activity_id": "elastic",
                "activity_kind": "free_time",
                "source_place_id": None,
                "place_name": None,
                "location": None,
                "start_time": a.end_time,
                "end_time": a.end_time + timedelta(hours=7),
                "estimated_cost": None,
            }
        )
    )
    model = GraphModel(original, "existing_add")
    result, model, places, runtime = asyncio.run(graph_execute(model, quantity_review_enabled=True))
    assert result.v3.repair.status.startswith("ACCEPTED"), result.v3.repair.reason
    assert model.payload["time_windows"]
    assert result.v3.repair.window_adjustments
    assert not any(
        f.check == "overlap" and f.status == "CONFIRMED" for f in result.v3.final_report.findings
    )
    assert result.generation_diagnostics == result.v3.final_report.diagnostics
    assert result.request_resources["closed"] and runtime.closes == 1
    assert model.repair_calls >= 1
    assert result.v3.draft == original
    ids = {
        a.source_place_id
        for d in result.v3.final_primary.days
        for a in d.activities
        if a.source_place_id
    }
    assert {a["place_id"] for a in result.nearby_diagnostics["anchors"]} <= ids
    assert len(places.nearby) <= 2
    assert result.v3.draft_cost_projections == result.v3.final_cost_projections


def test_intermediate_addition_checks_two_real_neighbors_and_retains_route_evidence():
    from backend.app.versions.v3.repair_service import relevant_routes
    from backend.tests.versions.v3.test_repair import route

    original, ctx, scope = setup(
        [
            activity(start="09:00", end="10:00"),
            activity("free", None, "10:00", "17:00", activity_kind="free_time", place_name=None),
            activity("last", "a", "17:00", "18:00"),
        ]
    )
    # Quantity remains one distinct main identity; this is not repeat repair.
    result = execute(original, ctx, scope, [addition()])
    assert result.status == "ACCEPTED_COMPLETE", result.reason
    assert len(result.spatial["legs"]) == 2
    assert {(r["from_activity_id"], r["to_activity_id"]) for r in result.spatial["legs"]} == {
        ("one", "repair_r1_new_1"),
        ("repair_r1_new_1", "last"),
    }
    evidence = route(travel_mode="WALK", representative_departure_time=None)
    assert relevant_routes(result.final, scope, (evidence,), result.schedule)
    assert result.candidate_preparation.elastic_windows


def test_fixed_occupancy_cannot_be_credited_as_transfer_time():
    from backend.app.versions.v3.repair_schedule import TimeWindow, available_minutes
    from backend.app.versions.v3.repair_spatial import layout_measure
    from backend.tests.versions.v3.test_repair import route

    left = activity(start="09:00", end="10:00")
    right = activity("two", "b", "12:00", "13:00")
    _, ctx, _ = setup()
    fixed = TimeWindow(
        root_activity_id="fixed",
        start=left.end_time,
        end=right.start_time - timedelta(minutes=30),
        source="fixture",
    )
    state = ctx.schedule.model_copy(update={"fixed": (fixed,)})
    measured = route(duration=1200, travel_mode="WALK", representative_departure_time=None)
    timed = route(duration=1200, travel_mode="WALK", representative_departure_time=left.end_time)
    assert available_minutes(left, right, state) == 30
    assert available_minutes(left, right, state, at_departure=True) == 0
    assert layout_measure(left, right, "WALK", (timed,), schedule=state)[1] == "route_unknown"
    assert (
        layout_measure(left, right, "WALK", (measured,), schedule=state)[1]
        == "untimed_walk_measurement"
    )


def test_unbound_explicit_transport_is_neither_erased_nor_credited():
    original, ctx, scope = setup(
        [
            activity(start="09:00", end="10:00"),
            activity("ride", None, "10:00", "11:00", activity_kind="transport"),
            activity("free", None, "11:00", "17:00", activity_kind="free_time", place_name=None),
        ]
    )
    result = execute(original, ctx, scope, [addition()])
    assert not result.status.startswith("ACCEPTED")
    assert result.final == original
    assert "ride" in [a.activity_id for a in ordered_activities(original.days[0], ctx.schedule)]


def test_scope_cannot_expand_root_authorization_and_direct_placeholder_edit_is_rejected():
    from backend.app.versions.v3.repair_models import ActivityPermission

    original, ctx, scope = setup()
    scope = scope.model_copy(update={"window_roots": ("invented",)})
    result = execute(original, ctx, scope, [addition()])
    assert result.status == "REJECTED" and result.final == original
    original, ctx, scope = setup()
    scope = scope.model_copy(
        update={"permissions": (ActivityPermission(activity_id="free", operations={"retime"}),)}
    )
    result = execute(original, ctx, scope, [edit("14:00", "15:00", activity_id="free")])
    assert "application" in result.reason and result.final == original


def test_relaxed_soft_preference_does_not_freeze_generated_window():
    from backend.app.policies.interpreted_requirements import canonicalize_requirements
    from backend.tests.request_fixtures import make_request
    from backend.tests.versions.v1.test_interpreted_requirements import draft_for

    original, ctx, scope = setup()
    semantic = canonicalize_requirements(
        draft_for("relaxed", time_protections=()), make_request("relaxed")
    ).semantic_requirements
    ctx = ctx.model_copy(
        update={"contract": ctx.contract.model_copy(update={"semantic_requirements": semantic})}
    )
    ctx = ctx.model_copy(
        update={
            "schedule": build_schedule(original, ctx.contract, ctx.places, primary_generated=True)
        }
    )
    result = execute(original, ctx, scope, [addition()])
    assert result.status == "ACCEPTED_COMPLETE", result.reason


def test_meaningful_cost_projection_without_safe_amount_is_not_discarded():
    from backend.app.schemas.itinerary_projection import (
        EstimatedCostProjectionDiagnostic,
        V1Itinerary,
    )

    original, ctx, _ = setup()
    original = V1Itinerary.model_validate(original.model_dump())
    original.set_cost_projections(
        (
            EstimatedCostProjectionDiagnostic(
                field_path="days[0].activities[1].estimated_cost",
                projection="exact_point",
                midpoint="10",
            ),
        )
    )
    state = build_schedule(original, ctx.contract, ctx.places, primary_generated=True)
    assert not state.windows
    assert state.classifications[0]["reason"] == "cost_obligation"


def test_confirmed_real_route_conflict_survives_elastic_endpoint_view():
    from backend.app.versions.v3.repair_routes import check_transitions
    from backend.tests.versions.v3.test_repair import route

    original, ctx, _ = setup()
    original.days[0].activities.append(activity("two", "b", "12:00", "13:00"))
    evidence = route(
        duration=8000,
        travel_mode="WALK",
        representative_departure_time=original.days[0].activities[0].end_time,
    )
    findings = list(
        check_transitions(
            original,
            bind_transitions(original, "WALK", schedule=ctx.schedule),
            (evidence,),
            ctx.schedule,
        )
    )
    assert any(f["status"] == "CONFIRMED" and f["activity_ids"] == ("one", "two") for f in findings)


def test_existing_private_activity_is_protected_without_claiming_semantic_conflict():
    from backend.app.versions.v3.repair_acceptance import assess
    from backend.app.versions.v3.repair_schedule import check_time_permissions

    original, ctx, _ = setup(
        [
            activity(start="09:00", end="10:00"),
            activity("private", None, "12:00", "14:00", activity_kind="generic_activity"),
        ],
        protections=(protection(),),
    )
    report = assess(original, ctx)
    assert any(
        f.reason == "activity_time_protection_relationship_unbound" and f.status == "UNKNOWN"
        for f in report.findings
    )
    changed = original.model_copy(deep=True)
    changed.days[0].activities.pop()
    with pytest.raises(ValueError, match="safe change binding"):
        check_time_permissions(original, changed, ctx.schedule)


def test_superseded_transfer_is_not_counted_as_simultaneous_travel():
    from backend.app.versions.v3.repair_schedule import retained_transfers

    original, ctx, scope = setup()
    first = execute(original, ctx, scope, [addition()])
    assert first.status == "ACCEPTED_COMPLETE"
    adopted = first.final
    inserted = adopted.model_copy(deep=True)
    inserted.days[0].activities.append(activity("another", "c", "11:00", "11:15"))
    assert first.schedule.occupied_transfers
    assert retained_transfers(adopted, adopted, first.schedule) == first.schedule.occupied_transfers
    assert not retained_transfers(adopted, inserted, first.schedule)
    assert first.schedule.occupied_transfers  # Prior audit is immutable.
