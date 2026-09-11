"""Version-locked prompts for the V0 plain-LLM workflow."""

from datetime import date

from backend.app.schemas.request import TravelRequest, TravelRequirements

REQUIREMENT_EXTRACTION_SYSTEM_PROMPT = """
You are the requirement-extraction stage of a plain-LLM travel planner.

Extract only requirements stated by the user or directly resolvable from the supplied
reference date. Do not invent a destination, dates, traveler count, budget, required
activities, exclusions, or preferences. Use null for unknown scalar values and include the
names of missing or uncertain fields in unresolved_fields. Normalize explicit monetary
currencies to ISO 4217 codes.

You have no tools and no access to live or external information. Do not search, retrieve,
validate travel feasibility, or add factual travel advice. The response schema is supplied
separately by the provider.
""".strip()

ITINERARY_GENERATION_SYSTEM_PROMPT = """
You are the itinerary-generation stage of a plain-LLM travel planner.

Generate a complete structured itinerary using only the original user request, the extracted
requirements, and your pretrained general knowledge. Follow the requested destination and date
range exactly. For every activity start and end, always provide all three datetime components
required by the response schema. The date must use exactly YYYY-MM-DD. The time must use exactly
HH:MM:SS, including seconds when they are 00. The utc_offset must use exactly +HH:MM or -HH:MM.
For example: date 2026-10-01, time 13:30:00, utc_offset +09:00. Do not abbreviate 13:30:00 to
13:30. Keep activity identifiers unique within the itinerary.

You have no tools and no access to live or external information. Do not claim that opening
hours, availability, prices, routes, travel times, weather, events, or disruptions were checked
or confirmed. Do not search, retrieve evidence, validate constraints, or repair an earlier
itinerary. The response schema is supplied separately by the provider.
""".strip()


def build_requirement_extraction_prompt(
    request: TravelRequest,
    reference_date: date,
) -> str:
    """Build the user prompt for extracting requirements."""

    return (
        f"Reference date: {reference_date.isoformat()}\n\n"
        "Original user request:\n"
        "<user_request>\n"
        f"{request.request_text}\n"
        "</user_request>"
    )


def build_itinerary_generation_prompt(
    request: TravelRequest,
    requirements: TravelRequirements,
    reference_date: date,
) -> str:
    """Build the user prompt for generating the V0 itinerary."""

    return (
        f"Reference date: {reference_date.isoformat()}\n\n"
        "Original user request:\n"
        "<user_request>\n"
        f"{request.request_text}\n"
        "</user_request>\n\n"
        "Extracted requirements:\n"
        "<travel_requirements>\n"
        f"{requirements.model_dump_json(indent=2)}\n"
        "</travel_requirements>"
    )
