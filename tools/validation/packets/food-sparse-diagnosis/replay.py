"""Offline capture replay. No providers; optional red quality observation assertion."""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from backend.app.policies.generation_diagnostics import observe_generation
from backend.app.schemas.interpreted_requirements import InterpretedTripRequirements
from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.poi_semantics import POISemanticAssessment
from backend.app.schemas.request import TravelRequirements

BASE = Path(__file__).resolve().parents[4] / "logs/semantic_short_reference_revalidation_20260927"
CASES = {"sydney_v1": "semantic_3", "melbourne_v1": "semantic_2", "sydney_v3": "semantic_3"}


def replay():
    output = {}
    for case, food_id in CASES.items():
        data = json.loads((BASE / case / "result.json").read_text())
        itinerary = Itinerary.model_validate(data["itinerary"])
        contract = InterpretedTripRequirements.model_validate(data["interpreted_requirements"])
        rows = [
            POISemanticAssessment.model_validate(r)
            for r in data["semantic_assessment"]["assessments"]
        ]
        selected = set(data["planning_supply"]["selected_place_ids"])
        evidence = json.loads(
            next((BASE / case / "trace").rglob("0001_selected_place_evidence.json")).read_text()
        )
        assert len(evidence) == len(selected)
        scheduled = {
            a.source_place_id for d in itinerary.days for a in d.activities if a.source_place_id
        }
        observed = observe_generation(
            itinerary,
            TravelRequirements.model_validate(data["requirements"]),
            reference_date=date(2026, 9, 27),
            supplied_ids=selected | scheduled,
            semantic_assessments=rows,
            contract=contract,
        )
        assert [r.distinct_main_poi_count for r in observed.days] == [
            r["distinct_main_poi_count"] for r in data["generation_diagnostics"]["days"]
        ]
        food = [
            r
            for r in rows
            if any(m.requirement_id == food_id and m.relation == "supported" for m in r.matches)
        ]
        output[case] = {
            "counts": [r.distinct_main_poi_count for r in observed.days],
            "sparse_dates": [
                str(r.date) for r in observed.days if r.target_status == "below_target"
            ],
            "completion": observed.policy_completion,
            "goal_progress": list(observed.goal_progress),
            "eligible": data["planning_supply"]["eligible_count"],
            "selected": len(selected),
            "scheduled_ids": len(scheduled),
            "unused_selected": len(selected - scheduled),
            "food_supported": [
                {
                    "name": r.visit_object,
                    "role": r.role,
                    "selected": r.place_id in selected,
                    "scheduled": r.place_id in scheduled,
                }
                for r in food
            ],
            "generic": [
                {"date": str(d.date), "title": a.title, "notes": a.notes}
                for d in itinerary.days
                for a in d.activities
                if a.activity_kind == "generic_activity"
            ],
        }
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--assert-no-sparse", action="store_true")
    args = parser.parse_args()
    report = replay()
    print(json.dumps(report, indent=2))
    if args.assert_no_sparse:
        assert not any(r["sparse_dates"] for r in report.values()), (
            "Observed quality gap: four V1 days below default target; not a hard Spec assertion"
        )
