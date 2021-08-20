"""Define Home Assistant-related functionality."""
import argparse
from typing import Any, Dict, Optional, Tuple

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
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
)
from ecowitt2mqtt.device import Device

COMPONENT_BINARY_SENSOR = "binary_sensor"
COMPONENT_SENSOR = "sensor"

DEVICE_CLASS_BATTERY = "battery"
DEVICE_CLASS_CO = "carbon_monoxide"
DEVICE_CLASS_HUMIDITY = "humidity"
DEVICE_CLASS_ILLUMINANCE = "illuminance"
DEVICE_CLASS_PRESSURE = "pressure"
DEVICE_CLASS_TEMPERATURE = "temperature"

UNIT_CLASS_PRESSURE = "pressure"
UNIT_CLASS_RAIN = "rain"
UNIT_CLASS_TEMPERATURE = "temperature"
UNIT_CLASS_WIND = "wind"

GLOBBED_ENTITIES = {
    DATA_POINT_GLOB_BAROM: (
        COMPONENT_SENSOR,
        None,
        DEVICE_CLASS_PRESSURE,
        UNIT_CLASS_PRESSURE,
        None,
    ),
    DATA_POINT_GLOB_BATT: (
        COMPONENT_BINARY_SENSOR,
        None,
        DEVICE_CLASS_BATTERY,
        None,
        "v",
    ),
    DATA_POINT_GLOB_GUST: (
        COMPONENT_SENSOR,
        "mdi:weather-windy",
        None,
        UNIT_CLASS_WIND,
        None,
    ),
    DATA_POINT_GLOB_HUMIDITY: (
        COMPONENT_SENSOR,
        None,
        DEVICE_CLASS_HUMIDITY,
        None,
        "%",
    ),
    DATA_POINT_GLOB_MOISTURE: (COMPONENT_SENSOR, "mdi:water-percent", None, None, "%"),
    DATA_POINT_GLOB_RAIN: (COMPONENT_SENSOR, "mdi:water", None, UNIT_CLASS_RAIN, None),
    DATA_POINT_GLOB_TEMP: (
        COMPONENT_SENSOR,
        None,
        DEVICE_CLASS_TEMPERATURE,
        UNIT_CLASS_TEMPERATURE,
        None,
    ),
    DATA_POINT_GLOB_WIND: (
        COMPONENT_SENSOR,
        "mdi:weather-windy",
        None,
        UNIT_CLASS_WIND,
        None,
    ),
}

SPECIFIC_ENTITIES = {
    DATA_POINT_CO2: (COMPONENT_SENSOR, None, DEVICE_CLASS_CO, None, "ppm"),
    DATA_POINT_DEWPOINT: (
        COMPONENT_SENSOR,
        "mdi:thermometer",
        None,
        UNIT_CLASS_TEMPERATURE,
        None,
    ),
    DATA_POINT_FEELSLIKE: (
        COMPONENT_SENSOR,
        "mdi:thermometer",
        None,
        UNIT_CLASS_TEMPERATURE,
        None,
    ),
    DATA_POINT_HEATINDEX: (
        COMPONENT_SENSOR,
        "mdi:thermometer",
        None,
        UNIT_CLASS_TEMPERATURE,
        None,
    ),
    DATA_POINT_PM25: (COMPONENT_SENSOR, "mdi:biohazard", None, None, "µg/m^3"),
    DATA_POINT_PM25_24H: (COMPONENT_SENSOR, "mdi:biohazard", None, None, "µg/m^3"),
    DATA_POINT_SOLARRADIATION: (
        COMPONENT_SENSOR,
        None,
        DEVICE_CLASS_ILLUMINANCE,
        None,
        "w/m^2",
    ),
    DATA_POINT_SOLARRADIATION_LUX: (
        COMPONENT_SENSOR,
        None,
        DEVICE_CLASS_ILLUMINANCE,
        None,
        "lx",
    ),
    DATA_POINT_SOLARRADIATION_PERCEIVED: (
        COMPONENT_SENSOR,
        None,
        DEVICE_CLASS_ILLUMINANCE,
        None,
        "%",
    ),
    DATA_POINT_UV: (COMPONENT_SENSOR, "mdi:weather-sunny", None, None, "UV index"),
    DATA_POINT_WINDCHILL: (
        COMPONENT_SENSOR,
        "mdi:weather-windy",
        None,
        UNIT_CLASS_TEMPERATURE,
        None,
    ),
    DATA_POINT_WINDDIR: (COMPONENT_SENSOR, "mdi:weather-windy", None, None, "°"),
}

UNIT_MAPPING = {
    UNIT_CLASS_PRESSURE: {UNIT_SYSTEM_IMPERIAL: "inHg", UNIT_SYSTEM_METRIC: "hPa"},
    UNIT_CLASS_RAIN: {UNIT_SYSTEM_IMPERIAL: "in", UNIT_SYSTEM_METRIC: "mm"},
    UNIT_CLASS_TEMPERATURE: {UNIT_SYSTEM_IMPERIAL: "°F", UNIT_SYSTEM_METRIC: "°C"},
    UNIT_CLASS_WIND: {UNIT_SYSTEM_IMPERIAL: "mph", UNIT_SYSTEM_METRIC: "km/h"},
}


def get_data_point_characteristics(
    key: str,
) -> Tuple[str, Optional[str], Optional[str], Optional[str], Optional[str]]:
    """Get a data point's characteristics.

    1. Return a specific data point if it exists.
    2. Return a globbed data point if it exists.
    3. Return defaults if no specific or globbed data points exist.
    """
    if key in SPECIFIC_ENTITIES:
        return SPECIFIC_ENTITIES[key]

    matches = [v for k, v in GLOBBED_ENTITIES.items() if k in key]
    if matches:
        return matches[0]

    return (COMPONENT_SENSOR, None, None, None, None)


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

        (
            component,
            icon,
            device_class,
            unit_class,
            unit,
        ) = get_data_point_characteristics(key)
        if unit_class:
            unit = UNIT_MAPPING[unit_class][self._args.output_unit_system]

        self._config_payloads[key] = {
            "availability_topic": self._get_topic(key, component, "availability"),
            "device": {
                "identifiers": [self._device.unique_id],
                "manufacturer": self._device.manufacturer,
                "model": self._device.name,
                "name": self._device.name,
                "sw_version": self._device.station_type,
            },
            "name": key,
            "qos": 1,
            "state_topic": self._get_topic(key, component, "state"),
            "unique_id": f"{self._device.unique_id}_{key}",
        }
        if device_class:
            self._config_payloads[key]["device_class"] = device_class
        if icon:
            self._config_payloads[key]["icon"] = icon
        if unit:
            self._config_payloads[key]["unit_of_measurement"] = unit

        return self._config_payloads[key]

    def get_config_topic(self, key: str) -> str:
        """Return the config topic for a particular entity type."""
        component, _, _, _, _ = get_data_point_characteristics(key)
        return self._get_topic(key, component, "config")
