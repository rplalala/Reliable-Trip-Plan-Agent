"""Offline primary-payload sizing using schema-validated, explicitly synthetic fixtures."""

import argparse
import hashlib
import json
from datetime import date, timedelta
from itertools import combinations
from pathlib import Path
from types import SimpleNamespace

from backend.app.evidence.experience_models import ExperienceProfile, ExperienceSignal
from backend.app.evidence.models import RouteEvidenceBundle, WeatherEvidence
from backend.app.evidence.official_models import OfficialCurrentEvidence, OfficialGapOutcome
from backend.app.evidence.web_models import WebEvidenceTask, WebTaskOutcome
from backend.app.policies.official_evidence_resolver import resolve_effective_evidence
from backend.app.policies.planning_supply import profile_relations
from backend.app.policies.poi_capacity import quality_capacities
from backend.app.policies.trip_dates import create_trip_date_window
from backend.app.runtime.config_loader import load_runtime_config_file, runtime_config_snapshot
from backend.app.runtime.token_counting import count_tokens
from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements
from backend.app.schemas.request import PlanningRequest
from backend.app.services.generation_resources import GenerationResourceError, check_primary_input
from backend.app.services.official_web_integration import OfficialWebIntegrationResult
from backend.app.services.planning_supply_pipeline import planner_supply_projection
from backend.app.versions.v1.official_planner import build_official_planner_evidence
from backend.app.versions.v1.official_web import OfficialWebProjection
from backend.app.versions.v1.prompts import (
    ITINERARY_GENERATION_SYSTEM_PROMPT,
    build_itinerary_generation_prompt,
)
from tools.diagnostics.itinerary_fixtures import (
    RETRIEVED,
    _places,
    _route_element,
    _routes,
)


