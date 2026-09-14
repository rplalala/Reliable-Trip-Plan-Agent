"""Select only temporally applicable Places opening hours for V1 planning."""

from datetime import date, timedelta

from backend.app.evidence.models import (
    OpeningHoursEvidence,
    OpeningHoursPlanningDay,
    PlaceEvidence,
)


def _weekday_description(hours: OpeningHoursEvidence, day: date) -> str | None:
    full_name = day.strftime("%A").casefold()
    short_name = full_name[:3]
    for description in hours.weekday_descriptions:
        label = description.partition(":")[0].strip().casefold()
        if label in (full_name, short_name):
            return description
    return None


def opening_hours_for_date(place: PlaceEvidence, day: date) -> OpeningHoursPlanningDay:
    """Current seven-day evidence outranks the regular baseline only inside its window."""

    current = place.current_opening_hours
    if (
        current is not None
        and current.valid_from is not None
        and current.valid_through is not None
        and current.valid_from <= day <= current.valid_through
        and (description := _weekday_description(current, day)) is not None
    ):
        return OpeningHoursPlanningDay(
            date=day,
            basis="current_date_window",
            weekday_description=description,
            source_window_start=current.valid_from,
            source_window_end=current.valid_through,
        )
    regular = place.regular_opening_hours
    if regular is not None and (description := _weekday_description(regular, day)) is not None:
        return OpeningHoursPlanningDay(
            date=day,
            basis="regular_weekly_baseline",
            weekday_description=description,
        )
    return OpeningHoursPlanningDay(date=day, basis="unknown")


def planning_opening_hours(
    place: PlaceEvidence, start: date, end: date
) -> list[OpeningHoursPlanningDay]:
    """Expose one explicit hours basis for each requested inclusive trip date."""

    return [
        opening_hours_for_date(place, start + timedelta(days=offset))
        for offset in range((end - start).days + 1)
    ]
