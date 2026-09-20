"""Bounded review enrichment and review-aware service-level selection."""

import hashlib
import json
from collections.abc import Sequence

from backend.app.evidence.experience_models import (
    ExperienceProfile,
    ExperienceProfileDraft,
    ReviewEvidence,
    unavailable_profile,
)
from backend.app.integrations.google.places import PLACES_REVIEWS_FIELD_MASK
from backend.app.integrations.models import PlaceReviewsDTO, PlaceReviewsRequest
from backend.app.integrations.protocols import PlacesProvider
from backend.app.llm.client import StructuredLLMClient
from backend.app.observability.run_trace import RunTracer, TracePayloadMode
from backend.app.policies.experience_profile import preprocess_reviews, validate_profile_draft
from backend.app.runtime.budget import ToolBudget, ToolBudgetExceededError, ToolBudgetKey
from backend.app.runtime.cache import RequestCache

PROFILE_PROMPT_VERSION = "v1a_review_profile_1"
_PROFILE_SYSTEM_PROMPT = """Interpret only supplied Places reviews as qualitative visitor evidence.
Return one structured profile for the supplied Place ID. Use no world knowledge or other evidence.
Allowed signals and values, at most one value per dimension:
- crowding: LOW, MODERATE, HIGH
- walking_intensity: LIGHT, MODERATE, HIGH (walking within the POI, not travel to it)
- accessibility: ACCESSIBLE, MIXED, LIMITED (visitor impressions, not certification)
- family_friendliness: FAMILY_FRIENDLY, MIXED, NOT_FAMILY_FRIENDLY
- visit_duration: SHORT, MEDIUM, LONG. SHORT means at most about 90 minutes or a clear quick stop;
  MEDIUM means over 90 minutes but under 3 hours; LONG means 3+ hours or a half/full-day visit.
Omit any dimension that reviews do not directly support, including vague or contradictory duration.
Every signal must cite one or more supplied review IDs. A concise summary, if present, must be
review-derived and cite supplied review IDs. Do not infer official operating facts, business status,
opening dates, route feasibility, weather, a POI selection score, or a recommendation.
review_count_used must equal the supplied usable review count. Do not fabricate evidence."""


class ReviewSelectionService:
    """Use one run's provider, budget, and cache without graph integration."""

    def __init__(
        self,
        *,
        places_provider: PlacesProvider,
        llm_client: StructuredLLMClient,
        llm_config_identity: str,
        budget: ToolBudget,
        cache: RequestCache,
        tracer: RunTracer,
    ) -> None:
        if not llm_config_identity:
            raise ValueError("A non-empty LLM configuration identity is required for Profile cache")
        self._places = places_provider
        self._llm = llm_client
        self._llm_identity = llm_config_identity
        self._budget = budget
        self._cache = cache
        self._tracer = tracer

    async def _reviews(self, place_id: str) -> tuple[PlaceReviewsDTO | None, str | None]:
        request = PlaceReviewsRequest(place_id=place_id, field_mask=PLACES_REVIEWS_FIELD_MASK)
        key = ("place_reviews", request.place_id, request.field_mask, request.language_code)

        async def load() -> tuple[PlaceReviewsDTO | None, str | None]:
            self._budget.consume(ToolBudgetKey.REVIEW_DETAIL_CALLS)
            try:
                return await self._places.get_place_reviews(request), None
            except Exception as exc:
                return None, type(exc).__name__

        result, cache_hit = await self._cache.get_or_create(key, load)
        self._tracer.event(
            "v1_review_provider_completed",
            {"place_id": place_id, "cache_hit": cache_hit, "error_type": result[1]},
        )
        return result

    async def _profile(
        self,
        place_id: str,
        reviews: Sequence[ReviewEvidence],
        retrieved_at: str,
    ) -> ExperienceProfile:
        evidence_hash = hashlib.sha256(
            json.dumps(
                [(item.review_id, item.text) for item in reviews],
                ensure_ascii=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        key = (
            "v1_experience_profile",
            place_id,
            evidence_hash,
            retrieved_at,
            PROFILE_PROMPT_VERSION,
            self._llm_identity,
        )

        async def load() -> ExperienceProfile:
            self._budget.consume(ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS)
            user_prompt = json.dumps(
                {
                    "place_id": place_id,
                    "reviews": [
                        {"review_id": item.review_id, "text": item.text} for item in reviews
                    ],
                },
                ensure_ascii=True,
            )
            self._tracer.event(
                "v1_experience_profile_llm_started",
                {"place_id": place_id, "review_count": len(reviews)},
            )
            self._tracer.payload(
                "llm",
                "v1_experience_profile_request",
                {
                    "system_prompt": _PROFILE_SYSTEM_PROMPT,
                    "place_id": place_id,
                    "review_ids": [item.review_id for item in reviews],
                    "review_count": len(reviews),
                    "review_evidence_sha256": evidence_hash,
                    "prompt_version": PROFILE_PROMPT_VERSION,
                },
                minimum_mode=TracePayloadMode.RAW,
            )
            try:
                draft = await self._llm.generate_structured(
                    system_prompt=_PROFILE_SYSTEM_PROMPT,
                    user_prompt=user_prompt,
                    response_schema=ExperienceProfileDraft,
                )
                self._tracer.payload(
                    "llm",
                    "v1_experience_profile_response",
                    draft,
                    minimum_mode=TracePayloadMode.RAW,
                )
                return validate_profile_draft(
                    draft,
                    place_id=place_id,
                    reviews=reviews,
                    retrieved_at=retrieved_at,
                )
            except Exception as exc:
                self._tracer.event(
                    "v1_experience_profile_llm_failed",
                    {"place_id": place_id, "error_type": type(exc).__name__},
                )
                return unavailable_profile(
                    place_id,
                    f"profile_invalid_or_unavailable:{type(exc).__name__}",
                    review_count_used=len(reviews),
                    retrieved_at=retrieved_at,
                )

        profile, cache_hit = await self._cache.get_or_create(key, load)
        self._tracer.event(
            "v1_experience_profile_completed",
            {
                "place_id": place_id,
                "cache_hit": cache_hit,
                "availability": profile.availability.value,
                "signal_count": len(profile.signals),
                "review_count_used": profile.review_count_used,
                "unavailable_reason": profile.unavailable_reason,
            },
        )
        self._tracer.payload(
            "evidence",
            "v1_experience_profile",
            profile,
            minimum_mode=TracePayloadMode.NORMALIZED,
        )
        return profile

    async def acquire_profile(self, place_id: str) -> ExperienceProfile:
        """Acquire one cached, budgeted Profile from registered review evidence."""

        async def load() -> ExperienceProfile:
            try:
                self._budget.consume(ToolBudgetKey.REVIEW_ENRICHED_PLACES)
                response, error = await self._reviews(place_id)
                if response is None:
                    return unavailable_profile(place_id, f"review_provider_unavailable:{error}")
                reviews = preprocess_reviews(response, place_id=place_id)
                if not reviews:
                    return unavailable_profile(place_id, "no_usable_reviews")
                return await self._profile(place_id, reviews, response.retrieved_at)
            except (ToolBudgetExceededError, ValueError) as exc:
                return unavailable_profile(place_id, f"profile_unavailable:{type(exc).__name__}")

        profile, _ = await self._cache.get_or_create(
            ("linked_experience_profile", place_id, self._llm_identity), load
        )
        return profile
