"""Define a publisher factory."""
from __future__ import annotations

from asyncio_mqtt import Client

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.helpers.publisher import MqttPublisher
from ecowitt2mqtt.helpers.publisher.hass import HomeAssistantDiscoveryPublisher
from ecowitt2mqtt.helpers.publisher.topic import TopicPublisher


def get_publisher(config: Config, client: Client) -> MqttPublisher:
    """Get an MQTT publisher."""
    if config.hass_discovery:
        return HomeAssistantDiscoveryPublisher(config, client)
    return TopicPublisher(config, client)
