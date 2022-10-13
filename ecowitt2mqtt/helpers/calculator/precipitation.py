"""Define precipitation calculators."""
from __future__ import annotations

from ecowitt2mqtt.const import (
    PRECIPITATION_INCHES,
    PRECIPITATION_INCHES_PER_HOUR,
    PRECIPITATION_MILLIMETERS,
    PRECIPITATION_MILLIMETERS_PER_HOUR,
    UNIT_SYSTEM_IMPERIAL,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, Calculator
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType


class RainRateCalculator(Calculator):
    """Define a rain rate calculator."""

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        if self._config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return PRECIPITATION_INCHES_PER_HOUR
        return PRECIPITATION_MILLIMETERS_PER_HOUR

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(value, float)

        if self._config.input_unit_system == self._config.output_unit_system:
            rain_volume = value
        elif self._config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            rain_volume = round(value / 25.4, 1)
        else:
            rain_volume = round(value * 25.4, 1)
        return self.get_calculated_data_point(rain_volume)


class RainVolumeCalculator(Calculator):
    """Define a rain volume calculator."""

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        if self._config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return PRECIPITATION_INCHES
        return PRECIPITATION_MILLIMETERS

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(value, float)

        if self._config.input_unit_system == self._config.output_unit_system:
            final_value = value
        elif self._config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            final_value = round(value / 25.4, 1)
        else:
            final_value = round(value * 25.4, 1)

        return self.get_calculated_data_point(final_value)
