"""Define illuminance calculators."""
from __future__ import annotations

from typing import cast

from ecowitt2mqtt.const import (
    DATA_POINT_SOLARRADIATION,
    ILLUMINANCE_LUX,
    ILLUMINANCE_WATTS_PER_SQUARE_METER,
    PERCENTAGE,
)
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    Calculator,
    SimpleCalculator,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.unit_conversion import IlluminanceConverter


class BaseIlluminanceCalculator(Calculator):
    """Define a base illuminance calculator."""

    DEFAULT_INPUT_UNIT = ILLUMINANCE_WATTS_PER_SQUARE_METER


class IlluminanceLuxCalculator(BaseIlluminanceCalculator):
    """Define a illuminance calculator (lux)."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation."""
        return ILLUMINANCE_LUX

    @Calculator.requires_keys(DATA_POINT_SOLARRADIATION)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        solar_rad = cast(float, payload[DATA_POINT_SOLARRADIATION])
        converted_value = self.convert_value(IlluminanceConverter, solar_rad)
        return self.get_calculated_data_point(converted_value)


class IlluminancePerceivedCalculator(BaseIlluminanceCalculator):
    """Define a illuminance calculator (perceived)."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation."""
        return PERCENTAGE

    @Calculator.requires_keys(DATA_POINT_SOLARRADIATION)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        solar_rad = cast(float, payload[DATA_POINT_SOLARRADIATION])
        converted_value = IlluminanceConverter.convert_to_percentage(
            solar_rad, ILLUMINANCE_WATTS_PER_SQUARE_METER
        )
        return self.get_calculated_data_point(converted_value)


class IlluminanceWM2Calculator(SimpleCalculator):
    """Define a illuminance calculator (W/m²)."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation."""
        return ILLUMINANCE_WATTS_PER_SQUARE_METER
