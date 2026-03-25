# gitlater

Respect your time boundaries.

## What is this?

`gitlater` is a small tool that helps you **do things at the right time**.

Originally built for git commits, it now works anywhere —
CLI, pre-commit, or inside your Python scripts.

It doesn’t optimize productivity.
It protects your boundaries.

## Why?

Sometimes the problem is not:

- writing code
- committing code
- running scripts

But **when** you do it.

`gitlater` helps you say:

> “Not now. This can wait.”

## Features

- simple time-based commit guard
- two modes:
  - `personal` → allow outside working hours
  - `work` → allow during working hours
- weekend & holiday awareness
- project-level configuration
- zero external dependencies

## Installation

### Using pipx (recommended for CLI)

```bash
pipx install gitlater
```

### Using uv (CLI tool)

```bash
uv tool install gitlater
```

### Using uv (Python dependency)

```bash
uv add gitlater
```

### Local development

```bash
uv sync
uv run gitlater status
```

## Setup

Initialize in your project:

```bash
gitlater init
```

This creates:

```text
.gitlater/
  config.toml
  holidays.txt
```

## Configuration

### .gitlater/config.toml

```toml
mode = "personal"

[work_hours]
start = 9
end = 18
```

### .gitlater/holidays.txt

```text
2026-01-01 # New Year
2026-08-17 # Independence Day
```

## Pre-commit integration

Add to your local pre-commit config:

```yaml
- repo: local
  hooks:
    - id: gitlater
      name: git later
      entry: gitlater check
      language: system
      stages: [pre-commit]
      pass_filenames: false
```

`pass_filenames: false` ensures the check runs once (not per file).

## Usage

```bash
gitlater status
```

Example:

```text
🌙 Not now — this time is yours.

🗓 Friday • 10:08
⏳ Next window: 18:00
```

## Using in Python scripts

`gitlater` can also be used directly inside Python scripts.

### Basic check

```python
from gitlater import allow

if not allow():
    print("Skip execution")
    exit()

# run your logic
print("Running task...")
```

### Get status message

```python
from gitlater import status

allowed, message = status()

if not allowed:
    print(message)
else:
    print("Running task...")
```

### Enforce (exit automatically)

```python
from gitlater import guard

guard()

# only runs if allowed
print("Running task...")
```

### Notes

- Uses the same .gitlater/ configuration as the CLI
- Behavior depends on the current working directory
- No external dependencies required

## Philosophy

gitlater is intentionally simple.

- no remote API
- no auto-detection
- no global config

It doesn’t decide your schedule.

## Roadmap

Keep it boring.

Future improvements (if needed):

- better status output
- small UX refinements
- optional helpers (init, holidays)

## License

MIT
