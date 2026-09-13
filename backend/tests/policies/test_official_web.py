"""Offline checks for V1-B residual gaps and proactive task ordering."""

from datetime import UTC, date, datetime

from backend.app.evidence.models import (
    EvidenceAvailability,
    OpeningHoursEvidence,
    PlaceCandidate,
    PlaceEvidence,
)
from backend.app.evidence.scope_models import SubjectScope
from backend.app.evidence.web_models import (
    OfficialInformationNeed,
    RequestedFacet,
    WebTriggerReason,
)
from backend.app.policies.official_web import plan_official_web_tasks
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.schemas.request import TravelRequest, TravelRequirements

START = date(2026, 12, 25)


def _pair(
    place_id: str,
    name: str,
    *,
    availability: EvidenceAvailability = EvidenceAvailability.AVAILABLE,
    candidate_status: str | None = "OPERATIONAL",
    evidence_status: str | None = "OPERATIONAL",
    website: str | None = None,
    hours: OpeningHoursEvidence | None = None,
) -> tuple[PlaceCandidate, PlaceEvidence]:
    candidate = PlaceCandidate(
        place_id=place_id,
        name=name,
        latitude=-33.8,
        longitude=151.2,
        source_query="Sydney attractions",
        category="category_1",
        provider_rank=0,
        business_status=candidate_status,
    )
    place = PlaceEvidence(
        place_id=place_id,
        name=name,
        latitude=-33.8,
        longitude=151.2,
        business_status=evidence_status,
        availability=availability,
        website_uri=website or f"https://{place_id}.example.org",
        opening_hours=hours,
        retrieved_at=datetime(2026, 12, 20, tzinfo=UTC),
        source_ref=f"google_places:{place_id}",
    )
    return candidate, place


def _plan(text: str, pairs: list[tuple[PlaceCandidate, PlaceEvidence]], required=()):
    return plan_official_web_tasks(
        TravelRequest(request_text=text),
        TravelRequirements(
            destination="Sydney",
            start_date=START,
            end_date=START,
            required_activities=list(required),
        ),
        [candidate for candidate, _ in pairs],
        [place for _, place in pairs],
        load_runtime_config().web_evidence,
    )


def test_sufficient_current_status_creates_no_residual_gap() -> None:
    tasks, gaps, assessments = _plan("Is Alpha Zoo open now?", [_pair("alpha", "Alpha Zoo")])
    assert gaps == []
    assert [task.information_need for task in tasks] == [
        OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION
    ]
    assert any(item["decision"] == "sufficient" for item in assessments)


def test_missing_partial_and_conflicting_status_are_residual_gaps() -> None:
    for pair, reason in (
        (_pair("alpha", "Alpha Zoo", evidence_status=None), WebTriggerReason.RESIDUAL_MISSING),
        (
            _pair("alpha", "Alpha Zoo", availability=EvidenceAvailability.PARTIAL),
            WebTriggerReason.RESIDUAL_FAILED_OR_PARTIAL,
        ),
        (
            _pair("alpha", "Alpha Zoo", evidence_status="FUTURE_OPENING"),
            WebTriggerReason.RESIDUAL_CONFLICT,
        ),
    ):
        _, gaps, _ = _plan("Visit Alpha Zoo.", [pair])
        assert len(gaps) == 1
        assert gaps[0].information_need is OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS
        assert gaps[0].reason is reason


def test_future_maintenance_gap_merges_with_proactive_despite_operational_status() -> None:
    tasks, gaps, _ = _plan(
        "Must visit Alpha Zoo. Will Alpha Zoo be closed for maintenance on 2026-12-25?",
        [_pair("alpha", "Alpha Zoo")],
        required=("Alpha Zoo",),
    )
    assert len(gaps) == len(tasks) == 1
    assert tasks[0].priority_group == 1
    assert set(tasks[0].trigger_reasons) == {
        WebTriggerReason.EXPLICIT_DATE_QUESTION,
        WebTriggerReason.PROACTIVE_CRITICAL_CURRENT,
    }


