"""Select only temporally applicable Places opening hours for V1 planning."""

from datetime import date, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

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

    view = selected_hours(place, day)
    if view["known"] or view["reason"] in {
        "current_special_or_invalid_periods",
        "invalid_structured_period",
        "current_special_date_without_usable_periods",
    }:
        source = (
            place.current_opening_hours
            if view["basis"] == "current_date_window"
            else place.regular_opening_hours
            if view["basis"] == "regular_weekly_baseline"
            else None
        )
        return OpeningHoursPlanningDay(
            weekday_description=_weekday_description(source, day) if source else None,
            date=day,
            basis=view["basis"],
            structured_known=view["known"],
            structured_reason=view["reason"],
            intervals=view["intervals"],
            source_window_start=source.valid_from if source else None,
            source_window_end=source.valid_through if source else None,
        )
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


def selected_hours(place, day, effective=None):
    """Select structured local intervals, retaining provenance and explicit unknown reasons.

    Intervals use naive venue-local datetimes. Text descriptions are never parsed.
    """
    from datetime import datetime

    result = dict(
        date=str(day),
        place_id=place.place_id,
        source_ref=place.source_ref,
        retrieved_at=place.retrieved_at.isoformat(),
        timezone=place.timezone_id,
        basis="unknown",
        reason="structured_periods_unavailable",
        intervals=[],
        evidence_refs=[place.source_ref],
        known=False,
    )
    if effective is not None:
        operation = next((d for d in effective.operational_days if d.date == day), None)
        facts = [
            f
            for f in effective.facts
            if f.subject_scope == "whole_venue"
            and f.dimension in {"opening_hours", "operational_availability"}
            and f.temporal_basis == "explicit_date_or_range"
            and f.applicable_start_date
            and f.applicable_end_date
            and f.applicable_start_date <= day <= f.applicable_end_date
        ]
        if (
            operation
            and (operation.status == "unresolved_conflict" or operation.unresolved_reason)
            or any(f.relation in {"conflict", "unresolved"} or f.unresolved_reason for f in facts)
        ):
            return result | dict(reason="conflicting_operational_evidence")
        trusted = [f for f in facts if f.source_refs and f.authority_bases]
        refs = sorted({r for f in trusted for r in f.source_refs})
        if any(f.value_kind in {"temporary_closure", "permanent_closure"} for f in trusted):
            return result | dict(
                known=True,
                basis="special_evidence",
                reason="adopted_date_closed",
                evidence_refs=refs,
            )
        windows = [f for f in trusted if f.dimension == "opening_hours"]
        if windows:
            if any(
                f.opens_at is None
                or f.closes_at is None
                or f.schedule_scope != "daily"
                or f.opens_at.tzinfo
                or f.closes_at.tzinfo
                or f.opens_at >= f.closes_at
                for f in windows
            ):
                return result | dict(reason="special_hours_uninterpretable", evidence_refs=refs)
            intervals = []
            for f in windows:
                start, end = datetime.combine(day, f.opens_at), datetime.combine(day, f.closes_at)
                if end <= start:
                    end += timedelta(days=1)
                intervals.append((start, end))
            return result | dict(
                known=True,
                basis="special_evidence",
                reason="adopted_intervals",
                evidence_refs=refs,
                intervals=_merge_intervals(intervals),
            )
    current = place.current_opening_hours
    in_window = bool(
        current
        and current.valid_from
        and current.valid_through
        and current.valid_from <= day <= current.valid_through
    )
    if in_window:
        if current.periods_state == "present":
            return _period_view(result, current, day, "current_date_window")
        if current.periods_state == "invalid" or day in current.special_days:
            return result | dict(
                reason="current_special_or_invalid_periods", basis="current_date_window"
            )
    if current and day in current.special_days:
        return result | dict(reason="current_special_date_without_usable_periods")
    regular = place.regular_opening_hours
    if regular and regular.periods_state == "present":
        return _period_view(result, regular, day, "regular_weekly_baseline")
    state = regular.periods_state if regular else current.periods_state if current else "missing"
    return result | dict(reason=f"structured_periods_{state}")


