"""Define helpers to publish Ecowitt payloads."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import TYPE_CHECKING, Any

from asyncio_mqtt import Client

from ecowitt2mqtt.helpers.typing import DataValueType

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


def generate_mqtt_payload(data: DataValueType) -> bytes:
    """Generate a binary MQTT payload from input data."""
    if isinstance(data, dict):
        converted_data = json.dumps(data, default=json_serializer)
    elif not isinstance(data, str):
        converted_data = str(data)
    else:
        converted_data = data
    return converted_data.encode("utf-8")


def json_serializer(obj: Any) -> Any:
    """Define a custom JSON serializer."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


class MqttPublisher(ABC):
    """Define a base MQTT publisher."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self.ecowitt = ecowitt

    @abstractmethod
    async def async_publish(self, client: Client, data: dict[str, Any]) -> None:
        """Publish the data."""
        raise NotImplementedError()