def test_specific_open_on_phrase_suppresses_overlapping_current_status_gap() -> None:
    regular = OpeningHoursEvidence(
        applicability="regular_weekly_pattern", weekday_descriptions=["Friday 09:00-17:00"]
    )
    tasks, gaps, _ = _plan(
        "Is Alpha Zoo open on Christmas?",
        [_pair("alpha", "Alpha Zoo", availability=EvidenceAvailability.PARTIAL, hours=regular)],
    )
    assert [gap.information_need for gap in gaps] == [OfficialInformationNeed.SPECIAL_DATE_HOURS]
    assert OfficialInformationNeed.CURRENT_OPERATIONAL_STATUS not in {
        task.information_need for task in tasks
    }


def test_trip_scoped_open_question_supersedes_generic_current_status_gap() -> None:
    _, gaps, _ = _plan(
        "Is Alpha Zoo open during my trip?",
        [_pair("alpha", "Alpha Zoo", availability=EvidenceAvailability.PARTIAL)],
    )
    assert [gap.information_need for gap in gaps] == [
        OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION
    ]


def test_unnamed_cross_sentence_question_is_not_assigned_to_only_named_place() -> None:
    _, gaps, _ = _plan(
        "I want to visit Alpha Zoo. Is it open on Christmas?",
        [_pair("alpha", "Alpha Zoo")],
    )
    assert gaps == []


def test_price_range_does_not_answer_explicit_admission_question() -> None:
    candidate, place = _pair("alpha", "Alpha Zoo")
    place = place.model_copy(update={"price_range": "AUD 20.00 - AUD 50.00"})
    _, gaps, _ = _plan("What is Alpha Zoo admission price?", [(candidate, place)])
    assert [gap.information_need for gap in gaps] == [OfficialInformationNeed.ADMISSION_TICKET]
    assert gaps[0].requested_facets == (RequestedFacet.ADMISSION_FEE,)


def test_explicit_admission_facets_merge_without_requiring_every_facet() -> None:
    tasks, gaps, _ = _plan(
        "How much is Alpha Zoo admission? Do I need a ticket for Alpha Zoo?",
        [_pair("alpha", "Alpha Zoo")],
    )
    admission = [
        task for task in tasks if task.information_need is OfficialInformationNeed.ADMISSION_TICKET
    ]
    assert len(admission) == 1
    assert admission[0].requested_facets == (
        RequestedFacet.ADMISSION_FEE,
        RequestedFacet.TICKET_REQUIREMENT,
    )
    assert [gap.requested_facets for gap in gaps] == [
        (RequestedFacet.ADMISSION_FEE,),
        (RequestedFacet.TICKET_REQUIREMENT,),
    ]


def test_broad_admission_advance_purchase_and_booking_are_distinct() -> None:
    for text, expected_need, expected_facet in (
        (
            "Check Alpha Zoo admission information.",
            OfficialInformationNeed.ADMISSION_TICKET,
            RequestedFacet.GENERAL_ADMISSION_POLICY,
        ),
        (
            "Do I need to buy a ticket in advance at Alpha Zoo?",
            OfficialInformationNeed.ADMISSION_TICKET,
            RequestedFacet.ADVANCE_TICKET_PURCHASE_REQUIREMENT,
        ),
        (
            "Do I need to book Alpha Zoo?",
            OfficialInformationNeed.RESERVATION_REQUIREMENT,
            RequestedFacet.RESERVATION_REQUIREMENT,
        ),
        (
            "Do I need to book tickets in advance at Alpha Zoo?",
            OfficialInformationNeed.RESERVATION_REQUIREMENT,
            RequestedFacet.RESERVATION_REQUIREMENT,
        ),
    ):
        tasks, _, _ = _plan(text, [_pair("alpha", "Alpha Zoo")])
        residual = [task for task in tasks if task.priority_group == 2]
        assert len(residual) == 1
        assert residual[0].information_need is expected_need
        assert residual[0].requested_facets == (expected_facet,)


