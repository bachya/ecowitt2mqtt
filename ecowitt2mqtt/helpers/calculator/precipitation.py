"""Define precipitation calculators."""
from __future__ import annotations

from ecowitt2mqtt.const import (
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

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial)."""
        return PRECIPITATION_INCHES

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric)."""
        return PRECIPITATION_MILLIMETERS

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(value, float)
        return self.get_calculated_data_point(
            value, unit_converter=AccumulatedPrecipitationConverter
        )


class PrecipitationRateCalculator(Calculator):
    """Define a rain rate calculator."""

    DEFAULT_INPUT_UNIT = PRECIPITATION_INCHES_PER_HOUR

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial)."""
        return PRECIPITATION_INCHES_PER_HOUR

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric)."""
        return PRECIPITATION_MILLIMETERS_PER_HOUR

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(value, float)
        return self.get_calculated_data_point(
            value, unit_converter=PrecipitationRateConverter
        )
