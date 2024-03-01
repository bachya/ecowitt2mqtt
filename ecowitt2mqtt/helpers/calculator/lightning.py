"""Define lightning-related calculators."""

from __future__ import annotations

from ecowitt2mqtt.const import CONF_OUTPUT_UNIT_DISTANCE, STRIKES, UnitOfLength
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    CalculationFailedError,
    Calculator,
    SimpleCalculator,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.unit_conversion import DistanceConverter


class LightningStrikeCountCalculator(SimpleCalculator):
    """Define a lightning strike count calculator."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation.

        Returns:
            A unit string.
        """
        return STRIKES


class LightningStrikeDistanceCalculator(Calculator):
    """Define a lightning strike distance calculator.

    Note that lightning strike distances always have metric as the input unit system.
    """

    DEFAULT_INPUT_UNIT = UnitOfLength.KILOMETERS
    UNIT_OVERRIDE_CONFIG_OPTION = CONF_OUTPUT_UNIT_DISTANCE

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial).

        Returns:
            A unit string.
        """
        return UnitOfLength.MILES

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric).

        Returns:
            A unit string.
        """
        return UnitOfLength.KILOMETERS

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
            raise CalculationFailedError("Cannot parse value as a number")
        return self.get_calculated_data_point(value, unit_converter=DistanceConverter)
