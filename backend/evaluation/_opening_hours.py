"""Private civil-calendar expansion of original Places opening observations."""

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from .occupancy import intersections, union
from .schedule_time import Span, normalize_interval


class HoursError(ValueError):
    """A provider semantic defect, not corrupt delivery material."""


def subtract(scope, covered):
    """Subtract known spans while preserving exact datetime boundaries."""
    result = []
    for span in union(scope):
        cursor = span.start
        for item in intersections([span], covered):
            if cursor < item.start:
                result.append(Span(cursor, item.start))
            cursor = item.end
        if cursor < span.end:
            result.append(Span(cursor, span.end))
    return result


def seconds(spans):
    return sum((s.end - s.start) // timedelta(microseconds=1) for s in spans) / 1_000_000


def _point(raw):
    if not isinstance(raw, dict):
        raise HoursError("point_invalid")
    if not {"day", "hour", "minute"} <= raw.keys():
        raise HoursError("point_components_missing")
    for key, maximum in (("day", 6), ("hour", 23), ("minute", 59)):
        if type(raw[key]) is not int or not 0 <= raw[key] <= maximum:
            raise HoursError("point_components_invalid")
    if type(raw.get("truncated", False)) is not bool:
        raise HoursError("truncation_invalid")
    if "date" in raw:
        day = _date(raw["date"])
        if (day.weekday() + 1) % 7 != raw["day"]:
            raise HoursError("point_date_weekday_conflict")
    return raw


def _span(start_day, start, end_day, end, zone):
    a = datetime.combine(start_day, time(start["hour"], start["minute"]))
    b = datetime.combine(end_day, time(end["hour"], end["minute"]))
    interval = normalize_interval(
        a.isoformat(), b.isoformat(), start_day.isoformat(), zone, allow_cross_date=True
    )
    if interval.span is None:
        raise HoursError(interval.reasons[0])
    return interval.span


def _periods(hours):
    if hours is None:
        raise HoursError("hours_missing")
    if not isinstance(hours, dict):
        raise HoursError("hours_invalid")
    if "periods" not in hours:
        raise HoursError("periods_missing")
    if not isinstance(hours["periods"], list):
        raise HoursError("periods_invalid")
    return hours["periods"]


def regular(hours, scope, zone):
    try:
        periods = _periods(hours)
    except HoursError as exc:
        return [], [], [str(exc)]
    opened, reasons = [], []
    visit_first = scope.start.astimezone(ZoneInfo(zone)).date()
    first = visit_first - timedelta(days=7)
    last = (scope.end - timedelta(microseconds=1)).astimezone(ZoneInfo(zone)).date()
    for item in periods:
        try:
            if not isinstance(item, dict) or "open" not in item:
                raise HoursError("period_invalid")
            start = _point(item["open"])
            if start.get("truncated") or "date" in start:
                raise HoursError("regular_point_scope_invalid")
            if "close" not in item:
                if len(periods) == 1 and (start["day"], start["hour"], start["minute"]) == (
                    0,
                    0,
                    0,
                ):
                    opened.append(scope)
                    continue
                raise HoursError("close_missing")
            end = _point(item["close"])
            if end.get("truncated") or "date" in end:
                raise HoursError("regular_point_scope_invalid")
            delta = (end["day"] - start["day"]) % 7
            if delta == 0:
                if (end["hour"], end["minute"]) == (start["hour"], start["minute"]):
                    raise HoursError("nonpositive_period")
                if (end["hour"], end["minute"]) < (start["hour"], start["minute"]):
                    delta = 7
            day = first
            while day <= last:
                if (day.weekday() + 1) % 7 == start["day"]:
                    try:
                        opened.append(_span(day, start, day + timedelta(days=delta), end, zone))
                    except HoursError as exc:
                        if day <= last and day + timedelta(days=delta) >= visit_first:
                            reasons.append(str(exc))
                day += timedelta(days=1)
        except HoursError as exc:
            reasons.append(str(exc))
    opened = intersections([scope], opened)
    return opened, [] if reasons else subtract([scope], opened), list(dict.fromkeys(reasons))


def _date(value):
    if (
        not isinstance(value, dict)
        or not {"year", "month", "day"} <= value.keys()
        or any(type(value[k]) is not int for k in ("year", "month", "day"))
    ):
        raise HoursError("point_date_invalid")
    try:
        return date(value["year"], value["month"], value["day"])
    except ValueError as exc:
        raise HoursError("point_date_invalid") from exc


def _midnight(day, zone):
    value = datetime.combine(day, time.min).isoformat()
    end = datetime.combine(day + timedelta(days=1), time.min).isoformat()
    interval = normalize_interval(value, end, day.isoformat(), zone, allow_cross_date=True)
    if not interval.span:
        raise HoursError(interval.reasons[0])
    return interval.span


def _current_day(point, window_start):
    if "date" in point:
        return _date(point["date"])
    return window_start + timedelta(days=(point["day"] - (window_start.weekday() + 1)) % 7)


def current(hours, scope, zone, window_start, collection_crossed_date):
    """Bound completeness to the observed window; defects retain affected unknown dates."""
    try:
        periods = _periods(hours)
    except HoursError as exc:
        return [], [], [str(exc)]
    opened, incomplete, reasons = [], [], []
    if collection_crossed_date:
        incomplete.append(scope)
        reasons.append("current_collection_date_uncertain")
    window_end = window_start + timedelta(days=6)
    for item in periods:
        affected = [scope]
        try:
            if not isinstance(item, dict) or "open" not in item:
                raise HoursError("period_invalid")
            # A malformed clock with independently valid explicit dates can only affect
            # those calendar dates. Without such bounds, completeness is unknown globally.
            if all(isinstance(item.get(k), dict) and "date" in item[k] for k in ("open", "close")):
                first, last = (_date(item[k]["date"]) for k in ("open", "close"))
                dates_consistent = all(
                    type(item[k].get("day")) is int and item[k]["day"] == (day.weekday() + 1) % 7
                    for k, day in (("open", first), ("close", last))
                )
                if dates_consistent and window_start <= first <= last <= window_end:
                    affected = [
                        _midnight(first + timedelta(days=i), zone)
                        for i in range((last - first).days + 1)
                    ]
            start = _point(item["open"])
            if "close" not in item:
                raise HoursError("close_missing")
            end = _point(item["close"])
            if collection_crossed_date and ("date" not in start or "date" not in end):
                raise HoursError("current_collection_date_uncertain")
            first, last = _current_day(start, window_start), _current_day(end, window_start)
            if not window_start <= first <= last <= window_end:
                raise HoursError("current_period_outside_window")
            if start.get("truncated") and (
                first != window_start or (start["hour"], start["minute"]) != (0, 0)
            ):
                raise HoursError("truncated_open_boundary_invalid")
            if end.get("truncated") and (
                last != window_end or (end["hour"], end["minute"]) != (23, 59)
            ):
                raise HoursError("truncated_close_boundary_invalid")
            span = _span(first, start, last, end, zone)
            opened.append(span)
            if end.get("truncated"):
                incomplete.append(Span(span.end, _midnight(last, zone).end))
                reasons.append("truncated_boundary_unknown")
        except HoursError as exc:
            reasons.append(str(exc))
            incomplete.extend(affected)
    opened = intersections([scope], opened)
    closed = subtract(subtract([scope], incomplete), opened)
    return opened, closed, list(dict.fromkeys(reasons))


def _special_dates(payload):
    days = set()
    for field in ("currentOpeningHours", "regularOpeningHours"):
        hours = payload.get(field)
        if isinstance(hours, dict) and "specialDays" in hours:
            special = hours["specialDays"]
            if not isinstance(special, list):
                return days, True
            for item in special:
                try:
                    days.add(_date(item.get("date") if isinstance(item, dict) else None))
                except HoursError:
                    return days, True
    return days, False


def availability(payload, visit, zone, requested_at, retrieved_at):
    """Select a basis per local date, keeping weaker fallback and missingness explicit."""
    timezone = ZoneInfo(zone)
    window_start = datetime.fromisoformat(requested_at).astimezone(timezone).date()
    retrieval_day = datetime.fromisoformat(retrieved_at).astimezone(timezone).date()
    first, last = visit.start.astimezone(timezone).date(), visit.end.astimezone(timezone).date()
    special_dates, special_invalid = _special_dates(payload)
    opened, closed, segments, reasons = [], [], [], []
    for i in range((last - first).days + 1):
        day = first + timedelta(days=i)
        try:
            scopes = intersections([visit], [_midnight(day, zone)])
        except HoursError as exc:
            reasons.append(str(exc))
            continue
        for scope in scopes:
            use_current = (
                "currentOpeningHours" in payload
                and window_start <= day <= window_start + timedelta(days=6)
            )
            basis = "current" if use_current else "regular"
            if use_current:
                a, b, issues = current(
                    payload["currentOpeningHours"],
                    scope,
                    zone,
                    window_start,
                    retrieval_day != window_start,
                )
                if (day in special_dates or special_invalid) and not a and not b:
                    issues.append("special_date_unresolved")
            elif day in special_dates or special_invalid:
                a, b, issues = [], [], ["special_date_unresolved"]
                basis = "unavailable"
            else:
                a, b, issues = regular(payload.get("regularOpeningHours"), scope, zone)
            opened.extend(a)
            closed.extend(b)
            reasons.extend(issues)
            segments.append(
                {
                    "date": day.isoformat(),
                    "interval": scope.to_dict(),
                    "basis": basis if a or b else "unavailable",
                    "selected_basis": "current" if use_current else "regular",
                    "hours_field": "currentOpeningHours" if use_current else "regularOpeningHours",
                    "current_window_start": window_start.isoformat(),
                    "current_window_end": (window_start + timedelta(days=6)).isoformat(),
                    "known_open": [s.to_dict() for s in a],
                    "known_closed": [s.to_dict() for s in b],
                    "unknown": [s.to_dict() for s in subtract([scope], a + b)],
                    "reasons": list(dict.fromkeys(issues)),
                }
            )
    return union(opened), union(closed), segments, list(dict.fromkeys(reasons))
