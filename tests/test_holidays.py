# tests/test_holidays.py

from pathlib import Path

from gitlater.holidays import load_holidays


def test_load_holidays_basic(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    d = Path(".gitlater")
    d.mkdir()

    (d / "holidays.txt").write_text(
        """
2026-01-01
2026-08-17 # Independence Day
"""
    )

    holidays = load_holidays()

    assert "2026-01-01" in holidays
    assert "2026-08-17" in holidays


def test_load_holidays_ignore_comments(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    d = Path(".gitlater")
    d.mkdir()

    (d / "holidays.txt").write_text(
        """
# comment
2026-01-01
"""
    )

    holidays = load_holidays()

    assert holidays == {"2026-01-01"}


def test_load_holidays_missing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    holidays = load_holidays()

    assert holidays == set()
