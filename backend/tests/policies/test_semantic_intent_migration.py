"""Offline checks that active V1 policies consume one typed semantic authority."""

from datetime import UTC, date, datetime

from backend.app.evidence.models import (
    EvidenceAvailability,
    OpeningHoursEvidence,
    PlaceCandidate,
    PlaceEvidence,
)
from backend.app.evidence.selection_models import SearchIntentKind
from backend.app.evidence.web_models import (
    OfficialInformationNeed,
    RequestedFacet,
    WebTriggerReason,
)
from backend.app.policies.experience_selection import experience_needs_from_intents
from backend.app.policies.named_place_intent import validate_named_place_intents
from backend.app.policies.official_web import plan_official_web_tasks
from backend.app.policies.poi_funnel import build_place_search_intents
from backend.app.policies.transport import select_transport_mode_from_intent
from backend.app.policies.trip_intent import validate_trip_intents
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.schemas.named_place_intent import NamedPlaceInclusion, NamedPlaceIntent
from backend.app.schemas.request import TravelRequest, TravelRequirements
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

MELBOURNE_REQUEST = (
    "Plan a 5-day trip to Melbourne from 2026-09-17 to 2026-09-21 for one traveler. "
    "Melbourne Museum and National Gallery of Victoria are must-visits. "
    "I want to avoid crowds and prefer less walking. "
    "I am interested in museums, architecture, markets, parks, viewpoints, laneways, "
    "and cultural attractions. Please take into account Melbourne Museum's general "
    "admission fee, whether I need a ticket, whether I need to buy a ticket in advance, "
    "and whether a reservation is required."
)


def _melbourne_extraction() -> TripIntentExtractionResult:
    source = (
        "Melbourne Museum's general admission fee, whether I need a ticket, "
        "whether I need to buy a ticket in advance, and whether a reservation is required"
    )
    named_source = "Melbourne Museum and National Gallery of Victoria are must-visits"
    return TripIntentExtractionResult(
        requirements=TravelRequirements(
            destination="Melbourne",
            start_date=date(2026, 9, 17),
            end_date=date(2026, 9, 21),
            traveler_count=1,
            required_activities=["museums", "architecture", "markets", "parks"],
            preferences=["avoid crowds", "prefer less walking"],
        ),
        named_place_intents=(
            NamedPlaceIntent(
                place_text="Melbourne Museum",
                inclusion=NamedPlaceInclusion.REQUIRED,
                source_text=named_source,
            ),
            NamedPlaceIntent(
                place_text="National Gallery of Victoria",
                inclusion=NamedPlaceInclusion.REQUIRED,
                source_text=named_source,
            ),
        ),
        requested_place_information=tuple(
            RequestedPlaceInformation(
                target_surface="Melbourne Museum",
                target_source_text="Melbourne Museum's general admission fee",
                source_text=source,
                requested_facet=facet,
                operational_need=None,
            )
            for facet in (
                RequestedFacet.ADMISSION_FEE,
                RequestedFacet.TICKET_REQUIREMENT,
                RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT,
                RequestedFacet.RESERVATION_REQUIREMENT,
            )
        ),
        experience_preferences=(
            ExperiencePreferenceIntent(
                preference=ExperiencePreference.AVOID_CROWDS,
                importance=SearchIntentKind.NORMAL_PREFERENCE,
                source_text="avoid crowds",
            ),
            ExperiencePreferenceIntent(
                preference=ExperiencePreference.PREFER_LESS_WALKING,
                importance=SearchIntentKind.NORMAL_PREFERENCE,
                source_text="prefer less walking",
            ),
        ),
        transport_preference=None,
        poi_interests=tuple(
            PoiInterest(
                surface=surface,
                importance=SearchIntentKind.NORMAL_PREFERENCE,
                source_text=(
                    "I am interested in museums, architecture, markets, parks, viewpoints, "
                    "laneways, and cultural attractions"
                ),
            )
            for surface in (
                "museums",
                "architecture",
                "markets",
                "parks",
                "viewpoints",
                "laneways",
                "cultural attractions",
            )
        ),
    )


