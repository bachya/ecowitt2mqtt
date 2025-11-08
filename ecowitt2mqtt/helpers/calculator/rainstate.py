"""Define rain state calculators."""

from __future__ import annotations

from ecowitt2mqtt.backports.enum import StrEnum
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    Calculator,
    DataPointType,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType


class RainState(StrEnum):
    """Define types of rain state configuration."""

    OFF = "OFF"
    ON = "ON"


class RainStateCalculator(Calculator):
    """Define a boolean rain state calculator."""

    OFF_STATES = ("dry", "off")

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            value: calculated value.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        # Handle string values "Wet"/"Dry" from newer devices
        if isinstance(value, str):
            if value.lower() in self.OFF_STATES:
                return self.get_calculated_data_point(
                    RainState.OFF, data_type=DataPointType.BOOLEAN
                )
            return self.get_calculated_data_point(
                RainState.ON, data_type=DataPointType.BOOLEAN
            )

        # Handle numeric values (0/1 or 0.0/non-zero)
        if value == 0.0:
            return self.get_calculated_data_point(
                RainState.OFF, data_type=DataPointType.BOOLEAN
            )
        return self.get_calculated_data_point(
            RainState.ON, data_type=DataPointType.BOOLEAN
        )
