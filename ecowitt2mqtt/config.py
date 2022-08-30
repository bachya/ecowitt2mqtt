"""Define a configuration management module."""
from __future__ import annotations

import os
from typing import Any, Dict, cast

from ruamel.yaml import YAML
import voluptuous as vol

from ecowitt2mqtt.const import (
    CONF_BATTERY_OVERRIDES,
    CONF_CONFIG,
    CONF_DEFAULT_BATTERY_STRATEGY,
    CONF_DIAGNOSTICS,
    CONF_DISABLE_CALCULATED_DATA,
    CONF_ENDPOINT,
    CONF_GATEWAYS,
    CONF_HASS_DISCOVERY,
    CONF_HASS_DISCOVERY_PREFIX,
    CONF_HASS_ENTITY_ID_PREFIX,
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
    DEFAULT_ENDPOINT,
    DEFAULT_HASS_DISCOVERY_PREFIX,
    DEFAULT_MQTT_PORT,
    DEFAULT_PORT,
    ENV_BATTERY_OVERRIDES,
    UNIT_SYSTEM_IMPERIAL,
)
from ecowitt2mqtt.errors import EcowittError
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy
import ecowitt2mqtt.helpers.config_validation as cv
from ecowitt2mqtt.helpers.typing import UnitSystemType

CONF_DEFAULT = "default"

HASS_DISCOVERY_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HASS_DISCOVERY): vol.All(cv.boolean, True),
        vol.Optional(
            CONF_HASS_DISCOVERY_PREFIX, default=DEFAULT_HASS_DISCOVERY_PREFIX
        ): str,
        vol.Optional(CONF_HASS_ENTITY_ID_PREFIX): cv.optional_string,
    },
    extra=vol.ALLOW_EXTRA,
)

MQTT_TOPIC_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_MQTT_TOPIC): str,
    },
    extra=vol.ALLOW_EXTRA,
)

CONFIG_SCHEMA = vol.All(
    vol.Any(
        HASS_DISCOVERY_SCHEMA,
        MQTT_TOPIC_SCHEMA,
        msg="Must provide an MQTT topic or enable Home Assistant MQTT Discovery",
    ),
    vol.Schema(
        {
            vol.Required(CONF_MQTT_BROKER): str,
            vol.Inclusive(CONF_MQTT_USERNAME, "mqtt_auth"): cv.optional_string,
            vol.Inclusive(CONF_MQTT_PASSWORD, "mqtt_auth"): cv.optional_string,
            vol.Optional(CONF_MQTT_PORT, default=DEFAULT_MQTT_PORT): cv.port,
            vol.Optional(CONF_MQTT_RETAIN, default=False): cv.boolean,
            vol.Optional(CONF_MQTT_TLS, default=False): cv.boolean,
            vol.Optional(CONF_BATTERY_OVERRIDES, default={}): cv.battery_override,
            vol.Optional(
                CONF_DEFAULT_BATTERY_STRATEGY, default=BatteryStrategy.BOOLEAN
            ): vol.Coerce(BatteryStrategy),
            vol.Optional(CONF_DIAGNOSTICS, default=False): cv.boolean,
            vol.Optional(CONF_DISABLE_CALCULATED_DATA, default=False): cv.boolean,
            vol.Optional(CONF_ENDPOINT, default=DEFAULT_ENDPOINT): str,
            vol.Optional(
                CONF_INPUT_UNIT_SYSTEM, default=UNIT_SYSTEM_IMPERIAL
            ): cv.unit_system,
            vol.Optional(
                CONF_OUTPUT_UNIT_SYSTEM, default=UNIT_SYSTEM_IMPERIAL
            ): cv.unit_system,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
            vol.Optional(CONF_RAW_DATA, default=False): cv.boolean,
            vol.Optional(CONF_VERBOSE, default=False): cv.boolean,
        },
        extra=vol.ALLOW_EXTRA,
    ),
)


class ConfigError(EcowittError):
    """Define an error related to bad configuration."""

    pass


def load_config_from_file(config_path: str) -> dict[str, Any]:
    """Load config data from a YAML or JSON file."""
    config_file_data = {}

    parser = YAML(typ="safe")
    with open(config_path, encoding="utf-8") as config_file:
        config_file_data = parser.load(config_file)

    if not isinstance(config_file_data, dict):
        raise ConfigError(f"Unable to parse config file: {config_path}")

    return config_file_data


