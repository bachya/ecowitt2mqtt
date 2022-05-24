"""Define meteorological utilities."""
import math
from typing import Optional, cast

import meteocalc

from ecowitt2mqtt.const import LOGGER, UNIT_SYSTEM_IMPERIAL


def _get_temperature_object(temperature: float, unit_system: str) -> meteocalc.Temp:
    """Get a meteocalc temperature object based on a temperature and unit system."""
    if unit_system == UNIT_SYSTEM_IMPERIAL:
        unit = "f"
    else:
        unit = "c"
    return meteocalc.Temp(temperature, unit)


def calculate_dew_point(
    temperature: float,
    humidity: float,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> float:
    """Calculate dew point in the appropriate unit system."""
    temp_obj = _get_temperature_object(temperature, input_unit_system)
    dew_point_obj = meteocalc.dew_point(temp_obj, humidity)

    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        value = round(dew_point_obj.f, 1)
    else:
        value = round(dew_point_obj.c, 1)
    return cast(float, value)


def calculate_feels_like(
    temperature: float,
    humidity: float,
    wind_speed: float,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> float:
    """Calculate "feels like" temperature in the appropriate unit system."""
    temp_obj = _get_temperature_object(temperature, input_unit_system)
    feels_like_obj = meteocalc.feels_like(temp_obj, humidity, wind_speed)

    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        value = round(feels_like_obj.f, 1)
    else:
        value = round(feels_like_obj.c, 1)
    return cast(float, value)


def calculate_heat_index(
    temperature: float,
    humidity: float,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> float:
    """Calculate heat index in the appropriate unit system."""
    temp_obj = _get_temperature_object(temperature, input_unit_system)
    heat_index_obj = meteocalc.heat_index(temp_obj, humidity)

    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        value = round(heat_index_obj.f, 1)
    else:
        value = round(heat_index_obj.c, 1)
    return cast(float, value)


def calculate_illuminance_wm2_to_lux(value: float) -> float:
    """Calculate illuminance (in lux)."""
    return round(float(value) / 0.0079, 1)


def calculate_illuminance_wm2_to_perceived(value: float) -> float:
    """Calculate illuminance (in lux)."""
    lux = calculate_illuminance_wm2_to_lux(value)
    try:
        perceived = round(math.log10(lux) / 5, 2) * 100
    except ValueError:
        # If we've approached negative infinity, we'll get a math domain error; in that
        # case, return 0.0:
        return 0.0
    if perceived < 0:
        return 0.0
    return perceived


def calculate_pressure(
    value: float,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> float:
    """Calculate pressure in the appropriate unit system."""
    if input_unit_system == output_unit_system:
        return value
    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        return round(value / 33.8639, 3)
    return round(value * 33.8639, 3)


def calculate_rain_volume(
    value: float,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> float:
    """Calculate rain volume in the appropriate unit system."""
    if input_unit_system == output_unit_system:
        return value
    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        return round(value / 25.4, 1)
    return round(value * 25.4, 1)


def calculate_temperature(
    value: float,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> float:
    """Calculate temperature in the appropriate unit system."""
    temp_obj = _get_temperature_object(value, input_unit_system)

    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        value = round(temp_obj.f, 1)
    else:
        value = round(temp_obj.c, 1)
    return value


def calculate_wind_chill(
    temperature: float,
    wind_speed: float,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> Optional[float]:
    """Calculate wind chill in the appropriate unit system."""
    temp_obj = _get_temperature_object(temperature, input_unit_system)

    try:
        wind_chill_obj = meteocalc.wind_chill(temp_obj, wind_speed)
    except ValueError as err:
        LOGGER.debug("%s (temperature: %s, wind speed: %s)", err, temp_obj, wind_speed)
        return None

    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        value = round(wind_chill_obj.f, 1)
    else:
        value = round(wind_chill_obj.c, 1)
    return cast(float, value)


def calculate_wind_speed(
    value: float,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> float:
    """Calculate wind speed in the appropriate unit system."""
    if input_unit_system == output_unit_system:
        return value
    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        return round(value / 1.60934, 1)
    return round(value * 1.60934, 1)
