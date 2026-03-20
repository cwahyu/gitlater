# src/gitlater/holidays.py

from pathlib import Path

HOLIDAY_FILE = Path(".gitlater") / "holidays.txt"


def load_holidays() -> set[str]:
    """
    Load holidays from .gitlater/holidays.txt
    Format:
        YYYY-MM-DD
        YYYY-MM-DD # comment
    """
    if not HOLIDAY_FILE.exists():
        return set()

    holidays = set()

    for line in HOLIDAY_FILE.read_text().splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        # remove inline comment
        if "#" in line:
            line = line.split("#", 1)[0].strip()

        if is_valid_date(line):
            holidays.add(line)

    return holidays


def is_valid_date(value: str) -> bool:
    """
    Very simple validation: YYYY-MM-DD
    """
    if len(value) != 10:
        return False

    parts = value.split("-")
    if len(parts) != 3:
        return False

    y, m, d = parts

    return y.isdigit() and m.isdigit() and d.isdigit()
