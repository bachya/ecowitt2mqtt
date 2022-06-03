"""Define tests for the various calculators."""
# pylint: disable=protected-access,too-many-arguments
import pytest

from ecowitt2mqtt.const import (
    CONF_INPUT_UNIT_SYSTEM,
    CONF_OUTPUT_UNIT_SYSTEM,
    DISTANCE_KILOMETERS,
    DISTANCE_MILES,
    LIGHT_LUX,
    PERCENTAGE,
    PRESSURE_HPA,
    PRESSURE_INHG,
    RAINFALL_INCHES,
    RAINFALL_MILLIMETERS,
    SPEED_KILOMETERS_PER_HOUR,
    SPEED_MILES_PER_HOUR,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
)
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint
from ecowitt2mqtt.helpers.calculator.battery import calculate_battery
from ecowitt2mqtt.helpers.calculator.distance import calculate_distance
from ecowitt2mqtt.helpers.calculator.meteo import (
    calculate_dew_point,
    calculate_feels_like,
    calculate_heat_index,
    calculate_illuminance_wm2_to_lux,
    calculate_illuminance_wm2_to_perceived,
    calculate_pressure,
    calculate_rain_volume,
    calculate_temperature,
    calculate_wind_chill,
    calculate_wind_speed,
)
from ecowitt2mqtt.helpers.typing import UnitSystemType


@pytest.mark.parametrize("value,expected_value", [(0, "OFF"), (1, "ON"), (3.17, 3.17)])
def test_calculate_battery(expected_value, value):
    """Test the battery calculator."""
    assert calculate_battery(value) == expected_value


