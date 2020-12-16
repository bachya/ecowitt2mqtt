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
    DATA_POINT_HUMIDITYIN,
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
    DATA_POINT_WINDGUST,
    DATA_POINT_WINDSPD_AVG2M,
    DATA_POINT_WINDSPD_AVG10M,
    DATA_POINT_WINDSPEED,
    DATA_POINT_YEARLYRAIN,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
)

DEFAULT_DISCOVERY_PREFIX = "homeassistant"
DEFAULT_ICON = "mdi:server"

DATA_CLASS_PRESSURE = "pressure"
DATA_CLASS_RAIN = "rain"
DATA_CLASS_TEMPERATURE = "temperature"
DATA_CLASS_WIND = "wind"

DATA_POINTS = {
    DATA_POINT_24HOURRAIN: ("mdi:water", DATA_CLASS_RAIN, None),
    DATA_POINT_BAROMABS: ("mdi:cloud", DATA_CLASS_PRESSURE, None),
    DATA_POINT_BAROMREL: ("mdi:cloud", DATA_CLASS_PRESSURE, None),
    DATA_POINT_CO2: ("CO2", None, "ppm"),
    DATA_POINT_DAILYRAIN: ("mdi:weather-pouring", DATA_CLASS_RAIN, None),
    DATA_POINT_DEWPOINT: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_EVENTRAIN: ("mdi:weather-pouring", DATA_CLASS_RAIN, None),
    DATA_POINT_FEELSLIKE: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_HEATINDEX: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_HOURLYRAIN: ("mdi:weather-pouring", DATA_CLASS_RAIN, None),
    DATA_POINT_HUMIDITY10: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITY1: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITY2: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITY3: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITY4: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITY5: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITY6: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITY7: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITY8: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITY9: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITY: ("mdi:water-percent", None, "%"),
    DATA_POINT_HUMIDITYIN: ("mdi:water-percent", None, "%"),
    DATA_POINT_LASTRAIN: ("mdi:water", DATA_CLASS_RAIN, None),
    DATA_POINT_MAXDAILYGUST: ("mdi:weather-windy", DATA_CLASS_WIND, None),
    DATA_POINT_MONTHLYRAIN: ("mdi:weather-pouring", DATA_CLASS_RAIN, None),
    DATA_POINT_PM25: ("mdi:biohazard", None, "µg/m^3"),
    DATA_POINT_PM25_24H: ("mdi:biohazard", None, "µg/m^3"),
    DATA_POINT_RAINRATE: ("mdi:weather-pouring", DATA_CLASS_RAIN, None),
    DATA_POINT_SOILMOISTURE10: ("mdi:water-percent", None, "%"),
    DATA_POINT_SOILMOISTURE1: ("mdi:water-percent", None, "%"),
    DATA_POINT_SOILMOISTURE2: ("mdi:water-percent", None, "%"),
    DATA_POINT_SOILMOISTURE3: ("mdi:water-percent", None, "%"),
    DATA_POINT_SOILMOISTURE4: ("mdi:water-percent", None, "%"),
    DATA_POINT_SOILMOISTURE5: ("mdi:water-percent", None, "%"),
    DATA_POINT_SOILMOISTURE6: ("mdi:water-percent", None, "%"),
    DATA_POINT_SOILMOISTURE7: ("mdi:water-percent", None, "%"),
    DATA_POINT_SOILMOISTURE8: ("mdi:water-percent", None, "%"),
    DATA_POINT_SOILMOISTURE9: ("mdi:water-percent", None, "%"),
    DATA_POINT_SOILTEMP10: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_SOILTEMP1: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_SOILTEMP2: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_SOILTEMP3: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_SOILTEMP4: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_SOILTEMP5: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_SOILTEMP6: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_SOILTEMP7: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_SOILTEMP8: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_SOILTEMP9: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_SOLARRADIATION: ("mdi:weather-sunny", None, "w/m^2"),
    DATA_POINT_TEMP10: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMP1: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMP2: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMP3: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMP4: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMP5: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMP6: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMP7: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMP8: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMP9: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMP: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TEMPIN: ("mdi:thermometer", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_TOTALRAIN: ("mdi:weather-pouring", DATA_CLASS_RAIN, None),
    DATA_POINT_UV: ("mdi:weather-sunny", None, "UV index"),
    DATA_POINT_WEEKLYRAIN: ("mdi:weather-pouring", DATA_CLASS_RAIN, None),
    DATA_POINT_WINDCHILL: ("mdi:weather-windy", DATA_CLASS_TEMPERATURE, None),
    DATA_POINT_WINDGUST: ("mdi:weather-windy", DATA_CLASS_WIND, None),
    DATA_POINT_WINDSPD_AVG10M: ("mdi:weather-windy", DATA_CLASS_WIND, None),
    DATA_POINT_WINDSPD_AVG2M: ("mdi:weather-windy", DATA_CLASS_WIND, None),
    DATA_POINT_WINDSPEED: ("mdi:weather-windy", DATA_CLASS_WIND, None),
    DATA_POINT_YEARLYRAIN: ("mdi:weather-pouring", DATA_CLASS_RAIN, None),
}

UNIT_MAPPING = {
    DATA_CLASS_PRESSURE: {UNIT_SYSTEM_IMPERIAL: "inHg", UNIT_SYSTEM_METRIC: "hPa"},
    DATA_CLASS_RAIN: {UNIT_SYSTEM_IMPERIAL: "in", UNIT_SYSTEM_METRIC: "mm"},
    DATA_CLASS_TEMPERATURE: {UNIT_SYSTEM_IMPERIAL: "°F", UNIT_SYSTEM_METRIC: "°C"},
    DATA_CLASS_WIND: {UNIT_SYSTEM_IMPERIAL: "mph", UNIT_SYSTEM_METRIC: "km/h"},
}


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
        self._config_payloads: Dict[str, dict] = {}
        self._discovery_prefix = discovery_prefix
        self._unique_id = unique_id
        self._unit_system = unit_system

    def _get_topic(self, key: str, topic_type: str) -> str:
        """Get the attributes topic for a particular entity type."""
        return f"{self._discovery_prefix}/sensor/{self._unique_id}/{key}/{topic_type}"

    def get_config_payload(self, key: str) -> dict:
        """Return the config payload for a particular entity type."""
        if key in self._config_payloads:
            return self._config_payloads[key]

        if key in DATA_POINTS:
            icon, data_class, unit = DATA_POINTS[key]
            if data_class:
                unit = UNIT_MAPPING[data_class][self._unit_system]
        else:
            icon = DEFAULT_ICON
            unit = None

        self._config_payloads[key] = {
            "availability_topic": self._get_topic(key, "availability"),
            "icon": icon,
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
