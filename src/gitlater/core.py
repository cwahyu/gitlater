# src/gitlater/core.py

from datetime import datetime, time
from pathlib import Path

from gitlater.config import load_config
from gitlater.holidays import load_holidays


# ---------- Core Logic ----------


def check_allowed() -> tuple[bool, str]:
    now = datetime.now()

    config = load_config()
    holidays = load_holidays()

    mode = config["mode"]
    work_start = config["work_start"]
    work_end = config["work_end"]

    today_str = now.strftime("%Y-%m-%d")

    weekend = is_weekend(now)
    working_hours = is_working_hours(now, work_start, work_end)
    holiday = today_str in holidays

    allowed = is_allowed(
        mode=mode,
        weekend=weekend,
        working_hours=working_hours,
        holiday=holiday,
    )

    if allowed:
        return True, ""

    # blocked → generate message
    message = build_block_message(now, mode, work_start, work_end)
    return False, message


def get_status() -> str:
    now = datetime.now()

    config = load_config()
    holidays = load_holidays()

    mode = config["mode"]
    work_start = config["work_start"]
    work_end = config["work_end"]

    today_str = now.strftime("%Y-%m-%d")

    weekend = is_weekend(now)
    working_hours = is_working_hours(now, work_start, work_end)
    holiday = today_str in holidays

    allowed = is_allowed(
        mode=mode,
        weekend=weekend,
        working_hours=working_hours,
        holiday=holiday,
    )

    if allowed:
        return "✅ Allowed now"

    return build_block_message(now, mode, work_start, work_end)


# ---------- Rules ----------


def is_allowed(
    *,
    mode: str,
    weekend: bool,
    working_hours: bool,
    holiday: bool,
) -> bool:
    if mode == "personal":
        return weekend or holiday or not working_hours

    if mode == "work":
        return (not weekend) and working_hours and (not holiday)

    # fallback: allow
    return True


def is_weekend(now: datetime) -> bool:
    return now.weekday() >= 5  # 5=Sat, 6=Sun


def is_working_hours(now: datetime, start: int, end: int) -> bool:
    return start <= now.hour < end


# ---------- Message ----------


def build_block_message(now: datetime, mode: str, start: int, end: int) -> str:
    lines = []

    if mode == "personal":
        lines.append("🌙 Not now — this time is yours.")
    elif mode == "work":
        lines.append("⛔ Outside working window.")
    else:
        lines.append("⛔ Not allowed at this time.")

    lines.append(f"🗓 {now.strftime('%A')} • {now.strftime('%H:%M')}")
    lines.append(f"⏳ Next window: {next_allowed_time(now, start, end)}")
    return "\n".join([lines[0], "", *lines[1:]])


def next_allowed_time(now: datetime, start: int, end: int) -> str:
    today_start = datetime.combine(now.date(), time(start, 0))
    today_end = datetime.combine(now.date(), time(end, 0))

    if now < today_start:
        return f"{start:02d}:00"
    elif now < today_end:
        return f"{end:02d}:00"
    else:
        return "tomorrow"
