"""Define time calculators."""
from __future__ import annotations

from datetime import datetime, timezone

from ecowitt2mqtt.const import LOGGER, TIME_SECONDS
from ecowitt2mqtt.helpers.calculator import (
    Calculator,
    CalculatedDataPoint,
    SimpleCalculator,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType


class EpochCalculator(Calculator):
    """Define a time-since-epoch calculator."""

    def calculate(self, value: PreCalculatedValueType) -> CalculatedDataPoint:
        """Perform the calculation."""
        try:
            float_value = float(value)
        except ValueError:
            LOGGER.debug("Can't convert value to number: %s", value)
            return self.get_calculated_data_point(None)

        timestamp = datetime.utcfromtimestamp(float_value).replace(tzinfo=timezone.utc)
        return self.get_calculated_data_point(timestamp)


class RuntimeCalculator(SimpleCalculator):
    """Define a runtime calculator."""

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        return TIME_SECONDS
