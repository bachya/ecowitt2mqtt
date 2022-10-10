"""Test unit conversion helpers."""
import pytest

from ecowitt2mqtt.util.unit_conversion import SpeedConverter, UnitConversionError


@pytest.mark.parametrize(
    "unit_class,from_unit,to_unit",
    [
        ("speed", "mph", "whatever"),
        ("speed", "whatever", "m/s"),
    ],
)
def test_invalid_units(from_unit, to_unit, unit_class):
    """Test that invalid units raise an error."""
    with pytest.raises(UnitConversionError) as err:
        _ = SpeedConverter.convert(10, from_unit, to_unit)
        assert f"is not a recognized {unit_class} unit" in str(err)


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
