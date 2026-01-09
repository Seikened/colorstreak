class Logger:
    """
    Logger minimalista con colores ANSI.
    Retrocompatible: Logger.info("x"), Logger.error("x"), etc.
    Soporta *args y **kwargs igual que print().
    """

    COLORS = {
        "debug":    "\033[92m",         # green
        "info":     "\033[94m",         # blue
        "note":     "\033[90m",         # gray
        "step":     "\033[96m",         # cyan
        "warning":  "\033[93m",         # yellow
        "error":    "\033[91m",         # red
        "critical": "\033[91m",         # red
        "success":  "\033[92m",         # green
        "ok":       "\033[92m",         # green
        "fail":     "\033[91m",         # red
        "library":  "\033[95m",         # magenta
        "title":    "\033[1m\033[94m",  # bold blue
        "math":     "\033[96m",         # cyan
        "metric":   "\033[95m",         # magenta
    }

    RESET = "\033[0m"

    @staticmethod
    def _print(message, level: str, *args, **kwargs):
        """Internal: prints a colored [LEVEL] prefix + normal message (print-compatible)."""
        color = Logger.COLORS.get(level, Logger.RESET)
        print(f"{color}[{level.upper()}]{Logger.RESET}", message, *args, **kwargs)

    # ==========================
    # Base logs (retrocompatible)
    # ==========================

    @staticmethod
    def debug(message, *args, **kwargs):
        """Color: **GREEN**. Use: debugging / dev traces."""
        Logger._print(message, "debug", *args, **kwargs)

    @staticmethod
    def info(message, *args, **kwargs):
        """Color: **BLUE**. Use: general info (startup, status)."""
        Logger._print(message, "info", *args, **kwargs)

    @staticmethod
    def warning(message, *args, **kwargs):
        """Color: **YELLOW**. Use: warnings (non-fatal issues)."""
        Logger._print(message, "warning", *args, **kwargs)

    @staticmethod
    def error(message, *args, **kwargs):
        """Color: **RED**. Use: errors (exceptions, failures)."""
        Logger._print(message, "error", *args, **kwargs)

    @staticmethod
    def library(message, *args, **kwargs):
        """Color: **MAGENTA**. Use: library/tooling logs (internal helpers)."""
        Logger._print(message, "library", *args, **kwargs)

    # ==========================
    # Operation state
    # ==========================

    @staticmethod
    def success(message, *args, **kwargs):
        """Color: **GREEN**. Use: success states (deploy ok, done)."""
        Logger._print(message, "success", *args, **kwargs)

    @staticmethod
    def ok(message, *args, **kwargs):
        """Color: **GREEN**. Use: quick confirmations (healthcheck ok)."""
        Logger._print(message, "ok", *args, **kwargs)

    @staticmethod
    def fail(message, *args, **kwargs):
        """Color: **RED**. Use: explicit failure states (operation failed)."""
        Logger._print(message, "fail", *args, **kwargs)

    @staticmethod
    def critical(message, *args, **kwargs):
        """Color: **RED**. Use: fatal/stop-the-world problems."""
        Logger._print(message, "critical", *args, **kwargs)

    # ==========================
    # Terminal UX / flow helpers
    # ==========================

    @staticmethod
    def step(message, *args, **kwargs):
        """Color: **CYAN**. Use: step markers (Step 1/3, etc.)."""
        Logger._print(message, "step", *args, **kwargs)

    @staticmethod
    def title(message, *args, **kwargs):
        """Color: **BOLD BLUE**. Use: section headers / separators."""
        Logger._print(message, "title", *args, **kwargs)

    @staticmethod
    def note(message, *args, **kwargs):
        """Color: **GRAY**. Use: low-priority notes (quiet debug)."""
        Logger._print(message, "note", *args, **kwargs)

    # ==========================
    # Math / metrics vibe
    # ==========================

    @staticmethod
    def math(message, *args, **kwargs):
        """Color: **CYAN**. Use: math-related traces / explanations."""
        Logger._print(message, "math", *args, **kwargs)

    @staticmethod
    def metric(message, *args, **kwargs):
        """Color: **MAGENTA**. Use: key metrics (loss, acc, latency)."""
        Logger._print(message, "metric", *args, **kwargs)