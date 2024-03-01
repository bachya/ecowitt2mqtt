"""Define illuminance calculators."""

from __future__ import annotations

from typing import cast

from ecowitt2mqtt.const import (
    CONF_OUTPUT_UNIT_ILLUMINANCE,
    DATA_POINT_SOLARRADIATION,
    PERCENTAGE,
    UnitOfIlluminance,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, Calculator
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.unit_conversion import IlluminanceConverter


class BaseIlluminanceCalculator(Calculator):
    """Define a base illuminance calculator."""

    DEFAULT_INPUT_UNIT = UnitOfIlluminance.WATTS_PER_SQUARE_METER


class IlluminanceCalculator(BaseIlluminanceCalculator):
    """Define an illuminance calculator."""

    UNIT_OVERRIDE_CONFIG_OPTION = CONF_OUTPUT_UNIT_ILLUMINANCE

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial).

        Returns:
            A unit string.
        """
        return UnitOfIlluminance.WATTS_PER_SQUARE_METER

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric).

        Returns:
            A unit string.
        """
        return UnitOfIlluminance.WATTS_PER_SQUARE_METER

    def calculate_from_value(
        self, value: PreCalculatedValueType
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            value: calculated value.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        return self.get_calculated_data_point(
            value, unit_converter=IlluminanceConverter
        )


class PerceivedIlluminanceCalculator(BaseIlluminanceCalculator):
    """Define a perceived illuminance calculator."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation.

        Returns:
            A unit string.
        """
        return PERCENTAGE

    @Calculator.requires_keys(DATA_POINT_SOLARRADIATION)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        solar_rad = cast(float, payload[DATA_POINT_SOLARRADIATION])
        return self.get_calculated_data_point(
            solar_rad, unit_converter=IlluminanceConverter
        )
