"""Offline semantic boundary and input sizing; no provider construction."""

import asyncio
import json

import pytest

from backend.app.runtime.config_loader import load_runtime_config
from backend.app.schemas.poi_semantics import SemanticAssessmentError, SemanticPreparationLimit
from backend.app.services.poi_semantics import (
    POISemanticsService,
    semantic_input_tokens,
    serialize_semantic_input,
)
from backend.tests.versions.v3.test_validation import contract, place


class Model:
    def __init__(self, mutate=None):
        self.calls = 0
        self.mutate = mutate

    async def generate_poi_semantics_structured(self, **kwargs):
        self.calls += 1
        data = json.loads(kwargs["user_prompt"])
        rows = [
            dict(
                place_id=p["place_id"],
                visit_object=p["name"],
                role="attraction",
                categories=["museum"],
                reason="Supplied museum evidence",
                evidence_refs=[p["source_ref"]],
                matches=[],
                exception_requirement_ids=[],
            )
            for p in data["places"]
        ]
        if self.mutate:
            self.mutate(rows)
        return {"assessments": rows}


def service(model=None, **config):
    runtime = load_runtime_config()
    return POISemanticsService(
        model or Model(),
        runtime.poi_semantics.model_copy(update=config),
        runtime.main_generation.framing_tokens,
    )


def test_batch_cache_and_total_calls():
    svc = service()
    places = [place(str(i)) for i in range(64)]

    async def run():
        await svc.assess(places, contract())
        await svc.assess(list(reversed(places)), contract())

    asyncio.run(run())
    assert svc.calls == 2
    assert len(svc.ledger) == 64


@pytest.mark.parametrize(
    "mutate",
    [
        lambda rows: rows.pop(),
        lambda rows: rows.append(rows[0]),
        lambda rows: rows[0].update(place_id="invented"),
        lambda rows: rows[0].update(evidence_refs=["invented"]),
        lambda rows: rows[0].update(role="exception_only", exception_requirement_ids=["invented"]),
    ],
)
def test_invalid_contract_is_terminal(mutate):
    svc = service(Model(mutate))
    with pytest.raises(SemanticAssessmentError):
        asyncio.run(svc.assess([place()], contract()))
    with pytest.raises(SemanticAssessmentError, match="already failed"):
        asyncio.run(svc.assess([place()], contract()))
    assert svc.calls == 1


def test_unknown_operations_do_not_disqualify_role():
    svc = service()
    rows = asyncio.run(svc.assess([place().model_copy(update={"opening_hours": None})], contract()))
    assert rows[place().place_id].main_eligible


def test_unknown_role_cannot_qualify():
    svc = service(Model(lambda rows: rows[0].update(role="unresolved")))
    assert not asyncio.run(svc.assess([place()], contract()))[place().place_id].main_eligible


@pytest.mark.parametrize("frequency", ["exact", "minimum"])
def test_explicit_category_count_has_supply_before_ordinary_diversification(frequency):
    from backend.app.policies.planning_supply import SupplyCandidate, select_planning_supply
    from backend.app.schemas.interpreted_requirements import DiscoveryIntent
    from backend.tests.versions.v3.test_b_targets import setup, visit
    from backend.tests.versions.v3.test_semantic_repair import category_goal

    _, ctx, _, _ = setup([[visit("a", "a")]], reviews=())
    ctx = category_goal(ctx, frequency=frequency, matched_ids=("a", "b"))
    current = ctx.contract.model_copy(
        update={
            "discovery_intents": (
                DiscoveryIntent(
                    intent_id="discovery_1",
                    requirement_refs=("semantic_1",),
                    purpose="activity_or_category",
                    query_text="zoos",
                ),
            )
        }
    )
    candidates = [
        SupplyCandidate(
            place_id=pid,
            primary_type=category,
            rating=None,
            latitude=0,
            longitude=0,
            intent_ids=("discovery_1",) if pid in {"a", "b"} else (),
        )
        for pid, category in [
            ("a", "zoo"),
            ("b", "zoo"),
            ("c", "art"),
            ("d", "history"),
            ("e", "park"),
        ]
    ]
    result = select_planning_supply(
        candidates,
        current,
        required_ids=(),
        excluded_ids=(),
        capacity=4,
        hard_capacity=4,
        destination_coordinates=(0, 0),
        semantic_assessments={r.place_id: r for r in ctx.semantic_assessments},
        semantic_config=load_runtime_config().poi_semantics,
    )
    assert {"a", "b"} <= set(result.selected_place_ids)
    assert len(result.selected_place_ids) == 4


