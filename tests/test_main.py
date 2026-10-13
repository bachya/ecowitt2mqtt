"""Test the main entrypoint."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from ecowitt2mqtt.__main__ import get_cli_arguments, get_env_vars, main
from ecowitt2mqtt.config import ConfigError, Configs
from ecowitt2mqtt.const import (
    CONF_HASS_EXPIRE_AFTER,
    CONF_MQTT_BROKER,
    CONF_MQTT_TOPIC,
    CONF_VERBOSE,
    ENV_HASS_EXPIRE_AFTER,
    ENV_VERBOSE,
)
from tests.common import TEST_CONFIG_JSON


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


def test_hass_expire_after_cli_and_env() -> None:
    """Test Home Assistant expiration CLI and environment options."""
    assert get_cli_arguments(["--hass-expire-after", "3600"]) == {
        CONF_HASS_EXPIRE_AFTER: "3600"
    }
    assert (
        Configs(
            TEST_CONFIG_JSON | get_cli_arguments(["--hass-expire-after", "3600"])
        ).default_config.hass_expire_after
        == 3600
    )
    os.environ[ENV_HASS_EXPIRE_AFTER] = "3600"
    try:
        assert get_env_vars() == {CONF_HASS_EXPIRE_AFTER: "3600"}
        assert (
            Configs(TEST_CONFIG_JSON | get_env_vars()).default_config.hass_expire_after
            == 3600
        )
    finally:
        os.environ.pop(ENV_HASS_EXPIRE_AFTER)


def test_hass_expire_after_invalid_cli_value() -> None:
    """Test invalid CLI expiration values fail configuration validation."""
    arguments = get_cli_arguments(["--hass-expire-after", "not-an-integer"])
    with pytest.raises(ConfigError):
        _ = Configs(TEST_CONFIG_JSON | arguments)


def test_main() -> None:
    """Test the main entrypoint.

    This is effectively a quick sanity check to ensure that the CLI doesn't blow up.
    """
    with (
        patch(
            "sys.argv",
            [
                "ecowitt2mqtt",
                "--mqtt-broker",
                "127.0.0.1",
                "--mqtt-topic",
                "Test",
                "--diagnostics",
            ],
        ),
        patch("ecowitt2mqtt.core.Ecowitt.async_start"),
    ):
        main()
