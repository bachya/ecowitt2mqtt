"""Define unit conversion helpers."""

from __future__ import annotations

import math

from ecowitt2mqtt.backports.enum import StrEnum
from ecowitt2mqtt.const import (
    ACCUMULATED_PRECIPITATION,
    DISTANCE,
    ILLUMINANCE,
    PERCENTAGE,
    PRECIPITATION_RATE,
    PRESSURE,
    SPEED,
    TEMPERATURE,
    UNIT_NOT_RECOGNIZED_TEMPLATE,
    VOLUME,
    UnitOfAccumulatedPrecipitation,
    UnitOfIlluminance,
    UnitOfLength,
    UnitOfPrecipitationRate,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfVolume,
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

# Mass conversion constants:
_POUND_TO_GRAM = 453.59237

# Pressure conversion constants:
_STANDARD_GRAVITY = 9.80665
_MERCURY_DENSITY = 13.5951

# Volume conversion constants:
_CUBIC_FOOT_TO_CUBIC_METER = pow(_FOOT_TO_M, 3)


class UnitConversionError(EcowittError):
    """Define an error for general unit conversion issues."""

    pass


class BaseUnitConverter:
    """Define the format of a conversion utility."""

    UNIT_CLASS: str
    VALID_UNITS: type[StrEnum]

    # This the unit to/from which calculations are done and is stored primarily for
    # documentation:
    NORMALIZED_UNIT: str

    _UNIT_CONVERSION: dict[str, float]

    @classmethod
    def _trim_value_precision_to_ratio(
        cls, value: float, from_unit: str, to_unit: str
    ) -> float:
        """Trim a value to the appropriate precision using the unit ratio.

        Args:
            value: The value to trim.
            from_unit: The unit we are converting from.
            to_unit: The unit we are converting to.

        Returns:
            A trimmed value.
        """
        value_s = str(value)
        precision = len(value_s) - value_s.index(".") - 1 if "." in value_s else 0
        ratio_log = max(0, math.log10(cls.get_unit_ratio(from_unit, to_unit)))
        precision = precision + math.floor(ratio_log)
        return round(value) if precision == 0 else round(value, precision)

    @classmethod
    def _validate_unit(cls, unit: str) -> None:
        """Validate a unit of measurement.

        Args:
            unit: The unit to validate.

        Raises:
            ValueError: Raised when a unit is not recognized.
        """
        try:
            cls.VALID_UNITS(unit)
        except ValueError as err:
            raise UnitConversionError(
                UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, cls.UNIT_CLASS)
            ) from err

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert one unit of measurement to another.

        Args:
            value: The value to convert.
            from_unit: The unit we are converting from.
            to_unit: The unit we are converting to.

        Returns:
            A converted value.

        Raises:
            UnitConversionError: Raised when a unit cannot be recognized.
        """
        if from_unit == to_unit:
            return value

        for unit in (from_unit, to_unit):
            cls._validate_unit(unit)

        from_ratio = cls._UNIT_CONVERSION[from_unit]
        to_ratio = cls._UNIT_CONVERSION[to_unit]
        value = value / from_ratio
        value = value * to_ratio
        return cls._trim_value_precision_to_ratio(value, from_unit, to_unit)

    @classmethod
    def get_unit_ratio(cls, from_unit: str, to_unit: str) -> float:
        """Get unit ratio between units of measurement.

        Args:
            from_unit: The unit we are converting from.
            to_unit: The unit we are converting to.

        Returns:
            A unit ratio.
        """
        return cls._UNIT_CONVERSION[from_unit] / cls._UNIT_CONVERSION[to_unit]


class AccumulatedPrecipitationConverter(BaseUnitConverter):
    """Utility to convert accumulated precipitation values."""

    UNIT_CLASS = ACCUMULATED_PRECIPITATION
    VALID_UNITS = UnitOfAccumulatedPrecipitation
    NORMALIZED_UNIT = UnitOfAccumulatedPrecipitation.MILLIMETERS

    _UNIT_CONVERSION = {
        UnitOfAccumulatedPrecipitation.INCHES: 1 * _MM_TO_M / _IN_TO_M,
        UnitOfAccumulatedPrecipitation.MILLIMETERS: 1,
    }


class DistanceConverter(BaseUnitConverter):
    """Utility to convert distance values."""

    UNIT_CLASS = DISTANCE
    VALID_UNITS = UnitOfLength
    NORMALIZED_UNIT = UnitOfLength.METERS

    _UNIT_CONVERSION = {
        UnitOfLength.METERS: 1,
        UnitOfLength.MILLIMETERS: 1 / _MM_TO_M,
        UnitOfLength.CENTIMETERS: 1 / _CM_TO_M,
        UnitOfLength.KILOMETERS: 1 / _KM_TO_M,
        UnitOfLength.INCHES: 1 / _IN_TO_M,
        UnitOfLength.FEET: 1 / _FOOT_TO_M,
        UnitOfLength.YARD: 1 / _YARD_TO_M,
        UnitOfLength.MILES: 1 / _MILE_TO_M,
    }


class IlluminanceConverter(BaseUnitConverter):
    """Utility to convert illuminance values."""

    UNIT_CLASS = ILLUMINANCE
    VALID_UNITS = UnitOfIlluminance
    NORMALIZED_UNIT = UnitOfIlluminance.LUX

    _UNIT_CONVERSION = {
        UnitOfIlluminance.FOOT_CANDLES: 1 / _FC_TO_LUX,
        UnitOfIlluminance.KILOFOOT_CANDLES: 1 / _FC_TO_LUX / 1000,
        UnitOfIlluminance.KILOLUX: 1 / _KLUX_TO_LUX,
        UnitOfIlluminance.LUX: 1,
        UnitOfIlluminance.WATTS_PER_SQUARE_METER: 1 * _WM2_TO_LUX,
    }

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert one unit of measurement to another.

        Args:
            value: The value to convert.
            from_unit: The unit we are converting from.
            to_unit: The unit we are converting to.

        Returns:
            A converted value.
        """
        if from_unit == to_unit:
            return value

        if from_unit == PERCENTAGE:
            lux = pow(10, value / 20)
            return cls.convert(lux, UnitOfIlluminance.LUX, to_unit)

        if to_unit == PERCENTAGE:
            lux = cls.convert(value, from_unit, UnitOfIlluminance.LUX)
            try:
                return 20 * math.log10(lux)
            except ValueError:
                # If we've approached negative infinity, we'll get a math domain error;
                # in that case, return 0.0:
                return 0.0

        return super().convert(value, from_unit, to_unit)


