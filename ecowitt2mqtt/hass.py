"""Define Home Assistant-related functionality."""
from typing import Dict

DEFAULT_DISCOVERY_PREFIX = "homeassistant"
DEFAULT_ENTITY_TYPE = "sensor"
DEFAULT_ICON = "mdi:server"

DATA_POINTS = {
    "tempinf": ("mdi:thermometer", "°F"),
    "humidityin": ("mdi:water-perecent", "inches"),
    "baromrelin": ("mdi:cloud", "inches"),
    "baromabsin": ("mdi:cloud", "inches"),
    "tempf": ("mdi:thermometer", "°F"),
    "humidity": ("mdi:water-percent", "%"),
    "winddir": ("mdi:weather-windy", "°"),
    "windspeedmph": ("mdi:weather-windy", "mph"),
    "windgustmph": ("mdi:weather-windy", "mph"),
    "maxdailygust": ("mdi:weather-windy", "mph"),
    "solarradiation": ("mdi:weather-sunny", "w/m^2"),
    "uv": ("mdi:weather-sunny", "UV index"),
    "rainratein": ("mdi:weather-pouring", "inches"),
    "eventrainin": ("mdi:weather-pouring", "inches"),
    "hourlyrainin": ("mdi:weather-pouring", "inches"),
    "dailyrainin": ("mdi:weather-pouring", "inches"),
    "weeklyrainin": ("mdi:weather-pouring", "inches"),
    "monthlyrainin": ("mdi:weather-pouring", "inches"),
    "yearlyrainin": ("mdi:weather-pouring", "inches"),
    "totalrainin": ("mdi:weather-pouring", "inches"),
}

ENTITY_TYPES = {
    "tempinf": "sensor",
    "humidityin": "sensor",
    "baromrelin": "sensor",
    "baromabsin": "sensor",
    "tempf": "sensor",
    "humidity": "sensor",
    "winddir": "sensor",
    "windspeedmph": "sensor",
    "windgustmph": "sensor",
    "maxdailygust": "sensor",
    "solarradiation": "sensor",
    "uv": "sensor",
    "rainratein": "sensor",
    "eventrainin": "sensor",
    "hourlyrainin": "sensor",
    "dailyrainin": "sensor",
    "weeklyrainin": "sensor",
    "monthlyrainin": "sensor",
    "yearlyrainin": "sensor",
    "totalrainin": "sensor",
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
