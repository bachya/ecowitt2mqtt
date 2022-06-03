"""Define distance utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ecowitt2mqtt.const import (
    DISTANCE_KILOMETERS,
    DISTANCE_MILES,
    LOGGER,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
)
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

UNIT_MAP = {
    UNIT_SYSTEM_IMPERIAL: DISTANCE_MILES,
    UNIT_SYSTEM_METRIC: DISTANCE_KILOMETERS,
}


def calculate_distance(ecowitt: Ecowitt, *, value: float | int) -> CalculatedDataPoint:
    """Calculate distance in the appropriate unit system."""
    try:
        float_value = float(value)
    except ValueError:
        LOGGER.warning("Could not convert distance value to float: %s", value)
        final_value = None
    else:
        if ecowitt.config.input_unit_system == ecowitt.config.output_unit_system:
            final_value = float_value
        elif ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
            final_value = round(float_value / 1.609, 1)
        else:
            final_value = round(float_value * 1.609, 1)
    return CalculatedDataPoint(final_value, UNIT_MAP[ecowitt.config.output_unit_system])
