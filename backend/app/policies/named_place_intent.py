"""Mechanical provenance checks for extracted named-place intents."""

import re
import unicodedata
from collections.abc import Sequence

from backend.app.policies.poi_funnel import is_generic_category_surface
from backend.app.schemas.named_place_intent import NamedPlaceIntent

_ACTION_WRAPPER = re.compile(r"^(?:visit|go to|see)\s+", re.IGNORECASE)


class NamedPlaceIntentContractError(ValueError):
    """Reject unsupported, generic, or contradictory extracted place intents."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"Named-place intent extraction contract failed: {code}")


def normalize_place_surface(value: str) -> str:
    """Normalize only Unicode, case, and spacing, never aliases or semantics."""

    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def validate_named_place_intents(
    intents: Sequence[NamedPlaceIntent], request_text: str
) -> tuple[NamedPlaceIntent, ...]:
    """Verify copied spans and merge equal intents without hiding contradictions."""

    groups: dict[str, list[NamedPlaceIntent]] = {}
    for intent in intents:
        if intent.additional_source_texts:
            raise NamedPlaceIntentContractError("unexpected_derived_source_spans")
        if intent.source_text not in request_text:
            raise NamedPlaceIntentContractError("source_not_in_request")
        surface = normalize_place_surface(intent.place_text)
        source = normalize_place_surface(intent.source_text)
        if not re.search(rf"(?<!\w){re.escape(surface)}(?!\w)", source):
            raise NamedPlaceIntentContractError("place_not_in_source")
        if is_generic_category_surface(surface):
            raise NamedPlaceIntentContractError("generic_category_as_named_place")
        if _ACTION_WRAPPER.match(surface):
            raise NamedPlaceIntentContractError("action_wrapper_in_place_text")
        groups.setdefault(surface, []).append(intent)

    merged: list[tuple[int, str, NamedPlaceIntent]] = []
    for surface, group in groups.items():
        if len({item.inclusion for item in group}) != 1:
            raise NamedPlaceIntentContractError("conflicting_inclusion")
        ordered = sorted(
            group,
            key=lambda item: (request_text.index(item.source_text), item.source_text),
        )
        sources = tuple(dict.fromkeys(item.source_text for item in ordered))
        first = ordered[0]
        merged.append(
            (
                request_text.index(sources[0]),
                surface,
                first.model_copy(
                    update={"source_text": sources[0], "additional_source_texts": sources[1:]}
                ),
            )
        )
    return tuple(item for _, _, item in sorted(merged, key=lambda row: (row[0], row[1])))
