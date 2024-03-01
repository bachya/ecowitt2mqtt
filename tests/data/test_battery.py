"""Define tests for batteries and battery strategies."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pytest

from ecowitt2mqtt.const import (
    CONF_BATTERY_OVERRIDES,
    CONF_DEFAULT_BATTERY_STRATEGY,
    DEGREE,
    PERCENTAGE,
    STRIKES,
    UV_INDEX,
    UnitOfAccumulatedPrecipitation,
    UnitOfElectricPotential,
    UnitOfIlluminance,
    UnitOfLength,
    UnitOfPrecipitationRate,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
)
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, DataPointType
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy, BooleanBatteryState
from ecowitt2mqtt.helpers.calculator.temperature import (
    FrostRisk,
    HumidexPerception,
    RsiPerception,
    SimmerZone,
    ThermalPerception,
)
from tests.common import TEST_CONFIG_JSON


@pytest.mark.parametrize(
    "config",
    [
        TEST_CONFIG_JSON
        | {
            CONF_BATTERY_OVERRIDES: (
                "wh40batt=numeric",
                "soilbatt1=numeric",
                "wh26batt=percentage",
            )
        }
    ],
)
@pytest.mark.parametrize("device_data_filename", ["payload_gw1100b.json"])
def test_battery_config(device_data: dict[str, Any], ecowitt: Ecowitt) -> None:
    """Test overriding a battery configuration.

    Args:
        device_data: A dictionary of device data.
        ecowitt: An Ecowitt object.
    """
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)
    assert processed_data.output == {
        "tempin": CalculatedDataPoint(
            "temp",
            76.5,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityin": CalculatedDataPoint(
            "humidity",
            46,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "baromrel": CalculatedDataPoint(
            "barom",
            29.244,
            unit=UnitOfPressure.INHG,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "baromabs": CalculatedDataPoint(
            "barom",
            29.244,
            unit=UnitOfPressure.INHG,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "temp": CalculatedDataPoint(
            "temp",
            91.4,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidity": CalculatedDataPoint(
            "humidity",
            48,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "rainrate": CalculatedDataPoint(
            "rainrate",
            0.000,
            unit=UnitOfPrecipitationRate.INCHES_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "eventrain": CalculatedDataPoint(
            "rain",
            0.000,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "hourlyrain": CalculatedDataPoint(
            "rain",
            0.000,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "dailyrain": CalculatedDataPoint(
            "rain",
            0.000,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "weeklyrain": CalculatedDataPoint(
            "rain",
            0.004,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "monthlyrain": CalculatedDataPoint(
            "rain",
            1.402,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "yearlyrain": CalculatedDataPoint(
            "rain",
            48.504,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "totalrain": CalculatedDataPoint(
            "rain",
            48.504,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "temp1": CalculatedDataPoint(
            "temp",
            77.7,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidity1": CalculatedDataPoint(
            "humidity",
            51,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "soilmoisture1": CalculatedDataPoint(
            "moisture",
            40,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "soilmoisture2": CalculatedDataPoint(
            "moisture",
            56,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "wh40batt": CalculatedDataPoint(
            "batt",
            1.6,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "wh26batt": CalculatedDataPoint(
            "batt",
            0.0,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "batt1": CalculatedDataPoint(
            "batt",
            BooleanBatteryState.ON,
            unit=None,
            attributes={},
            data_type=DataPointType.BOOLEAN,
        ),
        "soilbatt1": CalculatedDataPoint(
            "batt",
            1.5,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "soilbatt2": CalculatedDataPoint(
            "batt",
            1.8,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch1": CalculatedDataPoint(
            "tf",
            84.7,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt1": CalculatedDataPoint(
            "batt",
            1.6,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch2": CalculatedDataPoint(
            "tf",
            82.9,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt2": CalculatedDataPoint(
            "batt",
            1.47,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch3": CalculatedDataPoint(
            "tf",
            84.0,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt3": CalculatedDataPoint(
            "batt",
            1.6,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch4": CalculatedDataPoint(
            "tf",
            84.2,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt4": CalculatedDataPoint(
            "batt",
            1.6,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch5": CalculatedDataPoint(
            "tf",
            85.1,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt5": CalculatedDataPoint(
            "batt",
            1.2,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch6": CalculatedDataPoint(
            "tf",
            84.2,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt6": CalculatedDataPoint(
            "batt",
            1.77,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch7": CalculatedDataPoint(
            "tf",
            84.3,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt7": CalculatedDataPoint(
            "batt",
            1.6,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch8": CalculatedDataPoint(
            "tf",
            84.2,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt8": CalculatedDataPoint(
            "batt",
            1.3,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "dewpoint": CalculatedDataPoint(
            "dewpoint",
            68.94187855398938,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "heatindex": CalculatedDataPoint(
            "heatindex",
            96.31383009280017,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=0.0010682941088042506,
            unit=UnitOfVolume.POUNDS_PER_CUBIC_FOOT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=0.0010682941088042506,
            unit=UnitOfVolume.POUNDS_PER_CUBIC_FOOT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception",
            value=ThermalPerception.SOMEWHAT_UNCOMFORTABLE,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint",
            value=60.34798837725798,
            unit=UnitOfTemperature.FAHRENHEIT,
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
            value=105.228248,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "simmerzone": CalculatedDataPoint(
            data_point_key="simmerzone",
            value=SimmerZone.CAUTION_HEAT_EXHAUSTION,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidex": CalculatedDataPoint(
            data_point_key="humidex",
            value=41,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidex_perception": CalculatedDataPoint(
            data_point_key="humidex_perception",
            value=HumidexPerception.GREAT_DISCOMFORT,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "relative_strain_index": CalculatedDataPoint(
            data_point_key="relative_strain_index",
            value=0.35,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "relative_strain_index_perception": CalculatedDataPoint(
            data_point_key="relative_strain_index_perception",
            value=RsiPerception.SIGNIFICANT_DISCOMFORT,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
    }


@pytest.mark.parametrize(
    "config",
    [TEST_CONFIG_JSON | {CONF_DEFAULT_BATTERY_STRATEGY: BatteryStrategy.NUMERIC}],
)
@pytest.mark.parametrize("device_data_filename", ["payload_gw1100b.json"])
def test_default_battery_strategy(
    device_data: dict[str, Any], ecowitt: Ecowitt
) -> None:
    """Test overriding the default battery configuration.

    Args:
        device_data: A dictionary of device data.
        ecowitt: An Ecowitt object.
    """
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)
    assert processed_data.output == {
        "tempin": CalculatedDataPoint(
            "temp",
            76.5,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityin": CalculatedDataPoint(
            "humidity",
            46,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "baromrel": CalculatedDataPoint(
            "barom",
            29.244,
            unit=UnitOfPressure.INHG,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "baromabs": CalculatedDataPoint(
            "barom",
            29.244,
            unit=UnitOfPressure.INHG,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "temp": CalculatedDataPoint(
            "temp",
            91.4,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidity": CalculatedDataPoint(
            "humidity",
            48,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "rainrate": CalculatedDataPoint(
            "rainrate",
            0.000,
            unit=UnitOfPrecipitationRate.INCHES_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "eventrain": CalculatedDataPoint(
            "rain",
            0.000,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "hourlyrain": CalculatedDataPoint(
            "rain",
            0.000,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "dailyrain": CalculatedDataPoint(
            "rain",
            0.000,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "weeklyrain": CalculatedDataPoint(
            "rain",
            0.004,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "monthlyrain": CalculatedDataPoint(
            "rain",
            1.402,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "yearlyrain": CalculatedDataPoint(
            "rain",
            48.504,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "totalrain": CalculatedDataPoint(
            "rain",
            48.504,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "temp1": CalculatedDataPoint(
            "temp",
            77.7,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidity1": CalculatedDataPoint(
            "humidity",
            51,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "soilmoisture1": CalculatedDataPoint(
            "moisture",
            40,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "soilmoisture2": CalculatedDataPoint(
            "moisture",
            56,
            unit=PERCENTAGE,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "wh40batt": CalculatedDataPoint(
            "batt",
            1.6,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "wh26batt": CalculatedDataPoint(
            "batt",
            BooleanBatteryState.OFF,
            unit=None,
            attributes={},
            data_type=DataPointType.BOOLEAN,
        ),
        "soilbatt1": CalculatedDataPoint(
            "batt",
            1.5,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "soilbatt2": CalculatedDataPoint(
            "batt",
            1.8,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch1": CalculatedDataPoint(
            "tf",
            84.7,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt1": CalculatedDataPoint(
            "batt",
            1.6,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch2": CalculatedDataPoint(
            "tf",
            82.9,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt2": CalculatedDataPoint(
            "batt",
            1.47,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch3": CalculatedDataPoint(
            "tf",
            84.0,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt3": CalculatedDataPoint(
            "batt",
            1.6,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch4": CalculatedDataPoint(
            "tf",
            84.2,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt4": CalculatedDataPoint(
            "batt",
            1.6,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch5": CalculatedDataPoint(
            "tf",
            85.1,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt5": CalculatedDataPoint(
            "batt",
            1.2,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch6": CalculatedDataPoint(
            "tf",
            84.2,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt6": CalculatedDataPoint(
            "batt",
            1.77,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch7": CalculatedDataPoint(
            "tf",
            84.3,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt7": CalculatedDataPoint(
            "batt",
            1.6,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_ch8": CalculatedDataPoint(
            "tf",
            84.2,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tf_batt8": CalculatedDataPoint(
            "batt",
            1.3,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "batt1": CalculatedDataPoint(
            "batt",
            1.0,
            unit=UnitOfElectricPotential.VOLT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "dewpoint": CalculatedDataPoint(
            "dewpoint",
            68.94187855398938,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "heatindex": CalculatedDataPoint(
            "heatindex",
            96.31383009280017,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=0.0010682941088042506,
            unit=UnitOfVolume.POUNDS_PER_CUBIC_FOOT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=0.0010682941088042506,
            unit=UnitOfVolume.POUNDS_PER_CUBIC_FOOT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception",
            value=ThermalPerception.SOMEWHAT_UNCOMFORTABLE,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint",
            value=60.34798837725798,
            unit=UnitOfTemperature.FAHRENHEIT,
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
            value=105.228248,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "simmerzone": CalculatedDataPoint(
            data_point_key="simmerzone",
            value=SimmerZone.CAUTION_HEAT_EXHAUSTION,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidex": CalculatedDataPoint(
            data_point_key="humidex",
            value=41,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidex_perception": CalculatedDataPoint(
            data_point_key="humidex_perception",
            value=HumidexPerception.GREAT_DISCOMFORT,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "relative_strain_index": CalculatedDataPoint(
            data_point_key="relative_strain_index",
            value=0.35,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "relative_strain_index_perception": CalculatedDataPoint(
            data_point_key="relative_strain_index_perception",
            value=RsiPerception.SIGNIFICANT_DISCOMFORT,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
    }


def test_unknown_battery(device_data: dict[str, Any], ecowitt: Ecowitt) -> None:
    """Test that an unknown battery is given the default strategy.

    Args:
        device_data: A dictionary of device data.
        ecowitt: An Ecowitt object.
    """
    device_data["playstationbattery1"] = 0
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)
    assert processed_data.output == {
        "runtime": CalculatedDataPoint(
            "runtime",
            319206.0,
            unit=UnitOfTime.SECONDS,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "tempin": CalculatedDataPoint(
            "temp",
            79.52,
            unit=UnitOfTemperature.FAHRENHEIT,
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
            24.74,
            unit=UnitOfPressure.INHG,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "baromabs": CalculatedDataPoint(
            "barom",
            24.74,
            unit=UnitOfPressure.INHG,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "temp": CalculatedDataPoint(
            "temp",
            93.2,
            unit=UnitOfTemperature.FAHRENHEIT,
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
            20.89,
            unit=UnitOfSpeed.MILES_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "windgust": CalculatedDataPoint(
            "gust",
            1.12,
            unit=UnitOfSpeed.MILES_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "maxdailygust": CalculatedDataPoint(
            "gust",
            8.05,
            unit=UnitOfSpeed.MILES_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "solarradiation": CalculatedDataPoint(
            "solarradiation",
            264.61,
            unit=UnitOfIlluminance.WATTS_PER_SQUARE_METER,
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
            unit=UnitOfTime.MINUTES,
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
            unit=UnitOfTime.MINUTES,
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
            unit=UnitOfTime.MINUTES,
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
            unit=UnitOfTime.MINUTES,
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
            unit=UnitOfTime.MINUTES,
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
            unit=UnitOfTime.MINUTES,
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
            unit=UnitOfPrecipitationRate.INCHES_PER_HOUR,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "eventrain": CalculatedDataPoint(
            "rain",
            0.0,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "hourlyrain": CalculatedDataPoint(
            "rain",
            0.0,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "dailyrain": CalculatedDataPoint(
            "rain",
            0.0,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "weeklyrain": CalculatedDataPoint(
            "rain",
            0.0,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "monthlyrain": CalculatedDataPoint(
            "rain",
            2.177,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "yearlyrain": CalculatedDataPoint(
            "rain",
            4.441,
            unit=UnitOfAccumulatedPrecipitation.INCHES,
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
            unit=UnitOfLength.MILES,
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
            79.19328776816637,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "feelslike": CalculatedDataPoint(
            "feelslike",
            111.0553021896001,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "heatindex": CalculatedDataPoint(
            "heatindex",
            111.0553021896001,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "windchill": CalculatedDataPoint(
            "windchill",
            None,
            unit=UnitOfTemperature.FAHRENHEIT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=0.001501643470436062,
            unit=UnitOfVolume.POUNDS_PER_CUBIC_FOOT,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=0.001501643470436062,
            unit=UnitOfVolume.POUNDS_PER_CUBIC_FOOT,
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
            value=70.28882284994654,
            unit=UnitOfTemperature.FAHRENHEIT,
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
            value=113.90619200000002,
            unit=UnitOfTemperature.FAHRENHEIT,
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
            value=48,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "humidex_perception": CalculatedDataPoint(
            data_point_key="humidex_perception",
            value=HumidexPerception.DANGEROUS,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "relative_strain_index": CalculatedDataPoint(
            data_point_key="relative_strain_index",
            value=0.54,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "relative_strain_index_perception": CalculatedDataPoint(
            data_point_key="relative_strain_index_perception",
            value=RsiPerception.EXTREME_DISCOMFORT,
            unit=None,
            attributes={},
            data_type=DataPointType.NON_BOOLEAN,
        ),
        "playstationbattery1": CalculatedDataPoint(
            "batt",
            BooleanBatteryState.OFF,
            unit=None,
            attributes={},
            data_type=DataPointType.BOOLEAN,
        ),
    }
