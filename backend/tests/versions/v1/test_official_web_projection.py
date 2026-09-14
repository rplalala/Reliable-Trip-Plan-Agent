"""Final V1-A to official-Web projection boundary."""

from datetime import UTC, date, datetime
from types import SimpleNamespace

import pytest

from backend.app.evidence.models import EvidenceAvailability, PlaceCandidate, PlaceEvidence
from backend.app.evidence.selection_models import PlaceOpeningDate
from backend.app.versions.v1.official_web import project_official_web_inputs


def _pair(place_id: str) -> tuple[PlaceCandidate, PlaceEvidence]:
    candidate = PlaceCandidate(
        place_id=place_id,
        name=f"Place {place_id}",
        latitude=-33.8,
        longitude=151.2,
        source_query="Sydney places",
        category="museum",
        provider_rank=0,
        business_status="OPERATIONAL",
    )
    place = PlaceEvidence(
        place_id=place_id,
        name=candidate.name,
        latitude=-33.8,
        longitude=151.2,
        business_status="OPERATIONAL",
        website_uri=f"https://{place_id}.example.org",
        rating=4.7,
        availability=EvidenceAvailability.AVAILABLE,
        retrieved_at=datetime(2026, 9, 14, tzinfo=UTC),
        source_ref=f"google_places:{place_id}",
    )
    return candidate, place


def _context():
    return SimpleNamespace(
        named_place_resolutions=(
            SimpleNamespace(resolved_place_id="b"),
            SimpleNamespace(resolved_place_id="a"),
            SimpleNamespace(resolved_place_id=None),
            SimpleNamespace(resolved_place_id="not_selected"),
        ),
        must_visit_place_ids=frozenset({"b", "not_selected"}),
        enriched_candidates=tuple(
            SimpleNamespace(
                candidate=SimpleNamespace(place_id=place_id),
                search_opening_date_observations=(),
                details_opening_date=None,
            )
            for place_id in ("b", "a")
        ),
    ), SimpleNamespace(
        selected_place_ids=("b", "a"),
        final_selection=SimpleNamespace(
            eligibility=tuple(
                SimpleNamespace(place_id=place_id, opening_date_conflict=False)
                for place_id in ("b", "a")
            )
        ),
    )


def test_projection_keeps_final_order_and_only_resolved_selected_intents() -> None:
    funnel, selection = _context()
    b, b_place = _pair("b")
    a, a_place = _pair("a")
    projection = project_official_web_inputs(
        funnel=funnel,
        selection=selection,
        candidates=[b, a],
        places=[b_place, a_place],
    )
    assert [item.place_id for item in projection.candidates] == ["b", "a"]
    assert [item.place_id for item in projection.places] == ["b", "a"]
    assert projection.named_place_ids == frozenset({"b", "a"})
    assert projection.must_visit_place_ids == frozenset({"b"})
    assert [item.rating for item in projection.places] == [None, None]
    assert b_place.rating == 4.7
    assert projection.places[0].website_uri == b_place.website_uri
    assert projection.places[0].availability is EvidenceAvailability.AVAILABLE
    assert projection.opening_date_conflicts == {}
    assert "profiles" not in vars(projection)


def test_projection_carries_only_selected_conflicting_opening_dates() -> None:
    funnel, selection = _context()
    funnel.enriched_candidates = (
        SimpleNamespace(
            candidate=SimpleNamespace(place_id="b"),
            search_opening_date_observations=(PlaceOpeningDate(year=2026, month=12),),
            details_opening_date=PlaceOpeningDate(year=2026, month=12, day=25),
        ),
        funnel.enriched_candidates[1],
    )
    selection.final_selection.eligibility = (
        SimpleNamespace(place_id="b", opening_date_conflict=True),
        SimpleNamespace(place_id="a", opening_date_conflict=False),
    )
    b, b_place = _pair("b")
    a, a_place = _pair("a")
    projection = project_official_web_inputs(
        funnel=funnel, selection=selection, candidates=[b, a], places=[b_place, a_place]
    )
    assert projection.opening_date_conflicts == {"b": (date(2026, 12, 31), date(2026, 12, 25))}


@pytest.mark.parametrize("invalid", ["short", "reversed", "wrong_id"])
def test_projection_rejects_misalignment(invalid: str) -> None:
    funnel, selection = _context()
    b, b_place = _pair("b")
    a, a_place = _pair("a")
    candidates = [b, a]
    places = [b_place, a_place]
    if invalid == "short":
        places.pop()
    elif invalid == "reversed":
        candidates.reverse()
    else:
        places[1] = _pair("c")[1]
    with pytest.raises(ValueError):
        project_official_web_inputs(
            funnel=funnel,
            selection=selection,
            candidates=candidates,
            places=places,
        )
