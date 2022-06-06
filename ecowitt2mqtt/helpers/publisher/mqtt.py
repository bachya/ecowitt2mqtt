"""Define MQTT publishing."""
from __future__ import annotations

from datetime import datetime
import json
from typing import TYPE_CHECKING, Any

from asyncio_mqtt import Client, MqttError

from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.errors import EcowittError
from ecowitt2mqtt.helpers.publisher import Publisher
from ecowitt2mqtt.helpers.typing import DataValueType

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


class PublishError(EcowittError):
    """Define an error related to a failed data publish."""

    pass


def generate_mqtt_payload(data: dict[str, Any] | str) -> bytes:
    """Generate a binary MQTT payload from input data."""
    if isinstance(data, dict):
        data = json.dumps(data, default=json_serializer)
    return data.encode("utf-8")


def json_serializer(obj: Any) -> Any:
    """Define a custom JSON serializer."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


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


def get_mqtt_publisher(ecowitt: Ecowitt) -> MqttPublisher:
    """Get an MQTT publisher."""
    # This will be expanded to include other MQTT publishers:
    return MqttTopicPublisher(ecowitt)
