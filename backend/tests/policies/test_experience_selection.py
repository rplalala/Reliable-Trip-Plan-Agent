"""Offline V1-A review taxonomy, provenance, scoring, and counterfactual tests."""

from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from backend.app.evidence.experience_models import (
    ExperienceConfidence,
    ExperienceDimension,
    ExperienceProfile,
    ExperienceProfileDraft,
    ExperienceSignal,
    ExperienceSignalDraft,
    ExperienceValue,
)
from backend.app.evidence.models import EvidenceAvailability, PlaceCandidate, PlaceEvidence
from backend.app.evidence.selection_models import (
    PlaceSelectionInput,
    QueryIntentHit,
    RatingAcquisitionState,
)
from backend.app.integrations.models import PlaceReviewDTO, PlaceReviewsDTO
from backend.app.policies.experience_profile import preprocess_reviews, validate_profile_draft
from backend.app.policies.experience_selection import (
    extract_experience_needs,
    reachable_experience_values,
    score_experience,
)
from backend.app.policies.review_sensitivity import (
    ReviewSelectionContext,
    find_review_sensitive_candidates,
)
from backend.app.policies.trip_dates import create_trip_date_window
from backend.app.schemas.request import TravelRequirements

WINDOW = create_trip_date_window(date(2026, 9, 11))


def requirements(*preferences: str) -> TravelRequirements:
    return TravelRequirements(
        destination="Sydney",
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 12),
        preferences=list(preferences),
    )


def selection_place(place_id: str, rating: float) -> PlaceSelectionInput:
    candidate = PlaceCandidate(
        place_id=place_id,
        name=place_id,
        latitude=-33.87,
        longitude=151.20,
        business_status="OPERATIONAL",
        source_query="museum in Sydney",
        category="museum",
        provider_rank=0,
    )
    evidence = PlaceEvidence(
        place_id=place_id,
        name=place_id,
        latitude=-33.87,
        longitude=151.20,
        business_status="OPERATIONAL",
        rating=rating,
        availability=EvidenceAvailability.AVAILABLE,
        retrieved_at=datetime(2026, 9, 11, tzinfo=UTC),
        source_ref=f"places:{place_id}",
    )
    return PlaceSelectionInput(
        candidate=candidate,
        query_hits=[
            QueryIntentHit(
                intent_id="museum",
                source_query="museum in Sydney",
                provider_rank=0,
                actual_result_count=2,
            )
        ],
        structured_evidence=evidence,
        rating=rating,
        rating_state=RatingAcquisitionState.AVAILABLE,
    )


def profile(
    value: ExperienceValue,
    *,
    dimension: ExperienceDimension = ExperienceDimension.CROWDING,
    confidence: ExperienceConfidence = ExperienceConfidence.MEDIUM,
) -> ExperienceProfile:
    return ExperienceProfile(
        place_id="a",
        availability=EvidenceAvailability.AVAILABLE,
        signals=(
            ExperienceSignal(
                dimension=dimension,
                value=value,
                review_refs=("review_1", "review_2")
                if confidence is ExperienceConfidence.MEDIUM
                else ("review_1",),
                confidence=confidence,
            ),
        ),
    )


def test_preprocess_removes_empty_duplicates_and_preserves_bounded_order() -> None:
    response = PlaceReviewsDTO(
        place_id="a",
        reviews=[
            PlaceReviewDTO(text="  First  review ", resource_name="one"),
            PlaceReviewDTO(text="first review"),
            PlaceReviewDTO(text="  "),
            *(PlaceReviewDTO(text=f"Review {index}") for index in range(2, 10)),
        ],
        retrieved_at="2026-09-11T00:00:00+00:00",
    )
    result = preprocess_reviews(response, place_id="a")
    assert len(result) == 5
    assert [item.review_id for item in result] == [f"review_{i}" for i in range(1, 6)]
    assert [item.text for item in result] == [
        "First review",
        "Review 2",
        "Review 3",
        "Review 4",
        "Review 5",
    ]
    assert preprocess_reviews(response, place_id="a") == result
    with pytest.raises(ValueError, match="Place ID"):
        preprocess_reviews(response, place_id="b")


