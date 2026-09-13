"""Strict parsing of date, time, and monetary spans quoted from official sources."""

import re
from datetime import date, time
from decimal import Decimal, InvalidOperation

_MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}
_MONTH = (
    r"(?:January|February|March|April|May|June|July|August|September|October|"
    r"November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
)
_SEPARATOR = r"\s*(?:[-\u2013\u2014]|to)\s*"
_ISO = re.compile(r"(\d{4})-(\d{2})-(\d{2})", re.I)
_DAY_RANGE = re.compile(rf"(\d{{1,2}}){_SEPARATOR}(\d{{1,2}})\s+({_MONTH})\s+(\d{{4}})", re.I)
_MONTH_RANGE = re.compile(rf"({_MONTH})\s+(\d{{1,2}}){_SEPARATOR}(\d{{1,2}}),?\s+(\d{{4}})", re.I)
_DAY_FIRST = re.compile(rf"(\d{{1,2}})\s+({_MONTH})\s+(\d{{4}})", re.I)
_MONTH_FIRST = re.compile(rf"({_MONTH})\s+(\d{{1,2}}),?\s+(\d{{4}})", re.I)
_TIME = re.compile(
    r"(?<!\w)(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b|(?<!\w)(\d{1,2}):(\d{2})(?!\w)", re.I
)
_NUMBER = re.compile(r"(?<![\w.])\d+(?:\.\d{1,2})?(?![\w.])")


def _month(value: str) -> int:
    return _MONTHS[value[:3].casefold()]


def parse_official_date_scope(value: str) -> tuple[date, date] | None:
    """Parse a complete explicit date span without borrowing a task year."""

    text = " ".join(value.strip().split())
    try:
        if match := _ISO.fullmatch(text):
            day = date(int(match[1]), int(match[2]), int(match[3]))
            return day, day
        if match := _DAY_RANGE.fullmatch(text):
            start = date(int(match[4]), _month(match[3]), int(match[1]))
            end = date(int(match[4]), _month(match[3]), int(match[2]))
            return (start, end) if start <= end else None
        if match := _MONTH_RANGE.fullmatch(text):
            start = date(int(match[4]), _month(match[1]), int(match[2]))
            end = date(int(match[4]), _month(match[1]), int(match[3]))
            return (start, end) if start <= end else None
        if match := _DAY_FIRST.fullmatch(text):
            day = date(int(match[3]), _month(match[2]), int(match[1]))
            return day, day
        if match := _MONTH_FIRST.fullmatch(text):
            day = date(int(match[3]), _month(match[1]), int(match[2]))
            return day, day
    except ValueError:
        return None
    return None


def parse_official_times(value: str) -> tuple[time, ...]:
    """Return source-visible clock values, including compact 12-hour spelling."""

    found: list[time] = []
    for match in _TIME.finditer(value):
        try:
            if match[3]:
                hour = int(match[1])
                if not 1 <= hour <= 12:
                    continue
                hour = hour % 12 + (12 if match[3].casefold() == "pm" else 0)
                minute = int(match[2] or "0")
            else:
                hour = int(match[4])
                minute = int(match[5])
            parsed = time(hour, minute)
        except ValueError:
            continue
        if parsed not in found:
            found.append(parsed)
    return tuple(found)


def parse_official_amounts(value: str) -> tuple[Decimal, ...]:
    found: list[Decimal] = []
    for match in _NUMBER.finditer(value.replace(",", "")):
        try:
            amount = Decimal(match.group())
        except InvalidOperation:
            continue
        if amount not in found:
            found.append(amount)
    return tuple(found)
