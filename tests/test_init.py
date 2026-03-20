# tests/test_init.py

from gitlater.init import run_init
from pathlib import Path


def test_init_creates_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    run_init()

    assert Path(".gitlater/config.toml").exists()
    assert Path(".gitlater/holidays.txt").exists()


def test_init_already_exists(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    Path(".gitlater").mkdir()

    run_init()  # should not crash
