"""Define MQTT publishing."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypedDict

from asyncio_mqtt import MqttError

from ecowitt2mqtt.backports.enum import StrEnum
from ecowitt2mqtt.const import (
    DATA_POINT_CO2,
    DATA_POINT_CO2_24H,
    DATA_POINT_DAILY_RAIN,
    DATA_POINT_DEWPOINT,
    DATA_POINT_DRAIN_PIEZO,
    DATA_POINT_ERAIN_PIEZO,
    DATA_POINT_EVENT_RAIN,
    DATA_POINT_FEELSLIKE,
    DATA_POINT_FROST_POINT,
    DATA_POINT_FROST_RISK,
    DATA_POINT_GLOB_BAROM,
    DATA_POINT_GLOB_BATT,
    DATA_POINT_GLOB_GUST,
    DATA_POINT_GLOB_HUMIDITY,
    DATA_POINT_GLOB_LEAK,
    DATA_POINT_GLOB_MOISTURE,
    DATA_POINT_GLOB_PM10,
    DATA_POINT_GLOB_PM25,
    DATA_POINT_GLOB_R_RAIN,
    DATA_POINT_GLOB_RAIN,
    DATA_POINT_GLOB_TEMP,
    DATA_POINT_GLOB_TF,
    DATA_POINT_GLOB_VOLT,
    DATA_POINT_GLOB_WETNESS,
    DATA_POINT_GLOB_WIND,
    DATA_POINT_GLOB_WINDDIR,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HOURLY_RAIN,
    DATA_POINT_HRAIN_PIEZO,
    DATA_POINT_HUMI_CO2,
    DATA_POINT_HUMIDITY_ABS,
    DATA_POINT_HUMIDITY_ABS_IN,
    DATA_POINT_LIGHTNING,
    DATA_POINT_LIGHTNING_NUM,
    DATA_POINT_LIGHTNING_TIME,
    DATA_POINT_MONTHLY_RAIN,
    DATA_POINT_MRAIN_PIEZO,
    DATA_POINT_RAIN_RATE,
    DATA_POINT_RUNTIME,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5,
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6,
    DATA_POINT_SIMMER_INDEX,
    DATA_POINT_SIMMER_ZONE,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_SOLARRADIATION_LUX,
    DATA_POINT_SOLARRADIATION_PERCEIVED,
    DATA_POINT_TF_CO2,
    DATA_POINT_THERMAL_PERCEPTION,
    DATA_POINT_TOTAL_AIN,
    DATA_POINT_TOTAL_RAIN,
    DATA_POINT_UV,
    DATA_POINT_WEEKLY_RAIN,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WRAIN_PIEZO,
    DATA_POINT_YEARLY_RAIN,
    DATA_POINT_YRAIN_PIEZO,
    LOGGER,
)
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint, DataPointType
from ecowitt2mqtt.helpers.calculator.battery import (
    BatteryStrategy,
    get_battery_strategy,
)
from ecowitt2mqtt.helpers.device import Device
from ecowitt2mqtt.helpers.publisher import (
    MqttPublisher,
    PublishError,
    generate_mqtt_payload,
)
from ecowitt2mqtt.helpers.typing import DataValueType

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


class DeviceClass(StrEnum):
    """Define a device class enum."""

    BATTERY = "battery"
    CO2 = "carbon_dioxide"
    DURATION = "duration"
    HUMIDITY = "humidity"
    ILLUMINANCE = "illuminance"
    MOISTURE = "moisture"
    PM10 = "pm10"
    PM25 = "pm25"
    PRESSURE = "pressure"
    TEMPERATURE = "temperature"
    TIMESTAMP = "timestamp"
    VOLTAGE = "voltage"


class EntityCategory(StrEnum):
    """Define an entity category enum."""

    CONFIG = "config"
    DIAGNOSTIC = "diagnostic"


class Platform(StrEnum):
    """Define a platform enum."""

    BINARY_SENSOR = "binary_sensor"
    SENSOR = "sensor"


class StateClass(StrEnum):
    """Define a state class enum."""

    MEASUREMENT = "measurement"
    TOTAL = "total"
    TOTAL_INCREASING = "total_increasing"


class DeviceType(TypedDict):
    """Define a type that represents a Home Assistant device."""

    identifiers: list[str]
    manufacturer: str
    model: str
    name: str
    sw_version: str


@dataclass
class EntityDescription:
    """Define a description (set of characteristics) of a Home Assistant entity."""

    device_class: str | None = None
    entity_category: str | None = None
    icon: str | None = None
    state_class: str | None = None


@dataclass
class HassDiscoveryPayload:
    """Define a MQTT Discovery configuration for an entity."""

    payload: dict[str, Any]
    topic: str


AVAILABILITY_OFFLINE = "offline"
AVAILABILITY_ONLINE = "online"

DATA_POINT_BATTERY_BOOLEAN = "battery_boolean"
DATA_POINT_BATTERY_NUMERIC = "battery_numeric"
DATA_POINT_BATTERY_PERCENTAGE = "battery_percentage"

ENTITY_DESCRIPTIONS = {
    DATA_POINT_BATTERY_BOOLEAN: EntityDescription(
        device_class=DeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    DATA_POINT_BATTERY_NUMERIC: EntityDescription(
        device_class=DeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_BATTERY_PERCENTAGE: EntityDescription(
        device_class=DeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_CO2: EntityDescription(
        device_class=DeviceClass.CO2,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_CO2_24H: EntityDescription(
        device_class=DeviceClass.CO2,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_DEWPOINT: EntityDescription(
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_FEELSLIKE: EntityDescription(
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_FROST_POINT: EntityDescription(
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_FROST_RISK: EntityDescription(
        icon="mdi:snowflake-alert",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_BAROM: EntityDescription(
        device_class=DeviceClass.PRESSURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_GUST: EntityDescription(
        icon="mdi:weather-windy",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_HUMIDITY: EntityDescription(
        device_class=DeviceClass.HUMIDITY,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_LEAK: EntityDescription(
        device_class=DeviceClass.MOISTURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_MOISTURE: EntityDescription(
        icon="mdi:water-percent",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_PM10: EntityDescription(
        device_class=DeviceClass.PM10,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_PM25: EntityDescription(
        device_class=DeviceClass.PM25,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_R_RAIN: EntityDescription(
        icon="mdi:water",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_RAIN: EntityDescription(
        icon="mdi:water",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_TEMP: EntityDescription(
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_TF: EntityDescription(
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_VOLT: EntityDescription(
        device_class=DeviceClass.VOLTAGE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_WETNESS: EntityDescription(
        icon="mdi:water-percent",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_WIND: EntityDescription(
        icon="mdi:weather-windy",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_WINDDIR: EntityDescription(
        icon="mdi:compass",
    ),
    DATA_POINT_HEATINDEX: EntityDescription(
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_HUMI_CO2: EntityDescription(
        device_class=DeviceClass.HUMIDITY,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_HUMIDITY_ABS: EntityDescription(
        device_class=DeviceClass.HUMIDITY,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_HUMIDITY_ABS_IN: EntityDescription(
        device_class=DeviceClass.HUMIDITY,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_LIGHTNING: EntityDescription(
        icon="mdi:map-marker-distance",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_LIGHTNING_NUM: EntityDescription(
        icon="mdi:weather-lightning",
        state_class=StateClass.TOTAL,
    ),
    DATA_POINT_LIGHTNING_TIME: EntityDescription(
        device_class=DeviceClass.TIMESTAMP,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1: EntityDescription(
        icon="mdi:timer",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2: EntityDescription(
        icon="mdi:timer",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3: EntityDescription(
        icon="mdi:timer",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4: EntityDescription(
        icon="mdi:timer",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5: EntityDescription(
        icon="mdi:timer",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6: EntityDescription(
        icon="mdi:timer",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SIMMER_INDEX: EntityDescription(
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SIMMER_ZONE: EntityDescription(
        icon="mdi:heat-wave",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SOLARRADIATION: EntityDescription(
        device_class=DeviceClass.ILLUMINANCE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SOLARRADIATION_LUX: EntityDescription(
        device_class=DeviceClass.ILLUMINANCE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SOLARRADIATION_PERCEIVED: EntityDescription(
        device_class=DeviceClass.ILLUMINANCE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_RAIN_RATE: EntityDescription(
        icon="mdi:water",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_RUNTIME: EntityDescription(
        device_class=DeviceClass.DURATION,
        icon="mdi:timer",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_THERMAL_PERCEPTION: EntityDescription(
        icon="mdi:water",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_TF_CO2: EntityDescription(
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_TOTAL_AIN: EntityDescription(
        icon="mdi:water",
        state_class=StateClass.TOTAL_INCREASING,
    ),
    DATA_POINT_UV: EntityDescription(
        icon="mdi:weather-sunny",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_WINDCHILL: EntityDescription(
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
}

PLATFORM_MAP = {
    DataPointType.BOOLEAN: Platform.BINARY_SENSOR,
    DataPointType.NON_BOOLEAN: Platform.SENSOR,
}

STATE_CLASS_OVERRIDES = {
    DATA_POINT_DAILY_RAIN: StateClass.TOTAL,
    DATA_POINT_DRAIN_PIEZO: StateClass.TOTAL,
    DATA_POINT_ERAIN_PIEZO: StateClass.TOTAL,
    DATA_POINT_EVENT_RAIN: StateClass.TOTAL,
    DATA_POINT_HOURLY_RAIN: StateClass.TOTAL,
    DATA_POINT_HRAIN_PIEZO: StateClass.TOTAL,
    DATA_POINT_MONTHLY_RAIN: StateClass.TOTAL,
    DATA_POINT_MRAIN_PIEZO: StateClass.TOTAL,
    DATA_POINT_TOTAL_RAIN: StateClass.TOTAL,
    DATA_POINT_WEEKLY_RAIN: StateClass.TOTAL,
    DATA_POINT_WRAIN_PIEZO: StateClass.TOTAL,
    DATA_POINT_YEARLY_RAIN: StateClass.TOTAL,
    DATA_POINT_YRAIN_PIEZO: StateClass.TOTAL,
}


def get_availability_payload(data_point: CalculatedDataPoint) -> str:
    """Get the availability payload for a data point."""
    if data_point.value is None:
        return AVAILABILITY_OFFLINE
    return AVAILABILITY_ONLINE


class HomeAssistantDiscoveryPublisher(MqttPublisher):
    """Define an MQTT publisher for the MQTT Discovery standard."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        super().__init__(ecowitt)

        self._discovery_payloads: dict[str, HassDiscoveryPayload] = {}

    def _generate_discovery_payload(
        self, device: Device, payload_key: str, data_point: CalculatedDataPoint
    ) -> HassDiscoveryPayload:
        """Generate a discovery payload for an entity."""
        # Since batteries can be one of many different strategies, we calculate an
        # entity description at runtime:
        if data_point.data_point_key in (DATA_POINT_GLOB_BATT, DATA_POINT_GLOB_VOLT):
            strategy = get_battery_strategy(self.ecowitt, payload_key)
            if strategy == BatteryStrategy.BOOLEAN:
                data_point_key = DATA_POINT_BATTERY_BOOLEAN
            elif strategy == BatteryStrategy.NUMERIC:
                data_point_key = DATA_POINT_BATTERY_NUMERIC
            else:
                data_point_key = DATA_POINT_BATTERY_PERCENTAGE
        else:
            data_point_key = data_point.data_point_key

        if self.ecowitt.config.hass_entity_id_prefix:
            name = f"{self.ecowitt.config.hass_entity_id_prefix}_{payload_key}"
        else:
            name = payload_key

        base_topic = (
            f"{self.ecowitt.config.hass_discovery_prefix}"
            f"/{PLATFORM_MAP[data_point.data_type]}/{device.unique_id}/{payload_key}"
        )

        payload = self._discovery_payloads[payload_key] = HassDiscoveryPayload(
            {
                "availability_topic": f"{base_topic}/availability",
                "device": {
                    "identifiers": [device.unique_id],
                    "manufacturer": device.manufacturer,
                    "model": device.name,
                    "name": device.name,
                    "sw_version": device.station_type,
                },
                "name": name,
                "qos": 1,
                "state_topic": f"{base_topic}/state",
                "unique_id": f"{device.unique_id}_{payload_key}",
            },
            f"{base_topic}/config",
        )

        if data_point.unit:
            payload.payload["unit_of_measurement"] = data_point.unit

        # If we have an entity description, use it:
        if description := ENTITY_DESCRIPTIONS.get(data_point_key):
            for discovery_key, value in (
                ("device_class", description.device_class),
                ("entity_category", description.entity_category),
                ("icon", description.icon),
                (
                    "state_class",
                    STATE_CLASS_OVERRIDES.get(payload_key, description.state_class),
                ),
            ):
                if not value:
                    continue
                payload.payload[discovery_key] = value
        else:
            LOGGER.debug(
                'Missing entity description for "%s" (please report it!)',
                payload_key,
            )

        return payload

    async def async_publish(self, data: dict[str, DataValueType]) -> None:
        """Publish to MQTT."""
        processed_data = ProcessedData(self.ecowitt, data)
        publish_tasks = []

        for payload_key, data_point in processed_data.output.items():
            discovery_payload = self._generate_discovery_payload(
                processed_data.device, payload_key, data_point
            )

            for topic, payload in (
                (discovery_payload.topic, discovery_payload.payload),
                (
                    discovery_payload.payload["availability_topic"],
                    get_availability_payload(data_point),
                ),
                (discovery_payload.payload["state_topic"], data_point.value),
            ):
                publish_tasks.append(
                    self.client.publish(topic, generate_mqtt_payload(payload))
                )

        async with self.client:
            futures = [asyncio.ensure_future(task) for task in publish_tasks]
            try:
                await asyncio.gather(*futures)
            except MqttError as err:
                for future in futures:
                    future.cancel()
                raise PublishError(
                    f"Error while publishing to Home Assisstant MQTT Discovery: {err}"
                ) from err

        LOGGER.info("Published to Home Assistant MQTT Discovery")
