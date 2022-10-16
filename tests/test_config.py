"""Define tests for configuration management."""
import json
import os

import pytest

from ecowitt2mqtt.config import ConfigError, Configs
from ecowitt2mqtt.const import (
    CONF_BATTERY_OVERRIDES,
    CONF_CONFIG,
    CONF_DEFAULT_BATTERY_STRATEGY,
    CONF_GATEWAYS,
    CONF_MQTT_BROKER,
    CONF_MQTT_TOPIC,
    CONF_OUTPUT_UNIT_ACCUMULATED_PRECIPITATION,
    CONF_OUTPUT_UNIT_DISTANCE,
    CONF_OUTPUT_UNIT_HUMIDITY,
    CONF_OUTPUT_UNIT_ILLUMINANCE,
    CONF_OUTPUT_UNIT_PRECIPITATION_RATE,
    CONF_OUTPUT_UNIT_PRESSURE,
    CONF_OUTPUT_UNIT_SPEED,
    CONF_OUTPUT_UNIT_TEMPERATURE,
    CONF_VERBOSE,
    ENV_BATTERY_OVERRIDES,
    ILLUMINANCE_LUX,
    LENGTH_KILOMETERS,
    PRECIPITATION_MILLIMETERS,
    PRECIPITATION_MILLIMETERS_PER_HOUR,
    PRESSURE_HPA,
    SPEED_KILOMETERS_PER_HOUR,
    TEMP_CELSIUS,
    VOLUME_GRAMS_PER_CUBIC_METER,
)
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy

from tests.common import (
    TEST_CONFIG_JSON,
    TEST_CONFIG_RAW_YAML,
    TEST_ENDPOINT,
    TEST_MQTT_BROKER,
    TEST_MQTT_TOPIC,
    TEST_PORT,
)


@pytest.mark.parametrize(
    "config",
    [
        {
            **TEST_CONFIG_JSON,
            CONF_BATTERY_OVERRIDES: (
                "testbatt0=boolean",
                "testbatt1=numeric",
                "testbatt2=percentage",
            ),
        },
    ],
)
def test_battery_overrides_cli_options(config):
    """Test battery configs provided by CLI options."""
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
            {
                **TEST_CONFIG_JSON,
                CONF_BATTERY_OVERRIDES: {
                    "testbatt0": "boolean",
                    "testbatt1": "numeric",
                    "testbatt2": "percentage",
                },
            }
        )
    ],
)
def test_battery_overrides_config_file(config_filepath):
    """Test battery configs provided by a config file."""
    configs = Configs({CONF_CONFIG: config_filepath})
    assert configs.default_config.battery_overrides == {
        "testbatt0": BatteryStrategy.BOOLEAN,
        "testbatt1": BatteryStrategy.NUMERIC,
        "testbatt2": BatteryStrategy.PERCENTAGE,
    }


def test_battery_overrides_env_vars(config):
    """Test battery configs provided by environment variables."""
    os.environ[
        ENV_BATTERY_OVERRIDES
    ] = "testbatt0=boolean;testbatt1=numeric;testbatt2=percentage"
    configs = Configs(config)
    assert configs.default_config.battery_overrides == {
        "testbatt0": BatteryStrategy.BOOLEAN,
        "testbatt1": BatteryStrategy.NUMERIC,
        "testbatt2": BatteryStrategy.PERCENTAGE,
    }
    os.environ.pop(ENV_BATTERY_OVERRIDES)


@pytest.mark.parametrize(
    "config",
    [
        {
            **TEST_CONFIG_JSON,
            CONF_BATTERY_OVERRIDES: ("testbatt0;boolean",),
        },
    ],
)
def test_battery_overrides_error(config):
    """Test handling invalid battery configs."""
    with pytest.raises(ConfigError):
        _ = Configs(config)

    os.environ[ENV_BATTERY_OVERRIDES] = "some-random-string"
    with pytest.raises(ConfigError):
        _ = Configs(config)
    os.environ.pop(ENV_BATTERY_OVERRIDES)


def test_battery_overrides_missing(config):
    """Test that missing battery configs doesn't cause an issue."""
    configs = Configs(config)
    assert configs.default_config.battery_overrides == {}


@pytest.mark.parametrize(
    "raw_config",
    [
        json.dumps(TEST_CONFIG_JSON),
        TEST_CONFIG_RAW_YAML,
    ],
)
def test_config_file(config_filepath):
    """Test successfully loading a valid config file."""
    configs = Configs({CONF_CONFIG: config_filepath})
    assert configs.default_config.endpoint == TEST_ENDPOINT
    assert configs.default_config.port == TEST_PORT


@pytest.mark.parametrize("raw_config", ["{}"])
def test_config_file_empty(config_filepath):
    """Test an empty config file with no overrides."""
    with pytest.raises(ConfigError) as err:
        _ = Configs({CONF_CONFIG: config_filepath})
    assert "Must provide an MQTT topic or enable Home Assistant MQTT Discovery" in str(
        err
    )


