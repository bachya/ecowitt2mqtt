"""Define battery utilities."""
BATTERY_STATE_OFF = "off"
BATTERY_STATE_ON = "on"


def calculate_binary_battery(value: float) -> str:
    """Calculate a "binary battery" value (OK/Low)."""
    if value == 0:
        return BATTERY_STATE_OFF
    return BATTERY_STATE_ON
