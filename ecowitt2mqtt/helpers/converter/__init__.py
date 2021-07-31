"""Define converter helpers."""
from abc import ABC, abstractmethod
from typing import Any


class Converter(ABC):  # pylint: disable=too-few-public-methods
    """Define an abstract data converter base."""

    @abstractmethod
    def parse(self) -> Any:
        """Parse and return the data."""
        pass
