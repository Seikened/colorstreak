# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is this

`colorstreak` is a minimal Python library for colored terminal output using ANSI codes. It exposes a single `Logger` class with static methods (`.info()`, `.error()`, `.warning()`, etc.) that behave like `print()` (accept `sep`, `end`, `file`, `flush`). Published on PyPI.

## Commands

```bash
# Install / sync dependencies
uv sync

# Run the visual test (no test framework — manual visual check)
python test.py

# Build and publish to PyPI (requires .env.secret with UV_PUBLISH_TOKEN)
python publish.py
```

## Architecture

The entire library lives in one module:

- `colorstreak/logger.py` — the `Logger` class. All log methods are `@staticmethod` that delegate to the `@classmethod _print()`, which handles ANSI formatting based on level + style.
- `colorstreak/__init__.py` — re-exports `Logger`.

Key design decisions:
- **No dependencies at runtime** — only ANSI escape codes, no `rich` or `click` used by the library itself (those are dev/publish deps).
- **Three styles** controlled by `Logger.configure(style=...)` or `COLORSTREAK_STYLE` env var: `full` (default), `prefix`, `soft`.
- **`NO_COLOR` convention** — setting `NO_COLOR=1` disables all ANSI output.
- **Class-level state** — `STYLE` and `ENABLED` are `ClassVar` on `Logger`, configured globally via `configure()`.

## Publishing

`publish.py` is a Typer CLI that reads `UV_PUBLISH_TOKEN` from `.env.secret`, runs `uv build` + `uv publish`. The version is in `pyproject.toml` under `[project].version`. Remember to bump the version there before publishing.
