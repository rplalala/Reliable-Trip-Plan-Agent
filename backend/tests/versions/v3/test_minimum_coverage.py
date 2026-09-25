"""Product minimum versus review quota; real validator and stage, fake providers."""

import asyncio
from datetime import timedelta

import pytest

from backend.app.policies.generation_diagnostics import observe_generation
from backend.app.schemas.interpreted_requirements import TimeProtection
from backend.app.versions.v3.repair_acceptance import assess
from backend.tests.versions.v3.test_b_targets import edit, run, setup, visit
from backend.tests.versions.v3.test_validation import DAY, activity


def protection(**changes):
    return TimeProtection.model_validate(
        dict(
            dates=[DAY],
            full_day=True,
            start_time=None,
            end_time=None,
            status="fixed",
            reason=None,
            source_refs=[
                dict(quote="Rest all day", occurrence=0, start=0, end=12, match_mode="exact")
            ],
            **changes,
        )
    )


@pytest.mark.parametrize("role", ["generic_activity", "free_time", "transport"])
def test_non_primary_is_missing_without_review(role):
    a = activity(pid=None, place_name=None, activity_kind=role)
    original, ctx, scope, _ = setup([[a]], reviews=())
    before = original.model_dump()
    report = assess(original, ctx)
    row = report.diagnostics.days[0]
    assert row.minimum_coverage == "missing"
    target = next(f for f in report.findings if f.reason == "minimum_daily_coverage_missing")
    assert target.status == "CONFIRMED" and target.magnitude == 1
    assert target.finding_id in scope.target_ids
    assert original.model_dump() == before


@pytest.mark.parametrize("missing", [False, True])
def test_zero_to_one_completes_without_quantity_review(missing):
    args = setup([[]], reviews=(), extra_days=int(missing))
    patches = [[edit("add", pid="a", start="10:00", end="11:00")]]
    if missing:
        patches[0].append(edit("add", pid="b", day=1, start="10:00", end="11:00"))
    result, model = run(args, patches)
    assert result.status == "ACCEPTED_COMPLETE", result.reason
    assert all(d.minimum_coverage == "satisfied" for d in result.adopted_report.diagnostics.days)
    assert model.calls == 1


def test_one_visit_passes_minimum_but_optional_review_remains():
    args = setup([[visit("a", "a")]])
    report = assess(args[0], args[1])
    assert report.diagnostics.days[0].minimum_coverage == "satisfied"
    assert any(f.check == "coverage" and f.status == "NEEDS_REVIEW" for f in report.findings)


def test_explicit_full_day_protection_exempts_and_blocks_visits():
    args = setup([[]], protections=(protection(),), reviews=())
    report = assess(args[0], args[1])
    assert report.diagnostics.days[0].minimum_coverage == "exempt"
    assert not report.improvement_targets and args[2] is None
    assert (args[1].schedule.fixed[0].end - args[1].schedule.fixed[0].start).days == 1


def test_complete_fixed_window_exempts_but_short_gap_does_not():
    for end, expected in [("18:00", "exempt"), ("17:59", "missing")]:
        p = protection().model_copy(
            update={
                "full_day": False,
                "start_time": __import__("datetime").time(9),
                "end_time": __import__("datetime").time.fromisoformat(end),
            }
        )
        args = setup([[]], protections=(p,))
        assert assess(args[0], args[1]).diagnostics.days[0].minimum_coverage == expected


@pytest.mark.parametrize(
    "protections",
    [
        None,
        (
            protection().model_copy(
                update={"full_day": None, "status": "unresolved", "reason": "Ambiguous day"}
            ),
        ),
    ],
)
def test_unassessed_or_unresolved_protection_is_not_confirmed_missing(protections):
    args = setup([[]], protections=protections)
    report = assess(args[0], args[1])
    assert report.diagnostics.days[0].minimum_coverage == "unknown"
    assert not any(f.status == "CONFIRMED" for f in report.findings)


def test_unknown_role_not_forced_to_zero_and_relaxed_not_exempt():
    args = setup([[activity(pid=None, place_name=None, activity_kind="unknown")]])
    assert assess(args[0], args[1]).diagnostics.days[0].minimum_coverage == "unknown"
    args = setup([[]])
    c = args[1].contract.model_copy(
        update={
            "requirements": args[1].contract.requirements.model_copy(
                update={"preferences": ["relaxed"]}
            )
        }
    )
    assert (
        assess(args[0], args[1].model_copy(update={"contract": c}))
        .diagnostics.days[0]
        .minimum_coverage
        == "missing"
    )


def test_minimum_is_first_active_target_and_failure_preserves_draft():
    args = setup([[visit("a", "a")], []])
    result, _ = run(args, [[]])
    assert result.final == args[0]
    first = result.rounds[0].result
    assert first.scope.add_dates == (DAY + timedelta(days=1),)
    assert first.scope.deferred_review_target_ids
    assert all(
        a.date == DAY + timedelta(days=1) for a in first.candidate_preparation.authorizations
    )
    assert result.adopted_report.diagnostics.days[1].minimum_coverage == "missing"


def test_shared_v0_proxy_and_canonical_observation_preserve_basis():
    args = setup([[visit("a", "a")], []])
    for supplied in [None, ("a",)]:
        report = observe_generation(
            args[0],
            args[1].contract.requirements,
            reference_date=DAY - timedelta(days=1),
            supplied_ids=supplied,
            contract=args[1].contract,
        )
        assert [d.minimum_coverage for d in report.days] == ["satisfied", "missing"]
        assert report.days[0].count_basis == ("name_proxy" if supplied is None else "canonical_id")


