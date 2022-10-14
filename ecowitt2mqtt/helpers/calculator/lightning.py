"""Define lightning-related calculators."""
from __future__ import annotations

from ecowitt2mqtt.const import (
    LENGTH_KILOMETERS,
    LENGTH_MILES,
    LOGGER,
    STRIKES,
    UNIT_SYSTEM_METRIC,
)
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    Calculator,
    SimpleCalculator,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType


class LightningStrikeCountCalculator(SimpleCalculator):
    """Define a lightning strike count calculator."""

    @property
    def default_imperial_unit(self) -> str:
        """Get the default unit (imperial)."""
        return STRIKES

    @property
    def default_metric_unit(self) -> str:
        """Get the default unit (metric)."""
        return STRIKES


class LightningStrikeDistanceCalculator(Calculator):
    """Define a lightning strike distance calculator.

    Note that lightning strike distances always have metric as the input unit system.
    """

    @property
    def default_imperial_unit(self) -> str:
        """Get the default unit (imperial)."""
        return LENGTH_MILES

    @property
    def default_metric_unit(self) -> str:
        """Get the default unit (metric)."""
        return LENGTH_KILOMETERS

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        if isinstance(value, str):
            LOGGER.debug("Can't convert value to number: %s", value)
            return self.get_calculated_data_point(None)

        if self._config.output_unit_system == UNIT_SYSTEM_METRIC:
            final_value = value
        else:
            final_value = round(value / 1.609, 1)

        return self.get_calculated_data_point(final_value)