def test_london_historical_search_lanes_retain_exploration_before_details():
    from math import ceil
    from pathlib import Path
    from types import SimpleNamespace

    from backend.app.policies.acquisition_opportunities import opportunity_order
    from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements

    saved = json.loads(
        (Path(__file__).parents[1] / "fixtures/poi_semantics_london.json").read_text()
    )
    rows = [
        SimpleNamespace(candidate=SimpleNamespace(**r), discovery_intent_ids=r["intent_ids"])
        for r in saved["candidates"]
    ]
    general = {
        r.candidate.place_id
        for r in rows
        if not set(r.discovery_intent_ids) & {"discovery_1", "discovery_2"}
    }
    order = opportunity_order(
        rows,
        set(),
        InterpretedTripRequirements.model_validate(saved["contract"]),
        SimpleNamespace(latitude=51.5072, longitude=-0.1276),
        exploration_fraction=load_runtime_config().poi_semantics.exploration_fraction,
    )
    assert len(set(order)) == len(rows)
    for capacity in (16, 32, 48):
        assert len(set(order[:capacity]) & general) >= min(len(general), ceil(capacity / 3))
    # The raw Google lane is not the later merged Google/RAG association ledger.
    assert set(saved["historical_selection_reasons"]) == {"discovery_opportunity"}


def test_overflow_is_presend_failure():
    svc = service(input_tokens=1)
    with pytest.raises(SemanticPreparationLimit, match="overflow"):
        asyncio.run(svc.assess([place()], contract()))
    assert svc.calls == 0


def test_call_budget_is_shared_across_batches():
    svc = service(max_calls=1, batch_size=1)
    with pytest.raises(SemanticPreparationLimit, match="budget"):
        asyncio.run(svc.assess([place(), place("b")], contract()))
    assert svc.calls == 1


@pytest.mark.parametrize("change", ["missing", "zero", "timeout"])
def test_semantic_config_cannot_silently_disable_service(change):
    from backend.app.runtime.config_models import RuntimeConfig

    data = load_runtime_config().model_dump()
    if change == "missing":
        data.pop("poi_semantics")
    elif change == "zero":
        data["poi_semantics"]["max_calls"] = 0
    else:
        data["poi_semantics"]["call_timeout_seconds"] = data["poi_semantics"]["total_seconds"] + 1
    with pytest.raises(ValueError):
        RuntimeConfig.model_validate(data)


def test_cancel_propagates():
    class Cancel:
        async def generate_poi_semantics_structured(self, **kwargs):
            raise asyncio.CancelledError()

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(service(Cancel()).assess([place()], contract()))


@pytest.mark.parametrize("count", [1, 16, 32])
def test_real_serializer_size(count):
    payload = serialize_semantic_input([place(str(i)) for i in range(count)], contract())
    size = semantic_input_tokens(payload, load_runtime_config().main_generation.framing_tokens)
    assert size < load_runtime_config().poi_semantics.input_tokens


@pytest.mark.parametrize("bound", ["a", "other", None])
def test_named_exception_requires_application_identity_binding(bound):
    def exception(rows):
        rows[0].update(
            role="exception_only",
            exception_requirement_ids=["named_1"],
            matches=[
                dict(requirement_id="named_1", relation="supported", evidence_refs=["places:a"])
            ],
        )

    svc = service(Model(exception))
    svc.named_bindings = {"named_1": bound} if bound else {}
    if bound == "a":
        assert asyncio.run(svc.assess([place()], contract("REQUIRED")))["a"].main_eligible
    else:
        with pytest.raises(SemanticAssessmentError):
            asyncio.run(svc.assess([place()], contract("REQUIRED")))


