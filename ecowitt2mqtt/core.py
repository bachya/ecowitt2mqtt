"""Define the core application objects."""
from __future__ import annotations

import asyncio
import logging
import os
from typing import Any

import uvloop

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.const import CONF_VERBOSE, LEGACY_ENV_LOG_LEVEL, LOGGER
from ecowitt2mqtt.helpers.logging import TyperLoggerHandler
from ecowitt2mqtt.server import Server


def setup_logging(verbose: bool = False) -> None:
    """Set up logging."""
    if verbose or os.getenv(LEGACY_ENV_LOG_LEVEL):
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=(TyperLoggerHandler(),),
    )


class Ecowitt:  # pylint: disable=too-few-public-methods
    """Define the base application object."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Initialize."""
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        setup_logging(params.get(CONF_VERBOSE, False))

        self.config = Config(params)
        self.server = Server(self)

    def start(self) -> None:
        """Start ecowitt2mqtt."""
        LOGGER.info("Starting ecowitt2mqtt")
        self.server.start()
