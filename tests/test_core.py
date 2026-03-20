# tests/test_core.py

from datetime import datetime

from gitlater.core import is_allowed, next_allowed_time


def test_personal_allows_outside_working_hours():
    allowed = is_allowed(
        mode="personal",
        weekend=False,
        working_hours=False,
        holiday=False,
    )
    assert allowed is True


def test_personal_blocks_working_hours_weekday():
    allowed = is_allowed(
        mode="personal",
        weekend=False,
        working_hours=True,
        holiday=False,
    )
    assert allowed is False


def test_personal_allows_weekend():
    allowed = is_allowed(
        mode="personal",
        weekend=True,
        working_hours=True,
        holiday=False,
    )
    assert allowed is True


def test_personal_allows_holiday():
    allowed = is_allowed(
        mode="personal",
        weekend=False,
        working_hours=True,
        holiday=True,
    )
    assert allowed is True


def test_work_allows_working_hours_weekday():
    allowed = is_allowed(
        mode="work",
        weekend=False,
        working_hours=True,
        holiday=False,
    )
    assert allowed is True


def test_work_blocks_outside_working_hours():
    allowed = is_allowed(
        mode="work",
        weekend=False,
        working_hours=False,
        holiday=False,
    )
    assert allowed is False


def test_work_blocks_weekend():
    allowed = is_allowed(
        mode="work",
        weekend=True,
        working_hours=True,
        holiday=False,
    )
    assert allowed is False


def test_work_blocks_holiday():
    allowed = is_allowed(
        mode="work",
        weekend=False,
        working_hours=True,
        holiday=True,
    )
    assert allowed is False


def test_next_window_skips_weekend_and_holiday():
    # Friday, after working hours
    now = datetime(2026, 8, 14, 18, 30)  # Friday

    # Weekend (15-16), Monday is holiday (17)
    holidays = {"2026-08-17"}

    result = next_allowed_time(
        now=now,
        start=9,
        end=18,
        holidays=holidays,
        mode="work",
    )

    # Expect Tuesday (18th) 09:00
    assert result == "Tuesday 09:00"


def test_next_window_same_day_before_start():
    now = datetime(2026, 8, 14, 7, 0)  # before work hours

    holidays = set()

    result = next_allowed_time(
        now=now,
        start=9,
        end=18,
        holidays=holidays,
        mode="work",
    )

    assert result == "09:00"


def test_work_mode_after_hours_goes_to_next_business_day():
    # Friday after working hours
    now = datetime(2026, 8, 14, 19, 0)  # Friday

    holidays = set()

    result = next_allowed_time(
        now=now,
        start=9,
        end=18,
        holidays=holidays,
        mode="work",
    )

    # Expect next Monday
    assert result == "Monday 09:00"
