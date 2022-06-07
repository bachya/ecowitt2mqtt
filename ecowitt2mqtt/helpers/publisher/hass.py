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
    DATA_POINT_FEELSLIKE,
    DATA_POINT_GLOB_BAROM,
    DATA_POINT_GLOB_BATT,
    DATA_POINT_GLOB_GUST,
    DATA_POINT_GLOB_HUMIDITY,
    DATA_POINT_GLOB_MOISTURE,
    DATA_POINT_GLOB_PM10,
    DATA_POINT_GLOB_PM25,
    DATA_POINT_GLOB_RAIN,
    DATA_POINT_GLOB_TEMP,
    DATA_POINT_GLOB_VOLT,
    DATA_POINT_GLOB_WIND,
    DATA_POINT_GLOB_WINDDIR,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HOURLY_RAIN,
    DATA_POINT_HUMI_CO2,
    DATA_POINT_LIGHTNING,
    DATA_POINT_LIGHTNING_NUM,
    DATA_POINT_LIGHTNING_TIME,
    DATA_POINT_MONTHLY_RAIN,
    DATA_POINT_RUNTIME,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_SOLARRADIATION_LUX,
    DATA_POINT_SOLARRADIATION_PERCEIVED,
    DATA_POINT_TF_CO2,
    DATA_POINT_TOTAL_RAIN,
    DATA_POINT_UV,
    DATA_POINT_WEEKLY_RAIN,
    DATA_POINT_WINDCHILL,
    DATA_POINT_YEARLY_RAIN,
    LOGGER,
)
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.errors import EcowittError
from ecowitt2mqtt.helpers.calculator import CalculatedDataPoint
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy, BooleanBatteryState
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


class HassError(EcowittError):
    """Define an error related to a MQTT Discovery error."""

    pass


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

    platform: str
    device_class: str | None = None
    entity_category: str | None = None
    icon: str | None = None
    state_class: str | None = None


@dataclass
class HassDiscoveryPayload:
    """Define a MQTT Discovery configuration for an entity."""

    payload: dict[str, Any]
    topic: str


DATA_POINT_BINARY_BATTERY = "binary_battery"
DATA_POINT_NUMERIC_BATTERY = "numeric_battery"

ENTITY_DESCRIPTIONS = {
    DATA_POINT_BINARY_BATTERY: EntityDescription(
        platform=Platform.BINARY_SENSOR,
        device_class=DeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_BAROM: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.PRESSURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_GUST: EntityDescription(
        platform=Platform.SENSOR,
        icon="mdi:weather-windy",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_HUMIDITY: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.HUMIDITY,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_MOISTURE: EntityDescription(
        platform=Platform.SENSOR,
        icon="mdi:water-percent",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_PM10: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.PM10,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_PM25: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.PM25,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_RAIN: EntityDescription(
        platform=Platform.SENSOR,
        icon="mdi:water",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_TEMP: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_VOLT: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.VOLTAGE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_WIND: EntityDescription(
        platform=Platform.SENSOR,
        icon="mdi:weather-windy",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_GLOB_WINDDIR: EntityDescription(
        platform=Platform.SENSOR,
        icon="mdi:compass",
    ),
    DATA_POINT_CO2: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.CO2,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_CO2_24H: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.CO2,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_DEWPOINT: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_FEELSLIKE: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_HEATINDEX: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_HUMI_CO2: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.HUMIDITY,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_LIGHTNING: EntityDescription(
        platform=Platform.SENSOR,
        icon="mdi:map-marker-distance",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_LIGHTNING_NUM: EntityDescription(
        platform=Platform.SENSOR,
        icon="mdi:weather-lightning",
        state_class=StateClass.TOTAL,
    ),
    DATA_POINT_LIGHTNING_TIME: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.TIMESTAMP,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SOLARRADIATION: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.ILLUMINANCE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SOLARRADIATION_LUX: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.ILLUMINANCE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_SOLARRADIATION_PERCEIVED: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.ILLUMINANCE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_RUNTIME: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.DURATION,
        icon="mdi:timer",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_TF_CO2: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_UV: EntityDescription(
        platform=Platform.SENSOR,
        icon="mdi:weather-sunny",
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_WINDCHILL: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.TEMPERATURE,
        state_class=StateClass.MEASUREMENT,
    ),
    DATA_POINT_NUMERIC_BATTERY: EntityDescription(
        platform=Platform.SENSOR,
        device_class=DeviceClass.VOLTAGE,
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=StateClass.MEASUREMENT,
    ),
}

STATE_CLASS_OVERRIDES = {
    DATA_POINT_DAILY_RAIN: StateClass.TOTAL_INCREASING,
    DATA_POINT_HOURLY_RAIN: StateClass.TOTAL_INCREASING,
    DATA_POINT_MONTHLY_RAIN: StateClass.TOTAL_INCREASING,
    DATA_POINT_TOTAL_RAIN: StateClass.TOTAL_INCREASING,
    DATA_POINT_WEEKLY_RAIN: StateClass.TOTAL_INCREASING,
    DATA_POINT_YEARLY_RAIN: StateClass.TOTAL_INCREASING,
}


class HomeAssistantDiscoveryPublisher(MqttPublisher):
    """Define an MQTT publisher for the MQTT Discovery standard."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        super().__init__(ecowitt)

        self._discovery_payloads: dict[str, HassDiscoveryPayload] = {}

    def _generate_discovery_payload(
        self, device: Device, key: str, data_point: CalculatedDataPoint
    ) -> HassDiscoveryPayload:
        """Generate a discovery payload for an entity."""
        # Since batteries can be either boolean or numeric depending on their
        # strategy, we calculate an entity description at runtime:
        if data_point.data_point_key == DATA_POINT_GLOB_BATT:
            if (
                isinstance(data_point.unit, BooleanBatteryState)
                or self.ecowitt.config.default_battery_strategy
                == BatteryStrategy.BOOLEAN
            ):
                data_point_key = DATA_POINT_BINARY_BATTERY
            else:
                data_point_key = DATA_POINT_NUMERIC_BATTERY
        else:
            data_point_key = data_point.data_point_key

        if (description := ENTITY_DESCRIPTIONS.get(data_point_key)) is None:
            raise HassError("No entity description")

        if self.ecowitt.config.hass_entity_id_prefix:
            name = f"{self.ecowitt.config.hass_entity_id_prefix}_{key}"
        else:
            name = key

        base_topic = (
            f"{self.ecowitt.config.hass_discovery_prefix}/{description.platform}/"
            f"{device.unique_id}/{key}"
        )

        payload = self._discovery_payloads[key] = HassDiscoveryPayload(
            {
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
                "unique_id": f"{device.unique_id}_{key}",
            },
            f"{base_topic}/config",
        )

        for discovery_key, value in (
            ("device_class", description.device_class),
            ("entity_category", description.entity_category),
            ("icon", description.icon),
            ("unit_of_measurement", data_point.unit),
        ):
            if not value:
                continue
            payload.payload[discovery_key] = value

        payload.payload["state_class"] = STATE_CLASS_OVERRIDES.get(
            key, description.state_class
        )

        return payload

    async def async_publish(self, data: dict[str, DataValueType]) -> None:
        """Publish to MQTT."""
        processed_data = ProcessedData(self.ecowitt, data)
        publish_tasks = []

        for key, data_point in processed_data.output.items():
            try:
                discovery_payload = self._generate_discovery_payload(
                    processed_data.device, key, data_point
                )
            except HassError as err:
                LOGGER.warning("Skipping %s due to error: %s", key, err)
                continue

            for topic, payload in (
                (discovery_payload.topic, discovery_payload.payload),
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
