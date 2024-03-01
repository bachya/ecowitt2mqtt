"""Define time calculators."""

from __future__ import annotations

from ecowitt2mqtt.const import UnitOfMemory
from ecowitt2mqtt.helpers.calculator import SimpleCalculator


class HeapCalculator(SimpleCalculator):
    """Define a data update interval calculator."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation.

        Returns:
            A unit string.
        """
        return UnitOfMemory.BYTES
