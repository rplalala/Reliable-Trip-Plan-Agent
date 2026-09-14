"""Join bounded official-Web outcomes to the final selected V1 POIs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from backend.app.evidence.effective_models import EffectiveFacetStatus, EffectivePlaceEvidence
from backend.app.evidence.official_models import OfficialCurrentEvidence, OfficialGapOutcome
from backend.app.evidence.web_models import InformationGap, WebEvidenceTask, WebTaskOutcome
from backend.app.observability.run_trace import RunTracer
from backend.app.policies.official_evidence_resolver import resolve_effective_evidence
from backend.app.runtime.budget import ToolBudget, ToolBudgetKey
from backend.app.schemas.request import TravelRequest, TravelRequirements
from backend.app.schemas.trip_intent import RequestedPlaceInformation
from backend.app.services.official_web_grounding import OfficialWebGroundingService
from backend.app.services.web_evidence_acquisition import WebEvidenceAcquisitionService

if TYPE_CHECKING:
    from backend.app.versions.v1.official_web import OfficialWebProjection


@dataclass(frozen=True)
class OfficialWebIntegrationResult:
    projection: OfficialWebProjection
    tasks: tuple[WebEvidenceTask, ...]
    information_gaps: tuple[InformationGap, ...]
    acquisition_outcomes: tuple[WebTaskOutcome, ...]
    gap_outcomes: tuple[OfficialGapOutcome, ...]
    accepted_evidence: tuple[OfficialCurrentEvidence, ...]
    effective_places: tuple[EffectivePlaceEvidence, ...]
    facet_statuses_by_task: tuple[tuple[str, tuple[EffectiveFacetStatus, ...]], ...]


class OfficialWebIntegrationService:
    """Sequence accepted Phase 1/2 services without changing their policies."""

    def __init__(
        self,
        *,
        acquisition: WebEvidenceAcquisitionService,
        grounding: OfficialWebGroundingService,
        budget: ToolBudget,
        tracer: RunTracer,
    ) -> None:
        self._acquisition = acquisition
        self._grounding = grounding
        self._budget = budget
        self._tracer = tracer

    async def run(
        self,
        *,
        request: TravelRequest | None = None,
        requirements: TravelRequirements,
        projection: OfficialWebProjection,
        requested_information: tuple[RequestedPlaceInformation, ...] | None = None,
    ) -> OfficialWebIntegrationResult:
        if requirements.start_date is None or requirements.end_date is None:
            raise ValueError("Complete trip dates are required for official-Web integration")
        self._tracer.event(
            "official_web_projection_completed",
            {
                "selected_place_ids": [item.place_id for item in projection.candidates],
                "named_place_ids": sorted(projection.named_place_ids),
                "must_visit_place_ids": sorted(projection.must_visit_place_ids),
                "opening_date_conflict_place_ids": sorted(projection.opening_date_conflicts),
            },
        )
        before = self._budget.summary()
        tasks, gaps = self._acquisition.plan_tasks(
            request,
            requirements,
            projection.candidates,
            projection.places,
            named_place_ids=projection.named_place_ids,
            must_visit_place_ids=projection.must_visit_place_ids,
            opening_date_conflicts=projection.opening_date_conflicts,
            requested_information=requested_information,
            named_surface_place_ids=projection.named_surface_place_ids,
        )
        acquired = await self._acquisition.acquire(tasks)
        places_by_id = {place.place_id: place for place in projection.places}
        grounded = [
            await self._grounding.ground(outcome, places_by_id[outcome.task.place_id])
            for outcome in acquired
        ]
        accepted_by_place: dict[str, list[OfficialCurrentEvidence]] = {
            place.place_id: [] for place in projection.places
        }
        for outcome in grounded:
            accepted_by_place[outcome.place_id].extend(outcome.accepted_evidence)

        effective_places: list[EffectivePlaceEvidence] = []
        facet_statuses_by_task: list[tuple[str, tuple[EffectiveFacetStatus, ...]]] = []
        for place in projection.places:
            official = tuple(
                {item.source_ref: item for item in accepted_by_place[place.place_id]}.values()
            )
            place_tasks = [item for item in tasks if item.place_id == place.place_id]
            needs = tuple(dict.fromkeys(item.information_need for item in place_tasks))
            effective = resolve_effective_evidence(
                place,
                official,
                trip_start=requirements.start_date,
                trip_end=requirements.end_date,
                needs=needs,
            )
            effective_places.append(effective)
            for task in place_tasks:
                if not task.requested_facets:
                    continue
                facet_view = resolve_effective_evidence(
                    place,
                    official,
                    trip_start=requirements.start_date,
                    trip_end=requirements.end_date,
                    needs=(task.information_need,),
                    requested_facets=task.requested_facets,
                    requested_subject_scope=task.requested_subject_scope,
                    requested_scope_text=task.requested_scope_text,
                )
                facet_statuses_by_task.append((task.task_id, facet_view.facet_statuses))
            self._tracer.event(
                "official_effective_place_resolved",
                {
                    "place_id": place.place_id,
                    "accepted_count": len(official),
                    "fact_count": len(effective.facts),
                    "need_statuses": [
                        {"need": item.information_need.value, "status": item.status.value}
                        for item in effective.need_statuses
                    ],
                    "conflict_source_refs": list(effective.conflict_source_refs),
                    "operational_days": [
                        {"date": item.date, "status": item.status.value}
                        for item in effective.operational_days
                    ],
                },
            )
        accepted = tuple(
            item
            for place in projection.places
            for item in {
                fact.source_ref: fact for fact in accepted_by_place[place.place_id]
            }.values()
        )
        after = self._budget.summary()
        self._tracer.event(
            "official_web_integration_completed",
            {
                "task_count": len(tasks),
                "gap_count": len(gaps),
                "acquisition_statuses": [item.status.value for item in acquired],
                "gap_statuses": [item.status.value for item in grounded],
                "accepted_count": len(accepted),
                "web_budget_before": before[ToolBudgetKey.WEB_EVIDENCE_TASKS.value],
                "web_budget_after": after[ToolBudgetKey.WEB_EVIDENCE_TASKS.value],
                "page_budget_before": before[ToolBudgetKey.PAGE_FETCHES.value],
                "page_budget_after": after[ToolBudgetKey.PAGE_FETCHES.value],
            },
        )
        return OfficialWebIntegrationResult(
            projection=projection,
            tasks=tuple(tasks),
            information_gaps=tuple(gaps),
            acquisition_outcomes=tuple(acquired),
            gap_outcomes=tuple(grounded),
            accepted_evidence=accepted,
            effective_places=tuple(effective_places),
            facet_statuses_by_task=tuple(facet_statuses_by_task),
        )