class Config:  # pylint: disable=too-many-public-methods
    """Define the configuration management object."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize."""
        self._config = {**config}

        # The battery override env var is the only one that isn't passed through from
        # the CLI (given its special format), so check for it here:
        if battery_overrides_env_var := os.getenv(ENV_BATTERY_OVERRIDES):
            self._config[CONF_BATTERY_OVERRIDES] = battery_overrides_env_var

        try:
            self._config = CONFIG_SCHEMA(self._config)
        except vol.Invalid as err:
            raise ConfigError(err) from err

        self._mqtt_connection_info = (
            f"{self._config.get(CONF_MQTT_USERNAME)}@{self._config[CONF_MQTT_BROKER]}"
            f":{self._config[CONF_MQTT_PORT]}"
        )

    def __repr__(self) -> str:
        """Define a string representation of this object."""
        return str(self._config)

    @property
    def battery_overrides(self) -> dict[str, BatteryStrategy]:
        """Return the battery overrides."""
        return cast(Dict[str, BatteryStrategy], self._config[CONF_BATTERY_OVERRIDES])

    @property
    def default_battery_strategy(self) -> BatteryStrategy:
        """Return the default battery strategy."""
        return cast(BatteryStrategy, self._config[CONF_DEFAULT_BATTERY_STRATEGY])

    @property
    def diagnostics(self) -> bool:
        """Return whether diagnostics is enabled."""
        return cast(bool, self._config[CONF_DIAGNOSTICS])

    @property
    def disable_calculated_data(self) -> bool:
        """Return whether calculated sensor output is disabled."""
        return cast(bool, self._config[CONF_DISABLE_CALCULATED_DATA])

    @property
    def endpoint(self) -> str:
        """Return the ecowitt2mqtt API endpoint."""
        return cast(str, self._config[CONF_ENDPOINT])

    @property
    def hass_discovery(self) -> bool:
        """Return whether Home Assistant Discovery should be used."""
        return cast(bool, self._config.get(CONF_HASS_DISCOVERY))

    @property
    def hass_discovery_prefix(self) -> str:
        """Return the Home Assistant Discovery MQTT prefix."""
        return cast(str, self._config[CONF_HASS_DISCOVERY_PREFIX])

    @property
    def hass_entity_id_prefix(self) -> str | None:
        """Return the Home Assistant entity ID prefix."""
        return self._config.get(CONF_HASS_ENTITY_ID_PREFIX)

    @property
    def input_unit_system(self) -> UnitSystemType:
        """Return the input unit system."""
        return cast(UnitSystemType, self._config[CONF_INPUT_UNIT_SYSTEM])

    @property
    def mqtt_broker(self) -> str:
        """Return the MQTT broker host/IP address."""
        return cast(str, self._config[CONF_MQTT_BROKER])

    @property
    def mqtt_connection_info(self) -> str:
        """Return a string representation of MQTT connection parameters."""
        return self._mqtt_connection_info

    @property
    def mqtt_password(self) -> str | None:
        """Return the MQTT broker password."""
        return self._config.get(CONF_MQTT_PASSWORD)

    @property
    def mqtt_port(self) -> int:
        """Return the MQTT broker port."""
        return cast(int, self._config[CONF_MQTT_PORT])

    @property
    def mqtt_retain(self) -> bool:
        """Return whether MQTT messages should be retained."""
        return cast(bool, self._config[CONF_MQTT_RETAIN])

    @property
    def mqtt_tls(self) -> bool:
        """Return whether MQTT over TLS is configured."""
        return cast(bool, self._config[CONF_MQTT_TLS])

    @property
    def mqtt_topic(self) -> str | None:
        """Return the MQTT broker topic."""
        return self._config.get(CONF_MQTT_TOPIC)

    @property
    def mqtt_username(self) -> str | None:
        """Return the MQTT broker username."""
        return self._config.get(CONF_MQTT_USERNAME)

    @property
    def output_unit_system(self) -> UnitSystemType:
        """Return the output unit system."""
        return cast(UnitSystemType, self._config[CONF_OUTPUT_UNIT_SYSTEM])

    @property
    def port(self) -> int:
        """Return the ecowitt2mqtt API port."""
        return cast(int, self._config[CONF_PORT])

    @property
    def raw_data(self) -> bool:
        """Return whether raw data is configured."""
        return cast(bool, self._config[CONF_RAW_DATA])

    @property
    def verbose(self) -> bool:
        """Return whether verbose logging is enabled."""
        return cast(bool, self._config[CONF_VERBOSE])


class Configs:
    """Define a coordinator of various Config objects."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize."""
        self._configs: dict[str, Config] = {}
        self._config_file_parser = YAML(typ="safe")

        if config_path := config.get(CONF_CONFIG):
            config_file_config = load_config_from_file(config_path)
        else:
            config_file_config = {}

        # Store the default config:
        self._configs[CONF_DEFAULT] = Config({**config_file_config, **config})

        # Store configs for any gateways:
        gateways_file_config = config_file_config.get(CONF_GATEWAYS, {})
        for passkey, gateway_config in gateways_file_config.items():
            self._configs[passkey] = Config({**gateway_config, **config})

    def __repr__(self) -> str:
        """Define a string representation of this object."""
        return f"<Configs _configs={self._configs}"

    @property
    def default_config(self) -> Config:
        """Return the default config."""
        return self._configs[CONF_DEFAULT]

    def get(self, passkey: str) -> Config:
        """Get the config for a particular passkey (returning the default if none)."""
        return self._configs.get(passkey, self.default_config)
