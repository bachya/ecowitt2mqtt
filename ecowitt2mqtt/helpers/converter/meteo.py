"""Define meteorological converter helpers."""
# pylint: disable=too-few-public-methods
from typing import cast

import meteocalc

from ecowitt2mqtt.const import LOGGER, UNIT_SYSTEM_IMPERIAL
from ecowitt2mqtt.helpers.converter import Converter


def get_temperature_object(temperature: float, unit_system: str) -> meteocalc.Temp:
    """Get a meteocalc temperature object based on a temperature and unit system."""
    if unit_system == UNIT_SYSTEM_IMPERIAL:
        unit = "f"
    else:
        unit = "c"
    return meteocalc.Temp(temperature, unit)


class MeteoConverter(Converter):
    """Define a base meteorological data strategy."""

    def __init__(self, *, input_unit_system: str, output_unit_system: str) -> None:
        """Initialize."""
        self._input_unit_system = input_unit_system
        self._output_unit_system = output_unit_system


class DewPointConverter(MeteoConverter):
    """Define an object to hold convertible dew point data."""

    def __init__(
        self,
        temperature: float,
        humidity: int,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(
            input_unit_system=input_unit_system, output_unit_system=output_unit_system
        )

        temp_obj = get_temperature_object(temperature, input_unit_system)
        self._dew_point_obj = meteocalc.dew_point(temp_obj, humidity)

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            value = round(self._dew_point_obj.f, 1)
        else:
            value = round(self._dew_point_obj.c, 1)
        return cast(float, value)


class FeelsLikeConverter(MeteoConverter):
    """Define an object to hold convertible "feels like" data."""

    def __init__(
        self,
        temperature: float,
        humidity: int,
        wind_speed: int,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(
            input_unit_system=input_unit_system, output_unit_system=output_unit_system
        )

        temp_obj = get_temperature_object(temperature, input_unit_system)
        self._feels_like_obj = meteocalc.feels_like(temp_obj, humidity, wind_speed)

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            value = round(self._feels_like_obj.f, 1)
        else:
            value = round(self._feels_like_obj.c, 1)
        return cast(float, value)


class HeatIndexConverter(MeteoConverter):
    """Define an object to hold convertible heat index data."""

    def __init__(
        self,
        temperature: float,
        humidity: int,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(
            input_unit_system=input_unit_system, output_unit_system=output_unit_system
        )

        temp_obj = get_temperature_object(temperature, input_unit_system)
        self._heat_index_obj = meteocalc.heat_index(temp_obj, humidity)

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            value = round(self._heat_index_obj.f, 1)
        else:
            value = round(self._heat_index_obj.c, 1)
        return cast(float, value)


class PressureConverter(MeteoConverter):
    """Define an object to hold convertible barometric pressure data."""

    def __init__(
        self,
        value: float,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(
            input_unit_system=input_unit_system, output_unit_system=output_unit_system
        )

        self._value = value

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._input_unit_system == self._output_unit_system:
            return self._value
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return self._value / 33.8639
        return self._value * 33.8639


class RainConverter(MeteoConverter):
    """Define an object to hold convertible rain data."""

    def __init__(
        self,
        value: float,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(
            input_unit_system=input_unit_system, output_unit_system=output_unit_system
        )

        self._value = value

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._input_unit_system == self._output_unit_system:
            return self._value
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return self._value / 25.4
        return self._value * 25.4


class TemperatureConverter(MeteoConverter):
    """Define an object to hold convertible temperature data."""

    def __init__(
        self,
        value: float,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(
            input_unit_system=input_unit_system, output_unit_system=output_unit_system
        )

        self._temp_obj = get_temperature_object(value, input_unit_system)

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            value = round(self._temp_obj.f, 1)
        else:
            value = round(self._temp_obj.c, 1)
        return cast(float, value)


class WindChillConverter(MeteoConverter):
    """Define an object to hold convertible wind chill data."""

    def __init__(
        self,
        temperature: float,
        wind_speed: int,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(
            input_unit_system=input_unit_system, output_unit_system=output_unit_system
        )

        temp_obj = get_temperature_object(temperature, input_unit_system)
        try:
            self._wind_chill_obj = meteocalc.wind_chill(temp_obj, wind_speed)
        except ValueError as err:
            LOGGER.debug(
                "%s (temperature: %s, wind speed: %s)", err, temp_obj, wind_speed
            )
            self._wind_chill_obj = None

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if not self._wind_chill_obj:
            return 0.0

        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            value = round(self._wind_chill_obj.f, 1)
        else:
            value = round(self._wind_chill_obj.c, 1)
        return cast(float, value)


class WindSpeedConverter(MeteoConverter):
    """Define an object to hold convertible wind speed data."""

    def __init__(
        self,
        value: float,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(
            input_unit_system=input_unit_system, output_unit_system=output_unit_system
        )

        self._value = value

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._input_unit_system == self._output_unit_system:
            return self._value
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return self._value / 1.60934
        return self._value * 1.60934
