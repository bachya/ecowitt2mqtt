"""Define Home Assistant-related functionality."""
from typing import Dict

from ecowitt2mqtt.const import (
    DATA_POINT_24HOURRAIN,
    DATA_POINT_BAROMABS,
    DATA_POINT_BAROMREL,
    DATA_POINT_CO2,
    DATA_POINT_DAILYRAIN,
    DATA_POINT_DEWPOINT,
    DATA_POINT_EVENTRAIN,
    DATA_POINT_FEELSLIKE,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HOURLYRAIN,
    DATA_POINT_HUMIDITY,
    DATA_POINT_HUMIDITY1,
    DATA_POINT_HUMIDITY2,
    DATA_POINT_HUMIDITY3,
    DATA_POINT_HUMIDITY4,
    DATA_POINT_HUMIDITY5,
    DATA_POINT_HUMIDITY6,
    DATA_POINT_HUMIDITY7,
    DATA_POINT_HUMIDITY8,
    DATA_POINT_HUMIDITY9,
    DATA_POINT_HUMIDITY10,
    DATA_POINT_LASTRAIN,
    DATA_POINT_MAXDAILYGUST,
    DATA_POINT_MONTHLYRAIN,
    DATA_POINT_PM25,
    DATA_POINT_PM25_24H,
    DATA_POINT_RAINRATE,
    DATA_POINT_SOILMOISTURE1,
    DATA_POINT_SOILMOISTURE2,
    DATA_POINT_SOILMOISTURE3,
    DATA_POINT_SOILMOISTURE4,
    DATA_POINT_SOILMOISTURE5,
    DATA_POINT_SOILMOISTURE6,
    DATA_POINT_SOILMOISTURE7,
    DATA_POINT_SOILMOISTURE8,
    DATA_POINT_SOILMOISTURE9,
    DATA_POINT_SOILMOISTURE10,
    DATA_POINT_SOILTEMP1,
    DATA_POINT_SOILTEMP2,
    DATA_POINT_SOILTEMP3,
    DATA_POINT_SOILTEMP4,
    DATA_POINT_SOILTEMP5,
    DATA_POINT_SOILTEMP6,
    DATA_POINT_SOILTEMP7,
    DATA_POINT_SOILTEMP8,
    DATA_POINT_SOILTEMP9,
    DATA_POINT_SOILTEMP10,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_TEMP,
    DATA_POINT_TEMP1,
    DATA_POINT_TEMP2,
    DATA_POINT_TEMP3,
    DATA_POINT_TEMP4,
    DATA_POINT_TEMP5,
    DATA_POINT_TEMP6,
    DATA_POINT_TEMP7,
    DATA_POINT_TEMP8,
    DATA_POINT_TEMP9,
    DATA_POINT_TEMP10,
    DATA_POINT_TEMPIN,
    DATA_POINT_TOTALRAIN,
    DATA_POINT_UV,
    DATA_POINT_WEEKLYRAIN,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDGUSTMPH,
    DATA_POINT_WINDSPDMPH_AVG2M,
    DATA_POINT_WINDSPDMPH_AVG10M,
    DATA_POINT_WINDSPEEDMPH,
    DATA_POINT_YEARLYRAIN,
)

DEFAULT_DISCOVERY_PREFIX = "homeassistant"
DEFAULT_ICON = "mdi:server"

DATA_POINTS = {
    DATA_POINT_24HOURRAIN: ("mdi:water", "in"),
    DATA_POINT_BAROMABS: ("mdi:cloud", "inches"),
    DATA_POINT_BAROMREL: ("mdi:cloud", "inches"),
    DATA_POINT_CO2: ("CO2", "ppm"),
    DATA_POINT_DAILYRAIN: ("mdi:weather-pouring", "inches"),
    DATA_POINT_DEWPOINT: ("mdi:thermometer", "°F"),
    DATA_POINT_EVENTRAIN: ("mdi:weather-pouring", "inches"),
    DATA_POINT_FEELSLIKE: ("mdi:thermometer", "°F"),
    DATA_POINT_HEATINDEX: ("mdi:thermometer", "°F"),
    DATA_POINT_HOURLYRAIN: ("mdi:weather-pouring", "inches"),
    DATA_POINT_HUMIDITY10: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY1: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY2: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY3: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY4: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY5: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY6: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY7: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY8: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY9: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY: ("mdi:water-percent", "%"),
    DATA_POINT_HUMIDITY: ("mdi:water-percent", "%"),
    DATA_POINT_LASTRAIN: ("mdi:water", "in"),
    DATA_POINT_MAXDAILYGUST: ("mdi:weather-windy", "mph"),
    DATA_POINT_MONTHLYRAIN: ("mdi:weather-pouring", "inches"),
    DATA_POINT_PM25: ("mdi:biohazard", "µg/m^3"),
    DATA_POINT_PM25_24H: ("mdi:biohazard", "µg/m^3"),
    DATA_POINT_RAINRATE: ("mdi:weather-pouring", "inches"),
    DATA_POINT_SOILMOISTURE10: ("mdi:water-percent", "%"),
    DATA_POINT_SOILMOISTURE1: ("mdi:water-percent", "%"),
    DATA_POINT_SOILMOISTURE2: ("mdi:water-percent", "%"),
    DATA_POINT_SOILMOISTURE3: ("mdi:water-percent", "%"),
    DATA_POINT_SOILMOISTURE4: ("mdi:water-percent", "%"),
    DATA_POINT_SOILMOISTURE5: ("mdi:water-percent", "%"),
    DATA_POINT_SOILMOISTURE6: ("mdi:water-percent", "%"),
    DATA_POINT_SOILMOISTURE7: ("mdi:water-percent", "%"),
    DATA_POINT_SOILMOISTURE8: ("mdi:water-percent", "%"),
    DATA_POINT_SOILMOISTURE9: ("mdi:water-percent", "%"),
    DATA_POINT_SOILTEMP10: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP1: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP2: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP3: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP4: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP5: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP6: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP7: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP8: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP9: ("mdi:thermometer", "°F"),
    DATA_POINT_SOLARRADIATION: ("mdi:weather-sunny", "w/m^2"),
    DATA_POINT_TEMP10: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP1: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP2: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP3: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP4: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP5: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP6: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP7: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP8: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP9: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMPIN: ("mdi:thermometer", "°F"),
    DATA_POINT_TOTALRAIN: ("mdi:weather-pouring", "inches"),
    DATA_POINT_UV: ("mdi:weather-sunny", "UV index"),
    DATA_POINT_WEEKLYRAIN: ("mdi:weather-pouring", "inches"),
    DATA_POINT_WINDCHILL: ("mdi:weather-windy", "°F"),
    DATA_POINT_WINDGUSTMPH: ("mdi:weather-windy", "mph"),
    DATA_POINT_WINDSPDMPH_AVG10M: ("mdi:weather-windy", "mph"),
    DATA_POINT_WINDSPDMPH_AVG2M: ("mdi:weather-windy", "mph"),
    DATA_POINT_WINDSPEEDMPH: ("mdi:weather-windy", "mph"),
    DATA_POINT_YEARLYRAIN: ("mdi:weather-pouring", "inches"),
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
        return f"{self._discovery_prefix}/sensor/{self._unique_id}/{key}/{topic_type}"

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
