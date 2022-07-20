"""Define meteorological utilities."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import TYPE_CHECKING, cast

import meteocalc

from ecowitt2mqtt.backports.enum import StrEnum
from ecowitt2mqtt.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6,
    DEGREE,
    DISTANCE_KILOMETERS,
    DISTANCE_MILES,
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
    TIME_MINUTES,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
    UV_INDEX,
    WATER_VAPOR_GRAMS_PER_CUBIC_METER,
    WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint
from ecowitt2mqtt.helpers.typing import UnitSystemType

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

FROST_RISK_HUMIDITY_ABS_THRESHOLD = 2.8

ABSOLUTE_HUMIDITY_MAP = {
    UNIT_SYSTEM_IMPERIAL: WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
    UNIT_SYSTEM_METRIC: WATER_VAPOR_GRAMS_PER_CUBIC_METER,
}

DISTANCE_UNIT_MAP = {
    UNIT_SYSTEM_IMPERIAL: DISTANCE_MILES,
    UNIT_SYSTEM_METRIC: DISTANCE_KILOMETERS,
}

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

SAFE_EXPOSURE_CONSTANT_MAP: dict[str, float] = {
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1: 2.5,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2: 3.0,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3: 4.0,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4: 5.0,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5: 8.0,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6: 13.0,
}


class FrostRisk(StrEnum):
    """Define types of frost risk."""

    NO_RISK = "No risk"
    PROBABLE = "Probable"
    UNLIKELY = "Unlikely"
    VERY_PROBABLE = "Very probable"


class SimmerZone(StrEnum):
    """Define types of simmer zone."""

    CAUTION_HEAT_EXHAUSTION = "Caution: Heat exhaustion"
    CIRCULATORY_COLLAPSE_IMMINENT = "Circulatory collapse imminent"
    COMFORTABLE = "Comfortable"
    DANGER_OF_HEATSTROKE = "Danger of heatstroke"
    EXTREME_DANGER_OF_HEATSTROKE = "Extreme danger of heatstroke"
    INCREASED_DISCOMFORT = "Increased discomfort"
    SLIGHTLY_COOL = "Slightly cool"
    SLIGHTLY_WARM = "Slightly warm"


@dataclass
class SimmerZoneRating:
    """Define a dataclass to store a simmer zone rating."""

    zone: SimmerZone
    minimum_f: float | None = None
    maximum_f: float | None = None


class ThermalPerception(StrEnum):
    """Define types of thermal perception."""

    COMFORTABLE = "Comfortable"
    DRY = "Dry"
    EXTREMELY_UNCOMFORTABLE = "Extremely uncomfortable"
    OK_BUT_HUMID = "OK for most"
    QUITE_UNCOMFORTABLE = "Quite uncomfortable"
    SEVERELY_HIGH = "Severely high"
    SOMEWHAT_UNCOMFORTABLE = "Somewhat uncomfortable"
    VERY_COMFORTABLE = "Very comfortable"


@dataclass
class ThermalPerceptionRating:
    """Define a dataclass to store a thermal perception rating."""

    perception: ThermalPerception
    minimum_c: float
    maximum_c: float


SIMMER_ZONE_RATINGS: list[SimmerZoneRating] = [
    SimmerZoneRating(
        zone=SimmerZone.SLIGHTLY_COOL,
        minimum_f=70.0,
        maximum_f=77.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.COMFORTABLE,
        minimum_f=77.0,
        maximum_f=83.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.SLIGHTLY_WARM,
        minimum_f=83.0,
        maximum_f=91.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.INCREASED_DISCOMFORT,
        minimum_f=91.0,
        maximum_f=100.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.CAUTION_HEAT_EXHAUSTION,
        minimum_f=100.0,
        maximum_f=112.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.DANGER_OF_HEATSTROKE,
        minimum_f=112.0,
        maximum_f=125.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.EXTREME_DANGER_OF_HEATSTROKE,
        minimum_f=125.0,
        maximum_f=150.0,
    ),
    SimmerZoneRating(
        zone=SimmerZone.CIRCULATORY_COLLAPSE_IMMINENT,
        minimum_f=150.0,
        maximum_f=200.0,
    ),
]


THERMAL_PERCEPTION_RATINGS: list[ThermalPerceptionRating] = [
    ThermalPerceptionRating(
        perception=ThermalPerception.SEVERELY_HIGH,
        minimum_c=26.0,
        maximum_c=100.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.EXTREMELY_UNCOMFORTABLE,
        minimum_c=24.0,
        maximum_c=26.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.QUITE_UNCOMFORTABLE,
        minimum_c=21.0,
        maximum_c=24.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.SOMEWHAT_UNCOMFORTABLE,
        minimum_c=18.0,
        maximum_c=21.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.OK_BUT_HUMID,
        minimum_c=16.0,
        maximum_c=18.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.COMFORTABLE,
        minimum_c=13.0,
        maximum_c=16.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.VERY_COMFORTABLE,
        minimum_c=10.0,
        maximum_c=12.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.DRY,
        maximum_c=10.0,
        minimum_c=-100.0,
    ),
]


def _get_absolute_humidity(temp_obj: meteocalc.Temp, relative_humidity: float) -> float:
    """Get absolute humidity."""
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


def _get_frost_point_object(
    temp_obj: meteocalc.Temp, relative_humidity: float
) -> meteocalc.Temp:
    """Get a frost point object."""
    dew_point_obj = meteocalc.dew_point(temp_obj, relative_humidity)
    absolute_temp_c = temp_obj.c + 273.15
    absolute_dew_point_c = dew_point_obj.c + 273.15

    return _get_temperature_object(
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
        UNIT_SYSTEM_METRIC,
    )


def _get_simmer_index_object(
    temp_obj: meteocalc.Temp, relative_humidity: float
) -> meteocalc.Temp | None:
    """Get a simmer index object."""
    if temp_obj.f < 70:
        return None
    return _get_temperature_object(
        (
            1.98
            * (temp_obj.f - (0.55 - (0.0055 * relative_humidity)) * (temp_obj.f - 58.0))
            - 56.83
        ),
        UNIT_SYSTEM_IMPERIAL,
    )


def _get_temperature_object(
    temperature: float, unit_system: UnitSystemType
) -> meteocalc.Temp:
    """Get a temperature object."""
    if unit_system == UNIT_SYSTEM_IMPERIAL:
        unit = "f"
    else:
        unit = "c"
    return meteocalc.Temp(temperature, unit)


def calculate_absolute_humidity(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    temperature: float,
    relative_humidity: float,
) -> CalculatedDataPoint:
    """Calculate absolute humidity."""
    temp_obj = _get_temperature_object(temperature, ecowitt.config.input_unit_system)
    final_value = _get_absolute_humidity(temp_obj, relative_humidity)

    if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value /= 16018.46592051

    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=round(final_value, 1),
        unit=ABSOLUTE_HUMIDITY_MAP[ecowitt.config.output_unit_system],
    )


def calculate_co2(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate CO2."""
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=value, unit=CONCENTRATION_PARTS_PER_MILLION
    )


