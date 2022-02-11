"""Define distance utilities."""
from ecowitt2mqtt.const import UNIT_SYSTEM_IMPERIAL


def calculate_distance(
    value: float,
    *,
    input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: str = UNIT_SYSTEM_IMPERIAL
) -> float:
    """Calculate distance in the appropriate unit system."""
    if input_unit_system == output_unit_system:
        return value
    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        return round(value / 1.609, 1)
    return round(value * 1.609, 1)
