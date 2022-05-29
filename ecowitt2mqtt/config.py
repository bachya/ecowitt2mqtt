"""Define a configuration management module."""
from __future__ import annotations

import os
from typing import Any, cast

from ruamel.yaml import YAML

from ecowitt2mqtt.const import (
    CONF_CONFIG,
    CONF_ENDPOINT,
    CONF_HASS_DISCOVERY,
    CONF_MQTT_BROKER,
    CONF_MQTT_PASSWORD,
    CONF_MQTT_PORT,
    CONF_MQTT_TOPIC,
    CONF_MQTT_USERNAME,
    CONF_PORT,
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
from ecowitt2mqtt.errors import EcowittError

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


class ConfigError(EcowittError):
    """Define an error related to bad configuration."""

    pass


class Config:
    """Define the configuration management object."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Initialize."""
        LOGGER.info("CLI options: %s", params)

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
        if config_path := params.get(CONF_CONFIG):
            parser = YAML(typ="safe")
            with open(config_path, encoding="utf-8") as config_file:
                self._config = parser.load(config_file)

        if not isinstance(self._config, dict):
            raise ConfigError(f"Unable to parse config file: {config_path}")

        # Merge the CLI options/environment variables in using this logic:
        #   1. If the value is not None, its an override and we should use it
        #   2. If a key doesn't exist in self._config yet, include it
        for key, value in params.items():
            if value is not None or key not in self._config:
                self._config[key] = value

        # If we don't have an MQTT broker, we can't proceed:
        if self._config.get(CONF_MQTT_BROKER) is None:
            raise ConfigError("Missing required option: --mqtt-broker")

        if all(not self._config.get(c) for c in (CONF_MQTT_TOPIC, CONF_HASS_DISCOVERY)):
            raise ConfigError(
                "Missing required option: --mqtt-topic or --hass-discovery"
            )

        LOGGER.debug("Loaded Config: %s", self._config)

    @property
    def endpoint(self) -> str:
        """Return the ecowitt2mqtt API endpoint."""
        return cast(str, self._config[CONF_ENDPOINT])

    @property
    def mqtt_broker(self) -> str:
        """Return the MQTT broker host/IP address."""
        return cast(str, self._config[CONF_MQTT_BROKER])

    @property
    def mqtt_password(self) -> str:
        """Return the MQTT broker password."""
        return cast(str, self._config[CONF_MQTT_PASSWORD])

    @property
    def mqtt_port(self) -> int:
        """Return the MQTT broker port."""
        return cast(int, self._config[CONF_MQTT_PORT])

    @property
    def mqtt_topic(self) -> str | None:
        """Return the MQTT broker topic."""
        return self._config.get(CONF_MQTT_TOPIC)

    @property
    def port(self) -> int:
        """Return the ecowitt2mqtt API port."""
        return cast(int, self._config[CONF_PORT])

    @property
    def mqtt_username(self) -> str:
        """Return the MQTT broker username."""
        return cast(str, self._config[CONF_MQTT_USERNAME])
