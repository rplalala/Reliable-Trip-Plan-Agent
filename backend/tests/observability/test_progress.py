"""Opt-in timing, safe projection and concurrent observation isolation."""

import asyncio
from types import SimpleNamespace

import pytest

from backend.app.observability.progress import (
    ProgressObserver,
    ProgressTracer,
    current_progress,
    observed,
    progress_scope,
    skipped,
)


def test_real_duration_occurrences_parent_and_skips():
    clock = [10.0]
    observer = ProgressObserver(developer=True, version="v3", clock=lambda: clock[0])

    @observed("validation")
    def validate():
        clock[0] += 0.25

    @observed("repair")
    def repair():
        validate()
        validate()

    @observed("repair_round")
    def skip():
        clock[0] += 0.5
        return SimpleNamespace(
            status="SKIPPED",
            reason="insufficient_time_for_model_and_rechecks",
            model_attempted=False,
            target_progress=(),
        )

    with progress_scope(observer):
        repair()
        skip()
    events = list(observer.buffer)
    validations = [e for e in events if e.get("stage") == "validation"]
    assert [e["occurrence"] for e in validations] == [1, 1, 2, 2]
    assert all(e["parent_id"] == "repair:1" for e in validations)
    assert validations[1]["duration_ms"] == 250
    assert events[5]["duration_ms"] == 500  # Parent includes nested work, not a sum to display.
    assert events[-1]["status"] == "completed" and events[-1]["duration_ms"] == 500
    assert events[-1]["details"]["repair_status"] == "SKIPPED"
    assert events[-1]["details"]["model_attempted"] is False
    with progress_scope(observer):
        skipped("repair_model")
    assert observer.buffer[-1]["status"] == "skipped"
    assert "duration_ms" not in observer.buffer[-1]
    assert current_progress() is None


def test_opt_in_preserves_result_and_error_without_observer():
    value = object()

    @observed("generation")
    def run():
        return value

    assert run() is value


def test_failure_is_timed_without_exception_text():
    observer = ProgressObserver(developer=True)

    @observed("generation")
    def fail():
        raise ValueError("PRIVATE prompt")

    with progress_scope(observer), pytest.raises(ValueError):
        fail()
    assert observer.buffer[-1]["status"] == "failed"
    assert "duration_ms" in observer.buffer[-1]
    assert "PRIVATE" not in str(observer.buffer)


def test_product_projection_has_no_debug_details_or_version():
    observer = ProgressObserver()
    tracer = ProgressTracer(observer)
    with progress_scope(observer):
        observer.begin("repair", target_ids=["private"])
        tracer.event("semantic_candidate_admission", {"raw_count": 42})
        tracer.payload("llm", "prompt", "PRIVATE", minimum_mode=None)
    assert len(observer.buffer) == 1
    assert "version" not in observer.buffer[0]
    assert "details" not in observer.buffer[0]
    assert "PRIVATE" not in str(observer.buffer)


def test_developer_counter_allowlist_does_not_forward_raw_payload():
    observer = ProgressObserver(developer=True)
    tracer = ProgressTracer(observer)
    tracer.event(
        "semantic_candidate_admission",
        {
            "raw_count": 12,
            "merged_count": 8,
            "admitted_ids": ["a", "b"],
            "omitted_ids": ["c"],
            "prompt": "PRIVATE",
        },
    )
    tracer.event("v3_repair_patch", {"raw": "PRIVATE"})
    assert observer.buffer[0]["details"]["admitted_count"] == 2
    assert "PRIVATE" not in str(observer.buffer)


def test_bounded_buffer_reports_lost_events():
    observer = ProgressObserver(capacity=2)
    for _ in range(5):
        observer.emit("stage")
    event = asyncio.run(observer.next())
    assert event["sequence"] == 4
    assert event["dropped_events"] == 3


def test_concurrent_contexts_and_cancellation_are_independent():
    async def scenario():
        entered = asyncio.Event()
        observers = [ProgressObserver(developer=True, version=f"v{i}") for i in range(4)]

        @observed("generation")
        async def stage(index):
            if index == 0:
                entered.set()
                await asyncio.Event().wait()
            await entered.wait()

        async def run(index):
            with progress_scope(observers[index]):
                await stage(index)

        tasks = [asyncio.create_task(run(i)) for i in range(4)]
        await entered.wait()
        tasks[0].cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        return observers

    observers = asyncio.run(scenario())
    assert observers[0].buffer[-1]["status"] == "cancelled"
    for i, observer in enumerate(observers):
        assert all(e["version"] == f"v{i}" for e in observer.buffer)
        if i:
            assert observer.buffer[-1]["status"] == "completed"


def test_real_v3_graph_observation_keeps_final_result_and_reports_repair():
    from backend.tests.versions.v3.test_wiring import execute

    observer = ProgressObserver(developer=True, version="v3", capacity=1024)

    async def run():
        with progress_scope(observer):
            return await execute(tracer=ProgressTracer(observer))

    result = asyncio.run(run())
    # execute returns the result and its owned retrieval test double.
    output = result[0] if isinstance(result, tuple) else result
    assert output.system_version == "v3"
    events = list(observer.buffer)
    assert any(e.get("stage") == "repair_round" and e["status"] == "started" for e in events)
    assert any(e.get("stage") == "validation" and e["status"] == "completed" for e in events)
    assert any(e.get("name") == "generation_input" for e in events)
    assert any(e.get("stage") == "nearby" and e["status"] == "completed" for e in events)


def test_real_v0_runtime_observes_generation_without_changing_v0_files():
    from contextlib import asynccontextmanager
    from datetime import date

    from backend.app.services.planner_runtime import PlannerDependencies, RequestPlannerRuntime
    from backend.tests.request_fixtures import make_request
    from backend.tests.versions.v0.fakes import FakeStructuredLLMClient, make_itinerary

    client = FakeStructuredLLMClient([make_itinerary()])

    @asynccontextmanager
    async def dependencies(*args):
        yield PlannerDependencies(llm=client)

    observer = ProgressObserver(developer=True, version="v0")

    async def run():
        with progress_scope(observer):
            return await RequestPlannerRuntime(dependency_factory=dependencies).run(
                "v0", make_request(), reference_date=date(2026, 9, 11)
            )

    result = asyncio.run(run())
    assert result.system_version == "v0" and len(client.calls) == 1
    assert [(e["stage"], e["status"]) for e in observer.buffer] == [
        ("requirements", "started"),
        ("requirements", "completed"),
        ("generation", "started"),
        ("generation", "completed"),
    ]


@pytest.mark.parametrize("keyword_call", [False, True])
def test_repair_metadata_is_explicit_and_independent_of_argument_position(
    monkeypatch, keyword_call
):
    from inspect import signature

    from backend.app.versions.v3 import repair_service
    from backend.tests.versions.v3.test_wiring import execute

    original = repair_service.run_repair_once
    if keyword_call:

        async def dispatch(*args, **kwargs):
            bound = signature(original).bind(*args, **kwargs)
            return await original(**bound.arguments)

        monkeypatch.setattr(repair_service, "run_repair_once", dispatch)
    observer = ProgressObserver(developer=True, version="v3", capacity=1024)

    async def run():
        with progress_scope(observer):
            await execute(tracer=ProgressTracer(observer))

    asyncio.run(run())
    events = [e for e in observer.buffer if e.get("name") == "repair_targets"]
    assert events
    assert events[0]["stage_id"] == "repair_round:1"
    assert events[0]["details"]["round_index"] == 1
    assert events[0]["details"]["target_ids"]
    assert "permitted_operations" in events[0]["details"]
