"""Define tests for the various calculators."""
# pylint: disable=too-many-arguments
import pytest

from ecowitt2mqtt.const import UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC
from ecowitt2mqtt.util.calculator.battery import calculate_battery
from ecowitt2mqtt.util.calculator.distance import calculate_distance
from ecowitt2mqtt.util.calculator.meteo import (
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


@pytest.mark.parametrize("value,expected_output", [(0, "OFF"), (1, "ON"), (3.17, 3.17)])
def test_calculate_battery(expected_output, value):
    """Test the battery calculator."""
    assert calculate_battery(value) == expected_output


@pytest.mark.parametrize(
    "temperature,humidity,expected_output,input_unit_system,output_unit_system",
    [
        (74.7, 31, 42.1, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (74.2, 16.1, -3.7, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (22.1, 15, -5.7, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (28.4, 45.2, 59.7, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_dew_point(
    expected_output, humidity, input_unit_system, output_unit_system, temperature
):
    """Test the dew point calculator."""
    dew_point = calculate_dew_point(
        temperature,
        humidity,
        input_unit_system=input_unit_system,
        output_unit_system=output_unit_system,
    )
    assert dew_point == expected_output


@pytest.mark.parametrize(
    "value,expected_output,input_unit_system,output_unit_system",
    [
        (10, 10, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (17.7, 17.7, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        ("20.23", 20.23, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        ("Bad String", None, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (10, 16.1, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (17.7, 17.7, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (10, 6.2, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_distance(
    expected_output, input_unit_system, output_unit_system, value
):
    """Test the distance calculator."""
    distance = calculate_distance(
        value,
        input_unit_system=input_unit_system,
        output_unit_system=output_unit_system,
    )
    assert distance == expected_output


@pytest.mark.parametrize(
    "temperature,humidity,wind_speed,expected_output,input_unit_system,output_unit_system",
    [
        (24.2, 31, 25.2, 8.2, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (74.2, 16.1, 12, 23.4, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (7.1, 15, 18.7, 2.8, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (28.4, 45.2, 22, 83.2, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_feels_like(
    expected_output,
    humidity,
    input_unit_system,
    output_unit_system,
    temperature,
    wind_speed,
):
    """Test the "feels like" calculator."""
    feels_like = calculate_feels_like(
        temperature,
        humidity,
        wind_speed,
        input_unit_system=input_unit_system,
        output_unit_system=output_unit_system,
    )
    assert feels_like == expected_output


@pytest.mark.parametrize(
    "temperature,humidity,expected_output,input_unit_system,output_unit_system",
    [
        (74.7, 31, 73.3, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (74.2, 16.1, 22.3, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (22.1, 15, 20.8, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (28.4, 45.2, 83.2, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_heat_index(
    expected_output, humidity, input_unit_system, output_unit_system, temperature
):
    """Test the heat index calculator."""
    heat_index = calculate_heat_index(
        temperature,
        humidity,
        input_unit_system=input_unit_system,
        output_unit_system=output_unit_system,
    )
    assert heat_index == expected_output


@pytest.mark.parametrize(
    "calculator,value,expected_output",
    [
        (calculate_illuminance_wm2_to_lux, 264.48, 33478.5),
        (calculate_illuminance_wm2_to_perceived, 264.48, 90.0),
        (calculate_illuminance_wm2_to_perceived, 1, 42.0),
    ],
)
def test_calculate_illuminance(calculator, expected_output, value):
    """Test the illuminance calculator."""
    assert calculator(value) == expected_output


@pytest.mark.parametrize(
    "value,expected_output,input_unit_system,output_unit_system",
    [
        (28.122, 28.122, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (28.122, 952.321, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (8.7, 8.7, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (8.7, 0.257, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_pressure(
    expected_output, input_unit_system, output_unit_system, value
):
    """Test the pressure calculator."""
    pressure = calculate_pressure(
        value,
        input_unit_system=input_unit_system,
        output_unit_system=output_unit_system,
    )
    assert pressure == expected_output


@pytest.mark.parametrize(
    "value,expected_output,input_unit_system,output_unit_system",
    [
        (1.3, 1.3, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (1.3, 33.0, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (7.2, 7.2, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (7.2, 0.3, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_rain_volume(
    expected_output, input_unit_system, output_unit_system, value
):
    """Test the rain volume calculator."""
    rain_volume = calculate_rain_volume(
        value,
        input_unit_system=input_unit_system,
        output_unit_system=output_unit_system,
    )
    assert rain_volume == expected_output


@pytest.mark.parametrize(
    "value,expected_output,input_unit_system,output_unit_system",
    [
        (72.3, 72.3, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (82.3, 27.9, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (26.8, 26.8, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (21.4, 70.5, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_temperature(
    expected_output, input_unit_system, output_unit_system, value
):
    """Test the temperature calculator."""
    temperature = calculate_temperature(
        value,
        input_unit_system=input_unit_system,
        output_unit_system=output_unit_system,
    )
    assert temperature == expected_output


@pytest.mark.parametrize(
    "temperature,wind_speed,expected_output,input_unit_system,output_unit_system",
    [
        (10.2, 8.8, -2.4, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (74.2, 14.2, None, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (2.1, 42.7, -6.3, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (28.4, 45.2, None, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_wind_chill(
    expected_output, input_unit_system, output_unit_system, temperature, wind_speed
):
    """Test the wind chill calculator."""
    wind_chill = calculate_wind_chill(
        temperature,
        wind_speed,
        input_unit_system=input_unit_system,
        output_unit_system=output_unit_system,
    )
    assert wind_chill == expected_output


@pytest.mark.parametrize(
    "value,expected_output,input_unit_system,output_unit_system",
    [
        (10.2, 10.2, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_IMPERIAL),
        (16.2, 26.1, UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC),
        (1.8, 1.8, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_METRIC),
        (20.2, 12.6, UNIT_SYSTEM_METRIC, UNIT_SYSTEM_IMPERIAL),
    ],
)
def test_calculate_wind_speed(
    expected_output, input_unit_system, output_unit_system, value
):
    """Test the wind speed calculator."""
    wind_speed = calculate_wind_speed(
        value,
        input_unit_system=input_unit_system,
        output_unit_system=output_unit_system,
    )
    assert wind_speed == expected_output
