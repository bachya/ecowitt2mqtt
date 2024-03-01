"""Define time calculators."""

from __future__ import annotations

from ecowitt2mqtt.const import UnitOfTime
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    CalculationFailedError,
    Calculator,
    SimpleCalculator,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.dt import utc_from_timestamp


class EpochCalculator(Calculator):
    """Define a time-since-epoch calculator."""

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            value: calculated value.

        Returns:
            A parsed CalculatedDataPoint object.

        Raises:
            CalculationFailedError: Raised if the calculation fails.
        """
        if isinstance(value, str):
            raise CalculationFailedError("Cannot parse value as datetime")

        timestamp = utc_from_timestamp(value)
        return self.get_calculated_data_point(timestamp)


class RuntimeCalculator(SimpleCalculator):
    """Define a runtime calculator."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation.

        Returns:
            A unit string.
        """
        return UnitOfTime.SECONDS


class UpdateIntervalCalculator(SimpleCalculator):
    """Define a data update interval calculator."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation.

        Returns:
            A unit string.
        """
        return UnitOfTime.SECONDS
