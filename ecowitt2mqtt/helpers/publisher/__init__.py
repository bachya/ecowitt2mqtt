"""Define helpers to publish Ecowitt payloads."""
from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from asyncio_mqtt import Client

from ecowitt2mqtt.config import Config
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


class MqttPublisher(ABC):  # pylint: disable=too-few-public-methods
    """Define a base MQTT publisher."""

    def __init__(self, config: Config, client: Client) -> None:
        """Initialize.

        Args:
            config: A Config object.
            client: An MQTT Client object.
        """
        self._client = client
        self._config = config

    @abstractmethod
    async def async_publish(self, data: dict[str, Any]) -> None:
        """Publish the data.

        Args:
            data: A data payload.

        Raises:
            NotImplementedError: Raised if not implemented.
        """
        raise NotImplementedError()
