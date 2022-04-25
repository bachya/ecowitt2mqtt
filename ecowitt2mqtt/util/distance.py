"""Define distance utilities."""
from typing import Any, Optional

from ecowitt2mqtt.const import LOGGER, UNIT_SYSTEM_IMPERIAL


def calculate_distance(
    value: Any,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> Optional[float]:
    """Calculate distance in the appropriate unit system."""
    try:
        float_value = float(value)
    except ValueError:
        LOGGER.debug("Could not convert distance value to float: %s", value)
        return None

    if input_unit_system == output_unit_system:
        return float_value
    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        return round(float_value / 1.609, 1)
    return round(float_value * 1.609, 1)
