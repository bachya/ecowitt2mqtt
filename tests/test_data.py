"""Define tests for data processing."""
from datetime import datetime, timezone

import pytest

from ecowitt2mqtt.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    CONF_BATTERY_OVERRIDES,
    CONF_DEFAULT_BATTERY_STRATEGY,
    CONF_ENDPOINT,
    CONF_HASS_DISCOVERY,
    CONF_HASS_DISCOVERY_PREFIX,
    CONF_HASS_ENTITY_ID_PREFIX,
    CONF_INPUT_UNIT_SYSTEM,
    CONF_MQTT_BROKER,
    CONF_MQTT_PASSWORD,
    CONF_MQTT_PORT,
    CONF_MQTT_TOPIC,
    CONF_MQTT_USERNAME,
    CONF_OUTPUT_UNIT_SYSTEM,
    CONF_PORT,
    CONF_RAW_DATA,
    CONF_VERBOSE,
    DEGREE,
    DISTANCE_KILOMETERS,
    DISTANCE_MILES,
    ELECTRIC_POTENTIAL_VOLT,
    IRRADIATION_WATTS_PER_SQUARE_METER,
    LIGHT_LUX,
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
    TIME_SECONDS,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
    UV_INDEX,
    WATER_VAPOR_GRAMS_PER_CUBIC_METER,
    WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
)
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy, BooleanBatteryState
from ecowitt2mqtt.helpers.calculator.leak import LeakState
from ecowitt2mqtt.helpers.calculator.meteo import FrostRisk, ThermalPerception
from ecowitt2mqtt.helpers.device import Device

from tests.common import (
    TEST_ENDPOINT,
    TEST_HASS_DISCOVERY_PREFIX,
    TEST_HASS_ENTITY_ID_PREFIX,
    TEST_MQTT_BROKER,
    TEST_MQTT_PASSWORD,
    TEST_MQTT_PORT,
    TEST_MQTT_TOPIC,
    TEST_MQTT_USERNAME,
    TEST_PORT,
)


