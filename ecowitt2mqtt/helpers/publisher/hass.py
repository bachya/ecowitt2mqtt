"""Define MQTT publishing."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypedDict

from asyncio_mqtt import MqttError

from ecowitt2mqtt.const import (
    DATA_POINT_CO2,
    DATA_POINT_CO2_24H,
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
    DATA_POINT_HUMI_CO2,
    DATA_POINT_LIGHTNING,
    DATA_POINT_LIGHTNING_NUM,
    DATA_POINT_LIGHTNING_TIME,
    DATA_POINT_RUNTIME,
    DATA_POINT_SOLARRADIATION,
    DATA_POINT_SOLARRADIATION_LUX,
    DATA_POINT_SOLARRADIATION_PERCEIVED,
    DATA_POINT_TF_CO2,
    DATA_POINT_UV,
    DATA_POINT_WINDCHILL,
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

DEVICE_CLASS_BATTERY = "battery"
DEVICE_CLASS_CO2 = "carbon_dioxide"
DEVICE_CLASS_DURATION = "duration"
DEVICE_CLASS_HUMIDITY = "humidity"
DEVICE_CLASS_ILLUMINANCE = "illuminance"
DEVICE_CLASS_PM10 = "pm10"
DEVICE_CLASS_PM25 = "pm25"
DEVICE_CLASS_PRESSURE = "pressure"
DEVICE_CLASS_TEMPERATURE = "temperature"
DEVICE_CLASS_TIMESTAMP = "timestamp"
DEVICE_CLASS_VOLTAGE = "voltage"

ENTITY_CATEGORY_DIAGNOSTIC = "diagnostic"

PLATFORM_BINARY_SENSOR = "binary_sensor"
PLATFORM_SENSOR = "sensor"


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


@dataclass
class HassDiscoveryPayload:
    """Define a MQTT Discovery configuration for an entity."""

    payload: dict[str, Any]
    topic: str


DATA_POINT_BINARY_BATTERY = "binary_battery"
DATA_POINT_NUMERIC_BATTERY = "numeric_battery"

ENTITY_DESCRIPTIONS = {
    DATA_POINT_BINARY_BATTERY: EntityDescription(
        platform=PLATFORM_BINARY_SENSOR,
        device_class=DEVICE_CLASS_BATTERY,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
    DATA_POINT_GLOB_BAROM: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_PRESSURE,
    ),
    DATA_POINT_GLOB_GUST: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-windy",
    ),
    DATA_POINT_GLOB_HUMIDITY: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_HUMIDITY,
    ),
    DATA_POINT_GLOB_MOISTURE: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:water-percent",
    ),
    DATA_POINT_GLOB_PM10: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_PM10,
    ),
    DATA_POINT_GLOB_PM25: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_PM25,
    ),
    DATA_POINT_GLOB_RAIN: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:water",
    ),
    DATA_POINT_GLOB_TEMP: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    DATA_POINT_GLOB_VOLT: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_VOLTAGE,
    ),
    DATA_POINT_GLOB_WIND: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-windy",
    ),
    DATA_POINT_GLOB_WINDDIR: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:compass",
    ),
    DATA_POINT_CO2: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_CO2,
    ),
    DATA_POINT_CO2_24H: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_CO2,
    ),
    DATA_POINT_DEWPOINT: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    DATA_POINT_FEELSLIKE: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    DATA_POINT_HEATINDEX: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    DATA_POINT_HUMI_CO2: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_HUMIDITY,
    ),
    DATA_POINT_LIGHTNING: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:map-marker-distance",
    ),
    DATA_POINT_LIGHTNING_NUM: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-lightning",
    ),
    DATA_POINT_LIGHTNING_TIME: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TIMESTAMP,
    ),
    DATA_POINT_SOLARRADIATION: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_ILLUMINANCE,
    ),
    DATA_POINT_SOLARRADIATION_LUX: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_ILLUMINANCE,
    ),
    DATA_POINT_SOLARRADIATION_PERCEIVED: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_ILLUMINANCE,
    ),
    DATA_POINT_RUNTIME: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_DURATION,
        icon="mdi:timer",
    ),
    DATA_POINT_TF_CO2: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    DATA_POINT_UV: EntityDescription(
        platform=PLATFORM_SENSOR,
        icon="mdi:weather-sunny",
    ),
    DATA_POINT_WINDCHILL: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_TEMPERATURE,
    ),
    DATA_POINT_NUMERIC_BATTERY: EntityDescription(
        platform=PLATFORM_SENSOR,
        device_class=DEVICE_CLASS_VOLTAGE,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
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

        try:
            async with self.client:
                await asyncio.gather(
                    *[asyncio.ensure_future(task) for task in publish_tasks]
                )
        except MqttError as err:
            for task in publish_tasks:
                task.cancel()
            raise PublishError(
                f"Error while publishing to Home Assisstant MQTT Discovery: {err}"
            ) from err

        LOGGER.info("Published to Home Assistant MQTT Discovery")
