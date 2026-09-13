"""Injected, source-only EvidenceReasoner contract and prompt checks."""

import asyncio
import json
from datetime import UTC, date, datetime

import pytest

from backend.app.evidence.models import EvidenceAvailability, PlaceEvidence
from backend.app.evidence.official_models import EvidenceSourceBlock, SourceKind
from backend.app.evidence.web_models import (
    OfficialInformationNeed,
    WebEvidenceTask,
    WebTriggerReason,
)
from backend.app.integrations.azure_foundry.evidence_reasoner import (
    OUTPUT_SCHEMA,
    SYSTEM_PROMPT,
    AzureFoundryEvidenceReasoner,
)
from backend.app.runtime.config_loader import load_runtime_config

URL = "https://alpha.example.org/admission"
TEXT = "Alpha Zoo offers free general admission."


class FakeResponses:
    def __init__(self, assessments):
        self.calls = []
        self.assessments = assessments

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        return {"output_text": json.dumps({"assessments": self.assessments})}


def _place():
    return PlaceEvidence(
        place_id="alpha",
        name="Alpha Zoo",
        latitude=-33.8,
        longitude=151.2,
        business_status="OPERATIONAL",
        availability=EvidenceAvailability.AVAILABLE,
        website_uri="https://alpha.example.org",
        source_ref="google_places:alpha",
        retrieved_at=datetime(2026, 12, 20, tzinfo=UTC),
    )


def _task(need=OfficialInformationNeed.ADMISSION_TICKET):
    return WebEvidenceTask(
        task_id="task-1",
        place_id="alpha",
        place_name="Alpha Zoo",
        information_need=need,
        applicable_start_date=date(2026, 12, 25),
        applicable_end_date=date(2026, 12, 25),
        allowed_domains=("alpha.example.org",),
        trigger_reasons=(WebTriggerReason.RESIDUAL_MISSING,),
        priority_group=2,
        shortlist_index=0,
    )


def _source(text=TEXT):
    return EvidenceSourceBlock(
        task_id="task-1",
        source_kind=SourceKind.NATIVE_SNIPPET,
        source_url=URL,
        text=text,
    )


