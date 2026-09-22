"""Revised V1 contract and bounded selection tests without live providers."""

import pytest
from pydantic import ValidationError

from backend.app.policies.interpreted_requirements import (
    assess_requirements,
    canonicalize_requirements,
    locate_source,
    require_resolved_hard,
)
from backend.app.schemas.interpreted_requirements import (
    ClarificationRequired,
    InterpretationDraft,
    SemanticDraft,
    SourceQuote,
)
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.tests.request_fixtures import make_request


def draft_for(text="Prefer local places", **updates):
    semantic = SemanticDraft(
        local_key="s",
        normalized_text=text,
        kind="preference",
        polarity="favor",
        strength="high",
        scope="selected_poi_set",
        subject_target={"kind": "party"},
        source_refs=(SourceQuote(quote=text, occurrence=0),),
    )
    fields = dict(
        named_places=(),
        requested_place_information=(),
        transport_preference=None,
        semantic_requirements=(semantic,),
        subjects=(),
        discovery_intents=(),
        experience_evidence_requests=(),
        extraction_issues=(),
        overflow=False,
    )
    fields.update(updates)
    return InterpretationDraft(**fields)


@pytest.mark.parametrize(
    "text",
    [
        "I want historical places but not typical tourist traps.",
        "I prefer somewhere unusual but not gimmicky.",
        "I don't want three similar museums.",
        "I am willing to travel farther for something unique.",
        "My mother prefers quiet places, my father likes architecture.",
        "Absolutely no stairs.",
        "I prefer less walking.",
        "I want places locals actually visit.",
        "I do not want casinos.",
    ],
)
def test_arbitrary_semantics_survive_without_new_vocabulary(text):
    contract = canonicalize_requirements(draft_for(text), make_request(text))
    item = contract.semantic_requirements[0]
    assert item.normalized_text == text
    assert item.source_refs[0].quote == text
    assert item.requirement_id == "semantic_1"
    assert contract.requirements.preferences == []


def test_hard_is_not_certified_by_accessibility_evidence():
    text = "Absolutely no stairs."
    draft = draft_for(text)
    draft = draft.model_copy(
        update={
            "semantic_requirements": (
                draft.semantic_requirements[0].model_copy(update={"strength": "hard"}),
            )
        }
    )
    assessment = assess_requirements(canonicalize_requirements(draft, make_request(text)))
    assert assessment[0].check_result == "unknown"
    with pytest.raises(ClarificationRequired, match="unsupported_hard"):
        require_resolved_hard(assessment)


def test_unicode_occurrence_offsets_are_application_owned():
    text = "\U0001f30f local; local"
    ref = locate_source(text, SourceQuote(quote="local", occurrence=1))
    assert text[ref.start : ref.end] == "local"
    assert ref.start == 9
    with pytest.raises(RequirementBoundaryError):
        locate_source(text, SourceQuote(quote="local", occurrence=2))


def test_exact_duplicates_share_identity_and_do_not_multiply_weight():
    text = "Prefer local places"
    draft = draft_for(text)
    duplicate = draft.semantic_requirements[0].model_copy(update={"local_key": "s2"})
    contract = canonicalize_requirements(
        draft.model_copy(
            update={"semantic_requirements": (*draft.semantic_requirements, duplicate)}
        ),
        make_request(text),
    )
    assert len(contract.semantic_requirements) == 1


def test_model_cannot_supply_enforcement_or_app_ids():
    with pytest.raises(ValidationError):
        SemanticDraft(**{**draft_for().semantic_requirements[0].model_dump(), "verified": True})
