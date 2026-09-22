"""Current evidence-linked review opportunity ordering."""

from backend.app.schemas.interpreted_requirements import ExperienceEvidenceRequest
from backend.app.services.candidate_acquisition import allocate_review_order
from backend.tests.candidate_fixtures import candidate_fixture


def test_reviews_only_registered_dimensions_with_required_relevance_and_dedup():
    p = candidate_fixture(4, 2)
    contract = p.requirements
    first, second = contract.semantic_requirements
    contract = contract.model_copy(
        update={
            "experience_evidence_requests": (
                ExperienceEvidenceRequest(
                    requirement_id=first.requirement_id, dimension="walking_intensity"
                ),
            )
        }
    )
    ids = [x.candidate.place_id for x in p.canonical_places]
    links = {
        ids[0]: (first.requirement_id,),
        ids[1]: (second.requirement_id,),
        ids[2]: (first.requirement_id,),
    }
    assert allocate_review_order(contract, p.canonical_places, {ids[2], ids[1]}, links) == (
        ids[2],
        ids[0],
    )
    assert allocate_review_order(p.requirements, p.canonical_places, set(), links) == ()


def test_registered_pool_requirement_without_discovery_still_has_bounded_opportunity():
    p = candidate_fixture(4, 1)
    contract = p.requirements.model_copy(
        update={
            "experience_evidence_requests": (
                ExperienceEvidenceRequest(requirement_id="semantic_1", dimension="crowding"),
            )
        }
    )
    assert len(allocate_review_order(contract, p.canonical_places, set(), {})) == 4
