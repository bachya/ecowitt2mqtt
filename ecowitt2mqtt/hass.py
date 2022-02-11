"""Define Home Assistant-related functionality."""
import argparse
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from ecowitt2mqtt.const import (
    DATA_POINT_CO2,
    DATA_POINT_DEWPOINT,
    DATA_POINT_FEELSLIKE,
    DATA_POINT_GLOB_BAROM,
    DATA_POINT_GLOB_BATT,
    DATA_POINT_GLOB_BATT_BINARY,
    DATA_POINT_GLOB_GUST,
    DATA_POINT_GLOB_HUMIDITY,
    DATA_POINT_GLOB_MOISTURE,
    DATA_POINT_GLOB_RAIN,
    DATA_POINT_GLOB_TEMP,
    DATA_POINT_GLOB_WIND,
    DATA_POINT_HEATINDEX,
    DATA_POINT_LIGHTNING,
    DATA_POINT_LIGHTNING_NUM,
    DATA_POINT_LIGHTNING_TIME,
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

# Device classes
DEVICE_CLASS_BATTERY = "battery"
DEVICE_CLASS_CO2 = "carbon_dioxide"
DEVICE_CLASS_HUMIDITY = "humidity"
DEVICE_CLASS_ILLUMINANCE = "illuminance"
DEVICE_CLASS_PM25 = "pm25"
DEVICE_CLASS_PRESSURE = "pressure"
DEVICE_CLASS_TEMPERATURE = "temperature"
DEVICE_CLASS_TIMESTAMP = "timestamp"

# Unit classes:
UNIT_CLASS_DISTANCE = "distance"
UNIT_CLASS_PRESSURE = "pressure"
UNIT_CLASS_RAIN = "rain"
UNIT_CLASS_TEMPERATURE = "temperature"
UNIT_CLASS_WIND = "wind"

# Concentration units:
CONCENTRATION_MICROGRAMS_PER_CUBIC_METER = "µg/m³"
CONCENTRATION_PARTS_PER_MILLION = "ppm"

# Electric units:
ELECTRIC_POTENTIAL_VOLT = "V"

# Generic units:
DEGREE = "°"
INDEX = "index"
PERCENTAGE = "%"

# Irradiation units:
IRRADIATION_WATTS_PER_SQUARE_METER = "W/m²"

# Length units:
LENGTH_INCHES = "in"
LENGTH_KILOMETERS = "km"
LENGTH_MILES = "mi"
LENGTH_MILLIMETERS = "mm"

# Light units:
LIGHT_LUX = "lx"

# Lightning units:
LIGHTNING_STRIKES = "strikes"

# Pressure units:
PRESSURE_INHG = "inHg"
PRESSURE_HPA = "hPa"

# Speed units:
SPEED_KILOMETERS_PER_HOUR = "km/h"
SPEED_MILES_PER_HOUR = "mph"

# Temperature units:
TEMP_CELSIUS = "°C"
TEMP_FAHRENHEIT = "°F"


@dataclass
class EntityDescription:
    """Define a description (set of characteristics) of a Home Assistant entity."""

    platform: str

    device_class: Optional[str] = None
    icon: Optional[str] = None
    unit: Optional[str] = None
    unit_class: Optional[str] = None


ENTITY_DESCRIPTIONS = {
    DATA_POINT_GLOB_BAROM: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_PRESSURE,
        unit_class=UNIT_CLASS_PRESSURE,
    ),
    DATA_POINT_GLOB_BATT: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_BATTERY,
        unit=ELECTRIC_POTENTIAL_VOLT,
    ),
    DATA_POINT_GLOB_BATT_BINARY: EntityDescription(
        platform=PLATFORM_BINARY_SENSOR,
        device_class=DEVICE_CLASS_BATTERY,
    ),
    DATA_POINT_GLOB_GUST: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-windy",
        unit_class=UNIT_CLASS_WIND,
    ),
    DATA_POINT_GLOB_HUMIDITY: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_HUMIDITY,
        unit=PERCENTAGE,
    ),
    DATA_POINT_GLOB_MOISTURE: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:water-percent",
        unit=PERCENTAGE,
    ),
    DATA_POINT_GLOB_RAIN: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:water",
        unit_class=UNIT_CLASS_RAIN,
    ),
    DATA_POINT_GLOB_TEMP: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
        unit_class=UNIT_CLASS_TEMPERATURE,
    ),
    DATA_POINT_GLOB_WIND: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-windy",
        unit_class=UNIT_CLASS_WIND,
    ),
    DATA_POINT_CO2: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_CO2,
        unit=CONCENTRATION_PARTS_PER_MILLION,
    ),
    DATA_POINT_DEWPOINT: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
        unit_class=UNIT_CLASS_TEMPERATURE,
    ),
    DATA_POINT_FEELSLIKE: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
        unit_class=UNIT_CLASS_TEMPERATURE,
    ),
    DATA_POINT_HEATINDEX: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
        unit_class=UNIT_CLASS_TEMPERATURE,
    ),
    DATA_POINT_LIGHTNING: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:map-marker-distance",
        unit_class=UNIT_CLASS_DISTANCE,
    ),
    DATA_POINT_LIGHTNING_NUM: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-lightning",
        unit=LIGHTNING_STRIKES,
    ),
    DATA_POINT_LIGHTNING_TIME: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TIMESTAMP,
    ),
    DATA_POINT_PM25: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_PM25,
        unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    DATA_POINT_PM25_24H: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_PM25,
        unit=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    DATA_POINT_SOLARRADIATION: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_ILLUMINANCE,
        unit=IRRADIATION_WATTS_PER_SQUARE_METER,
    ),
    DATA_POINT_SOLARRADIATION_LUX: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_ILLUMINANCE,
        unit=LIGHT_LUX,
    ),
    DATA_POINT_SOLARRADIATION_PERCEIVED: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_ILLUMINANCE,
        unit=PERCENTAGE,
    ),
    DATA_POINT_UV: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-sunny",
        unit=INDEX,
    ),
    DATA_POINT_WINDCHILL: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
        unit_class=UNIT_CLASS_TEMPERATURE,
    ),
    DATA_POINT_WINDDIR: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-windy",
        unit=DEGREE,
    ),
}

