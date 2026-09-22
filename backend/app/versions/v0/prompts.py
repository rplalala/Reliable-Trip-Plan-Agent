"""Plain-LLM generation over the shared structured input foundation."""

from datetime import date

from backend.app.policies.generation_policy import FIRST_GENERATION_POLICY
from backend.app.schemas.request import PlanningRequest, TravelRequirements

ITINERARY_GENERATION_SYSTEM_PROMPT = """
You are the itinerary-generation stage of a plain-LLM travel planner.

Generate a structured sightseeing/experience itinerary using only validated structured trip facts,
normalized semantic requirements, and your pretrained general knowledge. Follow the requested
destination and date range exactly. For every activity start and end, always provide all three
datetime components
required by the response schema. The date must use exactly YYYY-MM-DD. The time must use exactly
HH:MM:SS, including seconds when they are 00. The utc_offset must use exactly +HH:MM or -HH:MM.
For example: date 2026-10-01, time 13:30:00, utc_offset +09:00. Do not abbreviate 13:30:00 to
13:30. Keep activity identifiers unique within the itinerary.

Respect named REQUIRED/OPTIONAL/EXCLUDED intentions by user-mentioned name, without provider IDs.
Honor subject-specific preferences and conditional tradeoffs without inventing evidence.
You have no tools and no access to live or external information. Do not claim that opening
hours, availability, prices, routes, travel times, weather, events, or disruptions were checked
or confirmed. Do not search, retrieve evidence, validate constraints, or repair an earlier
itinerary. The response schema is supplied separately by the provider.

Output contract: itinerary_2. Produce a coherent timed primary sightseeing/experience itinerary
and zero to three reference_recommendations for the WHOLE trip. References are optional,
unscheduled suggestions, not bookings, committed costs or REQUIRED visit satisfaction.
Keep primary activity times required. References have no visit times or costs. Return []
when no suitable extra option exists. Do not fill the whole day, require meals/hotel returns,
nightlife or filler, or treat the default daily target as a mandatory quota.
Consider the user's pace and purpose;
an early finish is not automatically good or bad. Do not force three references or use every
option. Place type does not assign role: a REQUIRED cafe belongs in scheduled visits when
feasible. Preserve exclusions in BOTH sections. Do not duplicate scheduled venues as references.
A generic non-venue activity may have null place_name and source_place_id; do not invent identity.
Do not output source_ref, provenance objects, verified labels or booking claims.
For V0, every source_place_id is null. Recommendations use model knowledge only and are
not live-verified. Do not invent external IDs, confirmed hours, prices or reservations.
Complete the primary itinerary first. References should supplement its actual planned places;
do not sacrifice primary activities to fill references. Do not claim measured nearby distances
or walking times. References remain model-knowledge suggestions, not live nearby search results.
""".strip() + "\n\n" + FIRST_GENERATION_POLICY


def build_itinerary_generation_prompt(
    request: PlanningRequest,
    requirements: TravelRequirements,
    reference_date: date,
    interpreted_requirements,
) -> str:
    """Build the user prompt for generating the V0 itinerary."""

    return (
        f"Reference date: {reference_date.isoformat()}\n\n"
        "Original user request:\n"
        "<user_request>\n"
        f"{request.additional_preferences}\n"
        "</user_request>\n\n"
        "Authoritative trip facts:\n"
        "<travel_requirements>\n"
        f"{requirements.model_dump_json(indent=2)}\n"
        "</travel_requirements>\n"
        "Shared semantic context (named intentions do not require provider IDs):\n"
        f"{interpreted_requirements.model_dump_json()}"
    )
