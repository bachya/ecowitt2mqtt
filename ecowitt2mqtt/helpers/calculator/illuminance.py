"""Define illuminance calculators."""
from __future__ import annotations

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


class IlluminanceLuxCalculator(Calculator):
    """Define a illuminance calculator (lux)."""

    @property
    def default_imperial_unit(self) -> str:
        """Get the default unit (imperial)."""
        return ILLUMINANCE_LUX

    @property
    def default_metric_unit(self) -> str:
        """Get the default unit (metric)."""
        return ILLUMINANCE_LUX

    @Calculator.requires_keys(DATA_POINT_SOLARRADIATION)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(payload[DATA_POINT_SOLARRADIATION], float)

        value = IlluminanceConverter.convert(
            payload[DATA_POINT_SOLARRADIATION],
            ILLUMINANCE_WATTS_PER_SQUARE_METER,
            ILLUMINANCE_LUX,
        )

        return self.get_calculated_data_point(value)


class IlluminancePerceivedCalculator(Calculator):
    """Define a illuminance calculator (perceived)."""

    @property
    def default_imperial_unit(self) -> str:
        """Get the default unit (imperial)."""
        return PERCENTAGE

    @property
    def default_metric_unit(self) -> str:
        """Get the default unit (metric)."""
        return PERCENTAGE

    @Calculator.requires_keys(DATA_POINT_SOLARRADIATION)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(payload[DATA_POINT_SOLARRADIATION], float)

        value = IlluminanceConverter.convert_to_percentage(
            payload[DATA_POINT_SOLARRADIATION], ILLUMINANCE_WATTS_PER_SQUARE_METER
        )

        return self.get_calculated_data_point(value)


class IlluminanceWM2Calculator(SimpleCalculator):
    """Define a illuminance calculator (W/m²)."""

    @property
    def default_imperial_unit(self) -> str:
        """Get the default unit (imperial)."""
        return ILLUMINANCE_WATTS_PER_SQUARE_METER

    @property
    def default_metric_unit(self) -> str:
        """Get the default unit (metric)."""
        return ILLUMINANCE_WATTS_PER_SQUARE_METER
