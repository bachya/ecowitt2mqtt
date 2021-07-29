"""Define converter helpers."""
from abc import ABC, abstractmethod


class Converter(ABC):  # pylint: disable=too-few-public-methods
    """Define an abstract data converter base."""

    @abstractmethod
    def parse(self) -> float:
        """Parse and return the data."""
        pass
