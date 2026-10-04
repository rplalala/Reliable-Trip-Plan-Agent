"""Small synthetic adapter fixtures; they are not independently acquired place facts."""

from tools.validation.short_reference_smoke import SmokeCase

PLACE_A = "ChIJsynthetic-museum-A-0123456789abcdef"
PLACE_B = "ChIJsynthetic-museum-B-0123456789abcdef"
ACTIVITY_A = "activity-first-0123456789abcdef0123456789abcdef"
ACTIVITY_B = "activity-second-0123456789abcdef0123456789abcdef"
TARGET = "finding-replace-0123456789abcdef0123456789abcdef"
DAY = "2026-10-07"


def official_case():
    from backend.app.evidence.official_models import EvidenceSourceBlock
    from backend.app.evidence.web_models import WebEvidenceTask

    baseline = repair_case().payload["preparation"]["ledger"][0]["place"]
    task = WebEvidenceTask(
        task_id="task-official-0123456789abcdef0123456789abcdef",
        place_id=PLACE_A,
        place_name="Synthetic Museum A",
        information_need="admission_ticket",
        applicable_start_date=DAY,
        applicable_end_date=DAY,
        allowed_domains=["museum.example.org"],
        trigger_reasons=["residual_missing"],
        priority_group=2,
        shortlist_index=0,
    )
    source = EvidenceSourceBlock(
        task_id=task.task_id,
        source_kind="native_snippet",
        source_url="https://museum.example.org/admission",
        text="Synthetic Museum A offers free general admission.",
    )
    return SmokeCase(
        "official_reasoning",
        {
            "task": task.model_dump(mode="json"),
            "source": source.model_dump(mode="json"),
            "baseline": baseline,
        },
    )


def introduction_case():
    original = repair_case().payload["original"]
    original["days"][0]["activities"][1].update(
        activity_kind="main_poi",
        source_place_id=PLACE_B,
        place_name="Synthetic Museum B",
        title="Second museum visit",
    )
    return SmokeCase("product_introduction", {"original": original})


def repair_case():
    from datetime import datetime

    from backend.app.evidence.models import PlaceEvidence
    from backend.app.schemas.itinerary import Activity, Itinerary, ItineraryDay
    from backend.app.versions.v3.repair_models import (
        ActivityPermission,
        CandidateDecision,
        CandidatePreparation,
        RepairCandidate,
        RepairScope,
    )

    places = [
        PlaceEvidence(
            place_id=pid,
            name=name,
            latitude=37.5,
            longitude=127.0,
            formatted_address="Seoul",
            availability="available",
            retrieved_at=datetime.fromisoformat("2026-10-05T00:00:00+00:00"),
            source_ref="synthetic_fixture",
        )
        for pid, name in [(PLACE_A, "Synthetic Museum A"), (PLACE_B, "Synthetic Museum B")]
    ]
    original = Itinerary(
        destination="Seoul",
        start_date=DAY,
        end_date=DAY,
        days=[
            ItineraryDay(
                date=DAY,
                activities=[
                    Activity(
                        activity_kind="main_poi",
                        activity_id=ACTIVITY_A,
                        title="Museum visit",
                        place_name="Synthetic Museum A",
                        source_place_id=PLACE_A,
                        start_time=f"{DAY}T09:00:00+09:00",
                        end_time=f"{DAY}T10:00:00+09:00",
                    ),
                    Activity(
                        activity_kind="generic_activity",
                        activity_id=ACTIVITY_B,
                        title="Lunch",
                        start_time=f"{DAY}T11:00:00+09:00",
                        end_time=f"{DAY}T12:00:00+09:00",
                    ),
                ],
            )
        ],
    )
    scope = RepairScope(
        dates=[DAY],
        target_ids=[TARGET],
        permissions=[ActivityPermission(activity_id=ACTIVITY_A, operations={"replace"})],
    )
    candidates = [
        RepairCandidate(place=p, origin="original_supply", provenance=["synthetic"]) for p in places
    ]
    preparation = CandidatePreparation(
        ledger=candidates,
        input_candidates=candidates,
        authorizations=[
            CandidateDecision(
                place_id=PLACE_B,
                target_id=TARGET,
                date=DAY,
                operation="replace",
                disposition="eligible",
                reason="Synthetic authorized replacement",
            )
        ],
    )
    return SmokeCase(
        "v3_repair",
        {
            "request": "Replace the first museum with Synthetic Museum B at the original times. "
            "Preserve lunch. Report one proposed target disposition. This is synthetic data.",
            "original": original.model_dump(mode="json"),
            "scope": scope.model_dump(mode="json"),
            "preparation": preparation.model_dump(mode="json"),
            "time_protection": {"lineage": {ACTIVITY_A: ACTIVITY_A, ACTIVITY_B: ACTIVITY_B}},
        },
    )


