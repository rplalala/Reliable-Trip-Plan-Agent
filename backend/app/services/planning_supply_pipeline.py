"""Active V1 acquisition adapter for deterministic planning candidate supply."""

from dataclasses import dataclass, replace

from backend.app.policies.planning_supply import (
    PlanningSupplyResult,
    SupplyCandidate,
    select_planning_supply,
)
from backend.app.policies.poi_capacity import apply_poi_operating_budgets, derive_poi_capacities
from backend.app.policies.poi_selection import POISelectionResult
from backend.app.schemas.interpreted_requirements import ClarificationRequired
from backend.app.services.candidate_acquisition import CandidateAcquisition, selection_record


@dataclass(frozen=True)
class PlanningSupplySelection:
    final_selection: POISelectionResult
    policy_result: PlanningSupplyResult
    profiles: tuple

    evaluator_calls = 0
    subset_enumerator_calls = 0

    @property
    def selected_place_ids(self):
        return self.policy_result.selected_place_ids


class PlanningCandidateSupplyPipeline:
    """Reuse bounded acquisition; never construct or call the historical evaluator."""

    completion_event = "planning_supply_completed"

    def __init__(self, acquisition, llm, tracer, llm_identity):
        self.acquisition = acquisition
        self.tracer = tracer
        self.candidate_acquisition = CandidateAcquisition(acquisition, llm, tracer, llm_identity)

    async def run(self, contract, destination, window):
        return await self.candidate_acquisition.run(contract, destination, window, supply=self)

    def capacities(self, requirements, window):
        self._requirements, self._window = requirements, window
        if (
            getattr(self.acquisition, "runtime_config", None)
            and self.acquisition.runtime_config.acquisition.policy_id == "quality_first_1"
        ):
            from backend.app.policies.poi_capacity import quality_capacities

            return quality_capacities(requirements.start_date, requirements.end_date, window)
        return apply_poi_operating_budgets(
            derive_poi_capacities(requirements.start_date, requirements.end_date, window),
            self.acquisition._budget.limits,
        )

    def acquisition_order(self, places, required, associations, strengths, contract, destination):
        from backend.app.policies.acquisition_opportunities import opportunity_order

        return opportunity_order(places, required, contract, destination)

    def required_capacities(self, capacities, count):
        limits = self.acquisition._budget.limits
        config = getattr(self.acquisition, "runtime_config", None)
        if config and config.acquisition.policy_id == "quality_first_1":
            from backend.app.policies.poi_capacity import quality_capacities

            self._normal_supply_capacity = capacities.k_final
            values = quality_capacities(
                self._requirements.start_date, self._requirements.end_date, self._window, count
            )
            effective = limits.model_copy(
                update={
                    "max_candidates": values.c_raw,
                    "max_place_detail_calls": values.r_pool + 8,
                    "max_review_detail_calls": values.review_pool_cap,
                    "max_review_enriched_places": values.review_pool_cap,
                    "max_experience_profile_llm_calls": values.review_pool_cap,
                }
            )
            self.acquisition._budget.set_limits(effective)
            self.tracer.event(
                "effective_acquisition_policy",
                {
                    "policy_id": config.acquisition.policy_id,
                    "days": values.algorithmic.trip_days,
                    "required": count,
                    "normal_capacity": capacities.c_raw,
                    "normal_new_success_target": capacities.r_pool,
                    "normal_supply_target": capacities.k_final,
                    "normal_review_cap": capacities.review_pool_cap,
                    "capacity": values.c_raw,
                    "new_success_target": values.r_pool,
                    "send_cap": values.r_pool + 8,
                    "supply_target": values.k_final,
                    "review_cap": values.review_pool_cap,
                },
            )
            return values
        if count > min(limits.max_candidates, limits.max_place_detail_calls, limits.max_final_pois):
            raise ClarificationRequired("required_capacity_conflict")
        # Normal final capacity stays visible; only acquisition expands for required identities.
        return replace(
            capacities, c_raw=max(capacities.c_raw, count), r_pool=max(capacities.r_pool, count)
        )

    async def select(
        self,
        contract,
        assessments,
        rich,
        required,
        excluded,
        capacities,
        destination,
        profiles,
        optional,
        associations,
        strengths,
    ):
        candidates = tuple(
            SupplyCandidate(
                place_id=p.candidate.place_id,
                primary_type=p.structured_evidence.primary_type,
                rating=p.rating,
                latitude=p.structured_evidence.latitude,
                longitude=p.structured_evidence.longitude,
                intent_ids=p.discovery_intent_ids,
            )
            for p in rich
        )
        result = select_planning_supply(
            candidates,
            contract,
            required_ids=required,
            excluded_ids=excluded,
            capacity=getattr(self, "_normal_supply_capacity", capacities.k_final),
            hard_capacity=self.acquisition._budget.limits.max_final_pois,
            destination_coordinates=(destination.latitude, destination.longitude),
            profiles=profiles,
        )
        result = result.model_copy(
            update={"acquisition_diagnostics": getattr(self.acquisition, "details_report", {})}
        )
        final = selection_record(
            result.selected_place_ids,
            rich,
            required,
            contract.requirements.end_date,
            details=True,
        )
        return PlanningSupplySelection(final, result, tuple(profiles.values()))


def planner_supply_projection(selection, contract):
    """The planner sees options, explicit must-visits, and evidence uncertainty."""
    result = selection.policy_result
    return {
        "contract_version": "planning_supply_1",
        "required_canonical_ids": result.required_canonical_ids,
        "optional_canonical_ids": result.optional_canonical_ids,
        "planning_supply_count": len(result.selected_place_ids),
        "supply_shortfall": result.shortfall,
        "semantics": [
            r.model_dump(exclude={"source_refs"}) for r in contract.semantic_requirements
        ],
        "subjects": [
            {"subject_id": "party", "label": "Travel party"},
            *[s.model_dump(exclude={"source_refs"}) for s in contract.subjects],
        ],
        "review_evidence_relations": {
            pid: [r.model_dump() for r in result.profile_relations[pid]]
            for pid in result.selected_place_ids
        },
        "instructions": (
            "REQUIRED IDs are explicit user must-visits; preserve their canonical identities. "
            "OPTIONAL candidates are planning options: use a suitable subset, not every option. "
            "Attempt a coherent trip and preference alignment; soft trade-offs are allowed. "
            "UNKNOWN is neither failure nor satisfaction. Review relations are uncertain, "
            "review-supported judgments, not official facts or verified hard compliance. "
            "Do not assert unsupported local authenticity, quietness or family suitability. "
            "Supply size is not a mandatory visit count. An optional candidate may be scheduled "
            "or unused. Do not allocate references from this supply; the application handles "
            "nearby discovery after primary generation. "
            "Schedule feasibility is not validated."
        ),
    }
