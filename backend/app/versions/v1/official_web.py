"""Project final V1-A POIs into the bounded official-Web input contract."""

from calendar import monthrange
from dataclasses import dataclass, field
from datetime import date

from backend.app.evidence.models import PlaceCandidate, PlaceEvidence
from backend.app.evidence.selection_models import PlaceOpeningDate
from backend.app.services.evidence_acquisition import CandidateFunnelResult
from backend.app.services.review_selection import ReviewAwareSelectionResult


@dataclass(frozen=True)
class OfficialWebProjection:
    candidates: list[PlaceCandidate]
    places: list[PlaceEvidence]
    named_place_ids: frozenset[str]
    must_visit_place_ids: frozenset[str]
    opening_date_conflicts: dict[str, tuple[date | None, ...]] = field(default_factory=dict)


def _latest_possible_opening(value: PlaceOpeningDate) -> date | None:
    """Keep partial Places dates conservative when checking trip relevance."""

    if value.year is None or (value.month is None and value.day is not None):
        return None
    month = value.month or 12
    day = value.day or monthrange(value.year, month)[1]
    try:
        return date(value.year, month, day)
    except ValueError:
        return None


def project_official_web_inputs(
    *,
    funnel: CandidateFunnelResult,
    selection: ReviewAwareSelectionResult,
    candidates: list[PlaceCandidate],
    places: list[PlaceEvidence],
) -> OfficialWebProjection:
    """Keep only selected structured Places facts and resolved named identities."""

    selected_ids = selection.selected_place_ids
    if not selected_ids or len(candidates) != len(places) or len(candidates) != len(selected_ids):
        raise ValueError("Final selected POIs and official-Web inputs must have equal lengths")
    candidate_ids = tuple(item.place_id for item in candidates)
    place_ids = tuple(item.place_id for item in places)
    if candidate_ids != selected_ids or place_ids != selected_ids:
        raise ValueError("Official-Web input Place IDs must match final selected order")
    if len(set(selected_ids)) != len(selected_ids):
        raise ValueError("Final selected POI Place IDs must be unique")
    named_ids = frozenset(
        item.resolved_place_id
        for item in funnel.named_place_resolutions
        if item.resolved_place_id in selected_ids
    )
    required_ids = funnel.must_visit_place_ids.intersection(selected_ids)
    if not required_ids <= named_ids:
        raise ValueError("Final must-visit IDs must be resolved named Places")
    eligibility_by_id = {item.place_id: item for item in selection.final_selection.eligibility}
    enriched_by_id = {item.candidate.place_id: item for item in funnel.enriched_candidates}
    if not set(selected_ids) <= eligibility_by_id.keys() & enriched_by_id.keys():
        raise ValueError("Final selected POIs must have structured date-risk inputs")
    opening_date_conflicts: dict[str, tuple[date | None, ...]] = {}
    for place_id in selected_ids:
        if not eligibility_by_id[place_id].opening_date_conflict:
            continue
        enriched = enriched_by_id[place_id]
        observations = (
            *enriched.search_opening_date_observations,
            enriched.details_opening_date,
        )
        opening_date_conflicts[place_id] = tuple(
            _latest_possible_opening(item) for item in observations if item is not None
        )
    return OfficialWebProjection(
        candidates=list(candidates),
        places=[item.model_copy(update={"rating": None}) for item in places],
        named_place_ids=named_ids,
        must_visit_place_ids=required_ids,
        opening_date_conflicts=opening_date_conflicts,
    )
