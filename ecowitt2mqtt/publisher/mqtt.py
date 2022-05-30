"""Define MQTT publishing."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from asyncio_mqtt import Client, MqttError

from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.errors import EcowittError
from ecowitt2mqtt.publisher import Publisher

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


class PublishError(EcowittError):
    """Define an error related to a failed data publish."""

    pass


def generate_mqtt_payload(data: dict[str, Any] | str) -> bytes:
    """Generate a binary MQTT payload from input data."""
    if isinstance(data, dict):
        data = json.dumps(data)
    return data.encode("utf-8")


class MqttPublisher(Publisher):
    """Define a base MQTT publisher."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        super().__init__(ecowitt)

        self.client = Client(
            ecowitt.config.mqtt_broker,
            port=ecowitt.config.mqtt_port,
            username=ecowitt.config.mqtt_username,
            password=ecowitt.config.mqtt_password,
            logger=LOGGER,
        )


class MqttTopicPublisher(MqttPublisher):
    """Define an MQTT publisher that publishes to a topic."""

    async def async_publish(self, data: dict[str, Any]) -> None:
        """Publish to MQTT."""
        try:
            async with self.client:
                await self.client.publish(
                    self.ecowitt.config.mqtt_topic, generate_mqtt_payload(data)
                )
        except MqttError as err:
            raise PublishError(
                f"Error while publishing to {self.ecowitt.config.mqtt_topic}: {err}"
            ) from err

        LOGGER.info("Published to %s: %s", self.ecowitt.config.mqtt_topic, data)


def get_mqtt_publisher(ecowitt: Ecowitt) -> MqttPublisher:
    """Get an MQTT publisher."""
    # This will be expanded to include other MQTT publishers:
    return MqttTopicPublisher(ecowitt)