def test_real_graph_quantity_off_adds_to_empty_day_once_and_nearby_uses_adoption():
    from backend.tests.versions.v3.test_wiring import Model, execute, primary

    class Add(Model):
        async def generate_repair_structured(self, **kwargs):
            import json

            self.repair_calls += 1
            data = json.loads(kwargs["user_prompt"])
            c = data["addition_candidates"][0]
            return {
                "edits": [
                    dict(
                        operation="add",
                        activity_id=None,
                        place_id=c["place_id"],
                        date="2026-09-13",
                        start_time="2026-09-13T10:00:00+10:00",
                        end_time="2026-09-13T11:00:00+10:00",
                    )
                ]
            }

    draft = primary(False)
    draft.days[1].activities = []
    result, model, places, runtime = asyncio.run(execute(Add(draft)))
    assert model.repair_calls == 1
    assert result.v3.repair.status == "ACCEPTED_COMPLETE"
    assert result.generation_diagnostics.days[1].minimum_coverage == "satisfied"
    assert result.v3.draft.days[1].activities == []
    assert result.itinerary.days == result.v3.final_primary.days
    assert runtime.closes == 1 and places.nearby


def honolulu_context():
    import json
    from datetime import date
    from pathlib import Path

    from backend.app.evidence.models import PlaceEvidence
    from backend.app.policies.itinerary_schedule import build_schedule
    from backend.app.policies.trip_dates import create_trip_date_window
    from backend.app.runtime.config_loader import load_runtime_config
    from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements
    from backend.app.schemas.itinerary import Itinerary
    from backend.app.versions.v3.models import ValidationPolicy
    from backend.app.versions.v3.repair_models import ValidationContext
    from backend.app.versions.v3.wiring import operation_scope

    raw = json.loads(
        (Path(__file__).parents[2] / "fixtures/v3/honolulu_minimum_coverage.json").read_text()
    )
    draft = Itinerary.model_validate(raw["draft"])
    contract = InterpretedTripRequirements.model_validate(raw["contract"])
    places = tuple(PlaceEvidence.model_validate(p) for p in raw["places"])
    ctx = ValidationContext(
        contract=contract,
        window=create_trip_date_window(date(2026, 9, 25)),
        places=places,
        original_supply_ids=tuple(raw["supplied_ids"]),
        policy=ValidationPolicy(review_targets={"coverage", "repetition", "overfull"}),
        schedule=build_schedule(draft, contract, places, primary_generated=True),
    )
    policy = load_runtime_config().v3_repair
    scope = operation_scope(draft, assess(draft, ctx), context=ctx, policy=policy, mode="WALK")
    return draft, ctx, scope, policy


def test_honolulu_reconstruction_prioritizes_oct5_without_consuming_generic_activity():
    args = honolulu_context()
    original = args[0].model_dump()
    report = assess(args[0], args[1])
    by_day = {str(d.date): d for d in report.diagnostics.days}
    assert by_day["2026-10-05"].minimum_coverage == "missing"
    assert by_day["2026-10-01"].minimum_coverage == "satisfied"
    result, _ = run(args, [[]])
    first = result.rounds[0].result
    assert tuple(map(str, first.scope.add_dates)) == ("2026-10-05",)
    assert first.scope.deferred_review_target_ids
    assert all(str(a.date) == "2026-10-05" for a in first.candidate_preparation.authorizations)
    assert not first.window_adjustments
    assert result.final.model_dump() == original


def test_full_day_dto_mapping_requires_exact_user_source():
    from backend.app.llm.azure_foundry.dto import FoundryTimeProtectionDTO
    from backend.app.policies.interpreted_requirements import canonicalize_requirements
    from backend.app.schemas.interpreted_requirements import InterpretationDraft
    from backend.tests.request_fixtures import make_request

    request = make_request("Rest all day", start_date=DAY, end_date=DAY)
    wire = FoundryTimeProtectionDTO(dates=[str(DAY)], full_day=True,
        start_time=None, end_time=None, status="fixed", reason=None,
        source_refs=[{"quote": "Rest all day", "occurrence": 0}])
    from backend.tests.versions.v1.fakes import make_revised_extraction
    values = make_revised_extraction().model_dump()
    values["time_protections"] = [wire.model_dump()]
    draft = InterpretationDraft.model_validate(values)
    contract = canonicalize_requirements(draft, request)
    assert contract.time_protections[0].full_day
    assert contract.time_protections[0].source_refs[0].quote == request.additional_preferences
    with pytest.raises(Exception, match="source"):
        canonicalize_requirements(
            draft, make_request("A relaxed trip", start_date=DAY, end_date=DAY)
        )


def test_nearby_does_not_satisfy_minimum_and_public_report_has_no_quotes():
    from backend.app.schemas.generation_diagnostics import public_minimum_coverage
    args = setup([[]], reviews=())
    args[0].reference_recommendations = []
    # References are never traversed by the counting policy (regardless of ledger size).
    args[0].reference_recommendations.append({"place_name": "Nearby museum"})
    report = observe_generation(args[0], args[1].contract.requirements,
        reference_date=DAY-timedelta(days=1), supplied_ids=("a",), contract=args[1].contract)
    public = public_minimum_coverage(report)[0].model_dump()
    assert public["status"] == "missing" and public["countable_primary_activities"] == 0
    assert "source_refs" not in public and "minimum_coverage_evidence" not in public
