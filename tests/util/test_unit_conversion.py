"""Test unit conversion helpers."""
import pytest

from ecowitt2mqtt.util.unit_conversion import (
    DistanceConverter,
    IlluminanceConverter,
    PrecipitationConverter,
    PressureConverter,
    SpeedConverter,
    TemperatureConverter,
    UnitConversionError,
)


@pytest.mark.parametrize(
    "unit_class,converter,from_unit,to_unit",
    [
        ("distance", DistanceConverter, "miles", "ft"),
        ("distance", DistanceConverter, "m", "dm"),
        ("illuminance", IlluminanceConverter, "lux", "bulbs"),
        ("illuminance", IlluminanceConverter, "sunbeams", "klux"),
        ("precipitation", PrecipitationConverter, "mm/s", "mm/h"),
        ("precipitation", PrecipitationConverter, "in/h", "yd/yr"),
        ("pressure", PressureConverter, "hPa", "hPa/s"),
        ("pressure", PressureConverter, "units", "hPa"),
        ("speed", SpeedConverter, "mph", "km/s"),
        ("speed", SpeedConverter, "km/d", "m/s"),
        ("temperature", TemperatureConverter, "°C", "Bolts"),
        ("temperature", TemperatureConverter, "Fake", "°C"),
    ],
)
def test_invalid_units(converter, from_unit, to_unit, unit_class):
    """Test that invalid units raise an error."""
    with pytest.raises(UnitConversionError) as err:
        _ = converter.convert(10, from_unit, to_unit)
        assert f"is not a recognized {unit_class} unit" in str(err)


@pytest.mark.parametrize(
    "value,from_unit,to_unit,converted_value",
    [
        (10, "km", "km", 10.0),
        (10, "km", "mi", 6.21371192237334),
        (10, "km", "ft", 32808.39895013124),
        (10, "km", "m", 10000.0),
        (10, "km", "cm", 1000000.0),
        (10, "km", "mm", 10000000.0),
        (10, "km", "in", 393700.78740157484),
        (10, "km", "yd", 10936.13298337708),
    ],
)
def test_distance_conversion(converted_value, from_unit, to_unit, value):
    """Test distance conversions."""
    assert DistanceConverter.convert(value, from_unit, to_unit) == converted_value


@pytest.mark.parametrize(
    "value,from_unit,to_unit,converted_value",
    [
        (10, "lux", "lux", 10.0),
        (10, "lux", "fc", 0.9290312990644656),
        (10, "lux", "kfc", 0.0009290312990644657),
        (10, "lux", "klux", 0.01),
        (10, "lux", "W/m²", 0.07900000000000001),
        (10, "W/m²", "lux", 1265.8227848101264),
        (10, "fc", "lux", 107.639),
        (10, "fc", "klux", 0.107639),
    ],
)
def test_illuminance_conversion(converted_value, from_unit, to_unit, value):
    """Test illuminance conversions."""
    assert IlluminanceConverter.convert(value, from_unit, to_unit) == converted_value


@pytest.mark.parametrize(
    "value,from_unit,to_unit,converted_value",
    [
        (10, "mm", "mm", 10.0),
        (10, "in", "mm", 254.0),
        (10, "mm", "in", 0.39370078740157477),
        (10, "mm/h", "mm/h", 10.0),
        (10, "in/h", "mm/h", 254.0),
        (10, "mm/h", "in/h", 0.39370078740157477),
    ],
)
def test_precipitation_conversion(converted_value, from_unit, to_unit, value):
    """Test precipitation conversions."""
    assert PrecipitationConverter.convert(value, from_unit, to_unit) == converted_value


@pytest.mark.parametrize(
    "value,from_unit,to_unit,converted_value",
    [
        (10, "bar", "Pa", 999999.9999999999),
        (10, "cbar", "Pa", 10000.0),
        (10, "hPa", "Pa", 1000.0),
        (10, "inHg", "Pa", 33863.88640341),
        (10, "kPa", "Pa", 10000.0),
        (10, "mbar", "Pa", 1000.0),
        (10, "mmHg", "Pa", 1333.22387415),
        (10, "Pa", "Pa", 10.0),
        (10, "Pa", "psi", 0.0014503774389728313),
        (10, "inHg", "cbar", 33.86388640341),
    ],
)
def test_pressure_conversion(converted_value, from_unit, to_unit, value):
    """Test pressure conversions."""
    assert PressureConverter.convert(value, from_unit, to_unit) == converted_value


@pytest.mark.parametrize(
    "value,from_unit,to_unit,converted_value",
    [
        (10, "ft/s", "m/s", 3.0479999999999996),
        (1000, "in/d", "m/s", 0.00029398148148148144),
        (100, "in/h", "m/s", 0.0007055555555555556),
        (100, "km/h", "m/s", 27.77777777777778),
        (10, "kn", "m/s", 5.144444444444445),
        (1, "m/s", "m/s", 1.0),
        (100, "mph", "m/s", 44.70399999999999),
        (10000, "mm/d", "m/s", 0.00011574074074074075),
        (1, "m/s", "in/d", 3401574.8031496066),
        (10, "in/h", "km/h", 0.000254),
    ],
)
def test_speed_conversion(converted_value, from_unit, to_unit, value):
    """Test speed conversions."""
    assert SpeedConverter.convert(value, from_unit, to_unit) == converted_value


@pytest.mark.parametrize(
    "value,from_unit,to_unit,converted_value",
    [
        (20, "°C", "°C", 20.0),
        (20, "°C", "°F", 68.0),
        (10, "°C", "K", 283.15),
        (80, "°F", "°C", 26.666666666666664),
        (70, "°F", "K", 294.26111111111106),
        (200, "K", "°C", -73.14999999999998),
        (350, "K", "°F", 170.33000000000004),
    ],
)
def test_temperature_conversion(converted_value, from_unit, to_unit, value):
    """Test temperature conversions."""
    assert TemperatureConverter.convert(value, from_unit, to_unit) == converted_value


@pytest.mark.parametrize(
    "converter,from_unit,to_unit,ratio",
    [
        (DistanceConverter, "km", "m", 0.001),
        (DistanceConverter, "mi", "m", 0.000621371192237334),
        (DistanceConverter, "ft", "m", 3.280839895013124),
        (DistanceConverter, "m", "m", 1.0),
        (DistanceConverter, "cm", "m", 100.0),
        (DistanceConverter, "mm", "m", 1000.0),
        (DistanceConverter, "in", "m", 39.37007874015748),
        (DistanceConverter, "yd", "m", 1.093613298337708),
    ],
)
def test_unit_ratio(converter, from_unit, ratio, to_unit):
    """Test the ratio between two units."""
    assert converter.get_unit_ratio(from_unit, to_unit) == ratio
