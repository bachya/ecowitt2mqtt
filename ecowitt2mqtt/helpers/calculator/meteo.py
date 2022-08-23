"""Define meteorological helpers."""
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

IMPERIAL_HIGH_THRESHOLD = 110.0
IMPERIAL_LOW_THRESHOLD = -10.0

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


@dataclass
class BeaufortScaleRating:  # pylint: disable=too-many-instance-attributes
    """Define a dataclass to store a Beaufort scale rating."""

    number: int
    minimum_kmh: float
    maximum_kmh: float
    minimum_mph: float
    maximum_mph: float
    description: str
    sea_conditions: str
    land_conditions: str


BEAUFORT_SCALE_RATINGS: list[BeaufortScaleRating] = [
    BeaufortScaleRating(
        number=0,
        minimum_kmh=0.0,
        maximum_kmh=2.0,
        minimum_mph=0.0,
        maximum_mph=1.0,
        description="Calm",
        sea_conditions="Sea like a mirror",
        land_conditions="Smoke rises vertically",
    ),
    BeaufortScaleRating(
        number=1,
        minimum_kmh=2.0,
        maximum_kmh=6.0,
        minimum_mph=1.0,
        maximum_mph=4.0,
        description="Light air",
        sea_conditions=(
            "Ripples with appearance of scales are formed, without foam crests"
        ),
        land_conditions="Direction shown by smoke drift but not by wind vanes",
    ),
    BeaufortScaleRating(
        number=2,
        minimum_kmh=6.0,
        maximum_kmh=12.0,
        minimum_mph=4.0,
        maximum_mph=8.0,
        description="Light breeze",
        sea_conditions=(
            "Small wavelets still short but more pronounced; crests have a glassy "
            "appearance but do not break"
        ),
        land_conditions="Wind felt on face; leaves rustle; wind vane moved by wind",
    ),
    BeaufortScaleRating(
        number=3,
        minimum_kmh=12.0,
        maximum_kmh=20.0,
        minimum_mph=8.0,
        maximum_mph=13.0,
        description="Gentle breeze",
        sea_conditions=(
            "Large wavelets; crests begin to break; foam of glassy appearance; perhaps "
            "scattered white horses"
        ),
        land_conditions=(
            "Leaves and small twigs in constant motion; light flags extended"
        ),
    ),
    BeaufortScaleRating(
        number=4,
        minimum_kmh=20.0,
        maximum_kmh=29.0,
        minimum_mph=13.0,
        maximum_mph=19.0,
        description="Moderate breeze",
        sea_conditions="Small waves becoming longer; fairly frequent white horses",
        land_conditions="Raises dust and loose paper; small branches moved",
    ),
    BeaufortScaleRating(
        number=5,
        minimum_kmh=29.0,
        maximum_kmh=39.0,
        minimum_mph=19.0,
        maximum_mph=25.0,
        description="Fresh breeze",
        sea_conditions=(
            "Moderate waves taking a more pronounced long form; many white horses are "
            "formed; chance of some spray"
        ),
        land_conditions=(
            "Small trees in leaf begin to sway; crested wavelets form on inland waters"
        ),
    ),
    BeaufortScaleRating(
        number=6,
        minimum_kmh=39.0,
        maximum_kmh=50.0,
        minimum_mph=25.0,
        maximum_mph=32.0,
        description="Strong breeze",
        sea_conditions=(
            "Large waves begin to form; the white foam crests are more "
            "extensive everywhere; probably some spray"
        ),
        land_conditions=(
            "Large branches in motion; whistling heard in telegraph wires; "
            "umbrellas used with difficulty"
        ),
    ),
    BeaufortScaleRating(
        number=7,
        minimum_kmh=50.0,
        maximum_kmh=62.0,
        minimum_mph=32.0,
        maximum_mph=39.0,
        description="High wind, moderate gale, near gale",
        sea_conditions=(
            "Sea heaps up and white foam from breaking waves begins to be "
            "blown in streaks along the direction of the wind; spindrift begins to be "
            "seen"
        ),
        land_conditions=(
            "Whole trees in motion; inconvenience felt when walking against the wind"
        ),
    ),
    BeaufortScaleRating(
        number=8,
        minimum_kmh=62.0,
        maximum_kmh=75.0,
        minimum_mph=39.0,
        maximum_mph=47.0,
        description="Gale, fresh gale",
        sea_conditions=(
            "Moderately high waves of greater length; edges of crests break into "
            "spindrift; foam is blown in well-marked streaks along the direction of "
            "the wind"
        ),
        land_conditions=("Twigs break off trees; generally impedes progress"),
    ),
    BeaufortScaleRating(
        number=9,
        minimum_kmh=75.0,
        maximum_kmh=89.0,
        minimum_mph=47.0,
        maximum_mph=55.0,
        description="Strong/severe gale",
        sea_conditions=(
            "High waves; dense streaks of foam along the direction of the "
            "wind; sea begins to roll; spray affects visibility"
        ),
        land_conditions="Slight structural damage (chimney pots and slates removed)",
    ),
    BeaufortScaleRating(
        number=10,
        minimum_kmh=89.0,
        maximum_kmh=103.0,
        minimum_mph=55.0,
        maximum_mph=64.0,
        description="Storm, whole gale",
        sea_conditions=(
            "Very high waves with long overhanging crests; resulting foam in great "
            "patches is blown in dense white streaks along the direction of the wind; "
            "on the whole the surface of the sea takes on a white appearance; rolling "
            "of the sea becomes heavy; visibility affected"
        ),
        land_conditions=(
            "Seldom experienced inland; trees uprooted; considerable structural damage"
        ),
    ),
    BeaufortScaleRating(
        number=11,
        minimum_kmh=103.0,
        maximum_kmh=118.0,
        minimum_mph=64.0,
        maximum_mph=73.0,
        description="Violent storm",
        sea_conditions=(
            "Exceptionally high waves; small- and medium-sized ships might be for a "
            "long time lost to view behind the waves; sea is covered with long white "
            "patches of foam; everywhere the edges of the wave crests are blown into "
            "foam; visibility affected"
        ),
        land_conditions="Very rarely experienced; accompanied by widespread damage",
    ),
    BeaufortScaleRating(
        number=12,
        minimum_kmh=118.0,
        maximum_kmh=300.0,
        minimum_mph=73.0,
        maximum_mph=200.0,
        description="Hurricane force",
        sea_conditions=(
            "The air is filled with foam and spray; sea is completely white with "
            "driving spray; visibility very seriously affected"
        ),
        land_conditions="Devastation",
    ),
]


