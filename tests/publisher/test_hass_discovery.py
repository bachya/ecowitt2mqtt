"""Define tests for the Home Assistant MQTT Discovery publisher."""
from unittest.mock import call, patch

from asyncio_mqtt import MqttError
import pytest

from ecowitt2mqtt.const import (
    CONF_DEFAULT_BATTERY_STRATEGY,
    CONF_ENDPOINT,
    CONF_HASS_DISCOVERY,
    CONF_HASS_DISCOVERY_PREFIX,
    CONF_HASS_ENTITY_ID_PREFIX,
    CONF_INPUT_UNIT_SYSTEM,
    CONF_MQTT_BROKER,
    CONF_MQTT_PASSWORD,
    CONF_MQTT_PORT,
    CONF_MQTT_TOPIC,
    CONF_MQTT_USERNAME,
    CONF_OUTPUT_UNIT_SYSTEM,
    CONF_PORT,
    CONF_RAW_DATA,
    CONF_VERBOSE,
    UNIT_SYSTEM_IMPERIAL,
)
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy
from ecowitt2mqtt.helpers.publisher import PublishError, generate_mqtt_payload
from ecowitt2mqtt.helpers.publisher.factory import get_publisher
from ecowitt2mqtt.helpers.publisher.hass import HomeAssistantDiscoveryPublisher

from tests.common import (
    TEST_ENDPOINT,
    TEST_HASS_DISCOVERY_PREFIX,
    TEST_MQTT_BROKER,
    TEST_MQTT_PASSWORD,
    TEST_MQTT_PORT,
    TEST_MQTT_USERNAME,
)


