"""Define illuminance calculators."""
from __future__ import annotations

import math

from ecowitt2mqtt.const import (
    DATA_POINT_SOLARRADIATION,
    ILLUMINANCE_WATTS_PER_SQUARE_METER,
    LIGHT_LUX,
    PERCENTAGE,
)
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    Calculator,
    SimpleCalculator,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType


class IlluminanceLuxCalculator(Calculator):
    """Define a illuminance calculator (lux)."""

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        return LIGHT_LUX

    @Calculator.requires_keys(DATA_POINT_SOLARRADIATION)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(payload[DATA_POINT_SOLARRADIATION], float)

        return self.get_calculated_data_point(
            round(float(payload[DATA_POINT_SOLARRADIATION]) / 0.0079, 1)
        )


class IlluminancePerceivedCalculator(Calculator):
    """Define a illuminance calculator (perceived)."""

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        return PERCENTAGE

    @Calculator.requires_keys(DATA_POINT_SOLARRADIATION)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(payload[DATA_POINT_SOLARRADIATION], float)

        lux_value = round(float(payload[DATA_POINT_SOLARRADIATION]) / 0.0079, 1)

        try:
            final_value = round(math.log10(lux_value) / 5, 2) * 100
        except ValueError:
            # If we've approached negative infinity, we'll get a math domain error; in
            # that case, return 0.0:
            final_value = 0.0

        return self.get_calculated_data_point(final_value)


class IlluminanceWM2Calculator(SimpleCalculator):
    """Define a illuminance calculator (W/m²)."""

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        return ILLUMINANCE_WATTS_PER_SQUARE_METER
