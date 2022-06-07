"""Define the core application objects."""
from __future__ import annotations

import logging
import os
from typing import Any

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.const import CONF_VERBOSE, LEGACY_ENV_LOG_LEVEL, LOGGER
from ecowitt2mqtt.helpers.logging import TyperLoggerHandler
from ecowitt2mqtt.helpers.publisher.factory import get_publisher
from ecowitt2mqtt.server import Server


class Ecowitt:  # pylint: disable=too-few-public-methods
    """Define the base application object."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Initialize."""
        if params.get(CONF_VERBOSE, False) or os.getenv(LEGACY_ENV_LOG_LEVEL):
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            handlers=(TyperLoggerHandler(),),
        )

        self.config = Config(params)
        self.server = Server(self)

        mqtt_publisher = get_publisher(self)

        async def publish_data_to_mqtt(payload: dict[str, Any]) -> None:
            """Publish device data to MQTT."""
            await mqtt_publisher.async_publish(payload)

        self.server.add_device_payload_callback(publish_data_to_mqtt)

    def start(self) -> None:
        """Start ecowitt2mqtt."""
        LOGGER.info("Starting ecowitt2mqtt")
        self.server.start()
