"""Define tests for configuration management."""
import json
import os

import pytest

from ecowitt2mqtt.config import Config, ConfigError
from ecowitt2mqtt.const import (
    CONF_BATTERY_OVERRIDES,
    CONF_CONFIG,
    CONF_DEFAULT_BATTERY_STRATEGY,
    CONF_MQTT_BROKER,
    CONF_VERBOSE,
    ENV_BATTERY_OVERRIDES,
)
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy

from tests.common import (
    TEST_CONFIG_JSON,
    TEST_CONFIG_RAW_YAML,
    TEST_ENDPOINT,
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
    config = Config(config)
    assert config.battery_overrides == {
        "testbatt0": BatteryStrategy.BOOLEAN,
        "testbatt1": BatteryStrategy.NUMERIC,
        "testbatt2": BatteryStrategy.PERCENTAGE,
    }
    assert config.default_battery_strategy == BatteryStrategy.BOOLEAN


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
    config = Config({CONF_CONFIG: config_filepath})
    assert config.battery_overrides == {
        "testbatt0": BatteryStrategy.BOOLEAN,
        "testbatt1": BatteryStrategy.NUMERIC,
        "testbatt2": BatteryStrategy.PERCENTAGE,
    }


def test_battery_overrides_env_vars(config):
    """Test battery configs provided by environment variables."""
    os.environ[
        ENV_BATTERY_OVERRIDES
    ] = "testbatt0=boolean;testbatt1=numeric;testbatt2=percentage"
    config = Config(config)
    assert config.battery_overrides == {
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
        _ = Config(config)

    os.environ[ENV_BATTERY_OVERRIDES] = "some-random-string"
    with pytest.raises(ConfigError):
        _ = Config(config)
    os.environ.pop(ENV_BATTERY_OVERRIDES)


def test_battery_overrides_missing(config):
    """Test that missing battery configs doesn't cause an issue."""
    config = Config(config)
    assert config.battery_overrides == {}


@pytest.mark.parametrize(
    "raw_config",
    [
        json.dumps(TEST_CONFIG_JSON),
        TEST_CONFIG_RAW_YAML,
    ],
)
def test_config_file(config_filepath):
    """Test successfully loading a valid config file."""
    config = Config({CONF_CONFIG: config_filepath})
    assert config.endpoint == TEST_ENDPOINT
    assert config.port == TEST_PORT


@pytest.mark.parametrize("raw_config", ["{}"])
def test_config_file_empty(config_filepath):
    """Test an empty config file with no overrides."""
    with pytest.raises(ConfigError) as err:
        _ = Config({CONF_CONFIG: config_filepath})
    assert "Must provide an MQTT topic or enable Home Assistant MQTT Discovery" in str(
        err
    )


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
    config = Config(config)
    assert config.mqtt_broker == "192.168.1.100"


@pytest.mark.parametrize("raw_config", ["Fake configuration!"])
def test_config_file_unparsable(config_filepath):
    """Test a config file that can't be parsed as JSON or YAML."""
    with pytest.raises(ConfigError) as err:
        _ = Config({CONF_CONFIG: config_filepath})
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
    config = Config(config)
    assert config.default_battery_strategy == BatteryStrategy.NUMERIC


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
        _ = Config(config)


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
    config = Config(config)
    assert config.verbose is verbose_value