class PrecipitationRateConverter(BaseUnitConverter):
    """Utility to convert precipitation rate values."""

    UNIT_CLASS = PRECIPITATION_RATE
    VALID_UNITS = UnitOfPrecipitationRate
    NORMALIZED_UNIT = UnitOfPrecipitationRate.MILLIMETERS_PER_HOUR

    _UNIT_CONVERSION = {
        UnitOfPrecipitationRate.INCHES_PER_HOUR: 1 * _MM_TO_M / _IN_TO_M,
        UnitOfPrecipitationRate.MILLIMETERS_PER_HOUR: 1,
    }


class PressureConverter(BaseUnitConverter):
    """Define a utility to convert pressure values."""

    UNIT_CLASS = PRESSURE
    VALID_UNITS = UnitOfPressure
    NORMALIZED_UNIT = UnitOfPressure.PA

    _UNIT_CONVERSION = {
        UnitOfPressure.BAR: 1 / 100000,
        UnitOfPressure.CBAR: 1 / 1000,
        UnitOfPressure.HPA: 1 / 100,
        UnitOfPressure.INHG: 1
        / (_IN_TO_M * 1000 * _STANDARD_GRAVITY * _MERCURY_DENSITY),
        UnitOfPressure.KPA: 1 / 1000,
        UnitOfPressure.MBAR: 1 / 100,
        UnitOfPressure.MMHG: 1
        / (_MM_TO_M * 1000 * _STANDARD_GRAVITY * _MERCURY_DENSITY),
        UnitOfPressure.PA: 1,
        UnitOfPressure.PSI: 1 / 6894.757,
    }


class SpeedConverter(BaseUnitConverter):
    """Define a utility to convert speed values."""

    UNIT_CLASS = SPEED
    VALID_UNITS = UnitOfSpeed
    NORMALIZED_UNIT = UnitOfSpeed.METERS_PER_SECOND

    _UNIT_CONVERSION = {
        UnitOfSpeed.FEET_PER_SECOND: 1 / _FOOT_TO_M,
        UnitOfSpeed.INCHES_PER_DAY: _DAYS_TO_SECS / _IN_TO_M,
        UnitOfSpeed.INCHES_PER_HOUR: _HRS_TO_SECS / _IN_TO_M,
        UnitOfSpeed.KILOMETERS_PER_HOUR: _HRS_TO_SECS / _KM_TO_M,
        UnitOfSpeed.KNOTS: _HRS_TO_SECS / _NAUTICAL_MILE_TO_M,
        UnitOfSpeed.METERS_PER_SECOND: 1,
        UnitOfSpeed.MILES_PER_HOUR: _HRS_TO_SECS / _MILE_TO_M,
        UnitOfSpeed.MILLIMETERS_PER_DAY: _DAYS_TO_SECS / _MM_TO_M,
    }


