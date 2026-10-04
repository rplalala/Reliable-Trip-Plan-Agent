"""Minimal diagnostic counterfactuals, not feasible insertion or model replays."""

import json
from datetime import date
from types import SimpleNamespace

from replay import BASE

from backend.app.policies.generation_diagnostics import observe_generation
from backend.app.schemas.itinerary import Itinerary

d = json.loads((BASE / "sydney_v1/result.json").read_text())
full = Itinerary.model_validate(d["itinerary"])
last = full.days[-1]
single = full.model_copy(
    update={
        "days": [last],
        "start_date": last.date,
        "end_date": last.date,
        "transfers": [],
        "route_diagnostics": [],
        "reference_recommendations": [],
    }
)
req = SimpleNamespace(start_date=last.date, end_date=last.date)
ids = d["planning_supply"]["selected_place_ids"]


def count(it):
    return (
        observe_generation(it, req, reference_date=date(2026, 9, 27), supplied_ids=ids)
        .days[0]
        .distinct_main_poi_count
    )


assert count(single) == 1
base = last.activities[0]
generic = base.model_copy(
    update={
        "activity_id": "diagnostic_generic",
        "activity_kind": "generic_activity",
        "source_place_id": None,
        "place_name": None,
    }
)
with_generic = single.model_copy(
    update={"days": [last.model_copy(update={"activities": [base, generic]})]}
)
assert count(with_generic) == 1
other = full.days[0].activities[0]
with_primary = single.model_copy(
    update={"days": [last.model_copy(update={"activities": [base, other]})]}
)
# Normalize only date/time in this synthetic counting probe; no feasibility claim.
other = other.model_copy(update={"start_time": base.start_time, "end_time": base.end_time})
with_primary = single.model_copy(
    update={"days": [last.model_copy(update={"activities": [base, other]})]}
)
assert count(with_primary) == 2
print(
    "PASS: one-date reproduction counts 1; generic addition stays 1; "
    "distinct main addition counts 2. "
    "Synthetic count-only probes, not valid insertions."
)
