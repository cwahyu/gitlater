# tests/test_version.py


import importlib.metadata

from gitlater.version import get_version


def test_get_version_from_installed_package(monkeypatch):
    # simulate installed package
    monkeypatch.setattr(
        importlib.metadata,
        "version",
        lambda name: "1.2.3",
    )

    assert get_version() == "1.2.3"


def test_get_version_from_pyproject(tmp_path, monkeypatch):
    # simulate package not installed
    def raise_not_found(name):
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(importlib.metadata, "version", raise_not_found)

    # create fake pyproject.toml
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """
[project]
version = "0.9.0"
"""
    )

    # change working directory
    monkeypatch.chdir(tmp_path)

    assert get_version() == "0.9.0"


def test_get_version_default(monkeypatch, tmp_path):
    # simulate package not installed
    def raise_not_found(name):
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(importlib.metadata, "version", raise_not_found)

    # empty directory (no pyproject.toml)
    monkeypatch.chdir(tmp_path)

    assert get_version() == "0.0.0"