class FrostRisk(StrEnum):
    """Define types of frost risk."""

    NO_RISK = "No risk"
    PROBABLE = "Probable"
    UNLIKELY = "Unlikely"
    VERY_PROBABLE = "Very probable"


@dataclass
class SafeExposureInfo:
    """Define a dataclass to store information about a safe exposure level."""

    constant: float
    typical_features: str
    tanning_ability: str
    ethnicity: str


SAFE_EXPOSURE_INFO_MAP: dict[str, SafeExposureInfo] = {
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1: SafeExposureInfo(
        constant=2.5,
        ethnicity="Scandinavian, Celtic",
        tanning_ability="Always burns, does not tan",
        typical_features=(
            "Very fair skin, white; red or blond hair; light-colored eyes; freckles "
            "likely"
        ),
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2: SafeExposureInfo(
        constant=3.0,
        ethnicity="Northern European (Caucasian)",
        tanning_ability="Burns easily, tans poorly",
        typical_features="Fair skin, white; light eyes; light hair",
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3: SafeExposureInfo(
        constant=4.0,
        ethnicity="Darker Caucasian (Central Europe)",
        tanning_ability="Tans after initial burn",
        typical_features=(
            "Fair skin, cream white; any eye or hair color (very common skin type)"
        ),
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4: SafeExposureInfo(
        constant=5.0,
        ethnicity="Mediterranean, Asian, Hispanic",
        tanning_ability="Burns minimally, tans easily",
        typical_features=(
            "Olive skin, typical Mediterranean Caucasian skin; dark brown hair; medium "
            "to heavy pigmentation"
        ),
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5: SafeExposureInfo(
        constant=8.0,
        ethnicity="Middle eastern, Latin, light-skinned African-American, Indian",
        tanning_ability="Rarely burns, tans darkly easily",
        typical_features=(
            "Brown skin, typical Middle Eastern skin; dark hair; rarely sun sensitive"
        ),
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6: SafeExposureInfo(
        constant=13.0,
        ethnicity="Dark-skinned African American",
        tanning_ability="Never burns, always tans darkly",
        typical_features="Black skin; rarely sun sensitive",
    ),
}


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
        minimum_c=12.0,
        maximum_c=16.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.VERY_COMFORTABLE,
        minimum_c=10.0,
        maximum_c=12.0,
    ),
    ThermalPerceptionRating(
        perception=ThermalPerception.DRY,
        minimum_c=-100.0,
        maximum_c=10.0,
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
        raise ValueError(
            "Simmer Index is only valid for temperatures above 70°F (21.1 °C)"
        )

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


def calculate_beaufort_scale(
    ecowitt: Ecowitt,
    payload_key: str,
    data_point_key: str,
    wind_speed: float,
) -> CalculatedDataPoint:
    """Calculate the Beaufort Scale of a wind speed."""
    [rating] = [
        r
        for r in BEAUFORT_SCALE_RATINGS
        if (
            ecowitt.config.input_unit_system == UNIT_SYSTEM_IMPERIAL
            and r.minimum_mph <= wind_speed < r.maximum_mph
        )
        or (
            ecowitt.config.input_unit_system == UNIT_SYSTEM_METRIC
            and r.minimum_kmh <= wind_speed < r.maximum_kmh
        )
    ]

    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=rating.number,
        attributes={
            "description": rating.description,
            "sea_conditions": rating.sea_conditions,
            "land_conditions": rating.land_conditions,
        },
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
    try:
        final_value = float(value)
    except ValueError:
        LOGGER.debug("Can't convert value to number: %s", value)
        return CalculatedDataPoint(data_point_key=data_point_key, value=None)

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
    safe_exposure_info = SAFE_EXPOSURE_INFO_MAP[payload_key]

    try:
        final_value = round((200 * safe_exposure_info.constant) / (3 * value), 1)
    except ZeroDivisionError:
        return CalculatedDataPoint(
            data_point_key=data_point_key, value=None, unit=TIME_MINUTES
        )

    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=TIME_MINUTES,
        attributes={
            "ethnicity": safe_exposure_info.ethnicity,
            "tanning_ability": safe_exposure_info.tanning_ability,
            "typical_features": safe_exposure_info.typical_features,
        },
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

    try:
        simmer_obj = _get_simmer_index_object(temp_obj, relative_humidity)
    except ValueError as err:
        LOGGER.debug("%s (temperature: %s)", err, temp_obj)
        final_value = None
    else:
        assert simmer_obj
        if ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            final_value = round(simmer_obj.f, 1)
        else:
            final_value = round(simmer_obj.c, 1)

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

    try:
        simmer_obj = _get_simmer_index_object(temp_obj, relative_humidity)
    except ValueError as err:
        LOGGER.debug("%s (temperature: %s)", err, temp_obj)
        final_value = None
    else:
        assert simmer_obj
        [rating] = [
            r for r in SIMMER_ZONE_RATINGS if r.minimum_f <= simmer_obj.f < r.maximum_f
        ]
        final_value = rating.zone

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

    if temp_obj.f < IMPERIAL_LOW_THRESHOLD or temp_obj.f > IMPERIAL_HIGH_THRESHOLD:
        LOGGER.warning(
            'Value of "%s" (%s) with input unit system "%s" seems suspicious',
            payload_key,
            value,
            ecowitt.config.input_unit_system,
        )

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
        if r.minimum_c <= dew_point_obj.c < r.maximum_c
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
