"""Offline shared-primary sizing. Synthetic provider evidence; no network or model calls."""

import json
from datetime import date, timedelta

from backend.app.llm.azure_foundry.dto import FoundryPrimaryItineraryDTO
from backend.app.runtime.config_loader import load_runtime_config
from backend.app.runtime.token_counting import count_tokens
from backend.app.versions.v1.prompts import ITINERARY_GENERATION_SYSTEM_PROMPT
from tools.diagnostics.itinerary_payload import fixtures, measure


def output_fixture():
    start = date(2026, 9, 12)
    days = []
    for n in range(10):
        day = str(start + timedelta(days=n))
        activities = []
        for i in range(5):
            activities.append(
                dict(
                    activity_kind="main_poi",
                    activity_id=f"a{n}_{i}",
                    title="Visit a supplied cultural place",
                    source_place_id=f"place-{(n * 5 + i) % 20}",
                    place_name="Synthetic museum",
                    location="Fixture city",
                    estimated_cost=None,
                    start_time=dict(date=day, time=f"{9 + 2 * i:02}:00:00", utc_offset="+10:00"),
                    end_time=dict(date=day, time=f"{10 + 2 * i:02}:00:00", utc_offset="+10:00"),
                    notes=(
                        "Admission and booking remain unverified; "
                        "allow for the supplied transport option."
                    ),
                )
            )
        days.append(dict(date=day, activities=activities))
    return FoundryPrimaryItineraryDTO(
        output_version="itinerary_2",
        destination="Fixture city",
        start_date=str(start),
        end_date=str(start + timedelta(days=9)),
        days=days,
    )


def main():
    config = load_runtime_config()
    rows = []
    for days, k, long in [(3, 12, False), (5, 16, False), (10, 20, False), (10, 20, True)]:
        user, metadata = fixtures(days, k, long)
        rows.append(
            measure(ITINERARY_GENERATION_SYSTEM_PROMPT, user, config.main_generation, metadata)
        )
        if days == 10 and not long:
            # Normalize additional synthetic mode facts using the actual bundle/compact serializer.
            from backend.app.services.initial_routes import compact_routes
            from tools.diagnostics.itinerary_fixtures import _places, _routes

            bundle = _routes(sorted(p.place_id for p in _places(20)[1]))
            drive = bundle.baseline.model_copy(
                update={
                    "travel_mode": "DRIVE",
                    "routing_preference": "TRAFFIC_UNAWARE",
                    "source_ref": "fixture:drive",
                    "elements": bundle.baseline.elements[:32],
                }
            )
            projection = compact_routes(
                bundle.model_copy(update={"alternatives": [*bundle.alternatives, drive]})
            )
            a = user.index("<external_evidence>") + len("<external_evidence>")
            b = user.index("</external_evidence>")
            content = json.loads(user[a:b])
            content["routes"] = projection
            mixed = user[:a] + json.dumps(content, indent=2) + user[b:]
            rows.append(
                measure(
                    ITINERARY_GENERATION_SYSTEM_PROMPT,
                    mixed,
                    config.main_generation,
                    {**metadata, "scenario": "dense_all_directed_modes_synthetic"},
                )
            )
    user, metadata = fixtures(10, 20, True)
    base = measure(ITINERARY_GENERATION_SYSTEM_PROMPT, user, config.main_generation, metadata)[
        "total_tokens"
    ]
    for total in (251900, 252100):
        # Engineering guard stress, explicitly not a claim that upstream facts have these lengths.
        padded = user + "\nSynthetic engineering padding:\n" + " x" * max(0, total - base)
        rows.append(
            measure(
                ITINERARY_GENERATION_SYSTEM_PROMPT,
                padded,
                config.main_generation,
                {
                    "scenario": "engineering_guard_only",
                    "target": total,
                    "upstream_validated": False,
                },
            )
        )
    output = output_fixture()
    print(
        json.dumps(
            dict(
                input_rows=rows,
                output=dict(
                    activities=50,
                    days=10,
                    tokens=count_tokens(output.model_dump_json()),
                    ceiling=config.main_generation.output_tokens,
                    model_generated_transfers=False,
                ),
                limitation=(
                    "Offline engineering counts, not provider usage or proof of model completion."
                ),
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
