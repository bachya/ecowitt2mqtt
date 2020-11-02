"""Define Home Assistant-related functionality."""
from typing import Dict

from ecowitt2mqtt.const import (
    DATA_POINT_24HOURRAININ,
    DATA_POINT_BAROMABSIN,
    DATA_POINT_BAROMRELIN,
    DATA_POINT_CO2,
    DATA_POINT_DAILYRAININ,
    DATA_POINT_DEWPOINT,
    DATA_POINT_EVENTRAININ,
    DATA_POINT_FEELSLIKEF,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HOURLYRAININ,
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
    DATA_POINT_HUMIDITYIN,
    DATA_POINT_LASTRAIN,
    DATA_POINT_MAXDAILYGUST,
    DATA_POINT_MONTHLYRAININ,
    DATA_POINT_PM25,
    DATA_POINT_PM25_24H,
    DATA_POINT_RAINRATEIN,
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
    DATA_POINT_SOILTEMP1F,
    DATA_POINT_SOILTEMP2F,
    DATA_POINT_SOILTEMP3F,
    DATA_POINT_SOILTEMP4F,
    DATA_POINT_SOILTEMP5F,
    DATA_POINT_SOILTEMP6F,
    DATA_POINT_SOILTEMP7F,
    DATA_POINT_SOILTEMP8F,
    DATA_POINT_SOILTEMP9F,
    DATA_POINT_SOILTEMP10F,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_TEMP1F,
    DATA_POINT_TEMP2F,
    DATA_POINT_TEMP3F,
    DATA_POINT_TEMP4F,
    DATA_POINT_TEMP5F,
    DATA_POINT_TEMP6F,
    DATA_POINT_TEMP7F,
    DATA_POINT_TEMP8F,
    DATA_POINT_TEMP9F,
    DATA_POINT_TEMP10F,
    DATA_POINT_TEMPF,
    DATA_POINT_TEMPINF,
    DATA_POINT_TOTALRAININ,
    DATA_POINT_UV,
    DATA_POINT_WEEKLYRAININ,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDGUSTMPH,
    DATA_POINT_WINDSPDMPH_AVG2M,
    DATA_POINT_WINDSPDMPH_AVG10M,
    DATA_POINT_WINDSPEEDMPH,
    DATA_POINT_YEARLYRAININ,
)

DEFAULT_DISCOVERY_PREFIX = "homeassistant"
DEFAULT_ICON = "mdi:server"

DATA_POINTS = {
    DATA_POINT_24HOURRAININ: ("mdi:water", "in"),
    DATA_POINT_BAROMABSIN: ("mdi:cloud", "inches"),
    DATA_POINT_BAROMRELIN: ("mdi:cloud", "inches"),
    DATA_POINT_CO2: ("CO2", "ppm"),
    DATA_POINT_DAILYRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_DEWPOINT: ("mdi:thermometer", "°F"),
    DATA_POINT_EVENTRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_FEELSLIKEF: ("mdi:thermometer", "°F"),
    DATA_POINT_HEATINDEX: ("mdi:thermometer", "°F"),
    DATA_POINT_HOURLYRAININ: ("mdi:weather-pouring", "inches"),
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
    DATA_POINT_HUMIDITYIN: ("mdi:water-percent", "%"),
    DATA_POINT_LASTRAIN: ("mdi:water", "in"),
    DATA_POINT_MAXDAILYGUST: ("mdi:weather-windy", "mph"),
    DATA_POINT_MONTHLYRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_PM25: ("mdi:biohazard", "µg/m^3"),
    DATA_POINT_PM25_24H: ("mdi:biohazard", "µg/m^3"),
    DATA_POINT_RAINRATEIN: ("mdi:weather-pouring", "inches"),
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
    DATA_POINT_SOILTEMP10F: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP1F: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP2F: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP3F: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP4F: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP5F: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP6F: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP7F: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP8F: ("mdi:thermometer", "°F"),
    DATA_POINT_SOILTEMP9F: ("mdi:thermometer", "°F"),
    DATA_POINT_SOLARRADIATION: ("mdi:weather-sunny", "w/m^2"),
    DATA_POINT_TEMP10F: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP1F: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP2F: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP3F: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP4F: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP5F: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP6F: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP7F: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP8F: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMP9F: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMPF: ("mdi:thermometer", "°F"),
    DATA_POINT_TEMPINF: ("mdi:thermometer", "°F"),
    DATA_POINT_TOTALRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_UV: ("mdi:weather-sunny", "UV index"),
    DATA_POINT_WEEKLYRAININ: ("mdi:weather-pouring", "inches"),
    DATA_POINT_WINDCHILL: ("mdi:weather-windy", "°F"),
    DATA_POINT_WINDGUSTMPH: ("mdi:weather-windy", "mph"),
    DATA_POINT_WINDSPDMPH_AVG10M: ("mdi:weather-windy", "mph"),
    DATA_POINT_WINDSPDMPH_AVG2M: ("mdi:weather-windy", "mph"),
    DATA_POINT_WINDSPEEDMPH: ("mdi:weather-windy", "mph"),
    DATA_POINT_YEARLYRAININ: ("mdi:weather-pouring", "inches"),
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
