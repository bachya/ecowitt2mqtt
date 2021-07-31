"""Define an Ecowitt device."""
from typing import Any, Dict, NamedTuple, Optional

from ecowitt2mqtt.const import LOGGER

DEFAULT_MANUFACTURER = "Unknown"
DEFAULT_NAME = "Unknown Device"
DEFAULT_STATION_TYPE = "Unknown Station Type"

DEVICE_DATA = {
    "GW1000_Pro": ("Ecowitt", "GW1000 Pro"),
    "WH2650": ("Waldbeck", "Hally Weather Station"),
}


class Device(NamedTuple):
    """Simple data object to provide device details."""

    manufacturer: str
    name: str
    station_type: Optional[str]


def get_device_from_raw_payload(payload: Dict[str, Any]) -> Device:
    """Return a device based upon a model string."""
    model = payload.get("model")
    station_type = payload.get("stationtype")

    if not model:
        return Device(DEFAULT_MANUFACTURER, DEFAULT_NAME, DEFAULT_STATION_TYPE)

    try:
        manufacturer, name = DEVICE_DATA[model]
    except KeyError:
        LOGGER.info(
            'Unknown device model ("%s"); please report it at '
            "https://github.com/bachya/ecowitt2mqtt",
            model,
        )
        manufacturer = DEFAULT_MANUFACTURER
        name = DEFAULT_NAME
        station_type = DEFAULT_STATION_TYPE

    return Device(manufacturer, name, station_type)
