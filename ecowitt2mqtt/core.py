"""Define the core application objects."""
from __future__ import annotations

import asyncio
import logging
import os
import traceback
from typing import Any

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.const import (
    CONF_VERBOSE,
    LEGACY_ENV_LOG_LEVEL,
    LOGGER,
    __version__ as version,
)
from ecowitt2mqtt.helpers.logging import TyperLoggerHandler
from ecowitt2mqtt.helpers.publisher import PublishError
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

    async def async_start(self) -> None:
        """Start ecowitt2mqtt."""
        LOGGER.info("Starting ecowitt2mqtt")

        async def async_publish(payload: dict[str, Any]) -> None:
            """Publish a payload to the MQTT broker."""
            try:
                await self.mqtt_publisher.async_publish(payload)
            except PublishError as err:
                LOGGER.error("Unable to publish payload: %s", err)
                LOGGER.debug("".join(traceback.format_tb(err.__traceback__)))

        async def async_get_diagnostics(payload: dict[str, Any]) -> None:
            """Publish a diagnostics payload to the MQTT broker and exit."""
            LOGGER.debug("*** COLLECTING DIAGNOSTICS (version: %s)", version)
            await async_publish(payload)
            await asyncio.sleep(0.1)
            self.server.stop()
            LOGGER.debug("*** DIAGNOSTICS COLLECTED")

        if self.config.diagnostics:
            self.server.add_device_payload_callback(async_get_diagnostics)
        else:
            self.server.add_device_payload_callback(async_publish)

        await self.server.async_start()
