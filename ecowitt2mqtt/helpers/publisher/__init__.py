"""Define helpers to publish Ecowitt payloads."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.helpers.typing import CalculatedValueType


class Publisher(ABC):  # pylint: disable=too-few-public-methods
    """Define a base publisher."""

    def __init__(self, config: Config) -> None:
        """Initialize.

        Args:
            config: A Config object.
        """
        self._config = config

    @abstractmethod
    async def async_publish(self, data: dict[str, CalculatedValueType]) -> None:
        """Publish the data.

        Args:
            data: A data payload.

        Raises:
            NotImplementedError: Raised if not implemented.
        """
        raise NotImplementedError()