def calculate_dew_point(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    temperature: float,
    relative_humidity: float,
) -> CalculatedDataPoint:
    """Calculate dew point in the appropriate unit system."""
    temp_obj = _get_temperature_object(temperature, ecowitt.config.input_unit_system)
    dew_point_obj = meteocalc.dew_point(temp_obj, relative_humidity)

    if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(dew_point_obj.f, 1)
    else:
        final_value = round(dew_point_obj.c, 1)

    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TEMP_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_feels_like(  # pylint: disable=too-many-arguments
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    temperature: float,
    relative_humidity: float,
    wind_speed: float,
) -> CalculatedDataPoint:
    """Calculate "feels like" temperature in the appropriate unit system."""
    temp_obj = _get_temperature_object(temperature, ecowitt.config.input_unit_system)
    feels_like_obj = meteocalc.feels_like(temp_obj, relative_humidity, wind_speed)

    if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(feels_like_obj.f, 1)
    else:
        final_value = round(feels_like_obj.c, 1)

    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TEMP_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_frost_point(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    temperature: float,
    relative_humidity: float,
) -> CalculatedDataPoint:
    """Calculate frost point in the appropriate unit system."""
    temp_obj = _get_temperature_object(temperature, ecowitt.config.input_unit_system)
    frost_point_obj = _get_frost_point_object(temp_obj, relative_humidity)

    if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(frost_point_obj.f, 1)
    else:
        final_value = round(frost_point_obj.c, 1)

    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TEMP_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_frost_risk(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    temperature: float,
    relative_humidity: float,
) -> CalculatedDataPoint:
    """Calculate the risk of frost forming."""
    temp_obj = _get_temperature_object(temperature, ecowitt.config.input_unit_system)
    absolute_humidity = _get_absolute_humidity(temp_obj, relative_humidity)
    frost_point_obj = _get_frost_point_object(temp_obj, relative_humidity)

    if temp_obj.c <= 1.0 and frost_point_obj.c <= 0:
        if absolute_humidity <= FROST_RISK_HUMIDITY_ABS_THRESHOLD:
            final_value = FrostRisk.UNLIKELY
        else:
            final_value = FrostRisk.VERY_PROBABLE
    elif (
        temp_obj.c <= 4.0
        and frost_point_obj.c <= 0.5
        and absolute_humidity > FROST_RISK_HUMIDITY_ABS_THRESHOLD
    ):
        final_value = FrostRisk.PROBABLE
    else:
        final_value = FrostRisk.NO_RISK

    return CalculatedDataPoint(data_point_key=data_point_key, value=final_value)


