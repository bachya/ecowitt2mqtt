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

    OFF = "Dry"
    ON = "Wet"


class RainStateCalculator(Calculator):
    """Define a boolean rain state calculator."""

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            value: calculated value.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        if value == 0.0:
            return self.get_calculated_data_point(
                RainState.OFF, data_type=DataPointType.BOOLEAN
            )
        return self.get_calculated_data_point(
            RainState.ON, data_type=DataPointType.BOOLEAN
        )