def test_preprocess_empty_and_truncated_review_content() -> None:
    empty = PlaceReviewsDTO(
        place_id="a",
        reviews=[PlaceReviewDTO(text=None), PlaceReviewDTO(text=" ")],
        retrieved_at="now",
    )
    assert preprocess_reviews(empty, place_id="a") == ()
    long = PlaceReviewsDTO(
        place_id="a",
        reviews=[PlaceReviewDTO(text="A" * 1500), PlaceReviewDTO(text="A" * 1500 + "B")],
        retrieved_at="now",
    )
    bounded = preprocess_reviews(long, place_id="a")
    assert len(bounded) == 1
    assert len(bounded[0].text) == 1200


def test_profile_provenance_and_confidence_are_application_derived() -> None:
    reviews = preprocess_reviews(
        PlaceReviewsDTO(
            place_id="a",
            reviews=[PlaceReviewDTO(text="crowded"), PlaceReviewDTO(text="busy")],
            retrieved_at="now",
        ),
        place_id="a",
    )
    draft = ExperienceProfileDraft(
        place_id="a",
        summary="Visitors describe crowds.",
        summary_review_refs=["review_1"],
        signals=[
            ExperienceSignalDraft(
                dimension=ExperienceDimension.CROWDING,
                value=ExperienceValue.HIGH,
                review_refs=["review_1", "review_1"],
            )
        ],
        review_count_used=2,
    )
    result = validate_profile_draft(draft, place_id="a", reviews=reviews, retrieved_at="now")
    assert result.signals[0].confidence is ExperienceConfidence.LOW
    assert result.signals[0].review_refs == ("review_1",)
    medium = validate_profile_draft(
        draft.model_copy(
            update={
                "signals": [
                    draft.signals[0].model_copy(update={"review_refs": ["review_1", "review_2"]})
                ]
            }
        ),
        place_id="a",
        reviews=reviews,
        retrieved_at="now",
    )
    assert medium.signals[0].confidence is ExperienceConfidence.MEDIUM
    for invalid in (
        draft.model_copy(update={"place_id": "b"}),
        draft.model_copy(update={"review_count_used": 1}),
        draft.model_copy(update={"summary_review_refs": ["missing"]}),
    ):
        with pytest.raises(ValueError):
            validate_profile_draft(invalid, place_id="a", reviews=reviews, retrieved_at="now")
    with pytest.raises(ValidationError):
        ExperienceSignalDraft(dimension="crowding", value="ACCESSIBLE", review_refs=["review_1"])
    with pytest.raises(ValidationError):
        ExperienceProfileDraft.model_validate({**draft.model_dump(), "selection_score": 5})
    with pytest.raises(ValidationError):
        ExperienceSignal(
            dimension="crowding", value="LOW", review_refs=("review_1",), confidence="high"
        )
    no_summary = draft.model_copy(update={"summary": None, "summary_review_refs": []})
    assert (
        validate_profile_draft(
            no_summary, place_id="a", reviews=reviews, retrieved_at="now"
        ).availability
        is EvidenceAvailability.PARTIAL
    )
    unsupported_signal = draft.model_copy(
        update={"signals": [draft.signals[0].model_copy(update={"review_refs": []})]}
    )
    retained = validate_profile_draft(
        unsupported_signal, place_id="a", reviews=reviews, retrieved_at="now"
    )
    assert retained.signals == ()
    assert retained.availability is EvidenceAvailability.PARTIAL


