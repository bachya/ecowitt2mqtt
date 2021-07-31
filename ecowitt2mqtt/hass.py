"""Define Home Assistant-related functionality."""
from typing import Dict, Optional, Tuple, TypedDict

from ecowitt2mqtt.const import (
    DATA_POINT_CO2,
    DATA_POINT_DEWPOINT,
    DATA_POINT_FEELSLIKE,
    DATA_POINT_HEATINDEX,
    DATA_POINT_PM25,
    DATA_POINT_PM25_24H,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_UV,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDDIR,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
)

COMPONENT_BINARY_SENSOR = "binary_sensor"
COMPONENT_SENSOR = "sensor"

DEFAULT_DISCOVERY_PREFIX = "homeassistant"
DEFAULT_ICON = "mdi:server"

DEVICE_CLASS_BATTERY = "battery"

UNIT_CLASS_PRESSURE = "pressure"
UNIT_CLASS_RAIN = "rain"
UNIT_CLASS_TEMPERATURE = "temperature"
UNIT_CLASS_WIND = "wind"

GLOB_DATA_POINTS = {
    "barom": (COMPONENT_SENSOR, "mdi:cloud", None, UNIT_CLASS_PRESSURE, None),
    "gust": (COMPONENT_SENSOR, "mdi:weather-windy", None, UNIT_CLASS_WIND, None),
    "humidity": (COMPONENT_SENSOR, "mdi:water-percent", None, None, "%"),
    "moisture": (COMPONENT_SENSOR, "mdi:water-percent", None, None, "%"),
    "rain": (COMPONENT_SENSOR, "mdi:water", None, UNIT_CLASS_RAIN, None),
    "temp": (COMPONENT_SENSOR, "mdi:thermometer", None, UNIT_CLASS_TEMPERATURE, None),
    "wind": (COMPONENT_SENSOR, "mdi:weather-windy", None, UNIT_CLASS_WIND, None),
}

SPECIFIC_DATA_POINTS = {
    DATA_POINT_CO2: (COMPONENT_SENSOR, "mdi:molecule-co", None, None, "ppm"),
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
        "mdi:weather-sunny",
        None,
        None,
        "w/m^2",
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
) -> Tuple[str, str, Optional[str], Optional[str], Optional[str]]:
    """Get a data point's characteristics.

    1. Return a specific data point if it exists.
    2. Return a globbed data point if it exists.
    3. Return defaults if no specific or globbed data points exist.
    """
    if key in SPECIFIC_DATA_POINTS:
        return SPECIFIC_DATA_POINTS[key]

    matches = [v for k, v in GLOB_DATA_POINTS.items() if k in key]
    if matches:
        return matches[0]

    return (COMPONENT_SENSOR, DEFAULT_ICON, None, None, None)


class ConfigPayloadType(TypedDict):
    """Define a type for a config payload."""

    availability_topic: str
    config_topic: str
    device_class: Optional[str]
    icon: str
    name: str
    qos: int
    state_topic: str
    unique_id: str
    unit_of_measurement: Optional[str]


class HassDiscovery:  # pylint: disable=too-few-public-methods
    """Define a Home Assistant MQTT Discovery manager."""

    def __init__(
        self,
        unique_id: str,
        unit_system: str,
        *,
        discovery_prefix: str = DEFAULT_DISCOVERY_PREFIX,
    ) -> None:
        """Initialize."""
        self._config_payloads: Dict[str, ConfigPayloadType] = {}
        self._prefix = discovery_prefix
        self._unique_id = unique_id
        self._unit_system = unit_system

    def _get_topic(self, key: str, component: str, topic_type: str) -> str:
        """Get the attributes topic for a particular entity type."""
        return f"{self._prefix}/{component}/{self._unique_id}/{key}/{topic_type}"

    def get_config_payload(self, key: str) -> ConfigPayloadType:
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
            unit = UNIT_MAPPING[unit_class][self._unit_system]

        self._config_payloads[key] = {
            "availability_topic": self._get_topic(key, component, "availability"),
            "config_topic": self._get_topic(key, component, "config"),
            "device_class": device_class,
            "icon": icon,
            "name": key,
            "qos": 1,
            "state_topic": self._get_topic(key, component, "state"),
            "unique_id": f"{self._unique_id}_{key}",
            "unit_of_measurement": unit,
        }

        return self._config_payloads[key]
