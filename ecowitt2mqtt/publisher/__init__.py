"""Define helpers to publish Ecowitt payloads."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


class Publisher(ABC):
    """Define an abstract class for a data publisher."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self.ecowitt = ecowitt

    @abstractmethod
    async def async_publish(self, data: dict[str, Any]) -> None:
        """Publish the data."""
        raise NotImplementedError()
