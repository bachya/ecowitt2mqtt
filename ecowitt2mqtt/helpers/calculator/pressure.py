"""Define pressure calculators."""
from __future__ import annotations

from ecowitt2mqtt.const import PRESSURE_INHG, PRESSURE_HPA, UNIT_SYSTEM_IMPERIAL

from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, Calculator
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType


class PressureCalculator(Calculator):
    """Define a pressure calculator."""

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        if self._config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return PRESSURE_INHG
        return PRESSURE_HPA

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        if self._config.input_unit_system == self._config.output_unit_system:
            final_value = value
        elif self._config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            final_value = round(value / 33.8639, 3)
        else:
            final_value = round(value * 33.8639, 3)

        return self.get_calculated_data_point(final_value)
