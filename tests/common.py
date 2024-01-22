"""Define common test utilities."""
import os

from ecowitt2mqtt.const import (
    CONF_BOOLEAN_BATTERY_TRUE_VALUE,
    CONF_DEFAULT_BATTERY_STRATEGY,
    CONF_DIAGNOSTICS,
    CONF_DISABLE_CALCULATED_DATA,
    CONF_ENDPOINT,
    CONF_HASS_DISCOVERY,
    CONF_HASS_DISCOVERY_PREFIX,
    CONF_HASS_ENTITY_ID_PREFIX,
    CONF_INPUT_DATA_FORMAT,
    CONF_INPUT_UNIT_SYSTEM,
    CONF_MQTT_BROKER,
    CONF_MQTT_PASSWORD,
    CONF_MQTT_PORT,
    CONF_MQTT_RETAIN,
    CONF_MQTT_TLS,
    CONF_MQTT_TOPIC,
    CONF_MQTT_USERNAME,
    CONF_OUTPUT_UNIT_SYSTEM,
    CONF_PORT,
    CONF_RAW_DATA,
    CONF_VERBOSE,
    UnitSystem,
)
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy
from ecowitt2mqtt.helpers.server import InputDataFormat

TEST_ENDPOINT = "/data/report"
TEST_HASS_DISCOVERY_PREFIX = "homeassistant"
TEST_HASS_ENTITY_ID_PREFIX = "test_prefix"
TEST_MQTT_BROKER = "127.0.0.1"
TEST_MQTT_PASSWORD = "password"  # noqa: S105
TEST_MQTT_PORT = 1883
TEST_MQTT_TOPIC = "topic/"
TEST_MQTT_USERNAME = "username"
TEST_PORT = 9999

TEST_CONFIG_JSON = {
    CONF_BOOLEAN_BATTERY_TRUE_VALUE: 1,
    CONF_DEFAULT_BATTERY_STRATEGY: BatteryStrategy.BOOLEAN,
    CONF_DIAGNOSTICS: False,
    CONF_DISABLE_CALCULATED_DATA: False,
    CONF_ENDPOINT: TEST_ENDPOINT,
    CONF_HASS_DISCOVERY: False,
    CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
    CONF_HASS_ENTITY_ID_PREFIX: None,
    CONF_INPUT_DATA_FORMAT: InputDataFormat.ECOWITT,
    CONF_INPUT_UNIT_SYSTEM: UnitSystem.IMPERIAL,
    CONF_MQTT_BROKER: TEST_MQTT_BROKER,
    CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
    CONF_MQTT_PORT: TEST_MQTT_PORT,
    CONF_MQTT_RETAIN: False,
    CONF_MQTT_TLS: False,
    CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
    CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
    CONF_OUTPUT_UNIT_SYSTEM: UnitSystem.IMPERIAL,
    CONF_PORT: TEST_PORT,
    CONF_RAW_DATA: False,
    CONF_VERBOSE: False,
}

TEST_CONFIG_RAW_YAML = f"""
---
{CONF_BOOLEAN_BATTERY_TRUE_VALUE}: 1
{CONF_DEFAULT_BATTERY_STRATEGY}: {BatteryStrategy.BOOLEAN}
{CONF_DIAGNOSTICS}: false
{CONF_DISABLE_CALCULATED_DATA}: false
{CONF_ENDPOINT}: {TEST_ENDPOINT}
{CONF_HASS_DISCOVERY}: false
{CONF_HASS_DISCOVERY_PREFIX}: {TEST_HASS_DISCOVERY_PREFIX}
{CONF_HASS_ENTITY_ID_PREFIX}: null
{CONF_INPUT_DATA_FORMAT}: {InputDataFormat.ECOWITT}
{CONF_INPUT_UNIT_SYSTEM}: {UnitSystem.IMPERIAL}
{CONF_MQTT_BROKER}: {TEST_MQTT_BROKER}
{CONF_MQTT_PASSWORD}: {TEST_MQTT_PASSWORD}
{CONF_MQTT_PORT}: {TEST_MQTT_PORT}
{CONF_MQTT_RETAIN}: false
{CONF_MQTT_TLS}: false
{CONF_MQTT_TOPIC}: {TEST_MQTT_TOPIC}
{CONF_MQTT_USERNAME}: {TEST_MQTT_USERNAME}
{CONF_OUTPUT_UNIT_SYSTEM}: {UnitSystem.IMPERIAL}
{CONF_PORT}: {TEST_PORT}
{CONF_RAW_DATA}: false
{CONF_VERBOSE}: false
"""


def load_fixture(filename: str) -> str:
    """Load a fixture.

    Args:
        filename: The filename of the fixtures/ file to load.

    Returns:
        A string containing the contents of the file.
    """
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
