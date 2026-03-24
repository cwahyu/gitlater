# src/gitlater/__init__.py

from gitlater.core import check_allowed


def allow() -> bool:
    allowed, _ = check_allowed()
    return allowed


def status() -> tuple[bool, str]:
    return check_allowed()


def guard() -> None:
    import sys

    allowed, message = check_allowed()

    if not allowed:
        print(message)
        sys.exit(1)
