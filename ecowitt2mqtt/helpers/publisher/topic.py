"""Define MQTT publishing."""
from __future__ import annotations

from asyncio_mqtt import MqttError

from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.publisher import (
    MqttPublisher,
    PublishError,
    generate_mqtt_payload,
)
from ecowitt2mqtt.helpers.typing import DataValueType


class TopicPublisher(MqttPublisher):
    """Define an MQTT publisher that publishes to a topic."""

    async def async_publish(self, data: dict[str, DataValueType]) -> None:
        """Publish to MQTT."""
        if not self.ecowitt.config.raw_data:
            processed_data = ProcessedData(self.ecowitt, data)
            data = {key: value.value for key, value in processed_data.output.items()}

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
