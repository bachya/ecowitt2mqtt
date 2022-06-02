"""Define tests for configuration management."""
import json
import os

import pytest

from ecowitt2mqtt.config import Config, ConfigError
from ecowitt2mqtt.const import (
    CONF_BATTERY_CONFIG,
    CONF_MQTT_BROKER,
    CONF_MQTT_TOPIC,
    ENV_BATTERY_CONFIG,
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
from ecowitt2mqtt.util.calculator.battery import BatteryConfig

from tests.common import (
    TEST_ENDPOINT,
    TEST_MQTT_BROKER,
    TEST_MQTT_TOPIC,
    TEST_PORT,
    TEST_RAW_JSON,
    TEST_RAW_YAML,
)


def test_battery_config_cli_options(config):
    """Test battery configs provided by CLI options."""
    config = Config(
        {**config, **{"battery_config": ("wh65batt0=raw", "wh65batt1=numeric")}}
    )
    assert config.battery_config == {
        "wh65batt0": BatteryConfig.RAW,
        "wh65batt1": BatteryConfig.NUMERIC,
    }


@pytest.mark.parametrize(
    "raw_config",
    [
        json.dumps(
            {
                CONF_BATTERY_CONFIG: {"wh65batt0": "raw", "wh65batt1": "numeric"},
                CONF_MQTT_BROKER: TEST_MQTT_BROKER,
                CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
            }
        )
    ],
)
def test_battery_config_config_file(config):
    """Test battery configs provided by a config file."""
    config = Config(config)
    assert config.battery_config == {
        "wh65batt0": BatteryConfig.RAW,
        "wh65batt1": BatteryConfig.NUMERIC,
    }


def test_battery_config_error(config):
    """Test handling invalid battery configs."""
    with pytest.raises(ConfigError):
        _ = Config(
            {**config, **{"battery_config": ("wh65batt0;raw", "wh65batt1=numeric")}}
        )

    os.environ[ENV_BATTERY_CONFIG] = "some-random-string"
    with pytest.raises(ConfigError):
        _ = Config(config)


def test_battery_config_env_vars(config):
    """Test battery configs provided by environment variables."""
    os.environ[ENV_BATTERY_CONFIG] = "wh65batt0=raw;wh65batt1=numeric"
    config = Config(config)
    assert config.battery_config == {
        "wh65batt0": BatteryConfig.RAW,
        "wh65batt1": BatteryConfig.NUMERIC,
    }
    os.environ.pop(ENV_BATTERY_CONFIG)


def test_battery_config_missing(config):
    """Test that missing battery configs doesn't cause an issue."""
    config = Config(config)
    assert config.battery_config == {}


@pytest.mark.parametrize("raw_config", [TEST_RAW_JSON, TEST_RAW_YAML])
def test_config_file(config):
    """Test successfully loading a valid config file."""
    config = Config(config)
    assert config.endpoint == TEST_ENDPOINT
    assert config.port == TEST_PORT


@pytest.mark.parametrize("raw_config", ["{}"])
def test_config_file_empty(config):
    """Test an empty config file with no overrides."""
    with pytest.raises(ConfigError) as err:
        _ = Config(config)
    assert "Missing required option: --mqtt-broker" in str(err)


def test_config_file_overrides(config):
    """Test a config file with overrides."""
    config = Config({**config, **{CONF_MQTT_BROKER: "192.168.1.100"}})
    assert config.mqtt_broker == "192.168.1.100"


@pytest.mark.parametrize("raw_config", ["Fake configuration!"])
def test_config_file_unparsable(config):
    """Test a config file that can't be parsed as JSON or YAML."""
    with pytest.raises(ConfigError) as err:
        _ = Config(config)
    assert "Unable to parse config file" in str(err)


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
