"""Define various meteorological utils."""

from __future__ import annotations

import math
from typing import cast

import meteocalc

from ecowitt2mqtt.const import UnitOfTemperature, UnitSystem
from ecowitt2mqtt.util.unit_conversion import TemperatureConverter


def get_absolute_humidity_in_metric(
    temp_obj: meteocalc.Temp, relative_humidity: float
) -> float:
    """Get the absolute humidity (amount of water vapor in the air) in metric.

    Args:
        temp_obj: A meteocalc.Temp object.
        relative_humidity: A float representing relative humidity.

    Returns:
        A float representing absolute humidity.
    """
    return cast(
        float,
        (
            6.112
            * math.exp((17.67 * temp_obj.c) / (temp_obj.c + 243.5))
            * relative_humidity
            * 2.1674
        )
        / (273.15 + temp_obj.c),
    )


def get_dew_point_meteocalc_object(
    temperature: float, relative_humidity: float, unit_system: UnitSystem
) -> meteocalc.Temp:
    """Get a dew point meteocalc object.

    Args:
        temperature: A float representing temperature.
        relative_humidity: A float representing relative humidity.
        unit_system: The target unit system.

    Returns:
        A meteocalc.Temp object.
    """
    temp_obj = get_temperature_meteocalc_object(temperature, unit_system)
    return meteocalc.dew_point(temp_obj, relative_humidity)


def get_feels_like_meteocalc_object(
    temperature: float,
    relative_humidity: float,
    wind_speed: float,
    unit_system: UnitSystem,
) -> meteocalc.Temp:
    """Get a "feels like" meteocalc object.

    Args:
        temperature: A float representing temperature.
        relative_humidity: A float representing relative humidity.
        wind_speed: A float representing wind speed.
        unit_system: The target unit system.

    Returns:
        A meteocalc.Temp object.
    """
    temp_obj = get_temperature_meteocalc_object(temperature, unit_system)
    return meteocalc.feels_like(temp_obj, relative_humidity, wind_speed)


def get_frost_point_meteocalc_object(
    temp_obj: meteocalc.Temp, relative_humidity: float
) -> meteocalc.Temp:
    """Get a frost point meteocalc object.

    Args:
        temp_obj: A meteocalc.Temp object.
        relative_humidity: A float representing relative humidity.

    Returns:
        A meteocalc.Temp object.
    """
    dew_point_obj = meteocalc.dew_point(temp_obj, relative_humidity)
    absolute_temp_c = temp_obj.c + 273.15
    absolute_dew_point_c = dew_point_obj.c + 273.15

    return get_temperature_meteocalc_object(
        (
            absolute_dew_point_c
            + (
                2671.02
                / (
                    (2954.61 / absolute_temp_c)
                    + 2.193665 * math.log(absolute_temp_c)
                    - 13.3448
                )
            )
            - absolute_temp_c
        )
        - 273.15,
        UnitSystem.METRIC,
    )


def get_heat_index_meteocalc_object(
    temperature: float,
    relative_humidity: float,
    unit_system: UnitSystem,
) -> meteocalc.Temp:
    """Get a heat index meteocalc object.

    Args:
        temperature: A float representing temperature.
        relative_humidity: A float representing relative humidity.
        unit_system: A target unit system.

    Returns:
        A meteocalc.Temp object.
    """
    temp_obj = get_temperature_meteocalc_object(temperature, unit_system)
    return meteocalc.heat_index(temp_obj, relative_humidity)


def get_humidex(
    temperature: float, relative_humidity: float, unit_system: UnitSystem
) -> int:
    """Get a humidex.

    Args:
        temperature: A float representing temperature.
        relative_humidity: A float representing relative humidity.
        unit_system: The target unit system.

    Returns:
        The index.
    """
    dew_point_obj = get_dew_point_meteocalc_object(
        temperature, relative_humidity, unit_system
    )
    temp_obj = get_temperature_meteocalc_object(temperature, unit_system)

    return cast(
        int,
        round(
            temp_obj.c
            + (
                0.5555
                * (
                    (
                        6.11
                        * math.exp(
                            5417.7530
                            * (
                                (1 / 273.16)
                                - (
                                    1
                                    / TemperatureConverter.convert(
                                        dew_point_obj.c,
                                        UnitOfTemperature.CELSIUS,
                                        UnitOfTemperature.KELVIN,
                                    )
                                )
                            )
                        )
                    )
                    - 10
                )
            )
        ),
    )


def get_relative_strain_index(
    temperature: float, relative_humidity: float, unit_system: UnitSystem
) -> float:
    """Get a simmer index meteocalc object.

    Args:
        temperature: A float representing temperature.
        relative_humidity: A float representing relative humidity.
        unit_system: A target unit system.

    Returns:
        The index.

    Raises:
        ValueError: Raised when the index cannot be calculated.
    """
    temp_obj = get_temperature_meteocalc_object(temperature, unit_system)

    if temp_obj.c < 26 or temp_obj.c > 35:
        raise ValueError(
            "Relative Strain Index is only valid for temperatures above 26°C and "
            "below 35°C"
        )

    return cast(
        float,
        round(
            (temp_obj.c - 21)
            / (
                58
                - (
                    relative_humidity
                    * (6.112 * pow(10, 7.5 * temp_obj.c / (237.7 + temp_obj.c)))
                    / 100
                )
            ),
            2,
        ),
    )


def get_simmer_index_meteocalc_object(
    temp_obj: meteocalc.Temp, relative_humidity: float, unit_system: UnitSystem
) -> meteocalc.Temp:
    """Get a simmer index meteocalc object.

    Args:
        temp_obj: A meteocalc.Temp object.
        relative_humidity: A float representing relative humidity.
        unit_system: A target unit system.

    Returns:
        A meteocalc.Temp object (if it exists).

    Raises:
        ValueError: Raised when the index cannot be calculated.
    """
    if temp_obj.f < 70:
        raise ValueError(
            "Simmer Index is only valid for temperatures above "
            f"{'70°F' if unit_system == UnitSystem.IMPERIAL else '21.1°C'}"
        )

    return get_temperature_meteocalc_object(
        (
            1.98
            * (temp_obj.f - (0.55 - (0.0055 * relative_humidity)) * (temp_obj.f - 58.0))
            - 56.83
        ),
        UnitSystem.IMPERIAL,
    )


def get_temperature_meteocalc_object(
    temperature: float, unit_system: UnitSystem
) -> meteocalc.Temp:
    """Get a temperature meteocalc object.

    Args:
        temperature: A float representing temperature.
        unit_system: A target unit system.

    Returns:
        A meteocalc.Temp object.
    """
    if unit_system == UnitSystem.IMPERIAL:
        unit = "f"
    else:
        unit = "c"
    return meteocalc.Temp(temperature, unit)


def get_wind_chill_meteocalc_object(
    temperature: float, wind_speed: float, unit_system: UnitSystem
) -> meteocalc.Temp:
    """Get a wind chill meteocalc object.

    Args:
        temperature: A float representing temperature.
        wind_speed: A float representing wind speed.
        unit_system: A target unit system.

    Returns:
        A meteocalc.Temp object.
    """
    temp_obj = get_temperature_meteocalc_object(temperature, unit_system)
    return meteocalc.wind_chill(temp_obj, wind_speed)
