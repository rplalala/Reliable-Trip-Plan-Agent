"""Provider-owned facts survive model presentation without mutating raw output."""

from types import SimpleNamespace

import pytest

from backend.app.policies.itinerary_output import validate_output_sources
from backend.tests.policies.test_itinerary_ordering import make_itinerary


@pytest.mark.parametrize("model_location", [None, "Short address", "Wrong address"])
def test_linked_activity_uses_canonical_facts_and_preserves_model_claim(model_location):
    raw = make_itinerary("v1", ordered=True)
    activity = raw.days[0].activities[0]
    activity.place_name = "Model name"
    activity.location = model_location
    before = raw.model_dump()
    diagnostics = raw.cost_projections
    places = [
        SimpleNamespace(
            place_id=a.source_place_id,
            name=f"Provider {a.activity_id}",
            formatted_address=f"17 Example Road, Sample City 2000, Country ({a.activity_id})",
        )
        for day in raw.days
        for a in day.activities
    ]
    kwargs = {"places": places, "supplied_ids": [p.place_id for p in places]}
    accepted = validate_output_sources(raw, **kwargs)
    expected = {p.place_id: p for p in places}
    for day in accepted.days:
        for a in day.activities:
            assert a.place_name == expected[a.source_place_id].name
            assert a.location == expected[a.source_place_id].formatted_address
            original = next(
                x for d in raw.days for x in d.activities if x.activity_id == a.activity_id
            )
            assert a.model_dump(exclude={"place_name", "location"}) == original.model_dump(
                exclude={"place_name", "location"}
            )
    assert raw.model_dump() == before
    assert accepted.cost_projections == diagnostics
    assert validate_output_sources(accepted, **kwargs).model_dump() == accepted.model_dump()


@pytest.mark.parametrize("version", ["v0", "v1"])
def test_unlinked_activities_keep_model_location(version):
    raw = make_itinerary(version, ordered=True)
    for day in raw.days:
        for activity in day.activities:
            activity.source_place_id = None
            activity.place_name = None
            activity.location = "Generic meeting area"
    before = raw.model_dump()
    kwargs = {} if version == "v0" else {"places": [], "supplied_ids": []}
    assert validate_output_sources(raw, **kwargs).model_dump() == before
    assert raw.model_dump() == before


@pytest.mark.parametrize("supplied_ids", [[], ["early"]])
def test_foreign_or_unavailable_id_is_rejected_before_backfill(supplied_ids):
    raw = make_itinerary("v1", ordered=True)
    before = raw.model_dump()
    places = [SimpleNamespace(place_id="foreign", name="Other", formatted_address="Other")]
    with pytest.raises(ValueError, match="outside the supplied candidate ledger"):
        validate_output_sources(raw, places=places, supplied_ids=supplied_ids)
    assert raw.model_dump() == before


def test_absent_provider_address_does_not_adopt_model_guess():
    raw = make_itinerary("v1", ordered=True)
    places = [
        SimpleNamespace(place_id=a.source_place_id, name=a.place_name, formatted_address=None)
        for day in raw.days
        for a in day.activities
    ]
    result = validate_output_sources(raw, places=places, supplied_ids=[p.place_id for p in places])
    assert all(a.location is None for day in result.days for a in day.activities)
    assert all(a.location == "Known location" for day in raw.days for a in day.activities)


def test_v0_retains_model_name_address_and_rejects_external_identity():
    raw = make_itinerary("v0", ordered=True)
    before = raw.model_dump()
    assert validate_output_sources(raw).model_dump() == before
    raw.days[0].activities[0].source_place_id = "foreign"
    with pytest.raises(ValueError, match="V0 cannot author external place identities"):
        validate_output_sources(raw)
