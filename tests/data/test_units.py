"""Define tests for unit systems."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest

from ecowitt2mqtt.const import (
    CONF_INPUT_UNIT_SYSTEM,
    CONF_OUTPUT_UNIT_ACCUMULATED_PRECIPITATION,
    CONF_OUTPUT_UNIT_DISTANCE,
    CONF_OUTPUT_UNIT_HUMIDITY,
    CONF_OUTPUT_UNIT_ILLUMINANCE,
    CONF_OUTPUT_UNIT_PRECIPITATION_RATE,
    CONF_OUTPUT_UNIT_PRESSURE,
    CONF_OUTPUT_UNIT_SPEED,
    CONF_OUTPUT_UNIT_SYSTEM,
    CONF_OUTPUT_UNIT_TEMPERATURE,
    DEGREE,
    ILLUMINANCE_LUX,
    ILLUMINANCE_WATTS_PER_SQUARE_METER,
    LENGTH_KILOMETERS,
    LENGTH_MILES,
    PERCENTAGE,
    PRECIPITATION_INCHES,
    PRECIPITATION_INCHES_PER_HOUR,
    PRECIPITATION_MILLIMETERS,
    PRECIPITATION_MILLIMETERS_PER_HOUR,
    PRESSURE_HPA,
    PRESSURE_INHG,
    SPEED_KILOMETERS_PER_HOUR,
    SPEED_MILES_PER_HOUR,
    STRIKES,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    TIME_MINUTES,
    TIME_SECONDS,
    UNIT_SYSTEM_METRIC,
    UV_INDEX,
    VOLUME_GRAMS_PER_CUBIC_METER,
    VOLUME_POUNDS_PER_CUBIC_FOOT,
)
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, DataPointType
from ecowitt2mqtt.helpers.calculator.battery import BooleanBatteryState
from ecowitt2mqtt.helpers.calculator.temperature import (
    FrostRisk,
    SimmerZone,
    ThermalPerception,
)
from tests.common import TEST_CONFIG_JSON


@pytest.mark.parametrize(
    "config",
    [
        TEST_CONFIG_JSON
        | {
            CONF_OUTPUT_UNIT_ACCUMULATED_PRECIPITATION: PRECIPITATION_MILLIMETERS,
            CONF_OUTPUT_UNIT_DISTANCE: LENGTH_KILOMETERS,
            CONF_OUTPUT_UNIT_HUMIDITY: VOLUME_GRAMS_PER_CUBIC_METER,
            CONF_OUTPUT_UNIT_ILLUMINANCE: ILLUMINANCE_LUX,
            CONF_OUTPUT_UNIT_PRECIPITATION_RATE: PRECIPITATION_MILLIMETERS_PER_HOUR,
            CONF_OUTPUT_UNIT_PRESSURE: PRESSURE_HPA,
            CONF_OUTPUT_UNIT_SPEED: SPEED_KILOMETERS_PER_HOUR,
            CONF_OUTPUT_UNIT_TEMPERATURE: TEMP_CELSIUS,
        }
    ],
)
def test_output_units(device_data: dict[str, Any], ecowitt: Ecowitt) -> None:
    """Test providing output units.

    Args:
        device_data: A dictionary of device data.
        ecowitt: An Ecowitt object.
    """
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)
    assert processed_data.output == {
        "runtime": CalculatedDataPoint(
            "runtime",
            319206.0,
            unit=TIME_SECONDS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tempin": CalculatedDataPoint(
            "temp",
            26.4,
            unit=TEMP_CELSIUS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityin": CalculatedDataPoint(
            "humidity",
            31.0,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "baromrel": CalculatedDataPoint(
            "barom",
            837.7925496203633,
            unit=PRESSURE_HPA,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "baromabs": CalculatedDataPoint(
            "barom",
            837.7925496203633,
            unit=PRESSURE_HPA,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "temp": CalculatedDataPoint(
            "temp",
            34.0,
            unit=TEMP_CELSIUS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidity": CalculatedDataPoint(
            "humidity",
            64,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "winddir": CalculatedDataPoint(
            "winddir",
            139.0,
            unit=DEGREE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "windspeed": CalculatedDataPoint(
            "wind",
            33.619196159999994,
            unit=SPEED_KILOMETERS_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "windgust": CalculatedDataPoint(
            "gust",
            1.8024652800000003,
            unit=SPEED_KILOMETERS_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "maxdailygust": CalculatedDataPoint(
            "gust",
            12.9552192,
            unit=SPEED_KILOMETERS_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "solarradiation": CalculatedDataPoint(
            "solarradiation",
            33494.93670886076,
            unit=ILLUMINANCE_LUX,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "solarradiation_perceived": CalculatedDataPoint(
            "solarradiation_perceived",
            90.49958322993245,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "uv": CalculatedDataPoint(
            "uv",
            2.0,
            unit=UV_INDEX,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_1": CalculatedDataPoint(
            "safe_exposure_time_skin_type_1",
            83.3,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": "Scandinavian, Celtic",
                "tanning_ability": "Always burns, does not tan",
                "typical_features": (
                    "Very fair skin, white; red or blond hair; light-colored eyes; "
                    "freckles likely"
                ),
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_2": CalculatedDataPoint(
            "safe_exposure_time_skin_type_2",
            100.0,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": "Northern European (Caucasian)",
                "tanning_ability": "Burns easily, tans poorly",
                "typical_features": "Fair skin, white; light eyes; light hair",
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_3": CalculatedDataPoint(
            "safe_exposure_time_skin_type_3",
            133.3,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": "Darker Caucasian (Central Europe)",
                "tanning_ability": "Tans after initial burn",
                "typical_features": (
                    "Fair skin, cream white; any eye or hair color (very common skin "
                    "type)"
                ),
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_4": CalculatedDataPoint(
            "safe_exposure_time_skin_type_4",
            166.7,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": "Mediterranean, Asian, Hispanic",
                "tanning_ability": "Burns minimally, tans easily",
                "typical_features": (
                    "Olive skin, typical Mediterranean Caucasian skin; dark brown "
                    "hair; medium to heavy pigmentation"
                ),
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_5": CalculatedDataPoint(
            "safe_exposure_time_skin_type_5",
            266.7,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": (
                    "Middle eastern, Latin, light-skinned African-American, Indian"
                ),
                "tanning_ability": "Rarely burns, tans darkly easily",
                "typical_features": (
                    "Brown skin, typical Middle Eastern skin; dark hair; rarely sun "
                    "sensitive"
                ),
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_6": CalculatedDataPoint(
            "safe_exposure_time_skin_type_6",
            433.3,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": "Dark-skinned African American",
                "tanning_ability": "Never burns, always tans darkly",
                "typical_features": "Black skin; rarely sun sensitive",
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "rainrate": CalculatedDataPoint(
            "rainrate",
            0.0,
            unit=PRECIPITATION_MILLIMETERS_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "eventrain": CalculatedDataPoint(
            "rain",
            0.0,
            unit=PRECIPITATION_MILLIMETERS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "hourlyrain": CalculatedDataPoint(
            "rain",
            0.0,
            unit=PRECIPITATION_MILLIMETERS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "dailyrain": CalculatedDataPoint(
            "rain",
            0.0,
            unit=PRECIPITATION_MILLIMETERS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "weeklyrain": CalculatedDataPoint(
            "rain",
            0.0,
            unit=PRECIPITATION_MILLIMETERS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "monthlyrain": CalculatedDataPoint(
            "rain",
            55.2958,
            unit=PRECIPITATION_MILLIMETERS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "yearlyrain": CalculatedDataPoint(
            "rain",
            112.8014,
            unit=PRECIPITATION_MILLIMETERS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "lightning_num": CalculatedDataPoint(
            "lightning_num",
            13,
            unit=STRIKES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "lightning": CalculatedDataPoint(
            "lightning",
            1.0,
            unit=LENGTH_KILOMETERS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "lightning_time": CalculatedDataPoint(
            "lightning_time",
            datetime(2022, 4, 20, 17, 17, 17, tzinfo=timezone.utc),
        ),
        "wh65batt": CalculatedDataPoint(
            "batt",
            BooleanBatteryState.OFF,
            unit=None,
            attributes={},
            data_type=DataPointType.BOOLEAN,
        ),
        "dewpoint": CalculatedDataPoint(
            "dewpoint",
            26.218493204536873,
            unit=TEMP_CELSIUS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "feelslike": CalculatedDataPoint(
            "feelslike",
            43.91961232755561,
            unit=TEMP_CELSIUS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "heatindex": CalculatedDataPoint(
            "heatindex",
            43.91961232755561,
            unit=TEMP_CELSIUS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "windchill": CalculatedDataPoint(
            "windchill",
            None,
            unit=TEMP_CELSIUS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=24.054020931926463,
            unit=VOLUME_GRAMS_PER_CUBIC_METER,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=24.054020931926463,
            unit=VOLUME_GRAMS_PER_CUBIC_METER,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception",
            value=ThermalPerception.SEVERELY_HIGH,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint",
            value=21.2715682499703,
            unit=TEMP_CELSIUS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "frostrisk": CalculatedDataPoint(
            data_point_key="frostrisk",
            value=FrostRisk.NO_RISK,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "simmerindex": CalculatedDataPoint(
            data_point_key="simmerindex",
            value=45.50344000000001,
            unit=TEMP_CELSIUS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "simmerzone": CalculatedDataPoint(
            data_point_key="simmerzone",
            value=SimmerZone.DANGER_OF_HEATSTROKE,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "beaufortscale": CalculatedDataPoint(
            data_point_key="beaufortscale",
            value=5,
            unit=None,
            attributes={
                "description": "Fresh breeze",
                "sea_conditions": (
                    "Moderate waves taking a more pronounced long form; many "
                    "white horses are formed; chance of some spray"
                ),
                "land_conditions": (
                    "Small trees in leaf begin to sway; crested wavelets form "
                    "on inland waters"
                ),
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidex": CalculatedDataPoint(
            data_point_key="humidex",
            value=48,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
    }


@pytest.mark.parametrize(
    "config,device_data_filename",
    [
        (
            TEST_CONFIG_JSON | {CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_METRIC},
            "payload_gw1000bpro_metric.json",
        )
    ],
)
def test_unit_conversion_to_imperial(
    device_data: dict[str, Any], ecowitt: Ecowitt
) -> None:
    """Test conversion between units.

    Args:
        device_data: A dictionary of device data.
        ecowitt: An Ecowitt object.
    """
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)
    assert processed_data.output == {
        "runtime": CalculatedDataPoint(
            "runtime",
            319206,
            unit=TIME_SECONDS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tempin": CalculatedDataPoint(
            "temp",
            79.52,
            unit=TEMP_FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityin": CalculatedDataPoint(
            "humidity",
            31,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "baromrel": CalculatedDataPoint(
            "barom",
            837.793,
            unit=PRESSURE_INHG,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "baromabs": CalculatedDataPoint(
            "barom",
            837.793,
            unit=PRESSURE_INHG,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "temp": CalculatedDataPoint(
            "temp",
            24.08,
            unit=TEMP_FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidity": CalculatedDataPoint(
            "humidity",
            74,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "winddir": CalculatedDataPoint(
            "winddir",
            139,
            unit=DEGREE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "windspeed": CalculatedDataPoint(
            "wind",
            32.4,
            unit=SPEED_MILES_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "windgust": CalculatedDataPoint(
            "gust",
            1.8,
            unit=SPEED_MILES_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "maxdailygust": CalculatedDataPoint(
            "gust",
            13.0,
            unit=SPEED_MILES_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "solarradiation": CalculatedDataPoint(
            "solarradiation",
            264.61,
            unit=ILLUMINANCE_WATTS_PER_SQUARE_METER,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "solarradiation_perceived": CalculatedDataPoint(
            "solarradiation_perceived",
            90.49958322993245,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "uv": CalculatedDataPoint(
            "uv",
            2.0,
            unit=UV_INDEX,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_1": CalculatedDataPoint(
            "safe_exposure_time_skin_type_1",
            83.3,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": "Scandinavian, Celtic",
                "tanning_ability": "Always burns, does not tan",
                "typical_features": (
                    "Very fair skin, white; red or blond hair; light-colored eyes; "
                    "freckles likely"
                ),
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_2": CalculatedDataPoint(
            "safe_exposure_time_skin_type_2",
            100.0,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": "Northern European (Caucasian)",
                "tanning_ability": "Burns easily, tans poorly",
                "typical_features": "Fair skin, white; light eyes; light hair",
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_3": CalculatedDataPoint(
            "safe_exposure_time_skin_type_3",
            133.3,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": "Darker Caucasian (Central Europe)",
                "tanning_ability": "Tans after initial burn",
                "typical_features": (
                    "Fair skin, cream white; any eye or hair color (very common skin "
                    "type)"
                ),
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_4": CalculatedDataPoint(
            "safe_exposure_time_skin_type_4",
            166.7,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": "Mediterranean, Asian, Hispanic",
                "tanning_ability": "Burns minimally, tans easily",
                "typical_features": (
                    "Olive skin, typical Mediterranean Caucasian skin; dark brown "
                    "hair; medium to heavy pigmentation"
                ),
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_5": CalculatedDataPoint(
            "safe_exposure_time_skin_type_5",
            266.7,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": (
                    "Middle eastern, Latin, light-skinned African-American, Indian"
                ),
                "tanning_ability": "Rarely burns, tans darkly easily",
                "typical_features": (
                    "Brown skin, typical Middle Eastern skin; dark hair; rarely sun "
                    "sensitive"
                ),
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "safe_exposure_time_skin_type_6": CalculatedDataPoint(
            "safe_exposure_time_skin_type_6",
            433.3,
            unit=TIME_MINUTES,
            attributes={
                "ethnicity": "Dark-skinned African American",
                "tanning_ability": "Never burns, always tans darkly",
                "typical_features": "Black skin; rarely sun sensitive",
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "rainrate": CalculatedDataPoint(
            "rainrate",
            0.000,
            unit=PRECIPITATION_INCHES_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "eventrain": CalculatedDataPoint(
            "rain",
            0.000,
            unit=PRECIPITATION_INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "hourlyrain": CalculatedDataPoint(
            "rain",
            0.000,
            unit=PRECIPITATION_INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "dailyrain": CalculatedDataPoint(
            "rain",
            0.000,
            unit=PRECIPITATION_INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "weeklyrain": CalculatedDataPoint(
            "rain",
            0.000,
            unit=PRECIPITATION_INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "monthlyrain": CalculatedDataPoint(
            "rain",
            55.3,
            unit=PRECIPITATION_INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "yearlyrain": CalculatedDataPoint(
            "rain",
            112.8,
            unit=PRECIPITATION_INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "lightning_num": CalculatedDataPoint(
            "lightning_num",
            13,
            unit=STRIKES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "lightning": CalculatedDataPoint(
            "lightning",
            0.6213711922373341,
            unit=LENGTH_MILES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "lightning_time": CalculatedDataPoint(
            "lightning_time", datetime(2022, 4, 20, 17, 17, 17, tzinfo=timezone.utc)
        ),
        "wh65batt": CalculatedDataPoint(
            "batt",
            BooleanBatteryState.OFF,
            unit=None,
            attributes={},
            data_type=DataPointType.BOOLEAN,
        ),
        "dewpoint": CalculatedDataPoint(
            "dewpoint",
            17.003700506238328,
            unit=TEMP_FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "feelslike": CalculatedDataPoint(
            "feelslike",
            6.296417532871434,
            unit=TEMP_FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "heatindex": CalculatedDataPoint(
            "heatindex",
            19.666,
            unit=TEMP_FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "windchill": CalculatedDataPoint(
            "windchill",
            6.296417532871434,
            unit=TEMP_FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=0.00016449986246231337,
            unit=VOLUME_POUNDS_PER_CUBIC_FOOT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=0.00016449986246231337,
            unit=VOLUME_POUNDS_PER_CUBIC_FOOT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception",
            value=ThermalPerception.DRY,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint",
            value=17.915538220062125,
            unit=TEMP_FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "frostrisk": CalculatedDataPoint(
            data_point_key="frostrisk",
            value=FrostRisk.UNLIKELY,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "simmerindex": CalculatedDataPoint(
            data_point_key="simmerindex",
            value=None,
            unit=TEMP_FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "simmerzone": CalculatedDataPoint(
            data_point_key="simmerzone",
            value=None,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "beaufortscale": CalculatedDataPoint(
            data_point_key="beaufortscale",
            value=5,
            unit=None,
            attributes={
                "description": "Fresh breeze",
                "sea_conditions": (
                    "Moderate waves taking a more pronounced long form; many white "
                    "horses are formed; chance of some spray"
                ),
                "land_conditions": (
                    "Small trees in leaf begin to sway; crested wavelets form on "
                    "inland waters"
                ),
            },
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidex": CalculatedDataPoint(
            data_point_key="humidex",
            value=-8,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
    }


@pytest.mark.parametrize(
    "config", [TEST_CONFIG_JSON | {CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_METRIC}]
)
@pytest.mark.parametrize(
    "device_data_filename,expected_output",
    [
        (
            "payload_gw1000bpro.json",
            {
                "runtime": CalculatedDataPoint(
                    "runtime",
                    319206.0,
                    unit=TIME_SECONDS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "tempin": CalculatedDataPoint(
                    "temp",
                    26.4,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "humidityin": CalculatedDataPoint(
                    "humidity",
                    31.0,
                    unit=PERCENTAGE,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "baromrel": CalculatedDataPoint(
                    "barom",
                    837.7925496203633,
                    unit=PRESSURE_HPA,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "baromabs": CalculatedDataPoint(
                    "barom",
                    837.7925496203633,
                    unit=PRESSURE_HPA,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "temp": CalculatedDataPoint(
                    "temp",
                    34.0,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "humidity": CalculatedDataPoint(
                    "humidity",
                    64,
                    unit=PERCENTAGE,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "winddir": CalculatedDataPoint(
                    "winddir",
                    139.0,
                    unit=DEGREE,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "windspeed": CalculatedDataPoint(
                    "wind",
                    33.619196159999994,
                    unit=SPEED_KILOMETERS_PER_HOUR,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "windgust": CalculatedDataPoint(
                    "gust",
                    1.8024652800000003,
                    unit=SPEED_KILOMETERS_PER_HOUR,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "maxdailygust": CalculatedDataPoint(
                    "gust",
                    12.9552192,
                    unit=SPEED_KILOMETERS_PER_HOUR,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "solarradiation": CalculatedDataPoint(
                    "solarradiation",
                    264.61,
                    unit=ILLUMINANCE_WATTS_PER_SQUARE_METER,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "solarradiation_perceived": CalculatedDataPoint(
                    "solarradiation_perceived",
                    90.49958322993245,
                    unit=PERCENTAGE,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "uv": CalculatedDataPoint(
                    "uv",
                    2.0,
                    unit=UV_INDEX,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_1": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_1",
                    83.3,
                    unit=TIME_MINUTES,
                    attributes={
                        "ethnicity": "Scandinavian, Celtic",
                        "tanning_ability": "Always burns, does not tan",
                        "typical_features": (
                            "Very fair skin, white; red or blond hair; light-colored "
                            "eyes; freckles likely"
                        ),
                    },
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_2": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_2",
                    100.0,
                    unit=TIME_MINUTES,
                    attributes={
                        "ethnicity": "Northern European (Caucasian)",
                        "tanning_ability": "Burns easily, tans poorly",
                        "typical_features": "Fair skin, white; light eyes; light hair",
                    },
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_3": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_3",
                    133.3,
                    unit=TIME_MINUTES,
                    attributes={
                        "ethnicity": "Darker Caucasian (Central Europe)",
                        "tanning_ability": "Tans after initial burn",
                        "typical_features": (
                            "Fair skin, cream white; any eye or hair color (very "
                            "common skin type)"
                        ),
                    },
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_4": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_4",
                    166.7,
                    unit=TIME_MINUTES,
                    attributes={
                        "ethnicity": "Mediterranean, Asian, Hispanic",
                        "tanning_ability": "Burns minimally, tans easily",
                        "typical_features": (
                            "Olive skin, typical Mediterranean Caucasian skin; dark "
                            "brown hair; medium to heavy pigmentation"
                        ),
                    },
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_5": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_5",
                    266.7,
                    unit=TIME_MINUTES,
                    attributes={
                        "ethnicity": (
                            "Middle eastern, Latin, light-skinned African-American, "
                            "Indian"
                        ),
                        "tanning_ability": "Rarely burns, tans darkly easily",
                        "typical_features": (
                            "Brown skin, typical Middle Eastern skin; dark hair; "
                            "rarely sun sensitive"
                        ),
                    },
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_6": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_6",
                    433.3,
                    unit=TIME_MINUTES,
                    attributes={
                        "ethnicity": "Dark-skinned African American",
                        "tanning_ability": "Never burns, always tans darkly",
                        "typical_features": "Black skin; rarely sun sensitive",
                    },
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "rainrate": CalculatedDataPoint(
                    "rainrate",
                    0.0,
                    unit=PRECIPITATION_MILLIMETERS_PER_HOUR,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "eventrain": CalculatedDataPoint(
                    "rain",
                    0.0,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "hourlyrain": CalculatedDataPoint(
                    "rain",
                    0.0,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "dailyrain": CalculatedDataPoint(
                    "rain",
                    0.0,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "weeklyrain": CalculatedDataPoint(
                    "rain",
                    0.0,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "monthlyrain": CalculatedDataPoint(
                    "rain",
                    55.2958,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "yearlyrain": CalculatedDataPoint(
                    "rain",
                    112.8014,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "lightning_num": CalculatedDataPoint(
                    "lightning_num",
                    13,
                    unit=STRIKES,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "lightning": CalculatedDataPoint(
                    "lightning",
                    1.0,
                    unit=LENGTH_KILOMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "lightning_time": CalculatedDataPoint(
                    "lightning_time",
                    datetime(2022, 4, 20, 17, 17, 17, tzinfo=timezone.utc),
                ),
                "wh65batt": CalculatedDataPoint(
                    "batt",
                    BooleanBatteryState.OFF,
                    unit=None,
                    attributes={},
                    data_type=DataPointType.BOOLEAN,
                ),
                "dewpoint": CalculatedDataPoint(
                    "dewpoint",
                    26.218493204536873,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "feelslike": CalculatedDataPoint(
                    "feelslike",
                    43.91961232755561,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "heatindex": CalculatedDataPoint(
                    "heatindex",
                    43.91961232755561,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "windchill": CalculatedDataPoint(
                    "windchill",
                    None,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "humidityabs": CalculatedDataPoint(
                    data_point_key="humidityabs",
                    value=24.054020931926463,
                    unit=VOLUME_GRAMS_PER_CUBIC_METER,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "humidityabsin": CalculatedDataPoint(
                    data_point_key="humidityabsin",
                    value=24.054020931926463,
                    unit=VOLUME_GRAMS_PER_CUBIC_METER,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "thermalperception": CalculatedDataPoint(
                    data_point_key="thermalperception",
                    value=ThermalPerception.SEVERELY_HIGH,
                    unit=None,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "frostpoint": CalculatedDataPoint(
                    data_point_key="frostpoint",
                    value=21.2715682499703,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "frostrisk": CalculatedDataPoint(
                    data_point_key="frostrisk",
                    value=FrostRisk.NO_RISK,
                    unit=None,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "simmerindex": CalculatedDataPoint(
                    data_point_key="simmerindex",
                    value=45.50344000000001,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "simmerzone": CalculatedDataPoint(
                    data_point_key="simmerzone",
                    value=SimmerZone.DANGER_OF_HEATSTROKE,
                    unit=None,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "beaufortscale": CalculatedDataPoint(
                    data_point_key="beaufortscale",
                    value=5,
                    unit=None,
                    attributes={
                        "description": "Fresh breeze",
                        "sea_conditions": (
                            "Moderate waves taking a more pronounced long form; many "
                            "white horses are formed; chance of some spray"
                        ),
                        "land_conditions": (
                            "Small trees in leaf begin to sway; crested wavelets form "
                            "on inland waters"
                        ),
                    },
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "humidex": CalculatedDataPoint(
                    data_point_key="humidex",
                    value=48,
                    unit=None,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
            },
        ),
        (
            "payload_gw1000pro.json",
            {
                "tempin": CalculatedDataPoint(
                    "temp",
                    24.888888888888886,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "humidityin": CalculatedDataPoint(
                    "humidity",
                    26,
                    unit=PERCENTAGE,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "baromrel": CalculatedDataPoint(
                    "barom",
                    833.1870610694995,
                    unit=PRESSURE_HPA,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "baromabs": CalculatedDataPoint(
                    "barom",
                    833.1870610694995,
                    unit=PRESSURE_HPA,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "temp": CalculatedDataPoint(
                    "temp",
                    -2.9444444444444446,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "humidity": CalculatedDataPoint(
                    "humidity",
                    27,
                    unit=PERCENTAGE,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "winddir": CalculatedDataPoint(
                    "winddir",
                    46,
                    unit=DEGREE,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "windspeed": CalculatedDataPoint(
                    "wind",
                    35.598689279999995,
                    unit=SPEED_KILOMETERS_PER_HOUR,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "windgust": CalculatedDataPoint(
                    "gust",
                    7.193767679999999,
                    unit=SPEED_KILOMETERS_PER_HOUR,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "maxdailygust": CalculatedDataPoint(
                    "gust",
                    25.556382720000002,
                    unit=SPEED_KILOMETERS_PER_HOUR,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "solarradiation": CalculatedDataPoint(
                    "solarradiation",
                    25.56,
                    unit=ILLUMINANCE_WATTS_PER_SQUARE_METER,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "solarradiation_perceived": CalculatedDataPoint(
                    "solarradiation_perceived",
                    70.19867516391842,
                    unit=PERCENTAGE,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "uv": CalculatedDataPoint(
                    "uv",
                    0,
                    unit=UV_INDEX,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_1": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_1",
                    None,
                    unit=TIME_MINUTES,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_2": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_2",
                    None,
                    unit=TIME_MINUTES,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_3": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_3",
                    None,
                    unit=TIME_MINUTES,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_4": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_4",
                    None,
                    unit=TIME_MINUTES,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_5": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_5",
                    None,
                    unit=TIME_MINUTES,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "safe_exposure_time_skin_type_6": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_6",
                    None,
                    unit=TIME_MINUTES,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "rainrate": CalculatedDataPoint(
                    "rainrate",
                    0.000,
                    unit=PRECIPITATION_MILLIMETERS_PER_HOUR,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "eventrain": CalculatedDataPoint(
                    "rain",
                    0.000,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "hourlyrain": CalculatedDataPoint(
                    "rain",
                    0.000,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "dailyrain": CalculatedDataPoint(
                    "rain",
                    0.000,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "weeklyrain": CalculatedDataPoint(
                    "rain",
                    0.000,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "monthlyrain": CalculatedDataPoint(
                    "rain",
                    0.000,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "yearlyrain": CalculatedDataPoint(
                    "rain",
                    298.6024,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "totalrain": CalculatedDataPoint(
                    "rain",
                    298.6024,
                    unit=PRECIPITATION_MILLIMETERS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "wh65batt": CalculatedDataPoint(
                    "batt",
                    BooleanBatteryState.OFF,
                    unit=None,
                    attributes={},
                    data_type=DataPointType.BOOLEAN,
                ),
                "dewpoint": CalculatedDataPoint(
                    "dewpoint",
                    -19.348468202050693,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "feelslike": CalculatedDataPoint(
                    "feelslike",
                    -10.892311666309867,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "heatindex": CalculatedDataPoint(
                    "heatindex",
                    -6.478333333333332,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "windchill": CalculatedDataPoint(
                    "windchill",
                    -10.892311666309867,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "humidityabs": CalculatedDataPoint(
                    data_point_key="humidityabs",
                    value=1.0662546271835098,
                    unit=VOLUME_GRAMS_PER_CUBIC_METER,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "humidityabsin": CalculatedDataPoint(
                    data_point_key="humidityabsin",
                    value=1.0662546271835098,
                    unit=VOLUME_GRAMS_PER_CUBIC_METER,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "thermalperception": CalculatedDataPoint(
                    data_point_key="thermalperception",
                    value=ThermalPerception.DRY,
                    unit=None,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "frostpoint": CalculatedDataPoint(
                    data_point_key="frostpoint",
                    value=-19.00542378034868,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "frostrisk": CalculatedDataPoint(
                    data_point_key="frostrisk",
                    value=FrostRisk.UNLIKELY,
                    unit=None,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "simmerindex": CalculatedDataPoint(
                    data_point_key="simmerindex",
                    value=None,
                    unit=TEMP_CELSIUS,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "simmerzone": CalculatedDataPoint(
                    data_point_key="simmerzone",
                    value=None,
                    unit=None,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "beaufortscale": CalculatedDataPoint(
                    data_point_key="beaufortscale",
                    value=5,
                    unit=None,
                    attributes={
                        "description": "Fresh breeze",
                        "sea_conditions": (
                            "Moderate waves taking a more pronounced long form; many "
                            "white horses are formed; chance of some spray"
                        ),
                        "land_conditions": (
                            "Small trees in leaf begin to sway; crested wavelets form "
                            "on inland waters"
                        ),
                    },
                    data_type=DataPointType.NON_BOOLEAN,
                ),
                "humidex": CalculatedDataPoint(
                    data_point_key="humidex",
                    value=-8,
                    unit=None,
                    attributes={},
                    data_type=DataPointType.NON_BOOLEAN,
                ),
            },
        ),
    ],
)
def test_unit_conversion_to_metric(
    device_data: dict[str, Any], ecowitt: Ecowitt, expected_output: dict[str, Any]
) -> None:
    """Test conversion between units.

    Args:
        device_data: A dictionary of device data.
        ecowitt: An Ecowitt object.
        expected_output: A dictionary of parsed output.
    """
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)
    assert processed_data.output == expected_output
