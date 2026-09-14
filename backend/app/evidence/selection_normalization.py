"""Convert Places DTOs into selection observations."""

from backend.app.evidence.normalization import (
    normalize_place_candidate,
    normalize_place_details,
)
from backend.app.evidence.selection_models import (
    PlaceOpeningDate,
    PlaceSelectionInput,
    QueryIntentHit,
    RatingAcquisitionState,
    SearchIntentKind,
)
from backend.app.integrations.models import PlaceCandidateDTO, PlaceDetailsDTO


def normalize_place_search_hit(
    dto: PlaceCandidateDTO,
    *,
    intent_id: str,
    source_query: str,
    actual_result_count: int,
    intent_kind: SearchIntentKind = SearchIntentKind.FALLBACK,
) -> PlaceSelectionInput:
    """Preserve one raw-response hit without merging or selecting candidates."""

    return PlaceSelectionInput(
        candidate=normalize_place_candidate(
            dto,
            source_query=source_query,
            category=intent_id,
        ),
        query_hits=[
            QueryIntentHit(
                intent_id=intent_id,
                source_query=source_query,
                provider_rank=dto.provider_rank,
                actual_result_count=actual_result_count,
                intent_kind=intent_kind,
            )
        ],
        search_opening_date=(
            PlaceOpeningDate.model_validate(dto.opening_date.model_dump())
            if dto.opening_date is not None
            else None
        ),
        search_opening_date_observations=(
            (PlaceOpeningDate.model_validate(dto.opening_date.model_dump()),)
            if dto.opening_date is not None
            else ()
        ),
    )


def normalize_place_details_for_selection(
    selection_input: PlaceSelectionInput,
    details: PlaceDetailsDTO,
) -> PlaceSelectionInput:
    """Retain rating and opening date without changing shared evidence semantics."""

    if details.place_id != selection_input.candidate.place_id:
        raise ValueError("Place Details ID does not match the selection candidate")
    return PlaceSelectionInput(
        candidate=selection_input.candidate,
        query_hits=selection_input.query_hits,
        search_opening_date=selection_input.search_opening_date,
        search_opening_date_observations=selection_input.search_opening_date_observations,
        details_opening_date=(
            PlaceOpeningDate.model_validate(details.opening_date.model_dump())
            if details.opening_date is not None
            else None
        ),
        opening_date_conflict=selection_input.opening_date_conflict,
        structured_evidence=normalize_place_details(details, candidate=selection_input.candidate),
        rating=details.rating,
        rating_state=(
            RatingAcquisitionState.AVAILABLE
            if details.rating is not None
            else RatingAcquisitionState.MISSING
        ),
        coordinate_state=selection_input.coordinate_state,
    )
