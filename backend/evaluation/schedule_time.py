"""Independent civil-date and instant preparation; never use the host timezone."""

import re
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Span:
    """A positive half-open interval between UTC instants."""

    start: datetime
    end: datetime

    @property
    def seconds(self) -> float:
        return (self.end - self.start).total_seconds()

    def to_dict(self) -> dict:
        return {
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "seconds": self.seconds,
        }


@dataclass(frozen=True)
class IntervalResult:
    status: str
    span: Span | None
    reasons: tuple[str, ...]
    date_consistent: bool
    original_start: object
    original_end: object

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "interval": self.span.to_dict() if self.span else None,
            "reasons": list(self.reasons),
            "date_consistent": self.date_consistent,
            "original_start": self.original_start,
            "original_end": self.original_end,
        }


def _instant(value: datetime, timezone: str | None) -> tuple[datetime | None, str | None]:
    if value.utcoffset() is not None:
        if timezone:
            local = value.astimezone(ZoneInfo(timezone))
            if (
                value.replace(tzinfo=None) != local.replace(tzinfo=None)
                or value.utcoffset() != local.utcoffset()
            ):
                return None, "timezone_offset_conflict"
        return value.astimezone(UTC), None
    if not timezone:
        return None, "timezone_missing"
    zone = ZoneInfo(timezone)
    candidates = set()
    for fold in (0, 1):
        instant = value.replace(tzinfo=zone, fold=fold).astimezone(UTC)
        if instant.astimezone(zone).replace(tzinfo=None) == value:
            candidates.add(instant)
    if len(candidates) != 1:
        return None, "dst_fold" if candidates else "dst_gap"
    return candidates.pop(), None


def _timestamp(value) -> tuple[datetime | None, str | None]:
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}[T ][0-9]{2}:[0-9]{2}"
        r"(?::[0-9]{2}(?:\.[0-9]+)?)?(?:Z|[+-][0-9]{2}:[0-9]{2})?",
        value,
    ):
        return None, "invalid_timestamp"
    fraction = re.search(r"\.([0-9]+)", value)
    if fraction and len(fraction[1]) > 6:
        return None, "unsupported_timestamp_precision"
    try:
        return datetime.fromisoformat(value), None
    except ValueError:
        return None, "invalid_timestamp"


def normalize_interval(
    start, end, declared_day, timezone=None, *, allow_day_end=False, allow_cross_date=False
) -> IntervalResult:
    """Preserve missingness and civil-date disagreement separately from valid instants."""
    parsed = [_timestamp(value) for value in (start, end)]

    def matches_day(value, index):
        return value.date().isoformat() == declared_day or (
            index == 1
            and allow_cross_date
            and value.date() > date.fromisoformat(declared_day)
        ) or (
            index == 1
            and allow_day_end
            and value.date() == date.fromisoformat(declared_day) + timedelta(days=1)
            and value.time().replace(tzinfo=None) == time.min
        )

    consistent = all(matches_day(value, i) for i, (value, _) in enumerate(parsed) if value)
    if timezone:
        consistent = consistent and all(
            matches_day(value.astimezone(ZoneInfo(timezone)), i)
            for i, (value, _) in enumerate(parsed)
            if value is not None and value.utcoffset() is not None
        )
    reasons = tuple(dict.fromkeys(reason for _, reason in parsed if reason))
    if not consistent:
        return IntervalResult("unknown", None, ("declared_date_mismatch",), False, start, end)
    if reasons:
        return IntervalResult("unknown", None, reasons, True, start, end)
    instants = [_instant(value, timezone) for value, _ in parsed]
    reasons = tuple(dict.fromkeys(reason for _, reason in instants if reason))
    if reasons:
        return IntervalResult("unknown", None, reasons, True, start, end)
    first, last = [value for value, _ in instants]
    if first >= last:
        return IntervalResult("unknown", None, ("nonpositive_interval",), True, start, end)
    return IntervalResult("known", Span(first, last), (), True, start, end)


def expand_protection(obligation, timezone=None) -> IntervalResult:
    """Expand a reviewed protection using civil midnight, including DST day lengths."""
    day = obligation["date"]
    interval = obligation["interval"]
    start = "00:00" if interval["kind"] == "full_day" else interval["start"]
    end = "24:00" if interval["kind"] == "full_day" else interval["end"]
    if end in ("24:00", "24:00:00"):
        end_day = (date.fromisoformat(day) + timedelta(days=1)).isoformat()
        end_value = end_day + "T00:00:00"
    else:
        end_value = day + "T" + end
    return normalize_interval(day + "T" + start, end_value, day, timezone, allow_day_end=True)
