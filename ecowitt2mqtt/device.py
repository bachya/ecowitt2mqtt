"""Define an Ecowitt device."""
from typing import Any, Dict, NamedTuple, Optional

from ecowitt2mqtt.const import LOGGER

DEFAULT_MANUFACTURER = "Unknown"
DEFAULT_NAME = "Unknown Device"
DEFAULT_STATION_TYPE = "Unknown Station Type"
DEFAULT_UNIQUE_ID = "default"

DEVICE_DATA = {
    "GW1000_Pro": ("Ecowitt", "GW1000 Pro"),
    "WH2650": ("Fine Offset", "WH2650"),
    "WS2900": ("Ambient Weather", "WS-2902C"),
}


class Device(NamedTuple):
    """Simple data object to provide device details."""

    unique_id: str
    manufacturer: str
    name: str
    station_type: Optional[str]


def get_device_from_raw_payload(payload: Dict[str, Any]) -> Device:
    """Return a device based upon a model string."""
    model = payload["model"]
    station_type = payload.get("stationtype", DEFAULT_STATION_TYPE)
    unique_id = payload.get("PASSKEY", DEFAULT_UNIQUE_ID)

    if model in DEVICE_DATA:
        manufacturer, name = DEVICE_DATA[model]
    else:
        matches = [v for k, v in DEVICE_DATA.items() if k in model]
        if matches:
            manufacturer, name = matches[0]
        else:
            LOGGER.info(
                (
                    "Unknown device; please report it at "
                    "https://github.com/bachya/ecowitt2mqtt (payload: %s)"
                ),
                payload,
            )
            manufacturer = DEFAULT_MANUFACTURER
            name = DEFAULT_NAME

    return Device(unique_id, manufacturer, name, station_type)
