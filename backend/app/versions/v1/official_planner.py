"""Bounded, accepted-only official evidence supplied to itinerary generation."""

from backend.app.evidence.effective_models import EvidenceRelation
from backend.app.services.official_web_integration import OfficialWebIntegrationResult


def build_official_planner_evidence(
    result: OfficialWebIntegrationResult,
) -> list[dict[str, object]]:
    """Expose resolved claims and uncertainty, never raw acquisition or rejected claims."""

    if len(result.projection.places) != len(result.effective_places):
        raise ValueError("Effective official evidence must align with final selected POIs")
    gap_by_task = {item.task_id: item for item in result.gap_outcomes}
    acquisition_by_task = {item.task.task_id: item for item in result.acquisition_outcomes}
    facets_by_task = dict(result.facet_statuses_by_task)
    output: list[dict[str, object]] = []
    for place, effective in zip(result.projection.places, result.effective_places, strict=True):
        if place.place_id != effective.place_id:
            raise ValueError("Effective official evidence Place IDs must align")
        accepted_refs = {
            item.source_ref for item in result.accepted_evidence if item.place_id == place.place_id
        }
        place_tasks = [task for task in result.tasks if task.place_id == place.place_id]
        tasks: list[dict[str, object]] = []
        for task in place_tasks:
            acquisition = acquisition_by_task[task.task_id]
            gap = gap_by_task[task.task_id]
            tasks.append(
                {
                    "information_need": task.information_need.value,
                    "requested_facets": [item.value for item in task.requested_facets],
                    "requested_subject_scope": task.requested_subject_scope.value,
                    "requested_scope_text": task.requested_scope_text,
                    "applicable_start_date": task.applicable_start_date.isoformat(),
                    "applicable_end_date": task.applicable_end_date.isoformat(),
                    "acquisition_status": acquisition.status.value,
                    "evidence_status": gap.status.value,
                    "reason_codes": list(gap.reason_codes),
                    "facet_statuses": [
                        item.model_dump(mode="json")
                        for item in facets_by_task.get(task.task_id, ())
                    ],
                }
            )
        facts = [
            fact.model_dump(mode="json")
            for fact in effective.facts
            if any(ref in accepted_refs for ref in fact.source_refs)
            and fact.relation
            not in {
                EvidenceRelation.CONFLICT,
                EvidenceRelation.DUPLICATE,
                EvidenceRelation.UNRESOLVED,
            }
        ]
        output.append(
            {
                "place_id": place.place_id,
                "operational_days": [
                    day.model_dump(mode="json") for day in effective.operational_days
                ],
                "accepted_effective_facts": facts,
                "need_statuses": [item.model_dump(mode="json") for item in effective.need_statuses],
                "unresolved_conflict_source_refs": list(effective.conflict_source_refs),
                "tasks": tasks,
            }
        )
    return output
