"""Define unit conversion helpers."""
from __future__ import annotations

from typing import Final

from ecowitt2mqtt.const import (
    ILLUMINANCE_FOOT_CANDLES,
    ILLUMINANCE_KILOFOOT_CANDLES,
    ILLUMINANCE_KILOLUX,
    ILLUMINANCE_LUX,
    ILLUMINANCE_WATTS_PER_SQUARE_METER,
    LENGTH_CENTIMETERS,
    LENGTH_FEET,
    LENGTH_INCHES,
    LENGTH_KILOMETERS,
    LENGTH_METERS,
    LENGTH_MILES,
    LENGTH_MILLIMETERS,
    LENGTH_YARD,
    PRECIPITATION_INCHES,
    PRECIPITATION_INCHES_PER_HOUR,
    PRECIPITATION_MILLIMETERS,
    PRECIPITATION_MILLIMETERS_PER_HOUR,
    PRESSURE_BAR,
    PRESSURE_CBAR,
    PRESSURE_HPA,
    PRESSURE_INHG,
    PRESSURE_KPA,
    PRESSURE_MBAR,
    PRESSURE_MMHG,
    PRESSURE_PA,
    PRESSURE_PSI,
    SPEED_FEET_PER_SECOND,
    SPEED_INCHES_PER_DAY,
    SPEED_INCHES_PER_HOUR,
    SPEED_KILOMETERS_PER_HOUR,
    SPEED_KNOTS,
    SPEED_METERS_PER_SECOND,
    SPEED_MILES_PER_HOUR,
    SPEED_MILLIMETERS_PER_DAY,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    TEMP_KELVIN,
)
from ecowitt2mqtt.errors import EcowittError

# Distance conversion constants:
_CM_TO_M = 0.01
_IN_TO_M = 0.0254
_KM_TO_M = 1000
_MM_TO_M = 0.001
_NAUTICAL_MILE_TO_M = 1852
_FOOT_TO_M = _IN_TO_M * 12
_YARD_TO_M = _FOOT_TO_M * 3
_MILE_TO_M = _YARD_TO_M * 1760

# Duration conversion constants:
_HRS_TO_SECS = 60 * 60
_DAYS_TO_SECS = _HRS_TO_SECS * 24

# Illuminance conversion constants:
_KLUX_TO_LUX = 1000
_FC_TO_LUX = 10.7639
_WM2_TO_LUX = 0.0079

# Pressure conversion constants:
_STANDARD_GRAVITY = 9.80665
_MERCURY_DENSITY = 13.5951

UNIT_NOT_RECOGNIZED_TEMPLATE: Final = '"{}" is not a recognized {} unit'


class UnitConversionError(EcowittError):
    """Define an error for general unit conversion issues."""

    pass


