"""Bounded review enrichment and review-aware service-level selection."""

import hashlib
import json
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Literal

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
from backend.app.policies.experience_selection import (
    ExperienceNeedExtraction,
    ExperienceScoreResult,
    experience_needs_from_intents,
    experience_score_map,
    extract_experience_needs,
    score_experience,
)
from backend.app.policies.poi_selection import POISelectionResult
from backend.app.policies.review_sensitivity import (
    ReviewSelectionContext,
    find_review_sensitive_candidates,
    select_with_experience,
)
from backend.app.policies.trip_dates import TripDateWindow
from backend.app.runtime.budget import ToolBudget, ToolBudgetExceededError, ToolBudgetKey
from backend.app.runtime.cache import RequestCache
from backend.app.schemas.request import TravelRequirements
from backend.app.schemas.trip_intent import ExperiencePreferenceIntent
from backend.app.services.evidence_acquisition import CandidateFunnelResult

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


@dataclass(frozen=True)
class ReviewAttempt:
    place_id: str
    status: str
    review_count: int
    profile_availability: str
    minimum_flip_magnitude: Decimal


@dataclass(frozen=True)
class ReviewAwareSelectionResult:
    """Phase-4 service result; deliberately not a planner or V1-B input."""

    final_selection: POISelectionResult
    profiles: tuple[ExperienceProfile, ...]
    attempts: tuple[ReviewAttempt, ...]
    experience_scores: tuple[tuple[str, ExperienceScoreResult], ...]
    need_extraction: ExperienceNeedExtraction
    stop_reason: Literal[
        "no_sensitive_candidates",
        "review_pool_cap_exhausted",
        "safety_budget_exhausted",
        "insufficient_review_evidence",
    ]

    @property
    def selected_place_ids(self) -> tuple[str, ...]:
        return self.final_selection.selected_place_ids


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

    async def run(
        self,
        *,
        funnel: CandidateFunnelResult,
        requirements: TravelRequirements,
        window: TripDateWindow,
        experience_preferences: Sequence[ExperiencePreferenceIntent] | None = None,
    ) -> ReviewAwareSelectionResult:
        if requirements.start_date is None or requirements.end_date is None:
            raise ValueError("Complete trip dates are required for review-aware selection")
        needs = (
            experience_needs_from_intents(experience_preferences)
            if experience_preferences is not None
            else extract_experience_needs(requirements)
        )
        context = ReviewSelectionContext(
            start_date=requirements.start_date,
            end_date=requirements.end_date,
            window=window,
            capacity=funnel.capacities.k_final,
            must_visit_place_ids=funnel.must_visit_place_ids,
            excluded_place_ids=funnel.excluded_place_ids,
            unresolved_required_names=funnel.unresolved_required_names,
        )
        profiles: dict[str, ExperienceProfile] = {}
        attempted: set[str] = set()
        attempts: list[ReviewAttempt] = []
        stop_reason: Literal[
            "no_sensitive_candidates",
            "review_pool_cap_exhausted",
            "safety_budget_exhausted",
            "insufficient_review_evidence",
        ] = "no_sensitive_candidates"
        while True:
            scores = experience_score_map(profiles, needs.needs)
            sensitive = find_review_sensitive_candidates(
                funnel.enriched_candidates,
                context=context,
                needs=needs.needs,
                current_scores=scores,
                attempted_ids=frozenset(attempted),
            )
            self._tracer.event(
                "v1_review_sensitivity_evaluated",
                {
                    "selected_place_ids": select_with_experience(
                        funnel.enriched_candidates, context, scores
                    ).selected_place_ids,
                    "sensitive_candidates": [
                        {
                            "place_id": item.place_id,
                            "minimum_flip_magnitude": str(item.minimum_flip_magnitude),
                        }
                        for item in sensitive
                    ],
                    "review_pool_used": len(attempted),
                    "review_pool_cap": funnel.capacities.review_pool_cap,
                },
            )
            if not sensitive:
                if attempts and all(item.status != "available" for item in attempts):
                    stop_reason = "insufficient_review_evidence"
                break
            if len(attempted) >= funnel.capacities.review_pool_cap:
                stop_reason = "review_pool_cap_exhausted"
                break
            candidate = sensitive[0]
            place_id = candidate.place_id
            try:
                self._budget.consume(ToolBudgetKey.REVIEW_ENRICHED_PLACES)
            except ToolBudgetExceededError:
                stop_reason = "safety_budget_exhausted"
                break
            attempted.add(place_id)
            self._tracer.event(
                "v1_review_attempt_started",
                {
                    "place_id": place_id,
                    "minimum_flip_magnitude": str(candidate.minimum_flip_magnitude),
                    "triggering_values": [str(value) for value in candidate.triggering_values],
                },
            )
            try:
                response, error = await self._reviews(place_id)
            except ToolBudgetExceededError:
                profiles[place_id] = unavailable_profile(place_id, "review_budget_exhausted")
                attempts.append(
                    ReviewAttempt(
                        place_id,
                        "budget_exhausted",
                        0,
                        "unavailable",
                        candidate.minimum_flip_magnitude,
                    )
                )
                self._tracer.event(
                    "v1_review_attempt_completed",
                    {"place_id": place_id, "status": "budget_exhausted", "review_count": 0},
                )
                stop_reason = "safety_budget_exhausted"
                break
            reviews: tuple[ReviewEvidence, ...] = ()
            if response is None:
                profile = unavailable_profile(place_id, f"review_provider_unavailable:{error}")
            else:
                try:
                    reviews = preprocess_reviews(response, place_id=place_id)
                except ValueError as exc:
                    profile = unavailable_profile(
                        place_id, f"review_response_invalid:{type(exc).__name__}"
                    )
                else:
                    if not reviews:
                        profile = unavailable_profile(place_id, "no_usable_reviews")
                    else:
                        try:
                            profile = await self._profile(place_id, reviews, response.retrieved_at)
                        except ToolBudgetExceededError:
                            profile = unavailable_profile(
                                place_id,
                                "profile_budget_exhausted",
                                review_count_used=len(reviews),
                                retrieved_at=response.retrieved_at,
                            )
                            stop_reason = "safety_budget_exhausted"
            profiles[place_id] = profile
            status = (
                "available"
                if profile.availability.value in {"available", "partial"}
                else "unavailable"
            )
            attempts.append(
                ReviewAttempt(
                    place_id=place_id,
                    status=status,
                    review_count=len(reviews),
                    profile_availability=profile.availability.value,
                    minimum_flip_magnitude=candidate.minimum_flip_magnitude,
                )
            )
            self._tracer.event(
                "v1_review_attempt_completed",
                {
                    "place_id": place_id,
                    "status": status,
                    "review_count": len(reviews),
                    "profile_availability": profile.availability.value,
                    "experience_score": str(score_experience(profile, needs.needs).total),
                    "budget": {
                        key.value: self._budget.summary()[key.value]
                        for key in (
                            ToolBudgetKey.REVIEW_ENRICHED_PLACES,
                            ToolBudgetKey.REVIEW_DETAIL_CALLS,
                            ToolBudgetKey.EXPERIENCE_PROFILE_LLM_CALLS,
                        )
                    },
                },
            )
            if stop_reason == "safety_budget_exhausted":
                break
        score_results = tuple(
            (place_id, score_experience(profile, needs.needs))
            for place_id, profile in profiles.items()
        )
        final_selection = select_with_experience(
            funnel.enriched_candidates,
            context,
            {place_id: score.total for place_id, score in score_results},
        )
        self._tracer.event(
            "v1_review_selection_completed",
            {
                "selected_place_ids": final_selection.selected_place_ids,
                "review_attempted_place_ids": tuple(item.place_id for item in attempts),
                "stop_reason": stop_reason,
                "ambiguities": needs.ambiguities,
            },
        )
        return ReviewAwareSelectionResult(
            final_selection=final_selection,
            profiles=tuple(profiles.values()),
            attempts=tuple(attempts),
            experience_scores=score_results,
            need_extraction=needs,
            stop_reason=stop_reason,
        )
