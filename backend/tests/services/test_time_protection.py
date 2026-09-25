"""Shared A contract: provenance validation, no semantic text heuristics."""

import asyncio
from datetime import date

import pytest
from pydantic import ValidationError

from backend.app.llm.azure_foundry.dto import FoundryInterpretationDTO
from backend.app.policies.interpreted_requirements import canonicalize_requirements
from backend.app.schemas.interpreted_requirements import InterpretationDraft
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.app.services.preference_interpretation import interpret_preferences
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v1.test_interpreted_requirements import draft_for


def protected_draft(**changes):
    row = dict(
        dates=["2026-09-12"],
        start_time="12:00",
        end_time="14:00",
        status="fixed",
        full_day=False,
        reason=None,
        source_refs=[{"quote": "Private time", "occurrence": 0}],
    )
    row.update(changes)
    data = draft_for().model_dump(mode="json")
    data.update(semantic_requirements=[], time_protections=[row])
    return InterpretationDraft.model_validate(
        FoundryInterpretationDTO.model_validate(data).model_dump()
    )


def test_wire_mapping_preserves_local_interval_and_canonical_sources():
    request = make_request("Private time")
    value = canonicalize_requirements(protected_draft(), request)
    item = value.time_protections[0]
    assert item.dates == (date(2026, 9, 12),)
    assert item.start_time.hour == 12 and item.end_time.hour == 14
    assert (
        request.additional_preferences[item.source_refs[0].start : item.source_refs[0].end]
        == "Private time"
    )


@pytest.mark.parametrize(
    "updates",
    [
        {"end_time": "11:00"},
        {"start_time": None},
        {"start_time": "12:00+10:00"},
        {"status": "unresolved", "reason": None},
    ],
)
def test_invalid_time_shape_is_not_silently_interpreted(updates):
    with pytest.raises(ValidationError):
        protected_draft(**updates)


@pytest.mark.parametrize(
    "updates",
    [
        {"dates": ["2026-09-30"]},
        {"source_refs": [{"quote": "Invented", "occurrence": 0}]},
    ],
)
def test_date_and_quote_boundaries_are_enforced(updates):
    with pytest.raises(RequirementBoundaryError):
        canonicalize_requirements(protected_draft(**updates), make_request("Private time"))


def test_unresolved_scope_and_legacy_absence_remain_distinct():
    value = canonicalize_requirements(
        protected_draft(
            status="unresolved", start_time=None, end_time=None, reason="Time zone not specified"
        ),
        make_request("Private time"),
    )
    assert value.time_protections[0].status == "unresolved"
    legacy = canonicalize_requirements(draft_for("relaxed"), make_request("relaxed"))
    assert legacy.time_protections is None
    assessed = canonicalize_requirements(
        draft_for("relaxed", time_protections=()), make_request("relaxed")
    )
    assert assessed.time_protections == ()
    assert len(assessed.semantic_requirements) == 1


def test_existing_interpretation_call_carries_new_dimension_once():
    class Model:
        calls = 0

        async def generate_structured(self, **kwargs):
            self.calls += 1
            return protected_draft()

    model = Model()
    result = asyncio.run(
        interpret_preferences(make_request("Private time"), date(2026, 9, 11), model)
    )
    assert model.calls == 1 and result.time_protections[0].status == "fixed"
