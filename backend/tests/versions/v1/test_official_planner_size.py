"""Measure one deterministic configured upper-envelope V1 planner input."""

from datetime import UTC, date, datetime, timedelta

from backend.app.evidence.models import (
    EvidenceAvailability,
    PlaceCandidate,
    PlaceEvidence,
    WeatherDayEvidence,
    WeatherEvidence,
)
from backend.app.evidence.official_models import (
    OfficialClaimKind,
    OfficialCurrentEvidence,
    OfficialGapOutcome,
    OfficialGapStatus,
    SourceKind,
    SubjectScope,
    TemporalBasis,
)
from backend.app.evidence.web_models import (
    OfficialInformationNeed,
    WebEvidenceTask,
    WebTaskOutcome,
    WebTaskStatus,
    WebTriggerReason,
)
from backend.app.policies.official_evidence_resolver import resolve_effective_evidence
from backend.app.schemas.request import TravelRequirements
from backend.app.services.official_web_integration import OfficialWebIntegrationResult
from backend.app.versions.v1.official_planner import build_official_planner_evidence
from backend.app.versions.v1.official_web import OfficialWebProjection
from backend.app.versions.v1.prompts import build_itinerary_generation_prompt
from backend.tests.request_fixtures import make_request
from tools.diagnostics.itinerary_fixtures import _places, _routes

START = date(2026, 9, 12)
END = START + timedelta(days=9)
RETRIEVED = datetime(2026, 9, 11, tzinfo=UTC)








def _official_result(
    candidates: list[PlaceCandidate], places: list[PlaceEvidence]
) -> OfficialWebIntegrationResult:
    tasks = []
    acquired = []
    gaps = []
    accepted = []
    effective = []
    for index, place in enumerate(places):
        place_official = []
        task = WebEvidenceTask(
            task_id=f"task-{index}",
            place_id=place.place_id,
            place_name=place.name,
            information_need=OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,
            applicable_start_date=START,
            applicable_end_date=END,
            allowed_domains=(f"museum{index:02d}.example.org",),
            trigger_reasons=(WebTriggerReason.PROACTIVE_CRITICAL_CURRENT,),
            priority_group=5,
            shortlist_index=index,
        )
        tasks.append(task)
        acquired.append(
            WebTaskOutcome(
                task=task,
                status=(
                    WebTaskStatus.COMPLETED_WITH_SOURCES
                    if index < 6
                    else WebTaskStatus.BUDGET_NOT_ATTEMPTED
                ),
            )
        )
        if index < 6:
            for offset in range(6):
                day = START + timedelta(days=offset)
                place_official.append(
                    OfficialCurrentEvidence(
                        place_id=place.place_id,
                        place_name=place.name,
                        information_need=task.information_need,
                        claim_kind=OfficialClaimKind.MAINTENANCE_CLOSURE,
                        value_text=f"Closed for maintenance on {day.isoformat()}",
                        source_kind=SourceKind.FETCHED_HTML,
                        source_url=f"https://museum{index:02d}.example.org/notices/{day}",
                        supporting_excerpt=f"{place.name} closed for maintenance on {day}.",
                        subject_scope=SubjectScope.WHOLE_VENUE,
                        subject_text=place.name,
                        predicate_text="closed for maintenance",
                        temporal_basis=TemporalBasis.EXPLICIT_DATE_OR_RANGE,
                        applicable_start_date=day,
                        applicable_end_date=day,
                        date_text=day.isoformat(),
                        authority_basis="places_first_party_website",
                        retrieved_at=RETRIEVED,
                        source_ref=f"official:{place.place_id}:{offset}",
                    )
                )
            accepted.extend(place_official)
        gaps.append(
            OfficialGapOutcome(
                task_id=task.task_id,
                place_id=place.place_id,
                information_need=task.information_need,
                status=(OfficialGapStatus.PARTIAL if index < 6 else OfficialGapStatus.UNAVAILABLE),
                accepted_evidence=tuple(place_official),
                meaningful_evidence=tuple(place_official),
                reason_codes=() if index < 6 else ("budget_not_attempted",),
                extraction_calls=2 if index < 6 else 0,
                page_target_attempts=1 if index < 6 else 0,
                bounded_check_completed=index < 6,
            )
        )
        effective.append(
            resolve_effective_evidence(
                place,
                tuple(place_official),
                trip_start=START,
                trip_end=END,
                needs=(OfficialInformationNeed.DATE_SPECIFIC_OPERATIONAL_EXCEPTION,),
            )
        )
    return OfficialWebIntegrationResult(
        projection=OfficialWebProjection(
            candidates=candidates,
            places=[item.model_copy(update={"rating": None}) for item in places],
            named_place_ids=frozenset(),
            must_visit_place_ids=frozenset(),
        ),
        tasks=tuple(tasks),
        information_gaps=(),
        acquisition_outcomes=tuple(acquired),
        gap_outcomes=tuple(gaps),
        accepted_evidence=tuple(accepted),
        effective_places=tuple(effective),
        facet_statuses_by_task=(),
    )


def test_configured_upper_envelope_planner_prompt_size() -> None:
    candidates, places = _places()
    ids = [item.place_id for item in places]
    official = build_official_planner_evidence(_official_result(candidates, places))
    weather = WeatherEvidence(
        destination="Sydney",
        latitude=-33.8,
        longitude=151.2,
        availability=EvidenceAvailability.AVAILABLE,
        days=[
            WeatherDayEvidence(date=START + timedelta(days=offset), condition="CLEAR")
            for offset in range(10)
        ],
        retrieved_at=RETRIEVED,
        source_ref="google_weather:sydney",
    )
    request = make_request(
        additional_preferences="Plan ten days in Sydney with these selected museums."
    )
    requirements = TravelRequirements(destination="Sydney", start_date=START, end_date=END)
    routes = _routes(ids)
    base_prompt = build_itinerary_generation_prompt(
        request,
        requirements,
        START - timedelta(days=1),
        places=places,
        weather=weather,
        routes=routes,
    )
    prompt = build_itinerary_generation_prompt(
        request,
        requirements,
        START - timedelta(days=1),
        places=places,
        weather=weather,
        routes=routes,
        official_evidence=official,
    )
    fact_count = sum(len(item["accepted_effective_facts"]) for item in official)
    size = len(prompt.encode("utf-8"))
    base_size = len(base_prompt.encode("utf-8"))
    print(
        f"phase3_offline_prompt_bytes={size} base_prompt_bytes={base_size} "
        f"official_increment_bytes={size - base_size} official_facts={fact_count}"
    )
    assert len(places) == 16
    assert fact_count == 36
    assert size > 0
    assert '"rating"' not in prompt
    assert "supporting_excerpt" not in prompt
