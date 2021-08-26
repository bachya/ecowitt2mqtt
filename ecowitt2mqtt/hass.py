"""Define Home Assistant-related functionality."""
import argparse
from dataclasses import dataclass
from typing import Any, Dict, Optional

from ecowitt2mqtt.const import (
    DATA_POINT_CO2,
    DATA_POINT_DEWPOINT,
    DATA_POINT_FEELSLIKE,
    DATA_POINT_GLOB_BAROM,
    DATA_POINT_GLOB_BATT,
    DATA_POINT_GLOB_GUST,
    DATA_POINT_GLOB_HUMIDITY,
    DATA_POINT_GLOB_MOISTURE,
    DATA_POINT_GLOB_RAIN,
    DATA_POINT_GLOB_TEMP,
    DATA_POINT_GLOB_WIND,
    DATA_POINT_HEATINDEX,
    DATA_POINT_PM25,
    DATA_POINT_PM25_24H,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_SOLARRADIATION_LUX,
    DATA_POINT_SOLARRADIATION_PERCEIVED,
    DATA_POINT_UV,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDDIR,
    LOGGER,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
)
from ecowitt2mqtt.device import Device

PLATFORM_BINARY_SENSOR = "binary_sensor"
PLATFORM_SENSOR = "sensor"

DEVICE_CLASS_BATTERY = "battery"
DEVICE_CLASS_CO = "carbon_monoxide"
DEVICE_CLASS_HUMIDITY = "humidity"
DEVICE_CLASS_ILLUMINANCE = "illuminance"
DEVICE_CLASS_PM25 = "pm25"
DEVICE_CLASS_PRESSURE = "pressure"
DEVICE_CLASS_TEMPERATURE = "temperature"

UNIT_CLASS_PRESSURE = "pressure"
UNIT_CLASS_RAIN = "rain"
UNIT_CLASS_TEMPERATURE = "temperature"
UNIT_CLASS_WIND = "wind"


@dataclass
class EntityDescription:
    """Define a description (set of characteristics) of a Home Assistant entity."""

    key: str
    platform: str

    device_class: Optional[str] = None
    icon: Optional[str] = None
    unit: Optional[str] = None
    unit_class: Optional[str] = None


ENTITY_DESCRIPTIONS = (
    EntityDescription(
        key=DATA_POINT_GLOB_BAROM,
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_PRESSURE,
        unit_class=UNIT_CLASS_PRESSURE,
    ),
    EntityDescription(
        key=DATA_POINT_GLOB_BATT,
        platform=PLATFORM_BINARY_SENSOR,
        device_class=DEVICE_CLASS_BATTERY,
    ),
    EntityDescription(
        key=DATA_POINT_GLOB_GUST,
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-windy",
        unit_class=UNIT_CLASS_WIND,
    ),
    EntityDescription(
        key=DATA_POINT_GLOB_HUMIDITY,
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_HUMIDITY,
        unit="%",
    ),
    EntityDescription(
        key=DATA_POINT_GLOB_MOISTURE,
        platform=PLATFORM_SENSOR,
        icon="mdi:water-percent",
        unit="%",
    ),
    EntityDescription(
        key=DATA_POINT_GLOB_RAIN,
        platform=PLATFORM_SENSOR,
        icon="mdi:water",
        unit_class=UNIT_CLASS_RAIN,
    ),
    EntityDescription(
        key=DATA_POINT_GLOB_TEMP,
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
        unit_class=UNIT_CLASS_TEMPERATURE,
    ),
    EntityDescription(
        key=DATA_POINT_GLOB_WIND,
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-windy",
        unit_class=UNIT_CLASS_WIND,
    ),
    EntityDescription(
        key=DATA_POINT_CO2,
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_CO,
        unit="ppm",
    ),
    EntityDescription(
        key=DATA_POINT_DEWPOINT,
        platform=PLATFORM_SENSOR,
        icon="mdi:thermometer",
        unit_class=UNIT_CLASS_TEMPERATURE,
    ),
    EntityDescription(
        key=DATA_POINT_FEELSLIKE,
        platform=PLATFORM_SENSOR,
        icon="mdi:thermometer",
        unit_class=UNIT_CLASS_TEMPERATURE,
    ),
    EntityDescription(
        key=DATA_POINT_HEATINDEX,
        platform=PLATFORM_SENSOR,
        icon="mdi:thermometer",
        unit_class=UNIT_CLASS_TEMPERATURE,
    ),
    EntityDescription(
        key=DATA_POINT_PM25,
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_PM25,
        unit="µg/m^3",
    ),
    EntityDescription(
        key=DATA_POINT_PM25_24H,
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_PM25,
        unit="µg/m^3",
    ),
    EntityDescription(
        key=DATA_POINT_SOLARRADIATION,
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_ILLUMINANCE,
        unit="w/m^2",
    ),
    EntityDescription(
        key=DATA_POINT_SOLARRADIATION_LUX,
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_ILLUMINANCE,
        unit="lx",
    ),
    EntityDescription(
        key=DATA_POINT_SOLARRADIATION_PERCEIVED,
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_ILLUMINANCE,
        unit="%",
    ),
    EntityDescription(
        key=DATA_POINT_UV,
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-sunny",
        unit="index",
    ),
    EntityDescription(
        key=DATA_POINT_WINDCHILL,
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-windy",
        unit_class=UNIT_CLASS_TEMPERATURE,
    ),
    EntityDescription(
        key=DATA_POINT_WINDDIR,
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-windy",
        unit="°",
    ),
)

