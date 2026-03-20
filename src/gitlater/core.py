# src/gitlater/core.py

from datetime import datetime, time, timedelta

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
    message = build_block_message(now, mode, work_start, work_end, holidays)
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

    return build_block_message(now, mode, work_start, work_end, holidays)


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


def build_block_message(
    now: datetime,
    mode: str,
    start: int,
    end: int,
    holidays: set[str],
) -> str:
    lines = []

    if mode == "personal":
        lines.append("🌙 Not now — this time is yours.")
    elif mode == "work":
        lines.append("⛔ Outside working window.")
    else:
        lines.append("⛔ Not allowed at this time.")

    lines.append(f"🗓 {now.strftime('%A')} • {now.strftime('%H:%M')}")
    lines.append(
        f"⏳ Next window: {next_allowed_time(now, start, end, holidays, mode)}"
    )

    return "\n".join([lines[0], "", *lines[1:]])


def next_allowed_time(
    now: datetime,
    start: int,
    end: int,
    holidays: set[str],
    mode: str,
) -> str:
    # --- PERSONAL MODE (keep simple) ---
    if mode == "personal":
        today_start = datetime.combine(now.date(), time(start, 0))
        today_end = datetime.combine(now.date(), time(end, 0))

        if now < today_start:
            return f"{start:02d}:00"
        elif now < today_end:
            return f"{end:02d}:00"
        else:
            return "later"

    # --- WORK MODE (FIXED LOGIC) ---
    today_str = now.strftime("%Y-%m-%d")
    today_weekend = now.weekday() >= 5
    today_holiday = today_str in holidays

    today_start = datetime.combine(now.date(), time(start, 0))
    today_end = datetime.combine(now.date(), time(end, 0))

    # ✅ CASE 1: today is valid working day
    if not today_weekend and not today_holiday:
        if now < today_start:
            return f"{start:02d}:00"
        if now < today_end:
            return f"{end:02d}:00"

    # ❌ otherwise → find next valid day
    next_day = now.date()

    while True:
        next_day += timedelta(days=1)

        weekday = next_day.weekday()
        date_str = next_day.strftime("%Y-%m-%d")

        is_weekend = weekday >= 5
        is_holiday = date_str in holidays

        if not is_weekend and not is_holiday:
            return f"{next_day.strftime('%A')} {start:02d}:00"