def _museum_pair() -> tuple[PlaceCandidate, PlaceEvidence]:
    candidate = PlaceCandidate(
        place_id="museum",
        name="Melbourne Museum",
        latitude=-37.803,
        longitude=144.971,
        source_query="Melbourne Museum in Melbourne",
        category="explicit_requirement_1",
        provider_rank=0,
        business_status="OPERATIONAL",
    )
    place = PlaceEvidence(
        place_id="museum",
        name="Melbourne Museum",
        latitude=-37.803,
        longitude=144.971,
        business_status="OPERATIONAL",
        website_uri="https://museumsvictoria.com.au/melbournemuseum/",
        availability=EvidenceAvailability.AVAILABLE,
        retrieved_at=datetime(2026, 9, 15, tzinfo=UTC),
        source_ref="google_places:museum",
    )
    return candidate, place


def test_exact_melbourne_request_preserves_four_facets_into_targeted_tasks() -> None:
    extraction = _melbourne_extraction()
    validate_named_place_intents(extraction.named_place_intents, MELBOURNE_REQUEST)
    validate_trip_intents(extraction, MELBOURNE_REQUEST)
    candidate, place = _museum_pair()

    tasks, gaps, _ = plan_official_web_tasks(
        TravelRequest(request_text=MELBOURNE_REQUEST),
        extraction.requirements,
        [candidate],
        [place],
        load_runtime_config().web_evidence,
        named_place_ids=frozenset({"museum"}),
        must_visit_place_ids=frozenset({"museum"}),
        requested_information=extraction.requested_place_information,
        named_surface_place_ids={"melbourne museum": "museum"},
    )

    assert {gap.requested_facets[0] for gap in gaps} == {
        RequestedFacet.ADMISSION_FEE,
        RequestedFacet.TICKET_REQUIREMENT,
        RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT,
        RequestedFacet.RESERVATION_REQUIREMENT,
    }
    assert len(tasks) == 2
    assert all(task.priority_group == 1 for task in tasks)
    assert all(task.trigger_reasons == (WebTriggerReason.EXPLICIT_USER_NEED,) for task in tasks)
    admission = next(
        task for task in tasks if task.information_need is OfficialInformationNeed.ADMISSION_TICKET
    )
    assert admission.requested_facets == (
        RequestedFacet.ADMISSION_FEE,
        RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT,
        RequestedFacet.TICKET_REQUIREMENT,
    )
    reservation = next(
        task
        for task in tasks
        if task.information_need is OfficialInformationNeed.RESERVATION_REQUIREMENT
    )
    assert reservation.requested_facets == (RequestedFacet.RESERVATION_REQUIREMENT,)


def test_active_typed_web_path_does_not_reclassify_raw_request() -> None:
    extraction = _melbourne_extraction()
    candidate, place = _museum_pair()
    tasks, gaps, _ = plan_official_web_tasks(
        TravelRequest(request_text=MELBOURNE_REQUEST),
        extraction.requirements,
        [candidate],
        [place],
        load_runtime_config().web_evidence,
        named_place_ids=frozenset({"museum"}),
        must_visit_place_ids=frozenset({"museum"}),
        requested_information=(),
        named_surface_place_ids={"melbourne museum": "museum"},
    )
    assert tasks == gaps == []