def test_explicit_exhibition_scopes_are_not_merged_into_whole_venue() -> None:
    tasks, _, _ = _plan(
        "Do Alpha Zoo permanent exhibitions need a ticket? "
        "Do Alpha Zoo special exhibitions need a ticket? "
        "Do I need a ticket for Alpha Zoo?",
        [_pair("alpha", "Alpha Zoo")],
    )
    admission = [
        task for task in tasks if task.information_need is OfficialInformationNeed.ADMISSION_TICKET
    ]
    assert len(admission) == 3
    assert {task.requested_subject_scope for task in admission} == {
        SubjectScope.EXHIBITION,
        SubjectScope.WHOLE_VENUE,
    }
    assert {task.requested_scope_text for task in admission} == {
        "permanent exhibitions",
        "special exhibitions",
        None,
    }


def test_reservation_tasks_keep_exhibition_scope_separate_from_venue() -> None:
    tasks, _, _ = _plan(
        "Do I need to book Alpha Zoo permanent exhibitions? Do I need to book Alpha Zoo?",
        [_pair("alpha", "Alpha Zoo")],
    )
    reservation = [
        task
        for task in tasks
        if task.information_need is OfficialInformationNeed.RESERVATION_REQUIREMENT
    ]
    assert len(reservation) == 2
    assert {task.requested_scope_text for task in reservation} == {
        "permanent exhibitions",
        None,
    }


def test_applicable_date_specific_opening_evidence_does_not_make_duplicate_gap() -> None:
    hours = OpeningHoursEvidence(
        applicability="date_specific_verified",
        next_open_time=datetime(2026, 12, 25, 9, tzinfo=UTC),
        next_close_time=datetime(2026, 12, 25, 17, tzinfo=UTC),
    )
    _, gaps, _ = _plan(
        "Is Alpha Zoo open on Christmas?", [_pair("alpha", "Alpha Zoo", hours=hours)]
    )
    assert gaps == []


def test_missing_website_and_no_override_is_observable_without_search_domain() -> None:
    candidate, place = _pair("alpha", "Alpha Zoo")
    place = place.model_copy(update={"website_uri": None})
    tasks, _, _ = _plan("Visit Alpha Zoo.", [(candidate, place)])
    assert len(tasks) == 1
    assert tasks[0].allowed_domains == ()


def test_five_priority_groups_and_unnamed_shortlist_order_have_no_extra_cap() -> None:
    pairs = [
        _pair(x, name)
        for x, name in (
            ("alpha", "Alpha Zoo"),
            ("beta", "Beta Museum"),
            ("gamma", "Gamma Park"),
            ("delta", "Delta Gallery"),
        )
    ]
    tasks, _, _ = _plan(
        "Must visit Alpha Zoo. Alpha Zoo admission? Beta Museum admission?",
        pairs,
        required=("Alpha Zoo",),
    )
    assert [(task.priority_group, task.place_id) for task in tasks] == [
        (1, "alpha"),
        (2, "beta"),
        (3, "alpha"),
        (4, "beta"),
        (5, "gamma"),
        (5, "delta"),
    ]


def test_exact_required_activity_prioritizes_place_without_raw_name_match() -> None:
    tasks, gaps, _ = _plan(
        "Plan a day at the zoo.",
        [_pair("alpha", "Alpha Zoo", evidence_status=None), _pair("beta", "Beta Museum")],
        required=("Alpha Zoo",),
    )
    assert [(task.priority_group, task.place_id) for task in tasks] == [
        (1, "alpha"),
        (3, "alpha"),
        (5, "beta"),
    ]
    assert [gap.place_id for gap in gaps] == ["alpha"]


def test_non_english_explicit_wording_does_not_create_lexical_residual_gap() -> None:
    tasks, gaps, _ = _plan("去 Alpha Zoo 要买门票吗？", [_pair("alpha", "Alpha Zoo")])
    assert gaps == []
    assert len(tasks) == 1
    assert tasks[0].information_need is OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION


def test_ordinary_weekday_wording_and_negated_include_do_not_create_extra_gaps() -> None:
    tasks, gaps, _ = _plan(
        "Do not include Alpha Zoo. Is Alpha Zoo open on weekdays?",
        [_pair("alpha", "Alpha Zoo")],
    )
    assert gaps == []
    assert len(tasks) == 1
    assert tasks[0].priority_group == 4
