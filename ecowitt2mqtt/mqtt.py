"""Define MQTT functionality."""
import json
from typing import Optional

from asyncio_mqtt import Client, MqttError
from ecowitt2mqtt.const import LOGGER

DEFAULT_MQTT_PORT = 1883
DEFAULT_TOPIC_TEMPLATE = "ecowitt2mqtt/{0}"


class MQTT:
    """Define an MQTT manager."""

    def __init__(
        self,
        broker: str,
        *,
        port: int = DEFAULT_MQTT_PORT,
        username: Optional[str] = None,
        password: Optional[str] = None,
        topic: Optional[str] = None
    ) -> None:
        """Initialize."""
        self._client = Client(broker, port=port, username=username, password=password)
        self._topic = topic

    async def async_connect(self) -> None:
        """Connect to the MQTT broker."""
        try:
            await self._client.connect()
        except MqttError as err:
            LOGGER.error("Error while connecting to MQTT broker: %s", err)

        LOGGER.debug("Connected to MQTT broker")

    async def async_disconnect(self) -> None:
        """Disconnect from the MQTT broker."""
        try:
            await self._client.disconnect()
        except MqttError as err:
            LOGGER.error("Error while disconnecting from MQTT broker: %s", err)

        LOGGER.debug("Disconnected from MQTT broker")

    async def async_publish_topic(self, data: dict) -> None:
        """Publish data to an MQTT topic."""
        if self._topic:
            topic = self._topic
        else:
            topic = DEFAULT_TOPIC_TEMPLATE.format(data["PASSKEY"])

        try:
            await self._client.publish(topic, json.dumps(dict(data)).encode())
            LOGGER.info("Data published to topic %s: %s", topic, data)
        except MqttError as err:
            LOGGER.error("Error while publishing data to MQTT: %s", err)
