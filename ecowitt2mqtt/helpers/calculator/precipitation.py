"""Define precipitation calculators."""
from __future__ import annotations

from typing import cast

from ecowitt2mqtt.const import (
    CONF_OUTPUT_UNIT_ACCUMULATED_PRECIPITATION,
    CONF_OUTPUT_UNIT_PRECIPITATION_RATE,
    PRECIPITATION_INCHES,
    PRECIPITATION_INCHES_PER_HOUR,
    PRECIPITATION_MILLIMETERS,
    PRECIPITATION_MILLIMETERS_PER_HOUR,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, Calculator
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.unit_conversion import (
    AccumulatedPrecipitationConverter,
    PrecipitationRateConverter,
)


class AccumulatedPrecipitationCalculator(Calculator):
    """Define a rain volume calculator."""

    DEFAULT_INPUT_UNIT = PRECIPITATION_INCHES
    UNIT_OVERRIDE_CONFIG_OPTION = CONF_OUTPUT_UNIT_ACCUMULATED_PRECIPITATION

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial).

        Returns:
            A unit string.
        """
        return PRECIPITATION_INCHES

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric).

        Returns:
            A unit string.
        """
        return PRECIPITATION_MILLIMETERS

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
            float_value, unit_converter=AccumulatedPrecipitationConverter
        )


class PrecipitationRateCalculator(Calculator):
    """Define a rain rate calculator."""

    DEFAULT_INPUT_UNIT = PRECIPITATION_INCHES_PER_HOUR
    UNIT_OVERRIDE_CONFIG_OPTION = CONF_OUTPUT_UNIT_PRECIPITATION_RATE

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial).

        Returns:
            A unit string.
        """
        return PRECIPITATION_INCHES_PER_HOUR

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric).

        Returns:
            A unit string.
        """
        return PRECIPITATION_MILLIMETERS_PER_HOUR

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
            float_value, unit_converter=PrecipitationRateConverter
        )