def test_details_continue_same_queue_after_semantic_rejection():
    from datetime import date

    from backend.app.services.candidate_details import acquire_candidate_details
    from backend.tests.services.test_quality_first import acquisition

    async def run():
        acq, rows, provider, requirements, _ = acquisition(32)
        rejected = {p.candidate.place_id for p in rows[:24]}

        def classify(items):
            for item in items:
                item["role"] = "non_main" if item["place_id"] in rejected else "attraction"

        svc = service(Model(classify))

        async def adequate(items, deadline):
            judgments = await svc.prepare(
                [p.structured_evidence for p in items], requirements, deadline=deadline
            )
            return sum(r.main_eligible for r in judgments.values()) >= 8

        rich, _, _ = await acquire_candidate_details(
            acq, rows, date(2026, 9, 23), 24, adequate=adequate
        )
        await svc.prepare([p.structured_evidence for p in rich], requirements)
        assert len(rich) == len(provider.ids) == len(set(provider.ids)) == 32
        assert svc.calls == 2
        assert sum(r.main_eligible for r in svc.ledger.values()) == 8
        assert not provider.searches

    asyncio.run(run())


def test_exploration_supply_uses_judgment_not_search_origin():
    from types import SimpleNamespace

    from backend.app.schemas.poi_semantics import POISemanticAssessment
    from backend.tests.policies.test_planning_supply import candidate, select
    from backend.tests.policies.test_planning_supply import contract as make_contract

    req = make_contract()
    ref = req.semantic_requirements[0].requirement_id
    req = req.model_copy(
        update={"discovery_intents": (SimpleNamespace(intent_id="zoo", requirement_refs=(ref,)),)}
    )
    candidates = [candidate(str(i), intents=("zoo",)) for i in range(12)]
    rows = {
        p.place_id: POISemanticAssessment(
            place_id=p.place_id,
            visit_object=p.place_id,
            role="attraction",
            categories=["museum"],
            reason="Synthetic assessment",
            evidence_refs=[f"places:{p.place_id}"],
            matches=[
                dict(
                    requirement_id=ref,
                    relation="supported" if int(p.place_id) < 8 else "mismatch",
                    evidence_refs=[f"places:{p.place_id}"],
                )
            ],
            exception_requirement_ids=[],
        )
        for p in candidates
    }
    result = select(
        candidates,
        req,
        semantic_assessments=rows,
        semantic_config=load_runtime_config().poi_semantics,
    )
    assert sum(int(pid) >= 8 for pid in result.selected_place_ids) >= 3


def test_exception_alternatives_share_allowance_and_incomplete_output():
    from backend.app.policies.poi_semantic_output import semantic_policy_issues
    from backend.app.schemas.interpreted_requirements import ExperienceGoal
    from backend.app.schemas.poi_semantics import POISemanticAssessment
    from backend.tests.policies.test_planning_supply import candidate, select
    from backend.tests.policies.test_planning_supply import contract as make_contract
    from backend.tests.versions.v3.test_validation import activity, draft

    req = make_contract()
    goal = ExperienceGoal(
        frequency="one_off",
        target="category",
        explicit_primary_exception=True,
        distinct_dates=False,
        trip_scope="ordinary",
        count=None,
    )
    ref = req.semantic_requirements[0].requirement_id
    req = req.model_copy(
        update={
            "semantic_requirements": (
                req.semantic_requirements[0].model_copy(update={"experience_goal": goal}),
            )
        }
    )
    rows = {
        str(i): POISemanticAssessment(
            place_id=str(i),
            visit_object="Meal",
            role="exception_only",
            categories=["dining"],
            reason="Explicit fixture request",
            evidence_refs=[f"places:{i}"],
            matches=[dict(requirement_id=ref, relation="supported", evidence_refs=[f"places:{i}"])],
            exception_requirement_ids=[ref],
        )
        for i in range(5)
    }
    result = select(
        [candidate(str(i)) for i in range(5)],
        req,
        semantic_assessments=rows,
        semantic_config=load_runtime_config().poi_semantics,
    )
    assert len(result.selected_place_ids) == 2
    itinerary = draft([activity("a", "0"), activity("b", "1", "12:00", "13:00")])
    assert any(
        r["reason"] == "primary_exception_allowance_exceeded"
        for r in semantic_policy_issues(itinerary, req, tuple(rows.values()))
    )
