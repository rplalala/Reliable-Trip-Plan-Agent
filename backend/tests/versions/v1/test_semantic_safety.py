"""Operational and evidence boundaries of the revised selection path."""

import asyncio
from datetime import date

import pytest

from backend.app.policies.interpreted_requirements import canonicalize_requirements
from backend.app.schemas.interpreted_requirements import (
    ClarificationRequired,
    DiscoveryDraft,
    EvidenceRequestDraft,
    NamedRequirementDraft,
    SourceQuote,
    SpecifiedTarget,
    Subject,
)
from backend.app.schemas.requirement_boundary import RequirementBoundaryError
from backend.app.versions.v1.runner import run_v1
from backend.tests.request_fixtures import make_request
from backend.tests.versions.v0.fakes import FakeStructuredLLMClient
from backend.tests.versions.v1.fakes import (
    FakePlacesProvider,
    FakeRoutesProvider,
    FakeWeatherProvider,
    RevisedFakeLLM,
    make_itinerary,
)
from backend.tests.versions.v1.test_interpreted_requirements import draft_for


def test_subjects_do_not_merge_and_links_are_canonical():
    text = "Mother and Father prefer less walking"
    quote = SourceQuote(quote=text, occurrence=0)
    base = draft_for(text).semantic_requirements[0]
    draft = draft_for(
        text,
        subjects=tuple(
            Subject(local_key=s, label=s, source_refs=(quote,)) for s in ("mother", "father")
        ),
        semantic_requirements=(
            base.model_copy(
                update={
                    "subject_target": SpecifiedTarget(
                        kind="specified", first_ref="mother", additional_refs=()
                    )
                }
            ),
            base.model_copy(
                update={
                    "local_key": "s2",
                    "subject_target": SpecifiedTarget(
                        kind="specified", first_ref="father", additional_refs=()
                    ),
                }
            ),
        ),
        discovery_intents=(
            DiscoveryDraft(
                requirement_refs=("s",),
                purpose="semantic_discovery",
                query_text="Places with short internal walks",
            ),
        ),
        experience_evidence_requests=(
            EvidenceRequestDraft(requirement_ref="s2", dimension="walking_intensity"),
        ),
    )
    contract = canonicalize_requirements(draft, make_request(text))
    assert len(contract.semantic_requirements) == 2
    labels = {s.subject_id: s.label for s in contract.subjects}
    semantics = {
        s.requirement_id: labels[s.subject_refs[0]] for s in contract.semantic_requirements
    }
    assert semantics[contract.discovery_intents[0].requirement_refs[0]] == "mother"
    assert semantics[contract.experience_evidence_requests[0].requirement_id] == "father"
    assert contract.subjects[0].source_refs[0].start == 0


def test_overflow_and_unknown_links_are_explicit():
    with pytest.raises(RequirementBoundaryError, match="overflow"):
        canonicalize_requirements(draft_for(overflow=True), make_request("Prefer local places"))
    draft = draft_for(
        discovery_intents=(
            DiscoveryDraft(
                requirement_refs=("bad",),
                purpose="semantic_discovery",
                query_text="Local places",
            ),
        )
    )
    with pytest.raises(RequirementBoundaryError, match="unknown_discovery"):
        canonicalize_requirements(draft, make_request("Prefer local places"))


def test_hard_preflight_makes_no_provider_calls():
    text = "Absolutely no stairs."
    draft = draft_for(text)
    draft = draft.model_copy(
        update={
            "semantic_requirements": (
                draft.semantic_requirements[0].model_copy(update={"strength": "hard"}),
            )
        }
    )
    places = FakePlacesProvider()
    llm = FakeStructuredLLMClient([draft])
    with pytest.raises(ClarificationRequired):
        asyncio.run(
            run_v1(
                make_request(additional_preferences=text),
                llm,
                places,
                FakeWeatherProvider(),
                FakeRoutesProvider(),
                reference_date=date(2026, 9, 11),
            )
        )
    assert len(llm.calls) == 1
    assert places.search_requests == places.details_requests == places.reviews_requests == []


@pytest.mark.parametrize("inclusion", ["REQUIRED", "EXCLUDED"])
def test_named_identity_controls_membership_without_semantic_reward(inclusion):
    text = "Place poi-0-0"
    draft = draft_for(
        text,
        semantic_requirements=(),
        named_places=(
            NamedRequirementDraft(
                place_text=text,
                inclusion=inclusion,
                source_refs=(SourceQuote(quote=text, occurrence=0),),
            ),
        ),
    )
    places = FakePlacesProvider()
    result = asyncio.run(
        run_v1(
            make_request(additional_preferences=text),
            RevisedFakeLLM([draft, make_itinerary()]),
            places,
            FakeWeatherProvider(),
            FakeRoutesProvider(),
            reference_date=date(2026, 9, 11),
        )
    )
    ids = result.planning_supply.selected_place_ids
    assert ("poi-0-0" in ids) == (inclusion == "REQUIRED")
    assert not result.interpreted_requirements.semantic_requirements
    if inclusion == "EXCLUDED":
        assert "poi-0-0" not in [r.place_id for r in places.details_requests]


def test_reserves_stay_inside_total_details_attempt_budget():
    from backend.app.runtime.budget import ToolBudgetLimits
    from backend.app.runtime.config_loader import load_runtime_config
    from backend.app.runtime.config_models import AcquisitionConfig
    from backend.tests.versions.v1.test_supply_integration import ManyPlacesProvider

    places = ManyPlacesProvider(per_query=8, details_failure_ids={"poi-0-0", "poi-0-1"})
    draft = draft_for(semantic_requirements=())
    result = asyncio.run(
        run_v1(
            make_request(additional_preferences="Plan Sydney"),
            RevisedFakeLLM([draft, make_itinerary()]),
            places,
            FakeWeatherProvider(),
            FakeRoutesProvider(),
            reference_date=date(2026, 9, 11),
            runtime_config=load_runtime_config().model_copy(
                update={"acquisition": AcquisitionConfig(policy_id="conservative_1")}
            ),
            budget_limits=ToolBudgetLimits(max_place_detail_calls=10),
        )
    )
    assert len(places.details_requests) == 10
    assert not {"poi-0-0", "poi-0-1"} & set(result.planning_supply.selected_place_ids)
