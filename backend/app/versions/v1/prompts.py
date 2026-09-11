"""Evidence-informed V1 prompts while preserving the V0 planning objective."""

import json
from datetime import date

from backend.app.evidence.models import PlaceEvidence, RouteEvidence, WeatherEvidence
from backend.app.schemas.request import TravelRequest, TravelRequirements

ITINERARY_GENERATION_SYSTEM_PROMPT = """
You are the itinerary-generation stage of a travel planner.

Generate a complete structured itinerary using the original user request, the extracted
requirements, and only the supplied normalized external evidence for current place, weather,
and route facts. Follow the requested destination and date range exactly. For every activity
start and end, always provide all three datetime components required by the response schema.
The date must use exactly YYYY-MM-DD. The time must use exactly HH:MM:SS, including seconds
when they are 00. The utc_offset must use exactly +HH:MM or -HH:MM. For example: date
2026-10-01, time 13:30:00, utc_offset +09:00. Do not abbreviate 13:30:00 to 13:30. Keep
activity identifiers unique within the itinerary.

Use weather and route evidence to improve grouping and feasibility when it is available. Use
Place evidence only for the place it identifies. Do not infer missing external facts, convert
unavailable or partial evidence into confirmed facts, or claim that information outside the
supplied evidence was checked. Preserve uncertainty in activity notes when it materially
affects the plan. Do not search, call tools, validate an earlier itinerary, or repair an
earlier itinerary. The response schema is supplied separately by the provider.
""".strip()


def build_itinerary_generation_prompt(
    request: TravelRequest,
    requirements: TravelRequirements,
    reference_date: date,
    *,
    places: list[PlaceEvidence],
    weather: WeatherEvidence,
    routes: RouteEvidence,
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
