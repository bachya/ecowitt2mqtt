"""Define an Ecowitt device."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ecowitt2mqtt.const import LOGGER

DEFAULT_MANUFACTURER = "Unknown"
DEFAULT_NAME = "Unknown Device"
DEFAULT_STATION_TYPE = "Unknown Station Type"
DEFAULT_UNIQUE_ID = "default"

DEVICE_DATA = {
    "GW1000": ("Ecowitt", "GW1000"),
    "GW1100": ("Ecowitt", "GW1100"),
    "GW2000A": ("Ecowitt", "GW2000A"),
    "GW2000B": ("Ecowitt", "GW2000B"),
    "HP2550_Pro": ("Misol", "HP2250_Pro"),
    "PT-HP2550": ("Fine Offset", "HP2550"),
    "WH2650": ("Fine Offset", "WH2650"),
    "WS2900": ("Ambient Weather", "WS-2902C"),
}


@dataclass(frozen=True)
class Device:
    """Define a data object to provide device details."""

    unique_id: str
    manufacturer: str
    name: str
    station_type: str


def get_device_from_raw_payload(payload: dict[str, Any]) -> Device:
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
