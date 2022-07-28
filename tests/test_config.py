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
    ENV_BATTERY_OVERRIDE,
    ENV_DEFAULT_BATTERY_STRATEGY,
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
        ENV_BATTERY_OVERRIDE
    ] = "testbatt0=boolean;testbatt1=numeric;testbatt2=percentage"
    config = Config(config)
    assert config.battery_overrides == {
        "testbatt0": BatteryStrategy.BOOLEAN,
        "testbatt1": BatteryStrategy.NUMERIC,
        "testbatt2": BatteryStrategy.PERCENTAGE,
    }
    os.environ.pop(ENV_BATTERY_OVERRIDE)


@pytest.mark.parametrize(
    "config",
    [
        {
            **TEST_CONFIG_JSON,
            CONF_BATTERY_OVERRIDES: (
                "testbatt0;boolean",
                "testbatt1=numeric",
            ),
        },
    ],
)
def test_battery_overrides_error(config):
    """Test handling invalid battery configs."""
    with pytest.raises(ConfigError):
        _ = Config(config)

    os.environ[ENV_DEFAULT_BATTERY_STRATEGY] = "some-random-string"
    with pytest.raises(ConfigError):
        _ = Config(config)
    os.environ.pop(ENV_DEFAULT_BATTERY_STRATEGY)


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
    assert "Missing required option: --mqtt-broker" in str(err)


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
    "legacy_env_var,new_env_var,value",
    [
        (LEGACY_ENV_ENDPOINT, ENV_ENDPOINT, "/data/output"),
        (LEGACY_ENV_HASS_DISCOVERY, ENV_HASS_DISCOVERY, "True"),
        (LEGACY_ENV_HASS_DISCOVERY_PREFIX, ENV_HASS_DISCOVERY_PREFIX, "homeassistant"),
        (LEGACY_ENV_HASS_ENTITY_ID_PREFIX, ENV_HASS_ENTITY_ID_PREFIX, "ecowitt"),
        (LEGACY_ENV_INPUT_UNIT_SYSTEM, ENV_INPUT_UNIT_SYSTEM, "imperial"),
        (LEGACY_ENV_LOG_LEVEL, ENV_VERBOSE, "DEBUG"),
        (LEGACY_ENV_MQTT_BROKER, ENV_MQTT_BROKER, "127.0.0.1"),
        (LEGACY_ENV_MQTT_PASSWORD, ENV_MQTT_PASSWORD, "password"),
        (LEGACY_ENV_MQTT_PORT, ENV_MQTT_PORT, "1883"),
        (LEGACY_ENV_MQTT_TOPIC, ENV_MQTT_TOPIC, "topic"),
        (LEGACY_ENV_MQTT_USERNAME, ENV_MQTT_USERNAME, "username"),
        (LEGACY_ENV_OUTPUT_UNIT_SYSTEM, ENV_OUTPUT_UNIT_SYSTEM, "imperial"),
        (LEGACY_ENV_PORT, ENV_PORT, "8080"),
        (LEGACY_ENV_RAW_DATA, ENV_RAW_DATA, "True"),
    ],
)
def test_deprecated_env_var(caplog, config, legacy_env_var, new_env_var, value):
    """Test logging the usage of a deprecated environment variable."""
    os.environ[legacy_env_var] = value
    _ = Config(config)
    assert any(
        m
        for m in caplog.messages
        if f"Environment variable {legacy_env_var} is deprecated; use {new_env_var} instead"
        in m
    )
    os.environ.pop(legacy_env_var)
