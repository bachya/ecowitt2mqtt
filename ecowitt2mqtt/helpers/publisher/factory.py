"""Define a publisher factory."""

from __future__ import annotations

from aiomqtt import Client

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.helpers.publisher import Publisher
from ecowitt2mqtt.helpers.publisher.mqtt import TopicPublisher
from ecowitt2mqtt.helpers.publisher.mqtt.hass import HomeAssistantDiscoveryPublisher


def get_publishers(config: Config, client: Client) -> list[Publisher]:
    """Get configured MQTT publishers.

    Args:
        config: A Config object.
        client: An MQTT Client object.

    Returns:
        A list of MqttPublisher objects.
    """
    publishers: list[Publisher] = []
    if config.hass_discovery:
        publishers.append(HomeAssistantDiscoveryPublisher(config, client))
    if config.mqtt_topic:
        publishers.append(TopicPublisher(config, client))
    return publishers
