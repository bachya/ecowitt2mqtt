"""Define meteorological helpers."""
# pylint: disable=too-few-public-methods
from numbers import Number
from typing import Optional

import meteocalc

from ecowitt2mqtt.const import LOGGER, UNIT_SYSTEM_IMPERIAL


def get_temperature_unit(unit_system: str) -> str:
    """Get the correct temperature unit based on the provided unit system."""
    if unit_system == UNIT_SYSTEM_IMPERIAL:
        return "f"
    return "c"


def convert_rain_volume(value: Number, unit_system: str) -> float:
    """Convert a rain volume into the correct unit."""
    if unit_system == UNIT_SYSTEM_IMPERIAL:
        return value / 25.4
    return value * 25.4


def convert_wind_speed(value: Number, unit_system: str) -> float:
    """Convert a wind speed into the correct unit."""
    if unit_system == UNIT_SYSTEM_IMPERIAL:
        return value / 1.60934
    return value * 1.60934


def convert_pressure(value: Number, unit_system: str) -> float:
    """Convert a barometric pressure amount into the correct unit."""
    if unit_system == UNIT_SYSTEM_IMPERIAL:
        return value / 33.8639
    return value * 33.8639


class Converter:
    """Define a base class to convert meteorological data."""

    def __init__(self, input_unit_system: str, output_unit_system: str) -> None:
        """Initialize."""
        self._input_unit_system = input_unit_system
        self._output_unit_system = output_unit_system

    def parse(self) -> Optional[float]:
        """Return an appropriately-parsed data value."""
        raise NotImplementedError


class DewPointConverter(Converter):
    """Define an object hold convertable dew point data."""

    def __init__(
        self,
        temperature: float,
        humidity: int,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(input_unit_system, output_unit_system)

        temp_obj = meteocalc.Temp(temperature, get_temperature_unit(input_unit_system))
        self._dew_point_obj = meteocalc.dew_point(temp_obj, humidity)

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return round(self._dew_point_obj.f, 1)
        return round(self._dew_point_obj.c, 1)


class FeelsLikeConverter(Converter):
    """Define an object hold convertable "feels like" data."""

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
        super().__init__(input_unit_system, output_unit_system)

        temp_obj = meteocalc.Temp(temperature, get_temperature_unit(input_unit_system))
        self._feels_like_obj = meteocalc.feels_like(temp_obj, humidity, wind_speed)

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return round(self._feels_like_obj.f, 1)
        return round(self._feels_like_obj.c, 1)


class HeatIndexConverter(Converter):
    """Define an object hold convertable heat index data."""

    def __init__(
        self,
        temperature: float,
        humidity: int,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(input_unit_system, output_unit_system)

        temp_obj = meteocalc.Temp(temperature, get_temperature_unit(input_unit_system))
        self._heat_index_obj = meteocalc.heat_index(temp_obj, humidity)

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return round(self._heat_index_obj.f, 1)
        return round(self._heat_index_obj.c, 1)


class PressureConverter:
    """Define an object hold convertable barometric pressure data."""

    def __init__(
        self,
        value: str,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        self._input_unit_system = input_unit_system
        self._output_unit_system = output_unit_system
        self._value = value

    @property
    def pressure(self) -> float:
        """Return the rain accumulation."""
        if self._input_unit_system == self._output_unit_system:
            round(float(self._value), 1)
        return convert_pressure(self._value, self._output_unit_system)


class RainConverter:
    """Define an object hold convertable rain data."""

    def __init__(
        self,
        value: str,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        self._input_unit_system = input_unit_system
        self._output_unit_system = output_unit_system
        self._value = value

    @property
    def accumulation(self) -> float:
        """Return the rain accumulation."""
        if self._input_unit_system == self._output_unit_system:
            return round(float(self._value), 1)
        return convert_rain_volume(self._value, self._output_unit_system)


class WindChillConverter(Converter):
    """Define an object hold convertable wind chill data."""

    def __init__(
        self,
        temperature: float,
        wind_speed: int,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(input_unit_system, output_unit_system)

        temp_obj = meteocalc.Temp(temperature, get_temperature_unit(input_unit_system))
        try:
            self._wind_chill_obj = meteocalc.wind_chill(temp_obj, wind_speed)
        except ValueError as err:
            LOGGER.debug(
                "%s (temperature: %s, wind speed: %s)", err, temp_obj, wind_speed
            )
            self._wind_chill_obj = None

    def parse(self) -> Optional[float]:
        """Return an appropriately-parsed data value."""
        if not self._wind_chill_obj:
            return None

        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return round(self._wind_chill_obj.f, 1)
        return round(self._wind_chill_obj.c, 1)


class TemperatureConverter(Converter):
    """Define an object hold convertable temperature data."""

    def __init__(
        self,
        value: str,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(input_unit_system, output_unit_system)

        self._temperature_obj = meteocalc.Temp(
            value, get_temperature_unit(input_unit_system)
        )

    def parse(self) -> float:
        """Return an appropriately-parsed data value."""
        if self._output_unit_system == UNIT_SYSTEM_IMPERIAL:
            return round(self._temperature_obj.f, 1)
        return round(self._temperature_obj.c, 1)


class WindConverter:
    """Define an object hold convertable wind data."""

    def __init__(
        self,
        value: str,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        self._input_unit_system = input_unit_system
        self._output_unit_system = output_unit_system
        self._value = value

    @property
    def wind_speed(self) -> float:
        """Return the wind speed."""
        if self._input_unit_system == self._output_unit_system:
            return round(float(self._value), 1)
        return convert_wind_speed(self._value, self._output_unit_system)
