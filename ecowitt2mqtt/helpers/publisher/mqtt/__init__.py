"""Define MQTT publishers."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, cast

from aiomqtt import Client

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.publisher import Publisher
from ecowitt2mqtt.helpers.typing import CalculatedValueType


def generate_mqtt_payload(data: CalculatedValueType) -> bytes:
    """Generate a binary MQTT payload from input data.

    Args:
        data: The parsed value to use in a CalculatedDataPoint.

    Returns:
        Raw bytes.
    """
    if isinstance(data, dict):
        converted_data = json.dumps(data, default=json_serializer)
    elif not isinstance(data, str):
        converted_data = str(data)
    else:
        converted_data = data
    return converted_data.encode("utf-8")


# pylint: disable=inconsistent-return-statements
def json_serializer(obj: Any) -> float | int | str:  # type: ignore[return]
    """Define a custom JSON serializer.

    Args:
        obj: An object to JSON-serialize.

    Returns:
        A JSON-parseable value.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()


class MqttPublisher(Publisher):  # pylint: disable=too-few-public-methods
    """Define a base MQTT publisher."""

    def __init__(self, config: Config, client: Client) -> None:
        """Initialize.

        Args:
            config: A Config object.
            client: An MQTT Client object.
        """
        super().__init__(config)
        self._client = client


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
