# src/gitlater/version.py

import importlib.metadata
from pathlib import Path

import tomllib


def get_version() -> str:
    try:
        return importlib.metadata.version("gitlater")
    except importlib.metadata.PackageNotFoundError:
        pyproject = Path.cwd() / "pyproject.toml"
        if pyproject.exists():
            data = tomllib.loads(pyproject.read_text())
            return data["project"]["version"]

    return "0.0.0"
