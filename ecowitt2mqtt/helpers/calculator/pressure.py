"""Define pressure calculators."""

from __future__ import annotations

from typing import cast

from ecowitt2mqtt.const import CONF_OUTPUT_UNIT_PRESSURE, UnitOfPressure
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, Calculator
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.unit_conversion import PressureConverter


class PressureCalculator(Calculator):
    """Define a pressure calculator."""

    DEFAULT_INPUT_UNIT = UnitOfPressure.INHG
    UNIT_OVERRIDE_CONFIG_OPTION = CONF_OUTPUT_UNIT_PRESSURE

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial).

        Returns:
            A unit string.
        """
        return UnitOfPressure.INHG

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric).

        Returns:
            A unit string.
        """
        return UnitOfPressure.HPA

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            value: calculated value.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        float_value = cast(float, value)
        return self.get_calculated_data_point(
            float_value, unit_converter=PressureConverter
        )
