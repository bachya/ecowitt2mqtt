"""Define battery utilities."""
from typing import Union

BATTERY_STATE_OFF = "off"
BATTERY_STATE_ON = "on"


def calculate_battery(value: Union[float, int]) -> Union[float, str]:
    """Calculate a battery value.

    1. If the value is a float, we assume it represents voltage and return it as-is.
    2. If the value is an int, we assume it represents a binary state:
         * 0: OK
         * 1: Low
    """
    if isinstance(value, float):
        return value

    if value == 0:
        return BATTERY_STATE_OFF
    return BATTERY_STATE_ON
