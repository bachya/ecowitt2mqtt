"""Define tests for the CLI."""
import logging

import pytest
from typer.testing import CliRunner

from ecowitt2mqtt.cli import APP
from ecowitt2mqtt.const import (
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
from ecowitt2mqtt.helpers.logging import TyperLoggerHandler

from tests.common import TEST_RAW_JSON, TEST_RAW_YAML


@pytest.mark.parametrize("config", [TEST_RAW_JSON, TEST_RAW_YAML])
def test_config_file(caplog, config_filepath, runner):
    """Test successfully loading a valid config file."""
    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v", "-c", config_filepath])
    assert "Loaded Config" in caplog.messages[1]
    assert not any(
        level for _, level, _ in caplog.record_tuples if level == logging.ERROR
    )


@pytest.mark.parametrize("config", ["{}"])
def test_config_file_empty(caplog, config_filepath, runner):
    """Test an empty config file with no overrides."""
    runner.invoke(APP, ["-c", config_filepath])
    assert "Missing required option: --mqtt-broker" in caplog.messages[0]


def test_config_file_overrides_cli(caplog, config_filepath, runner):
    """Test a config file with CLI option overrides."""
    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v", "-c", config_filepath, "-b", "192.168.1.100"])
    assert "'mqtt_broker': '192.168.1.100'" in caplog.messages[0]


@pytest.mark.parametrize("runner", [CliRunner(env={ENV_PORT: "8081"})])
def test_config_file_overrides_env_vars(caplog, config_filepath, runner):
    """Test a config file with environment variable overrides."""
    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v", "-c", config_filepath])
    assert "'port': 8081" in caplog.messages[0]


@pytest.mark.parametrize("config", ["Fake configuration!"])
def test_config_file_unparsable(caplog, config_filepath, runner):
    """Test a config file that can't be parsed as JSON or YAML."""
    runner.invoke(APP, ["-c", config_filepath])
    assert "Unable to parse config file" in caplog.messages[0]


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
def test_deprecated_env_var(caplog, legacy_env_var, new_env_var, value):
    """Test logging the usage of a deprecated environment variable."""
    runner = CliRunner(env={legacy_env_var: value})
    runner.invoke(APP, [])
    assert any(
        m
        for m in caplog.messages
        if f"Environment variable {legacy_env_var} is deprecated; use {new_env_var} instead"
        in m
    )


@pytest.mark.parametrize(
    "args,missing_args_str",
    [
        ([], "--mqtt-broker"),
        (["-b", "127.0.0.1"], "--mqtt-topic or --hass-discovery"),
    ],
)
def test_missing_required_options(args, caplog, missing_args_str, runner):
    """Test that missing required options are handled."""
    runner.invoke(APP, args)
    assert caplog.messages[0] == f"Missing required option: {missing_args_str}"


def test_startup_logging(caplog, runner):
    """Test startup logging at various levels."""
    caplog.set_level(logging.INFO)
    runner.invoke(APP, [])
    info_log_messages = caplog.messages

    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v"])
    debug_log_messages = caplog.messages

    # There should be more DEBUG-level logs than INFO-level logs:
    assert len(debug_log_messages) > len(info_log_messages)


def test_typer_logging_handler(caplog, runner):
    """Test the TyperLoggerHandler helper."""
    caplog.set_level(logging.DEBUG)

    handler = TyperLoggerHandler()
    logger = logging.getLogger("test")
    logger.addHandler(handler)

    logger.critical("Test Critical Message")
    logger.debug("Test Debug Message")
    logger.error("Test Error Message")
    logger.info("Test Info Message")
    logger.warning("Test Warning Message")

    assert len(caplog.messages) == 5
