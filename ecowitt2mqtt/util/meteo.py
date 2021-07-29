"""Define meteorological utilities."""
from ecowitt2mqtt.const import UNIT_SYSTEM_IMPERIAL


def get_temperature_unit(unit_system: str) -> str:
    """Get the correct temperature unit based on the provided unit system."""
    if unit_system == UNIT_SYSTEM_IMPERIAL:
        return "f"
    return "c"
