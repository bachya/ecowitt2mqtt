"""Define helpers to publish Ecowitt payloads."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
import json
from typing import Any

from asyncio_mqtt import Client

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.helpers.typing import CalculatedValueType


def generate_mqtt_payload(data: CalculatedValueType) -> bytes:
    """Generate a binary MQTT payload from input data."""
    if isinstance(data, dict):
        converted_data = json.dumps(data, default=json_serializer)
    elif not isinstance(data, str):
        converted_data = str(data)
    else:
        converted_data = data
    return converted_data.encode("utf-8")


def json_serializer(obj: Any) -> Any:  # pylint: disable=inconsistent-return-statements
    """Define a custom JSON serializer."""
    if isinstance(obj, datetime):
        return obj.isoformat()


class MqttPublisher(ABC):
    """Define a base MQTT publisher."""

    def __init__(self, config: Config, client: Client) -> None:
        """Initialize."""
        self._client = client
        self._config = config

    @abstractmethod
    async def async_publish(self, data: dict[str, Any]) -> None:
        """Publish the data."""
        raise NotImplementedError()
