from pathlib import Path


CONFIG_DIR = Path(".gitlater")
CONFIG_FILE = CONFIG_DIR / "config.toml"
HOLIDAY_FILE = CONFIG_DIR / "holidays.txt"


DEFAULT_CONFIG = """mode = "personal"

[work_hours]
start = 9
end = 18
"""


def run_init() -> None:
    if CONFIG_DIR.exists():
        print("gitlater: already initialized")
        return

    CONFIG_DIR.mkdir()

    CONFIG_FILE.write_text(DEFAULT_CONFIG)
    HOLIDAY_FILE.write_text("# YYYY-MM-DD\n")

    print("✨ gitlater initialized")
    print("")
    print("Created:")
    print(f"  {CONFIG_FILE}")
    print(f"  {HOLIDAY_FILE}")