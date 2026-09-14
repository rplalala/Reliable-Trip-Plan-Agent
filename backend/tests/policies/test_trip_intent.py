"""Offline examples for the one-call user-semantic extraction contract."""

from datetime import date

import pytest

from backend.app.evidence.scope_models import SubjectScope
from backend.app.evidence.selection_models import SearchIntentKind
from backend.app.evidence.web_models import OfficialInformationNeed, RequestedFacet
from backend.app.policies.trip_intent import TripIntentContractError, validate_trip_intents
from backend.app.schemas.named_place_intent import NamedPlaceInclusion, NamedPlaceIntent
from backend.app.schemas.request import TravelRequirements
from backend.app.schemas.trip_intent import (
    ExperiencePreference,
    ExperiencePreferenceIntent,
    PoiInterest,
    RequestedPlaceInformation,
    RequestedTemporalScope,
    TransportPreferenceIntent,
    TravelMode,
    TripIntentExtractionResult,
)


def _result(
    text: str,
    *,
    information: tuple[RequestedPlaceInformation, ...] = (),
    experience: tuple[ExperiencePreferenceIntent, ...] = (),
    transport: TransportPreferenceIntent | None = None,
    poi: tuple[PoiInterest, ...] = (),
) -> TripIntentExtractionResult:
    named = (
        (
            NamedPlaceIntent(
                place_text="Melbourne Museum",
                inclusion=NamedPlaceInclusion.OPTIONAL,
                source_text="Melbourne Museum",
            ),
        )
        if "Melbourne Museum" in text
        else ()
    )
    return TripIntentExtractionResult(
        requirements=TravelRequirements(
            destination="Melbourne", start_date=date(2026, 9, 15), end_date=date(2026, 9, 15)
        ),
        named_place_intents=named,
        requested_place_information=information,
        experience_preferences=experience,
        transport_preference=transport,
        poi_interests=poi,
    )


@pytest.mark.parametrize(
    ("question", "facet"),
    [
        ("What's the entry fee?", RequestedFacet.ADMISSION_FEE),
        ("How much does it cost to get in?", RequestedFacet.ADMISSION_FEE),
        ("What is general admission?", RequestedFacet.GENERAL_ADMISSION_POLICY),
        ("Do I need a ticket?", RequestedFacet.TICKET_REQUIREMENT),
        (
            "Should I buy the ticket beforehand?",
            RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT,
        ),
        ("Do I have to reserve?", RequestedFacet.RESERVATION_REQUIREMENT),
    ],
)
def test_mocked_paraphrases_preserve_one_controlled_information_facet(
    question: str, facet: RequestedFacet
) -> None:
    text = f"Melbourne Museum. {question}"
    item = RequestedPlaceInformation(
        target_surface="Melbourne Museum",
        target_source_text="Melbourne Museum",
        source_text=question,
        requested_facet=facet,
        operational_need=None,
    )
    result = validate_trip_intents(_result(text, information=(item,)), text)
    assert result.requested_place_information[0].requested_facet is facet


def test_compound_request_keeps_four_independent_facets() -> None:
    question = (
        "How much is admission, do I need a ticket, should I buy it in advance, "
        "and is a reservation required?"
    )
    text = f"Melbourne Museum: {question}"
    information = tuple(
        RequestedPlaceInformation(
            target_surface="Melbourne Museum",
            target_source_text="Melbourne Museum",
            source_text=question,
            requested_facet=facet,
            operational_need=None,
        )
        for facet in (
            RequestedFacet.ADMISSION_FEE,
            RequestedFacet.TICKET_REQUIREMENT,
            RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT,
            RequestedFacet.RESERVATION_REQUIREMENT,
        )
    )
    result = validate_trip_intents(_result(text, information=information), text)
    assert {item.requested_facet for item in result.requested_place_information} == {
        RequestedFacet.ADMISSION_FEE,
        RequestedFacet.TICKET_REQUIREMENT,
        RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT,
        RequestedFacet.RESERVATION_REQUIREMENT,
    }


