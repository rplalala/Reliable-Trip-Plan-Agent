"""Evidence-informed V1 prompts while preserving the V0 planning objective."""

import json
from datetime import date

from backend.app.evidence.models import PlaceEvidence, RouteEvidenceBundle, WeatherEvidence
from backend.app.schemas.request import TravelRequest, TravelRequirements

ITINERARY_GENERATION_SYSTEM_PROMPT = """
You are the itinerary-generation stage of a travel planner.

Generate a complete structured itinerary from the original user request and extracted
requirements. Use only supplied normalized evidence for current place, weather, and route
facts; match the requested destination and date range exactly. Use available weather and
routes to improve grouping and feasibility. The response schema is supplied separately.
Every activity start and end must include date YYYY-MM-DD, time HH:MM:SS (including :00
seconds), and utc_offset +HH:MM or -HH:MM. Keep activity identifiers unique.

For a WALK baseline, use it for short pairs but never treat non_walkable_pairs as realistic
walking transfers. Honor an explicitly chosen transport mode without inferring a fallback.
TRANSIT alternatives give representative durations at their recorded departure time for
coarse sequencing and travel-time allowance only: provider_observed is measured by the
provider in that direction; mirrored_reverse_estimate copies only the observed duration in
reverse as an approximate proxy, not observed directional timetable evidence. If WALK is
unrealistic and TRANSIT unavailable, avoid tight sequencing or note uncertain transport
feasibility. Do not invent or promise transit lines, stops, timetables, departure times,
fares, bookings, or exact services. Before quoting route distance or duration, match the
element's origin_place_id and destination_place_id to the exact two Place evidence entries
for that transfer. Never reuse another pair's measurement; omit numbers without a match.

Use Place evidence only for its identified place. Do not infer missing facts, present
unavailable or partial evidence as confirmed, or claim checks outside supplied evidence.
When supplied opening hours apply to the planned date, schedule the entire visit within
them; do not excuse an early start or late finish in a note. If hours are unknown, do not
claim they were verified. Note material uncertainty in activity notes. Do not search, call
tools, validate an earlier itinerary, or repair an earlier itinerary.
""".strip()


def build_itinerary_generation_prompt(
    request: TravelRequest,
    requirements: TravelRequirements,
    reference_date: date,
    *,
    places: list[PlaceEvidence],
    weather: WeatherEvidence,
    routes: RouteEvidenceBundle,
) -> str:
    """Build one bounded prompt containing normalized evidence only."""

    evidence = {
        "places": [item.model_dump(mode="json") for item in places],
        "weather": weather.model_dump(mode="json"),
        "routes": routes.model_dump(mode="json"),
    }
    return (
        f"Reference date: {reference_date.isoformat()}\n\n"
        "Original user request:\n"
        "<user_request>\n"
        f"{request.request_text}\n"
        "</user_request>\n\n"
        "Extracted requirements:\n"
        "<travel_requirements>\n"
        f"{requirements.model_dump_json(indent=2)}\n"
        "</travel_requirements>\n\n"
        "Normalized V1-A external evidence:\n"
        "<external_evidence>\n"
        f"{json.dumps(evidence, indent=2, ensure_ascii=True)}\n"
        "</external_evidence>"
    )
