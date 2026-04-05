"""RichLogger — Beautiful terminal logging powered by Rich."""

from __future__ import annotations

import json as _json
import os
import sys
import time
from collections import Counter
from contextlib import contextmanager
from datetime import datetime
from difflib import unified_diff
from typing import Any, Iterator

from rich.console import Console
from rich.json import JSON
from rich.markup import escape
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from ._metadata import get_caller_metadata
from ._themes import (
    COLORSTREAK_THEME,
    HTTP_METHOD_STYLES,
    LEVEL_ICONS,
    LEVEL_LABELS,
    LEVEL_STYLES,
    LEVEL_VALUES,
)


class RichLogger:
    """
    Rich-powered logger with metadata, tables, panels, and more.

    Usage::

        from colorstreak import RichLogger

        log = RichLogger()
        log.info("Server started on port 8080")
        log.table([{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])
    """

    def __init__(
        self,
        *,
        level: str = "DEBUG",
        metadata: bool = True,
        timestamp: bool = True,
        style: str = "panel",
    ) -> None:
        self._console = Console(theme=COLORSTREAK_THEME)
        self._file_console: Console | None = None
        self._min_level = LEVEL_VALUES.get(level.lower(), 0)
        self._metadata = metadata
        self._timestamp = timestamp
        self._style = style  # "panel" | "inline" | "minimal"
        self._group_depth = 0
        self._counters: Counter[str] = Counter()

    # ── Configuration ──────────────────────────────────────────────

    def configure(
        self,
        *,
        level: str | None = None,
        metadata: bool | None = None,
        timestamp: bool | None = None,
        style: str | None = None,
    ) -> None:
        if level is not None:
            self._min_level = LEVEL_VALUES.get(level.lower(), 0)
        if metadata is not None:
            self._metadata = metadata
        if timestamp is not None:
            self._timestamp = timestamp
        if style is not None:
            if style not in {"panel", "inline", "minimal"}:
                raise ValueError("style must be: 'panel', 'inline', or 'minimal'")
            self._style = style

    # ── Internal helpers ───────────────────────────────────────────

    def _should_log(self, level: str) -> bool:
        return LEVEL_VALUES.get(level, 0) >= self._min_level

    def _format_metadata(self, meta: dict[str, Any]) -> str:
        parts: list[str] = []
        parts.append(f"[log.metadata]\U0001f4cd {meta['file']}:{meta['line']} \u2192 {meta['function']}()[/]")
        if self._timestamp:
            ts = datetime.now().strftime("%H:%M:%S")
            parts.append(f"[log.timestamp]{ts}[/]")
        return "  \u00b7  ".join(parts)

    def _print(self, text: str | Text, *, meta: dict[str, Any] | None = None) -> None:
        indent = "  \u2502 " * self._group_depth
        if indent:
            if isinstance(text, Text):
                text = Text(indent) + text
            else:
                text = indent + text
        self._console.print(text)
        if meta and self._metadata:
            meta_line = indent + "          " + self._format_metadata(meta)
            self._console.print(meta_line)
        if self._file_console:
            self._file_console.print(text)

    def _log(self, level: str, *values: object, stack_offset: int = 3) -> None:
        if not self._should_log(level):
            return

        icon = LEVEL_ICONS.get(level, "\u2022")
        label = LEVEL_LABELS.get(level, level.upper())
        style = LEVEL_STYLES.get(level, "white")
        message = " ".join("" if v is None else str(v) for v in values)
        meta = get_caller_metadata(stack_offset)

        if self._style == "minimal":
            line = Text(f" {icon}  {escape(message)}")
            line.stylize(style, 1, 2 + len(icon))
            self._print(line, meta=meta)

        elif self._style == "inline":
            text = Text()
            text.append(f" {icon}  ", style=style)
            text.append(f"{label:<5}", style=f"bold {style}")
            text.append(" \u2502 ", style="log.separator")
            text.append(escape(message))
            self._print(text, meta=meta)

        else:  # "panel"
            text = Text()
            text.append(f" {icon}  ", style=style)
            text.append(f"{label:<5}", style=f"bold {style}")
            text.append(" \u2502 ", style="log.separator")
            text.append(escape(message))
            self._print(text, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P0 — Core log levels
    # ══════════════════════════════════════════════════════════════

    def debug(self, *values: object) -> None:
        self._log("debug", *values)

    def info(self, *values: object) -> None:
        self._log("info", *values)

    def warning(self, *values: object) -> None:
        self._log("warning", *values)

    def error(self, *values: object) -> None:
        self._log("error", *values)

    def critical(self, *values: object) -> None:
        self._log("critical", *values)

    def success(self, *values: object) -> None:
        self._log("success", *values)

    def library(self, *values: object) -> None:
        self._log("library", *values)

    def step(self, *values: object) -> None:
        self._log("step", *values)

    def note(self, *values: object) -> None:
        self._log("note", *values)

    def metric(self, *values: object) -> None:
        self._log("metric", *values)

    def title(self, *values: object) -> None:
        self._log("title", *values)

    # ══════════════════════════════════════════════════════════════
    # P0 — log.table()
    # ══════════════════════════════════════════════════════════════

    def table(
        self,
        data: list[dict[str, Any]] | None = None,
        *,
        title: str | None = None,
        columns: list[str] | None = None,
        rows: list[list[Any]] | None = None,
    ) -> None:
        meta = get_caller_metadata(2)
        t = Table(title=title, show_header=True, header_style="bold cyan")

        if data:
            # Auto-detect columns from list of dicts
            cols = list(data[0].keys()) if data else []
            for c in cols:
                t.add_column(c)
            for row in data:
                t.add_row(*(str(row.get(c, "")) for c in cols))
        elif columns and rows:
            for c in columns:
                t.add_column(c)
            for row in rows:
                t.add_row(*(str(v) for v in row))
        else:
            self._console.print("[dim]log.table() called with no data[/]")
            return

        self._print(t, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P1 — log.json()
    # ══════════════════════════════════════════════════════════════

    def json(self, data: Any, *, title: str | None = None) -> None:
        meta = get_caller_metadata(2)
        raw = _json.dumps(data, indent=2, ensure_ascii=False, default=str)
        panel = Panel(
            JSON(raw),
            title=title or "{ JSON }",
            title_align="left",
            border_style="blue",
            padding=(0, 1),
        )
        self._print(panel, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P1 — log.exception()
    # ══════════════════════════════════════════════════════════════

    def exception(self, message: str = "An exception occurred") -> None:
        meta = get_caller_metadata(2)
        self._log("error", message, stack_offset=4)
        self._console.print_exception(show_locals=True)

    # ══════════════════════════════════════════════════════════════
    # P1 — log.benchmark()
    # ══════════════════════════════════════════════════════════════

    @contextmanager
    def benchmark(self, label: str = "Benchmark", *, slow_threshold: float = 2.0) -> Iterator[None]:
        meta = get_caller_metadata(3)
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start

            if elapsed >= slow_threshold:
                icon = "\u26a0"
                suffix = f"[bold yellow] SLOW[/]"
                style = "yellow"
            else:
                icon = "\u2714"
                suffix = ""
                style = "green"

            text = Text()
            text.append(" \u23f1  ", style="cyan")
            text.append("BENCH", style="bold cyan")
            text.append(" \u2502 ", style="log.separator")
            text.append(f"{escape(label)} ")
            text.append(f"\u2500\u2500 {elapsed:.3f}s ", style=style)
            text.append(f"{icon}")
            if suffix:
                text.append_text(Text.from_markup(suffix))

            self._print(text, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P1 — log.group()
    # ══════════════════════════════════════════════════════════════

    @contextmanager
    def group(self, title: str) -> Iterator[None]:
        meta = get_caller_metadata(3)
        indent = "  \u2502 " * self._group_depth
        start = time.perf_counter()

        self._console.print(f"{indent}[bold]\u25bc {escape(title)}[/]")
        self._group_depth += 1
        try:
            yield
        finally:
            self._group_depth -= 1
            elapsed = time.perf_counter() - start
            end_indent = "  \u2502 " * self._group_depth
            self._console.print(
                f"{end_indent}[dim]\u2570\u2500\u2500 {elapsed:.2f}s[/]"
            )

    # ══════════════════════════════════════════════════════════════
    # P1 — log.to_file()
    # ══════════════════════════════════════════════════════════════

    def to_file(self, path: str) -> None:
        fh = open(path, "a", encoding="utf-8")  # noqa: SIM115
        self._file_console = Console(
            file=fh,
            force_terminal=False,
            no_color=True,
            width=120,
        )

    # ══════════════════════════════════════════════════════════════
    # P2 — log.http()
    # ══════════════════════════════════════════════════════════════

    def http(
        self,
        method: str,
        path: str,
        *,
        status: int = 200,
        duration: float | None = None,
    ) -> None:
        meta = get_caller_metadata(2)
        method_upper = method.upper()
        method_style = HTTP_METHOD_STYLES.get(method_upper, "white")

        if status < 300:
            status_style = "green"
            status_icon = "\u2714"
        elif status < 400:
            status_style = "cyan"
            status_icon = "\u21aa"
        elif status < 500:
            status_style = "yellow"
            status_icon = "\u26a0"
        else:
            status_style = "red"
            status_icon = "\u2718"

        text = Text()
        text.append(" \u2192  ", style="dim")
        text.append(f"{method_upper:<7}", style=method_style)
        text.append(f"{path}  ", style="white")
        text.append("\u2500\u2500 ", style="dim")
        text.append(f"{status} {status_icon}", style=status_style)

        if duration is not None:
            if duration >= 1.0:
                dur_str = f"  {duration:.1f}s \U0001f40c"
            elif duration >= 0.1:
                dur_str = f"  {duration * 1000:.0f}ms"
            else:
                dur_str = f"  {duration * 1000:.0f}ms"
            text.append(dur_str, style="dim")

        self._print(text, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P2 — log.sql()
    # ══════════════════════════════════════════════════════════════

    def sql(self, query: str, *, title: str | None = None) -> None:
        meta = get_caller_metadata(2)
        syntax = Syntax(
            query.strip(),
            "sql",
            theme="monokai",
            padding=1,
        )
        panel = Panel(
            syntax,
            title=title or "\U0001f5c3  SQL",
            title_align="left",
            border_style="cyan",
            padding=(0, 1),
        )
        self._print(panel, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P2 — log.header()
    # ══════════════════════════════════════════════════════════════

    def header(
        self,
        title: str,
        *,
        version: str | None = None,
        **kwargs: Any,
    ) -> None:
        lines = Text()
        lines.append(f"\U0001f680 {title}\n\n", style="bold white")

        if version:
            lines.append(f"  version : {version}\n", style="cyan")

        for key, value in kwargs.items():
            lines.append(f"  {key:<8}: {value}\n", style="cyan")

        lines.append(f"  python  : {sys.version.split()[0]}\n", style="cyan")
        lines.append(f"  started : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", style="cyan")

        panel = Panel(
            lines,
            border_style="bold blue",
            padding=(1, 2),
        )
        self._console.print(panel)

    # ══════════════════════════════════════════════════════════════
    # P2 — log.env()
    # ══════════════════════════════════════════════════════════════

    _SECRET_KEYWORDS = {"SECRET", "KEY", "TOKEN", "PASSWORD", "PASS", "CREDENTIAL", "AUTH"}

    def env(self, *names: str) -> None:
        meta = get_caller_metadata(2)
        text = Text()
        text.append(" \U0001f510 ENV\n", style="bold cyan")

        for i, name in enumerate(names):
            is_last = i == len(names) - 1
            prefix = "\u2514\u2500\u2500" if is_last else "\u251c\u2500\u2500"
            value = os.environ.get(name)

            if value is None:
                text.append(f" {prefix} {name:<20}: ", style="dim")
                text.append("\u26a0 NOT SET\n", style="bold yellow")
            elif any(kw in name.upper() for kw in self._SECRET_KEYWORDS):
                masked = value[:3] + "****..." + value[-4:] if len(value) > 8 else "****"
                text.append(f" {prefix} {name:<20}: ", style="dim")
                text.append(f"{masked}  (masked)\n", style="yellow")
            else:
                text.append(f" {prefix} {name:<20}: ", style="dim")
                text.append(f"{value}\n", style="green")

        self._print(text, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P3 — log.inspect()
    # ══════════════════════════════════════════════════════════════

    def inspect(self, obj: Any, *, title: str | None = None, methods: bool = False) -> None:
        meta = get_caller_metadata(2)
        header = Text()
        header.append(f"\U0001f50d INSPECT \u2502 ", style="bold magenta")
        header.append(type(obj).__name__, style="bold white")
        self._print(header, meta=meta)
        self._console.print()

        from rich import inspect as _rich_inspect
        _rich_inspect(obj, methods=methods, title=title)

    # ══════════════════════════════════════════════════════════════
    # P3 — log.code()
    # ══════════════════════════════════════════════════════════════

    def code(
        self,
        source: str,
        *,
        language: str = "python",
        title: str | None = None,
        line_numbers: bool = True,
    ) -> None:
        meta = get_caller_metadata(2)
        syntax = Syntax(
            source.strip(),
            language,
            theme="monokai",
            line_numbers=line_numbers,
            padding=1,
        )
        panel = Panel(
            syntax,
            title=title or f"\U0001f4c4 {language.upper()}",
            title_align="left",
            border_style="green",
            padding=(0, 1),
        )
        self._print(panel, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P3 — log.tree()
    # ══════════════════════════════════════════════════════════════

    def tree(self, label: str, data: dict[str, Any]) -> None:
        meta = get_caller_metadata(2)
        root = Tree(f"\U0001f333 {escape(label)}")
        self._build_tree(root, data)
        self._print(root, meta=meta)

    def _build_tree(self, parent: Tree, data: dict[str, Any]) -> None:
        for key, value in data.items():
            if isinstance(value, dict):
                branch = parent.add(f"[bold]{escape(str(key))}[/]")
                self._build_tree(branch, value)
            else:
                parent.add(escape(str(key)))

    # ══════════════════════════════════════════════════════════════
    # P3 — log.diff()
    # ══════════════════════════════════════════════════════════════

    def diff(
        self,
        old: str,
        new: str,
        *,
        context: str = "diff",
        context_lines: int = 3,
    ) -> None:
        meta = get_caller_metadata(2)
        old_lines = old.splitlines(keepends=True)
        new_lines = new.splitlines(keepends=True)
        diff_lines = list(unified_diff(old_lines, new_lines, fromfile="old", tofile="new", n=context_lines))

        if not diff_lines:
            self.note("No differences found")
            return

        text = Text()
        text.append(f" DIFF \u2502 {context}\n", style="bold cyan")
        text.append("\u2500" * 40 + "\n", style="dim")

        for line in diff_lines:
            line_str = line.rstrip("\n")
            if line_str.startswith("+") and not line_str.startswith("+++"):
                text.append(f" {line_str}\n", style="green")
            elif line_str.startswith("-") and not line_str.startswith("---"):
                text.append(f" {line_str}\n", style="red")
            elif line_str.startswith("@@"):
                text.append(f" {line_str}\n", style="cyan")
            else:
                text.append(f" {line_str}\n", style="dim")

        self._print(text, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P3 — log.progress()
    # ══════════════════════════════════════════════════════════════

    @contextmanager
    def progress(self, description: str = "Processing...", total: int | None = None) -> Iterator[Any]:
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn

        columns = [
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ]
        with Progress(*columns, console=self._console) as progress:
            task = progress.add_task(description, total=total)
            progress._task = task  # expose for .advance()
            yield progress

    # ══════════════════════════════════════════════════════════════
    # P3 — log.count()
    # ══════════════════════════════════════════════════════════════

    def count(self, label: str, amount: int = 1) -> None:
        self._counters[label] += amount

    def count_summary(self, *, title: str = "Counters") -> None:
        meta = get_caller_metadata(2)
        if not self._counters:
            self.note("No counters recorded")
            return

        text = Text()
        text.append(f" #  {title}\n", style="bold cyan")
        items = self._counters.most_common()
        for i, (label, count) in enumerate(items):
            is_last = i == len(items) - 1
            prefix = "\u2514\u2500\u2500" if is_last else "\u251c\u2500\u2500"
            text.append(f" {prefix} {label:<25}: ", style="dim")
            text.append(f"{count:,}\n", style="bold white")

        self._print(text, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P3 — log.panel()
    # ══════════════════════════════════════════════════════════════

    def panel(
        self,
        message: str,
        *,
        title: str | None = None,
        style: str = "info",
    ) -> None:
        meta = get_caller_metadata(2)
        border_style = LEVEL_STYLES.get(style, "blue")
        icon = LEVEL_ICONS.get(style, "\u2139")
        panel_title = f" {icon} {title} " if title else None

        p = Panel(
            escape(message),
            title=panel_title,
            title_align="left",
            border_style=border_style,
            padding=(1, 2),
        )
        self._print(p, meta=meta)

    # ══════════════════════════════════════════════════════════════
    # P3 — log.rule()
    # ══════════════════════════════════════════════════════════════

    def rule(self, title: str = "", *, style: str = "dim") -> None:
        self._console.rule(title, style=style)
