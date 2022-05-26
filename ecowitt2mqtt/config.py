"""Define a configuration management module."""
from __future__ import annotations

import os

from ruamel.yaml import YAML
import typer

from ecowitt2mqtt.const import (
    CONF_CONFIG,
    CONF_HASS_DISCOVERY,
    CONF_MQTT_BROKER,
    CONF_MQTT_TOPIC,
    ENV_ENDPOINT,
    ENV_HASS_DISCOVERY,
    ENV_HASS_DISCOVERY_PREFIX,
    ENV_HASS_ENTITY_ID_PREFIX,
    ENV_INPUT_UNIT_SYSTEM,
    ENV_MQTT_BROKER,
    ENV_MQTT_PASSWORD,
    ENV_MQTT_PORT,
    ENV_MQTT_TOPIC,
    ENV_MQTT_USERNAME,
    ENV_OUTPUT_UNIT_SYSTEM,
    ENV_PORT,
    ENV_RAW_DATA,
    ENV_VERBOSE,
    LEGACY_ENV_ENDPOINT,
    LEGACY_ENV_HASS_DISCOVERY,
    LEGACY_ENV_HASS_DISCOVERY_PREFIX,
    LEGACY_ENV_HASS_ENTITY_ID_PREFIX,
    LEGACY_ENV_INPUT_UNIT_SYSTEM,
    LEGACY_ENV_LOG_LEVEL,
    LEGACY_ENV_MQTT_BROKER,
    LEGACY_ENV_MQTT_PASSWORD,
    LEGACY_ENV_MQTT_PORT,
    LEGACY_ENV_MQTT_TOPIC,
    LEGACY_ENV_MQTT_USERNAME,
    LEGACY_ENV_OUTPUT_UNIT_SYSTEM,
    LEGACY_ENV_PORT,
    LEGACY_ENV_RAW_DATA,
    LOGGER,
)
from ecowitt2mqtt.errors import ConfigError

DEPRECATED_ENV_VAR_MAP = {
    LEGACY_ENV_ENDPOINT: ENV_ENDPOINT,
    LEGACY_ENV_HASS_DISCOVERY: ENV_HASS_DISCOVERY,
    LEGACY_ENV_HASS_DISCOVERY_PREFIX: ENV_HASS_DISCOVERY_PREFIX,
    LEGACY_ENV_HASS_ENTITY_ID_PREFIX: ENV_HASS_ENTITY_ID_PREFIX,
    LEGACY_ENV_INPUT_UNIT_SYSTEM: ENV_INPUT_UNIT_SYSTEM,
    LEGACY_ENV_LOG_LEVEL: ENV_VERBOSE,
    LEGACY_ENV_MQTT_BROKER: ENV_MQTT_BROKER,
    LEGACY_ENV_MQTT_PASSWORD: ENV_MQTT_PASSWORD,
    LEGACY_ENV_MQTT_PORT: ENV_MQTT_PORT,
    LEGACY_ENV_MQTT_TOPIC: ENV_MQTT_TOPIC,
    LEGACY_ENV_MQTT_USERNAME: ENV_MQTT_USERNAME,
    LEGACY_ENV_OUTPUT_UNIT_SYSTEM: ENV_OUTPUT_UNIT_SYSTEM,
    LEGACY_ENV_PORT: ENV_PORT,
    LEGACY_ENV_RAW_DATA: ENV_RAW_DATA,
}


class Config:
    """Define the configuration management object."""

    def __init__(self, ctx: typer.Context) -> None:
        """Initialize."""
        LOGGER.info("CLI options: %s", ctx.params)

        for legacy_env_var, new_env_var in DEPRECATED_ENV_VAR_MAP.items():
            if os.getenv(legacy_env_var) is None:
                continue
            LOGGER.warning(
                "Environment variable %s is deprecated; use %s instead",
                legacy_env_var,
                new_env_var,
            )

        self._config = {}

        # If the user provides a config file, attempt to load it:
        if config_path := ctx.params[CONF_CONFIG]:
            parser = YAML(typ="safe")
            with open(config_path, encoding="utf-8") as config_file:
                self._config = parser.load(config_file)

        if not isinstance(self._config, dict):
            raise ConfigError(f"Unable to parse config file: {config_path}")

        # Merge the CLI options/environment variables in using this logic:
        #   1. If the value is not None, its an override and we should use it
        #   2. If a key doesn't exist in self._config yet, include it
        for key, value in ctx.params.items():
            if value is not None or key not in self._config:
                self._config[key] = value

        # If we don't have an MQTT broker, we can't proceed:
        if not self._config[CONF_MQTT_BROKER]:
            raise ConfigError("Missing required option: --mqtt-broker")

        if not self._config[CONF_MQTT_TOPIC] and not self._config[CONF_HASS_DISCOVERY]:
            raise ConfigError(
                "Missing required option: --mqtt-topic or --hass-discovery"
            )

        LOGGER.debug("Loaded Config: %s", self._config)
