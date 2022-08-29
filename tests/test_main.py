"""Test the main entrypoint."""
import os
import sys
from unittest.mock import patch

import pytest

from ecowitt2mqtt.__main__ import get_cli_arguments, get_env_vars, main
from ecowitt2mqtt.const import (
    CONF_MQTT_BROKER,
    CONF_MQTT_TOPIC,
    CONF_VERBOSE,
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
    os.environ[legacy_env_var] = value
    _ = get_env_vars()
    assert any(
        m
        for m in caplog.messages
        if f"Environment variable {legacy_env_var} is deprecated; use {new_env_var} instead"
        in m
    )
    os.environ.pop(legacy_env_var)


def test_get_cli_arguments():
    """Test getting all set CLI arguments."""
    cli_arguments = get_cli_arguments(
        ["--mqtt-broker", "127.0.0.1", "--mqtt-topic", "Test"]
    )
    assert cli_arguments == {CONF_MQTT_BROKER: "127.0.0.1", CONF_MQTT_TOPIC: "Test"}


def test_get_env_vars():
    """Test getting all set environment variables."""
    os.environ[ENV_VERBOSE] = "TRUE"
    env_vars = get_env_vars()
    assert env_vars == {CONF_VERBOSE: "TRUE"}
    os.environ.pop(ENV_VERBOSE)


def test_main():
    """Test the main entrypoint.

    This is effectively a quick sanity check to ensure that the CLI doesn't blow up.
    """
    with patch(
        "sys.argv",
        [
            "ecowitt2mqtt",
            "--mqtt-broker",
            "127.0.0.1",
            "--mqtt-topic",
            "Test",
            "--diagnostics",
        ],
    ), patch("ecowitt2mqtt.core.Ecowitt.async_start"):
        main()
