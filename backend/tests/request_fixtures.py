"""Explicit structured form fixtures, never natural-language input parsing."""

from backend.app.schemas.request import PlanningRequest


def make_request(additional_preferences="", *, requirements=None, **updates):
    fields = dict(
        destination="Sydney",
        start_date="2026-09-12",
        end_date="2026-09-13",
        traveler_count=2,
        budget={"amount": "1800.00", "currency": "AUD"},
    )
    if requirements is not None:
        fields.update(
            requirements.model_dump(
                include={"destination", "start_date", "end_date", "traveler_count", "budget"},
                exclude_none=True,
            )
        )
    fields.update(updates)
    return PlanningRequest(**fields, additional_preferences=additional_preferences)