def fixtures(days, count, long_text=False):
    """Local fabricated evidence only; no provider clients or acquisition."""
    start = date(2026, 9, 12)
    end = start + timedelta(days=days - 1)
    candidates, places = _places(count)
    candidates, places = candidates[:count], places[:count]
    ids = [p.place_id for p in places]
    n = 24 if long_text else 5
    sentence = "I prefer light walking and cultural places with varied architectural character."
    raw = (sentence + " ") * (300 if long_text else 1)
    request = PlanningRequest(
        destination="Synthetic fixture city",
        start_date=start,
        end_date=end,
        traveler_count=3,
        budget={"amount": 1800, "currency": "AUD"},
        additional_preferences=raw,
    )
    quote = {"quote": sentence, "occurrence": 0, "start": 0, "end": len(sentence)}
    dims = [
        "crowding",
        "walking_intensity",
        "accessibility",
        "family_friendliness",
        "visit_duration",
    ]
    vals = ["LOW", "LIGHT", "ACCESSIBLE", "FAMILY_FRIENDLY", "SHORT"]
    semantics = [
        dict(
            requirement_id=f"semantic_{i + 1}",
            normalized_text=(f"Fixture preference {i + 1}: " + sentence * 4)[
                : 250 if long_text else 160
            ],
            kind="preference",
            polarity="favor",
            strength="medium",
            scope="selected_poi_set",
            subject_refs=["party"],
            source_refs=[quote],
        )
        for i in range(n)
    ]
    contract = InterpretedTripRequirements(
        request_sha256=hashlib.sha256(raw.encode()).hexdigest(),
        structured_input_sha256=request.structured_hash(),
        interpretation_origin="model",
        requirements=request.trip_requirements(),
        named_places=(),
        requested_place_information=(),
        transport_preference=None,
        semantic_requirements=semantics,
        subjects=(),
        discovery_intents=(),
        experience_evidence_requests=[
            dict(
                requirement_id=f"semantic_{i + 1}",
                dimension=dims[i % 5],
                preferred_values=[vals[i % 5]],
            )
            for i in range(n)
        ],
        extraction_issues=(),
    )
    capacity = quality_capacities(start, end, create_trip_date_window(start))
    assert capacity.k_final == count and capacity.review_pool_cap in (6, 8)
    profiles = {
        pid: ExperienceProfile(
            place_id=pid,
            availability="available",
            signals=tuple(
                ExperienceSignal(
                    dimension=d, value=v, review_refs=(f"{pid}:review-1",), confidence="medium"
                )
                for d, v in zip(dims, vals, strict=True)
            ),
            review_count_used=1,
        )
        for pid in ids[: capacity.review_pool_cap]
    }
    policy = SimpleNamespace(
        required_canonical_ids=(),
        optional_canonical_ids=tuple(ids),
        selected_place_ids=tuple(ids),
        shortfall=0,
        profile_relations={pid: profile_relations(contract, profiles, pid) for pid in ids},
    )
    projection = planner_supply_projection(
        SimpleNamespace(policy_result=policy, semantic_assessments=()), contract
    )
    routes = _routes(ids)
    from backend.app.services.evidence_acquisition import V1EvidenceAcquisitionService

    grouped = {}
    for a, b in list(combinations(ids, 2))[:16]:
        grouped.setdefault(a, []).append(b)
    alternatives = []
    for index, (a, targets) in enumerate(grouped.items()):
        direct = routes.alternatives[0].model_copy(
            update={
                "elements": [_route_element(a, b) for b in targets],
                "source_ref": f"fixture:alternative:{index}",
            }
        )
        alternatives.append(V1EvidenceAcquisitionService._with_mirrored_reverse_estimates(direct))
    routes = RouteEvidenceBundle.model_validate(
        {**routes.model_dump(), "alternatives": [r.model_dump() for r in alternatives]}
    )
    assert (
        len(routes.baseline.elements) == count * count
        and sum(len(r.elements) for r in alternatives) == 32
    )
    weather = WeatherEvidence(
        destination=request.destination,
        latitude=-33.8,
        longitude=151.2,
        availability="available",
        days=[dict(date=start + timedelta(days=i), condition="CLEAR") for i in range(days)],
        retrieved_at=RETRIEVED,
        source_ref="fixture:weather",
    )
    tasks, acquired, gaps, accepted, effective = [], [], [], [], []
    for i, p in enumerate(places):
        facts = []
        if i < 8:
            task = WebEvidenceTask(
                task_id=f"fixture-task-{i}",
                place_id=p.place_id,
                place_name=p.name,
                information_need="date_specific_operational_exception",
                applicable_start_date=start,
                applicable_end_date=end,
                allowed_domains=(f"museum{i:02d}.example.org",),
                trigger_reasons=("proactive_critical_current",),
                priority_group=5,
                shortlist_index=i,
            )
            tasks.append(task)
            acquired.append(WebTaskOutcome(task=task, status="completed_with_sources"))
            for offset in range(min(6, days)):
                day = start + timedelta(days=offset)
                text = f"Closed for maintenance on {day}."
                if long_text:
                    text += " This synthetic notice describes a bounded dated closure." * 8
                facts.append(
                    OfficialCurrentEvidence(
                        place_id=p.place_id,
                        place_name=p.name,
                        information_need=task.information_need,
                        claim_kind="maintenance_closure",
                        value_text=text,
                        source_kind="fetched_html",
                        source_url=f"https://museum{i:02d}.example.org/notices",
                        supporting_excerpt=text,
                        subject_scope="whole_venue",
                        subject_text=p.name,
                        predicate_text="closed for maintenance",
                        temporal_basis="explicit_date_or_range",
                        applicable_start_date=day,
                        applicable_end_date=day,
                        date_text=str(day),
                        authority_basis="places_first_party_website",
                        retrieved_at=RETRIEVED,
                        source_ref=f"fixture:official:{i}:{offset}",
                    )
                )
            gaps.append(
                OfficialGapOutcome(
                    task_id=task.task_id,
                    place_id=p.place_id,
                    information_need=task.information_need,
                    status="partial",
                    accepted_evidence=tuple(facts),
                    meaningful_evidence=tuple(facts),
                    extraction_calls=(len(facts) + 2) // 3,
                    page_target_attempts=1,
                    bounded_check_completed=True,
                )
            )
        accepted.extend(facts)
        effective.append(
            resolve_effective_evidence(
                p,
                tuple(facts),
                trip_start=start,
                trip_end=end,
                needs=("date_specific_operational_exception",) if facts else (),
            )
        )
    result = OfficialWebIntegrationResult(
        projection=OfficialWebProjection(
            candidates=candidates,
            places=places,
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
    official = build_official_planner_evidence(result)
    prompt = build_itinerary_generation_prompt(
        request,
        contract.requirements,
        start,
        places=places,
        weather=weather,
        routes=routes,
        official_evidence=official,
    )
    prompt += "\nPlanning candidate supply contract:\n" + json.dumps(projection)
    return prompt, dict(
        synthetic=True,
        days=days,
        K=count,
        P=len(profiles),
        baseline_elements=count * count,
        alternative_billable_elements=16,
        alternative_mirrored_elements=16,
        alternative_requests=len(alternatives),
        web_tasks=len(tasks),
        web_pages=8,
        accepted_web_facts=len(accepted),
        semantic_requirements=n,
        preference_characters=len(raw),
        preference_tokens=count_tokens(raw),
    )


def measure(system, user, config, metadata):
    from backend.app.llm.azure_foundry.dto import FoundryPrimaryItineraryDTO

    parts = {
        "system_tokens": count_tokens(system),
        "user_tokens": count_tokens(user),
        "schema_tokens": count_tokens(json.dumps(FoundryPrimaryItineraryDTO.model_json_schema())),
        "framing_tokens": config.framing_tokens,
    }
    parts["total_tokens"] = sum(parts.values())
    parts["remaining"] = config.input_tokens - parts["total_tokens"]
    parts["overflow"] = parts["remaining"] < 0
    sections = {}
    for tag in (
        "user_request",
        "travel_requirements",
        "requirement_conflicts",
        "external_evidence",
        "official_current_evidence",
    ):
        value = user.split(f"<{tag}>", 1)[1].split(f"</{tag}>", 1)[0]
        sections[tag] = count_tokens(value)
        if tag == "external_evidence":
            for key, item in json.loads(value).items():
                sections[key] = count_tokens(json.dumps(item, indent=2, ensure_ascii=True))
    if "Planning candidate supply contract:\n" in user:
        sections["supply_projection"] = count_tokens(
            user.split("Planning candidate supply contract:\n", 1)[1]
        )
    try:
        check_primary_input(system, user, config)
    except GenerationResourceError:
        assert parts["overflow"]
    return {
        **metadata,
        **parts,
        "sections_non_additive": sections,
        "prompt_sha256": hashlib.sha256((system + user).encode()).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = load_runtime_config_file(Path("config/runtime.yaml"))
    raw = json.loads(args.capture.read_text(encoding="utf-8"))
    rows = [
        measure(
            raw["system_prompt"],
            raw["user_prompt"],
            config.main_generation,
            {
                "synthetic": False,
                "K": 8,
                "capture": str(args.capture),
                "capture_sha256": hashlib.sha256(args.capture.read_bytes()).hexdigest(),
            },
        )
    ]
    for days, k, long in [(3, 12, False), (10, 20, False), (10, 20, True)]:
        user, metadata = fixtures(days, k, long)
        rows.append(
            measure(ITINERARY_GENERATION_SYSTEM_PROMPT, user, config.main_generation, metadata)
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "config_hash": runtime_config_snapshot(config)[1],
        "method": (
            "Installed offline o200k tokenizer; current prompt and DTO serializer; "
            "section counts are diagnostic, not additive. Synthetic evidence is not "
            "Tokyo evidence or a universal maximum."
        ),
        "measurements": rows,
    }
    args.output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
