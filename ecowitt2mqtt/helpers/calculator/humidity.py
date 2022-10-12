"""Define humidity calculators."""
from __future__ import annotations

from ecowitt2mqtt.const import (
    DATA_POINT_TEMP,
    DATA_POINT_HUMIDITY,
    PERCENTAGE,
    UNIT_SYSTEM_IMPERIAL,
    WATER_VAPOR_GRAMS_PER_CUBIC_METER,
    WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
)
from ecowitt2mqtt.helpers.calculator import (
    Calculator,
    CalculatedDataPoint,
    SimpleCalculator,
    requires_keys,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.meteo import (
    get_absolute_humidity,
    get_temperature_meteocalc_object,
)


class AbsoluteHumidityCalculator(Calculator):
    """Define an absolute humidity calculator."""

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        if self._config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return WATER_VAPOR_POUNDS_PER_CUBIC_FOOT
        return WATER_VAPOR_GRAMS_PER_CUBIC_METER

    @requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(payload[DATA_POINT_TEMP], float)
        assert isinstance(payload[DATA_POINT_HUMIDITY], float)

        temp_obj = get_temperature_meteocalc_object(
            payload[DATA_POINT_TEMP], self._config.input_unit_system
        )
        value = get_absolute_humidity(temp_obj, payload[DATA_POINT_HUMIDITY])

        if self._config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            value /= 16018.46592051

        return self.get_calculated_data_point(value)


class RelativeHumidityCalculator(SimpleCalculator):
    """Define a boolean leak calculator."""

    @property
    def output_unit(self) -> str | None:
        """Get the output unit of measurement for this calculation."""
        return PERCENTAGE
