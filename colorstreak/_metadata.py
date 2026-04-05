"""Caller introspection utility for RichLogger metadata."""

from __future__ import annotations

import os
import sys


def get_caller_metadata(stack_offset: int = 2) -> dict[str, str | int]:
    """
    Extract caller file, line number, and function name.

    Uses sys._getframe() for performance (avoids reading source files
    like inspect.stack() does).

    Args:
        stack_offset: How many frames to go back. Default 2 means:
            0 = this function, 1 = the RichLogger method, 2 = the caller.
    """
    try:
        frame = sys._getframe(stack_offset)
        filename = frame.f_code.co_filename
        short_file = os.path.basename(filename)
        return {
            "file": short_file,
            "path": filename,
            "line": frame.f_lineno,
            "function": frame.f_code.co_name,
        }
    except (ValueError, AttributeError):
        return {
            "file": "?",
            "path": "?",
            "line": 0,
            "function": "?",
        }
