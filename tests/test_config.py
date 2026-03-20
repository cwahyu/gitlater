# tests/test_config.py

from gitlater.config import load_config
from pathlib import Path


def test_default_config_when_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    config = load_config()

    assert config["mode"] == "personal"
    assert config["work_start"] == 9
    assert config["work_end"] == 18


def test_load_config_from_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    config_dir = Path(".gitlater")
    config_dir.mkdir()

    (config_dir / "config.toml").write_text(
        """
mode = "work"

[work_hours]
start = 8
end = 17
"""
    )

    config = load_config()

    assert config["mode"] == "work"
    assert config["work_start"] == 8
    assert config["work_end"] == 17


def test_invalid_config_fallback(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    config_dir = Path(".gitlater")
    config_dir.mkdir()

    # invalid TOML
    (config_dir / "config.toml").write_text("invalid = [")

    config = load_config()

    assert config["mode"] == "personal"
    assert config["work_start"] == 9
    assert config["work_end"] == 18