UNIT_MAPPING = {
    UNIT_CLASS_PRESSURE: {UNIT_SYSTEM_IMPERIAL: "inHg", UNIT_SYSTEM_METRIC: "hPa"},
    UNIT_CLASS_RAIN: {UNIT_SYSTEM_IMPERIAL: "in", UNIT_SYSTEM_METRIC: "mm"},
    UNIT_CLASS_TEMPERATURE: {UNIT_SYSTEM_IMPERIAL: "°F", UNIT_SYSTEM_METRIC: "°C"},
    UNIT_CLASS_WIND: {UNIT_SYSTEM_IMPERIAL: "mph", UNIT_SYSTEM_METRIC: "km/h"},
}


def get_entity_description(key: str) -> EntityDescription:
    """Get an entity description for a data key.

    1. Return a specific data point if it exists.
    2. Return a globbed data point if it exists.
    3. Return defaults if no specific or globbed data points exist.
    """
    for description in ENTITY_DESCRIPTIONS:
        if description.key == key:
            return description

        if description.key in key:
            return description

    LOGGER.info("No entity description found for key: %s", key)
    return EntityDescription(key=key, platform=PLATFORM_SENSOR)


class HassDiscovery:  # pylint: disable=too-few-public-methods
    """Define a Home Assistant MQTT Discovery manager."""

    def __init__(self, device: Device, args: argparse.Namespace,) -> None:
        """Initialize."""
        self._args = args
        self._config_payloads: Dict[str, Dict[str, Any]] = {}
        self._device = device

    def _get_topic(self, key: str, component: str, topic_type: str) -> str:
        """Get the attributes topic for a particular entity type."""
        return (
            f"{self._args.hass_discovery_prefix}/{component}/{self._device.unique_id}/"
            f"{key}/{topic_type}"
        )

    def get_config_payload(self, key: str) -> Dict[str, Any]:
        """Return the config payload for a particular entity type."""
        if key in self._config_payloads:
            return self._config_payloads[key]

        description = get_entity_description(key)
        if description.unit_class:
            description.unit = UNIT_MAPPING[description.unit_class][
                self._args.output_unit_system
            ]

        self._config_payloads[key] = {
            "availability_topic": self._get_topic(
                key, description.platform, "availability"
            ),
            "device": {
                "identifiers": [self._device.unique_id],
                "manufacturer": self._device.manufacturer,
                "model": self._device.name,
                "name": self._device.name,
                "sw_version": self._device.station_type,
            },
            "name": key,
            "qos": 1,
            "state_topic": self._get_topic(key, description.platform, "state"),
            "unique_id": f"{self._device.unique_id}_{key}",
        }
        if description.device_class:
            self._config_payloads[key]["device_class"] = description.device_class
        if description.icon:
            self._config_payloads[key]["icon"] = description.icon
        if description.unit:
            self._config_payloads[key]["native_unit_of_measurement"] = description.unit

        return self._config_payloads[key]

    def get_config_topic(self, key: str) -> str:
        """Return the config topic for a particular entity type."""
        description = get_entity_description(key)
        return self._get_topic(key, description.platform, "config")
