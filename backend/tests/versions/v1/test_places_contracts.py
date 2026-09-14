"""V1-A-only Places contract and request-cache identity tests."""

import asyncio
from uuid import UUID

import pytest

from backend.app.evidence.models import DestinationContext, PlaceCandidate, PlaceEvidence
from backend.app.evidence.selection_models import (
    PlaceOpeningDate,
    PlaceSelectionInput,
    QueryIntentHit,
    RatingAcquisitionState,
)
from backend.app.evidence.selection_normalization import normalize_place_details_for_selection
from backend.app.integrations.google.places import (
    PLACES_CANDIDATE_FIELD_MASK,
    PLACES_DETAILS_FIELD_MASK,
    PLACES_REVIEWS_FIELD_MASK,
)
from backend.app.integrations.models import (
    LatLng,
    PlaceCandidateDTO,
    PlaceDetailsDTO,
    PlaceDetailsRequest,
    PlaceOpeningDateDTO,
    PlaceReviewsRequest,
    PlaceSearchRequest,
    PlaceSearchResponse,
)
from backend.app.observability.run_trace import NullRunTracer
from backend.app.runtime.budget import ToolBudget, ToolBudgetKey, ToolBudgetLimits
from backend.app.runtime.cache import RequestCache
from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    make_requirements,
)


def _service() -> tuple[V1EvidenceAcquisitionService, FakePlacesProvider, ToolBudget]:
    places = FakePlacesProvider()
    budget = ToolBudget(ToolBudgetLimits(max_candidate_search_calls=2))
    return (
        V1EvidenceAcquisitionService(
            places_provider=places,
            weather_provider=FakeWeatherProvider(),
            routes_provider=FakeRoutesProvider(),
            budget=budget,
            cache=RequestCache(),
            tracer=NullRunTracer(UUID("00000000-0000-0000-0000-000000000001")),
        ),
        places,
        budget,
    )


def test_current_graph_keeps_legacy_candidate_request_size_until_funnel_switch() -> None:
    destination = DestinationContext(
        place_id="sydney",
        name="Sydney",
        latitude=-33.8,
        longitude=151.2,
    )
    legacy_service, legacy_provider, _ = _service()
    asyncio.run(legacy_service.search_candidates(make_requirements(), destination))
    assert legacy_provider.search_requests
    assert {request.page_size for request in legacy_provider.search_requests} == {7}

    future_service, future_provider, _ = _service()
    asyncio.run(future_service.search_candidate_observations(make_requirements(), destination))
    assert {request.page_size for request in future_provider.search_requests} == {12}


def test_future_opening_parameter_changes_search_cache_identity() -> None:
    service, places, budget = _service()
    base = {
        "text_query": "museums in Sydney",
        "page_size": 3,
        "field_mask": PLACES_CANDIDATE_FIELD_MASK,
        "location_bias": LatLng(latitude=-33.8, longitude=151.2),
    }

    async def scenario() -> None:
        ordinary = PlaceSearchRequest(**base)
        future = PlaceSearchRequest(**base, include_future_opening_businesses=True)
        await service._search_places(ordinary, budget_key=ToolBudgetKey.CANDIDATE_SEARCH_CALLS)
        await service._search_places(ordinary, budget_key=ToolBudgetKey.CANDIDATE_SEARCH_CALLS)
        await service._search_places(future, budget_key=ToolBudgetKey.CANDIDATE_SEARCH_CALLS)

    asyncio.run(scenario())
    assert len(places.search_requests) == 2
    assert budget.summary()[ToolBudgetKey.CANDIDATE_SEARCH_CALLS.value]["used"] == 2


def test_search_observations_preserve_duplicate_place_intent_hits_before_merging() -> None:
    class RepeatedPlaceProvider(FakePlacesProvider):
        async def search_text(self, request: PlaceSearchRequest) -> PlaceSearchResponse:
            self.search_requests.append(request)
            rank = len(self.search_requests)
            return PlaceSearchResponse(
                candidates=[
                    PlaceCandidateDTO(
                        place_id="shared-poi",
                        display_name="Shared place",
                        location=LatLng(latitude=-33.8, longitude=151.2),
                        opening_date=PlaceOpeningDateDTO(year=2026, month=9),
                        provider_rank=rank,
                    )
                ],
                actual_result_count=3,
                retrieved_at="2026-09-11T00:00:00+00:00",
            )

    places = RepeatedPlaceProvider()
    service = V1EvidenceAcquisitionService(
        places_provider=places,
        weather_provider=FakeWeatherProvider(),
        routes_provider=FakeRoutesProvider(),
        budget=ToolBudget(ToolBudgetLimits(max_candidate_search_calls=2)),
        cache=RequestCache(),
        tracer=NullRunTracer(UUID("00000000-0000-0000-0000-000000000001")),
    )
    observations = asyncio.run(
        service.search_candidate_observations(
            requirements=make_requirements(),
            destination=DestinationContext(
                place_id="sydney",
                name="Sydney",
                latitude=-33.8,
                longitude=151.2,
            ),
        )
    )

    assert [item.candidate.place_id for item in observations] == ["shared-poi", "shared-poi"]
    assert [item.query_hits[0].provider_rank for item in observations] == [1, 2]
    assert all(item.query_hits[0].actual_result_count == 3 for item in observations)
    assert observations[0].query_hits[0].intent_id != observations[1].query_hits[0].intent_id
    assert observations[0].search_opening_date.model_dump() == {
        "year": 2026,
        "month": 9,
        "day": None,
    }


