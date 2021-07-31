"""Define converter helpers."""
from abc import ABC, abstractmethod
from typing import Any


class Converter(ABC):  # pylint: disable=too-few-public-methods
    """Define an abstract data converter base."""

    def __init__(self, *, input_unit_system: str, output_unit_system: str) -> None:
        """Initialize."""
        self._input_unit_system = input_unit_system
        self._output_unit_system = output_unit_system

    @abstractmethod
    def parse(self) -> Any:
        """Parse and return the data."""
        pass