class BaseUnitConverter:
    """Define the format of a conversion utility."""

    UNIT_CLASS: str
    NORMALIZED_UNIT: str
    VALID_UNITS: set[str]

    _UNIT_CONVERSION: dict[str, float]

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert one unit of measurement to another."""
        if from_unit == to_unit:
            return value

        for unit in (from_unit, to_unit):
            if unit in cls.VALID_UNITS:
                continue
            raise UnitConversionError(
                UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, cls.UNIT_CLASS)
            )

        from_ratio = cls._UNIT_CONVERSION[from_unit]
        to_ratio = cls._UNIT_CONVERSION[to_unit]
        new_value = value / from_ratio
        return new_value * to_ratio


class DistanceConverter(BaseUnitConverter):
    """Utility to convert distance values."""

    UNIT_CLASS = "distance"
    NORMALIZED_UNIT = LENGTH_METERS
    VALID_UNITS = {
        LENGTH_KILOMETERS,
        LENGTH_MILES,
        LENGTH_FEET,
        LENGTH_METERS,
        LENGTH_CENTIMETERS,
        LENGTH_MILLIMETERS,
        LENGTH_INCHES,
        LENGTH_YARD,
    }

    _UNIT_CONVERSION = {
        LENGTH_METERS: 1,
        LENGTH_MILLIMETERS: 1 / _MM_TO_M,
        LENGTH_CENTIMETERS: 1 / _CM_TO_M,
        LENGTH_KILOMETERS: 1 / _KM_TO_M,
        LENGTH_INCHES: 1 / _IN_TO_M,
        LENGTH_FEET: 1 / _FOOT_TO_M,
        LENGTH_YARD: 1 / _YARD_TO_M,
        LENGTH_MILES: 1 / _MILE_TO_M,
    }


class IlluminanceConverter(BaseUnitConverter):
    """Utility to convert illuminance values."""

    UNIT_CLASS = "illuminance"
    NORMALIZED_UNIT = ILLUMINANCE_LUX
    VALID_UNITS = {
        ILLUMINANCE_FOOT_CANDLES,
        ILLUMINANCE_KILOFOOT_CANDLES,
        ILLUMINANCE_KILOLUX,
        ILLUMINANCE_LUX,
        ILLUMINANCE_WATTS_PER_SQUARE_METER,
    }

    _UNIT_CONVERSION = {
        ILLUMINANCE_FOOT_CANDLES: 1 / _FC_TO_LUX,
        ILLUMINANCE_KILOFOOT_CANDLES: 1 / _FC_TO_LUX / 1000,
        ILLUMINANCE_KILOLUX: 1 / _KLUX_TO_LUX,
        ILLUMINANCE_LUX: 1,
        ILLUMINANCE_WATTS_PER_SQUARE_METER: 1 * _WM2_TO_LUX,
    }


class PrecipitationConverter(BaseUnitConverter):
    """Utility to convert precipitation values."""

    UNIT_CLASS = "precipitation"
    # Note that we can accept either mm or mm/h as the normalized unit:
    NORMALIZED_UNIT = PRECIPITATION_MILLIMETERS
    VALID_UNITS = {
        PRECIPITATION_MILLIMETERS,
        PRECIPITATION_MILLIMETERS_PER_HOUR,
        PRECIPITATION_INCHES,
        PRECIPITATION_INCHES_PER_HOUR,
    }

    _UNIT_CONVERSION = {
        PRECIPITATION_INCHES: 1 * _MM_TO_M / _IN_TO_M,
        PRECIPITATION_INCHES_PER_HOUR: 1 * _MM_TO_M / _IN_TO_M,
        PRECIPITATION_MILLIMETERS: 1,
        PRECIPITATION_MILLIMETERS_PER_HOUR: 1,
    }


class PressureConverter(BaseUnitConverter):
    """Define a utility to convert pressure values."""

    UNIT_CLASS = "pressure"
    NORMALIZED_UNIT = PRESSURE_PA
    VALID_UNITS = {
        PRESSURE_BAR,
        PRESSURE_CBAR,
        PRESSURE_HPA,
        PRESSURE_INHG,
        PRESSURE_KPA,
        PRESSURE_MBAR,
        PRESSURE_MMHG,
        PRESSURE_PA,
        PRESSURE_PSI,
    }

    _UNIT_CONVERSION = {
        PRESSURE_BAR: 1 / 100000,
        PRESSURE_CBAR: 1 / 1000,
        PRESSURE_HPA: 1 / 100,
        PRESSURE_INHG: 1 / (_IN_TO_M * 1000 * _STANDARD_GRAVITY * _MERCURY_DENSITY),
        PRESSURE_KPA: 1 / 1000,
        PRESSURE_MBAR: 1 / 100,
        PRESSURE_MMHG: 1 / (_MM_TO_M * 1000 * _STANDARD_GRAVITY * _MERCURY_DENSITY),
        PRESSURE_PA: 1,
        PRESSURE_PSI: 1 / 6894.757,
    }


class SpeedConverter(BaseUnitConverter):
    """Define a utility to convert speed values."""

    UNIT_CLASS = "speed"
    NORMALIZED_UNIT = SPEED_METERS_PER_SECOND
    VALID_UNITS = {
        SPEED_FEET_PER_SECOND,
        SPEED_INCHES_PER_DAY,
        SPEED_INCHES_PER_HOUR,
        SPEED_KILOMETERS_PER_HOUR,
        SPEED_KNOTS,
        SPEED_METERS_PER_SECOND,
        SPEED_MILES_PER_HOUR,
        SPEED_MILLIMETERS_PER_DAY,
    }

    _UNIT_CONVERSION = {
        SPEED_FEET_PER_SECOND: 1 / _FOOT_TO_M,
        SPEED_INCHES_PER_DAY: _DAYS_TO_SECS / _IN_TO_M,
        SPEED_INCHES_PER_HOUR: _HRS_TO_SECS / _IN_TO_M,
        SPEED_KILOMETERS_PER_HOUR: _HRS_TO_SECS / _KM_TO_M,
        SPEED_KNOTS: _HRS_TO_SECS / _NAUTICAL_MILE_TO_M,
        SPEED_METERS_PER_SECOND: 1,
        SPEED_MILES_PER_HOUR: _HRS_TO_SECS / _MILE_TO_M,
        SPEED_MILLIMETERS_PER_DAY: _DAYS_TO_SECS / _MM_TO_M,
    }


class TemperatureConverter(BaseUnitConverter):
    """Define a utility to convert temperature values."""

    UNIT_CLASS = "temperature"
    NORMALIZED_UNIT = TEMP_CELSIUS
    VALID_UNITS = {
        TEMP_CELSIUS,
        TEMP_FAHRENHEIT,
        TEMP_KELVIN,
    }

    _UNIT_CONVERSION = {
        TEMP_CELSIUS: 1.0,
        TEMP_FAHRENHEIT: 1.8,
        TEMP_KELVIN: 1.0,
    }

    @classmethod
    def _celsius_to_fahrenheit(cls, celsius: float) -> float:
        """Convert a temperature in Celsius to Fahrenheit."""
        return celsius * 1.8 + 32.0

    @classmethod
    def _celsius_to_kelvin(cls, celsius: float) -> float:
        """Convert a temperature in Celsius to Kelvin."""
        return celsius + 273.15

    @classmethod
    def _fahrenheit_to_celsius(cls, fahrenheit: float) -> float:
        """Convert a temperature in Fahrenheit to Celsius."""
        return (fahrenheit - 32.0) / 1.8

    @classmethod
    def _kelvin_to_celsius(cls, kelvin: float) -> float:
        """Convert a temperature in Kelvin to Celsius."""
        return kelvin - 273.15

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert a temperature from one unit to another.

        We cannot use the implementation from BaseUnitConverter because the temperature
        units do not use the same floor (0°C and 0°F do not align).
        """
        if from_unit == to_unit:
            return value

        for unit in (from_unit, to_unit):
            if unit in cls.VALID_UNITS:
                continue
            raise UnitConversionError(
                UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, cls.UNIT_CLASS)
            )

        if from_unit == TEMP_CELSIUS:
            if to_unit == TEMP_FAHRENHEIT:
                value = cls._celsius_to_fahrenheit(value)
            elif to_unit == TEMP_KELVIN:
                value = cls._celsius_to_kelvin(value)
        elif from_unit == TEMP_FAHRENHEIT:
            if to_unit == TEMP_CELSIUS:
                value = cls._fahrenheit_to_celsius(value)
            elif to_unit == TEMP_KELVIN:
                value = cls._celsius_to_kelvin(cls._fahrenheit_to_celsius(value))
        elif from_unit == TEMP_KELVIN:
            if to_unit == TEMP_CELSIUS:
                value = cls._kelvin_to_celsius(value)
            if to_unit == TEMP_FAHRENHEIT:
                value = cls._celsius_to_fahrenheit(cls._kelvin_to_celsius(value))

        return value
