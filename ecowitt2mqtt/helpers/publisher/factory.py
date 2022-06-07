"""Define a publisher factory."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ecowitt2mqtt.helpers.publisher import MqttPublisher
from ecowitt2mqtt.helpers.publisher.hass import HomeAssistantDiscoveryPublisher
from ecowitt2mqtt.helpers.publisher.topic import TopicPublisher

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


def get_publisher(ecowitt: Ecowitt) -> MqttPublisher:
    """Get an MQTT publisher."""
    if ecowitt.config.hass_discovery:
        return HomeAssistantDiscoveryPublisher(ecowitt)
    return TopicPublisher(ecowitt)