@pytest.mark.parametrize(
    ("preference", "dimension", "match", "conflict"),
    [
        ("avoid crowds", ExperienceDimension.CROWDING, ExperienceValue.LOW, ExperienceValue.HIGH),
        (
            "less walking",
            ExperienceDimension.WALKING_INTENSITY,
            ExperienceValue.LIGHT,
            ExperienceValue.HIGH,
        ),
        (
            "prefer accessible",
            ExperienceDimension.ACCESSIBILITY,
            ExperienceValue.ACCESSIBLE,
            ExperienceValue.LIMITED,
        ),
        (
            "family-friendly",
            ExperienceDimension.FAMILY_FRIENDLINESS,
            ExperienceValue.FAMILY_FRIENDLY,
            ExperienceValue.NOT_FAMILY_FRIENDLY,
        ),
        (
            "prefer short visits",
            ExperienceDimension.VISIT_DURATION,
            ExperienceValue.SHORT,
            ExperienceValue.LONG,
        ),
        (
            "prefer long visits",
            ExperienceDimension.VISIT_DURATION,
            ExperienceValue.LONG,
            ExperienceValue.SHORT,
        ),
    ],
)
def test_all_approved_preference_mappings(
    preference: str,
    dimension: ExperienceDimension,
    match: ExperienceValue,
    conflict: ExperienceValue,
) -> None:
    needs = extract_experience_needs(requirements(preference)).needs
    assert len(needs) == 1
    assert score_experience(profile(match, dimension=dimension), needs).total == 5
    assert score_experience(profile(conflict, dimension=dimension), needs).total == -10
    assert score_experience(
        profile(match, dimension=dimension, confidence=ExperienceConfidence.LOW), needs
    ).total == Decimal("2.5")
    assert score_experience(None, needs).total == 0


def test_reachable_values_clamp_and_contradictory_visit_preference() -> None:
    single = extract_experience_needs(requirements("avoid crowds"))
    assert reachable_experience_values(single.needs) == (
        Decimal(-10),
        Decimal(-5),
        Decimal(0),
        Decimal("2.5"),
        Decimal(5),
    )
    multiple = extract_experience_needs(
        requirements("avoid crowds", "less walking", "family-friendly")
    )
    values = reachable_experience_values(multiple.needs)
    assert values[0] == -15 and values[-1] == 10
    assert len(values) == len(set(values))
    ambiguous = extract_experience_needs(requirements("prefer short visits", "prefer long visits"))
    assert ambiguous.needs == ()
    assert ambiguous.ambiguities == ("contradictory_visit_duration_preferences",)
    assert extract_experience_needs(requirements("beaches")).needs == ()
    assert extract_experience_needs(requirements("not family-friendly")).needs == ()
    assert extract_experience_needs(requirements("not suitable for children")).needs == ()
    assert len(extract_experience_needs(requirements("avoid crowded places")).needs) == 1
    assert len(extract_experience_needs(requirements("short visits")).needs) == 1


def test_review_sensitivity_uses_real_selector_and_skips_must_visits() -> None:
    places = [selection_place("a", 4.0), selection_place("b", 3.8)]
    needs = extract_experience_needs(requirements("avoid crowds")).needs
    context = ReviewSelectionContext(
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 12),
        window=WINDOW,
        capacity=1,
        must_visit_place_ids=frozenset(),
        excluded_place_ids=frozenset(),
        unresolved_required_names=(),
    )
    sensitive = find_review_sensitive_candidates(
        places, context=context, needs=needs, current_scores={}
    )
    assert {item.place_id for item in sensitive} == {"a", "b"}
    assert sensitive[0].minimum_flip_magnitude == Decimal("2.5")
    must_context = ReviewSelectionContext(
        **{**context.__dict__, "must_visit_place_ids": frozenset({"a"})}
    )
    assert (
        find_review_sensitive_candidates(
            places, context=must_context, needs=needs, current_scores={}
        )
        == ()
    )


