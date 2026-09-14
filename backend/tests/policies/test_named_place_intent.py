"""Mechanical checks for named-place source grounding and duplicate intents."""

import pytest
from pydantic import ValidationError

from backend.app.policies.named_place_intent import (
    NamedPlaceIntentContractError,
    validate_named_place_intents,
)
from backend.app.schemas.named_place_intent import NamedPlaceInclusion, NamedPlaceIntent


def _intent(
    place_text: str,
    source_text: str,
    inclusion: NamedPlaceInclusion = NamedPlaceInclusion.REQUIRED,
) -> NamedPlaceIntent:
    return NamedPlaceIntent(
        place_text=place_text,
        inclusion=inclusion,
        source_text=source_text,
    )


def test_contiguous_source_and_original_place_surface_are_valid() -> None:
    request = "Plan Sydney. I want to visit Sydney Opera House on Tuesday."

    result = validate_named_place_intents(
        [_intent("Sydney Opera House", "I want to visit Sydney Opera House")], request
    )

    assert len(result) == 1
    assert result[0].place_text == "Sydney Opera House"
    assert result[0].source_text == "I want to visit Sydney Opera House"


@pytest.mark.parametrize(
    ("place_text", "source_text", "request_text", "code"),
    [
        (
            "Sydney Opera House",
            "I want to visit Sydney Opera House",
            "Plan Sydney",
            "source_not_in_request",
        ),
        (
            "Sydney Opera House",
            "I want to visit Opera House",
            "I want to visit Opera House",
            "place_not_in_source",
        ),
        (
            "Visit Sydney Opera House",
            "Visit Sydney Opera House",
            "Visit Sydney Opera House",
            "action_wrapper_in_place_text",
        ),
    ],
)
def test_invalid_provenance_or_place_shape_fails_explicitly(
    place_text: str, source_text: str, request_text: str, code: str
) -> None:
    with pytest.raises(NamedPlaceIntentContractError) as error:
        validate_named_place_intents([_intent(place_text, source_text)], request_text)
    assert error.value.code == code


@pytest.mark.parametrize("field", ["place_text", "source_text"])
def test_empty_or_overlong_text_is_structurally_invalid(field: str) -> None:
    values = {
        "place_text": "Sydney Opera House",
        "inclusion": NamedPlaceInclusion.REQUIRED,
        "source_text": "Sydney Opera House is a must-visit",
    }
    for value in ("", "   ", "x" * 321):
        values[field] = value
        with pytest.raises(ValidationError):
            NamedPlaceIntent.model_validate(values)


@pytest.mark.parametrize(
    "category",
    [
        "museum",
        "museums",
        "park",
        "parks",
        "beach",
        "beaches",
        "viewpoints",
        "cultural attractions",
    ],
)
def test_complete_generic_category_is_not_a_named_place(category: str) -> None:
    with pytest.raises(NamedPlaceIntentContractError) as error:
        validate_named_place_intents([_intent(category, category)], category)
    assert error.value.code == "generic_category_as_named_place"


def test_category_word_inside_real_name_does_not_reject_it() -> None:
    result = validate_named_place_intents(
        [_intent("Australian Museum", "I hope to visit Australian Museum")],
        "I hope to visit Australian Museum",
    )
    assert result[0].place_text == "Australian Museum"


def test_equal_duplicates_merge_in_request_order_and_keep_all_source_spans() -> None:
    request = "I want to visit Sydney Opera House. Sydney Opera House is a must-visit."
    first = _intent("Sydney Opera House", "I want to visit Sydney Opera House")
    second = _intent("SYDNEY  OPERA HOUSE", "Sydney Opera House is a must-visit")

    forward = validate_named_place_intents([first, second], request)
    reverse = validate_named_place_intents([second, first], request)

    assert forward == reverse
    assert len(forward) == 1
    assert forward[0].source_text == first.source_text
    assert forward[0].additional_source_texts == (second.source_text,)


def test_conflicting_inclusion_for_one_place_fails_without_precedence() -> None:
    request = "Sydney Opera House is a must-visit. Maybe Sydney Opera House."
    intents = [
        _intent("Sydney Opera House", "Sydney Opera House is a must-visit"),
        _intent("Sydney Opera House", "Maybe Sydney Opera House", NamedPlaceInclusion.OPTIONAL),
    ]

    with pytest.raises(NamedPlaceIntentContractError) as error:
        validate_named_place_intents(intents, request)
    assert error.value.code == "conflicting_inclusion"