def calculate_heat_index(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    temperature: float,
    relative_humidity: float,
) -> CalculatedDataPoint:
    """Calculate heat index in the appropriate unit system."""
    temp_obj = _get_temperature_object(temperature, ecowitt.config.input_unit_system)
    heat_index_obj = meteocalc.heat_index(temp_obj, relative_humidity)

    if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(heat_index_obj.f, 1)
    else:
        final_value = round(heat_index_obj.c, 1)

    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TEMP_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_lightning_strike_distance(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate lightning strike distance in the appropriate unit system.

    Note that lightning strike distances always have metric as the input unit system.
    """
    if ecowitt.config.output_unit_system == UNIT_SYSTEM_METRIC:
        final_value = value
    else:
        final_value = round(value / 1.609, 1)

    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=DISTANCE_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_lightning_strikes(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate lightning strikes."""
    return CalculatedDataPoint(data_point_key=data_point_key, value=value, unit=STRIKES)


def calculate_moisture(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate moisture."""
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=value, unit=PERCENTAGE
    )


def calculate_pm25(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate PM2.5 pollution."""
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=value,
        unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    )


def calculate_pm10(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate PM10.0 pollution."""
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=value,
        unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    )


def calculate_pressure(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
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


def calculate_rain_rate(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate rain rate in the appropriate unit system."""
    data_point = calculate_rain_volume(
        ecowitt, payload_key, data_point_key, value=value
    )
    data_point.unit = f"{data_point.unit}/hr"
    return data_point


def calculate_rain_volume(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
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


def calculate_relative_humidity(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate relative humidity."""
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=value, unit=PERCENTAGE
    )


def calculate_safe_exposure_time(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate the number of minutes one can be safely exposed to a UV index."""
    try:
        final_value = round(
            (200 * SAFE_EXPOSURE_CONSTANT_MAP[payload_key]) / (3 * value), 1
        )
    except ZeroDivisionError:
        final_value = None

    return CalculatedDataPoint(
        data_point_key=data_point_key, value=final_value, unit=TIME_MINUTES
    )


def calculate_simmer_index(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    temperature: float,
    relative_humidity: float,
) -> CalculatedDataPoint:
    """Calculate simmer index in the appropriate unit system."""
    temp_obj = _get_temperature_object(temperature, ecowitt.config.input_unit_system)
    simmer_obj = _get_simmer_index_object(temp_obj, relative_humidity)

    if simmer_obj:
        if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            final_value = round(simmer_obj.f, 1)
        else:
            final_value = round(simmer_obj.c, 1)
    else:
        final_value = None

    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TEMP_UNIT_MAP[ecowitt.config.output_unit_system],
    )


def calculate_simmer_zone(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    temperature: float,
    relative_humidity: float,
) -> CalculatedDataPoint:
    """Calculate the human perception of comfort level related to temperature."""
    temp_obj = _get_temperature_object(temperature, ecowitt.config.input_unit_system)
    simmer_obj = _get_simmer_index_object(temp_obj, relative_humidity)

    if simmer_obj:
        [rating] = [
            r for r in SIMMER_ZONE_RATINGS if r.minimum_f <= simmer_obj.f <= r.maximum_f
        ]
        final_value = rating.zone
    else:
        final_value = None

    return CalculatedDataPoint(data_point_key=data_point_key, value=final_value)


def calculate_solar_radiation_lux(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate solar radiation (lux)."""
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=round(float(value) / 0.0079, 1),
        unit=LIGHT_LUX,
    )


def calculate_solar_radiation_perceived(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate solar radiation (% perceived)."""
    lux_data_point = calculate_solar_radiation_lux(
        ecowitt, payload_key, data_point_key, value=value
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
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate solar radiation (W/m²)."""
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=value,
        unit=IRRADIATION_WATTS_PER_SQUARE_METER,
    )


def calculate_temperature(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
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


def calculate_thermal_perception(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    temperature: float,
    relative_humidity: float,
) -> CalculatedDataPoint:
    """Calculate the human perception of comfort level related to dew point."""
    temp_obj = _get_temperature_object(temperature, ecowitt.config.input_unit_system)
    dew_point_obj = meteocalc.dew_point(temp_obj, relative_humidity)

    [rating] = [
        r
        for r in THERMAL_PERCEPTION_RATINGS
        if r.minimum_c <= dew_point_obj.c <= r.maximum_c
    ]

    return CalculatedDataPoint(data_point_key=data_point_key, value=rating.perception)


def calculate_uv_index(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate UV index."""
    return CalculatedDataPoint(
        data_point_key=data_point_key, value=value, unit=UV_INDEX
    )


def calculate_wind_chill(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    temperature: float,
    wind_speed: float,
) -> CalculatedDataPoint:
    """Calculate wind chill in the appropriate unit system.

    Note that because wind chill only applies at certain combinations of temperature
    and wind speed, it is possible for this method to return None.
    """
    temp_obj = _get_temperature_object(temperature, ecowitt.config.input_unit_system)

    try:
        wind_chill_obj = meteocalc.wind_chill(temp_obj, wind_speed)
    except ValueError as err:
        LOGGER.debug("%s (temperature: %s, wind speed: %s)", err, temp_obj, wind_speed)
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
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
) -> CalculatedDataPoint:
    """Calculate wind direction."""
    return CalculatedDataPoint(data_point_key=data_point_key, value=value, unit=DEGREE)


def calculate_wind_speed(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, value: float
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
