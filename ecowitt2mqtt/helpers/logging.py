"""Define logging helpers."""
from __future__ import annotations

from functools import wraps
import logging
import traceback
from typing import Any, Callable, TypeVar

import typer

from ecowitt2mqtt.const import LOGGER

T = TypeVar("T")


class TyperLoggerHandler(logging.Handler):
    """Define a logging handler that works with Typer."""

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record."""
        foreground = None
        if record.levelno == logging.CRITICAL:
            foreground = typer.colors.BRIGHT_RED
        elif record.levelno == logging.DEBUG:
            foreground = typer.colors.BRIGHT_BLUE
        elif record.levelno == logging.ERROR:
            foreground = typer.colors.BRIGHT_RED
        elif record.levelno == logging.INFO:
            foreground = typer.colors.BRIGHT_GREEN
        elif record.levelno == logging.WARNING:
            foreground = typer.colors.BRIGHT_YELLOW
        typer.secho(self.format(record), fg=foreground)


def log_exception(
    *, exit_code: int = 1
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Define a dectorator to handle exceptions via typer output."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        """Decorate."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: dict[str, Any]) -> T:
            """Wrap."""
            try:
                return func(*args, **kwargs)
            except Exception as err:  # pylint: disable=broad-except
                LOGGER.error(err)
                LOGGER.debug("".join(traceback.format_tb(err.__traceback__)))
                raise typer.Exit(code=exit_code) from err

        return wrapper

    return decorator
