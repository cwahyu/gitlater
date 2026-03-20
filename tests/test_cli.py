# tests/test_cli.py

import subprocess
import sys

from gitlater.cli import main


def test_cli_no_args(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["gitlater"])

    try:
        main()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "missing command" in captured.out


def test_cli_binary_runs():
    result = subprocess.run(["gitlater", "status"])
    assert result.returncode in (0, 1)


def test_cli_check(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["gitlater", "check"])

    try:
        main()
    except SystemExit as e:
        assert e.code in (0, 1)


def test_cli_status(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["gitlater", "status"])

    try:
        main()
    except SystemExit:
        pass

    captured = capsys.readouterr()
    assert captured.out


def test_cli_unknown(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["gitlater", "???"])

    try:
        main()
    except SystemExit as e:
        assert e.code == 1

    captured = capsys.readouterr()
    assert "unknown command" in captured.out
