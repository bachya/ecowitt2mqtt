"""Define package constants."""
import logging

LOGGER = logging.getLogger(__package__)

# Configuration options:
CONF_VERBOSE = "verbose"

# Environment variables:
ENV_ENDPOINT = "ECOWITT2MQTT_ENDPOINT"
ENV_HASS_DISCOVERY = "ECOWITT2MQTT_HASS_DISCOVERY"
ENV_HASS_DISCOVERY_PREFIX = "ECOWITT2MQTT_HASS_DISCOVERY_PREFIX"
ENV_HASS_ENTITY_ID_PREFIX = "ECOWITT2MQTT_HASS_ENTITY_ID_PREFIX"
ENV_INPUT_UNIT_SYSTEM = "ECOWITT2MQTT_INPUT_UNIT_SYSTEM"
ENV_MQTT_BROKER = "ECOWITT2MQTT_MQTT_BROKER"
ENV_MQTT_PASSWORD = "ECOWITT2MQTT_MQTT_PASSWORD"
ENV_MQTT_PORT = "ECOWITT2MQTT_MQTT_PORT"
ENV_MQTT_TOPIC = "ECOWITT2MQTT_MQTT_TOPIC"
ENV_MQTT_USERNAME = "ECOWITT2MQTT_MQTT_USERNAME"
ENV_OUTPUT_UNIT_SYSTEM = "ECOWITT2MQTT_OUTPUT_UNIT_SYSTEM"
ENV_PORT = "ECOWITT2MQTT_PORT"
ENV_RAW_DATA = "ECOWITT2MQTT_RAW_DATA"
ENV_VERBOSE = "ECOWITT2MQTT_VERBOSE"

# Legacy environment variables that will be deprecated at some point:
LEGACY_ENV_ENDPOINT = "ENDPOINT"
LEGACY_ENV_HASS_DISCOVERY = "HASS_DISCOVERY"
LEGACY_ENV_HASS_DISCOVERY_PREFIX = "HASS_DISCOVERY_PREFIX"
LEGACY_ENV_HASS_ENTITY_ID_PREIFX = "HASS_ENTITY_ID_PREFIX"
LEGACY_ENV_INPUT_UNIT_SYSTEM = "INPUT_UNIT_SYSTEM"
LEGACY_ENV_LOG_LEVEL = "LOG_LEVEL"
LEGACY_ENV_MQTT_BROKER = "MQTT_BROKER"
LEGACY_ENV_MQTT_PASSWORD = "MQTT_PASSWORD"
LEGACY_ENV_MQTT_PORT = "MQTT_PORT"
LEGACY_ENV_MQTT_TOPIC = "MQTT_TOPIC"
LEGACY_ENV_MQTT_USERNAME = "MQTT_USERNAME"
LEGACY_ENV_OUTPUT_UNIT_SYSTEM = "OUTPUT_UNIT_SYSTEM"
LEGACY_ENV_PORT = "PORT"
LEGACY_ENV_RAW_DATA = "RAW_DATA"

# Unit systems:
UNIT_SYSTEM_IMPERIAL = "imperial"
UNIT_SYSTEM_METRIC = "metric"
