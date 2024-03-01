"""Define an Ecowitt device."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ecowitt2mqtt.util import glob_search

DEFAULT_MANUFACTURER = "Unknown Manufacturer"
DEFAULT_MODEL = "Unknown Model"
DEFAULT_NAME = "Unknown Device"

MODEL_BRAND_MAP = {
    "GW1000": "Ecowitt",
    "GW1100": "Ecowitt",
    "GW2000": "Ecowitt",
    "HP2550": "Ecowitt",
    "HP2551": "Ecowitt",
    "HP2553": "Ecowitt",
    "HP2561": "Ecowitt",
    "HP2564": "Ecowitt",
    "PT-HP2550": "Fine Offset",
    "WH2650": "Fine Offset",
    "WS2350": "La Crosse",
    "WS2900": "Ambient Weather",
}

STATION_TYPE_BRAND_MAP = {
    "AMBWeather": "Ambient Weather",
}


@dataclass(frozen=True)
class Device:
    """Define a data object to provide device details."""

    manufacturer: str
    model: str
    name: str
    station_type: str
    unique_id: str


def get_device_from_raw_payload(payload: dict[str, Any]) -> Device:
    """Return a device based upon a model string.

    Args:
        payload: An Ecowitt device payload.

    Returns:
        A parsed Device object.
    """
    station_type = payload["stationtype"]
    unique_id = payload["PASSKEY"]

    if model := payload.get("model"):
        name, manufacturer = glob_search(MODEL_BRAND_MAP, model)
    else:
        model = DEFAULT_MODEL
        name, manufacturer = glob_search(STATION_TYPE_BRAND_MAP, station_type)

    if not manufacturer:
        manufacturer = DEFAULT_MANUFACTURER
    if not name:
        name = DEFAULT_NAME

    return Device(
        manufacturer=manufacturer,
        model=model,
        name=name,
        station_type=station_type,
        unique_id=unique_id,
    )