@pytest.mark.parametrize(
    "raw_config",
    [
        json.dumps(
            {
                **TEST_CONFIG_JSON,
                CONF_GATEWAYS: {
                    "passkey123": {
                        CONF_MQTT_BROKER: "my.mqtt.local",
                        CONF_MQTT_TOPIC: "Some Topic",
                    }
                },
            }
        ),
    ],
)
def test_config_file_multiple_gateways(config_filepath):
    """Test successfully loading a config file with multiple gateways."""
    configs = Configs({CONF_CONFIG: config_filepath})

    # Test that the default config is returned with an invalid passkey:
    assert configs.get("some_other_passkey") == configs.default_config

    # Test three values of the default config: one that should be the same no matter
    # what and two that will be different for a gateway config:
    assert configs.default_config.endpoint == TEST_ENDPOINT
    assert configs.default_config.mqtt_broker == TEST_MQTT_BROKER
    assert configs.default_config.mqtt_topic == TEST_MQTT_TOPIC

    gateway_config = configs.get("passkey123")
    assert gateway_config.endpoint == TEST_ENDPOINT
    assert gateway_config.mqtt_broker == "my.mqtt.local"
    assert gateway_config.mqtt_topic == "Some Topic"


@pytest.mark.parametrize(
    "config",
    [
        {
            **TEST_CONFIG_JSON,
            CONF_MQTT_BROKER: "192.168.1.100",
        }
    ],
)
def test_config_file_overrides(config):
    """Test a config file with overrides."""
    configs = Configs(config)
    assert configs.default_config.mqtt_broker == "192.168.1.100"


@pytest.mark.parametrize("raw_config", ["Fake configuration!"])
def test_config_file_unparsable(config_filepath):
    """Test a config file that can't be parsed as JSON or YAML."""
    with pytest.raises(ConfigError) as err:
        _ = Configs({CONF_CONFIG: config_filepath})
    assert "Unable to parse config file" in str(err)


@pytest.mark.parametrize(
    "config",
    [
        {
            **TEST_CONFIG_JSON,
            CONF_DEFAULT_BATTERY_STRATEGY: BatteryStrategy.NUMERIC,
        },
    ],
)
def test_default_battery_strategy(config):
    """Test the default battery config."""
    configs = Configs(config)
    assert configs.default_config.default_battery_strategy == BatteryStrategy.NUMERIC


@pytest.mark.parametrize(
    "config",
    [
        {
            **TEST_CONFIG_JSON,
            CONF_VERBOSE: "This isn't a real value",
        },
    ],
)
def test_invalid_boolean_config_validation(config):
    """Test an invalid boolean config validation."""
    with pytest.raises(ConfigError):
        _ = Configs(config)


@pytest.mark.parametrize(
    "config_option,value",
    [
        (CONF_OUTPUT_UNIT_ACCUMULATED_PRECIPITATION, PRECIPITATION_MILLIMETERS),
        (CONF_OUTPUT_UNIT_DISTANCE, LENGTH_KILOMETERS),
        (CONF_OUTPUT_UNIT_HUMIDITY, VOLUME_GRAMS_PER_CUBIC_METER),
        (CONF_OUTPUT_UNIT_ILLUMINANCE, ILLUMINANCE_LUX),
        (CONF_OUTPUT_UNIT_PRECIPITATION_RATE, PRECIPITATION_MILLIMETERS_PER_HOUR),
        (CONF_OUTPUT_UNIT_PRESSURE, PRESSURE_HPA),
        (CONF_OUTPUT_UNIT_SPEED, SPEED_KILOMETERS_PER_HOUR),
        (CONF_OUTPUT_UNIT_TEMPERATURE, TEMP_CELSIUS),
    ],
)
def test_output_units(config_option, value):
    """Test output unit classes."""
    config = {**TEST_CONFIG_JSON, config_option: value}
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
def test_output_units_invalid(config_option):
    """Test output unit classes with invalid values."""
    config = {**TEST_CONFIG_JSON, config_option: "Some Fake Value"}
    with pytest.raises(ConfigError):
        _ = Configs(config)


@pytest.mark.parametrize(
    "config,verbose_value",
    [
        (
            {
                **TEST_CONFIG_JSON,
                CONF_VERBOSE: "yes",
            },
            True,
        ),
        (
            {
                **TEST_CONFIG_JSON,
                CONF_VERBOSE: "disable",
            },
            False,
        ),
        (
            {
                **TEST_CONFIG_JSON,
                CONF_VERBOSE: 5,
            },
            True,
        ),
    ],
)
def test_valid_boolean_config_validation(config, verbose_value):
    """Test that various boolean config validations work."""
    configs = Configs(config)
    assert configs.default_config.verbose is verbose_value
