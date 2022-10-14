"""Define humidity calculators."""
from __future__ import annotations

from typing import cast

from ecowitt2mqtt.const import (
    DATA_POINT_HUMIDITY,
    DATA_POINT_TEMP,
    PERCENTAGE,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
)
from ecowitt2mqtt.helpers.calculator import (
    CalculatedDataPoint,
    Calculator,
    SimpleCalculator,
)
from ecowitt2mqtt.helpers.typing import PreCalculatedValueType
from ecowitt2mqtt.util.meteo import (
    get_absolute_humidity_in_metric,
    get_temperature_meteocalc_object,
)
from ecowitt2mqtt.util.unit_conversion import VolumeConverter


class AbsoluteHumidityCalculator(Calculator):
    """Define an absolute humidity calculator."""

    DEFAULT_INPUT_UNIT = VolumeConverter.DEFAULT_UNITS[UNIT_SYSTEM_METRIC]

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial)."""
        return VolumeConverter.DEFAULT_UNITS[UNIT_SYSTEM_IMPERIAL]

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric)."""
        return VolumeConverter.DEFAULT_UNITS[UNIT_SYSTEM_METRIC]

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        temp = cast(float, payload[DATA_POINT_TEMP])
        humidity = cast(float, payload[DATA_POINT_HUMIDITY])
        temp_obj = get_temperature_meteocalc_object(
            temp, self._config.input_unit_system
        )
        value = get_absolute_humidity_in_metric(temp_obj, humidity)
        converted_value = self.convert_value(VolumeConverter, value)
        return self.get_calculated_data_point(converted_value)


class RelativeHumidityCalculator(SimpleCalculator):
    """Define a boolean leak calculator."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation."""
        return PERCENTAGE
