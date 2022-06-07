"""Define meteorological utilities."""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

import meteocalc

from ecowitt2mqtt.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    DEGREE,
    IRRADIATION_WATTS_PER_SQUARE_METER,
    LIGHT_LUX,
    LOGGER,
    PERCENTAGE,
    PRESSURE_HPA,
    PRESSURE_INHG,
    RAINFALL_INCHES,
    RAINFALL_MILLIMETERS,
    SPEED_KILOMETERS_PER_HOUR,
    SPEED_MILES_PER_HOUR,
    STRIKES,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
    UV_INDEX,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint
from ecowitt2mqtt.helpers.typing import UnitSystemType

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

PRESSURE_UNIT_MAP = {
    UNIT_SYSTEM_IMPERIAL: PRESSURE_INHG,
    UNIT_SYSTEM_METRIC: PRESSURE_HPA,
}

RAIN_VOLUME_UNIT_MAP = {
    UNIT_SYSTEM_IMPERIAL: RAINFALL_INCHES,
    UNIT_SYSTEM_METRIC: RAINFALL_MILLIMETERS,
}

TEMP_UNIT_MAP = {
    UNIT_SYSTEM_IMPERIAL: TEMP_FAHRENHEIT,
    UNIT_SYSTEM_METRIC: TEMP_CELSIUS,
}

WIND_SPEED_UNIT_MAP = {
    UNIT_SYSTEM_IMPERIAL: SPEED_MILES_PER_HOUR,
    UNIT_SYSTEM_METRIC: SPEED_KILOMETERS_PER_HOUR,
}


def _get_temperature_object(
    temperature: float, unit_system: UnitSystemType
) -> meteocalc.Temp:
    """Get a meteocalc temperature object based on a temperature and unit system."""
    if unit_system == UNIT_SYSTEM_IMPERIAL:
        unit = "f"
    else:
        unit = "c"
    return meteocalc.Temp(temperature, unit)


def calculate_co2(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate CO2."""
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=value, unit=CONCENTRATION_PARTS_PER_MILLION
    )


def calculate_dew_point(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    *,
    temp: float,
    humidity: float,
) -> CalculatedDataPoint:
    """Calculate dew point in the appropriate unit system."""
    temp_obj = _get_temperature_object(temp, ecowitt.config.input_unit_system)
    dew_point_obj = meteocalc.dew_point(temp_obj, humidity)

    if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(dew_point_obj.f, 1)
    else:
        final_value = round(dew_point_obj.c, 1)
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TEMP_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_feels_like(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    *,
    temp: float,
    humidity: float,
    windspeed: float,
) -> CalculatedDataPoint:
    """Calculate "feels like" temperature in the appropriate unit system."""
    temp_obj = _get_temperature_object(temp, ecowitt.config.input_unit_system)
    feels_like_obj = meteocalc.feels_like(temp_obj, humidity, windspeed)

    if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(feels_like_obj.f, 1)
    else:
        final_value = round(feels_like_obj.c, 1)
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TEMP_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_heat_index(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    *,
    temp: float,
    humidity: float,
) -> CalculatedDataPoint:
    """Calculate heat index in the appropriate unit system."""
    temp_obj = _get_temperature_object(temp, ecowitt.config.input_unit_system)
    heat_index_obj = meteocalc.heat_index(temp_obj, humidity)

    if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(heat_index_obj.f, 1)
    else:
        final_value = round(heat_index_obj.c, 1)
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TEMP_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_humidity(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate humidity."""
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=value, unit=PERCENTAGE
    )


def calculate_lightning_strikes(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate lightning strikes."""
    return CalculatedDataPoint(data_point_key=data_point_key, value=value, unit=STRIKES)


def calculate_moisture(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate moisture."""
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=value, unit=PERCENTAGE
    )


def calculate_pm25(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate PM2.5 pollution."""
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=value,
        unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    )


def calculate_pm10(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate PM10.0 pollution."""
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=value,
        unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    )


def calculate_pressure(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate pressure in the appropriate unit system."""
    if ecowitt.config.input_unit_system == ecowitt.config.output_unit_system:
        final_value = value
    elif ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(value / 33.8639, 3)
    else:
        final_value = round(value * 33.8639, 3)
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=PRESSURE_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_rain_volume(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate rain volume in the appropriate unit system."""
    if ecowitt.config.input_unit_system == ecowitt.config.output_unit_system:
        final_value = value
    elif ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(value / 25.4, 1)
    else:
        final_value = round(value * 25.4, 1)
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=RAIN_VOLUME_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_solar_radiation_lux(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, solarradiation: float
) -> CalculatedDataPoint:
    """Calculate solar radiation (lux)."""
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=round(float(solarradiation) / 0.0079, 1),
        unit=LIGHT_LUX,
    )


def calculate_solar_radiation_perceived(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, solarradiation: float
) -> CalculatedDataPoint:
    """Calculate solar radiation (% perceived)."""
    lux_data_point = calculate_solar_radiation_lux(
        ecowitt, payload_key, data_point_key, solarradiation=solarradiation
    )

    assert isinstance(lux_data_point.value, float)

    try:
        final_value = round(math.log10(lux_data_point.value) / 5, 2) * 100
    except ValueError:
        # If we've approached negative infinity, we'll get a math domain error; in that
        # case, return 0.0:
        final_value = 0.0
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=final_value, unit=PERCENTAGE
    )


def calculate_solar_radiation_wm2(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate solar radiation (W/m²)."""
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=value,
        unit=IRRADIATION_WATTS_PER_SQUARE_METER,
    )


def calculate_temperature(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate temperature in the appropriate unit system."""
    temp_obj = _get_temperature_object(value, ecowitt.config.input_unit_system)

    if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(temp_obj.f, 1)
    else:
        final_value = round(temp_obj.c, 1)
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TEMP_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_uv_index(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate UV index."""
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=value, unit=UV_INDEX
    )


def calculate_wind_chill(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    *,
    temp: float,
    windspeed: float,
) -> CalculatedDataPoint:
    """Calculate wind chill in the appropriate unit system.

    Note that because wind chill only applies at certain combinations of temperature
    and wind speed, it is possible for this method to return None.
    """
    temp_obj = _get_temperature_object(temp, ecowitt.config.input_unit_system)

    try:
        wind_chill_obj = meteocalc.wind_chill(temp_obj, windspeed)
    except ValueError as err:
        LOGGER.debug("%s (temperature: %s, wind speed: %s)", err, temp_obj, windspeed)
        final_value = None
    else:
        if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            final_value = round(wind_chill_obj.f, 1)
        else:
            final_value = round(wind_chill_obj.c, 1)
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TEMP_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_wind_dir(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate wind direction."""
    return CalculatedDataPoint(data_point_key=data_point_key, value=value, unit=DEGREE)


def calculate_wind_speed(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate wind speed in the appropriate unit system."""
    if ecowitt.config.input_unit_system == ecowitt.config.output_unit_system:
        final_value = value
    elif ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(value / 1.60934, 1)
    else:
        final_value = round(value * 1.60934, 1)
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=WIND_SPEED_UNIT_MAP[ecowitt.config.output_unit_system],
    )