def test_details_and_reviews_cache_keys_are_distinct_and_parameter_sensitive() -> None:
    service, _, _ = _service()
    details = PlaceDetailsRequest(place_id="poi-1", field_mask=PLACES_DETAILS_FIELD_MASK)
    reviews = PlaceReviewsRequest(place_id="poi-1", field_mask=PLACES_REVIEWS_FIELD_MASK)

    assert service._place_details_cache_key(details) != service._place_reviews_cache_key(reviews)
    assert service._place_details_cache_key(details) != service._place_details_cache_key(
        details.model_copy(update={"language_code": "fr"})
    )
    assert service._place_reviews_cache_key(reviews) != service._place_reviews_cache_key(
        reviews.model_copy(update={"field_mask": "id,reviews.name"})
    )


def test_v1_selection_models_keep_query_hits_rating_and_opening_date_separate() -> None:
    candidate = PlaceCandidate(
        place_id="poi-1",
        name="Museum",
        latitude=-33.8,
        longitude=151.2,
        source_query="museums in Sydney",
        category="category_1",
        provider_rank=1,
    )
    hit_a = QueryIntentHit(
        intent_id="museum",
        source_query="museums in Sydney",
        provider_rank=1,
        actual_result_count=4,
    )
    hit_b = QueryIntentHit(
        intent_id="culture",
        source_query="culture in Sydney",
        provider_rank=2,
        actual_result_count=5,
    )
    selection_input = PlaceSelectionInput(
        candidate=candidate,
        query_hits=[hit_a, hit_b],
        search_opening_date=PlaceOpeningDate(year=2026, month=9),
        rating_state=RatingAcquisitionState.MISSING,
    )

    assert len(selection_input.query_hits) == 2
    assert selection_input.search_opening_date.day is None
    assert selection_input.rating is None
    assert "query_hits" not in PlaceCandidate.model_fields
    assert "rating_state" not in PlaceEvidence.model_fields
    assert "user_rating_count" not in PlaceEvidence.model_fields
    with pytest.raises(ValueError, match="provider_rank must be inside"):
        QueryIntentHit(intent_id="bad", source_query="bad", provider_rank=4, actual_result_count=4)
    with pytest.raises(ValueError, match="rating is present exactly"):
        PlaceSelectionInput(
            candidate=candidate,
            query_hits=[hit_a],
            rating=4.5,
            rating_state=RatingAcquisitionState.NOT_ATTEMPTED,
        )


def test_v1_details_normalization_preserves_opening_date_and_missing_rating_state() -> None:
    candidate = PlaceCandidate(
        place_id="poi-1",
        name="Museum",
        latitude=-33.8,
        longitude=151.2,
        source_query="museums in Sydney",
        category="category_1",
        provider_rank=0,
    )
    selection_input = PlaceSelectionInput(
        candidate=candidate,
        query_hits=[
            QueryIntentHit(
                intent_id="category_1",
                source_query="museums in Sydney",
                provider_rank=0,
                actual_result_count=1,
            )
        ],
    )
    details = PlaceDetailsDTO(
        place_id="poi-1",
        display_name="Museum",
        location=LatLng(latitude=-33.8, longitude=151.2),
        opening_date=PlaceOpeningDateDTO(year=2026, month=9),
        retrieved_at="2026-09-11T00:00:00+00:00",
    )

    normalized = normalize_place_details_for_selection(selection_input, details)
    assert normalized.details_opening_date.model_dump() == {
        "year": 2026,
        "month": 9,
        "day": None,
    }
    assert normalized.rating_state is RatingAcquisitionState.MISSING
    assert normalized.rating is None
    assert normalized.structured_evidence is not None
    assert normalized.structured_evidence.availability.value == "available"
    with pytest.raises(ValueError, match="Details ID does not match"):
        normalize_place_details_for_selection(
            selection_input, details.model_copy(update={"place_id": "another-poi"})
        )


def test_shared_place_evidence_does_not_gain_review_or_opening_claims() -> None:
    assert "reviews" not in PlaceEvidence.model_fields
    assert "opening_date" not in PlaceEvidence.model_fields
    assert "experience_profile" not in PlaceEvidence.model_fields
