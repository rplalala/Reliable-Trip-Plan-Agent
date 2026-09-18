"""Versioned conservative discovery policy; no Google validation or identity repair."""

import hashlib
import unicodedata

from backend.app.tripworld.retrieval.entities import RetrievalEntity
from backend.app.tripworld.retrieval.geography import valid_coordinates

POLICY_VERSION = "tripworld-production-policy-v1"


def exclusion_reasons(entity: RetrievalEntity) -> list[str]:
    reasons = []
    if entity.eligibility_hint == "ineligible":
        reasons.append("ineligible")
    if not entity.retrieval_text.strip():
        reasons.append("empty_text")
    if not valid_coordinates(entity.latitude, entity.longitude):
        reasons.append("invalid_coordinates")
    if "country_conflict" in entity.location_flags:
        reasons.append("country_conflict")
    if entity.coordinate_spread_km > 10:
        reasons.append("coordinate_spread_over_10km")
    return reasons


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalized_name(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())
