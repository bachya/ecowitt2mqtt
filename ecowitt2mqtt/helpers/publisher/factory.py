"""Define a publisher factory."""
from __future__ import annotations

from asyncio_mqtt import Client

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.helpers.publisher import MqttPublisher
from ecowitt2mqtt.helpers.publisher.hass import HomeAssistantDiscoveryPublisher
from ecowitt2mqtt.helpers.publisher.topic import TopicPublisher


def get_publishers(config: Config, client: Client) -> list[MqttPublisher]:
    """Get configured MQTT publishers.

    Args:
        config: A Config object.
        client: An MQTT Client object.

    Returns:
        A list of MqttPublisher objects.
    """
    publishers: list[MqttPublisher] = []
    if config.hass_discovery:
        publishers.append(HomeAssistantDiscoveryPublisher(config, client))
    if config.mqtt_topic:
        publishers.append(TopicPublisher(config, client))
    return publishers