@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_BATTERY_OVERRIDES: (
                "wh40batt=numeric",
                "soilbatt1=numeric",
                "wh26batt=percentage",
            ),
            CONF_DEFAULT_BATTERY_STRATEGY: BatteryStrategy.BOOLEAN,
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: False,
            CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
            CONF_HASS_ENTITY_ID_PREFIX: TEST_HASS_ENTITY_ID_PREFIX,
            CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
            CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_PORT: TEST_PORT,
            CONF_RAW_DATA: False,
            CONF_VERBOSE: False,
        }
    ],
)
@pytest.mark.parametrize("device_data_filename", ["payload_gw1100b.json"])
def test_battery_config(device_data, ecowitt):
    """Test overriding a battery configuration."""
    processed_data = ProcessedData(ecowitt, device_data)
    assert processed_data.output == {
        "tempin": CalculatedDataPoint("temp", 76.5, unit=TEMP_FAHRENHEIT),
        "humidityin": CalculatedDataPoint("humidity", 46, unit=PERCENTAGE),
        "baromrel": CalculatedDataPoint("barom", 29.244, unit=PRESSURE_INHG),
        "baromabs": CalculatedDataPoint("barom", 29.244, unit=PRESSURE_INHG),
        "temp": CalculatedDataPoint("temp", 91.4, unit=TEMP_FAHRENHEIT),
        "humidity": CalculatedDataPoint("humidity", 48, unit=PERCENTAGE),
        "rainrate": CalculatedDataPoint(
            "rainrate", 0.000, unit=f"{RAINFALL_INCHES}/hr"
        ),
        "eventrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "hourlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "dailyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "weeklyrain": CalculatedDataPoint("rain", 0.004, unit=RAINFALL_INCHES),
        "monthlyrain": CalculatedDataPoint("rain", 1.402, unit=RAINFALL_INCHES),
        "yearlyrain": CalculatedDataPoint("rain", 48.504, unit=RAINFALL_INCHES),
        "totalrain": CalculatedDataPoint("rain", 48.504, unit=RAINFALL_INCHES),
        "temp1": CalculatedDataPoint("temp", 77.7, unit=TEMP_FAHRENHEIT),
        "humidity1": CalculatedDataPoint("humidity", 51, unit=PERCENTAGE),
        "soilmoisture1": CalculatedDataPoint("moisture", 40, unit=PERCENTAGE),
        "soilmoisture2": CalculatedDataPoint("moisture", 56, unit=PERCENTAGE),
        "wh40batt": CalculatedDataPoint("batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "wh26batt": CalculatedDataPoint("batt", 0.0, unit=PERCENTAGE),
        "batt1": CalculatedDataPoint("batt", BooleanBatteryState.ON),
        "soilbatt1": CalculatedDataPoint("batt", 1.5, unit=ELECTRIC_POTENTIAL_VOLT),
        "soilbatt2": CalculatedDataPoint("batt", 1.8, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch1": CalculatedDataPoint("tf", 84.7, unit=TEMP_FAHRENHEIT),
        "tf_batt1": CalculatedDataPoint("batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch2": CalculatedDataPoint("tf", 82.9, unit=TEMP_FAHRENHEIT),
        "tf_batt2": CalculatedDataPoint("batt", 1.47, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch3": CalculatedDataPoint("tf", 84.0, unit=TEMP_FAHRENHEIT),
        "tf_batt3": CalculatedDataPoint("batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch4": CalculatedDataPoint("tf", 84.2, unit=TEMP_FAHRENHEIT),
        "tf_batt4": CalculatedDataPoint("batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch5": CalculatedDataPoint("tf", 85.1, unit=TEMP_FAHRENHEIT),
        "tf_batt5": CalculatedDataPoint("batt", 1.2, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch6": CalculatedDataPoint("tf", 84.2, unit=TEMP_FAHRENHEIT),
        "tf_batt6": CalculatedDataPoint("batt", 1.77, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch7": CalculatedDataPoint("tf", 84.3, unit=TEMP_FAHRENHEIT),
        "tf_batt7": CalculatedDataPoint("batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch8": CalculatedDataPoint("tf", 84.2, unit=TEMP_FAHRENHEIT),
        "tf_batt8": CalculatedDataPoint("batt", 1.3, unit=ELECTRIC_POTENTIAL_VOLT),
        "dewpoint": CalculatedDataPoint("dewpoint", 68.9, unit=TEMP_FAHRENHEIT),
        "heatindex": CalculatedDataPoint("heatindex", 96.3, unit=TEMP_FAHRENHEIT),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception",
            value=ThermalPerception.SOMEWHAT_UNCOMFORTABLE,
            unit=None,
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint", value=60.3, unit="°F"
        ),
        "frostrisk": CalculatedDataPoint(
            data_point_key="frostrisk", value=FrostRisk.NO_RISK, unit=None
        ),
    }


@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_DEFAULT_BATTERY_STRATEGY: BatteryStrategy.NUMERIC,
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: False,
            CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
            CONF_HASS_ENTITY_ID_PREFIX: TEST_HASS_ENTITY_ID_PREFIX,
            CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
            CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_PORT: TEST_PORT,
            CONF_RAW_DATA: False,
            CONF_VERBOSE: False,
        }
    ],
)
@pytest.mark.parametrize("device_data_filename", ["payload_gw1100b.json"])
def test_default_battery_strategy(device_data, ecowitt):
    """Test overriding the default battery configuration."""
    processed_data = ProcessedData(ecowitt, device_data)
    assert processed_data.output == {
        "tempin": CalculatedDataPoint("temp", 76.5, unit=TEMP_FAHRENHEIT),
        "humidityin": CalculatedDataPoint("humidity", 46, unit=PERCENTAGE),
        "baromrel": CalculatedDataPoint("barom", 29.244, unit=PRESSURE_INHG),
        "baromabs": CalculatedDataPoint("barom", 29.244, unit=PRESSURE_INHG),
        "temp": CalculatedDataPoint("temp", 91.4, unit=TEMP_FAHRENHEIT),
        "humidity": CalculatedDataPoint("humidity", 48, unit=PERCENTAGE),
        "rainrate": CalculatedDataPoint(
            "rainrate", 0.000, unit=f"{RAINFALL_INCHES}/hr"
        ),
        "eventrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "hourlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "dailyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "weeklyrain": CalculatedDataPoint("rain", 0.004, unit=RAINFALL_INCHES),
        "monthlyrain": CalculatedDataPoint("rain", 1.402, unit=RAINFALL_INCHES),
        "yearlyrain": CalculatedDataPoint("rain", 48.504, unit=RAINFALL_INCHES),
        "totalrain": CalculatedDataPoint("rain", 48.504, unit=RAINFALL_INCHES),
        "temp1": CalculatedDataPoint("temp", 77.7, unit=TEMP_FAHRENHEIT),
        "humidity1": CalculatedDataPoint("humidity", 51, unit=PERCENTAGE),
        "soilmoisture1": CalculatedDataPoint("moisture", 40, unit=PERCENTAGE),
        "soilmoisture2": CalculatedDataPoint("moisture", 56, unit=PERCENTAGE),
        "wh40batt": CalculatedDataPoint("batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "wh26batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF, unit=None),
        "soilbatt1": CalculatedDataPoint("batt", 1.5, unit=ELECTRIC_POTENTIAL_VOLT),
        "soilbatt2": CalculatedDataPoint("batt", 1.8, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch1": CalculatedDataPoint("tf", 84.7, unit=TEMP_FAHRENHEIT),
        "tf_batt1": CalculatedDataPoint("batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch2": CalculatedDataPoint("tf", 82.9, unit=TEMP_FAHRENHEIT),
        "tf_batt2": CalculatedDataPoint("batt", 1.47, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch3": CalculatedDataPoint("tf", 84.0, unit=TEMP_FAHRENHEIT),
        "tf_batt3": CalculatedDataPoint("batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch4": CalculatedDataPoint("tf", 84.2, unit=TEMP_FAHRENHEIT),
        "tf_batt4": CalculatedDataPoint("batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch5": CalculatedDataPoint("tf", 85.1, unit=TEMP_FAHRENHEIT),
        "tf_batt5": CalculatedDataPoint("batt", 1.2, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch6": CalculatedDataPoint("tf", 84.2, unit=TEMP_FAHRENHEIT),
        "tf_batt6": CalculatedDataPoint("batt", 1.77, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch7": CalculatedDataPoint("tf", 84.3, unit=TEMP_FAHRENHEIT),
        "tf_batt7": CalculatedDataPoint("batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "tf_ch8": CalculatedDataPoint("tf", 84.2, unit=TEMP_FAHRENHEIT),
        "tf_batt8": CalculatedDataPoint("batt", 1.3, unit=ELECTRIC_POTENTIAL_VOLT),
        "batt1": CalculatedDataPoint("batt", 1.0, unit=ELECTRIC_POTENTIAL_VOLT),
        "dewpoint": CalculatedDataPoint("dewpoint", 68.9, unit=TEMP_FAHRENHEIT),
        "heatindex": CalculatedDataPoint("heatindex", 96.3, unit=TEMP_FAHRENHEIT),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception",
            value=ThermalPerception.SOMEWHAT_UNCOMFORTABLE,
            unit=None,
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint", value=60.3, unit="°F"
        ),
        "frostrisk": CalculatedDataPoint(
            data_point_key="frostrisk", value=FrostRisk.NO_RISK, unit=None
        ),
    }


@pytest.mark.parametrize(
    "device,device_data_filename",
    [
        (
            Device(
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "Ecowitt",
                "GW1000",
                "GW1000B_V1.7.3",
            ),
            "payload_gw1000bpro.json",
        ),
        (
            Device(
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "Unknown",
                "Unknown Device",
                "UNKNOWN_Vx.x.x",
            ),
            "payload_unknown_1.json",
        ),
        (
            Device(
                "default",
                "Unknown",
                "Unknown Device",
                "Unknown Station Type",
            ),
            "payload_unknown_2.json",
        ),
    ],
)
def test_device(device, device_data, ecowitt):
    """Test that a device object is properly created from a data payload."""
    processed_data = ProcessedData(ecowitt, device_data)
    assert processed_data.device == device


@pytest.mark.parametrize("device_data_filename", ["payload_gw2000a_1.json"])
def test_missing_distance(device_data, ecowitt, request):
    """Test that a distance key with an invalid value doesn't throw an error."""
    processed_data = ProcessedData(ecowitt, device_data)
    assert processed_data.output == {
        "runtime": CalculatedDataPoint("runtime", 3179, unit=TIME_SECONDS),
        "tempin": CalculatedDataPoint("temp", 71.2, unit=TEMP_FAHRENHEIT),
        "humidityin": CalculatedDataPoint("humidity", 49, unit=PERCENTAGE),
        "baromrel": CalculatedDataPoint("barom", 28.476, unit=PRESSURE_INHG),
        "baromabs": CalculatedDataPoint("barom", 28.476, unit=PRESSURE_INHG),
        "temp": CalculatedDataPoint("temp", 74.5, unit=TEMP_FAHRENHEIT),
        "humidity": CalculatedDataPoint("humidity", 47, unit=PERCENTAGE),
        "winddir": CalculatedDataPoint("winddir", 100, unit=DEGREE),
        "windspeed": CalculatedDataPoint("wind", 1.34, unit=SPEED_MILES_PER_HOUR),
        "windgust": CalculatedDataPoint("gust", 2.24, unit=SPEED_MILES_PER_HOUR),
        "maxdailygust": CalculatedDataPoint("gust", 2.24, unit=SPEED_MILES_PER_HOUR),
        "solarradiation": CalculatedDataPoint(
            "solarradiation", 0.00, unit=IRRADIATION_WATTS_PER_SQUARE_METER
        ),
        "solarradiation_lux": CalculatedDataPoint(
            "solarradiation_lux", 0.0, unit=LIGHT_LUX
        ),
        "solarradiation_perceived": CalculatedDataPoint(
            "solarradiation_perceived", 0.0, unit=PERCENTAGE
        ),
        "uv": CalculatedDataPoint("uv", 0, unit=UV_INDEX),
        "safe_exposure_time_skin_type_1": CalculatedDataPoint(
            "safe_exposure_time_skin_type_1", None, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_2": CalculatedDataPoint(
            "safe_exposure_time_skin_type_2", None, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_3": CalculatedDataPoint(
            "safe_exposure_time_skin_type_3", None, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_4": CalculatedDataPoint(
            "safe_exposure_time_skin_type_4", None, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_5": CalculatedDataPoint(
            "safe_exposure_time_skin_type_5", None, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_6": CalculatedDataPoint(
            "safe_exposure_time_skin_type_6", None, unit=TIME_MINUTES
        ),
        "rrain_piezo": CalculatedDataPoint(
            "rrain", 0.000, unit=f"{RAINFALL_INCHES}/hr"
        ),
        "erain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "hrain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "drain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "wrain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "mrain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "yrain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "ws90cap_volt": CalculatedDataPoint("volt", 0.6, unit=ELECTRIC_POTENTIAL_VOLT),
        "lightning_num": CalculatedDataPoint("lightning_num", 1, unit=STRIKES),
        "lightning": CalculatedDataPoint("lightning", 16.8, unit=DISTANCE_MILES),
        "lightning_time": CalculatedDataPoint("lightning_time", None, unit=None),
        "wh57batt": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
        "wh90batt": CalculatedDataPoint("batt", 3.16, unit=ELECTRIC_POTENTIAL_VOLT),
        "leak_ch1": CalculatedDataPoint("leak", LeakState.OFF, unit=None),
        "leakbatt1": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
        "leak_ch2": CalculatedDataPoint("leak", LeakState.ON, unit=None),
        "leakbatt2": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
        "leak_ch3": CalculatedDataPoint("leak", LeakState.OFF, unit=None),
        "leakbatt3": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
        "leak_ch4": CalculatedDataPoint("leak", LeakState.OFF, unit=None),
        "leakbatt4": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
        "leafwetness_ch1": CalculatedDataPoint("wetness", 14, unit=PERCENTAGE),
        "leaf_batt1": CalculatedDataPoint("batt", 1.78, unit=ELECTRIC_POTENTIAL_VOLT),
        "dewpoint": CalculatedDataPoint("dewpoint", 53.0, unit=TEMP_FAHRENHEIT),
        "feelslike": CalculatedDataPoint("feelslike", 74.5, unit=TEMP_FAHRENHEIT),
        "heatindex": CalculatedDataPoint("heatindex", 73.9, unit=TEMP_FAHRENHEIT),
        "windchill": CalculatedDataPoint("windchill", None, unit=TEMP_FAHRENHEIT),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception",
            value=ThermalPerception.VERY_COMFORTABLE,
            unit=None,
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint", value=47.1, unit="°F"
        ),
        "frostrisk": CalculatedDataPoint(
            data_point_key="frostrisk", value=FrostRisk.NO_RISK, unit=None
        ),
    }


@pytest.mark.parametrize(
    "device_data_filename,expected_output",
    [
        (
            "payload_gw1000bpro.json",
            {
                "runtime": CalculatedDataPoint("runtime", 319206.0, unit=TIME_SECONDS),
                "tempin": CalculatedDataPoint("temp", 79.5, unit=TEMP_FAHRENHEIT),
                "humidityin": CalculatedDataPoint("humidity", 31.0, unit=PERCENTAGE),
                "baromrel": CalculatedDataPoint("barom", 24.74, unit=PRESSURE_INHG),
                "baromabs": CalculatedDataPoint("barom", 24.74, unit=PRESSURE_INHG),
                "temp": CalculatedDataPoint("temp", 19.1, unit=TEMP_FAHRENHEIT),
                "humidity": CalculatedDataPoint("humidity", 34.0, unit=PERCENTAGE),
                "winddir": CalculatedDataPoint("winddir", 139.0, unit=DEGREE),
                "windspeed": CalculatedDataPoint(
                    "wind", 20.89, unit=SPEED_MILES_PER_HOUR
                ),
                "windgust": CalculatedDataPoint(
                    "gust", 1.12, unit=SPEED_MILES_PER_HOUR
                ),
                "maxdailygust": CalculatedDataPoint(
                    "gust", 8.05, unit=SPEED_MILES_PER_HOUR
                ),
                "solarradiation": CalculatedDataPoint(
                    "solarradiation", 264.61, unit=IRRADIATION_WATTS_PER_SQUARE_METER
                ),
                "solarradiation_lux": CalculatedDataPoint(
                    "solarradiation_lux", 33494.9, unit=LIGHT_LUX
                ),
                "solarradiation_perceived": CalculatedDataPoint(
                    "solarradiation_perceived", 90.0, unit=PERCENTAGE
                ),
                "uv": CalculatedDataPoint("uv", 2.0, unit=UV_INDEX),
                "safe_exposure_time_skin_type_1": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_1", 83.3, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_2": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_2", 100.0, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_3": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_3", 133.3, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_4": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_4", 166.7, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_5": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_5", 266.7, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_6": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_6", 433.3, unit=TIME_MINUTES
                ),
                "rainrate": CalculatedDataPoint(
                    "rainrate", 0.0, unit=f"{RAINFALL_INCHES}/hr"
                ),
                "eventrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
                "hourlyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
                "dailyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
                "weeklyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
                "monthlyrain": CalculatedDataPoint("rain", 2.177, unit=RAINFALL_INCHES),
                "yearlyrain": CalculatedDataPoint("rain", 4.441, unit=RAINFALL_INCHES),
                "lightning_num": CalculatedDataPoint("lightning_num", 13, unit=STRIKES),
                "lightning": CalculatedDataPoint("lightning", 0.6, unit=DISTANCE_MILES),
                "lightning_time": CalculatedDataPoint(
                    "lightning_time",
                    datetime(2022, 4, 20, 17, 17, 17, tzinfo=timezone.utc),
                ),
                "wh65batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "dewpoint": CalculatedDataPoint("dewpoint", -4.7, unit=TEMP_FAHRENHEIT),
                "feelslike": CalculatedDataPoint(
                    "feelslike", 2.7, unit=TEMP_FAHRENHEIT
                ),
                "heatindex": CalculatedDataPoint(
                    "heatindex", 12.3, unit=TEMP_FAHRENHEIT
                ),
                "windchill": CalculatedDataPoint(
                    "windchill", 2.7, unit=TEMP_FAHRENHEIT
                ),
                "humidityabs": CalculatedDataPoint(
                    data_point_key="humidityabs",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "humidityabsin": CalculatedDataPoint(
                    data_point_key="humidityabsin",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "thermalperception": CalculatedDataPoint(
                    data_point_key="thermalperception",
                    value=ThermalPerception.DRY,
                    unit=None,
                ),
                "frostpoint": CalculatedDataPoint(
                    data_point_key="frostpoint", value=-3.3, unit="°F"
                ),
                "frostrisk": CalculatedDataPoint(
                    data_point_key="frostrisk", value=FrostRisk.UNLIKELY, unit=None
                ),
            },
        ),
        (
            "payload_gw1000pro.json",
            {
                "tempin": CalculatedDataPoint("temp", 76.8, unit=TEMP_FAHRENHEIT),
                "humidityin": CalculatedDataPoint("humidity", 26, unit=PERCENTAGE),
                "baromrel": CalculatedDataPoint("barom", 24.604, unit=PRESSURE_INHG),
                "baromabs": CalculatedDataPoint("barom", 24.604, unit=PRESSURE_INHG),
                "temp": CalculatedDataPoint("temp", 56.7, unit=TEMP_FAHRENHEIT),
                "humidity": CalculatedDataPoint("humidity", 27, unit=PERCENTAGE),
                "winddir": CalculatedDataPoint("winddir", 46, unit=DEGREE),
                "windspeed": CalculatedDataPoint(
                    "wind", 0.89, unit=SPEED_MILES_PER_HOUR
                ),
                "windgust": CalculatedDataPoint(
                    "gust", 4.47, unit=SPEED_MILES_PER_HOUR
                ),
                "maxdailygust": CalculatedDataPoint(
                    "gust", 15.88, unit=SPEED_MILES_PER_HOUR
                ),
                "solarradiation": CalculatedDataPoint(
                    "solarradiation", 25.56, unit=IRRADIATION_WATTS_PER_SQUARE_METER
                ),
                "solarradiation_lux": CalculatedDataPoint(
                    "solarradiation_lux", 3235.4, unit=LIGHT_LUX
                ),
                "solarradiation_perceived": CalculatedDataPoint(
                    "solarradiation_perceived", 70.0, unit=PERCENTAGE
                ),
                "uv": CalculatedDataPoint("uv", 0, unit=UV_INDEX),
                "safe_exposure_time_skin_type_1": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_1", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_2": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_2", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_3": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_3", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_4": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_4", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_5": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_5", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_6": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_6", None, unit=TIME_MINUTES
                ),
                "rainrate": CalculatedDataPoint(
                    "rainrate", 0.000, unit=f"{RAINFALL_INCHES}/hr"
                ),
                "eventrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "hourlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "dailyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "weeklyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "monthlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "yearlyrain": CalculatedDataPoint("rain", 11.756, unit=RAINFALL_INCHES),
                "totalrain": CalculatedDataPoint("rain", 11.756, unit=RAINFALL_INCHES),
                "wh65batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "dewpoint": CalculatedDataPoint("dewpoint", 23.1, unit=TEMP_FAHRENHEIT),
                "feelslike": CalculatedDataPoint(
                    "feelslike", 56.7, unit=TEMP_FAHRENHEIT
                ),
                "heatindex": CalculatedDataPoint(
                    "heatindex", 53.3, unit=TEMP_FAHRENHEIT
                ),
                "windchill": CalculatedDataPoint(
                    "windchill", None, unit=TEMP_FAHRENHEIT
                ),
                "humidityabs": CalculatedDataPoint(
                    data_point_key="humidityabs",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "humidityabsin": CalculatedDataPoint(
                    data_point_key="humidityabsin",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "thermalperception": CalculatedDataPoint(
                    data_point_key="thermalperception",
                    value=ThermalPerception.DRY,
                    unit=None,
                ),
                "frostpoint": CalculatedDataPoint(
                    data_point_key="frostpoint", value=19.9, unit="°F"
                ),
                "frostrisk": CalculatedDataPoint(
                    data_point_key="frostrisk", value=FrostRisk.NO_RISK, unit=None
                ),
            },
        ),
        (
            "payload_gw1100b.json",
            {
                "tempin": CalculatedDataPoint("temp", 76.5, unit=TEMP_FAHRENHEIT),
                "humidityin": CalculatedDataPoint("humidity", 46, unit=PERCENTAGE),
                "baromrel": CalculatedDataPoint("barom", 29.244, unit=PRESSURE_INHG),
                "baromabs": CalculatedDataPoint("barom", 29.244, unit=PRESSURE_INHG),
                "temp": CalculatedDataPoint("temp", 91.4, unit=TEMP_FAHRENHEIT),
                "humidity": CalculatedDataPoint("humidity", 48, unit=PERCENTAGE),
                "rainrate": CalculatedDataPoint(
                    "rainrate", 0.000, unit=f"{RAINFALL_INCHES}/hr"
                ),
                "eventrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "hourlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "dailyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "weeklyrain": CalculatedDataPoint("rain", 0.004, unit=RAINFALL_INCHES),
                "monthlyrain": CalculatedDataPoint("rain", 1.402, unit=RAINFALL_INCHES),
                "yearlyrain": CalculatedDataPoint("rain", 48.504, unit=RAINFALL_INCHES),
                "totalrain": CalculatedDataPoint("rain", 48.504, unit=RAINFALL_INCHES),
                "temp1": CalculatedDataPoint("temp", 77.7, unit=TEMP_FAHRENHEIT),
                "humidity1": CalculatedDataPoint("humidity", 51, unit=PERCENTAGE),
                "soilmoisture1": CalculatedDataPoint("moisture", 40, unit=PERCENTAGE),
                "soilmoisture2": CalculatedDataPoint("moisture", 56, unit=PERCENTAGE),
                "wh40batt": CalculatedDataPoint(
                    "batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "wh26batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "batt1": CalculatedDataPoint("batt", BooleanBatteryState.ON),
                "soilbatt1": CalculatedDataPoint(
                    "batt", 1.5, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "soilbatt2": CalculatedDataPoint(
                    "batt", 1.8, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "tf_ch1": CalculatedDataPoint("tf", 84.7, unit=TEMP_FAHRENHEIT),
                "tf_batt1": CalculatedDataPoint(
                    "batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "tf_ch2": CalculatedDataPoint("tf", 82.9, unit=TEMP_FAHRENHEIT),
                "tf_batt2": CalculatedDataPoint(
                    "batt", 1.47, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "tf_ch3": CalculatedDataPoint("tf", 84.0, unit=TEMP_FAHRENHEIT),
                "tf_batt3": CalculatedDataPoint(
                    "batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "tf_ch4": CalculatedDataPoint("tf", 84.2, unit=TEMP_FAHRENHEIT),
                "tf_batt4": CalculatedDataPoint(
                    "batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "tf_ch5": CalculatedDataPoint("tf", 85.1, unit=TEMP_FAHRENHEIT),
                "tf_batt5": CalculatedDataPoint(
                    "batt", 1.2, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "tf_ch6": CalculatedDataPoint("tf", 84.2, unit=TEMP_FAHRENHEIT),
                "tf_batt6": CalculatedDataPoint(
                    "batt", 1.77, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "tf_ch7": CalculatedDataPoint("tf", 84.3, unit=TEMP_FAHRENHEIT),
                "tf_batt7": CalculatedDataPoint(
                    "batt", 1.6, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "tf_ch8": CalculatedDataPoint("tf", 84.2, unit=TEMP_FAHRENHEIT),
                "tf_batt8": CalculatedDataPoint(
                    "batt", 1.3, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "dewpoint": CalculatedDataPoint("dewpoint", 68.9, unit=TEMP_FAHRENHEIT),
                "heatindex": CalculatedDataPoint(
                    "heatindex", 96.3, unit=TEMP_FAHRENHEIT
                ),
                "humidityabs": CalculatedDataPoint(
                    data_point_key="humidityabs",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "humidityabsin": CalculatedDataPoint(
                    data_point_key="humidityabsin",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "thermalperception": CalculatedDataPoint(
                    data_point_key="thermalperception",
                    value=ThermalPerception.SOMEWHAT_UNCOMFORTABLE,
                    unit=None,
                ),
                "frostpoint": CalculatedDataPoint(
                    data_point_key="frostpoint", value=60.3, unit="°F"
                ),
                "frostrisk": CalculatedDataPoint(
                    data_point_key="frostrisk", value=FrostRisk.NO_RISK, unit=None
                ),
            },
        ),
        (
            "payload_gw2000a_1.json",
            {
                "runtime": CalculatedDataPoint("runtime", 3179, unit=TIME_SECONDS),
                "tempin": CalculatedDataPoint("temp", 71.2, unit=TEMP_FAHRENHEIT),
                "humidityin": CalculatedDataPoint("humidity", 49, unit=PERCENTAGE),
                "baromrel": CalculatedDataPoint("barom", 28.476, unit=PRESSURE_INHG),
                "baromabs": CalculatedDataPoint("barom", 28.476, unit=PRESSURE_INHG),
                "temp": CalculatedDataPoint("temp", 74.5, unit=TEMP_FAHRENHEIT),
                "humidity": CalculatedDataPoint("humidity", 47, unit=PERCENTAGE),
                "winddir": CalculatedDataPoint("winddir", 100, unit=DEGREE),
                "windspeed": CalculatedDataPoint(
                    "wind", 1.34, unit=SPEED_MILES_PER_HOUR
                ),
                "windgust": CalculatedDataPoint(
                    "gust", 2.24, unit=SPEED_MILES_PER_HOUR
                ),
                "maxdailygust": CalculatedDataPoint(
                    "gust", 2.24, unit=SPEED_MILES_PER_HOUR
                ),
                "solarradiation": CalculatedDataPoint(
                    "solarradiation", 0.0, unit=IRRADIATION_WATTS_PER_SQUARE_METER
                ),
                "solarradiation_lux": CalculatedDataPoint(
                    "solarradiation_lux", 0.0, unit=LIGHT_LUX
                ),
                "solarradiation_perceived": CalculatedDataPoint(
                    "solarradiation_perceived", 0.0, unit=PERCENTAGE
                ),
                "uv": CalculatedDataPoint("uv", 0, unit=UV_INDEX),
                "safe_exposure_time_skin_type_1": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_1", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_2": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_2", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_3": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_3", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_4": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_4", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_5": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_5", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_6": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_6", None, unit=TIME_MINUTES
                ),
                "rrain_piezo": CalculatedDataPoint(
                    "rrain", 0.000, unit=f"{RAINFALL_INCHES}/hr"
                ),
                "erain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "hrain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "drain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "wrain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "mrain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "yrain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "ws90cap_volt": CalculatedDataPoint(
                    "volt", 0.6, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "lightning_num": CalculatedDataPoint("lightning_num", 1, unit=STRIKES),
                "lightning": CalculatedDataPoint(
                    "lightning", 16.8, unit=DISTANCE_MILES
                ),
                "lightning_time": CalculatedDataPoint(
                    "lightning_time", None, unit=None
                ),
                "wh57batt": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
                "wh90batt": CalculatedDataPoint(
                    "batt", 3.16, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "leak_ch1": CalculatedDataPoint("leak", LeakState.OFF, unit=None),
                "leakbatt1": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
                "leak_ch2": CalculatedDataPoint("leak", LeakState.ON, unit=None),
                "leakbatt2": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
                "leak_ch3": CalculatedDataPoint("leak", LeakState.OFF, unit=None),
                "leakbatt3": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
                "leak_ch4": CalculatedDataPoint("leak", LeakState.OFF, unit=None),
                "leakbatt4": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
                "leafwetness_ch1": CalculatedDataPoint("wetness", 14, unit=PERCENTAGE),
                "leaf_batt1": CalculatedDataPoint(
                    "batt", 1.78, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "dewpoint": CalculatedDataPoint("dewpoint", 53.0, unit=TEMP_FAHRENHEIT),
                "feelslike": CalculatedDataPoint(
                    "feelslike", 74.5, unit=TEMP_FAHRENHEIT
                ),
                "heatindex": CalculatedDataPoint(
                    "heatindex", 73.9, unit=TEMP_FAHRENHEIT
                ),
                "windchill": CalculatedDataPoint(
                    "windchill", None, unit=TEMP_FAHRENHEIT
                ),
                "humidityabs": CalculatedDataPoint(
                    data_point_key="humidityabs",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "humidityabsin": CalculatedDataPoint(
                    data_point_key="humidityabsin",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "thermalperception": CalculatedDataPoint(
                    data_point_key="thermalperception",
                    value=ThermalPerception.VERY_COMFORTABLE,
                    unit=None,
                ),
                "frostpoint": CalculatedDataPoint(
                    data_point_key="frostpoint", value=47.1, unit="°F"
                ),
                "frostrisk": CalculatedDataPoint(
                    data_point_key="frostrisk", value=FrostRisk.NO_RISK, unit=None
                ),
            },
        ),
        (
            "payload_gw2000a_2.json",
            {
                "runtime": CalculatedDataPoint("runtime", 436796, unit=TIME_SECONDS),
                "tempin": CalculatedDataPoint("temp", 72.9, unit=TEMP_FAHRENHEIT),
                "humidityin": CalculatedDataPoint("humidity", 56, unit=PERCENTAGE),
                "baromrel": CalculatedDataPoint("barom", 29.870, unit=PRESSURE_INHG),
                "baromabs": CalculatedDataPoint("barom", 29.509, unit=PRESSURE_INHG),
                "temp": CalculatedDataPoint("temp", 59.7, unit=TEMP_FAHRENHEIT),
                "humidity": CalculatedDataPoint("humidity", 65, unit=PERCENTAGE),
                "winddir": CalculatedDataPoint("winddir", 327, unit=DEGREE),
                "windspeed": CalculatedDataPoint(
                    "wind", 2.24, unit=SPEED_MILES_PER_HOUR
                ),
                "windgust": CalculatedDataPoint(
                    "gust", 3.80, unit=SPEED_MILES_PER_HOUR
                ),
                "maxdailygust": CalculatedDataPoint(
                    "gust", 17.45, unit=SPEED_MILES_PER_HOUR
                ),
                "solarradiation": CalculatedDataPoint(
                    "solarradiation", 0.00, unit=IRRADIATION_WATTS_PER_SQUARE_METER
                ),
                "solarradiation_lux": CalculatedDataPoint(
                    "solarradiation_lux", 0.0, unit=LIGHT_LUX
                ),
                "solarradiation_perceived": CalculatedDataPoint(
                    "solarradiation_perceived", 0.0, unit=PERCENTAGE
                ),
                "uv": CalculatedDataPoint("uv", 0, unit=UV_INDEX),
                "safe_exposure_time_skin_type_1": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_1", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_2": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_2", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_3": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_3", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_4": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_4", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_5": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_5", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_6": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_6", None, unit=TIME_MINUTES
                ),
                "rainrate": CalculatedDataPoint(
                    "rainrate", 0.000, unit=f"{RAINFALL_INCHES}/hr"
                ),
                "eventrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "hourlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "dailyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "weeklyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "monthlyrain": CalculatedDataPoint("rain", 0.736, unit=RAINFALL_INCHES),
                "yearlyrain": CalculatedDataPoint("rain", 3.909, unit=RAINFALL_INCHES),
                "rrain_piezo": CalculatedDataPoint(
                    "rrain", 0.000, unit=f"{RAINFALL_INCHES}/hr"
                ),
                "erain_piezo": CalculatedDataPoint("rain", 0.063, unit=RAINFALL_INCHES),
                "hrain_piezo": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "drain_piezo": CalculatedDataPoint("rain", 0.075, unit=RAINFALL_INCHES),
                "wrain_piezo": CalculatedDataPoint("rain", 0.075, unit=RAINFALL_INCHES),
                "mrain_piezo": CalculatedDataPoint("rain", 0.941, unit=RAINFALL_INCHES),
                "yrain_piezo": CalculatedDataPoint("rain", 4.114, unit=RAINFALL_INCHES),
                "ws90cap_volt": CalculatedDataPoint(
                    "volt", 5.2, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "temp1": CalculatedDataPoint("temp", 71.2, unit=TEMP_FAHRENHEIT),
                "humidity1": CalculatedDataPoint("humidity", 61, unit=PERCENTAGE),
                "temp2": CalculatedDataPoint("temp", 71.2, unit=TEMP_FAHRENHEIT),
                "humidity2": CalculatedDataPoint("humidity", 58, unit=PERCENTAGE),
                "temp3": CalculatedDataPoint("temp", 70.5, unit=TEMP_FAHRENHEIT),
                "humidity3": CalculatedDataPoint("humidity", 61, unit=PERCENTAGE),
                "temp4": CalculatedDataPoint("temp", 73.0, unit=TEMP_FAHRENHEIT),
                "humidity4": CalculatedDataPoint("humidity", 58, unit=PERCENTAGE),
                "temp5": CalculatedDataPoint("temp", 70.7, unit=TEMP_FAHRENHEIT),
                "humidity5": CalculatedDataPoint("humidity", 69, unit=PERCENTAGE),
                "temp6": CalculatedDataPoint("temp", 72.7, unit=TEMP_FAHRENHEIT),
                "humidity6": CalculatedDataPoint("humidity", 58, unit=PERCENTAGE),
                "temp7": CalculatedDataPoint("temp", 67.1, unit=TEMP_FAHRENHEIT),
                "humidity7": CalculatedDataPoint("humidity", 54, unit=PERCENTAGE),
                "temp8": CalculatedDataPoint("temp", 68.0, unit=TEMP_FAHRENHEIT),
                "humidity8": CalculatedDataPoint("humidity", 56, unit=PERCENTAGE),
                "soilmoisture1": CalculatedDataPoint("moisture", 53, unit=PERCENTAGE),
                "soilmoisture2": CalculatedDataPoint("moisture", 57, unit=PERCENTAGE),
                "soilmoisture3": CalculatedDataPoint("moisture", 59, unit=PERCENTAGE),
                "soilmoisture4": CalculatedDataPoint("moisture", 49, unit=PERCENTAGE),
                "soilmoisture5": CalculatedDataPoint("moisture", 52, unit=PERCENTAGE),
                "pm25_ch1": CalculatedDataPoint(
                    "pm25", 21.0, unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
                ),
                "pm25_avg_24h_ch1": CalculatedDataPoint(
                    "pm25", 16.3, unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
                ),
                "tf_co2": CalculatedDataPoint("tf_co2", 62.2, unit=TEMP_FAHRENHEIT),
                "humi_co2": CalculatedDataPoint("humi_co2", 61, unit=PERCENTAGE),
                "pm25_co2": CalculatedDataPoint(
                    "pm25", 4.9, unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
                ),
                "pm25_24h_co2": CalculatedDataPoint(
                    "pm25", 7.5, unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
                ),
                "pm10_co2": CalculatedDataPoint(
                    "pm10", 6.1, unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
                ),
                "pm10_24h_co2": CalculatedDataPoint(
                    "pm10", 7.8, unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
                ),
                "co2": CalculatedDataPoint(
                    "co2", 455, unit=CONCENTRATION_PARTS_PER_MILLION
                ),
                "co2_24h": CalculatedDataPoint(
                    "co2_24h", 473, unit=CONCENTRATION_PARTS_PER_MILLION
                ),
                "lightning_num": CalculatedDataPoint("lightning_num", 13, unit=STRIKES),
                "lightning": CalculatedDataPoint("lightning", 0.6, unit=DISTANCE_MILES),
                "lightning_time": CalculatedDataPoint(
                    "lightning_time",
                    datetime(2022, 4, 20, 17, 17, 17, tzinfo=timezone.utc),
                ),
                "wh80batt": CalculatedDataPoint(
                    "batt", 3.28, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "batt1": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "batt2": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "batt3": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "batt4": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "batt5": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "batt6": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "batt7": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "batt8": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "soilbatt1": CalculatedDataPoint(
                    "batt", 1.4, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "soilbatt2": CalculatedDataPoint(
                    "batt", 1.3, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "soilbatt3": CalculatedDataPoint(
                    "batt", 1.3, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "soilbatt4": CalculatedDataPoint(
                    "batt", 1.3, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "soilbatt5": CalculatedDataPoint(
                    "batt", 1.3, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "pm25batt1": CalculatedDataPoint("batt", 60, unit=PERCENTAGE),
                "wh57batt": CalculatedDataPoint("batt", 60, unit=PERCENTAGE),
                "co2_batt": CalculatedDataPoint("batt", 120, unit=PERCENTAGE),
                "wh90batt": CalculatedDataPoint(
                    "batt", 3.22, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "dewpoint": CalculatedDataPoint("dewpoint", 47.9, unit=TEMP_FAHRENHEIT),
                "feelslike": CalculatedDataPoint(
                    "feelslike", 59.7, unit=TEMP_FAHRENHEIT
                ),
                "heatindex": CalculatedDataPoint(
                    "heatindex", 58.4, unit=TEMP_FAHRENHEIT
                ),
                "windchill": CalculatedDataPoint(
                    "windchill", None, unit=TEMP_FAHRENHEIT
                ),
                "humidityabs": CalculatedDataPoint(
                    data_point_key="humidityabs",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "humidityabsin": CalculatedDataPoint(
                    data_point_key="humidityabsin",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "thermalperception": CalculatedDataPoint(
                    data_point_key="thermalperception",
                    value=ThermalPerception.DRY,
                    unit=None,
                ),
                "frostpoint": CalculatedDataPoint(
                    data_point_key="frostpoint", value=44.3, unit="°F"
                ),
                "frostrisk": CalculatedDataPoint(
                    data_point_key="frostrisk", value=FrostRisk.NO_RISK, unit=None
                ),
            },
        ),
        (
            "payload_pthp2550pro.json",
            {
                "tempin": CalculatedDataPoint("temp", 64.4, unit=TEMP_FAHRENHEIT),
                "humidityin": CalculatedDataPoint("humidity", 72, unit=PERCENTAGE),
                "baromrel": CalculatedDataPoint("barom", 28.196, unit=PRESSURE_INHG),
                "baromabs": CalculatedDataPoint("barom", 28.196, unit=PRESSURE_INHG),
                "temp": CalculatedDataPoint("temp", 35.2, unit=TEMP_FAHRENHEIT),
                "humidity": CalculatedDataPoint("humidity", 60, unit=PERCENTAGE),
                "winddir": CalculatedDataPoint("winddir", 289, unit=DEGREE),
                "winddir_avg10m": CalculatedDataPoint("winddir", 282, unit=DEGREE),
                "windspeed": CalculatedDataPoint(
                    "wind", 2.7, unit=SPEED_MILES_PER_HOUR
                ),
                "windspdmph_avg10m": CalculatedDataPoint(
                    "wind", 2.5, unit=SPEED_MILES_PER_HOUR
                ),
                "windgust": CalculatedDataPoint("gust", 6.9, unit=SPEED_MILES_PER_HOUR),
                "maxdailygust": CalculatedDataPoint(
                    "gust", 20.6, unit=SPEED_MILES_PER_HOUR
                ),
                "rainrate": CalculatedDataPoint(
                    "rainrate", 0.000, unit=f"{RAINFALL_INCHES}/hr"
                ),
                "eventrain": CalculatedDataPoint("rain", 0.134, unit=RAINFALL_INCHES),
                "hourlyrain": CalculatedDataPoint("rain", 0.012, unit=RAINFALL_INCHES),
                "dailyrain": CalculatedDataPoint("rain", 0.134, unit=RAINFALL_INCHES),
                "weeklyrain": CalculatedDataPoint("rain", 0.134, unit=RAINFALL_INCHES),
                "monthlyrain": CalculatedDataPoint("rain", 1.110, unit=RAINFALL_INCHES),
                "yearlyrain": CalculatedDataPoint("rain", 11.610, unit=RAINFALL_INCHES),
                "solarradiation": CalculatedDataPoint(
                    "solarradiation", 174.81, unit=IRRADIATION_WATTS_PER_SQUARE_METER
                ),
                "solarradiation_lux": CalculatedDataPoint(
                    "solarradiation_lux", 22127.8, unit=LIGHT_LUX
                ),
                "solarradiation_perceived": CalculatedDataPoint(
                    "solarradiation_perceived", 87.0, unit=PERCENTAGE
                ),
                "uv": CalculatedDataPoint("uv", 1, unit=UV_INDEX),
                "safe_exposure_time_skin_type_1": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_1", 166.7, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_2": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_2", 200.0, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_3": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_3", 266.7, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_4": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_4", 333.3, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_5": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_5", 533.3, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_6": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_6", 866.7, unit=TIME_MINUTES
                ),
                "temp1": CalculatedDataPoint("temp", 66.4, unit=TEMP_FAHRENHEIT),
                "humidity1": CalculatedDataPoint("humidity", 69, unit=PERCENTAGE),
                "soilmoisture1": CalculatedDataPoint("moisture", 22, unit=PERCENTAGE),
                "pm25_ch1": CalculatedDataPoint(
                    "pm25", 7.0, unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
                ),
                "pm25_avg_24h_ch1": CalculatedDataPoint(
                    "pm25", 14.3, unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
                ),
                "wh65batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "wh25batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "batt1": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "soilbatt1": CalculatedDataPoint(
                    "batt", 1.5, unit=ELECTRIC_POTENTIAL_VOLT
                ),
                "pm25batt1": CalculatedDataPoint("batt", 100, unit=PERCENTAGE),
                "dewpoint": CalculatedDataPoint("dewpoint", 22.7, unit=TEMP_FAHRENHEIT),
                "feelslike": CalculatedDataPoint(
                    "feelslike", 35.2, unit=TEMP_FAHRENHEIT
                ),
                "heatindex": CalculatedDataPoint(
                    "heatindex", 31.2, unit=TEMP_FAHRENHEIT
                ),
                "windchill": CalculatedDataPoint(
                    "windchill", None, unit=TEMP_FAHRENHEIT
                ),
                "humidityabs": CalculatedDataPoint(
                    data_point_key="humidityabs",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "humidityabsin": CalculatedDataPoint(
                    data_point_key="humidityabsin",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "thermalperception": CalculatedDataPoint(
                    data_point_key="thermalperception",
                    value=ThermalPerception.DRY,
                    unit=None,
                ),
                "frostpoint": CalculatedDataPoint(
                    data_point_key="frostpoint", value=22.4, unit="°F"
                ),
                "frostrisk": CalculatedDataPoint(
                    data_point_key="frostrisk", value=FrostRisk.PROBABLE, unit=None
                ),
            },
        ),
        (
            "payload_wh2650a.json",
            {
                "runtime": CalculatedDataPoint("runtime", 49030, unit=TIME_SECONDS),
                "tempin": CalculatedDataPoint("temp", 71.2, unit=TEMP_FAHRENHEIT),
                "humidityin": CalculatedDataPoint("humidity", 60, unit=PERCENTAGE),
                "baromrel": CalculatedDataPoint("barom", 32.211, unit=PRESSURE_INHG),
                "baromabs": CalculatedDataPoint("barom", 29.648, unit=PRESSURE_INHG),
                "temp": CalculatedDataPoint("temp", 76.3, unit=TEMP_FAHRENHEIT),
                "humidity": CalculatedDataPoint("humidity", 54, unit=PERCENTAGE),
                "winddir": CalculatedDataPoint("winddir", 217, unit=DEGREE),
                "windspeed": CalculatedDataPoint(
                    "wind", 1.12, unit=SPEED_MILES_PER_HOUR
                ),
                "windgust": CalculatedDataPoint(
                    "gust", 2.24, unit=SPEED_MILES_PER_HOUR
                ),
                "maxdailygust": CalculatedDataPoint(
                    "gust", 10.07, unit=SPEED_MILES_PER_HOUR
                ),
                "solarradiation": CalculatedDataPoint(
                    "solarradiation", 642.38, unit=IRRADIATION_WATTS_PER_SQUARE_METER
                ),
                "solarradiation_lux": CalculatedDataPoint(
                    "solarradiation_lux", 81313.9, unit=LIGHT_LUX
                ),
                "solarradiation_perceived": CalculatedDataPoint(
                    "solarradiation_perceived", 98.0, unit=PERCENTAGE
                ),
                "uv": CalculatedDataPoint("uv", 6, unit=UV_INDEX),
                "safe_exposure_time_skin_type_1": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_1", 27.8, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_2": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_2", 33.3, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_3": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_3", 44.4, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_4": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_4", 55.6, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_5": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_5", 88.9, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_6": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_6", 144.4, unit=TIME_MINUTES
                ),
                "rainrate": CalculatedDataPoint(
                    "rainrate", 0.000, unit=f"{RAINFALL_INCHES}/hr"
                ),
                "eventrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "hourlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "dailyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "weeklyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "monthlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "yearlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "totalain": CalculatedDataPoint(
                    "totalain", 0.000, unit=RAINFALL_INCHES
                ),
                "wh65batt": CalculatedDataPoint(
                    "batt", BooleanBatteryState.OFF, unit=None
                ),
                "wh25batt": CalculatedDataPoint(
                    "batt", BooleanBatteryState.ON, unit=None
                ),
                "dewpoint": CalculatedDataPoint("dewpoint", 58.4, unit=TEMP_FAHRENHEIT),
                "feelslike": CalculatedDataPoint(
                    "feelslike", 76.3, unit=TEMP_FAHRENHEIT
                ),
                "heatindex": CalculatedDataPoint(
                    "heatindex", 76.1, unit=TEMP_FAHRENHEIT
                ),
                "windchill": CalculatedDataPoint(
                    "windchill", None, unit=TEMP_FAHRENHEIT
                ),
                "humidityabs": CalculatedDataPoint(
                    data_point_key="humidityabs",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "humidityabsin": CalculatedDataPoint(
                    data_point_key="humidityabsin",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "thermalperception": CalculatedDataPoint(
                    data_point_key="thermalperception",
                    value=ThermalPerception.COMFORTABLE,
                    unit=None,
                ),
                "frostpoint": CalculatedDataPoint(
                    data_point_key="frostpoint", value=52.3, unit="°F"
                ),
                "frostrisk": CalculatedDataPoint(
                    data_point_key="frostrisk", value=FrostRisk.NO_RISK, unit=None
                ),
            },
        ),
        (
            "payload_ws2900.json",
            {
                "tempin": CalculatedDataPoint("temp", 72.9, unit=TEMP_FAHRENHEIT),
                "humidityin": CalculatedDataPoint("humidity", 62, unit=PERCENTAGE),
                "baromrel": CalculatedDataPoint("barom", 29.829, unit=PRESSURE_INHG),
                "baromabs": CalculatedDataPoint("barom", 28.122, unit=PRESSURE_INHG),
                "temp": CalculatedDataPoint("temp", 22.0, unit=TEMP_FAHRENHEIT),
                "humidity": CalculatedDataPoint("humidity", 100, unit=PERCENTAGE),
                "winddir": CalculatedDataPoint("winddir", 271, unit=DEGREE),
                "windspeed": CalculatedDataPoint(
                    "wind", 6.9, unit=SPEED_MILES_PER_HOUR
                ),
                "windgust": CalculatedDataPoint("gust", 9.2, unit=SPEED_MILES_PER_HOUR),
                "maxdailygust": CalculatedDataPoint(
                    "gust", 9.2, unit=SPEED_MILES_PER_HOUR
                ),
                "rainrate": CalculatedDataPoint(
                    "rainrate", 0.000, unit=f"{RAINFALL_INCHES}/hr"
                ),
                "eventrain": CalculatedDataPoint("rain", 1.331, unit=RAINFALL_INCHES),
                "hourlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "dailyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
                "weeklyrain": CalculatedDataPoint("rain", 1.331, unit=RAINFALL_INCHES),
                "monthlyrain": CalculatedDataPoint("rain", 4.929, unit=RAINFALL_INCHES),
                "totalrain": CalculatedDataPoint("rain", 14.890, unit=RAINFALL_INCHES),
                "solarradiation": CalculatedDataPoint(
                    "solarradiation", 0.00, unit=IRRADIATION_WATTS_PER_SQUARE_METER
                ),
                "solarradiation_lux": CalculatedDataPoint(
                    "solarradiation_lux", 0.0, unit=LIGHT_LUX
                ),
                "solarradiation_perceived": CalculatedDataPoint(
                    "solarradiation_perceived", 0.0, unit=PERCENTAGE
                ),
                "uv": CalculatedDataPoint("uv", 0, unit=UV_INDEX),
                "safe_exposure_time_skin_type_1": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_1", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_2": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_2", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_3": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_3", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_4": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_4", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_5": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_5", None, unit=TIME_MINUTES
                ),
                "safe_exposure_time_skin_type_6": CalculatedDataPoint(
                    "safe_exposure_time_skin_type_6", None, unit=TIME_MINUTES
                ),
                "wh65batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
                "dewpoint": CalculatedDataPoint("dewpoint", 22.0, unit=TEMP_FAHRENHEIT),
                "feelslike": CalculatedDataPoint(
                    "feelslike", 13.5, unit=TEMP_FAHRENHEIT
                ),
                "heatindex": CalculatedDataPoint(
                    "heatindex", 18.6, unit=TEMP_FAHRENHEIT
                ),
                "windchill": CalculatedDataPoint(
                    "windchill", 13.5, unit=TEMP_FAHRENHEIT
                ),
                "humidityabs": CalculatedDataPoint(
                    data_point_key="humidityabs",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "humidityabsin": CalculatedDataPoint(
                    data_point_key="humidityabsin",
                    value=0.0,
                    unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
                ),
                "thermalperception": CalculatedDataPoint(
                    data_point_key="thermalperception",
                    value=ThermalPerception.DRY,
                    unit=None,
                ),
                "frostpoint": CalculatedDataPoint(
                    data_point_key="frostpoint", value=23.1, unit="°F"
                ),
                "frostrisk": CalculatedDataPoint(
                    data_point_key="frostrisk", value=FrostRisk.VERY_PROBABLE, unit=None
                ),
            },
        ),
    ],
)
def test_process(device_data, ecowitt, expected_output, request):
    """Test processing a raw data payload."""
    processed_data = ProcessedData(ecowitt, device_data)
    assert processed_data.output == expected_output


@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_DEFAULT_BATTERY_STRATEGY: BatteryStrategy.BOOLEAN,
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: False,
            CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
            CONF_HASS_ENTITY_ID_PREFIX: TEST_HASS_ENTITY_ID_PREFIX,
            CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_METRIC,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
            CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_PORT: TEST_PORT,
            CONF_RAW_DATA: False,
            CONF_VERBOSE: False,
        }
    ],
)
@pytest.mark.parametrize("device_data_filename", ["payload_gw1000bpro_metric.json"])
def test_unit_conversion_to_imperial(device_data, ecowitt):
    """Test conversion between units."""
    processed_data = ProcessedData(ecowitt, device_data)
    assert processed_data.output == {
        "runtime": CalculatedDataPoint("runtime", 319206, unit=TIME_SECONDS),
        "tempin": CalculatedDataPoint("temp", 79.5, unit=TEMP_FAHRENHEIT),
        "humidityin": CalculatedDataPoint("humidity", 31, unit=PERCENTAGE),
        "baromrel": CalculatedDataPoint("barom", 24.74, unit=PRESSURE_INHG),
        "baromabs": CalculatedDataPoint("barom", 24.74, unit=PRESSURE_INHG),
        "temp": CalculatedDataPoint("temp", 24.1, unit=TEMP_FAHRENHEIT),
        "humidity": CalculatedDataPoint("humidity", 74, unit=PERCENTAGE),
        "winddir": CalculatedDataPoint("winddir", 139, unit=DEGREE),
        "windspeed": CalculatedDataPoint("wind", 20.1, unit=SPEED_MILES_PER_HOUR),
        "windgust": CalculatedDataPoint("gust", 1.1, unit=SPEED_MILES_PER_HOUR),
        "maxdailygust": CalculatedDataPoint("gust", 8.1, unit=SPEED_MILES_PER_HOUR),
        "solarradiation": CalculatedDataPoint(
            "solarradiation", 264.61, unit=IRRADIATION_WATTS_PER_SQUARE_METER
        ),
        "solarradiation_lux": CalculatedDataPoint(
            "solarradiation_lux", 33494.9, unit=LIGHT_LUX
        ),
        "solarradiation_perceived": CalculatedDataPoint(
            "solarradiation_perceived", 90.0, unit=PERCENTAGE
        ),
        "uv": CalculatedDataPoint("uv", 2.0, unit=UV_INDEX),
        "safe_exposure_time_skin_type_1": CalculatedDataPoint(
            "safe_exposure_time_skin_type_1", 83.3, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_2": CalculatedDataPoint(
            "safe_exposure_time_skin_type_2", 100.0, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_3": CalculatedDataPoint(
            "safe_exposure_time_skin_type_3", 133.3, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_4": CalculatedDataPoint(
            "safe_exposure_time_skin_type_4", 166.7, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_5": CalculatedDataPoint(
            "safe_exposure_time_skin_type_5", 266.7, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_6": CalculatedDataPoint(
            "safe_exposure_time_skin_type_6", 433.3, unit=TIME_MINUTES
        ),
        "rainrate": CalculatedDataPoint(
            "rainrate", 0.000, unit=f"{RAINFALL_INCHES}/hr"
        ),
        "eventrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "hourlyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "dailyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "weeklyrain": CalculatedDataPoint("rain", 0.000, unit=RAINFALL_INCHES),
        "monthlyrain": CalculatedDataPoint("rain", 2.2, unit=RAINFALL_INCHES),
        "yearlyrain": CalculatedDataPoint("rain", 4.4, unit=RAINFALL_INCHES),
        "lightning_num": CalculatedDataPoint("lightning_num", 13, unit=STRIKES),
        "lightning": CalculatedDataPoint("lightning", 0.6, unit=DISTANCE_MILES),
        "lightning_time": CalculatedDataPoint(
            "lightning_time", datetime(2022, 4, 20, 17, 17, 17, tzinfo=timezone.utc)
        ),
        "wh65batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
        "dewpoint": CalculatedDataPoint("dewpoint", 17.0, unit=TEMP_FAHRENHEIT),
        "feelslike": CalculatedDataPoint("feelslike", 6.3, unit=TEMP_FAHRENHEIT),
        "heatindex": CalculatedDataPoint("heatindex", 19.7, unit=TEMP_FAHRENHEIT),
        "windchill": CalculatedDataPoint("windchill", 6.3, unit=TEMP_FAHRENHEIT),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception", value=ThermalPerception.DRY, unit=None
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint", value=17.9, unit="°F"
        ),
        "frostrisk": CalculatedDataPoint(
            data_point_key="frostrisk", value=FrostRisk.UNLIKELY, unit=None
        ),
    }


@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_DEFAULT_BATTERY_STRATEGY: BatteryStrategy.BOOLEAN,
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: False,
            CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
            CONF_HASS_ENTITY_ID_PREFIX: TEST_HASS_ENTITY_ID_PREFIX,
            CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
            CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_METRIC,
            CONF_PORT: TEST_PORT,
            CONF_RAW_DATA: False,
            CONF_VERBOSE: False,
        }
    ],
)
def test_unit_conversion_to_metric(device_data, ecowitt):
    """Test conversion between units."""
    processed_data = ProcessedData(ecowitt, device_data)
    assert processed_data.output == {
        "runtime": CalculatedDataPoint("runtime", 319206, unit=TIME_SECONDS),
        "tempin": CalculatedDataPoint("temp", 26.4, unit=TEMP_CELSIUS),
        "humidityin": CalculatedDataPoint("humidity", 31, unit=PERCENTAGE),
        "baromrel": CalculatedDataPoint("barom", 837.793, unit=PRESSURE_HPA),
        "baromabs": CalculatedDataPoint("barom", 837.793, unit=PRESSURE_HPA),
        "temp": CalculatedDataPoint("temp", -7.2, unit=TEMP_CELSIUS),
        "humidity": CalculatedDataPoint("humidity", 34, unit=PERCENTAGE),
        "winddir": CalculatedDataPoint("winddir", 139, unit=DEGREE),
        "windspeed": CalculatedDataPoint("wind", 33.6, unit=SPEED_KILOMETERS_PER_HOUR),
        "windgust": CalculatedDataPoint("gust", 1.8, unit=SPEED_KILOMETERS_PER_HOUR),
        "maxdailygust": CalculatedDataPoint(
            "gust", 13.0, unit=SPEED_KILOMETERS_PER_HOUR
        ),
        "solarradiation": CalculatedDataPoint(
            "solarradiation", 264.61, unit=IRRADIATION_WATTS_PER_SQUARE_METER
        ),
        "solarradiation_lux": CalculatedDataPoint(
            "solarradiation_lux", 33494.9, unit=LIGHT_LUX
        ),
        "solarradiation_perceived": CalculatedDataPoint(
            "solarradiation_perceived", 90.0, unit=PERCENTAGE
        ),
        "uv": CalculatedDataPoint("uv", 2.0, unit=UV_INDEX),
        "safe_exposure_time_skin_type_1": CalculatedDataPoint(
            "safe_exposure_time_skin_type_1", 83.3, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_2": CalculatedDataPoint(
            "safe_exposure_time_skin_type_2", 100.0, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_3": CalculatedDataPoint(
            "safe_exposure_time_skin_type_3", 133.3, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_4": CalculatedDataPoint(
            "safe_exposure_time_skin_type_4", 166.7, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_5": CalculatedDataPoint(
            "safe_exposure_time_skin_type_5", 266.7, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_6": CalculatedDataPoint(
            "safe_exposure_time_skin_type_6", 433.3, unit=TIME_MINUTES
        ),
        "rainrate": CalculatedDataPoint(
            "rainrate", 0.0, unit=f"{RAINFALL_MILLIMETERS}/hr"
        ),
        "eventrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_MILLIMETERS),
        "hourlyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_MILLIMETERS),
        "dailyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_MILLIMETERS),
        "weeklyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_MILLIMETERS),
        "monthlyrain": CalculatedDataPoint("rain", 55.3, unit=RAINFALL_MILLIMETERS),
        "yearlyrain": CalculatedDataPoint("rain", 112.8, unit=RAINFALL_MILLIMETERS),
        "lightning_num": CalculatedDataPoint("lightning_num", 13, unit=STRIKES),
        "lightning": CalculatedDataPoint("lightning", 1.0, unit=DISTANCE_KILOMETERS),
        "lightning_time": CalculatedDataPoint(
            "lightning_time", datetime(2022, 4, 20, 17, 17, 17, tzinfo=timezone.utc)
        ),
        "wh65batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
        "dewpoint": CalculatedDataPoint("dewpoint", -20.4, unit=TEMP_CELSIUS),
        "feelslike": CalculatedDataPoint("feelslike", -16.3, unit=TEMP_CELSIUS),
        "heatindex": CalculatedDataPoint("heatindex", -11.0, unit=TEMP_CELSIUS),
        "windchill": CalculatedDataPoint("windchill", -16.3, unit=TEMP_CELSIUS),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=1.0,
            unit=WATER_VAPOR_GRAMS_PER_CUBIC_METER,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=8.5,
            unit=WATER_VAPOR_GRAMS_PER_CUBIC_METER,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception", value=ThermalPerception.DRY, unit=None
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint", value=-19.6, unit="°C"
        ),
        "frostrisk": CalculatedDataPoint(
            data_point_key="frostrisk", value=FrostRisk.UNLIKELY, unit=None
        ),
    }


def test_nonnumeric_value(device_data, ecowitt):
    """Test a value that can't be parsed as a number."""
    device_data["Random New Key"] = "Some Value"
    processed_data = ProcessedData(ecowitt, device_data)
    assert processed_data.output == {
        "runtime": CalculatedDataPoint("runtime", 319206.0, unit=TIME_SECONDS),
        "tempin": CalculatedDataPoint("temp", 79.5, unit=TEMP_FAHRENHEIT),
        "humidityin": CalculatedDataPoint("humidity", 31.0, unit=PERCENTAGE),
        "baromrel": CalculatedDataPoint("barom", 24.74, unit=PRESSURE_INHG),
        "baromabs": CalculatedDataPoint("barom", 24.74, unit=PRESSURE_INHG),
        "temp": CalculatedDataPoint("temp", 19.1, unit=TEMP_FAHRENHEIT),
        "humidity": CalculatedDataPoint("humidity", 34.0, unit=PERCENTAGE),
        "winddir": CalculatedDataPoint("winddir", 139.0, unit=DEGREE),
        "windspeed": CalculatedDataPoint("wind", 20.89, unit=SPEED_MILES_PER_HOUR),
        "windgust": CalculatedDataPoint("gust", 1.12, unit=SPEED_MILES_PER_HOUR),
        "maxdailygust": CalculatedDataPoint("gust", 8.05, unit=SPEED_MILES_PER_HOUR),
        "solarradiation": CalculatedDataPoint(
            "solarradiation", 264.61, unit=IRRADIATION_WATTS_PER_SQUARE_METER
        ),
        "solarradiation_lux": CalculatedDataPoint(
            "solarradiation_lux", 33494.9, unit=LIGHT_LUX
        ),
        "solarradiation_perceived": CalculatedDataPoint(
            "solarradiation_perceived", 90.0, unit=PERCENTAGE
        ),
        "uv": CalculatedDataPoint("uv", 2.0, unit=UV_INDEX),
        "safe_exposure_time_skin_type_1": CalculatedDataPoint(
            "safe_exposure_time_skin_type_1", 83.3, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_2": CalculatedDataPoint(
            "safe_exposure_time_skin_type_2", 100.0, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_3": CalculatedDataPoint(
            "safe_exposure_time_skin_type_3", 133.3, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_4": CalculatedDataPoint(
            "safe_exposure_time_skin_type_4", 166.7, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_5": CalculatedDataPoint(
            "safe_exposure_time_skin_type_5", 266.7, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_6": CalculatedDataPoint(
            "safe_exposure_time_skin_type_6", 433.3, unit=TIME_MINUTES
        ),
        "rainrate": CalculatedDataPoint("rainrate", 0.0, unit=f"{RAINFALL_INCHES}/hr"),
        "eventrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
        "hourlyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
        "dailyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
        "weeklyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
        "monthlyrain": CalculatedDataPoint("rain", 2.177, unit=RAINFALL_INCHES),
        "yearlyrain": CalculatedDataPoint("rain", 4.441, unit=RAINFALL_INCHES),
        "lightning_num": CalculatedDataPoint("lightning_num", 13, unit=STRIKES),
        "lightning": CalculatedDataPoint("lightning", 0.6, unit=DISTANCE_MILES),
        "lightning_time": CalculatedDataPoint(
            "lightning_time", datetime(2022, 4, 20, 17, 17, 17, tzinfo=timezone.utc)
        ),
        "wh65batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
        "dewpoint": CalculatedDataPoint("dewpoint", -4.7, unit=TEMP_FAHRENHEIT),
        "feelslike": CalculatedDataPoint("feelslike", 2.7, unit=TEMP_FAHRENHEIT),
        "heatindex": CalculatedDataPoint("heatindex", 12.3, unit=TEMP_FAHRENHEIT),
        "windchill": CalculatedDataPoint("windchill", 2.7, unit=TEMP_FAHRENHEIT),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception", value=ThermalPerception.DRY, unit=None
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint", value=-3.3, unit="°F"
        ),
        "frostrisk": CalculatedDataPoint(
            data_point_key="frostrisk", value=FrostRisk.UNLIKELY, unit=None
        ),
        "Random New Key": CalculatedDataPoint("Random New Key", "Some Value"),
    }


@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_DEFAULT_BATTERY_STRATEGY: BatteryStrategy.BOOLEAN,
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: False,
            CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
            CONF_HASS_ENTITY_ID_PREFIX: TEST_HASS_ENTITY_ID_PREFIX,
            CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
            CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_PORT: TEST_PORT,
            CONF_RAW_DATA: False,
            CONF_VERBOSE: False,
        }
    ],
)
def test_unknown_battery(device_data, ecowitt):
    """Test that an unknown battery is given the default strategy."""
    device_data["playstationbattery1"] = 0
    processed_data = ProcessedData(ecowitt, device_data)
    assert processed_data.output == {
        "runtime": CalculatedDataPoint("runtime", 319206.0, unit=TIME_SECONDS),
        "tempin": CalculatedDataPoint("temp", 79.5, unit=TEMP_FAHRENHEIT),
        "humidityin": CalculatedDataPoint("humidity", 31.0, unit=PERCENTAGE),
        "baromrel": CalculatedDataPoint("barom", 24.74, unit=PRESSURE_INHG),
        "baromabs": CalculatedDataPoint("barom", 24.74, unit=PRESSURE_INHG),
        "temp": CalculatedDataPoint("temp", 19.1, unit=TEMP_FAHRENHEIT),
        "humidity": CalculatedDataPoint("humidity", 34.0, unit=PERCENTAGE),
        "winddir": CalculatedDataPoint("winddir", 139.0, unit=DEGREE),
        "windspeed": CalculatedDataPoint("wind", 20.89, unit=SPEED_MILES_PER_HOUR),
        "windgust": CalculatedDataPoint("gust", 1.12, unit=SPEED_MILES_PER_HOUR),
        "maxdailygust": CalculatedDataPoint("gust", 8.05, unit=SPEED_MILES_PER_HOUR),
        "solarradiation": CalculatedDataPoint(
            "solarradiation", 264.61, unit=IRRADIATION_WATTS_PER_SQUARE_METER
        ),
        "solarradiation_lux": CalculatedDataPoint(
            "solarradiation_lux", 33494.9, unit=LIGHT_LUX
        ),
        "solarradiation_perceived": CalculatedDataPoint(
            "solarradiation_perceived", 90.0, unit=PERCENTAGE
        ),
        "uv": CalculatedDataPoint("uv", 2.0, unit=UV_INDEX),
        "safe_exposure_time_skin_type_1": CalculatedDataPoint(
            "safe_exposure_time_skin_type_1", 83.3, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_2": CalculatedDataPoint(
            "safe_exposure_time_skin_type_2", 100.0, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_3": CalculatedDataPoint(
            "safe_exposure_time_skin_type_3", 133.3, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_4": CalculatedDataPoint(
            "safe_exposure_time_skin_type_4", 166.7, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_5": CalculatedDataPoint(
            "safe_exposure_time_skin_type_5", 266.7, unit=TIME_MINUTES
        ),
        "safe_exposure_time_skin_type_6": CalculatedDataPoint(
            "safe_exposure_time_skin_type_6", 433.3, unit=TIME_MINUTES
        ),
        "rainrate": CalculatedDataPoint("rainrate", 0.0, unit=f"{RAINFALL_INCHES}/hr"),
        "eventrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
        "hourlyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
        "dailyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
        "weeklyrain": CalculatedDataPoint("rain", 0.0, unit=RAINFALL_INCHES),
        "monthlyrain": CalculatedDataPoint("rain", 2.177, unit=RAINFALL_INCHES),
        "yearlyrain": CalculatedDataPoint("rain", 4.441, unit=RAINFALL_INCHES),
        "lightning_num": CalculatedDataPoint("lightning_num", 13, unit=STRIKES),
        "lightning": CalculatedDataPoint("lightning", 0.6, unit=DISTANCE_MILES),
        "lightning_time": CalculatedDataPoint(
            "lightning_time", datetime(2022, 4, 20, 17, 17, 17, tzinfo=timezone.utc)
        ),
        "wh65batt": CalculatedDataPoint("batt", BooleanBatteryState.OFF),
        "dewpoint": CalculatedDataPoint("dewpoint", -4.7, unit=TEMP_FAHRENHEIT),
        "feelslike": CalculatedDataPoint("feelslike", 2.7, unit=TEMP_FAHRENHEIT),
        "heatindex": CalculatedDataPoint("heatindex", 12.3, unit=TEMP_FAHRENHEIT),
        "windchill": CalculatedDataPoint("windchill", 2.7, unit=TEMP_FAHRENHEIT),
        "humidityabs": CalculatedDataPoint(
            data_point_key="humidityabs",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "humidityabsin": CalculatedDataPoint(
            data_point_key="humidityabsin",
            value=0.0,
            unit=WATER_VAPOR_POUNDS_PER_CUBIC_FOOT,
        ),
        "thermalperception": CalculatedDataPoint(
            data_point_key="thermalperception", value=ThermalPerception.DRY, unit=None
        ),
        "frostpoint": CalculatedDataPoint(
            data_point_key="frostpoint", value=-3.3, unit="°F"
        ),
        "frostrisk": CalculatedDataPoint(
            data_point_key="frostrisk", value=FrostRisk.UNLIKELY, unit=None
        ),
        "playstationbattery1": CalculatedDataPoint(
            "batt", BooleanBatteryState.OFF, None
        ),
    }
