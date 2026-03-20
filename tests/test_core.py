# tests/test_core.py

from gitlater.core import is_allowed


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
