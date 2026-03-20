# src/gitlater/config.py

from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    tomllib = None


CONFIG_DIR = Path(".gitlater")
CONFIG_FILE = CONFIG_DIR / "config.toml"


DEFAULT_CONFIG = {
    "mode": "personal",
    "work_start": 9,
    "work_end": 18,
}


def load_config() -> dict:
    """
    Load config from .gitlater/config.toml
    Fallback to defaults if not found or invalid
    """
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()

    if tomllib is None:
        # no TOML parser available → fallback
        return DEFAULT_CONFIG.copy()

    try:
        data = tomllib.loads(CONFIG_FILE.read_text())
    except Exception:
        return DEFAULT_CONFIG.copy()

    return normalize_config(data)


def normalize_config(data: dict) -> dict:
    """
    Normalize TOML structure into flat config
    """
    config = DEFAULT_CONFIG.copy()

    # mode
    if isinstance(data.get("mode"), str):
        config["mode"] = data["mode"]

    # work_hours table
    work_hours = data.get("work_hours", {})

    if isinstance(work_hours.get("start"), int):
        config["work_start"] = work_hours["start"]

    if isinstance(work_hours.get("end"), int):
        config["work_end"] = work_hours["end"]

    return config
