"""Shared structural ordering without itinerary feasibility repair."""

from types import SimpleNamespace

import pytest

from backend.app.policies.itinerary_output import validate_output_sources
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.itinerary_projection import EstimatedCostProjectionDiagnostic, V1Itinerary


def make_itinerary(version, ordered=False):
    def activity(identity, hour, day=22):
        return {
            "activity_id": identity, "title": identity, "place_name": identity,
            "source_place_id": None if version == "v0" else identity,
            "location": "Known location", "notes": "Unchanged uncertain access.",
            "start_time": f"2026-09-{day}T{hour:02}:00:00+10:00",
            "end_time": f"2026-09-{day}T{hour+2:02}:00:00+10:00",
            "estimated_cost": None if identity == "late" else {"amount": "12", "currency": "AUD"},
        }
    activities = [activity("late", 14), activity("early", 10), activity("tie", 10)]
    if ordered:
        activities = [activities[1], activities[2], activities[0]]
    cls = Itinerary if version == "v0" else V1Itinerary
    result = cls.model_validate({
        "output_version": "itinerary_2", "destination": "Example",
        "start_date": "2026-09-22", "end_date": "2026-09-23",
        "days": [{"date": "2026-09-22", "activities": activities},
                 {"date": "2026-09-23", "activities": [activity("tomorrow", 9, 23)]}],
        "reference_recommendations": [{"place_name": "Extra", "reason": "Optional",
                                       "source_ref": None}] if version == "v0" else [],
    })
    if isinstance(result, V1Itinerary):
        result.set_cost_projections(tuple(
            EstimatedCostProjectionDiagnostic(
                f"days[{di}].activities[{ai}].estimated_cost",
                "explicit_null" if a.estimated_cost is None else "exact_point",
            ) for di, day in enumerate(result.days) for ai, a in enumerate(day.activities)
        ))
    return result


@pytest.mark.parametrize("version", ["v0", "v1", "v2"])
@pytest.mark.parametrize("ordered", [False, True])
def test_shared_output_stably_orders_without_changing_fields(version, ordered):
    original = make_itinerary(version, ordered)
    before = original.model_dump()
    places = [SimpleNamespace(place_id=a.source_place_id, name=a.place_name)
              for day in original.days for a in day.activities]
    kwargs = {} if version == "v0" else {
        "places": places, "supplied_ids": [p.place_id for p in places],
    }
    result = validate_output_sources(original, **kwargs)
    assert [a.activity_id for a in result.days[0].activities] == ["early", "tie", "late"]
    assert original.model_dump() == before
    assert result.reference_recommendations == original.reference_recommendations
    assert [d.date for d in result.days] == [d.date for d in original.days]
    assert {a.activity_id: a.model_dump() for d in result.days for a in d.activities} == {
        a.activity_id: a.model_dump() for d in original.days for a in d.activities
    }
    assert validate_output_sources(result, **kwargs).model_dump() == result.model_dump()
    if ordered:
        assert result.model_dump() == before
    if isinstance(result, V1Itinerary):
        by_path = {p.field_path: p.projection for p in result.cost_projections}
        for di, day in enumerate(result.days):
            for ai, a in enumerate(day.activities):
                assert by_path[f"days[{di}].activities[{ai}].estimated_cost"] == (
                    "explicit_null" if a.estimated_cost is None else "exact_point"
                )
        assert original.cost_projections == make_itinerary(version, ordered).cost_projections
