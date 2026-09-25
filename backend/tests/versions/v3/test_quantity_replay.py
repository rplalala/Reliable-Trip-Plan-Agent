"""Synthetic stage snapshots exercise full-pool reuse without external services."""

import asyncio
import json

import pytest

from backend.app.evidence.selection_models import RatingAcquisitionState
from backend.app.runtime.cache import RequestCache
from backend.app.runtime.config_loader import load_runtime_config
from backend.tests.services.test_poi_semantics import service
from backend.tests.versions.v3.test_b_targets import setup, visit
from backend.tests.versions.v3.test_repair import selection
from backend.tests.versions.v3.test_validation import place


def snapshot():
    from tools.validation.repair_replay import make_snapshot

    original, context, scope, _ = setup([[visit("a", "a")]], reviews=("coverage",))
    context = context.model_copy(update={"original_supply_ids": ("a",), "places": (place("a"),)})
    rich = selection("z").model_copy(
        update={"structured_evidence": place("z"), "rating_state": RatingAcquisitionState.MISSING}
    )
    semantics = service()
    asyncio.run(semantics.assess([place("a"), place("z")], context.contract))
    return make_snapshot(
        original=original,
        context=context,
        scope=scope,
        enriched=(rich,),
        admitted=(rich, selection("pending")),
        runtime=load_runtime_config(),
        request_remaining=123,
        cache=RequestCache(),
        semantic_service=semantics,
        geographic_scope=None,
        intent_ids=(),
        provenance="synthetic",
    )


def test_complete_pool_roundtrip_reuses_details_and_semantics_without_new_calls():
    from tools.validation.repair_replay import ReplaySnapshot, replay

    saved = snapshot()
    restored = ReplaySnapshot.model_validate_json(saved.model_dump_json())
    first = asyncio.run(replay(restored))
    assert first == asyncio.run(replay(restored))
    assert first["provenance"] == "synthetic"
    assert first["pool_ids"] == ["z", "pending"]
    assert first["budget_used"]["qualified_reuse"] == 1
    assert first["semantic_missing"] == []
    assert first["semantic_calls"] == saved.semantics.calls
    assert "z" in [c["place"]["place_id"] for c in first["preparation"]["ledger"]]
    assert any(d["reason"] == "details_not_acquired" for d in first["preparation"]["decisions"])
    assert all(
        first["budget_used"].get(k, 0) == 0 for k in ("model", "google", "details", "routes")
    )


@pytest.mark.parametrize("review", [False, True])
def test_graph_capture_records_full_pool_even_when_review_is_off(tmp_path, review):
    from backend.tests.versions.v3.test_wiring import ManyPlaces, Model, execute, primary
    from tools.validation.repair_replay import CapturedRepair, ReplaySnapshot, replay

    errors = []
    wrapped = CapturedRepair(
        Model(primary(False), "add"), tmp_path, {"case_id": "synthetic"}, errors
    )
    result, _, _, _ = asyncio.run(
        execute(wrapped, places=ManyPlaces(), quantity_review_enabled=review)
    )
    assert result.v3.quantity_review_enabled is review
    assert not errors
    saved = ReplaySnapshot.model_validate(
        json.loads(next(tmp_path.glob("*.json")).read_text())["snapshot"]
    )
    assert len(saved.enriched) > len(saved.context.original_supply_ids)
    assert saved.admitted and saved.semantics.calls > 0
    if not review:
        assert not wrapped.client.repair_calls
        assert saved.scope is None
        assert asyncio.run(replay(saved))["stop"] == "no_authorized_targets"
    else:
        assert wrapped.client.repair_calls
        catalog = {c["place"]["place_id"] for c in wrapped.client.payload["candidate_catalog"]}
        assert catalog - set(saved.context.original_supply_ids)
        assert asyncio.run(replay(saved))["preparation"]


@pytest.mark.parametrize("failure", ["overflow", "write", "raise"])
def test_capture_failure_does_not_change_graph_result(tmp_path, monkeypatch, failure):
    from backend.tests.versions.v3.test_wiring import Model, execute, primary
    from tools.validation.repair_replay import CapturedRepair

    errors = []
    wrapped = CapturedRepair(Model(primary(False)), tmp_path, {}, errors)

    def fail(*args, **kwargs):
        if failure == "overflow":
            raise OverflowError("Synthetic cap")
        if failure == "raise":
            raise OSError("Synthetic disk error")
        return None

    monkeypatch.setattr(wrapped.capture, "record", fail)
    result, _, _, _ = asyncio.run(execute(wrapped))
    assert result.v3.quantity_review_enabled is False
    assert not wrapped.client.repair_calls
    assert errors


def test_acceptance_override_and_capture_are_explicit(tmp_path, monkeypatch):
    from backend.tests.llm.azure_foundry.test_poi_semantics_acceptance import setup_case
    from tools.validation import poi_semantics_acceptance as entry
    from tools.validation.poi_semantics_acceptance import run_case

    request, _, _ = setup_case(tmp_path, monkeypatch)
    seen = []
    original_main = entry.v3_main

    def observed_main(argv):
        seen.append(argv)
        return original_main(argv)

    monkeypatch.setattr(entry, "v3_main", observed_main)
    result = run_case(request, tmp_path / "off", reference_date="2026-09-26")
    assert result["repair_capture_status"] == "disabled"
    assert "--repair-quantity-review" not in seen[-1]
    assert "--no-repair-quantity-review" not in seen[-1]
    result = run_case(
        request,
        tmp_path / "on",
        reference_date="2026-09-26",
        capture_repair=True,
        repair_quantity_review=True,
    )
    manifest = json.loads((tmp_path / "on" / "manifest.json").read_text())
    assert manifest["repair_quantity_review"] is True
    assert manifest["quantity_review_source"] == "explicit_override"
    assert "--repair-quantity-review" in seen[-1]
    # This fixture fails interpretation, before a pre-Repair snapshot exists.
    assert result["repair_capture_status"] == "incomplete"
    assert "repair_snapshot_not_reached" in result["repair_capture_errors"]
    run_case(
        request,
        tmp_path / "explicit-off",
        reference_date="2026-09-26",
        repair_quantity_review=False,
    )
    assert "--no-repair-quantity-review" in seen[-1]


