# gitlater

Respect your time boundaries in git workflows.

## What is this?

`gitlater` is a small CLI tool that helps you **commit at the right time**.

It doesn’t optimize productivity.
It protects your boundaries.

## Why?

Sometimes the problem is not:

- writing code
- committing code

But **when** you do it.

`gitlater` helps you say:

> “This is the time I work on this project. Not now.”

## Features (v0.1.1)

- simple time-based commit guard
- two modes:
  - `personal` → allow outside working hours
  - `work` → allow during working hours
- weekend & holiday awareness
- project-level configuration
- zero external dependencies

## Installation

### Using pipx (recommended)

```bash
pipx install gitlater
```

### Using uv

```bash
uv tool install gitlater
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
```

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
