"""Define humidity calculators."""
from __future__ import annotations

from typing import cast

from ecowitt2mqtt.const import (
    CONF_OUTPUT_UNIT_HUMIDITY,
    DATA_POINT_HUMIDITY,
    DATA_POINT_TEMP,
    PERCENTAGE,
    VOLUME_GRAMS_PER_CUBIC_METER,
    VOLUME_POUNDS_PER_CUBIC_FOOT,
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

    DEFAULT_INPUT_UNIT = VOLUME_GRAMS_PER_CUBIC_METER
    UNIT_OVERRIDE_CONFIG_OPTION = CONF_OUTPUT_UNIT_HUMIDITY

    @property
    def output_unit_imperial(self) -> str:
        """Get the default unit (imperial).

        Returns:
            A unit string.
        """
        return VOLUME_POUNDS_PER_CUBIC_FOOT

    @property
    def output_unit_metric(self) -> str:
        """Get the default unit (metric).

        Returns:
            A unit string.
        """
        return VOLUME_GRAMS_PER_CUBIC_METER

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation.

        Args:
            payload: An Ecowitt data payload.

        Returns:
            A parsed CalculatedDataPoint object.
        """
        temp = cast(float, payload[DATA_POINT_TEMP])
        humidity = cast(float, payload[DATA_POINT_HUMIDITY])

        temp_obj = get_temperature_meteocalc_object(
            temp, self._config.input_unit_system
        )

        value = get_absolute_humidity_in_metric(temp_obj, humidity)
        return self.get_calculated_data_point(value, unit_converter=VolumeConverter)


class RelativeHumidityCalculator(SimpleCalculator):
    """Define a boolean leak calculator."""

    @property
    def output_unit(self) -> str:
        """Get the output unit of measurement for this calculation.

        Returns:
            A unit string.
        """
        return PERCENTAGE
