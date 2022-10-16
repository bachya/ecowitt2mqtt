"""Define pressure calculators."""
from __future__ import annotations

from ecowitt2mqtt.const import PRESSURE_HPA, PRESSURE_INHG
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, Calculator
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.unit_conversion import PressureConverter


class PressureCalculator(Calculator):
    """Define a pressure calculator."""

    DEFAULT_INPUT_UNIT = PRESSURE_INHG

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial)."""
        return PRESSURE_INHG

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric)."""
        return PRESSURE_HPA

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(value, float)
        return self.get_calculated_data_point(value, unit_converter=PressureConverter)
