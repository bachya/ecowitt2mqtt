"""Define tests for configuration management."""

from __future__ import annotations

import json
import os
from typing import Any

import pytest

from ecowitt2mqtt.config import ConfigError, Configs
from ecowitt2mqtt.const import (
    CONF_BATTERY_OVERRIDES,
    CONF_BOOLEAN_BATTERY_TRUE_VALUE,
    CONF_CONFIG,
    CONF_DEFAULT_BATTERY_STRATEGY,
    CONF_GATEWAYS,
    CONF_MQTT_BROKER,
    CONF_MQTT_PASSWORD,
    CONF_MQTT_TOPIC,
    CONF_MQTT_USERNAME,
    CONF_OUTPUT_UNIT_ACCUMULATED_PRECIPITATION,
    CONF_OUTPUT_UNIT_DISTANCE,
    CONF_OUTPUT_UNIT_HUMIDITY,
    CONF_OUTPUT_UNIT_ILLUMINANCE,
    CONF_OUTPUT_UNIT_PRECIPITATION_RATE,
    CONF_OUTPUT_UNIT_PRESSURE,
    CONF_OUTPUT_UNIT_SPEED,
    CONF_OUTPUT_UNIT_TEMPERATURE,
    CONF_PORT,
    CONF_PRECISION,
    CONF_VERBOSE,
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
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy
from ecowitt2mqtt.helpers.server import InputDataFormat
from tests.common import (
    TEST_CONFIG_JSON,
    TEST_CONFIG_RAW_YAML,
    TEST_ENDPOINT,
    TEST_HASS_DISCOVERY_PREFIX,
    TEST_MQTT_BROKER,
    TEST_MQTT_PASSWORD,
    TEST_MQTT_PORT,
    TEST_MQTT_TOPIC,
    TEST_MQTT_USERNAME,
    TEST_PORT,
)


@pytest.mark.parametrize(
    "config",
    [
        TEST_CONFIG_JSON
        | {
            CONF_BATTERY_OVERRIDES: (
                "testbatt0=boolean",
                "testbatt1=numeric",
                "testbatt2=percentage",
            )
        }
    ],
)
def test_battery_overrides_cli_options(config: dict[str, Any]) -> None:
    """Test battery configs provided by CLI options.

    Args:
        config: A configuration dictionary.
    """
    configs = Configs(config)
    assert configs.default_config.battery_overrides == {
        "testbatt0": BatteryStrategy.BOOLEAN,
        "testbatt1": BatteryStrategy.NUMERIC,
        "testbatt2": BatteryStrategy.PERCENTAGE,
    }
    assert configs.default_config.default_battery_strategy == BatteryStrategy.BOOLEAN


@pytest.mark.parametrize(
    "raw_config",
    [
        json.dumps(
            TEST_CONFIG_JSON
            | {
                CONF_BATTERY_OVERRIDES: {
                    "testbatt0": "boolean",
                    "testbatt1": "numeric",
                    "testbatt2": "percentage",
                }
            },
        )
    ],
)
def test_battery_overrides_config_file(config_filepath: str) -> None:
    """Test battery configs provided by a config file.

    Args:
        config_filepath: A configuration file path.
    """
    configs = Configs({CONF_CONFIG: config_filepath})
    assert configs.default_config.battery_overrides == {
        "testbatt0": BatteryStrategy.BOOLEAN,
        "testbatt1": BatteryStrategy.NUMERIC,
        "testbatt2": BatteryStrategy.PERCENTAGE,
    }


def test_battery_overrides_env_vars(config: dict[str, Any]) -> None:
    """Test battery configs provided by environment variables.

    Args:
        config: A configuration dictionary.
    """
    os.environ[ENV_BATTERY_OVERRIDES] = (
        "testbatt0=boolean;testbatt1=numeric;testbatt2=percentage"
    )
    configs = Configs(config)
    assert configs.default_config.battery_overrides == {
        "testbatt0": BatteryStrategy.BOOLEAN,
        "testbatt1": BatteryStrategy.NUMERIC,
        "testbatt2": BatteryStrategy.PERCENTAGE,
    }
    os.environ.pop(ENV_BATTERY_OVERRIDES)


@pytest.mark.parametrize(
    "config", [TEST_CONFIG_JSON | {CONF_BATTERY_OVERRIDES: ("testbatt0;boolean",)}]
)
def test_battery_overrides_error(config: dict[str, Any]) -> None:
    """Test handling invalid battery configs.

    Args:
        config: A configuration dictionary.
    """
    with pytest.raises(ConfigError):
        _ = Configs(config)

    os.environ[ENV_BATTERY_OVERRIDES] = "some-random-string"
    with pytest.raises(ConfigError):
        _ = Configs(config)
    os.environ.pop(ENV_BATTERY_OVERRIDES)


def test_battery_overrides_missing(config: dict[str, Any]) -> None:
    """Test that missing battery configs doesn't cause an issue.

    Args:
        config: A configuration dictionary.
    """
    configs = Configs(config)
    assert configs.default_config.battery_overrides == {}


@pytest.mark.parametrize(
    "config,value",
    [
        (TEST_CONFIG_JSON | {CONF_BOOLEAN_BATTERY_TRUE_VALUE: "0"}, 0),
        (TEST_CONFIG_JSON | {CONF_BOOLEAN_BATTERY_TRUE_VALUE: "1"}, 1),
        (TEST_CONFIG_JSON | {CONF_BOOLEAN_BATTERY_TRUE_VALUE: "2"}, None),
    ],
)
def test_boolean_battery_true_value(config: dict[str, Any], value: int | None) -> None:
    """Test configuring the default True value for a boolean battery.

    Args:
        config: A configuration dictionary.
        value: The expected value.
    """
    if value is not None:
        configs = Configs(config)
        assert configs.default_config.boolean_battery_true_value == value
    else:
        with pytest.raises(ConfigError):
            _ = Configs(config)


@pytest.mark.parametrize(
    "raw_config",
    [
        json.dumps(TEST_CONFIG_JSON),
        TEST_CONFIG_RAW_YAML,
    ],
)
def test_config_file(config_filepath: str) -> None:
    """Test successfully loading a valid config file.

    Args:
        config_filepath: A configuration file path.
    """
    configs = Configs({CONF_CONFIG: config_filepath})
    assert configs.default_config.battery_overrides == {}
    assert configs.default_config.default_battery_strategy == BatteryStrategy.BOOLEAN
    assert configs.default_config.diagnostics is False
    assert configs.default_config.disable_calculated_data is False
    assert configs.default_config.endpoint == TEST_ENDPOINT
    assert configs.default_config.hass_discovery is False
    assert configs.default_config.hass_discovery_prefix == TEST_HASS_DISCOVERY_PREFIX
    assert configs.default_config.hass_entity_id_prefix is None
    assert configs.default_config.input_data_format == InputDataFormat.ECOWITT
    assert configs.default_config.input_unit_system == UnitSystem.IMPERIAL
    assert configs.default_config.mqtt_broker == TEST_MQTT_BROKER
    assert configs.default_config.mqtt_password == TEST_MQTT_PASSWORD
    assert configs.default_config.mqtt_port == TEST_MQTT_PORT
    assert configs.default_config.mqtt_retain is False
    assert configs.default_config.mqtt_tls is False
    assert configs.default_config.mqtt_topic == TEST_MQTT_TOPIC
    assert configs.default_config.mqtt_username == TEST_MQTT_USERNAME
    assert configs.default_config.output_unit_system == UnitSystem.IMPERIAL
    assert configs.default_config.output_unit_accumulated_precipitation is None
    assert configs.default_config.output_unit_distance is None
    assert configs.default_config.output_unit_humidity is None
    assert configs.default_config.output_unit_illuminance is None
    assert configs.default_config.output_unit_precipitation_rate is None
    assert configs.default_config.output_unit_pressure is None
    assert configs.default_config.output_unit_speed is None
    assert configs.default_config.output_unit_temperature is None
    assert configs.default_config.port == TEST_PORT
    assert configs.default_config.precision is None
    assert configs.default_config.raw_data is False
    assert configs.default_config.verbose is False


@pytest.mark.parametrize("raw_config", ["{}"])
def test_config_file_empty(config_filepath: str) -> None:
    """Test an empty config file with no overrides.

    Args:
        config_filepath: A configuration file path.
    """
    with pytest.raises(ConfigError) as err:
        _ = Configs({CONF_CONFIG: config_filepath})
    assert "must provide at least one of" in str(err)


@pytest.mark.parametrize(
    "raw_config",
    [
        json.dumps(
            TEST_CONFIG_JSON
            | {
                CONF_GATEWAYS: {
                    "passkey123": {
                        CONF_MQTT_BROKER: "my.mqtt.local",
                        CONF_MQTT_TOPIC: "Some Topic",
                    }
                }
            },
        ),
    ],
)
def test_config_file_multiple_gateways(config_filepath: str) -> None:
    """Test successfully loading a config file with multiple gateways.

    Args:
        config_filepath: A configuration file path.
    """
    configs = Configs({CONF_CONFIG: config_filepath})

    # Test that the default config is returned with an invalid passkey:
    assert configs.get("some_other_passkey") == configs.default_config

    # Test three values of the default config: one that should be the same no matter
    # what and two that will be different for a gateway config:
    assert configs.default_config.default_battery_strategy == BatteryStrategy.BOOLEAN
    assert configs.default_config.endpoint == TEST_ENDPOINT
    assert configs.default_config.mqtt_broker == TEST_MQTT_BROKER
    assert configs.default_config.mqtt_topic == TEST_MQTT_TOPIC

    gateway_config = configs.get("passkey123")
    assert configs.default_config.default_battery_strategy == BatteryStrategy.BOOLEAN
    assert gateway_config.endpoint == TEST_ENDPOINT
    assert gateway_config.mqtt_broker == "my.mqtt.local"
    assert gateway_config.mqtt_topic == "Some Topic"


@pytest.mark.parametrize(
    "raw_config",
    [
        json.dumps(
            TEST_CONFIG_JSON
            | {
                CONF_GATEWAYS: {
                    "passkey123": {
                        CONF_MQTT_BROKER: "my.mqtt.local",
                        CONF_MQTT_TOPIC: "Some Topic",
                        CONF_PORT: "WHOOPS",
                    }
                }
            },
        ),
    ],
)
def test_config_file_invalid_gateway(config_filepath: str) -> None:
    """Test successfully loading a config file with an invalid gateway.

    Args:
        config_filepath: A configuration file path.
    """
    with pytest.raises(ConfigError):
        _ = Configs({CONF_CONFIG: config_filepath})


@pytest.mark.parametrize(
    "config", [TEST_CONFIG_JSON | {CONF_MQTT_BROKER: "192.168.1.100"}]
)
def test_config_file_overrides(config: dict[str, Any]) -> None:
    """Test a config file with overrides.

    Args:
        config: A configuration dictionary.
    """
    configs = Configs(config)
    assert configs.default_config.mqtt_broker == "192.168.1.100"


@pytest.mark.parametrize("raw_config", ["Fake configuration!"])
def test_config_file_unparsable(config_filepath: str) -> None:
    """Test a config file that can't be parsed as JSON or YAML.

    Args:
        config_filepath: A configuration file path.
    """
    with pytest.raises(ConfigError) as err:
        _ = Configs({CONF_CONFIG: config_filepath})
    assert "Unable to parse config file" in str(err)


@pytest.mark.parametrize(
    "config",
    [TEST_CONFIG_JSON | {CONF_DEFAULT_BATTERY_STRATEGY: BatteryStrategy.NUMERIC}],
)
def test_default_battery_strategy(config: dict[str, Any]) -> None:
    """Test the default battery config.

    Args:
        config: A configuration dictionary.
    """
    configs = Configs(config)
    assert configs.default_config.default_battery_strategy == BatteryStrategy.NUMERIC


@pytest.mark.parametrize(
    "config", [TEST_CONFIG_JSON | {CONF_VERBOSE: "This isn't a real value"}]
)
def test_invalid_boolean_config_validation(config: dict[str, Any]) -> None:
    """Test an invalid boolean config validation.

    Args:
        config: A configuration dictionary.
    """
    with pytest.raises(ConfigError):
        _ = Configs(config)


@pytest.mark.parametrize(
    "config",
    [TEST_CONFIG_JSON | {CONF_PORT: 99999999999}],
)
def test_invalid_port(config: dict[str, Any]) -> None:
    """Test that an invalid port is detected.

    Args:
        config: A configuration dictionary.
    """
    with pytest.raises(ConfigError):
        _ = Configs(config)


@pytest.mark.parametrize(
    "config,valid",
    [
        (
            TEST_CONFIG_JSON
            | {CONF_MQTT_USERNAME: None, CONF_MQTT_PASSWORD: "password"},
            False,
        ),
        (
            TEST_CONFIG_JSON
            | {CONF_MQTT_USERNAME: "username", CONF_MQTT_PASSWORD: None},
            False,
        ),
        (
            TEST_CONFIG_JSON
            | {CONF_MQTT_USERNAME: "username", CONF_MQTT_PASSWORD: "password"},
            True,
        ),
    ],
)
def test_mqtt_auth(config: dict[str, Any], valid: bool) -> None:
    """Test that we do the correct thing with various MQTT auth configurations.

    Args:
        config: A configuration dictionary.
        valid: Whether the configuration is valid.
    """
    if valid:
        _ = Configs(config)
    else:
        with pytest.raises(ConfigError):
            _ = Configs(config)


@pytest.mark.parametrize(
    "config_option,value",
    [
        (
            CONF_OUTPUT_UNIT_ACCUMULATED_PRECIPITATION,
            UnitOfAccumulatedPrecipitation.MILLIMETERS,
        ),
        (CONF_OUTPUT_UNIT_DISTANCE, UnitOfLength.KILOMETERS),
        (CONF_OUTPUT_UNIT_HUMIDITY, UnitOfVolume.GRAMS_PER_CUBIC_METER),
        (CONF_OUTPUT_UNIT_ILLUMINANCE, UnitOfIlluminance.LUX),
        (
            CONF_OUTPUT_UNIT_PRECIPITATION_RATE,
            UnitOfPrecipitationRate.MILLIMETERS_PER_HOUR,
        ),
        (CONF_OUTPUT_UNIT_PRESSURE, UnitOfPressure.HPA),
        (CONF_OUTPUT_UNIT_SPEED, UnitOfSpeed.KILOMETERS_PER_HOUR),
        (CONF_OUTPUT_UNIT_TEMPERATURE, UnitOfTemperature.CELSIUS),
    ],
)
def test_output_units(config_option: str, value: str) -> None:
    """Test output unit classes.

    Args:
        config_option: A unit configuration option.
        value: A value to use for the configuration option.
    """
    config = TEST_CONFIG_JSON | {config_option: value}
    configs = Configs(config)
    assert getattr(configs.default_config, config_option) == value


@pytest.mark.parametrize(
    "config_option",
    [
        CONF_OUTPUT_UNIT_ACCUMULATED_PRECIPITATION,
        CONF_OUTPUT_UNIT_DISTANCE,
        CONF_OUTPUT_UNIT_HUMIDITY,
        CONF_OUTPUT_UNIT_ILLUMINANCE,
        CONF_OUTPUT_UNIT_PRECIPITATION_RATE,
        CONF_OUTPUT_UNIT_PRESSURE,
        CONF_OUTPUT_UNIT_SPEED,
        CONF_OUTPUT_UNIT_TEMPERATURE,
    ],
)
def test_output_units_invalid(config_option: str) -> None:
    """Test output unit classes with invalid values.

    Args:
        config_option: A unit configuration option.
    """
    config = TEST_CONFIG_JSON | {config_option: "Some Fake Value"}
    with pytest.raises(ConfigError):
        _ = Configs(config)


def test_precision() -> None:
    """Test whether precision is configured."""
    config = TEST_CONFIG_JSON | {CONF_PRECISION: 2}
    configs = Configs(config)
    assert configs.default_config.precision == 2


@pytest.mark.parametrize(
    "config,is_valid",
    (
        [TEST_CONFIG_JSON | {CONF_PORT: 1883}, True],
        [TEST_CONFIG_JSON | {CONF_PORT: 9000}, True],
        [TEST_CONFIG_JSON | {CONF_PORT: "1883"}, True],
        [TEST_CONFIG_JSON | {CONF_PORT: "Not a port"}, False],
    ),
)
def test_port(config: dict[str, Any], is_valid: bool) -> None:
    """Test validating a port.

    Args:
        config: A configuration dictionary.
        is_valid: Whether the configuration is valid.
    """
    if not is_valid:
        with pytest.raises(ConfigError):
            _ = Configs(config)


@pytest.mark.parametrize(
    "config,verbose_value",
    [
        (TEST_CONFIG_JSON | {CONF_VERBOSE: "yes"}, True),
        (TEST_CONFIG_JSON | {CONF_VERBOSE: "disable"}, False),
        (TEST_CONFIG_JSON | {CONF_VERBOSE: 5}, True),
    ],
)
def test_valid_boolean_config_validation(
    config: dict[str, Any], verbose_value: Any
) -> None:
    """Test that various boolean config validations work.

    Args:
        config: A configuration dictionary.
        verbose_value: A value to the `--verbose` config option.
    """
    configs = Configs(config)
    assert configs.default_config.verbose is verbose_value
