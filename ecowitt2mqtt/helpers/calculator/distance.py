"""Define distance utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ecowitt2mqtt.const import (
    DISTANCE_KILOMETERS,
    DISTANCE_MILES,
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


def calculate_distance(
    ecowitt: Ecowitt, payload_key: str, data_point_key: str, *, value: float
) -> CalculatedDataPoint:
    """Calculate distance in the appropriate unit system."""
    if ecowitt.config.input_unit_system == ecowitt.config.output_unit_system:
        final_value = value
    elif ecowitt.config.output_unit_system == UNIT_SYSTEM_IMPERIAL:
        final_value = round(value / 1.609, 1)
    else:
        final_value = round(value * 1.609, 1)
    return CalculatedDataPoint(
        data_point_key=data_point_key,
        value=final_value,
        unit=UNIT_MAP[ecowitt.config.output_unit_system],
    )
