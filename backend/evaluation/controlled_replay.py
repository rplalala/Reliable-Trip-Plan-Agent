"""Offline execution of the actual V3 post-primary chain."""

import json
from copy import deepcopy
from types import SimpleNamespace

from ._controlled_ports import FrozenPorts, restore_cache, restore_semantics
from .controlled_models import ControlledCase
from .records import canonical_digest


class FrozenDiscovery:
    def __init__(self, saved):
        self.scope = saved.geographic_scope
        self.report = deepcopy(saved.original_rag)

    def finalize(self, state):
        return deepcopy(self.report)


class NullTrace:
    def event(self, *args):
        pass


async def replay_controlled_case(value):
    """Detach input state and derive real validator/scope/finalization outputs."""
    from backend.app.versions.v3.wiring import V3PostPrimary

    json.dumps(value, allow_nan=False)
    saved = ControlledCase.model_validate(deepcopy(value))
    ports = FrozenPorts(saved)
    acquisition = SimpleNamespace(
        runtime_config=saved.runtime,
        _cache=restore_cache(saved),
        _places=ports,
        _routes=ports,
        poi_semantics=restore_semantics(saved, ports),
    )
    funnel = SimpleNamespace(
        named_place_resolutions=saved.named_resolutions,
        enriched_candidates=saved.enriched,
        admitted_candidates=saved.admitted,
    )
    state = {
        "itinerary": saved.primary,
        "route_evidence": saved.routes,
        "official_web_result": SimpleNamespace(effective_places=saved.effective_places),
        "transport_mode": saved.transport,
        "review_selection": SimpleNamespace(
            semantic_assessments=saved.semantic_assessments,
            policy_result=SimpleNamespace(selected_place_ids=saved.supply_ids),
        ),
        "interpreted_requirements": saved.requirements,
        "reference_date": saved.reference_date,
        "place_evidence": saved.places,
        "candidate_funnel": funnel,
    }
    service = V3PostPrimary(
        ports,
        acquisition,
        NullTrace(),
        FrozenDiscovery(saved),
        ports,
        saved.request_remaining,
        saved.quantity_review,
        clock=ports.clock,
    )
    outcome = None
    fatal = None
    try:
        with ports.offline():
            result = await service(state)
        outcome = result["v3_outcome"].model_dump(mode="json")
    except Exception as exc:
        fatal = "execution_failed:" + type(exc).__name__
    report = {
        "schema_version": "rtpeval_controlled_replay_1",
        "case_id": saved.case_id,
        "revision": saved.revision,
        "case_hash": canonical_digest(saved.model_dump(mode="json")),
        "status": "execution_material_error"
        if ports.errors
        else "execution_failed"
        if fatal
        else "complete",
        "outcome": outcome,
        "calls": ports.calls,
        "logical_elapsed_seconds": ports.elapsed,
        "diagnostics": ports.errors + ([fatal] if fatal else []),
    }
    report["replay_hash"] = canonical_digest(report)
    return report
