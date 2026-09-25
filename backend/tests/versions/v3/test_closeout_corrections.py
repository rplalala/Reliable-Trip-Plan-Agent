"""Review regressions through real route validation and the offline Repair stage."""

from time import monotonic

import pytest

from backend.app.policies.itinerary_schedule import ScheduleState, TimeWindow
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.versions.v3.repair_budget import RepairBudget
from backend.app.versions.v3.repair_routes import bind_transitions, check_transitions
from backend.tests.versions.v3.test_b_targets import edit as b_edit
from backend.tests.versions.v3.test_b_targets import repeated, run, setup, visit
from backend.tests.versions.v3.test_mixed_transport import measured
from backend.tests.versions.v3.test_multiround import SequenceModel, policy, stage
from backend.tests.versions.v3.test_repair import activity, draft, edit


@pytest.mark.parametrize("mode", ["WALK", "DRIVE"])
def test_formal_route_uses_bound_departure_not_largest_free_interval(mode):
    left, right = activity(end="11:50"), activity("two", "b", "14:00", "15:00")
    original = draft([left, right])
    schedule = ScheduleState(
        fixed=(
            TimeWindow(
                root_activity_id="rest",
                start=left.end_time.replace(hour=12, minute=0),
                end=left.end_time.replace(hour=13, minute=0),
                source="explicit_fixed_rest",
            ),
        )
    )
    bindings = bind_transitions(
        original, mode, "TRAFFIC_UNAWARE" if mode == "DRIVE" else None, schedule
    )
    evidence = (measured(mode, 1200),)
    first = list(check_transitions(original, bindings, evidence, schedule))[0]
    assert first["status"] == "CONFIRMED"
    assert first["magnitude"] == 600
    later = (bindings[0].model_copy(update={"departure_time": schedule.fixed[0].end}),)
    assert list(check_transitions(original, later, evidence, schedule))[0]["status"] == "PASS"
    blocked = (bindings[0].model_copy(update={"departure_time": schedule.fixed[0].start}),)
    assert (
        list(check_transitions(original, blocked, evidence, schedule))[0]["status"] == "CONFIRMED"
    )


def test_runtime_snapshot_controls_standalone_stage_without_duplicate_policy(monkeypatch):
    config = load_runtime_config().model_copy(
        update={
            "v3_repair": policy(max_rounds=1, max_model_calls=1),
        }
    )

    def forbidden_reload():
        raise AssertionError("Injected runtime must not reload YAML")

    with monkeypatch.context() as patcher:
        patcher.setattr("backend.app.runtime.config_loader.load_runtime_config", forbidden_reload)
        budget = RepairBudget(monotonic() + 600, runtime_config=config)
    assert budget.policy is config.v3_repair
    model = SequenceModel([[edit("10:50", "11:50")], [edit()]])
    result = stage(model, runtime_config=config)
    assert model.calls == 1 and len(result.rounds) == 1
    assert result.effective_policy["max_rounds"] == 1


def test_missing_runtime_repair_policy_fails_and_explicit_policy_wins():
    config = load_runtime_config().model_copy(update={"v3_repair": None})
    with pytest.raises(ValueError, match="runtime.v3_repair"):
        RepairBudget(monotonic() + 600, runtime_config=config)
    explicit = policy(max_rounds=1, max_model_calls=1)
    assert (
        RepairBudget(monotonic() + 600, runtime_config=config, policy=explicit).policy is explicit
    )


@pytest.mark.parametrize("next_response", [[], RuntimeError("fixture failure")])
def test_stage_summary_retains_adopted_loss_after_noop_or_failure(next_response):
    args = setup(
        [[visit("a", "a"), visit("b", "b", start="12:00", end="13:00")]],
        reviews=(),
        required="EXCLUDED",
    )
    result, model = run(args, [[b_edit("delete", "a")], next_response])
    assert model.calls >= 2
    assert result.status == "ACCEPTED_PARTIAL"
    assert result.final == result.rounds[0].adopted
    assert result.main_visits_lost == ("a",)
    assert result.comparison.progress == result.target_progress
    assert result.comparison.accepted
    assert result.coverage_regressions == result.comparison.coverage_regressions
    assert result.spatial["accepted"]
    assert result.rounds[1].result.main_visits_lost == ()


def test_rejected_proposal_losses_remain_in_round_not_adopted_stage_summary():
    args = repeated()
    result, _ = run(args, [[b_edit("delete", "a2", day=1)]])
    assert result.final == args[0]
    assert result.main_visits_lost == ()
    assert result.coverage_regressions == ()
    assert result.rounds[0].result.main_visits_lost == ("a2",)
    assert result.comparison.progress == result.target_progress


def test_later_rejected_deletion_does_not_pollute_earlier_adopted_loss():
    args = setup(
        [
            [
                visit(pid, pid, start=f"{9 + i:02d}:00", end=f"{9 + i:02d}:30")
                for i, pid in enumerate("abcdef")
            ],
            [visit("a2", "a", 1), visit("g", "g", 1, start="12:00", end="13:00")],
        ],
        reviews=("overfull", "repetition"),
    )
    result, _ = run(args, [[b_edit("delete", "f")], [b_edit("delete", "a2", day=1)]])
    assert result.rounds[0].result.status == "ACCEPTED_PARTIAL"
    assert result.rounds[1].result.status == "REJECTED"
    assert result.rounds[1].result.main_visits_lost == ("a2",)
    assert result.main_visits_lost == ("f",)
    assert result.final == result.rounds[0].adopted
    assert result.comparison.accepted
    # Existing comparison records every count reduction, including allowed 6 -> 5.
    assert result.coverage_regressions == (args[0].days[0].date,)
    assert args[0].days[1].date not in result.coverage_regressions
