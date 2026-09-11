"""Deterministic single-mode Route Matrix selection for V1 and later versions."""

import re
from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from backend.app.schemas.request import TravelRequest, TravelRequirements


class TravelMode(StrEnum):
    DRIVE = "DRIVE"
    WALK = "WALK"
    BICYCLE = "BICYCLE"
    TRANSIT = "TRANSIT"


class TransportModeDecision(BaseModel):
    """One reproducible mode decision and any valid Routes preference."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    travel_mode: TravelMode
    reason: str
    routing_preference: str | None = None


_EXPLICIT_PREFERENCE_VALUES = {
    "drive": TravelMode.DRIVE,
    "driving": TravelMode.DRIVE,
    "car": TravelMode.DRIVE,
    "rental car": TravelMode.DRIVE,
    "walk": TravelMode.WALK,
    "walking": TravelMode.WALK,
    "on foot": TravelMode.WALK,
    "bike": TravelMode.BICYCLE,
    "bicycle": TravelMode.BICYCLE,
    "cycling": TravelMode.BICYCLE,
    "public transport": TravelMode.TRANSIT,
    "public transit": TravelMode.TRANSIT,
    "transit": TravelMode.TRANSIT,
}

_REQUEST_PATTERNS = {
    TravelMode.DRIVE: (
        r"\bby car\b",
        r"\brent(?:al|ing)? (?:a )?car\b",
        r"\b(?:we (?:will|plan to)|prefer to) drive\b",
    ),
    TravelMode.WALK: (
        r"\bon foot\b",
        r"\bwalking[- ]only\b",
        r"\bwalk everywhere\b",
        r"\bget(?:ting)? around by walking\b",
    ),
    TravelMode.BICYCLE: (
        r"\bby (?:bike|bicycle)\b",
        r"\bcycling[- ]only\b",
        r"\brent(?:ing)? (?:a )?(?:bike|bicycle)\b",
    ),
    TravelMode.TRANSIT: (
        r"\b(?:use|using|prefer|travel by|get(?:ting)? around by) public "
        r"(?:transport|transit)\b",
        r"\bby (?:bus|train|transit)\b",
        r"\buse (?:buses|trains|transit)\b",
    ),
}


def select_transport_mode(
    request: TravelRequest,
    requirements: TravelRequirements,
) -> TransportModeDecision:
    """Select exactly one explicit mode or a documented pedestrian fallback."""

    normalized_request = request.request_text.casefold()
    matches: list[tuple[int, TravelMode]] = []
    for mode, patterns in _REQUEST_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, normalized_request)
            if match is not None:
                matches.append((match.start(), mode))
    if matches:
        _, mode = min(matches, key=lambda item: (item[0], item[1].value))
        return TransportModeDecision(
            travel_mode=mode,
            reason="explicit_mode_in_user_request",
            routing_preference="TRAFFIC_UNAWARE" if mode is TravelMode.DRIVE else None,
        )

    for preference in requirements.preferences:
        mode = _EXPLICIT_PREFERENCE_VALUES.get(preference.casefold().strip())
        if mode is not None:
            return TransportModeDecision(
                travel_mode=mode,
                reason="explicit_mode_in_extracted_preferences",
                routing_preference=(
                    "TRAFFIC_UNAWARE" if mode is TravelMode.DRIVE else None
                ),
            )

    return TransportModeDecision(
        travel_mode=TravelMode.WALK,
        reason="default_pedestrian_transfer_for_poi_grouping",
    )
