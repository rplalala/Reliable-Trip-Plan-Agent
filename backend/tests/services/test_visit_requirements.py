"""B shared visit obligations use the existing interpretation and provenance boundary."""

import pytest
from pydantic import ValidationError

from backend.app.llm.azure_foundry.dto import FoundryInterpretationDTO
from backend.app.policies.interpreted_requirements import (
    canonicalize_requirements,
    validate_canonical_requirements,
)
from backend.app.schemas.interpreted_requirements import InterpretationDraft
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v1.test_interpreted_requirements import draft_for


def visit_draft(**changes):
    row = dict(
        place_text="Museum",
        minimum_visits=2,
        dates=["2026-09-12", "2026-09-13"],
        status="executable",
        reason=None,
        source_refs=[dict(quote="museum twice", occurrence=0)],
    )
    row.update(changes)
    return draft_for(
        "Museum twice",
        semantic_requirements=(),
        named_places=[
            dict(
                place_text="Museum",
                inclusion="REQUIRED",
                source_refs=[dict(quote="Museum twice", occurrence=0)],
            )
        ],
        visit_requirements=[row],
    )


def test_strict_mapping_and_canonical_roundtrip_preserve_count_dates_and_casefold_source():
    draft = visit_draft()
    mapped = InterpretationDraft.model_validate(
        FoundryInterpretationDTO.model_validate(draft.model_dump(mode="json")).model_dump()
    )
    request = make_request("Museum twice")
    canonical = canonicalize_requirements(mapped, request)
    assert canonical.visit_requirements[0].minimum_visits == 2
    assert canonical.visit_requirements[0].source_refs[0].match_mode == "casefold_equivalent"
    assert validate_canonical_requirements(canonical, request) == canonical


@pytest.mark.parametrize(
    "changes",
    [
        {"minimum_visits": 1},
        {"dates": ["2026-09-12", "2026-09-12"]},
        {"status": "unresolved", "reason": None},
    ],
)
def test_invalid_visit_contract_is_rejected(changes):
    with pytest.raises(ValidationError):
        visit_draft(**changes)


@pytest.mark.parametrize(
    "changes",
    [
        {"place_text": "Other"},
        {"dates": ["2026-09-30"]},
        {"source_refs": [dict(quote="Invented", occurrence=0)]},
    ],
)
def test_visit_identity_date_and_source_boundaries(changes):
    with pytest.raises(RequirementBoundaryError):
        canonicalize_requirements(visit_draft(**changes), make_request("Museum twice"))


def test_legacy_unassessed_and_assessed_empty_remain_distinct():
    assert draft_for().visit_requirements is None
    assert draft_for(visit_requirements=()).visit_requirements == ()


def test_explicit_access_mode_survives_shared_strict_mapping():
    draft = visit_draft(access_mode="venue_entry")
    wire = FoundryInterpretationDTO.model_validate(draft.model_dump(mode="json"))
    canonical = canonicalize_requirements(
        InterpretationDraft.model_validate(wire.model_dump()), make_request("Museum twice")
    )
    assert canonical.visit_requirements[0].access_mode == "venue_entry"
    assert visit_draft().visit_requirements[0].access_mode is None
    with pytest.raises(ValidationError):
        visit_draft(access_mode="public_access_verified")