def test_neutral_low_conflict_multiple_preferences_and_no_unexpressed_score() -> None:
    needs = extract_experience_needs(
        requirements("avoid crowds", "less walking", "family-friendly")
    ).needs
    assert score_experience(profile(ExperienceValue.MODERATE), needs).total == 0
    assert (
        score_experience(
            profile(ExperienceValue.HIGH, confidence=ExperienceConfidence.LOW), needs
        ).total
        == -5
    )
    positive = ExperienceProfile(
        place_id="a",
        availability=EvidenceAvailability.AVAILABLE,
        signals=tuple(
            ExperienceSignal(
                dimension=dimension,
                value=value,
                review_refs=("review_1", "review_2"),
                confidence=ExperienceConfidence.MEDIUM,
            )
            for dimension, value in (
                (ExperienceDimension.CROWDING, ExperienceValue.LOW),
                (ExperienceDimension.WALKING_INTENSITY, ExperienceValue.LIGHT),
                (ExperienceDimension.FAMILY_FRIENDLINESS, ExperienceValue.FAMILY_FRIENDLY),
            )
        ),
    )
    negative = ExperienceProfile(
        place_id="a",
        availability=EvidenceAvailability.AVAILABLE,
        signals=tuple(
            ExperienceSignal(
                dimension=dimension,
                value=value,
                review_refs=("review_1", "review_2"),
                confidence=ExperienceConfidence.MEDIUM,
            )
            for dimension, value in (
                (ExperienceDimension.CROWDING, ExperienceValue.HIGH),
                (ExperienceDimension.WALKING_INTENSITY, ExperienceValue.HIGH),
                (ExperienceDimension.FAMILY_FRIENDLINESS, ExperienceValue.NOT_FAMILY_FRIENDLY),
            )
        ),
    )
    assert score_experience(positive, needs).total == 10
    assert score_experience(negative, needs).total == -15
    unrelated = extract_experience_needs(requirements("less walking")).needs
    assert score_experience(profile(ExperienceValue.LOW), unrelated).total == 0


def test_counterfactual_does_not_use_unreachable_global_endpoint() -> None:
    places = [selection_place("a", 4.8), selection_place("b", 3.5)]
    context = ReviewSelectionContext(
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 12),
        window=WINDOW,
        capacity=1,
        must_visit_place_ids=frozenset(),
        excluded_place_ids=frozenset(),
        unresolved_required_names=(),
    )
    needs = extract_experience_needs(requirements("avoid crowds")).needs
    assert (
        find_review_sensitive_candidates(
            places,
            context=context,
            needs=needs,
            current_scores={},
            attempted_ids=frozenset({"a"}),
        )
        == ()
    )  # b needs more than +5, but only +5 is reachable for one signal.
    both_fit = ReviewSelectionContext(
        start_date=context.start_date,
        end_date=context.end_date,
        window=WINDOW,
        capacity=2,
        must_visit_place_ids=frozenset(),
        excluded_place_ids=frozenset(),
        unresolved_required_names=(),
    )
    assert (
        find_review_sensitive_candidates(places, context=both_fit, needs=needs, current_scores={})
        == ()
    )


def test_review_priority_uses_magnitude_then_stable_place_id() -> None:
    places = [selection_place(place_id, 4.0) for place_id in ("c", "a", "b")]
    context = ReviewSelectionContext(
        start_date=date(2026, 9, 12),
        end_date=date(2026, 9, 12),
        window=WINDOW,
        capacity=1,
        must_visit_place_ids=frozenset(),
        excluded_place_ids=frozenset(),
        unresolved_required_names=(),
    )
    needs = extract_experience_needs(requirements("avoid crowds")).needs
    first = find_review_sensitive_candidates(
        places, context=context, needs=needs, current_scores={}
    )
    second = find_review_sensitive_candidates(
        places, context=context, needs=needs, current_scores={}
    )
    assert first == second
    assert [item.place_id for item in first] == ["b", "c", "a"]
