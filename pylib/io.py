import os
import sys

CI = os.getenv("CI", "false").lower() in ("yes", "y", "true", "t", "1")


def info(message: str, end: str | None = None) -> None:
    print(message, end=end)


def warning(message: str) -> None:
    if CI:
        message = f"::warning::{message}"
    print(message)


def error(message: str) -> None:
    if CI:
        message = f"::error::{message}"
    print(message, file=sys.stderr)
