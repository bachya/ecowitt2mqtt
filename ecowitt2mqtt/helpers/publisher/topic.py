"""Define MQTT publishing."""
from __future__ import annotations

from typing import cast

from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.publisher import MqttPublisher, generate_mqtt_payload
from ecowitt2mqtt.helpers.typing import CalculatedValueType


class TopicPublisher(MqttPublisher):  # pylint: disable=too-few-public-methods
    """Define an MQTT publisher that publishes to a topic."""

    async def async_publish(self, data: dict[str, CalculatedValueType]) -> None:
        """Publish to MQTT.

        Args:
            data: A data payload.
        """
        if not self._config.raw_data:
            processed_data = ProcessedData(self._config, data)
            data = {key: value.value for key, value in processed_data.output.items()}

        topic = cast(str, self._config.mqtt_topic)
        await self._client.publish(
            topic, payload=generate_mqtt_payload(data), retain=self._config.mqtt_retain
        )

        LOGGER.info("Published to %s", self._config.mqtt_topic)
        LOGGER.debug("Published data: %s", data)
