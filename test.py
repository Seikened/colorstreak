"""
test_colorstreak_logger.py

Uso:
  python test_colorstreak_logger.py
"""

from colorstreak import Logger


Logger.configure(style="soft")  # o "soft"

def main() -> None:
    # ====== Basic levels ======
    Logger.debug("This is a debug message")        # GREEN
    Logger.info("This is an info message")         # BLUE
    Logger.warning("This is a warning message")    # YELLOW
    Logger.error("This is an error message")       # RED
    Logger.library("This is a library message")    # MAGENTA
    Logger.success("This is a success message")    # GREEN

    # ====== Print-compatible args/kwargs ======
    Logger.info("Multiple", "args", 123, {"a": 1}, sep=" | ")            # BLUE
    Logger.warning("No newline here...", end="")                         # YELLOW
    Logger.warning(" <- continues on same line")                         # YELLOW
    Logger.error("stderr example (still colored):", file=None)           # default print target (stdout)

    # ====== Helpful formatting patterns ======
    Logger.step("Step 1/3: Checking Docker daemon...")                   # CYAN (if you added step)
    Logger.note("Note: This is a low priority message")                  # GRAY (if you added note)
    Logger.title("=== Section: Metrics ===")                             # BOLD BLUE (if you added title)
    Logger.metric("loss=0.1234 acc=0.9876 latency_ms=42")                # MAGENTA (if you added metric)


if __name__ == "__main__":
    main()