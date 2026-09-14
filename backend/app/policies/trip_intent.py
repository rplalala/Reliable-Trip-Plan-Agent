"""Mechanical provenance checks for user-semantic structured extraction."""

import re
import unicodedata

from backend.app.schemas.trip_intent import TripIntentExtractionResult


class TripIntentContractError(ValueError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Trip intent extraction contract failed: {code}")


def _normalized(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _source_in_request(value: str, request_text: str) -> bool:
    return bool(value.strip()) and value in request_text


def validate_trip_intents(
    extraction: TripIntentExtractionResult, request_text: str
) -> TripIntentExtractionResult:
    """Check copied spans and exact surfaces without reclassifying meaning."""

    named_surfaces = {_normalized(item.place_text) for item in extraction.named_place_intents}
    for item in extraction.requested_place_information:
        if not _source_in_request(item.source_text, request_text) or not _source_in_request(
            item.target_source_text, request_text
        ):
            raise TripIntentContractError("information_source_not_in_request")
        target = _normalized(item.target_surface)
        source = _normalized(item.target_source_text)
        if (
            target not in named_surfaces
            or re.search(rf"(?<!\w){re.escape(target)}(?!\w)", source) is None
        ):
            raise TripIntentContractError("information_target_not_named_and_supported")
        if item.scope_text is not None and not _source_in_request(
            item.scope_text, item.source_text
        ):
            raise TripIntentContractError("information_scope_not_in_source")
        if item.date_source_text is not None and not _source_in_request(
            item.date_source_text, item.source_text
        ):
            raise TripIntentContractError("information_date_not_in_source")
        if item.requested_start_date is not None and (
            extraction.requirements.start_date is None
            or extraction.requirements.end_date is None
            or item.requested_start_date < extraction.requirements.start_date
            or item.requested_end_date > extraction.requirements.end_date
        ):
            raise TripIntentContractError("information_date_outside_trip")
    for item in extraction.experience_preferences:
        if not _source_in_request(item.source_text, request_text):
            raise TripIntentContractError("experience_source_not_in_request")
    if extraction.transport_preference is not None and not _source_in_request(
        extraction.transport_preference.source_text, request_text
    ):
        raise TripIntentContractError("transport_source_not_in_request")
    for item in extraction.poi_interests:
        if not _source_in_request(item.source_text, request_text):
            raise TripIntentContractError("poi_source_not_in_request")
        surface = _normalized(item.surface)
        source = _normalized(item.source_text)
        if re.search(rf"(?<!\w){re.escape(surface)}(?!\w)", source) is None:
            raise TripIntentContractError("poi_surface_not_in_source")
    return extraction
