"""Define a configuration management module."""

from __future__ import annotations

import os
from collections.abc import Generator
from numbers import Number
from typing import Any
from uuid import uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)
from ruamel.yaml import YAML

from ecowitt2mqtt.const import (
    CONF_BATTERY_OVERRIDES,
    CONF_CONFIG,
    CONF_DIAGNOSTICS,
    CONF_GATEWAYS,
    CONF_HASS_DISCOVERY,
    CONF_MQTT_PASSWORD,
    CONF_MQTT_TOPIC,
    CONF_MQTT_USERNAME,
    CONF_VERBOSE,
    DEFAULT_BOOLEAN_BATTERY_TRUE_VALUE,
    DEFAULT_ENDPOINT,
    DEFAULT_HASS_DISCOVERY_PREFIX,
    DEFAULT_LOCALE,
    DEFAULT_MQTT_PORT,
    DEFAULT_PORT,
    ENV_BATTERY_OVERRIDES,
    UnitOfAccumulatedPrecipitation,
    UnitOfIlluminance,
    UnitOfLength,
    UnitOfPrecipitationRate,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
    UnitOfVolume,
    UnitSystem,
)
from ecowitt2mqtt.errors import EcowittError
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy
from ecowitt2mqtt.helpers.server import InputDataFormat

CONF_DEFAULT = "default"

REQUIRES_AT_LEAST_ONE_OF = (
    CONF_MQTT_TOPIC,
    CONF_HASS_DISCOVERY,
)

TRUTHY_VALUES = {"1", "true", "yes", "on", "enable"}
FALSEY_VALUES = {"0", "false", "no", "off", "disable"}

BOOLEAN_BATTERY_TRUE_VALUES = {0, 1}


class ConfigError(EcowittError):
    """Define an error related to bad configuration."""

    pass


