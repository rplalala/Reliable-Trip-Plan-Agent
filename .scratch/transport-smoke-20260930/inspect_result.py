"""Read-only development observations; missing transfers never become passes."""

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.app.schemas.itinerary import Itinerary  # noqa: E402


def inspect(data):
    itinerary = Itinerary.model_validate(data["itinerary"])
    version = data["system_version"]
    transfers = itinerary.transfers
    records = []
    expected = set()
    unknown_adjacencies = []
    for day in itinerary.days:
        activities = sorted(day.activities, key=lambda a: a.start_time)
        if version == "v0":
            continue  # Model transport content and estimates are reviewed manually.
        for left, right in zip(activities, activities[1:], strict=False):
            pair = (left.activity_id, right.activity_id)
            if not left.source_place_id or not right.source_place_id:
                unknown_adjacencies.append({"date": str(day.date), "pair": pair})
                continue
            if left.source_place_id == right.source_place_id:
                continue
            expected.add(pair)
            matches = [t for t in transfers if (t.from_activity_id, t.to_activity_id) == pair]
            diagnostics = [
                d
                for d in itinerary.route_diagnostics
                if (d.get("from_activity_id"), d.get("to_activity_id")) == pair
            ]
            bound = len(matches) == 1 and (
                matches[0].origin_place_id == left.source_place_id
                and matches[0].destination_place_id == right.source_place_id
                and left.end_time <= matches[0].departure_time <= right.start_time
                and matches[0].arrival_time is not None
                and matches[0].departure_time <= matches[0].arrival_time <= right.start_time
            )
            records.append(
                {
                    "date": str(day.date),
                    "pair": pair,
                    "origin": left.source_place_id,
                    "destination": right.source_place_id,
                    "transfer_count": len(matches),
                    "diagnostic_count": len(diagnostics),
                    "structural_binding_complete": bound,
                    "diagnostics": diagnostics,
                    "transfers": [t.model_dump(mode="json") for t in matches],
                }
            )
    orphan = [
        t.model_dump(mode="json")
        for t in transfers
        if (t.from_activity_id, t.to_activity_id) not in expected
    ]
    activities = [a for d in itinerary.days for a in d.activities]
    declared = [a.activity_id for a in activities if a.activity_kind == "transport"]
    return {
        "version": version,
        "days": [
            {"date": str(d.date), "roles": dict(Counter(a.activity_kind for a in d.activities))}
            for d in itinerary.days
        ],
        "declared_transport_activity_ids": declared,
        "transport_source_boundary_passed": (not transfers if version == "v0" else not declared),
        "pair_observations": records,
        "unlocatable_adjacencies": unknown_adjacencies,
        "orphan_transfers": orphan,
        "missing_or_invalid_binding_count": sum(
            not r["structural_binding_complete"] for r in records
        ),
        "factual_feasibility": "not_independently_verified",
        "needs_manual_transport_prose_review": True,
    }


if __name__ == "__main__":
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(inspect(payload), ensure_ascii=True, indent=2))