@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: True,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
        }
    ],
)
def test_get_publisher(device_data_gw1000pro, ecowitt):
    """Test getting a publisher via the factory."""
    publisher = get_publisher(ecowitt)
    assert isinstance(publisher, HomeAssistantDiscoveryPublisher)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_DEFAULT_BATTERY_STRATEGY: "boolean",
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: True,
            CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
            CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
            CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
        }
    ],
)
async def test_publish(
    config, device_data_gw1000bpro, ecowitt, request, setup_asyncio_mqtt
):
    """Test publishing a payload."""
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data_gw1000bpro)

    publisher.client.publish.assert_has_awaits(
        [
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "runtime", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_runtime", "unit_of_measurement": "s", "device_class": "duration", "icon": "mdi:timer"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state",
                b"319206.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "tempin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tempin", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state",
                b"79.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "humidityin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityin", "unit_of_measurement": "%", "device_class": "humidity"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state",
                b"31.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "baromrel", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromrel", "unit_of_measurement": "inHg", "device_class": "pressure"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state",
                b"24.74",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "baromabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromabs", "unit_of_measurement": "inHg", "device_class": "pressure"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state",
                b"24.74",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "temp", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state",
                b"19.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "humidity", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity", "unit_of_measurement": "%", "device_class": "humidity"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state",
                b"34.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "winddir", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_winddir", "unit_of_measurement": "\\u00b0", "icon": "mdi:compass"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state",
                b"139.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "windspeed", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windspeed", "unit_of_measurement": "mph", "icon": "mdi:weather-windy"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state",
                b"20.89",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "windgust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windgust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state",
                b"1.12",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "maxdailygust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_maxdailygust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state",
                b"8.05",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "solarradiation", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation", "unit_of_measurement": "W/m\\u00b2", "device_class": "illuminance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state",
                b"264.61",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "uv", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_uv", "unit_of_measurement": "UV index", "icon": "mdi:weather-sunny"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", b"2.0"
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "rainrate", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rainrate", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "eventrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_eventrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "hourlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hourlyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "dailyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dailyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "weeklyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_weeklyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "monthlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_monthlyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state",
                b"2.177",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "yearlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yearlyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state",
                b"4.441",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "lightning_num", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_num", "unit_of_measurement": "strikes", "icon": "mdi:weather-lightning"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state",
                b"13.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "lightning", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning", "unit_of_measurement": "mi", "icon": "mdi:map-marker-distance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state",
                b"1.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "lightning_time", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_time", "device_class": "timestamp"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state",
                b"2022-04-20 17:17:17+00:00",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh65batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "wh65batt", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh65batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh65batt", "device_class": "battery"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh65batt/state",
                b"OFF",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "dewpoint", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dewpoint", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state",
                b"-4.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "feelslike", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_feelslike", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state",
                b"2.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "heatindex", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_heatindex", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state",
                b"12.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "solarradiation_lux", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_lux", "unit_of_measurement": "lx", "device_class": "illuminance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state",
                b"33494.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "solarradiation_perceived", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_perceived", "unit_of_measurement": "%", "device_class": "illuminance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state",
                b"90.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "windchill", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windchill", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state",
                b"2.7",
            ),
        ]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_DEFAULT_BATTERY_STRATEGY: "boolean",
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: True,
            CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
            CONF_HASS_ENTITY_ID_PREFIX: "test_prefix",
            CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
            CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
        }
    ],
)
async def test_publish_custom_entity_id_prefix(
    config, device_data_gw1000bpro, ecowitt, request, setup_asyncio_mqtt
):
    """Test publishing a payload with custom HASS entity ID prefix."""
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data_gw1000bpro)

    publisher.client.publish.assert_has_awaits(
        [
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_runtime", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_runtime", "unit_of_measurement": "s", "device_class": "duration", "icon": "mdi:timer"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state",
                b"319206.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_tempin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tempin", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state",
                b"79.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_humidityin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityin", "unit_of_measurement": "%", "device_class": "humidity"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state",
                b"31.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_baromrel", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromrel", "unit_of_measurement": "inHg", "device_class": "pressure"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state",
                b"24.74",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_baromabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromabs", "unit_of_measurement": "inHg", "device_class": "pressure"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state",
                b"24.74",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_temp", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state",
                b"19.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_humidity", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity", "unit_of_measurement": "%", "device_class": "humidity"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state",
                b"34.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_winddir", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_winddir", "unit_of_measurement": "\\u00b0", "icon": "mdi:compass"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state",
                b"139.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_windspeed", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windspeed", "unit_of_measurement": "mph", "icon": "mdi:weather-windy"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state",
                b"20.89",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_windgust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windgust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state",
                b"1.12",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_maxdailygust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_maxdailygust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state",
                b"8.05",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_solarradiation", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation", "unit_of_measurement": "W/m\\u00b2", "device_class": "illuminance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state",
                b"264.61",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_uv", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_uv", "unit_of_measurement": "UV index", "icon": "mdi:weather-sunny"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", b"2.0"
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_rainrate", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rainrate", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_eventrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_eventrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_hourlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hourlyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_dailyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dailyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_weeklyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_weeklyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_monthlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_monthlyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state",
                b"2.177",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_yearlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yearlyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state",
                b"4.441",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_lightning_num", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_num", "unit_of_measurement": "strikes", "icon": "mdi:weather-lightning"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state",
                b"13.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_lightning", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning", "unit_of_measurement": "mi", "icon": "mdi:map-marker-distance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state",
                b"1.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_lightning_time", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_time", "device_class": "timestamp"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state",
                b"2022-04-20 17:17:17+00:00",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh65batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_wh65batt", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh65batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh65batt", "device_class": "battery"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh65batt/state",
                b"OFF",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_dewpoint", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dewpoint", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state",
                b"-4.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_feelslike", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_feelslike", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state",
                b"2.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_heatindex", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_heatindex", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state",
                b"12.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_solarradiation_lux", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_lux", "unit_of_measurement": "lx", "device_class": "illuminance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state",
                b"33494.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_solarradiation_perceived", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_perceived", "unit_of_measurement": "%", "device_class": "illuminance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state",
                b"90.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "test_prefix_windchill", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windchill", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state",
                b"2.7",
            ),
        ]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_DEFAULT_BATTERY_STRATEGY: "numeric",
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: True,
            CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
            CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
            CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
        }
    ],
)
async def test_publish_numeric_battery_strategy(
    config, device_data_gw1000bpro, ecowitt, request, setup_asyncio_mqtt
):
    """Test publishing a payload with numeric battery strategy."""
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data_gw1000bpro)

    publisher.client.publish.assert_has_awaits(
        [
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "runtime", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_runtime", "unit_of_measurement": "s", "device_class": "duration", "icon": "mdi:timer"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state",
                b"319206.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "tempin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tempin", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state",
                b"79.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "humidityin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityin", "unit_of_measurement": "%", "device_class": "humidity"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state",
                b"31.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "baromrel", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromrel", "unit_of_measurement": "inHg", "device_class": "pressure"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state",
                b"24.74",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "baromabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromabs", "unit_of_measurement": "inHg", "device_class": "pressure"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state",
                b"24.74",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "temp", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state",
                b"19.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "humidity", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity", "unit_of_measurement": "%", "device_class": "humidity"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state",
                b"34.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "winddir", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_winddir", "unit_of_measurement": "\\u00b0", "icon": "mdi:compass"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state",
                b"139.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "windspeed", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windspeed", "unit_of_measurement": "mph", "icon": "mdi:weather-windy"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state",
                b"20.89",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "windgust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windgust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state",
                b"1.12",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "maxdailygust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_maxdailygust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state",
                b"8.05",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "solarradiation", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation", "unit_of_measurement": "W/m\\u00b2", "device_class": "illuminance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state",
                b"264.61",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "uv", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_uv", "unit_of_measurement": "UV index", "icon": "mdi:weather-sunny"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", b"2.0"
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "rainrate", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rainrate", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "eventrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_eventrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "hourlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hourlyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "dailyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dailyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "weeklyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_weeklyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "monthlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_monthlyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state",
                b"2.177",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "yearlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yearlyrain", "unit_of_measurement": "in", "icon": "mdi:water"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state",
                b"4.441",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "lightning_num", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_num", "unit_of_measurement": "strikes", "icon": "mdi:weather-lightning"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state",
                b"13.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "lightning", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning", "unit_of_measurement": "mi", "icon": "mdi:map-marker-distance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state",
                b"1.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "lightning_time", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_time", "device_class": "timestamp"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state",
                b"2022-04-20 17:17:17+00:00",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh65batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "wh65batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh65batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh65batt", "unit_of_measurement": "V", "device_class": "voltage"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh65batt/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "dewpoint", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dewpoint", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state",
                b"-4.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "feelslike", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_feelslike", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state",
                b"2.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "heatindex", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_heatindex", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state",
                b"12.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "solarradiation_lux", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_lux", "unit_of_measurement": "lx", "device_class": "illuminance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state",
                b"33494.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "solarradiation_perceived", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_perceived", "unit_of_measurement": "%", "device_class": "illuminance"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state",
                b"90.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW1000", "name": "GW1000", "sw_version": "GW1000B_V1.7.3"}, "name": "windchill", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windchill", "unit_of_measurement": "\\u00b0F", "device_class": "temperature"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state",
                b"2.7",
            ),
        ]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_DEFAULT_BATTERY_STRATEGY: "boolean",
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: True,
            CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
            CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
            CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
        }
    ],
)
async def test_publish_error_mqtt(device_data_gw1000pro, ecowitt):
    """Test handling an asyncio-mqtt error when publishing."""
    publisher = get_publisher(ecowitt)
    with patch.object(publisher.client, "publish", side_effect=MqttError):
        with pytest.raises(PublishError):
            await publisher.async_publish(device_data_gw1000pro)