@pytest.mark.parametrize("count", [1, 3, 5])
def test_addition_permissions_follow_arbitrary_sparse_dates(count):
    from tools.validation.repair_replay import make_snapshot, replay

    original, context, scope, _ = setup(
        [[visit(chr(97 + i), chr(97 + i), day=i)] for i in range(count)], reviews=("coverage",)
    )
    semantics = service()
    asyncio.run(semantics.assess(context.places, context.contract))
    saved = make_snapshot(
        original=original,
        context=context,
        scope=scope,
        enriched=(),
        admitted=(),
        runtime=load_runtime_config(),
        request_remaining=600,
        cache=RequestCache(),
        semantic_service=semantics,
        geographic_scope=None,
        intent_ids=(),
        provenance="synthetic",
    )
    result = asyncio.run(replay(saved))
    assert result["scope"]["add_dates"] == [str(d.date) for d in original.days]
    assert result["scope"]["permissions"] == []
    assert result["scope"]["revisits"] == []


def test_stale_semantic_input_and_budget_exhaustion_do_not_refresh_evidence(monkeypatch):
    from backend.app.services import poi_semantics
    from tools.validation.repair_replay import replay

    saved = snapshot()
    monkeypatch.setattr(poi_semantics, "POI_SEMANTICS_PROMPT", "Changed synthetic prompt")
    result = asyncio.run(replay(saved))
    assert result["semantic_missing"] == ["a", "z"]
    assert not result["semantic_prompt_matches"]
    assert not result["preparation"]["authorizations"]
    assert result["semantic_calls"] == saved.semantics.calls
    exhausted = saved.model_copy(update={"request_remaining": 0, "repair_remaining": 0})
    result = asyncio.run(replay(exhausted))
    assert result["stop"] == "insufficient_stage_time"
    assert result["preparation"] is None


def test_incomplete_snapshot_rejected_instead_of_fresh_defaults():
    from pydantic import ValidationError

    from tools.validation.repair_replay import ReplaySnapshot

    document = snapshot().model_dump(mode="json")
    del document["request_remaining"]
    with pytest.raises(ValidationError):
        ReplaySnapshot.model_validate(document)


def test_real_preparation_reuses_full_pool_at_semantic_call_limit():
    from backend.app.versions.v3.repair_budget import RepairBudget
    from backend.app.versions.v3.repair_candidates import prepare_candidates

    saved = snapshot()
    semantics = service()
    semantics.cache.update(saved.semantics.cache)
    semantics.calls = semantics.config.max_calls
    semantics.elapsed = semantics.config.total_seconds

    class NoProviderCalls:
        async def get_place_details(self, *_):
            pytest.fail("Stored Details must be reused")

        async def search_text(self, *_):
            pytest.fail("No discovery allowance in this fixture")

    budget = RepairBudget(123, clock=lambda: 0, runtime_config=saved.runtime)
    # Use only detailed choices: pending Details are covered separately by replay.
    result = asyncio.run(
        prepare_candidates(
            saved.context,
            saved.scope,
            budget,
            original=saved.original,
            pool=saved.enriched,
            semantic_service=semantics,
            provider=NoProviderCalls(),
        )
    )
    assert any(a.place_id == "z" for a in result.authorizations)
    assert budget.used["qualified_reuse"] == 1
    assert semantics.calls == semantics.config.max_calls
    assert semantics.elapsed == semantics.config.total_seconds


def test_capture_redaction_cap_and_no_second_attempt(tmp_path):
    from types import SimpleNamespace

    from tools.validation.repair_replay import CapturedRepair

    wrapped = CapturedRepair(
        SimpleNamespace(_capture_secrets=("sensitive-fixture",)), tmp_path, {}, []
    )
    # Exercise the same bounded writer used for snapshots, including immutable output.
    path = wrapped.capture.record("case", "snapshot", {"value": "sensitive-fixture"}, max_bytes=300)
    assert "sensitive-fixture" not in path.read_text()
    assert "[REDACTED]" in path.read_text()
    with pytest.raises(OverflowError):
        wrapped.capture.record("case", "snapshot", {"value": "x" * 400}, max_bytes=300)
    assert len(list(tmp_path.glob("*.json"))) == 1
    wrapped.capture_repair_snapshot()  # Invalid payload is an explicit capture failure.
    wrapped.capture_repair_snapshot()
    assert wrapped.errors[-1] == "repair_capture_duplicate_stage"
    assert len(list(tmp_path.glob("*.json"))) == 1


def test_replay_never_opens_network(monkeypatch):
    import socket

    from tools.validation.repair_replay import replay

    saved = snapshot()

    def denied(*args, **kwargs):
        pytest.fail("Offline replay attempted network access")

    async def guarded():
        # Windows creates an internal socketpair when constructing the event loop.
        with monkeypatch.context() as guard:
            guard.setattr(socket.socket, "connect", denied)
            guard.setattr(socket.socket, "connect_ex", denied)
            return await replay(saved)

    result = asyncio.run(guarded())
    assert result["preparation"]
