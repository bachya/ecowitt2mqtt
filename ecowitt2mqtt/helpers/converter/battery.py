"""Define battery converter helpers."""
# pylint: disable=too-few-public-methods

from ecowitt2mqtt.helpers.converter import Converter

BATTERY_STATE_OFF = "off"
BATTERY_STATE_ON = "on"


class BinaryBatteryConverter(Converter):
    """Define an object to hold convertible barometric pressure data."""

    def __init__(self, value: float) -> None:
        """Initialize."""
        self._value = value

    def parse(self) -> str:
        """Return an appropriately-parsed data value."""
        if self._value == 0:
            return BATTERY_STATE_OFF
        return BATTERY_STATE_ON
