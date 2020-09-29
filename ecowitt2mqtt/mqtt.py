"""Define MQTT functionality."""
import json
from typing import Optional, Union

from asyncio_mqtt import Client, MqttError

from ecowitt2mqtt.const import LOGGER

DEFAULT_MQTT_PORT = 1883


class MQTT:
    """Define an MQTT manager."""

    def __init__(
        self,
        broker: str,
        *,
        port: int = DEFAULT_MQTT_PORT,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """Initialize."""
        self._client = Client(broker, port=port, username=username, password=password)

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

    async def async_publish(self, topic: str, data: Union[dict, float, str]) -> None:
        """Publish data to an MQTT topic."""
        if isinstance(data, dict):
            payload = json.dumps(data).encode("utf-8")
        elif isinstance(data, str):
            payload = data.encode("utf-8")
        else:
            payload = str(data).encode("utf-8")

        try:
            await self._client.publish(topic, payload)
            LOGGER.info("Data published to topic %s: %s", topic, data)
        except MqttError as err:
            LOGGER.error("Error while publishing data to MQTT: %s", err)
