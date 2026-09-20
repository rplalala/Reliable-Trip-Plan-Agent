"""Bound and validate review-only qualitative evidence for V1-A selection."""

import re
from collections.abc import Sequence

from backend.app.evidence.experience_models import (
    ExperienceConfidence,
    ExperienceProfile,
    ExperienceProfileDraft,
    ExperienceSignal,
    ReviewEvidence,
)
from backend.app.evidence.models import EvidenceAvailability
from backend.app.integrations.models import PlaceReviewsDTO

MAX_USABLE_REVIEWS = 5
MAX_REVIEW_TEXT_CHARS = 1200


def preprocess_reviews(response: PlaceReviewsDTO, *, place_id: str) -> tuple[ReviewEvidence, ...]:
    """Preserve provider order, removing empty and duplicate review texts."""

    if response.place_id != place_id:
        raise ValueError("Review response Place ID does not match the requested Place ID")
    result: list[ReviewEvidence] = []
    seen: set[str] = set()
    for item in response.reviews:
        if item.text is None:
            continue
        cleaned = re.sub(r"\s+", " ", item.text).strip()
        bounded = cleaned[:MAX_REVIEW_TEXT_CHARS]
        if not bounded or bounded.casefold() in seen:
            continue
        seen.add(bounded.casefold())
        result.append(
            ReviewEvidence(
                review_id=f"review_{len(result) + 1}",
                place_id=place_id,
                text=bounded,
                resource_name=item.resource_name,
                google_maps_uri=item.google_maps_uri,
                publish_time=item.publish_time,
            )
        )
        if len(result) == MAX_USABLE_REVIEWS:
            break
    return tuple(result)


def validate_profile_draft(
    draft: ExperienceProfileDraft,
    *,
    place_id: str,
    reviews: Sequence[ReviewEvidence],
    retrieved_at: str,
) -> ExperienceProfile:
    """Reject unsupported refs and derive confidence solely from cited reviews."""

    if draft.place_id != place_id:
        raise ValueError("Profile Place ID does not match the requested Place ID")
    if draft.review_count_used != len(reviews):
        raise ValueError("Profile review_count_used differs from bounded input")
    valid_ids = {review.review_id for review in reviews}

    def refs(values: Sequence[str]) -> tuple[str, ...]:
        if not set(values) <= valid_ids:
            raise ValueError("Profile references a review outside the bounded input")
        return tuple(dict.fromkeys(values))

    summary_refs = refs(draft.summary_review_refs)
    signals: list[ExperienceSignal] = []
    for item in draft.signals:
        signal_refs = refs(item.review_refs)
        if not signal_refs:
            continue
        signals.append(
            ExperienceSignal(
                dimension=item.dimension,
                value=item.value,
                review_refs=signal_refs,
                confidence=(
                    ExperienceConfidence.LOW
                    if len(signal_refs) == 1
                    else ExperienceConfidence.MEDIUM
                ),
            )
        )
    if draft.summary is not None and not summary_refs:
        raise ValueError("Profile summary has no valid supporting review")
    availability = (
        EvidenceAvailability.AVAILABLE
        if draft.summary is not None and signals
        else EvidenceAvailability.PARTIAL
        if draft.summary is not None or signals
        else EvidenceAvailability.UNAVAILABLE
    )
    return ExperienceProfile(
        place_id=place_id,
        availability=availability,
        summary=draft.summary,
        summary_truncated=draft.summary_truncated,
        summary_review_refs=summary_refs,
        signals=tuple(signals),
        review_count_used=len(reviews),
        retrieved_at=retrieved_at,
        unavailable_reason="no_supported_review_evidence"
        if availability is EvidenceAvailability.UNAVAILABLE
        else None,
    )
