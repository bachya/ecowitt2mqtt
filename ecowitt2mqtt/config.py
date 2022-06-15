"""Define a configuration management module."""
from __future__ import annotations

import os
from typing import Any, Dict, cast

from ruamel.yaml import YAML

from ecowitt2mqtt.const import (
    CONF_BATTERY_OVERRIDES,
    CONF_CONFIG,
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
    CONF_MQTT_TLS,
    CONF_MQTT_TOPIC,
    CONF_MQTT_USERNAME,
    CONF_OUTPUT_UNIT_SYSTEM,
    CONF_PORT,
    CONF_RAW_DATA,
    CONF_VERBOSE,
    ENV_BATTERY_OVERRIDE,
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
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy
from ecowitt2mqtt.helpers.typing import UnitSystemType

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


def convert_battery_config(configs: str | tuple) -> dict[str, BatteryStrategy]:
    """Normalize incoming battery configurations depending on the input format.

    1. Environment Variables (str): "key1=value1;key2=value2"
    2. CLI Options (tuple): ("key1=val1", "key2=val2")
    """
    try:
        if isinstance(configs, str):
            return {
                pair[0]: BatteryStrategy(pair[1])
                for assignment in configs.split(";")
                if (pair := assignment.split("="))
            }
        return {
            pair[0]: BatteryStrategy(pair[1])
            for assignment in configs
            if (pair := assignment.split("="))
        }
    except (IndexError, KeyError, ValueError) as err:
        raise ConfigError(f"Unable to parse battery configurations: {configs}") from err


class Config:
    """Define the configuration management object."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Initialize."""
        LOGGER.debug("CLI options: %s", params)

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

        if not any(data.get(CONF_MQTT_BROKER) for data in (self._config, params)):
            raise ConfigError("Missing required option: --mqtt-broker")

        if not any(
            data.get(key)
            for key in (CONF_MQTT_TOPIC, CONF_HASS_DISCOVERY)
            for data in (self._config, params)
        ):
            raise ConfigError(
                "Missing required option: --mqtt-topic or --hass-discovery"
            )

        self._config.setdefault(CONF_BATTERY_OVERRIDES, {})

        # Merge the CLI options/environment variables; if the value is falsey (but *not*
        # False), ignore it:
        for key, value in params.items():
            if key == CONF_DEFAULT_BATTERY_STRATEGY:
                self._config[key] = BatteryStrategy(value)
            if value is not None:
                self._config[key] = value

        if env_battery_overrides := os.getenv(ENV_BATTERY_OVERRIDE):
            self._config[CONF_BATTERY_OVERRIDES] = convert_battery_config(
                env_battery_overrides
            )
        elif CONF_BATTERY_OVERRIDES in params:
            self._config[CONF_BATTERY_OVERRIDES] = convert_battery_config(
                params[CONF_BATTERY_OVERRIDES]
            )

        LOGGER.debug("Loaded Config: %s", self._config)

    @property
    def battery_overrides(self) -> dict[str, BatteryStrategy]:
        """Return the battery overrides."""
        return cast(
            Dict[str, BatteryStrategy], self._config.get(CONF_BATTERY_OVERRIDES)
        )

    @property
    def default_battery_strategy(self) -> BatteryStrategy:
        """Return the default battery strategy."""
        return cast(BatteryStrategy, self._config.get(CONF_DEFAULT_BATTERY_STRATEGY))

    @property
    def diagnostics(self) -> bool:
        """Return whether diagnostics is enabled."""
        return cast(bool, self._config.get(CONF_DIAGNOSTICS))

    @property
    def endpoint(self) -> str:
        """Return the ecowitt2mqtt API endpoint."""
        return cast(str, self._config.get(CONF_ENDPOINT))

    @property
    def hass_discovery(self) -> bool:
        """Return whether Home Assistant Discovery should be used."""
        return cast(bool, self._config.get(CONF_HASS_DISCOVERY))

    @property
    def hass_discovery_prefix(self) -> str:
        """Return the Home Assistant Discovery MQTT prefix."""
        return cast(str, self._config.get(CONF_HASS_DISCOVERY_PREFIX))

    @property
    def hass_entity_id_prefix(self) -> str | None:
        """Return the Home Assistant entity ID prefix."""
        return self._config.get(CONF_HASS_ENTITY_ID_PREFIX)

    @property
    def input_unit_system(self) -> UnitSystemType:
        """Return the input unit system."""
        return cast(UnitSystemType, self._config.get(CONF_INPUT_UNIT_SYSTEM))

    @property
    def mqtt_broker(self) -> str:
        """Return the MQTT broker host/IP address."""
        return cast(str, self._config.get(CONF_MQTT_BROKER))

    @property
    def mqtt_password(self) -> str:
        """Return the MQTT broker password."""
        return cast(str, self._config.get(CONF_MQTT_PASSWORD))

    @property
    def mqtt_port(self) -> int:
        """Return the MQTT broker port."""
        return cast(int, self._config.get(CONF_MQTT_PORT))

    @property
    def mqtt_tls(self) -> bool:
        """Return whether MQTT over TLS is configured."""
        return cast(bool, self._config.get(CONF_MQTT_TLS))

    @property
    def mqtt_topic(self) -> str | None:
        """Return the MQTT broker topic."""
        return self._config.get(CONF_MQTT_TOPIC)

    @property
    def mqtt_username(self) -> str:
        """Return the MQTT broker username."""
        return cast(str, self._config.get(CONF_MQTT_USERNAME))

    @property
    def output_unit_system(self) -> UnitSystemType:
        """Return the output unit system."""
        return cast(UnitSystemType, self._config.get(CONF_OUTPUT_UNIT_SYSTEM))

    @property
    def port(self) -> int:
        """Return the ecowitt2mqtt API port."""
        return cast(int, self._config.get(CONF_PORT))

    @property
    def raw_data(self) -> bool:
        """Return whether raw data is configured."""
        return cast(bool, self._config.get(CONF_RAW_DATA))

    @property
    def verbose(self) -> bool:
        """Return whether verbose logging is enabled."""
        return cast(bool, self._config.get(CONF_VERBOSE))