@pytest.mark.parametrize(
    "temp,humidity,expected_value,expected_unit,input_unit_system,output_unit_system",
    [
        (74.7, 31, 42.1, TEMP_FAHRENHEIT, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (74.2, 16.1, -3.7, TEMP_CELSIUS, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (22.1, 15, -5.7, TEMP_CELSIUS, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (28.4, 45.2, 59.7, TEMP_FAHRENHEIT, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_dew_point(
    config,
    expected_unit,
    expected_value,
    humidity,
    input_unit_system,
    output_unit_system,
    temp,
):
    """Test the dew point calculator."""
    ecowitt = Ecowitt(
        {
            **config,
            CONF_INPUT_UNIT_SYSTEM: input_unit_system,
            CONF_OUTPUT_UNIT_SYSTEM: output_unit_system,
        }
    )
    dew_point = calculate_dew_point(ecowitt, temp=temp, humidity=humidity)
    assert dew_point == CalculatedDataPoint(expected_value, expected_unit)


@pytest.mark.parametrize(
    "value,expected_value,expected_unit,input_unit_system,output_unit_system",
    [
        (10, 10, DISTANCE_MILES, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (17.7, 17.7, DISTANCE_MILES, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        ("20.23", 20.23, DISTANCE_MILES, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (
            "Bad String",
            None,
            DISTANCE_MILES,
            UNIT_SYSTEM_IMPERIAL,
            UNIT_SYSTEM_IMPERIAL,
        ),
        (10, 16.1, DISTANCE_KILOMETERS, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (17.7, 17.7, DISTANCE_KILOMETERS, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (10, 6.2, DISTANCE_MILES, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_distance(
    config, expected_unit, expected_value, input_unit_system, output_unit_system, value
):
    """Test the distance calculator."""
    ecowitt = Ecowitt(
        {
            **config,
            CONF_INPUT_UNIT_SYSTEM: input_unit_system,
            CONF_OUTPUT_UNIT_SYSTEM: output_unit_system,
        }
    )
    distance = calculate_distance(ecowitt, value=value)
    assert distance == CalculatedDataPoint(expected_value, expected_unit)


@pytest.mark.parametrize(
    "temp,humidity,windspeed,expected_value,expected_unit,input_unit_system,output_unit_system",
    [
        (
            24.2,
            31,
            25.2,
            8.2,
            TEMP_FAHRENHEIT,
            UNIT_SYSTEM_IMPERIAL,
            UNIT_SYSTEM_IMPERIAL,
        ),
        (74.2, 16.1, 12, 23.4, TEMP_CELSIUS, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (7.1, 15, 18.7, 2.8, TEMP_CELSIUS, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (
            28.4,
            45.2,
            22,
            83.2,
            TEMP_FAHRENHEIT,
            UNIT_SYSTEM_METRIC,
            UNIT_SYSTEM_IMPERIAL,
        ),
    ],
)
def test_calculate_feels_like(
    config,
    expected_unit,
    expected_value,
    humidity,
    input_unit_system,
    output_unit_system,
    temp,
    windspeed,
):
    """Test the "feels like" calculator."""
    ecowitt = Ecowitt(
        {
            **config,
            CONF_INPUT_UNIT_SYSTEM: input_unit_system,
            CONF_OUTPUT_UNIT_SYSTEM: output_unit_system,
        }
    )
    feels_like = calculate_feels_like(
        ecowitt, temp=temp, humidity=humidity, windspeed=windspeed
    )
    assert feels_like == CalculatedDataPoint(expected_value, expected_unit)


@pytest.mark.parametrize(
    "temp,humidity,expected_value,expected_unit,input_unit_system,output_unit_system",
    [
        (74.7, 31, 73.3, TEMP_FAHRENHEIT, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (74.2, 16.1, 22.3, TEMP_CELSIUS, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (22.1, 15, 20.8, TEMP_CELSIUS, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (28.4, 45.2, 83.2, TEMP_FAHRENHEIT, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_heat_index(
    config,
    expected_unit,
    expected_value,
    humidity,
    input_unit_system,
    output_unit_system,
    temp,
):
    """Test the heat index calculator."""
    ecowitt = Ecowitt(
        {
            **config,
            CONF_INPUT_UNIT_SYSTEM: input_unit_system,
            CONF_OUTPUT_UNIT_SYSTEM: output_unit_system,
        }
    )
    heat_index = calculate_heat_index(ecowitt, temp=temp, humidity=humidity)
    assert heat_index == CalculatedDataPoint(expected_value, expected_unit)


@pytest.mark.parametrize(
    "calculator,solarradiation,expected_value,expected_unit",
    [
        (calculate_illuminance_wm2_to_lux, 264.48, 33478.5, LIGHT_LUX),
        (calculate_illuminance_wm2_to_perceived, 264.48, 90.0, PERCENTAGE),
        (calculate_illuminance_wm2_to_perceived, 1, 42.0, PERCENTAGE),
    ],
)
def test_calculate_illuminance(
    calculator, ecowitt, expected_unit, expected_value, solarradiation
):
    """Test the illuminance calculator."""
    illuminance = calculator(ecowitt, solarradiation=solarradiation)
    assert illuminance == CalculatedDataPoint(expected_value, expected_unit)


@pytest.mark.parametrize(
    "value,expected_value,expected_unit,input_unit_system,output_unit_system",
    [
        (28.122, 28.122, PRESSURE_INHG, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (28.122, 952.321, PRESSURE_HPA, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (8.7, 8.7, PRESSURE_HPA, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (8.7, 0.257, PRESSURE_INHG, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_pressure(
    config, expected_unit, expected_value, input_unit_system, output_unit_system, value
):
    """Test the pressure calculator."""
    ecowitt = Ecowitt(
        {
            **config,
            CONF_INPUT_UNIT_SYSTEM: input_unit_system,
            CONF_OUTPUT_UNIT_SYSTEM: output_unit_system,
        }
    )
    pressure = calculate_pressure(ecowitt, value=value)
    assert pressure == CalculatedDataPoint(expected_value, expected_unit)


@pytest.mark.parametrize(
    "value,expected_value,expected_unit,input_unit_system,output_unit_system",
    [
        (1.3, 1.3, RAINFALL_INCHES, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (1.3, 33.0, RAINFALL_MILLIMETERS, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (7.2, 7.2, RAINFALL_MILLIMETERS, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (7.2, 0.3, RAINFALL_INCHES, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_rain_volume(
    config, expected_unit, expected_value, input_unit_system, output_unit_system, value
):
    """Test the rain volume calculator."""
    ecowitt = Ecowitt(
        {
            **config,
            CONF_INPUT_UNIT_SYSTEM: input_unit_system,
            CONF_OUTPUT_UNIT_SYSTEM: output_unit_system,
        }
    )
    rain_volume = calculate_rain_volume(ecowitt, value=value)
    assert rain_volume == CalculatedDataPoint(expected_value, expected_unit)


@pytest.mark.parametrize(
    "value,expected_value,expected_unit,input_unit_system,output_unit_system",
    [
        (72.3, 72.3, TEMP_FAHRENHEIT, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (82.3, 27.9, TEMP_CELSIUS, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (26.8, 26.8, TEMP_CELSIUS, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (21.4, 70.5, TEMP_FAHRENHEIT, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_temperature(
    config, expected_unit, expected_value, input_unit_system, output_unit_system, value
):
    """Test the temperature calculator."""
    ecowitt = Ecowitt(
        {
            **config,
            CONF_INPUT_UNIT_SYSTEM: input_unit_system,
            CONF_OUTPUT_UNIT_SYSTEM: output_unit_system,
        }
    )
    temperature = calculate_temperature(ecowitt, value=value)
    assert temperature == CalculatedDataPoint(expected_value, expected_unit)


@pytest.mark.parametrize(
    "temp,windspeed,expected_value,expected_unit,input_unit_system,output_unit_system",
    [
        (10.2, 8.8, -2.4, TEMP_FAHRENHEIT, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (74.2, 14.2, None, TEMP_CELSIUS, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (2.1, 42.7, -6.3, TEMP_CELSIUS, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (28.4, 45.2, None, TEMP_FAHRENHEIT, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_wind_chill(
    config,
    expected_unit,
    expected_value,
    input_unit_system,
    output_unit_system,
    temp,
    windspeed,
):
    """Test the wind chill calculator."""
    ecowitt = Ecowitt(
        {
            **config,
            CONF_INPUT_UNIT_SYSTEM: input_unit_system,
            CONF_OUTPUT_UNIT_SYSTEM: output_unit_system,
        }
    )
    wind_chill = calculate_wind_chill(ecowitt, temp=temp, windspeed=windspeed)
    assert wind_chill == CalculatedDataPoint(expected_value, expected_unit)


@pytest.mark.parametrize(
    "value,expected_value,expected_unit,input_unit_system,output_unit_system",
    [
        (10.2, 10.2, SPEED_MILES_PER_HOUR, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (
            16.2,
            26.1,
            SPEED_KILOMETERS_PER_HOUR,
            UNIT_SYSTEM_IMPERIAL,
            UNIT_SYSTEM_METRIC,
        ),
        (1.8, 1.8, SPEED_KILOMETERS_PER_HOUR, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (20.2, 12.6, SPEED_MILES_PER_HOUR, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_wind_speed(
    config, expected_unit, expected_value, input_unit_system, output_unit_system, value
):
    """Test the wind speed calculator."""
    ecowitt = Ecowitt(
        {
            **config,
            CONF_INPUT_UNIT_SYSTEM: input_unit_system,
            CONF_OUTPUT_UNIT_SYSTEM: output_unit_system,
        }
    )
    wind_speed = calculate_wind_speed(ecowitt, value=value)
    assert wind_speed == CalculatedDataPoint(expected_value, expected_unit)