def test_explicit_date_intent_keeps_its_narrow_task_window() -> None:
    text = "Will Melbourne Museum have special hours on 2026-09-18?"
    information = RequestedPlaceInformation(
        target_surface="Melbourne Museum",
        target_source_text="Melbourne Museum",
        source_text=text,
        requested_facet=None,
        operational_need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
        temporal_scope=RequestedTemporalScope.EXPLICIT_DATE,
        date_source_text="2026-09-18",
        requested_start_date=date(2026, 9, 18),
        requested_end_date=date(2026, 9, 18),
    )
    extraction = _melbourne_extraction().model_copy(
        update={"requested_place_information": (information,)}
    )
    validate_trip_intents(extraction, f"{MELBOURNE_REQUEST} {text}")
    candidate, place = _museum_pair()
    tasks, _, _ = plan_official_web_tasks(
        TravelRequest(request_text=f"{MELBOURNE_REQUEST} {text}"),
        extraction.requirements,
        [candidate],
        [place],
        load_runtime_config().web_evidence,
        named_place_ids=frozenset({"museum"}),
        must_visit_place_ids=frozenset({"museum"}),
        requested_information=extraction.requested_place_information,
        named_surface_place_ids={"melbourne museum": "museum"},
    )
    assert len(tasks) == 1
    assert tasks[0].applicable_start_date == date(2026, 9, 18)
    assert tasks[0].applicable_end_date == date(2026, 9, 18)


def test_typed_opening_question_uses_structured_sufficiency_but_closure_does_not() -> None:
    candidate, place = _museum_pair()
    place = place.model_copy(
        update={
            "opening_hours": OpeningHoursEvidence(
                applicability="date_specific_verified",
                next_open_time=datetime(2026, 9, 18, 9, tzinfo=UTC),
                next_close_time=datetime(2026, 9, 18, 17, tzinfo=UTC),
            )
        }
    )
    base = dict(
        target_surface="Melbourne Museum",
        target_source_text="Melbourne Museum",
        requested_facet=None,
        temporal_scope=RequestedTemporalScope.EXPLICIT_DATE,
        date_source_text="2026-09-18",
        requested_start_date=date(2026, 9, 18),
        requested_end_date=date(2026, 9, 18),
    )
    ordinary = RequestedPlaceInformation(
        **base,
        source_text="Is Melbourne Museum open on 2026-09-18?",
        operational_need=OfficialInformationNeed.SPECIAL_DATE_HOURS,
    )
    maintenance = RequestedPlaceInformation(
        **base,
        source_text="Will Melbourne Museum close for maintenance on 2026-09-18?",
        operational_need=OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
    )

    def plan(item: RequestedPlaceInformation):
        return plan_official_web_tasks(
            TravelRequest(request_text=item.source_text),
            _melbourne_extraction().requirements,
            [candidate],
            [place],
            load_runtime_config().web_evidence,
            named_place_ids=frozenset({"museum"}),
            must_visit_place_ids=frozenset({"museum"}),
            requested_information=(item,),
            named_surface_place_ids={"melbourne museum": "museum"},
        )

    assert plan(ordinary)[0] == []
    closure_tasks = plan(maintenance)[0]
    assert len(closure_tasks) == 1
    assert (
        closure_tasks[0].information_need
        is OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION
    )


def test_typed_poi_experience_and_transport_keep_algorithmic_mapping() -> None:
    extraction = _melbourne_extraction()
    search_intents = build_place_search_intents(
        extraction.requirements,
        named_place_intents=extraction.named_place_intents,
        poi_interests=extraction.poi_interests,
    )
    assert [item.term for item in search_intents[:4]] == [
        "Melbourne Museum",
        "National Gallery of Victoria",
        "museums",
        "architecture",
    ]
    assert "avoid crowds" not in {item.term for item in search_intents}
    assert "prefer less walking" not in {item.term for item in search_intents}
    assert search_intents[0].weight == 1
    assert search_intents[2].weight == SearchIntentKind.NORMAL_PREFERENCE.weight
    needs = experience_needs_from_intents(extraction.experience_preferences)
    assert {item.preference for item in needs.needs} == {
        ExperiencePreference.AVOID_CROWDS,
        ExperiencePreference.PREFER_LESS_WALKING,
    }
    assert select_transport_mode_from_intent(None).travel_mode is TravelMode.WALK
    assert (
        select_transport_mode_from_intent(
            TransportPreferenceIntent(mode=TravelMode.TRANSIT, source_text="use trams")
        ).travel_mode
        is TravelMode.TRANSIT
    )
