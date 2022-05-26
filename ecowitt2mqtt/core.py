"""Define the core application objects."""
from __future__ import annotations

import logging
import os

import typer

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.const import CONF_VERBOSE, LEGACY_ENV_LOG_LEVEL
from ecowitt2mqtt.helpers.logging import TyperLoggerHandler


class Ecowitt:
    """Define the base application object."""

    def __init__(self, ctx: typer.Context) -> None:
        """Initialize."""
        if ctx.params[CONF_VERBOSE] or os.getenv(LEGACY_ENV_LOG_LEVEL):
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        typer_handler = TyperLoggerHandler()
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            handlers=(typer_handler,),
        )

        self.config = Config(ctx)