def prepared_cases(judge_input=None):
    cases = [
        SmokeCase(
            "shared_primary",
            {
                "places": [
                    {
                        "place_id": PLACE_A,
                        "name": "Synthetic Museum A",
                        "formatted_address": "Seoul",
                    },
                    {
                        "place_id": PLACE_B,
                        "name": "Synthetic Museum B",
                        "formatted_address": "Seoul",
                    },
                ],
                "routes": {
                    "directed_facts": [
                        {
                            "origin": PLACE_A,
                            "destination": PLACE_B,
                            "mode": "WALK",
                            "duration_seconds": 600,
                        }
                    ]
                },
                "supply": {
                    "required_canonical_ids": [PLACE_A, PLACE_B],
                    "optional_canonical_ids": [],
                },
            },
        ),
        SmokeCase(
            "review_profile",
            {
                "place_id": PLACE_A,
                "reviews": [
                    {"review_id": "review_1", "text": "Quiet galleries with very few visitors."},
                    {"review_id": "review_2", "text": "Few crowds and a short visit."},
                ],
            },
        ),
        repair_case(),
        official_case(),
        introduction_case(),
    ]
    if judge_input is not None:
        cases.append(SmokeCase("v0_identity", judge_input))
    return cases


def primary_prompt(payload):
    import json

    return (
        "This is a synthetic adapter regression fixture, not a real trip request. "
        "Plan one day in Seoul on 2026-10-07. Include each of the two supplied museums once "
        "as main_poi; schedule one 09:00-10:00 and the other 11:00-12:00, UTC +09:00. "
        "Use supplied place IDs. Leave unknown cost null and note unknown operating hours.\n"
        "<travel_requirements>\n{}\n</travel_requirements>\n<external_evidence>\n"
        + json.dumps({k: v for k, v in payload.items() if k != "supply"})
        + "\n</external_evidence>\nPlanning candidate supply contract:\n"
        + json.dumps(payload["supply"])
    )


def primary_output():
    activities = []
    for i, (alias, name) in enumerate(
        [("p01", "Synthetic Museum A"), ("p02", "Synthetic Museum B")]
    ):
        activities.append(
            {
                "activity_kind": "main_poi",
                "activity_id": f"generated-visit-{i + 1}",
                "title": f"Visit {name}",
                "place_name": name,
                "source_place_id": alias,
                "location": "Seoul",
                "estimated_cost": None,
                "notes": "Operating hours unverified.",
                "start_time": {
                    "date": DAY,
                    "time": f"{9 + i * 2:02}:00:00",
                    "utc_offset": "+09:00",
                },
                "end_time": {"date": DAY, "time": f"{10 + i * 2:02}:00:00", "utc_offset": "+09:00"},
            }
        )
    return {
        "output_version": "itinerary_2",
        "destination": "Seoul",
        "start_date": DAY,
        "end_date": DAY,
        "days": [{"date": DAY, "activities": activities}],
    }


def mock_output(case):
    if case.name == "shared_primary":
        return primary_output()
    if case.name == "review_profile":
        return {
            "place_id": "p01",
            "summary": "Quiet galleries with few crowds.",
            "summary_review_refs": ["review_1", "review_2"],
            "signals": [],
            "review_count_used": 2,
        }
    if case.name == "v3_repair":
        return {
            "edits": [
                {
                    "operation": "replace",
                    "activity_id": "a01",
                    "place_id": "p02",
                    "date": DAY,
                    "start_time": f"{DAY}T09:00:00+09:00",
                    "end_time": f"{DAY}T10:00:00+09:00",
                }
            ],
            "target_dispositions": [
                {
                    "target_id": "t01",
                    "disposition": "proposed",
                    "reason": "Authorized fixture replacement.",
                }
            ],
        }
    if case.name == "official_reasoning":
        return {
            "assessments": [
                {
                    "relevant": True,
                    "supports_information_need": True,
                    "relevant_to_requested_dates": "uncertain",
                    "proposed_relation_to_baseline": None,
                    "confidence": "medium",
                    "brief_rationale": "The supplied synthetic source states admission.",
                    "candidate": {
                        "source_key": "s01",
                        "place_id": "p01",
                        "place_name": "Synthetic Museum A",
                        "information_need": "admission_ticket",
                        "claim_kind": "free_general_admission",
                        "value_text": "free general admission",
                        "source_kind": "native_snippet",
                        "source_url": "https://museum.example.org/admission",
                        "final_url": None,
                        "supporting_excerpt": "Synthetic Museum A offers free general admission.",
                        "subject_scope": "whole_venue",
                        "subject_text": "Synthetic Museum A",
                        "predicate_text": "offers free general admission",
                        "scope_text": None,
                        "temporal_basis": "current_general_policy",
                        "date_text": None,
                        "applicable_start_date": None,
                        "applicable_end_date": None,
                        "time_text": None,
                        "schedule_scope": None,
                        "schedule_text": None,
                        "opens_at": None,
                        "closes_at": None,
                        "amount_text": None,
                        "amount": None,
                        "currency": None,
                        "updated_at_text": None,
                        "updated_at": None,
                    },
                }
            ]
        }
    if case.name == "product_introduction":
        return {
            "introductions": [
                {"activity_id": "a01", "text": "Explore the first museum."},
                {"activity_id": "a02", "text": "Explore the second museum."},
            ]
        }
    if case.name == "v0_identity":
        from backend.evaluation.identity_assistance import IdentityAssistancePacket

        packet = IdentityAssistancePacket(case.payload["cases"])
        return {
            "decisions": [
                {
                    "reference_id": row["reference_id"],
                    "decision": "match" if row["candidates"] else "unknown",
                    "candidate_id": row["candidates"][0]["place_id"] if row["candidates"] else None,
                    "rationale": "Synthetic preflight response; not a semantic assessment.",
                    "evidence_fields": ["display_name"] if row["candidates"] else [],
                }
                for row in packet.payload["cases"]
            ]
        }
    raise ValueError("Unknown mock case")