def _merge_intervals(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return [(a.isoformat(), b.isoformat()) for a, b in merged]


def _period_view(result, hours, day, basis):
    from datetime import datetime, time

    midnight = datetime.combine(day, time())
    end_day = midnight + timedelta(days=1)
    intervals = []
    try:
        for period in hours.periods or []:
            opening, closing = period.get("open"), period.get("close")
            if not isinstance(opening, dict):
                raise ValueError("Missing opening endpoint")
            if (
                closing is None
                and "day" in opening
                and opening.get("day", 0) == 0
                and opening.get("hour", 0) == 0
                and opening.get("minute", 0) == 0
                and not opening.get("truncated", False)
                and not opening.get("date")
            ):
                intervals.append((midnight, end_day))
                continue
            if not isinstance(closing, dict):
                raise ValueError("Missing closing endpoint")
            # Weekly periods can start in the previous week, including overnight spans.
            for shift in (-7, 0, 7):
                start = _period_point(opening, day, shift)
                end = _period_point(closing, day, shift)
                if opening.get("truncated") and hours.valid_from:
                    start = datetime.combine(hours.valid_from, time())
                if closing.get("truncated") and hours.valid_through:
                    end = datetime.combine(hours.valid_through + timedelta(days=1), time())
                if end <= start and not closing.get("date"):
                    end += timedelta(days=7)
                if end <= start:
                    raise ValueError("Invalid interval")
                if hours.valid_from and hours.valid_through:
                    start = max(start, datetime.combine(hours.valid_from, time()))
                    end = min(
                        end, datetime.combine(hours.valid_through + timedelta(days=1), time())
                    )
                if start < end_day and end > midnight:
                    intervals.append((max(start, midnight), min(end, end_day)))
    except (ValueError, TypeError, KeyError, OverflowError):
        return result | dict(reason="invalid_structured_period", basis=basis)
    return result | dict(
        known=True,
        basis=basis,
        reason="adopted_intervals" if intervals else "adopted_date_closed",
        intervals=_merge_intervals(intervals),
        source_window_start=str(hours.valid_from) if hours.valid_from else None,
        source_window_end=str(hours.valid_through) if hours.valid_through else None,
    )


def _period_point(point, day, shift):
    from datetime import datetime, time

    if "date" not in point and "day" not in point:
        raise ValueError("Endpoint weekday missing")
    raw_date = point.get("date")
    if raw_date is not None:
        actual = date(raw_date["year"], raw_date["month"], raw_date["day"])
    else:
        weekday = point.get("day", 0)
        if type(weekday) is not int or not 0 <= weekday <= 6:
            raise ValueError("Invalid weekday")
        sunday = day - timedelta(days=(day.weekday() + 1) % 7)
        actual = sunday + timedelta(days=weekday + shift)
    hour, minute = point.get("hour", 0), point.get("minute", 0)
    if type(hour) is not int or type(minute) is not int:
        raise ValueError("Invalid endpoint time")
    return datetime.combine(actual, time(hour, minute))


def assess_opening(activity, place, effective=None, binding=None):
    """Evaluate the complete visit against adopted API/special intervals, not admission."""
    from datetime import datetime

    audit = dict(
        policy="explicit_visit_binding" if binding else "application_default",
        access_mode=binding.mode if binding else "obey_place_hours",
    )
    if binding and binding.mode != "venue_entry":
        return "UNKNOWN", "explicit_visit_scope_not_established_by_venue_hours", (), None, audit
    if not place.timezone_id or activity.start_time.utcoffset() is None:
        return "UNKNOWN", "venue_timezone_or_activity_offset_missing", (), None, audit
    try:
        zone = ZoneInfo(place.timezone_id)
    except ZoneInfoNotFoundError:
        return "UNKNOWN", "venue_timezone_unrecognized", (), None, audit
    start, end = (
        v.astimezone(zone).replace(tzinfo=None) for v in (activity.start_time, activity.end_time)
    )
    views = [
        selected_hours(place, start.date() + timedelta(days=i), effective)
        for i in range((end.date() - start.date()).days + 1)
        if datetime.combine(start.date() + timedelta(days=i), datetime.min.time()) < end
    ]
    audit["selected_hours"] = views
    if not views or any(not v["known"] for v in views):
        reason = next((v["reason"] for v in views if not v["known"]), "empty_visit_interval")
        return "UNKNOWN", reason, (), None, audit
    intervals = [
        (datetime.fromisoformat(a), datetime.fromisoformat(b))
        for v in views
        for a, b in v["intervals"]
    ]
    merged = _merge_intervals(intervals)
    covered = sum(
        max(
            0,
            (
                min(end, datetime.fromisoformat(b)) - max(start, datetime.fromisoformat(a))
            ).total_seconds(),
        )
        for a, b in merged
    )
    deficit = max(0, (end - start).total_seconds() - covered)
    refs = tuple(sorted({r for v in views for r in v["evidence_refs"]}))
    return (
        "CONFIRMED" if deficit else "PASS",
        "outside_adopted_hours" if deficit else "adopted_hours_only",
        refs,
        deficit,
        audit,
    )


def with_context_timezone(place, relevant_places):
    """Borrow only a unique reliable timezone from the related scheduled context."""
    if place.timezone_id:
        return place
    zones = {p.timezone_id for p in relevant_places if p.timezone_id}
    if len(zones) != 1:
        return place
    value = next(iter(zones))
    try:
        zone = ZoneInfo(value)
    except ZoneInfoNotFoundError:
        return place
    current = place.current_opening_hours
    if current and current.valid_from is None and place.requested_at is not None:
        start = place.requested_at.astimezone(zone).date()
        current = current.model_copy(
            update={"valid_from": start, "valid_through": start + timedelta(days=6)}
        )
    return place.model_copy(update={"timezone_id": value, "current_opening_hours": current})