@pytest.mark.parametrize(
    ("source", "preference"),
    [
        ("I dislike packed venues", ExperiencePreference.AVOID_CROWDS),
        ("Keep walking to a minimum", ExperiencePreference.PREFER_LESS_WALKING),
        ("Wheelchair access matters", ExperiencePreference.PREFER_ACCESSIBLE),
        ("Suitable for my children", ExperiencePreference.PREFER_FAMILY_FRIENDLY),
        ("I prefer quick stops", ExperiencePreference.PREFER_SHORT_VISIT),
        ("I want to spend a full day", ExperiencePreference.PREFER_LONG_VISIT),
    ],
)
def test_mocked_experience_paraphrases_use_approved_enum(
    source: str, preference: ExperiencePreference
) -> None:
    intent = ExperiencePreferenceIntent(
        preference=preference,
        importance=SearchIntentKind.NORMAL_PREFERENCE,
        source_text=source,
    )
    assert validate_trip_intents(_result(source, experience=(intent,)), source)


@pytest.mark.parametrize(
    ("source", "mode"),
    [
        ("We will hire a car", TravelMode.DRIVE),
        ("We plan to get around on foot", TravelMode.WALK),
        ("We will cycle between stops", TravelMode.BICYCLE),
        ("We prefer trains and buses", TravelMode.TRANSIT),
    ],
)
def test_mocked_transport_paraphrases_use_existing_modes(source: str, mode: TravelMode) -> None:
    intent = TransportPreferenceIntent(mode=mode, source_text=source)
    assert validate_trip_intents(_result(source, transport=intent), source)


def test_poi_category_is_separate_from_experience_preference() -> None:
    text = "I like architecture and markets, and I dislike packed venues."
    result = validate_trip_intents(
        _result(
            text,
            poi=(
                PoiInterest(
                    surface="architecture",
                    importance=SearchIntentKind.NORMAL_PREFERENCE,
                    source_text="I like architecture and markets",
                ),
                PoiInterest(
                    surface="markets",
                    importance=SearchIntentKind.NORMAL_PREFERENCE,
                    source_text="I like architecture and markets",
                ),
            ),
            experience=(
                ExperiencePreferenceIntent(
                    preference=ExperiencePreference.AVOID_CROWDS,
                    importance=SearchIntentKind.NORMAL_PREFERENCE,
                    source_text="I dislike packed venues",
                ),
            ),
        ),
        text,
    )
    assert [item.surface for item in result.poi_interests] == ["architecture", "markets"]
    assert result.experience_preferences[0].preference is ExperiencePreference.AVOID_CROWDS


def test_invalid_source_span_fails_without_reinterpreting_language() -> None:
    text = "Melbourne Museum. Do I need a ticket?"
    item = RequestedPlaceInformation(
        target_surface="Melbourne Museum",
        target_source_text="Melbourne Museum",
        source_text="Do I need a reservation?",
        requested_facet=RequestedFacet.RESERVATION_REQUIREMENT,
        operational_need=None,
    )
    with pytest.raises(TripIntentContractError, match="information_source_not_in_request"):
        validate_trip_intents(_result(text, information=(item,)), text)


def test_operational_question_keeps_explicit_scope_and_date_source() -> None:
    text = "Will Melbourne Museum's special exhibition open on September 15?"
    item = RequestedPlaceInformation(
        target_surface="Melbourne Museum",
        target_source_text="Melbourne Museum",
        source_text=text,
        requested_facet=None,
        operational_need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        subject_scope=SubjectScope.EXHIBITION,
        scope_text="special exhibition",
        temporal_scope=RequestedTemporalScope.EXPLICIT_DATE,
        date_source_text="September 15",
        requested_start_date=date(2026, 9, 15),
        requested_end_date=date(2026, 9, 15),
    )
    assert validate_trip_intents(_result(text, information=(item,)), text)


def test_explicit_information_date_outside_trip_fails_provenance_validation() -> None:
    text = "Will Melbourne Museum open on September 16?"
    item = RequestedPlaceInformation(
        target_surface="Melbourne Museum",
        target_source_text="Melbourne Museum",
        source_text=text,
        requested_facet=None,
        operational_need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        temporal_scope=RequestedTemporalScope.EXPLICIT_DATE,
        date_source_text="September 16",
        requested_start_date=date(2026, 9, 16),
        requested_end_date=date(2026, 9, 16),
    )
    with pytest.raises(TripIntentContractError, match="information_date_outside_trip"):
        validate_trip_intents(_result(text, information=(item,)), text)
