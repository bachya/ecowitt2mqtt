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
from ecowitt2mqtt.publisher.mqtt import get_mqtt_publisher
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
        setup_logging(params.get(CONF_VERBOSE, False))

        self.loop = uvloop.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.config = Config(params)
        self.server = Server(self)

        mqtt_publisher = get_mqtt_publisher(self)

        async def publish_data_to_mqtt(payload: dict[str, Any]) -> None:
            """Publish device data to MQTT."""
            await mqtt_publisher.async_publish(payload)

        self.server.add_device_payload_callback(publish_data_to_mqtt)

    def start(self) -> None:
        """Start ecowitt2mqtt."""
        LOGGER.info("Starting ecowitt2mqtt")
        self.server.start()
