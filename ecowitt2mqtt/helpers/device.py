"""Define an Ecowitt device."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ecowitt2mqtt.const import LOGGER

DEFAULT_MANUFACTURER = "Unknown"
DEFAULT_NAME = "Unknown Device"
DEFAULT_STATION_TYPE = "Unknown Station Type"
DEFAULT_UNIQUE_ID = "default"


@dataclass
class MappedDevice:
    """Define a registered device."""

    brand: str
    model: str


DEVICE_MAP = {
    "GW1000": MappedDevice("Ecowitt", "GW1000"),
    "GW1100": MappedDevice("Ecowitt", "GW1100"),
    "GW2000A": MappedDevice("Ecowitt", "GW2000A"),
    "GW2000B": MappedDevice("Ecowitt", "GW2000B"),
    "GW2000C": MappedDevice("Ecowitt", "GW2000C"),
    "HP2550_Pro": MappedDevice("Misol", "HP2250_Pro"),
    "PT-HP2550": MappedDevice("Fine Offset", "HP2550"),
    "WH2650": MappedDevice("Fine Offset", "WH2650"),
    "WS2900": MappedDevice("Ambient Weather", "WS-2902C"),
}


@dataclass(frozen=True)
class Device:
    """Define a data object to provide device details."""

    unique_id: str
    manufacturer: str
    name: str
    station_type: str


def get_device_from_raw_payload(payload: dict[str, Any]) -> Device:
    """Return a device based upon a model string.

    Args:
        payload: An Ecowitt device payload.

    Returns:
        A parsed Device object.
    """
    model = payload["model"]
    station_type = payload.get("stationtype", DEFAULT_STATION_TYPE)
    unique_id = payload.get("PASSKEY", DEFAULT_UNIQUE_ID)

    if model in DEVICE_MAP:
        mapped_device = DEVICE_MAP[model]
    else:
        if matches := [v for k, v in DEVICE_MAP.items() if k in model]:
            mapped_device = matches[0]
        else:
            LOGGER.info(
                (
                    "Unknown device; please report it at "
                    "https://github.com/bachya/ecowitt2mqtt (payload: %s)"
                ),
                payload,
            )
            mapped_device = MappedDevice(DEFAULT_MANUFACTURER, DEFAULT_NAME)

    return Device(unique_id, mapped_device.brand, mapped_device.model, station_type)
