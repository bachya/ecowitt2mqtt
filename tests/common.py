"""Define common test utilities."""
import json

from ecowitt2mqtt.const import (
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
)

TEST_ENDPOINT = "/data/output"
TEST_HASS_DISCOVERY_PREFIX = "homeassistant"
TEST_HASS_ENTITY_ID_PREFIX = "ecowitt"
TEST_INPUT_UNIT_SYSTEM = "imperial"
TEST_MQTT_BROKER = "127.0.0.1"
TEST_MQTT_PASSWORD = "password"
TEST_MQTT_PORT = 1883
TEST_MQTT_TOPIC = "topic/"
TEST_MQTT_USERNAME = "username"
TEST_OUTPUT_UNIT_SYSTEM = "imperial"
TEST_PORT = 9999

TEST_RAW_JSON = json.dumps(
    {
        CONF_ENDPOINT: TEST_ENDPOINT,
        CONF_HASS_DISCOVERY: False,
        CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
        CONF_HASS_ENTITY_ID_PREFIX: TEST_HASS_ENTITY_ID_PREFIX,
        CONF_INPUT_UNIT_SYSTEM: TEST_INPUT_UNIT_SYSTEM,
        CONF_MQTT_BROKER: TEST_MQTT_BROKER,
        CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
        CONF_MQTT_PORT: TEST_MQTT_PORT,
        CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
        CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
        CONF_OUTPUT_UNIT_SYSTEM: TEST_OUTPUT_UNIT_SYSTEM,
        CONF_PORT: TEST_PORT,
        CONF_RAW_DATA: False,
        CONF_VERBOSE: False,
    }
)
TEST_RAW_YAML = f"""
---
{CONF_ENDPOINT}: {TEST_ENDPOINT}
{CONF_HASS_DISCOVERY}: false
{CONF_HASS_DISCOVERY_PREFIX}: {TEST_HASS_DISCOVERY_PREFIX}
{CONF_HASS_ENTITY_ID_PREFIX}: {TEST_HASS_ENTITY_ID_PREFIX}
{CONF_INPUT_UNIT_SYSTEM}: {TEST_INPUT_UNIT_SYSTEM}
{CONF_MQTT_BROKER}: {TEST_MQTT_BROKER}
{CONF_MQTT_PASSWORD}: {TEST_MQTT_PASSWORD}
{CONF_MQTT_PORT}: {TEST_MQTT_PORT}
{CONF_MQTT_TOPIC}: {TEST_MQTT_TOPIC}
{CONF_MQTT_USERNAME}: {TEST_MQTT_USERNAME}
{CONF_OUTPUT_UNIT_SYSTEM}: {TEST_OUTPUT_UNIT_SYSTEM}
{CONF_PORT}: {TEST_PORT}
{CONF_RAW_DATA}: false
{CONF_VERBOSE}: false
"""
