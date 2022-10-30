"""Define pollution calculators."""
from __future__ import annotations

from ecowitt2mqtt.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    DATA_POINT_CO2,
    DATA_POINT_CO2_24H,
)
from ecowitt2mqtt.helpers.calculator import SimpleCalculator


class PollutantCalculator(SimpleCalculator):
    """Define a pollutant calculator."""

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation.

        Returns:
            A unit string.
        """
        if self._data_point_key in (DATA_POINT_CO2, DATA_POINT_CO2_24H):
            return CONCENTRATION_PARTS_PER_MILLION
        return CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
