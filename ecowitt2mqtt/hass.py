"""Define Home Assistant-related functionality."""
from typing import Dict

from ecowitt2mqtt.const import (
    DATA_POINT_BAROMABSIN,
    DATA_POINT_BAROMRELIN,
    DATA_POINT_DAILYRAININ,
    DATA_POINT_DEWPOINT,
    DATA_POINT_EVENTRAININ,
    DATA_POINT_FEELSLIKEF,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HOURLYRAININ,
    DATA_POINT_HUMIDITY,
    DATA_POINT_HUMIDITYIN,
    DATA_POINT_MAXDAILYGUST,
    DATA_POINT_MONTHLYRAININ,
    DATA_POINT_RAINRATEIN,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_TEMPF,
    DATA_POINT_TEMPINF,
    DATA_POINT_TOTALRAININ,
    DATA_POINT_UV,
    DATA_POINT_WEEKLYRAININ,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDDIR,
    DATA_POINT_WINDGUSTMPH,
    DATA_POINT_WINDSPEEDMPH,
    DATA_POINT_YEARLYRAININ,
)

DEFAULT_DISCOVERY_PREFIX = "homeassistant"
DEFAULT_ENTITY_TYPE = "sensor"
DEFAULT_ICON = "mdi:server"

DATA_POINTS = {
    DATA_POINT_BAROMABSIN: ("mdi:cloud", "inches"),
    DATA_POINT_BAROMRELIN: ("mdi:cloud", "inches"),
    DATA_POINT_DAILYRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_DEWPOINT: ("mdi:thermometer", "°F"),
    DATA_POINT_EVENTRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_FEELSLIKEF: ("mdi:thermometer", "°F"),
    DATA_POINT_HEATINDEX: ("mdi:thermometer", "°F"),
    DATA_POINT_HOURLYRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_HUMIDITY: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITYIN: ("mdi:water-perecent", "inches"),
    DATA_POINT_MAXDAILYGUST: ("mdi:weather-windy", "mph"),
    DATA_POINT_MONTHLYRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_RAINRATEIN: ("mdi:weather-pouring", "inches"),
    DATA_POINT_SOLARRADIATION: ("mdi:weather-sunny", "w/m^2"),
    DATA_POINT_TEMPF: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMPINF: ("mdi:thermometer", "°F"),
    DATA_POINT_TOTALRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_UV: ("mdi:weather-sunny", "UV index"),
    DATA_POINT_WEEKLYRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_WINDCHILL: ("mdi:weather-windy", "°F"),
    DATA_POINT_WINDDIR: ("mdi:weather-windy", "°"),
    DATA_POINT_WINDGUSTMPH: ("mdi:weather-windy", "mph"),
    DATA_POINT_WINDSPEEDMPH: ("mdi:weather-windy", "mph"),
    DATA_POINT_YEARLYRAININ: ("mdi:weather-pouring", "inches"),
}

ENTITY_TYPES = {
    DATA_POINT_BAROMABSIN: "sensor",
    DATA_POINT_BAROMRELIN: "sensor",
    DATA_POINT_DAILYRAININ: "sensor",
    DATA_POINT_DEWPOINT: "sensor",
    DATA_POINT_EVENTRAININ: "sensor",
    DATA_POINT_FEELSLIKEF: "sensor",
    DATA_POINT_HEATINDEX: "sensor",
    DATA_POINT_HOURLYRAININ: "sensor",
    DATA_POINT_HUMIDITY: "sensor",
    DATA_POINT_HUMIDITYIN: "sensor",
    DATA_POINT_MAXDAILYGUST: "sensor",
    DATA_POINT_MONTHLYRAININ: "sensor",
    DATA_POINT_RAINRATEIN: "sensor",
    DATA_POINT_SOLARRADIATION: "sensor",
    DATA_POINT_TEMPF: "sensor",
    DATA_POINT_TEMPINF: "sensor",
    DATA_POINT_TOTALRAININ: "sensor",
    DATA_POINT_UV: "sensor",
    DATA_POINT_WEEKLYRAININ: "sensor",
    DATA_POINT_WINDCHILL: "sensor",
    DATA_POINT_WINDDIR: "sensor",
    DATA_POINT_WINDGUSTMPH: "sensor",
    DATA_POINT_WINDSPEEDMPH: "sensor",
    DATA_POINT_YEARLYRAININ: "sensor",
}


class HassDiscovery:  # pylint: disable=too-few-public-methods
    """Define a Home Assistant MQTT Discovery manager."""

    def __init__(
        self, unique_id: str, *, discovery_prefix: str = DEFAULT_DISCOVERY_PREFIX,
    ) -> None:
        """Initialize."""
        self._config_payloads: Dict[str, dict] = {}
        self._discovery_prefix = discovery_prefix
        self._unique_id = unique_id

    def _get_topic(self, key: str, topic_type: str) -> str:
        """Get the attributes topic for a particular entity type."""
        return (
            f"{self._discovery_prefix}/{ENTITY_TYPES.get(key, DEFAULT_ENTITY_TYPE)}"
            f"/{self._unique_id}/{key}/{topic_type}"
        )

    def get_config_payload(self, key: str) -> dict:
        """Return the config payload for a particular entity type."""
        if key in self._config_payloads:
            return self._config_payloads[key]

        try:
            icon, unit = DATA_POINTS[key]
        except KeyError:
            icon, unit = (DEFAULT_ICON, "")

        self._config_payloads[key] = {
            "availability_topic": self._get_topic(key, "availability"),
            "icon": icon if icon else DEFAULT_ICON,
            "name": key,
            "qos": 1,
            "state_topic": self._get_topic(key, "state"),
            "unique_id": f"{self._unique_id}_{key}",
            "unit_of_measurement": unit,
        }

        return self._config_payloads[key]

    def get_config_topic(self, key: str) -> str:
        """Return the config topic for a particular entity type."""
        return self._get_topic(key, "config")

    def get_will_payload(self, key: str) -> str:
        """Return the config topic for a particular entity type."""
        return self._get_topic(key, "config")
