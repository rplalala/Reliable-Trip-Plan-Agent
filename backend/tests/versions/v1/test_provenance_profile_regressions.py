"""Regressions for the bounded live checkpoint; no provider calls."""

import pytest

from backend.app.evidence.experience_models import ExperienceProfileDraft, ReviewEvidence
from backend.app.policies.experience_profile import validate_profile_draft
from backend.app.policies.interpreted_requirements import locate_source
from backend.app.schemas.interpreted_requirements import SourceQuote
from backend.app.schemas.requirement_boundary import RequirementBoundaryError


@pytest.mark.parametrize(
    "text,quote,start,end,mode",
    [
        ("My mother", "My mother", 0, 9, "exact"),
        ("My mother", "my mother", 0, 9, "casefold_equivalent"),
        ("Stra\u00dfe", "STRASSE", 0, 6, "casefold_equivalent"),
        ("\u039f\u03a3", "\u03bf\u03c2", 0, 2, "casefold_equivalent"),
    ],
)
def test_source_original_unicode_boundaries(text, quote, start, end, mode):
    ref = locate_source(text, SourceQuote(quote=quote, occurrence=0))
    assert (ref.start, ref.end, ref.match_mode) == (start, end, mode)
    assert ref.quote == text[start:end]


@pytest.mark.parametrize(
    "text,quote,occurrence",
    [
        ("My mother; MY MOTHER", "my mother", 0),
        ("My mother; MY MOTHER", "my mother", 1),
        ("My mother", "My mother", 1),
        ("My mother", "Your mother", 0),
        ("My mother.", "my mother!", 0),
        ("My  mother", "my mother", 0),
        ("\u00df", "s", 0),
    ],
)
def test_source_rejects_ambiguous_altered_or_partial_fold(text, quote, occurrence):
    with pytest.raises(RequirementBoundaryError):
        locate_source(text, SourceQuote(quote=quote, occurrence=occurrence))


def test_exact_occurrence_wins_even_when_casefold_ambiguous():
    ref = locate_source(
        "My mother; my mother; My mother", SourceQuote(quote="My mother", occurrence=1)
    )
    assert ref.start == 22 and ref.match_mode == "exact"


def test_overlong_summary_preserves_structured_profile():
    draft = ExperienceProfileDraft(
        place_id="p",
        summary="\U0001f30f" * 300,
        summary_review_refs=["review_1"],
        signals=[{"dimension": "walking_intensity", "value": "LIGHT", "review_refs": ["review_1"]}],
        review_count_used=1,
    )
    profile = validate_profile_draft(
        draft,
        place_id="p",
        reviews=[ReviewEvidence(review_id="review_1", place_id="p", text="A short and easy walk.")],
        retrieved_at="2026-09-19",
    )
    assert profile.summary_truncated and profile.summary == "\U0001f30f" * 240
    assert profile.signals[0].dimension == "walking_intensity"
    assert profile.signals[0].value == "LIGHT"
    assert profile.signals[0].review_refs == ("review_1",)
    assert profile.availability == "available"
