"""Exact official date and time spans, including realistic page spelling."""

from datetime import date, time

import pytest

from backend.app.policies.official_temporal import (
    parse_official_date_scope,
    parse_official_times,
)


@pytest.mark.parametrize(
    "text",
    [
        "2026-09-15",
        "15 September 2026",
        "September 15, 2026",
        "15 Sep 2026",
    ],
)
def test_single_date_forms(text) -> None:
    day = date(2026, 9, 15)
    assert parse_official_date_scope(text) == (day, day)


@pytest.mark.parametrize(
    "text",
    [
        "15–17 September 2026",
        "15-17 September 2026",
        "September 15–17, 2026",
        "September 15-17, 2026",
    ],
)
def test_both_range_endpoints_are_checked(text) -> None:
    assert parse_official_date_scope(text) == (date(2026, 9, 15), date(2026, 9, 17))


@pytest.mark.parametrize(
    "text",
    [
        "September 15–17",
        "15–17 September",
        "32 September 2026",
        "17–15 September 2026",
        "September 15–35, 2026",
    ],
)
def test_invalid_or_yearless_dates_are_not_inferred_from_task(text) -> None:
    assert parse_official_date_scope(text) is None


def test_realistic_twelve_hour_and_twenty_four_hour_times() -> None:
    assert parse_official_times("9am to 5pm") == (time(9), time(17))
    assert parse_official_times("9:30am–2pm") == (time(9, 30), time(14))
    assert parse_official_times("09:00–17:00") == (time(9), time(17))
