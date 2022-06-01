"""Define battery utilities."""
from __future__ import annotations

BATTERY_STATE_OFF = "OFF"
BATTERY_STATE_ON = "ON"


def calculate_battery(value: float | int) -> float | str:
    """Calculate a battery value.

    1. If the value is a float, we assume it represents voltage and return it as-is.
    2. If the value is an int, we assume it represents a binary state:
         * 0: OK
         * 1: Low
    """
    if not isinstance(value, int):
        return float(value)

    if value == 0:
        return BATTERY_STATE_OFF
    return BATTERY_STATE_ON
