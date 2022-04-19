"""Define distance utilities."""
from typing import Any

from ecowitt2mqtt.const import UNIT_SYSTEM_IMPERIAL


def calculate_distance(
    value: Any,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> float:
    """Calculate distance in the appropriate unit system."""
    float_value = float(value)

    if input_unit_system == output_unit_system:
        return float_value
    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        return round(float_value / 1.609, 1)
    return round(float_value * 1.609, 1)
