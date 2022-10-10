"""Define unit conversion helpers."""
from __future__ import annotations

from typing import Final

from ecowitt2mqtt.const import (
    SPEED_FEET_PER_SECOND,
    SPEED_INCHES_PER_DAY,
    SPEED_INCHES_PER_HOUR,
    SPEED_KILOMETERS_PER_HOUR,
    SPEED_KNOTS,
    SPEED_METERS_PER_SECOND,
    SPEED_MILES_PER_HOUR,
    SPEED_MILLIMETERS_PER_DAY,
)
from ecowitt2mqtt.errors import EcowittError

# Distance conversion constants:
_MM_TO_M = 0.001
_CM_TO_M = 0.01
_KM_TO_M = 1000

_IN_TO_M = 0.0254
_FOOT_TO_M = _IN_TO_M * 12
_YARD_TO_M = _FOOT_TO_M * 3
_MILE_TO_M = _YARD_TO_M * 1760

_NAUTICAL_MILE_TO_M = 1852

# Duration conversion constants:
_HRS_TO_SECS = 60 * 60
_DAYS_TO_SECS = _HRS_TO_SECS * 24

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


class SpeedConverter(BaseUnitConverter):
    """Utility to convert speed values."""

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

    _UNIT_CONVERSION: dict[str, float] = {
        SPEED_FEET_PER_SECOND: 1 / _FOOT_TO_M,
        SPEED_INCHES_PER_DAY: _DAYS_TO_SECS / _IN_TO_M,
        SPEED_INCHES_PER_HOUR: _HRS_TO_SECS / _IN_TO_M,
        SPEED_KILOMETERS_PER_HOUR: _HRS_TO_SECS / _KM_TO_M,
        SPEED_KNOTS: _HRS_TO_SECS / _NAUTICAL_MILE_TO_M,
        SPEED_METERS_PER_SECOND: 1,
        SPEED_MILES_PER_HOUR: _HRS_TO_SECS / _MILE_TO_M,
        SPEED_MILLIMETERS_PER_DAY: _DAYS_TO_SECS / _MM_TO_M,
    }
