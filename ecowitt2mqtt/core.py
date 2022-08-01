"""Define the core application objects."""
from __future__ import annotations

import logging
import os
from typing import Any

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.const import (
    CONF_VERBOSE,
    LEGACY_ENV_LOG_LEVEL,
    LOGGER,
    __version__ as ecowitt2mqtt_version,
)
from ecowitt2mqtt.helpers.logging import TyperLoggerHandler
from ecowitt2mqtt.runtime import Runtime


class Ecowitt:  # pylint: disable=too-few-public-methods
    """Define the base application object."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Initialize."""
        if params.get(CONF_VERBOSE) or os.getenv(LEGACY_ENV_LOG_LEVEL):
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            handlers=(TyperLoggerHandler(),),
        )

        self._config = Config(params)
        self._runtime = Runtime(self)

    @property
    def config(self) -> Config:
        """Return the config object."""
        return self._config

    async def async_start(self) -> None:
        """Start ecowitt2mqtt."""
        LOGGER.info("Starting ecowitt2mqtt (version %s)", ecowitt2mqtt_version)
        await self._runtime.async_start()
