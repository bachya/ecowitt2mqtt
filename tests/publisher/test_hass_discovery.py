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
def test_get_publisher(device_data_gw2000a_2, ecowitt):
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
    config, device_data_gw2000a_2, ecowitt, request, setup_asyncio_mqtt
):
    """Test publishing a payload."""
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data_gw2000a_2)

    publisher.client.publish.assert_has_awaits(
        [
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "runtime", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_runtime", "device_class": "duration", "icon": "mdi:timer", "unit_of_measurement": "s", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state",
                b"436796.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "tempin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tempin", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state",
                b"72.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityin", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "baromrel", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromrel", "device_class": "pressure", "unit_of_measurement": "inHg", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state",
                b"29.87",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "baromabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromabs", "device_class": "pressure", "unit_of_measurement": "inHg", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state",
                b"29.509",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state",
                b"65.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "winddir", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_winddir", "icon": "mdi:compass", "unit_of_measurement": "\\u00b0", "state_class": null}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state",
                b"327.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windspeed", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windspeed", "icon": "mdi:weather-windy", "unit_of_measurement": "mph", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state",
                b"2.24",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windgust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windgust", "icon": "mdi:weather-windy", "unit_of_measurement": "mph", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state",
                b"3.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "maxdailygust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_maxdailygust", "icon": "mdi:weather-windy", "unit_of_measurement": "mph", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state",
                b"17.45",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation", "device_class": "illuminance", "unit_of_measurement": "W/m\\u00b2", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "uv", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_uv", "icon": "mdi:weather-sunny", "unit_of_measurement": "UV index", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", b"0.0"
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "rainrate", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rainrate", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "eventrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_eventrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "hourlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hourlyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "dailyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dailyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "weeklyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_weeklyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "monthlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_monthlyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state",
                b"0.736",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "yearlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yearlyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state",
                b"3.909",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "rrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "erain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_erain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state",
                b"0.063",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "hrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "drain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_drain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "mrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_mrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state",
                b"0.941",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "yrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state",
                b"4.114",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "ws90cap_volt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_ws90cap_volt", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state",
                b"5.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp1", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity1", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp2", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity2", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp3", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state",
                b"70.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity3", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp4", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state",
                b"73.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity4", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp5", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state",
                b"70.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity5", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state",
                b"69.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp6", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state",
                b"72.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity6", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp7", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state",
                b"67.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity7", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state",
                b"54.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp8", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state",
                b"68.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity8", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture1", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state",
                b"53.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture2", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state",
                b"57.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture3", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state",
                b"59.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture4", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state",
                b"49.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture5", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state",
                b"52.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_ch1", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state",
                b"21.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_avg_24h_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_avg_24h_ch1", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state",
                b"16.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "tf_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tf_co2", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state",
                b"62.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humi_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humi_co2", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_co2", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state",
                b"4.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_24h_co2", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state",
                b"7.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm10_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_co2", "device_class": "pm10", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state",
                b"6.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm10_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_24h_co2", "device_class": "pm10", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state",
                b"7.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2", "device_class": "carbon_dioxide", "unit_of_measurement": "ppm", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state",
                b"455.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2_24h", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_24h", "device_class": "carbon_dioxide", "unit_of_measurement": "ppm", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state",
                b"473.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning_num", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_num", "icon": "mdi:weather-lightning", "unit_of_measurement": "strikes", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state",
                b"13.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning", "icon": "mdi:map-marker-distance", "unit_of_measurement": "mi", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state",
                b"1.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning_time", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_time", "device_class": "timestamp", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state",
                b"2022-04-20 17:17:17+00:00",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh80batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh80batt", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state",
                b"3.28",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt1", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt1", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt2", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt2", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt3", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt3", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt4", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt4", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt5", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt5", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt6", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt6", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt7", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt7", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt8", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt8", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state",
                b"OFF",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt1", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state",
                b"1.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt2", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt3", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt4", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt5", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25batt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25batt1", "device_class": "battery", "entity_category": "diagnostic", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh57batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh57batt", "device_class": "battery", "entity_category": "diagnostic", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2_batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_batt", "device_class": "battery", "entity_category": "diagnostic", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state",
                b"120.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh90batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh90batt", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state",
                b"3.22",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "dewpoint", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dewpoint", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state",
                b"47.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "feelslike", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_feelslike", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "heatindex", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_heatindex", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state",
                b"58.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation_lux", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_lux", "device_class": "illuminance", "unit_of_measurement": "lx", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation_perceived", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_perceived", "device_class": "illuminance", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windchill", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windchill", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
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
async def test_publish_custom_entity_id_prefix(
    config, device_data_gw2000a_2, ecowitt, request, setup_asyncio_mqtt
):
    """Test publishing a payload with custom HASS entity ID prefix."""
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data_gw2000a_2)

    publisher.client.publish.assert_has_awaits(
        [
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_runtime", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_runtime", "device_class": "duration", "icon": "mdi:timer", "unit_of_measurement": "s", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state",
                b"436796.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_tempin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tempin", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state",
                b"72.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidityin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityin", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_baromrel", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromrel", "device_class": "pressure", "unit_of_measurement": "inHg", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state",
                b"29.87",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_baromabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromabs", "device_class": "pressure", "unit_of_measurement": "inHg", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state",
                b"29.509",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state",
                b"65.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_winddir", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_winddir", "icon": "mdi:compass", "unit_of_measurement": "\\u00b0", "state_class": null}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state",
                b"327.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_windspeed", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windspeed", "icon": "mdi:weather-windy", "unit_of_measurement": "mph", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state",
                b"2.24",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_windgust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windgust", "icon": "mdi:weather-windy", "unit_of_measurement": "mph", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state",
                b"3.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_maxdailygust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_maxdailygust", "icon": "mdi:weather-windy", "unit_of_measurement": "mph", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state",
                b"17.45",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_solarradiation", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation", "device_class": "illuminance", "unit_of_measurement": "W/m\\u00b2", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_uv", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_uv", "icon": "mdi:weather-sunny", "unit_of_measurement": "UV index", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", b"0.0"
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_rainrate", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rainrate", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_eventrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_eventrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_hourlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hourlyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_dailyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dailyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_weeklyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_weeklyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_monthlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_monthlyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state",
                b"0.736",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_yearlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yearlyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state",
                b"3.909",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_rrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_erain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_erain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state",
                b"0.063",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_hrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_drain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_drain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_wrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_mrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_mrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state",
                b"0.941",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_yrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state",
                b"4.114",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_ws90cap_volt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_ws90cap_volt", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state",
                b"5.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp1", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity1", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp2", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity2", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp3", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state",
                b"70.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity3", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp4", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state",
                b"73.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity4", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp5", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state",
                b"70.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity5", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state",
                b"69.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp6", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state",
                b"72.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity6", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp7", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state",
                b"67.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity7", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state",
                b"54.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_temp8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp8", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state",
                b"68.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humidity8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity8", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilmoisture1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture1", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state",
                b"53.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilmoisture2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture2", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state",
                b"57.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilmoisture3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture3", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state",
                b"59.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilmoisture4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture4", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state",
                b"49.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilmoisture5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture5", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state",
                b"52.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm25_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_ch1", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state",
                b"21.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm25_avg_24h_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_avg_24h_ch1", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state",
                b"16.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_tf_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tf_co2", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state",
                b"62.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_humi_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humi_co2", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm25_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_co2", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state",
                b"4.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm25_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_24h_co2", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state",
                b"7.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm10_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_co2", "device_class": "pm10", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state",
                b"6.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm10_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_24h_co2", "device_class": "pm10", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state",
                b"7.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2", "device_class": "carbon_dioxide", "unit_of_measurement": "ppm", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state",
                b"455.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_co2_24h", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_24h", "device_class": "carbon_dioxide", "unit_of_measurement": "ppm", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state",
                b"473.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_lightning_num", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_num", "icon": "mdi:weather-lightning", "unit_of_measurement": "strikes", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state",
                b"13.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_lightning", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning", "icon": "mdi:map-marker-distance", "unit_of_measurement": "mi", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state",
                b"1.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_lightning_time", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_time", "device_class": "timestamp", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state",
                b"2022-04-20 17:17:17+00:00",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_wh80batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh80batt", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state",
                b"3.28",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt1", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt1", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt2", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt2", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt3", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt3", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt4", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt4", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt5", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt5", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt6", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt6", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt7", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt7", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_batt8", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt8", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state",
                b"OFF",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilbatt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt1", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state",
                b"1.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilbatt2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt2", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilbatt3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt3", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilbatt4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt4", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_soilbatt5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt5", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_pm25batt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25batt1", "device_class": "battery", "entity_category": "diagnostic", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_wh57batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh57batt", "device_class": "battery", "entity_category": "diagnostic", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_co2_batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_batt", "device_class": "battery", "entity_category": "diagnostic", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state",
                b"120.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_wh90batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh90batt", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state",
                b"3.22",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_dewpoint", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dewpoint", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state",
                b"47.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_feelslike", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_feelslike", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_heatindex", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_heatindex", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state",
                b"58.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_solarradiation_lux", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_lux", "device_class": "illuminance", "unit_of_measurement": "lx", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_solarradiation_perceived", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_perceived", "device_class": "illuminance", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "test_prefix_windchill", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windchill", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
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
async def test_publish_numeric_battery_strategy(
    config, device_data_gw2000a_2, ecowitt, request, setup_asyncio_mqtt
):
    """Test publishing a payload with numeric battery strategy."""
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data_gw2000a_2)

    publisher.client.publish.assert_has_awaits(
        [
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "runtime", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_runtime", "device_class": "duration", "icon": "mdi:timer", "unit_of_measurement": "s", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/runtime/state",
                b"436796.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "tempin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tempin", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tempin/state",
                b"72.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidityin", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidityin", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidityin/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "baromrel", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromrel", "device_class": "pressure", "unit_of_measurement": "inHg", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromrel/state",
                b"29.87",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "baromabs", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_baromabs", "device_class": "pressure", "unit_of_measurement": "inHg", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/baromabs/state",
                b"29.509",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity/state",
                b"65.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "winddir", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_winddir", "icon": "mdi:compass", "unit_of_measurement": "\\u00b0", "state_class": null}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/winddir/state",
                b"327.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windspeed", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windspeed", "icon": "mdi:weather-windy", "unit_of_measurement": "mph", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windspeed/state",
                b"2.24",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windgust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windgust", "icon": "mdi:weather-windy", "unit_of_measurement": "mph", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windgust/state",
                b"3.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "maxdailygust", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_maxdailygust", "icon": "mdi:weather-windy", "unit_of_measurement": "mph", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/maxdailygust/state",
                b"17.45",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation", "device_class": "illuminance", "unit_of_measurement": "W/m\\u00b2", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "uv", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_uv", "icon": "mdi:weather-sunny", "unit_of_measurement": "UV index", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/uv/state", b"0.0"
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "rainrate", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rainrate", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rainrate/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "eventrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_eventrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/eventrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "hourlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hourlyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hourlyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "dailyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dailyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dailyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "weeklyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_weeklyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/weeklyrain/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "monthlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_monthlyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/monthlyrain/state",
                b"0.736",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "yearlyrain", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yearlyrain", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "total_increasing"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yearlyrain/state",
                b"3.909",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "rrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_rrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/rrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "erain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_erain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/erain_piezo/state",
                b"0.063",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "hrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_hrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/hrain_piezo/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "drain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_drain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/drain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wrain_piezo/state",
                b"0.075",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "mrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_mrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/mrain_piezo/state",
                b"0.941",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "yrain_piezo", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_yrain_piezo", "icon": "mdi:water", "unit_of_measurement": "in", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/yrain_piezo/state",
                b"4.114",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "ws90cap_volt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_ws90cap_volt", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/ws90cap_volt/state",
                b"5.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp1", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp1/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity1", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity1/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp2", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp2/state",
                b"71.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity2", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity2/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp3", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp3/state",
                b"70.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity3", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity3/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp4", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp4/state",
                b"73.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity4", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity4/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp5", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp5/state",
                b"70.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity5", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity5/state",
                b"69.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp6", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp6/state",
                b"72.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity6", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity6", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity6/state",
                b"58.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp7", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp7/state",
                b"67.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity7", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity7", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity7/state",
                b"54.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "temp8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_temp8", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/temp8/state",
                b"68.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humidity8", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humidity8", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humidity8/state",
                b"56.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture1", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture1/state",
                b"53.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture2", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture2/state",
                b"57.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture3", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture3/state",
                b"59.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture4", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture4/state",
                b"49.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilmoisture5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilmoisture5", "icon": "mdi:water-percent", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilmoisture5/state",
                b"52.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_ch1", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_ch1/state",
                b"21.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_avg_24h_ch1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_avg_24h_ch1", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_avg_24h_ch1/state",
                b"16.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "tf_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_tf_co2", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/tf_co2/state",
                b"62.2",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "humi_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_humi_co2", "device_class": "humidity", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/humi_co2/state",
                b"61.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_co2", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_co2/state",
                b"4.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25_24h_co2", "device_class": "pm25", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25_24h_co2/state",
                b"7.5",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm10_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_co2", "device_class": "pm10", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_co2/state",
                b"6.1",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm10_24h_co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm10_24h_co2", "device_class": "pm10", "unit_of_measurement": "\\u00b5g/m\\u00b3", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm10_24h_co2/state",
                b"7.8",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2", "device_class": "carbon_dioxide", "unit_of_measurement": "ppm", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2/state",
                b"455.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2_24h", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_24h", "device_class": "carbon_dioxide", "unit_of_measurement": "ppm", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_24h/state",
                b"473.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning_num", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_num", "icon": "mdi:weather-lightning", "unit_of_measurement": "strikes", "state_class": "total"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_num/state",
                b"13.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning", "icon": "mdi:map-marker-distance", "unit_of_measurement": "mi", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning/state",
                b"1.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "lightning_time", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_lightning_time", "device_class": "timestamp", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/lightning_time/state",
                b"2022-04-20 17:17:17+00:00",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh80batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh80batt", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh80batt/state",
                b"3.28",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt1", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt1", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt1/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt2", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt2", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt2/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt3", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt3", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt3/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt4", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt4", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt4/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt5", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt5", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt5/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt6", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt6", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt6/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt7", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt7", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt7/state",
                b"OFF",
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "batt8", "qos": 1, "state_topic": "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_batt8", "device_class": "battery", "entity_category": "diagnostic", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/binary_sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/batt8/state",
                b"OFF",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt1", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt1/state",
                b"1.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt2", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt2", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt2/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt3", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt3", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt3/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt4", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt4", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt4/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "soilbatt5", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_soilbatt5", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/soilbatt5/state",
                b"1.3",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "pm25batt1", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_pm25batt1", "device_class": "battery", "entity_category": "diagnostic", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/pm25batt1/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh57batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh57batt", "device_class": "battery", "entity_category": "diagnostic", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh57batt/state",
                b"60.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "co2_batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_co2_batt", "device_class": "battery", "entity_category": "diagnostic", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/co2_batt/state",
                b"120.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "wh90batt", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_wh90batt", "device_class": "voltage", "entity_category": "diagnostic", "unit_of_measurement": "V", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/wh90batt/state",
                b"3.22",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "dewpoint", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_dewpoint", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/dewpoint/state",
                b"47.9",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "feelslike", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_feelslike", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/feelslike/state",
                b"59.7",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "heatindex", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_heatindex", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/heatindex/state",
                b"58.4",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation_lux", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_lux", "device_class": "illuminance", "unit_of_measurement": "lx", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_lux/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "solarradiation_perceived", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_solarradiation_perceived", "device_class": "illuminance", "unit_of_measurement": "%", "state_class": "measurement"}',
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/solarradiation_perceived/state",
                b"0.0",
            ),
            call(
                "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/config",
                b'{"device": {"identifiers": ["xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"], "manufacturer": "Ecowitt", "model": "GW2000A", "name": "GW2000A", "sw_version": "GW2000A_V2.1.4"}, "name": "windchill", "qos": 1, "state_topic": "homeassistant/sensor/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/windchill/state", "unique_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_windchill", "device_class": "temperature", "unit_of_measurement": "\\u00b0F", "state_class": "measurement"}',
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
async def test_publish_error_mqtt(device_data_gw2000a_2, ecowitt, setup_asyncio_mqtt):
    """Test handling an asyncio-mqtt error when publishing."""
    publisher = get_publisher(ecowitt)
    with patch.object(publisher.client, "publish", side_effect=MqttError):
        with pytest.raises(PublishError):
            await publisher.async_publish(device_data_gw2000a_2)


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
async def test_unknown_key(caplog, device_data_gw2000a_2, ecowitt, setup_asyncio_mqtt):
    """Test that a key with no entity description is handled."""
    device_data_gw2000a_2["random"] = "value"
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data_gw2000a_2)
    assert any(m for m in caplog.messages if 'Skipping "random" due to error' in m)
