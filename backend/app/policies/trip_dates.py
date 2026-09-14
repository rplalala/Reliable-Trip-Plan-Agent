"""Shared project-wide trip-date policy."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import StrEnum
from typing import Protocol, runtime_checkable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from backend.app.schemas.itinerary import Itinerary
from backend.app.schemas.request import TravelRequirements

TRIP_DATE_WINDOW_DAYS = 10


@runtime_checkable
class DateProvider(Protocol):
    """Return the trusted calendar date for a new planning run."""

    def today(self) -> date:
        """Return the current runtime-local date."""

        ...


class SystemDateProvider:
    """Read the calendar date in one explicit application IANA time zone."""

    def __init__(
        self,
        time_zone: str | None = None,
        *,
        now: Callable[[ZoneInfo], datetime] = datetime.now,
    ) -> None:
        try:
            if time_zone is None:
                from backend.app.runtime.config_loader import load_runtime_config

                time_zone = load_runtime_config().app.time_zone
            self._time_zone = ZoneInfo(time_zone)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Unknown IANA time zone: {time_zone}") from exc
        self._now = now

    def today(self) -> date:
        """Return the configured-zone date at the point a run starts."""

        return self._now(self._time_zone).date()


@dataclass(frozen=True)
class TripDateWindow:
    """Immutable allowed date window captured once for a planning run."""

    reference_date: date
    allowed_start: date
    allowed_end: date


class TripDateErrorCode(StrEnum):
    """Stable reasons for rejecting requested or generated trip dates."""

    RANGE_REVERSED = "trip_date_range_reversed"
    BEFORE_WINDOW = "trip_date_before_window"
    AFTER_WINDOW = "trip_date_after_window"
    ITINERARY_OUTSIDE_REQUEST = "itinerary_date_outside_request"


class TripDatePolicyError(ValueError):
    """Describe a deterministic violation of the shared trip-date policy."""

    def __init__(
        self,
        *,
        code: TripDateErrorCode,
        window: TripDateWindow,
        start_date: date,
        end_date: date,
        offending_fields: tuple[str, ...] = (),
    ) -> None:
        self.code = code
        self.window = window
        self.start_date = start_date
        self.end_date = end_date
        self.offending_fields = offending_fields
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        if self.code is TripDateErrorCode.RANGE_REVERSED:
            return "end_date must be on or after start_date"
        if self.code is TripDateErrorCode.BEFORE_WINDOW:
            return (
                f"start_date must be on or after {self.window.allowed_start.isoformat()}"
            )
        if self.code is TripDateErrorCode.AFTER_WINDOW:
            return f"end_date must be on or before {self.window.allowed_end.isoformat()}"
        fields = ", ".join(self.offending_fields)
        return f"final itinerary dates must stay within the requested trip dates: {fields}"

    def as_detail(self) -> dict[str, object]:
        """Return a JSON-safe API or CLI error detail."""

        detail: dict[str, object] = {
            "code": self.code.value,
            "message": str(self),
            "reference_date": self.window.reference_date.isoformat(),
            "allowed_start": self.window.allowed_start.isoformat(),
            "allowed_end": self.window.allowed_end.isoformat(),
            "requested_start": self.start_date.isoformat(),
            "requested_end": self.end_date.isoformat(),
        }
        if self.offending_fields:
            detail["offending_fields"] = list(self.offending_fields)
        return detail


def create_trip_date_window(reference_date: date) -> TripDateWindow:
    """Compute the inclusive ten-day window for one fixed reference date."""

    return TripDateWindow(
        reference_date=reference_date,
        allowed_start=reference_date,
        allowed_end=reference_date + timedelta(days=TRIP_DATE_WINDOW_DAYS - 1),
    )


def validate_requested_trip_dates(
    start_date: date,
    end_date: date,
    window: TripDateWindow,
) -> None:
    """Require the complete requested range to stay inside the allowed window."""

    if end_date < start_date:
        raise TripDatePolicyError(
            code=TripDateErrorCode.RANGE_REVERSED,
            window=window,
            start_date=start_date,
            end_date=end_date,
        )
    if start_date < window.allowed_start:
        raise TripDatePolicyError(
            code=TripDateErrorCode.BEFORE_WINDOW,
            window=window,
            start_date=start_date,
            end_date=end_date,
        )
    if end_date > window.allowed_end:
        raise TripDatePolicyError(
            code=TripDateErrorCode.AFTER_WINDOW,
            window=window,
            start_date=start_date,
            end_date=end_date,
        )


def validate_itinerary_dates(
    requirements: TravelRequirements,
    itinerary: Itinerary,
    window: TripDateWindow,
) -> None:
    """Require every generated itinerary date to remain inside the requested range."""

    if requirements.start_date is None or requirements.end_date is None:
        raise ValueError("complete requested trip dates are required")

    requested_start = requirements.start_date
    requested_end = requirements.end_date
    validate_requested_trip_dates(requested_start, requested_end, window)

    itinerary_dates: list[tuple[str, date]] = [
        ("itinerary.start_date", itinerary.start_date),
        ("itinerary.end_date", itinerary.end_date),
    ]
    for day_index, day in enumerate(itinerary.days):
        itinerary_dates.append((f"itinerary.days[{day_index}].date", day.date))
        for activity_index, activity in enumerate(day.activities):
            activity_path = f"itinerary.days[{day_index}].activities[{activity_index}]"
            itinerary_dates.extend(
                (
                    (f"{activity_path}.start_time", activity.start_time.date()),
                    (f"{activity_path}.end_time", activity.end_time.date()),
                )
            )

    offending_fields = tuple(
        field_path
        for field_path, value in itinerary_dates
        if value < requested_start or value > requested_end
    )
    if offending_fields:
        raise TripDatePolicyError(
            code=TripDateErrorCode.ITINERARY_OUTSIDE_REQUEST,
            window=window,
            start_date=requested_start,
            end_date=requested_end,
            offending_fields=offending_fields,
        )
