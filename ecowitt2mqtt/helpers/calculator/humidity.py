"""Define humidity calculators."""
from __future__ import annotations

from ecowitt2mqtt.const import (
    DATA_POINT_HUMIDITY,
    DATA_POINT_TEMP,
    PERCENTAGE,
    UNIT_SYSTEM_IMPERIAL,
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

    @property
    def default_imperial_unit(self) -> str:
        """Get the default unit (imperial)."""
        return VOLUME_POUNDS_PER_CUBIC_FOOT

    @property
    def default_metric_unit(self) -> str:
        """Get the default unit (metric)."""
        return VOLUME_GRAMS_PER_CUBIC_METER

    @Calculator.requires_keys(DATA_POINT_TEMP, DATA_POINT_HUMIDITY)
    def calculate_from_payload(
        self, payload: dict[str, PreCalculatedValueType]
    ) -> CalculatedDataPoint:
        """Perform the calculation."""
        assert isinstance(payload[DATA_POINT_TEMP], float)
        assert isinstance(payload[DATA_POINT_HUMIDITY], float)

        temp_obj = get_temperature_meteocalc_object(
            payload[DATA_POINT_TEMP], self._config.input_unit_system
        )

        value = get_absolute_humidity_in_metric(temp_obj, payload[DATA_POINT_HUMIDITY])
        if self._config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            value = VolumeConverter.convert(
                value, VOLUME_GRAMS_PER_CUBIC_METER, VOLUME_POUNDS_PER_CUBIC_FOOT
            )

        return self.get_calculated_data_point(value)


class RelativeHumidityCalculator(SimpleCalculator):
    """Define a boolean leak calculator."""

    @property
    def default_imperial_unit(self) -> str:
        """Get the default unit (imperial)."""
        return PERCENTAGE

    @property
    def default_metric_unit(self) -> str:
        """Get the default unit (metric)."""
        return PERCENTAGE
