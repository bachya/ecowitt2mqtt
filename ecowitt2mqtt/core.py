"""Define the core application objects."""
from __future__ import annotations

import asyncio
import logging
import os
from typing import Any

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.const import (
    CONF_VERBOSE,
    LEGACY_ENV_LOG_LEVEL,
    LOGGER,
    __version__ as version,
)
from ecowitt2mqtt.helpers.logging import TyperLoggerHandler
from ecowitt2mqtt.helpers.publisher.factory import get_publisher
from ecowitt2mqtt.server import Server


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

        self.config = Config(params)
        self.mqtt_publisher = get_publisher(self)
        self.server = Server(self)

    async def async_start(self, *, diagnostics: bool = False) -> None:
        """Start ecowitt2mqtt."""
        LOGGER.info("Starting ecowitt2mqtt")

        self.server.add_device_payload_callback(self.mqtt_publisher.async_publish)

        if self.config.diagnostics:
            LOGGER.debug("*** COLLECTING DIAGNOSTICS (version: %s)", version)

            async def stop_after_diagnostics_collected(_: dict[str, Any]) -> None:
                """Stop the server."""
                # Sleep briefly to let the MQTT broker disconnect:
                await asyncio.sleep(0.1)
                self.server.stop()
                LOGGER.debug("*** DIAGNOSTICS COLLECTED")

            self.server.add_device_payload_callback(stop_after_diagnostics_collected)

        await self.server.async_start()
