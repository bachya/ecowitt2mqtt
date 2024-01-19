"""Test the main entrypoint."""
from __future__ import annotations

import os
from unittest.mock import Mock, patch

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
)


def test_get_cli_arguments() -> None:
    """Test getting all set CLI arguments."""
    cli_arguments = get_cli_arguments(
        ["--mqtt-broker", "127.0.0.1", "--mqtt-topic", "Test"]
    )
    assert cli_arguments == {CONF_MQTT_BROKER: "127.0.0.1", CONF_MQTT_TOPIC: "Test"}


def test_get_env_vars() -> None:
    """Test getting all set environment variables."""
    os.environ[ENV_VERBOSE] = "TRUE"
    env_vars = get_env_vars()
    assert env_vars == {CONF_VERBOSE: "TRUE"}
    os.environ.pop(ENV_VERBOSE)


def test_main() -> None:
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
