"""Define common test utilities."""
import asyncio
from contextlib import asynccontextmanager
import json
import os

from ecowitt2mqtt.const import (
    CONF_DEFAULT_BATTERY_STRATEGY,
    CONF_DIAGNOSTICS,
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

TEST_ENDPOINT = "/data/report"
TEST_HASS_DISCOVERY_PREFIX = "homeassistant"
TEST_HASS_ENTITY_ID_PREFIX = "ecowitt"
TEST_MQTT_BROKER = "127.0.0.1"
TEST_MQTT_PASSWORD = "password"
TEST_MQTT_PORT = 1883
TEST_MQTT_TOPIC = "topic/"
TEST_MQTT_USERNAME = "username"
TEST_PORT = 9999

TEST_RAW_JSON = json.dumps(
    {
        CONF_DEFAULT_BATTERY_STRATEGY: "boolean",
        CONF_DIAGNOSTICS: False,
        CONF_ENDPOINT: TEST_ENDPOINT,
        CONF_HASS_DISCOVERY: False,
        CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
        CONF_HASS_ENTITY_ID_PREFIX: TEST_HASS_ENTITY_ID_PREFIX,
        CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
        CONF_MQTT_BROKER: TEST_MQTT_BROKER,
        CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
        CONF_MQTT_PORT: TEST_MQTT_PORT,
        CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
        CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
        CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
        CONF_PORT: TEST_PORT,
        CONF_RAW_DATA: False,
        CONF_VERBOSE: False,
    }
)
TEST_RAW_YAML = f"""
---
{CONF_DEFAULT_BATTERY_STRATEGY}: boolean,
{CONF_DIAGNOSTICS}: false,
{CONF_ENDPOINT}: {TEST_ENDPOINT}
{CONF_HASS_DISCOVERY}: false
{CONF_HASS_DISCOVERY_PREFIX}: {TEST_HASS_DISCOVERY_PREFIX}
{CONF_HASS_ENTITY_ID_PREFIX}: {TEST_HASS_ENTITY_ID_PREFIX}
{CONF_INPUT_UNIT_SYSTEM}: {UNIT_SYSTEM_IMPERIAL}
{CONF_MQTT_BROKER}: {TEST_MQTT_BROKER}
{CONF_MQTT_PASSWORD}: {TEST_MQTT_PASSWORD}
{CONF_MQTT_PORT}: {TEST_MQTT_PORT}
{CONF_MQTT_TOPIC}: {TEST_MQTT_TOPIC}
{CONF_MQTT_USERNAME}: {TEST_MQTT_USERNAME}
{CONF_OUTPUT_UNIT_SYSTEM}: {UNIT_SYSTEM_IMPERIAL}
{CONF_PORT}: {TEST_PORT}
{CONF_RAW_DATA}: false
{CONF_VERBOSE}: false
"""


@asynccontextmanager
async def async_run_server(ecowitt: Ecowitt):
    """Run ecowitt2mqtt."""
    start_task = asyncio.create_task(ecowitt.async_start())
    await asyncio.sleep(0.1)
    try:
        yield
    finally:
        await ecowitt.server.server.shutdown()
        start_task.cancel()
    await asyncio.sleep(0.1)


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