UNIT_MAPPING = {
    UNIT_CLASS_DISTANCE: {
        UNIT_SYSTEM_IMPERIAL: LENGTH_MILES,
        UNIT_SYSTEM_METRIC: LENGTH_KILOMETERS,
    },
    UNIT_CLASS_PRESSURE: {
        UNIT_SYSTEM_IMPERIAL: PRESSURE_INHG,
        UNIT_SYSTEM_METRIC: PRESSURE_HPA,
    },
    UNIT_CLASS_RAIN: {
        UNIT_SYSTEM_IMPERIAL: LENGTH_INCHES,
        UNIT_SYSTEM_METRIC: LENGTH_MILLIMETERS,
    },
    UNIT_CLASS_TEMPERATURE: {
        UNIT_SYSTEM_IMPERIAL: TEMP_FAHRENHEIT,
        UNIT_SYSTEM_METRIC: TEMP_CELSIUS,
    },
    UNIT_CLASS_WIND: {
        UNIT_SYSTEM_IMPERIAL: SPEED_MILES_PER_HOUR,
        UNIT_SYSTEM_METRIC: SPEED_KILOMETERS_PER_HOUR,
    },
}


def get_entity_description(
    key: str, value: Union[float, int, str]
) -> EntityDescription:
    """Get an entity description for a data key.

    1. Return a specific data point if it exists.
    2. Return a globbed data point if it exists.
    3. Return defaults if no specific or globbed data points exist.
    """
    if DATA_POINT_GLOB_BATT in key and isinstance(value, str):
        # Because Ecowitt doesn't give us a clear way to know what sort of battery
        # we're looking at (a binary on/off battery or one that reports voltage), we
        # check its value: strings are binary, floats are voltage:
        return ENTITY_DESCRIPTIONS[DATA_POINT_GLOB_BATT_BINARY]

    if key in ENTITY_DESCRIPTIONS:
        return ENTITY_DESCRIPTIONS[key]

    globbed_descriptions = [v for k, v in ENTITY_DESCRIPTIONS.items() if k in key]
    if globbed_descriptions:
        return globbed_descriptions[0]

    LOGGER.info("No entity description found for key: %s", key)
    return EntityDescription(platform=PLATFORM_SENSOR)


class HassDiscovery:
    """Define a Home Assistant MQTT Discovery manager."""

    def __init__(self, device: Device, args: argparse.Namespace) -> None:
        """Initialize."""
        self._args = args
        self._config_payloads: Dict[str, Dict[str, Any]] = {}
        self._device = device

    def _get_topic(self, key: str, platform: str, topic_type: str) -> str:
        """Get the attributes topic for a particular entity type."""
        return (
            f"{self._args.hass_discovery_prefix}/{platform}/{self._device.unique_id}/"
            f"{key}/{topic_type}"
        )

    def get_config_payload(
        self, key: str, value: Union[float, int, str]
    ) -> Dict[str, Any]:
        """Return the config payload for a particular entity type."""
        if key in self._config_payloads:
            return self._config_payloads[key]

        description = get_entity_description(key, value)

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
            self._config_payloads[key]["unit_of_measurement"] = description.unit

        return self._config_payloads[key]

    def get_config_topic(self, key: str, value: Union[float, int, str]) -> str:
        """Return the config topic for a particular entity type."""
        description = get_entity_description(key, value)
        return self._get_topic(key, description.platform, "config")
