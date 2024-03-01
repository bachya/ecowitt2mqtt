"""Define moisture calculators."""

from __future__ import annotations

from ecowitt2mqtt.backports.enum import StrEnum
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    Calculator,
    DataPointType,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType


class LeakState(StrEnum):
    """Define types of battery configuration."""

    OFF = "OFF"
    ON = "ON"


class LeakCalculator(Calculator):
    """Define a boolean leak calculator."""

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
                LeakState.OFF, data_type=DataPointType.BOOLEAN
            )
        return self.get_calculated_data_point(
            LeakState.ON, data_type=DataPointType.BOOLEAN
        )
