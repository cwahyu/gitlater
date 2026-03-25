# CHANGELOG

## v0.2.0

- add embed mode API:
  - `allow()` → boolean check
  - `status()` → returns (allowed, message)
  - `guard()` → enforce and exit

This allows gitlater to be used directly in Python scripts,
not only as a CLI or pre-commit hook.

## v0.1.3

- add pre-commit hooks

## v0.1.2

- fix next window calculation in work mode (weekend + holiday aware)
- add tests for business day logic

## v0.1.1

- fix GitHub Actions configuration

## v0.1.0

Initial release