class TemperatureConverter(BaseUnitConverter):
    """Define a utility to convert temperature values."""

    UNIT_CLASS = TEMPERATURE
    VALID_UNITS = UnitOfTemperature
    NORMALIZED_UNIT = UnitOfTemperature.CELSIUS

    _UNIT_CONVERSION = {
        UnitOfTemperature.CELSIUS: 1.0,
        UnitOfTemperature.FAHRENHEIT: 1.8,
        UnitOfTemperature.KELVIN: 1.0,
    }

    @classmethod
    def _celsius_to_fahrenheit(cls, celsius: float) -> float:
        """Convert a temperature in Celsius to Fahrenheit.

        Args:
            celsius: A Celsius temperature

        Returns:
            A converted temperature.
        """
        return celsius * 1.8 + 32.0

    @classmethod
    def _celsius_to_kelvin(cls, celsius: float) -> float:
        """Convert a temperature in Celsius to Kelvin.

        Args:
            celsius: A Celsius temperature

        Returns:
            A converted temperature.
        """
        return celsius + 273.15

    @classmethod
    def _fahrenheit_to_celsius(cls, fahrenheit: float) -> float:
        """Convert a temperature in Fahrenheit to Celsius.

        Args:
            fahrenheit: A Fahrenheit temperature

        Returns:
            A converted temperature.
        """
        return (fahrenheit - 32.0) / 1.8

    @classmethod
    def _kelvin_to_celsius(cls, kelvin: float) -> float:
        """Convert a temperature in Kelvin to Celsius.

        Args:
            kelvin: A Kelvin temperature

        Returns:
            A converted temperature.
        """
        return kelvin - 273.15

    @classmethod
    def convert(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert a temperature from one unit to another.

        We cannot use the implementation from BaseUnitConverter because the temperature
        units do not use the same floor (0°C and 0°F do not align).

        Args:
            value: The value to convert.
            from_unit: The unit we are converting from.
            to_unit: The unit we are converting to.

        Returns:
            A converted value.

        Raises:
            UnitConversionError: Raised when a unit cannot be recognized.
        """
        if from_unit == to_unit:
            return value

        for unit in (from_unit, to_unit):
            cls._validate_unit(unit)

        if from_unit == UnitOfTemperature.CELSIUS:
            if to_unit == UnitOfTemperature.FAHRENHEIT:
                value = cls._celsius_to_fahrenheit(value)
            elif to_unit == UnitOfTemperature.KELVIN:
                value = cls._celsius_to_kelvin(value)
        elif from_unit == UnitOfTemperature.FAHRENHEIT:
            if to_unit == UnitOfTemperature.CELSIUS:
                value = cls._fahrenheit_to_celsius(value)
            elif to_unit == UnitOfTemperature.KELVIN:
                value = cls._celsius_to_kelvin(cls._fahrenheit_to_celsius(value))
        elif from_unit == UnitOfTemperature.KELVIN:
            if to_unit == UnitOfTemperature.CELSIUS:
                value = cls._kelvin_to_celsius(value)
            if to_unit == UnitOfTemperature.FAHRENHEIT:
                value = cls._celsius_to_fahrenheit(cls._kelvin_to_celsius(value))

        return cls._trim_value_precision_to_ratio(value, from_unit, to_unit)


class VolumeConverter(BaseUnitConverter):
    """Utility to convert volume values."""

    UNIT_CLASS = VOLUME
    VALID_UNITS = UnitOfVolume
    NORMALIZED_UNIT = UnitOfVolume.GRAMS_PER_CUBIC_METER

    _UNIT_CONVERSION = {
        UnitOfVolume.GRAMS_PER_CUBIC_METER: 1,
        UnitOfVolume.POUNDS_PER_CUBIC_FOOT: 1
        * _CUBIC_FOOT_TO_CUBIC_METER
        / _POUND_TO_GRAM,
    }