def validate_boolean(value: bool | str | Number) -> bool:
    """Validate a variety of possible boolean values.

    Args:
        value: A value to validate.

    Returns:
        A boolean value.

    Raises:
        ValueError: Raises if the value is not a valid boolean.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.lower().strip()
        if value in TRUTHY_VALUES:
            return True
        if value in FALSEY_VALUES:
            return False
    elif isinstance(value, Number):
        # type ignore: https://github.com/python/mypy/issues/3186
        return value != 0  # type: ignore[comparison-overlap]
    raise ValueError(f"invalid boolean value: {value}")


def validate_port(value: int | str) -> int:
    """Validate a port

    Args:
        value: A value to validate.

    Returns:
        An validated port.

    Raises:
        ValueError: Raises if the value is not a valid port.
    """
    parsed = int(value)
    if not 1 <= parsed <= 65536:
        raise ValueError(f"invalid port: {value}")
    return parsed


class Config(BaseModel):
    """Define a config object."""

    model_config = ConfigDict(frozen=True)

    # Required parameters:
    mqtt_broker: str

    # Optional MQTT parameters:
    mqtt_password: str | None = None
    mqtt_port: int = DEFAULT_MQTT_PORT
    mqtt_retain: bool = False
    mqtt_tls: bool = False
    mqtt_topic: str | None = None
    mqtt_username: str | None = None

    # Optional battery parameters:
    battery_overrides: dict[str, BatteryStrategy] = {}
    boolean_battery_true_value: int = DEFAULT_BOOLEAN_BATTERY_TRUE_VALUE
    default_battery_strategy: BatteryStrategy = BatteryStrategy.BOOLEAN

    # Optional data parameters:
    disable_calculated_data: bool = False
    input_data_format: InputDataFormat = InputDataFormat.ECOWITT
    precision: int | None = None
    raw_data: bool = False

    # Optional Home Assistant MQTT Discovery parameters:
    hass_discovery: bool = False
    hass_discovery_prefix: str = DEFAULT_HASS_DISCOVERY_PREFIX
    hass_entity_id_prefix: str | None = None

    # Optional HTTP parameters:
    endpoint: str = DEFAULT_ENDPOINT
    port: int = DEFAULT_PORT

    # Optional logging parameters:
    diagnostics: bool = False
    verbose: bool = False

    # Optional unit conversion parameters:
    output_unit_accumulated_precipitation: UnitOfAccumulatedPrecipitation | None = None
    output_unit_distance: UnitOfLength | None = None
    output_unit_humidity: UnitOfVolume | None = None
    output_unit_illuminance: UnitOfIlluminance | None = None
    output_unit_precipitation_rate: UnitOfPrecipitationRate | None = None
    output_unit_pressure: UnitOfPressure | None = None
    output_unit_speed: UnitOfSpeed | None = None
    output_unit_temperature: UnitOfTemperature | None = None

    # Optional unit system parameters:
    input_unit_system: UnitSystem = UnitSystem.IMPERIAL
    output_unit_system: UnitSystem = UnitSystem.IMPERIAL

    # Generated parameters:
    uuid: str = Field(default_factory=lambda: uuid4().hex)

    # Misc. parameters:
    locale: str = DEFAULT_LOCALE

    @model_validator(mode="before")
    @classmethod
    def get_raw_battery_overrides(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Get the raw battery overrides from the environment variable.

        The battery override env var is the only one that isn't passed through from the
        CLI (given its special format), so check for it here.

        Args:
            data: The config data.

        Returns:
            The potentially altered config data.
        """
        if battery_overrides_env_var := os.getenv(ENV_BATTERY_OVERRIDES):
            data[CONF_BATTERY_OVERRIDES] = battery_overrides_env_var
        return data

    @model_validator(mode="before")
    @classmethod
    def set_diagnostics_verbosity(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Set verbose when diagnostics is set.

        Args:
            data: The config data.

        Returns:
            The potentially altered config data.
        """
        if data.get(CONF_DIAGNOSTICS):
            data[CONF_VERBOSE] = True
        return data

    @field_validator("battery_overrides", mode="before")
    @classmethod
    def validate_battery_overrides(
        cls, value: dict[str, str] | tuple[str] | str
    ) -> dict[str, Any]:
        """Validate that the battery overrides are valid.

        Args:
            value: The battery overrides.

        Returns:
            The parsed battery overrides in a dictionary.

        Raises:
            ValueError: Raises if the battery overrides are invalid.
        """
        try:
            if isinstance(value, dict):
                return {key: BatteryStrategy(val) for key, val in value.items()}

            if isinstance(value, tuple):
                return {
                    pair[0]: BatteryStrategy(pair[1])
                    for assignment in value
                    if (pair := assignment.split("="))
                }

            return {
                pair[0]: BatteryStrategy(pair[1])
                for assignment in value.split(";")
                if (pair := assignment.split("="))
            }
        except (IndexError, ValueError) as err:
            raise ValueError(f"invalid battery overrides: {value}") from err

    @field_validator("boolean_battery_true_value", mode="before")
    @classmethod
    def validate_boolean_battery_true_value(cls, value: int | str) -> int:
        """Validate that boolean battery true value is valid.

        Args:
            value: The boolean battery true value.

        Returns:
            The parsed boolean battery true value.
        """
        if (parsed := int(value)) not in BOOLEAN_BATTERY_TRUE_VALUES:
            raise ValueError(f"invalid boolean battery true value: {value}")
        return parsed

    validate_diagnostics = field_validator("diagnostics", mode="before")(
        validate_boolean
    )

    validate_disable_calculated_data = field_validator(
        "disable_calculated_data", mode="before"
    )(validate_boolean)

    validate_hass_discovery = field_validator("hass_discovery", mode="before")(
        validate_boolean
    )

    @model_validator(mode="before")
    @classmethod
    def validate_mqtt_auth(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Validate that auth is either fully absent or fully present.

        Args:
            data: The config data.

        Returns:
            The config data with the MQTT auth validation.

        Raises:
            ValueError: Raises if the MQTT auth is invalid.
        """
        if (data.get(CONF_MQTT_USERNAME) is None) != (
            data.get(CONF_MQTT_PASSWORD) is None
        ):
            raise ValueError("Invalid MQTT auth configuration")
        return data

    validate_mqtt_port = field_validator("mqtt_port", mode="before")(validate_port)

    validate_mqtt_retain = field_validator("mqtt_retain", mode="before")(
        validate_boolean
    )

    validate_mqtt_tls = field_validator("mqtt_tls", mode="before")(validate_boolean)

    validate_port = field_validator("port", mode="before")(validate_port)

    validate_raw_data = field_validator("raw_data", mode="before")(validate_boolean)

    @model_validator(mode="before")
    @classmethod
    def validate_required_optional_parameters(
        cls, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate that an approved mixture of optional parameters is present.

        Args:
            data: The config data.

        Returns:
            The config data with the required optional parameters validated.

        Raises:
            ValueError: Raises if an invalid mixture of optional parameters is present.
        """
        if not any(data.get(param) for param in REQUIRES_AT_LEAST_ONE_OF):
            raise ValueError(
                f"must provide at least one of: {', '.join(REQUIRES_AT_LEAST_ONE_OF)}"
            )
        return data

    validate_verbose = field_validator("verbose", mode="before")(validate_boolean)


def load_config_from_file(config_path: str) -> dict[str, Any]:
    """Load config data from a YAML or JSON file.

    Args:
        config_path: A path to a configuration file.

    Returns:
        A dictionary of parsed config options.

    Raises:
        ConfigError: Raises if the config file contains unparsable data.
    """
    config_file_data = {}

    parser = YAML(typ="safe")
    with open(config_path, encoding="utf-8") as config_file:
        config_file_data = parser.load(config_file)

    if not isinstance(config_file_data, dict):
        raise ConfigError(f"Unable to parse config file: {config_path}")

    return config_file_data


class Configs:
    """Define a coordinator of various Config objects."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize.

        Args:
            config: Raw configuration data.
        """
        self._configs: dict[str, Config] = {}
        self._config_file_parser = YAML(typ="safe")

        if config_path := config.get(CONF_CONFIG):
            config_file_config = load_config_from_file(config_path)
        else:
            config_file_config = {}

        # Store the default config:
        default_config = config | config_file_config
        self._configs[CONF_DEFAULT] = self._validate_config(default_config)

        # Store configs for any gateways:
        gateways_file_config = config_file_config.get(CONF_GATEWAYS, {})
        for passkey, gateway_config in gateways_file_config.items():
            self._configs[passkey] = self._validate_config(
                default_config | gateway_config
            )

    def __repr__(self) -> str:
        """Define a string representation of this object.

        Returns:
            A string representation.
        """
        return f"<Configs _configs={self._configs}"

    def _validate_config(self, config: dict[str, Any]) -> Config:
        """Validate a config.

        Args:
            config: A config to validate.

        Raises:
            ConfigError: Raises if the config is invalid.
        """
        try:
            return Config.model_validate(config)
        except ValidationError as err:
            raise ConfigError(err) from err

    @property
    def default_config(self) -> Config:
        """Return the default config.

        Returns:
            A parsed Config object.
        """
        return self._configs[CONF_DEFAULT]

    def get(self, passkey: str) -> Config:
        """Get the config for a particular passkey (returning the default if none).

        Args:
            passkey: An Ecowitt passkey.

        Returns:
            A parsed Config object.
        """
        return self._configs.get(passkey, self.default_config)

    def iterate(self) -> Generator[Config, None, None]:
        """Get a generator to loop through all stored Config objects.

        Returns:
            An Generator of all stored Config objects.
        """
        return (config for config in self._configs.values())