def _assessment(source=None, **changes):
    source = source or _source()
    data = {
        "relevant": True,
        "supports_information_need": True,
        "relevant_to_requested_dates": "uncertain",
        "proposed_relation_to_baseline": None,
        "confidence": "medium",
        "brief_rationale": "Source states the venue policy.",
        "candidate": {
            "source_key": source.source_key,
            "place_id": "alpha",
            "place_name": "Alpha Zoo",
            "information_need": "admission_ticket",
            "claim_kind": "free_general_admission",
            "value_text": "free general admission",
            "source_kind": "native_snippet",
            "source_url": URL,
            "final_url": None,
            "supporting_excerpt": source.text,
            "subject_scope": "whole_venue",
            "subject_text": "Alpha Zoo",
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
    data.update(changes)
    return data


def _reasoner(fake):
    return AzureFoundryEvidenceReasoner(
        endpoint="https://example.test/openai/v1",
        deployment="gpt-5.6-luna",
        api_key="unused-test-value",
        config=load_runtime_config().web_evidence,
        responses_client=fake,
    )


def test_reasoner_separates_query_context_and_source_evidence_without_tools() -> None:
    source = _source()
    fake = FakeResponses([_assessment(source)])
    result = asyncio.run(_reasoner(fake).reason(_task(), (source,), _place()))
    assert len(result) == 1 and result[0].candidate is not None
    call = fake.calls[0]
    assert "tools" not in call
    assert call["model"] == "gpt-5.6-luna"
    assert call["max_output_tokens"] == 1200
    assert call["text"]["format"]["type"] == "json_schema"
    payload = json.loads(call["input"][1]["content"])
    assert payload["QUERY_CONTEXT_NOT_EVIDENCE"]["requested_start_date"] == "2026-12-25"
    assert payload["SOURCE_EVIDENCE"][0]["source_key"] == source.source_key
    assert "2026-12-25" not in payload["SOURCE_EVIDENCE"][0]["text"]
    assert "QUERY CONTEXT" in SYSTEM_PROMPT and "SOURCE EVIDENCE" in SYSTEM_PROMPT
    assert "not required" in SYSTEM_PROMPT and "FREE general entry" in SYSTEM_PROMPT
    assert "ticket-price question" in SYSTEM_PROMPT
    assert "plausible implication" in SYSTEM_PROMPT
    assert "ticket_not_required" in SYSTEM_PROMPT
    assert "reservation_not_required" in SYSTEM_PROMPT


def test_source_faithful_semantic_proposal_preserves_undated_general_policy() -> None:
    source = _source("Alpha Zoo entry is complimentary.")
    candidate = _assessment(source)["candidate"] | {
        "value_text": "complimentary",
        "supporting_excerpt": source.text,
        "predicate_text": "entry is complimentary",
    }
    result = asyncio.run(
        _reasoner(FakeResponses([_assessment(source, candidate=candidate)])).reason(
            _task(), (source,), _place()
        )
    )
    assert result[0].candidate.value_text == "complimentary"
    assert result[0].candidate.applicable_start_date is None


def test_source_span_contract_and_long_audit_text_remain_parseable() -> None:
    source = _source("Alpha Zoo has FREE general entry.")
    candidate = _assessment(source)["candidate"] | {
        "supporting_excerpt": source.text,
        "predicate_text": "has",
        "value_text": "FREE general entry",
        "scope_text": "general entry",
    }
    assessment = _assessment(
        source,
        candidate=candidate,
        brief_rationale="A" * 300,
        proposed_relation_to_baseline="B" * 140,
    )
    result = asyncio.run(
        _reasoner(FakeResponses([assessment])).reason(_task(), (source,), _place())
    )
    assert len(result) == 1
    assert result[0].candidate is not None
    assert result[0].candidate.predicate_text == "has"
    assert result[0].candidate.value_text == "FREE general entry"
    assert result[0].brief_rationale == "A" * 300
    assert result[0].proposed_relation_to_baseline == "B" * 140
    properties = OUTPUT_SCHEMA["properties"]["assessments"]["items"]["properties"]
    candidate_fields = properties["candidate"]["anyOf"][0]["properties"]
    for name in (
        "supporting_excerpt",
        "subject_text",
        "predicate_text",
        "value_text",
        "scope_text",
    ):
        assert candidate_fields[name]["description"]
        assert name in SYSTEM_PROMPT
    assert "need not" in candidate_fields["predicate_text"]["description"]


def test_related_direct_claim_can_remain_an_advisory_non_answer() -> None:
    source = _source("Alpha Zoo tickets are not required.")
    candidate = _assessment(source)["candidate"] | {
        "claim_kind": "ticket_not_required",
        "value_text": "tickets are not required",
        "predicate_text": "tickets are not required",
        "supporting_excerpt": source.text,
    }
    fake = FakeResponses(
        [
            _assessment(
                source,
                supports_information_need=False,
                candidate=candidate,
            )
        ]
    )
    result = asyncio.run(_reasoner(fake).reason(_task(), (source,), _place()))
    assert result[0].candidate is not None
    assert result[0].candidate.claim_kind.value == "ticket_not_required"
    assert not result[0].supports_information_need
    payload = json.loads(fake.calls[0]["input"][1]["content"])
    assert payload["QUERY_CONTEXT_NOT_EVIDENCE"]["requested_subject_scope"] == "whole_venue"


def test_reasoner_discards_cross_source_or_paraphrased_spans() -> None:
    source = _source()
    bad = _assessment(source)["candidate"] | {"value_text": "admission is complimentary"}
    wrong = _assessment(source)["candidate"] | {"source_url": "https://evil.example.net"}
    result = asyncio.run(
        _reasoner(
            FakeResponses(
                [_assessment(source, candidate=bad), _assessment(source, candidate=wrong)]
            )
        ).reason(_task(), (source,), _place())
    )
    assert result == ()


def test_no_claim_and_empty_assessment_are_valid() -> None:
    source = _source("Alpha Zoo visitor information...")
    no_claim = _assessment(source, relevant=False, supports_information_need=False, candidate=None)
    result = asyncio.run(_reasoner(FakeResponses([no_claim])).reason(_task(), (source,), _place()))
    assert result[0].candidate is None
    assert asyncio.run(_reasoner(FakeResponses([])).reason(_task(), (source,), _place())) == ()


def test_reasoner_rejects_excess_assessments_instead_of_truncating() -> None:
    source = _source()
    fake = FakeResponses([_assessment(source)] * 4)
    with pytest.raises(ValueError, match="assessment limit"):
        asyncio.run(_reasoner(fake).reason(_task(), (source,), _place()))


def test_reasoner_rejects_unbounded_source_text_before_provider_call() -> None:
    source = _source("A" * 1201)
    fake = FakeResponses([])
    with pytest.raises(ValueError, match="native snippet is outside the bound"):
        asyncio.run(_reasoner(fake).reason(_task(), (source,), _place()))
    assert fake.calls == []
