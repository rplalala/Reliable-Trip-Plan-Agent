"""Fake model outputs verify representation/policy, not real-language interpretation."""

import asyncio

import pytest

from backend.app.schemas.interpreted_requirements import ClarificationRequired
from backend.tests.llm.azure_foundry.test_requirement_boundary import interpret
from backend.tests.versions.v1.test_interpreted_requirements import draft_for


@pytest.mark.parametrize(
    "case",
    [
        "destination",
        "attraction",
        "area",
        "soft_negative",
        "hard_prohibition",
        "clear_pronoun",
        "ambiguous_pronoun",
        "complete_count",
        "unknown_count",
    ],
)
def test_semantic_representations_through_real_sdk(case):
    from backend.app.policies.interpreted_requirements import (
        assess_requirements,
        require_resolved_hard,
    )

    text = {
        "destination": "Plan a trip to Madrid.",
        "attraction": "I hope to visit the Prado Museum.",
        "area": "Include Madrid as an actual stop.",
        "soft_negative": "Prefer avoiding crowds, but I can compromise.",
        "hard_prohibition": "I cannot use any stairs.",
        "clear_pronoun": "My sister says she prefers museums.",
        "ambiguous_pronoun": "My sister and her friend are coming. She prefers museums.",
        "complete_count": "Only my sister, my brother and I will travel.",
        "unknown_count": "My sister and I will travel; others may join.",
    }[case]
    data = draft_for(text).model_dump(mode="json")
    data["semantic_requirements"] = []
    if case in ("attraction", "area"):
        data["named_places"] = [
            {
                "place_text": "Madrid" if case == "area" else "Prado Museum",
                "inclusion": "REQUIRED",
                "source_refs": [{"quote": text, "occurrence": 0}],
            }
        ]
    if case in ("soft_negative", "hard_prohibition", "clear_pronoun", "ambiguous_pronoun"):
        semantic = draft_for(text).model_dump(mode="json")["semantic_requirements"][0]
        data["semantic_requirements"] = [semantic]
        if case in ("soft_negative", "hard_prohibition"):
            semantic.update(
                polarity="avoid", strength="hard" if case == "hard_prohibition" else "medium"
            )
        elif case == "clear_pronoun":
            data["subjects"] = [
                {
                    "local_key": "owner",
                    "label": "Sister",
                    "source_refs": [{"quote": text, "occurrence": 0}],
                }
            ]
            semantic["subject_target"] = {
                "kind": "specified",
                "first_ref": "owner",
                "additional_refs": [],
            }
        else:
            semantic["subject_target"] = {
                "kind": "unresolved",
                "reason": "Two possible antecedents",
            }
    if case == "ambiguous_pronoun":
        with pytest.raises(ClarificationRequired, match="unresolved_subject_attribution"):
            asyncio.run(interpret(data, text=text))
        return
    result, _ = asyncio.run(interpret(data, text=text))
    if case == "destination":
        assert not result.named_places
    elif case in ("attraction", "area"):
        assert result.named_places[0].inclusion == "REQUIRED"
        assert result.named_places[0].source_refs[0].quote == text
    elif case in ("soft_negative", "hard_prohibition"):
        assert result.semantic_requirements[0].polarity == "avoid"
        if case == "hard_prohibition":
            with pytest.raises(ClarificationRequired, match="unsupported_hard"):
                require_resolved_hard(assess_requirements(result))
        else:
            require_resolved_hard(assess_requirements(result))
    elif case == "clear_pronoun":
        assert result.semantic_requirements[0].subject_refs == ("subject_1",)
    else:
        assert result.requirements.traveler_count == 2  # Form remains authoritative.
