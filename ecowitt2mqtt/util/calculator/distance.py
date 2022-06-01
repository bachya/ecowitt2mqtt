"""Define distance utilities."""
from __future__ import annotations

from ecowitt2mqtt.const import LOGGER, UNIT_SYSTEM_IMPERIAL
from ecowitt2mqtt.helpers.typing import UnitSystemType


def calculate_distance(
    value: float | int | str,
    *,
    input_unit_system: UnitSystemType = UNIT_SYSTEM_IMPERIAL,
    output_unit_system: UnitSystemType = UNIT_SYSTEM_IMPERIAL,
) -> float | None:
    """Calculate distance in the appropriate unit system.

    * Imperial: Miles (mi)
    * Metric: Kilometers (km)
    """
    try:
        float_value = float(value)
    except ValueError:
        LOGGER.warning("Could not convert distance value to float: %s", value)
        return None

    if input_unit_system == output_unit_system:
        return float_value
    if output_unit_system == UNIT_SYSTEM_IMPERIAL:
        return round(float_value / 1.609, 1)
    return round(float_value * 1.609, 1)
