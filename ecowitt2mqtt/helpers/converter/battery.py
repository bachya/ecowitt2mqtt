"""Define battery converter helpers."""
# pylint: disable=too-few-public-methods
from ecowitt2mqtt.const import UNIT_SYSTEM_IMPERIAL
from ecowitt2mqtt.helpers.converter import Converter

BATTERY_STATE_OFF = "off"
BATTERY_STATE_ON = "on"


class BinaryBatteryConverter(Converter):
    """Define an object to hold convertible barometric pressure data."""

    def __init__(
        self,
        value: float,
        *,
        input_unit_system: str = UNIT_SYSTEM_IMPERIAL,
        output_unit_system: str = UNIT_SYSTEM_IMPERIAL
    ) -> None:
        """Initialize."""
        super().__init__(
            input_unit_system=input_unit_system, output_unit_system=output_unit_system
        )

        self._value = value

    def parse(self) -> str:
        """Return an appropriately-parsed data value."""
        if self._value == 0:
            return BATTERY_STATE_OFF
        return BATTERY_STATE_ON
