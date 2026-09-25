"""Synthetic candidate evidence for current acquisition and RAG unit tests."""

from datetime import UTC, date, datetime
from types import SimpleNamespace

from backend.app.evidence.models import EvidenceAvailability, PlaceCandidate, PlaceEvidence
from backend.app.evidence.selection_models import PlaceSelectionInput, QueryIntentHit
from backend.app.policies.interpreted_requirements import (
    canonicalize_requirements,
)
from backend.app.schemas.interpreted_requirements import (
    InterpretationDraft,
    SemanticDraft,
    SourceQuote,
)
from backend.app.schemas.request import PlanningRequest


def candidate_fixture(n=4, r=2):
    text_unit = (
        "Distinctive cultural places with different architectural and historical character. "
    )
    texts = [(f"Preference {i}: " + text_unit * 15)[:100] for i in range(r)]
    raw = "\n".join(texts) or "Plan a trip to Sydney."
    draft = InterpretationDraft(
        # Synthetic current gate assessment for this offline fixture.
        preference_input_assessment={
            "input_disposition": "VALID", "safety_disposition": "CLEAR", "issues": []
        },
        semantic_requirements=tuple(
            SemanticDraft(
                local_key=f"r{i}",
                normalized_text=t,
                kind="preference",
                polarity="favor",
                strength="medium",
                scope="individual_poi",
                subject_target={"kind": "party"},
                source_refs=(SourceQuote(quote=t, occurrence=0),),
            )
            for i, t in enumerate(texts)
        ),
        named_places=(),
        requested_place_information=(),
        transport_preference=None,
        subjects=(),
        discovery_intents=(),
        experience_evidence_requests=(),
        extraction_issues=(),
        overflow=False,
    )
    contract = canonicalize_requirements(
        draft,
        PlanningRequest(
            destination="Sydney",
            start_date=date(2026, 9, 21),
            end_date=date(2026, 9, 23),
            traveler_count=2,
            budget={"amount": "1800", "currency": "AUD"},
            additional_preferences=raw,
        ),
    )
    places = []
    for i in range(n):
        pid = f"place_{i:02d}"
        name = f"Cultural place {i}"
        candidate = PlaceCandidate(
            place_id=pid,
            name=name,
            latitude=-33.86,
            longitude=151.2,
            business_status="OPERATIONAL",
            source_query="synthetic discovery",
            category="museum",
            provider_rank=i,
        )
        evidence = PlaceEvidence(
            place_id=pid,
            name=name,
            latitude=-33.86,
            longitude=151.2,
            business_status="OPERATIONAL",
            rating=4.0,
            availability=EvidenceAvailability.AVAILABLE,
            retrieved_at=datetime(2026, 9, 19, tzinfo=UTC),
            source_ref=f"fixture:{pid}",
        )
        places.append(
            PlaceSelectionInput(
                candidate=candidate,
                structured_evidence=evidence,
                query_hits=[
                    QueryIntentHit(
                        intent_id="d",
                        source_query="synthetic",
                        provider_rank=i,
                        actual_result_count=n,
                    )
                ],
                rating=4.0,
                rating_state="available",
            )
        )
    return SimpleNamespace(requirements=contract, canonical_places=tuple(places))
