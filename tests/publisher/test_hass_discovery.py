"""Define tests for the Home Assistant MQTT Discovery publisher."""
import logging
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
    CONF_MQTT_USERNAME,
    CONF_OUTPUT_UNIT_SYSTEM,
    UNIT_SYSTEM_IMPERIAL,
)
from ecowitt2mqtt.helpers.publisher import PublishError
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
def test_get_publisher(ecowitt):
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
@pytest.mark.parametrize("device_data_filename", ["payload_gw2000a_2.json"])
async def test_publish(config, device_data, ecowitt, request, setup_asyncio_mqtt):
    """Test publishing a payload."""
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data)

    publisher.client.publish.assert_has_awaits(
        [
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "runtime", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_runtime", "unit_of_measurement": "s", "device_class": "duration", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state",
                b"436796.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "tempin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tempin", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state",
                b"72.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityin", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "baromrel", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromrel", "unit_of_measurement": "inHg", "device_class": "pressure", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state",
                b"29.87",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "baromabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromabs", "unit_of_measurement": "inHg", "device_class": "pressure", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state",
                b"29.509",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state",
                b"65.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "winddir", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_winddir", "unit_of_measurement": "\\u00b0", "icon": "mdi:compass"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state",
                b"327.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windspeed", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windspeed", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state",
                b"2.24",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windgust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windgust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state",
                b"3.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "maxdailygust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_maxdailygust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state",
                b"17.45",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation", "unit_of_measurement": "W/m\\u00b2", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "uv", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_uv", "unit_of_measurement": "UV index", "icon": "mdi:weather-sunny", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", b"0.0"
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "rainrate", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rainrate", "unit_of_measurement": "in/hr", "icon": "mdi:water", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "eventrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_eventrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "hourlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hourlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "dailyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dailyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "weeklyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_weeklyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "monthlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_monthlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state",
                b"0.736",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "yearlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yearlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state",
                b"3.909",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "rrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rrain_piezo", "unit_of_measurement": "in/hr", "icon": "mdi:water", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "erain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_erain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state",
                b"0.063",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "hrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "drain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_drain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "mrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_mrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state",
                b"0.941",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "yrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state",
                b"4.114",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "ws90cap_volt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_ws90cap_volt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state",
                b"5.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp1", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity1", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp2", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity2", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp3", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state",
                b"70.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity3", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp4", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state",
                b"73.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity4", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp5", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state",
                b"70.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity5", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state",
                b"69.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp6", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state",
                b"72.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity6", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp7", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state",
                b"67.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity7", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state",
                b"54.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp8", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state",
                b"68.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity8", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture1", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state",
                b"53.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture2", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state",
                b"57.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture3", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state",
                b"59.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture4", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state",
                b"49.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture5", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state",
                b"52.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_ch1", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state",
                b"21.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_avg_24h_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_avg_24h_ch1", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state",
                b"16.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "tf_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tf_co2", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state",
                b"62.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humi_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humi_co2", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state",
                b"4.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_24h_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state",
                b"7.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm10_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm10", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state",
                b"6.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm10_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_24h_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm10", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state",
                b"7.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2", "unit_of_measurement": "ppm", "device_class": "carbon_dioxide", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state",
                b"455.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2_24h", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_24h", "unit_of_measurement": "ppm", "device_class": "carbon_dioxide", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state",
                b"473.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning_num", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_num", "unit_of_measurement": "strikes", "icon": "mdi:weather-lightning", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state",
                b"13.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning", "unit_of_measurement": "mi", "icon": "mdi:map-marker-distance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state",
                b"0.6",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning_time", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_time", "device_class": "timestamp", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state",
                b"2022-04-20 17:17:17+00:00",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh80batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh80batt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state",
                b"3.28",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt1", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt1", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt2", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt2", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt3", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt3", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt4", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt4", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt5", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt5", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt6", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt6", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt7", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt7", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt8", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt8", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state",
                b"OFF",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt1", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state",
                b"1.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt2", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt3", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt4", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt5", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25batt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25batt1", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh57batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh57batt", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2_batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_batt", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state",
                b"120.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh90batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh90batt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state",
                b"3.22",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "dewpoint", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dewpoint", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state",
                b"47.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "feelslike", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_feelslike", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "heatindex", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_heatindex", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state",
                b"58.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityabs", "unit_of_measurement": "lbs/ft\\u00b3"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityabsin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityabsin", "unit_of_measurement": "lbs/ft\\u00b3"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_1", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_2", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_3", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_4", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_5", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_6", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation_lux", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_lux", "unit_of_measurement": "lx", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation_perceived", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_perceived", "unit_of_measurement": "%", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state",
                b"0.0",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "thermalperception", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_thermalperception", "icon": "mdi:account", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/state",
                b"Dry",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windchill", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windchill", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state",
                b"None",
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
@pytest.mark.parametrize("device_data_filename", ["payload_gw2000a_2.json"])
async def test_publish_custom_entity_id_prefix(
    config, device_data, ecowitt, request, setup_asyncio_mqtt
):
    """Test publishing a payload with custom HASS entity ID prefix."""
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data)

    publisher.client.publish.assert_has_awaits(
        [
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_runtime", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_runtime", "unit_of_measurement": "s", "device_class": "duration", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state",
                b"436796.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_tempin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tempin", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state",
                b"72.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidityin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityin", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_baromrel", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromrel", "unit_of_measurement": "inHg", "device_class": "pressure", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state",
                b"29.87",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_baromabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromabs", "unit_of_measurement": "inHg", "device_class": "pressure", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state",
                b"29.509",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state",
                b"65.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_winddir", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_winddir", "unit_of_measurement": "\\u00b0", "icon": "mdi:compass"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state",
                b"327.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_windspeed", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windspeed", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state",
                b"2.24",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_windgust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windgust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state",
                b"3.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_maxdailygust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_maxdailygust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state",
                b"17.45",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_solarradiation", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation", "unit_of_measurement": "W/m\\u00b2", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_uv", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_uv", "unit_of_measurement": "UV index", "icon": "mdi:weather-sunny", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", b"0.0"
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_rainrate", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rainrate", "unit_of_measurement": "in/hr", "icon": "mdi:water", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_eventrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_eventrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_hourlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hourlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_dailyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dailyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_weeklyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_weeklyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_monthlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_monthlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state",
                b"0.736",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_yearlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yearlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state",
                b"3.909",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_rrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rrain_piezo", "unit_of_measurement": "in/hr", "icon": "mdi:water", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_erain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_erain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state",
                b"0.063",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_hrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_drain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_drain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_wrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_mrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_mrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state",
                b"0.941",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_yrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state",
                b"4.114",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_ws90cap_volt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_ws90cap_volt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state",
                b"5.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp1", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity1", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp2", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity2", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp3", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state",
                b"70.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity3", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp4", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state",
                b"73.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity4", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp5", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state",
                b"70.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity5", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state",
                b"69.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp6", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state",
                b"72.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity6", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp7", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state",
                b"67.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity7", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state",
                b"54.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp8", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state",
                b"68.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity8", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilmoisture1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture1", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state",
                b"53.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilmoisture2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture2", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state",
                b"57.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilmoisture3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture3", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state",
                b"59.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilmoisture4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture4", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state",
                b"49.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilmoisture5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture5", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state",
                b"52.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm25_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_ch1", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state",
                b"21.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm25_avg_24h_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_avg_24h_ch1", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state",
                b"16.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_tf_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tf_co2", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state",
                b"62.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humi_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humi_co2", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm25_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state",
                b"4.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm25_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_24h_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state",
                b"7.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm10_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm10", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state",
                b"6.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm10_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_24h_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm10", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state",
                b"7.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2", "unit_of_measurement": "ppm", "device_class": "carbon_dioxide", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state",
                b"455.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_co2_24h", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_24h", "unit_of_measurement": "ppm", "device_class": "carbon_dioxide", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state",
                b"473.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_lightning_num", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_num", "unit_of_measurement": "strikes", "icon": "mdi:weather-lightning", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state",
                b"13.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_lightning", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning", "unit_of_measurement": "mi", "icon": "mdi:map-marker-distance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state",
                b"0.6",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_lightning_time", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_time", "device_class": "timestamp", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state",
                b"2022-04-20 17:17:17+00:00",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_wh80batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh80batt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state",
                b"3.28",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt1", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt1", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt2", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt2", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt3", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt3", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt4", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt4", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt5", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt5", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt6", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt6", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt7", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt7", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt8", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt8", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state",
                b"OFF",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilbatt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt1", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state",
                b"1.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilbatt2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt2", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilbatt3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt3", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilbatt4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt4", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilbatt5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt5", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm25batt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25batt1", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_wh57batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh57batt", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_co2_batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_batt", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state",
                b"120.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_wh90batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh90batt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state",
                b"3.22",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_dewpoint", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dewpoint", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state",
                b"47.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_feelslike", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_feelslike", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_heatindex", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_heatindex", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state",
                b"58.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidityabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityabs", "unit_of_measurement": "lbs/ft\\u00b3"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidityabsin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityabsin", "unit_of_measurement": "lbs/ft\\u00b3"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_safe_exposure_time_skin_type_1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_1", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_safe_exposure_time_skin_type_2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_2", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_safe_exposure_time_skin_type_3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_3", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_safe_exposure_time_skin_type_4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_4", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_safe_exposure_time_skin_type_5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_5", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_safe_exposure_time_skin_type_6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_6", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_solarradiation_lux", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_lux", "unit_of_measurement": "lx", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_solarradiation_perceived", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_perceived", "unit_of_measurement": "%", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state",
                b"0.0",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_thermalperception", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_thermalperception", "icon": "mdi:account", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/state",
                b"Dry",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_windchill", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windchill", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state",
                b"None",
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
@pytest.mark.parametrize("device_data_filename", ["payload_gw2000a_2.json"])
async def test_publish_numeric_battery_strategy(
    config, device_data, ecowitt, request, setup_asyncio_mqtt
):
    """Test publishing a payload with numeric battery strategy."""
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data)

    publisher.client.publish.assert_has_awaits(
        [
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "runtime", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_runtime", "unit_of_measurement": "s", "device_class": "duration", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state",
                b"436796.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "tempin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tempin", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state",
                b"72.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityin", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "baromrel", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromrel", "unit_of_measurement": "inHg", "device_class": "pressure", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state",
                b"29.87",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "baromabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromabs", "unit_of_measurement": "inHg", "device_class": "pressure", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state",
                b"29.509",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state",
                b"65.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "winddir", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_winddir", "unit_of_measurement": "\\u00b0", "icon": "mdi:compass"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state",
                b"327.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windspeed", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windspeed", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state",
                b"2.24",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windgust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windgust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state",
                b"3.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "maxdailygust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_maxdailygust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state",
                b"17.45",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation", "unit_of_measurement": "W/m\\u00b2", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "uv", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_uv", "unit_of_measurement": "UV index", "icon": "mdi:weather-sunny", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", b"0.0"
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "rainrate", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rainrate", "unit_of_measurement": "in/hr", "icon": "mdi:water", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "eventrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_eventrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "hourlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hourlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "dailyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dailyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "weeklyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_weeklyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "monthlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_monthlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state",
                b"0.736",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "yearlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yearlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state",
                b"3.909",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "rrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rrain_piezo", "unit_of_measurement": "in/hr", "icon": "mdi:water", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "erain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_erain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state",
                b"0.063",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "hrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "drain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_drain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "mrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_mrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state",
                b"0.941",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "yrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state",
                b"4.114",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "ws90cap_volt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_ws90cap_volt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state",
                b"5.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp1", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity1", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp2", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity2", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp3", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state",
                b"70.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity3", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp4", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state",
                b"73.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity4", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp5", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state",
                b"70.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity5", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state",
                b"69.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp6", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state",
                b"72.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity6", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp7", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state",
                b"67.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity7", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state",
                b"54.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp8", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state",
                b"68.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity8", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture1", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state",
                b"53.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture2", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state",
                b"57.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture3", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state",
                b"59.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture4", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state",
                b"49.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture5", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state",
                b"52.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_ch1", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state",
                b"21.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_avg_24h_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_avg_24h_ch1", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state",
                b"16.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "tf_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tf_co2", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state",
                b"62.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humi_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humi_co2", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state",
                b"4.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_24h_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state",
                b"7.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm10_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm10", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state",
                b"6.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm10_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_24h_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm10", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state",
                b"7.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2", "unit_of_measurement": "ppm", "device_class": "carbon_dioxide", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state",
                b"455.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2_24h", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_24h", "unit_of_measurement": "ppm", "device_class": "carbon_dioxide", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state",
                b"473.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning_num", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_num", "unit_of_measurement": "strikes", "icon": "mdi:weather-lightning", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state",
                b"13.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning", "unit_of_measurement": "mi", "icon": "mdi:map-marker-distance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state",
                b"0.6",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning_time", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_time", "device_class": "timestamp", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state",
                b"2022-04-20 17:17:17+00:00",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh80batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh80batt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state",
                b"3.28",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt1", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt2", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt3", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt4", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt5", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt6", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt7", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt8", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt1", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state",
                b"1.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt2", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt3", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt4", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt5", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25batt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25batt1", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh57batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh57batt", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2_batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_batt", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state",
                b"120.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh90batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh90batt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state",
                b"3.22",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "dewpoint", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dewpoint", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state",
                b"47.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "feelslike", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_feelslike", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "heatindex", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_heatindex", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state",
                b"58.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityabs", "unit_of_measurement": "lbs/ft\\u00b3"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityabsin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityabsin", "unit_of_measurement": "lbs/ft\\u00b3"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_1", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_2", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_3", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_4", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_5", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_6", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation_lux", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_lux", "unit_of_measurement": "lx", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation_perceived", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_perceived", "unit_of_measurement": "%", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state",
                b"0.0",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "thermalperception", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_thermalperception", "icon": "mdi:account", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/state",
                b"Dry",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windchill", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windchill", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state",
                b"None",
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
@pytest.mark.parametrize("device_data_filename", ["payload_gw2000a_2.json"])
async def test_publish_error_mqtt(device_data, ecowitt, setup_asyncio_mqtt):
    """Test handling an asyncio-mqtt error when publishing."""
    publisher = get_publisher(ecowitt)
    with patch.object(publisher.client, "publish", side_effect=MqttError):
        with pytest.raises(PublishError):
            await publisher.async_publish(device_data)


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
@pytest.mark.parametrize("device_data_filename", ["payload_gw2000a_2.json"])
async def test_no_entity_description(caplog, device_data, ecowitt, setup_asyncio_mqtt):
    """Test that a key with no entity description is handled."""
    caplog.set_level(logging.DEBUG)

    device_data["random"] = "value"

    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data)

    publisher.client.publish.assert_has_awaits(
        [
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "runtime", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_runtime", "unit_of_measurement": "s", "device_class": "duration", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state",
                b"436796.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "tempin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tempin", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state",
                b"72.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityin", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "baromrel", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromrel", "unit_of_measurement": "inHg", "device_class": "pressure", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state",
                b"29.87",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "baromabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromabs", "unit_of_measurement": "inHg", "device_class": "pressure", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state",
                b"29.509",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state",
                b"65.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "winddir", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_winddir", "unit_of_measurement": "\\u00b0", "icon": "mdi:compass"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state",
                b"327.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windspeed", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windspeed", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state",
                b"2.24",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windgust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windgust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state",
                b"3.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "maxdailygust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_maxdailygust", "unit_of_measurement": "mph", "icon": "mdi:weather-windy", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state",
                b"17.45",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation", "unit_of_measurement": "W/m\\u00b2", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "uv", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_uv", "unit_of_measurement": "UV index", "icon": "mdi:weather-sunny", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", b"0.0"
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "rainrate", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rainrate", "unit_of_measurement": "in/hr", "icon": "mdi:water", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "eventrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_eventrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "hourlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hourlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "dailyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dailyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "weeklyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_weeklyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "monthlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_monthlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state",
                b"0.736",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "yearlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yearlyrain", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state",
                b"3.909",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "rrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rrain_piezo", "unit_of_measurement": "in/hr", "icon": "mdi:water", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "erain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_erain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state",
                b"0.063",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "hrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "drain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_drain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "mrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_mrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state",
                b"0.941",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "yrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yrain_piezo", "unit_of_measurement": "in", "icon": "mdi:water", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state",
                b"4.114",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "ws90cap_volt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_ws90cap_volt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state",
                b"5.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp1", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity1", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp2", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity2", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp3", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state",
                b"70.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity3", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp4", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state",
                b"73.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity4", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp5", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state",
                b"70.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity5", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state",
                b"69.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp6", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state",
                b"72.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity6", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp7", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state",
                b"67.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity7", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state",
                b"54.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp8", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state",
                b"68.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity8", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture1", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state",
                b"53.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture2", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state",
                b"57.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture3", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state",
                b"59.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture4", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state",
                b"49.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture5", "unit_of_measurement": "%", "icon": "mdi:water-percent", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state",
                b"52.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_ch1", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state",
                b"21.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_avg_24h_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_avg_24h_ch1", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state",
                b"16.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "tf_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tf_co2", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state",
                b"62.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humi_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humi_co2", "unit_of_measurement": "%", "device_class": "humidity", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state",
                b"4.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_24h_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm25", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state",
                b"7.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm10_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm10", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state",
                b"6.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm10_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_24h_co2", "unit_of_measurement": "\\u00b5g/m\\u00b3", "device_class": "pm10", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state",
                b"7.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2", "unit_of_measurement": "ppm", "device_class": "carbon_dioxide", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state",
                b"455.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2_24h", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_24h", "unit_of_measurement": "ppm", "device_class": "carbon_dioxide", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state",
                b"473.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning_num", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_num", "unit_of_measurement": "strikes", "icon": "mdi:weather-lightning", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state",
                b"13.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning", "unit_of_measurement": "mi", "icon": "mdi:map-marker-distance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state",
                b"0.6",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning_time", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_time", "device_class": "timestamp", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state",
                b"2022-04-20 17:17:17+00:00",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh80batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh80batt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state",
                b"3.28",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt1", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt1", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt2", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt2", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt3", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt3", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt4", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt4", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt5", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt5", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt6", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt6", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt7", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt7", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt8", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt8", "device_class": "battery", "entity_category": "diagnostic"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state",
                b"OFF",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt1", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state",
                b"1.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt2", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt3", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt4", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt5", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25batt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25batt1", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh57batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh57batt", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2_batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_batt", "unit_of_measurement": "%", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state",
                b"120.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh90batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh90batt", "unit_of_measurement": "V", "device_class": "voltage", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state",
                b"3.22",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/random/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/random/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "random", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/random/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_random"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/random/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/random/state",
                b"value",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "dewpoint", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dewpoint", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state",
                b"47.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "feelslike", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_feelslike", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "heatindex", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_heatindex", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state",
                b"58.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityabs", "unit_of_measurement": "lbs/ft\\u00b3"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabs/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityabsin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityabsin", "unit_of_measurement": "lbs/ft\\u00b3"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityabsin/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_1", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_1/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_2", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_2/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_3", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_3/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_4", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_4/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_5", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_5/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "safe_exposure_time_skin_type_6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_safe_exposure_time_skin_type_6", "unit_of_measurement": "min", "icon": "mdi:timer", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/safe_exposure_time_skin_type_6/state",
                b"None",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation_lux", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_lux", "unit_of_measurement": "lx", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation_perceived", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_perceived", "unit_of_measurement": "%", "device_class": "illuminance", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/availability",
                b"online",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state",
                b"0.0",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/config",
                b'{"availability_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "thermalperception", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_thermalperception", "icon": "mdi:account", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/availability",
                b"online",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/thermalperception/state",
                b"Dry",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/config",
                b'{"availability_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/availability", "device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windchill", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windchill", "unit_of_measurement": "\\u00b0F", "device_class": "temperature", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/availability",
                b"offline",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state",
                b"None",
            ),
        ]
    )

    assert any(
        m for m in caplog.messages if 'Missing entity description for "random"' in m
    )
