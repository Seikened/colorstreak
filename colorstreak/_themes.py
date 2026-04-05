"""Rich themes and style mappings for RichLogger."""

from __future__ import annotations

from rich.theme import Theme

# Log level → numeric value (same convention as Python logging)
LEVEL_VALUES: dict[str, int] = {
    "debug": 10,
    "info": 20,
    "success": 25,
    "step": 25,
    "note": 15,
    "metric": 25,
    "library": 20,
    "warning": 30,
    "error": 40,
    "critical": 50,
    "title": 0,  # always shown
}

# Log level → emoji/icon
LEVEL_ICONS: dict[str, str] = {
    "debug": "\u2022",       # •
    "info": "\u2139",        # ℹ
    "success": "\u2714",     # ✔
    "step": "\u25b6",        # ▶
    "note": "\u266a",        # ♪
    "metric": "\u2261",      # ≡
    "library": "\u25c6",     # ◆
    "warning": "\u26a0",     # ⚠
    "error": "\u2718",       # ✘
    "critical": "\U0001f4a5", # 💥
    "title": "\u2605",      # ★
}

# Log level → Rich style string
LEVEL_STYLES: dict[str, str] = {
    "debug": "green",
    "info": "blue",
    "success": "bold green",
    "step": "cyan",
    "note": "dim white",
    "metric": "magenta",
    "library": "magenta",
    "warning": "bold yellow",
    "error": "bold red",
    "critical": "bold white on red",
    "title": "bold blue",
}

# Log level → short label for display
LEVEL_LABELS: dict[str, str] = {
    "debug": "DEBUG",
    "info": "INFO",
    "success": "OK",
    "step": "STEP",
    "note": "NOTE",
    "metric": "METRIC",
    "library": "LIB",
    "warning": "WARN",
    "error": "ERROR",
    "critical": "CRIT",
    "title": "TITLE",
}

# HTTP method colors
HTTP_METHOD_STYLES: dict[str, str] = {
    "GET": "bold green",
    "POST": "bold blue",
    "PUT": "bold yellow",
    "PATCH": "bold yellow",
    "DELETE": "bold red",
    "HEAD": "dim white",
    "OPTIONS": "dim white",
}

# Build the Rich Theme from our styles
COLORSTREAK_THEME = Theme({
    f"log.{level}": style for level, style in LEVEL_STYLES.items()
} | {
    "log.metadata": "dim cyan",
    "log.timestamp": "dim white",
    "log.separator": "dim white",
})
