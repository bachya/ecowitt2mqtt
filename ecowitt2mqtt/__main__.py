"""Define the main interface to the CLI."""
from __future__ import annotations

import argparse
import asyncio
import os
import sys
from typing import Any

import uvloop

from ecowitt2mqtt.const import (
    CONF_BATTERY_OVERRIDES,
    CONF_CONFIG,
    CONF_DEFAULT_BATTERY_STRATEGY,
    CONF_DIAGNOSTICS,
    CONF_DISABLE_CALCULATED_DATA,
    CONF_ENDPOINT,
    CONF_HASS_DISCOVERY,
    CONF_HASS_DISCOVERY_PREFIX,
    CONF_HASS_ENTITY_ID_PREFIX,
    CONF_INPUT_UNIT_SYSTEM,
    CONF_MQTT_BROKER,
    CONF_MQTT_PASSWORD,
    CONF_MQTT_PORT,
    CONF_MQTT_RETAIN,
    CONF_MQTT_TLS,
    CONF_MQTT_TOPIC,
    CONF_MQTT_USERNAME,
    CONF_OUTPUT_UNIT_SYSTEM,
    CONF_PORT,
    CONF_RAW_DATA,
    CONF_VERBOSE,
    DEFAULT_ENDPOINT,
    DEFAULT_HASS_DISCOVERY_PREFIX,
    DEFAULT_MQTT_PORT,
    DEFAULT_PORT,
    ENV_BATTERY_OVERRIDES,
    ENV_CONFIG,
    ENV_DEFAULT_BATTERY_STRATEGY,
    ENV_DIAGNOSTICS,
    ENV_DISABLE_CALCULATED_DATA,
    ENV_ENDPOINT,
    ENV_HASS_DISCOVERY,
    ENV_HASS_DISCOVERY_PREFIX,
    ENV_HASS_ENTITY_ID_PREFIX,
    ENV_INPUT_UNIT_SYSTEM,
    ENV_MQTT_BROKER,
    ENV_MQTT_PASSWORD,
    ENV_MQTT_PORT,
    ENV_MQTT_RETAIN,
    ENV_MQTT_TLS,
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
    LOGGER,
    UNIT_SYSTEM_IMPERIAL,
    __version__,
)
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy

DEPRECATED_ENV_VAR_MAP = {
    LEGACY_ENV_ENDPOINT: ENV_ENDPOINT,
    LEGACY_ENV_HASS_DISCOVERY: ENV_HASS_DISCOVERY,
    LEGACY_ENV_HASS_DISCOVERY_PREFIX: ENV_HASS_DISCOVERY_PREFIX,
    LEGACY_ENV_HASS_ENTITY_ID_PREFIX: ENV_HASS_ENTITY_ID_PREFIX,
    LEGACY_ENV_INPUT_UNIT_SYSTEM: ENV_INPUT_UNIT_SYSTEM,
    LEGACY_ENV_LOG_LEVEL: ENV_VERBOSE,
    LEGACY_ENV_MQTT_BROKER: ENV_MQTT_BROKER,
    LEGACY_ENV_MQTT_PASSWORD: ENV_MQTT_PASSWORD,
    LEGACY_ENV_MQTT_PORT: ENV_MQTT_PORT,
    LEGACY_ENV_MQTT_TOPIC: ENV_MQTT_TOPIC,
    LEGACY_ENV_MQTT_USERNAME: ENV_MQTT_USERNAME,
    LEGACY_ENV_OUTPUT_UNIT_SYSTEM: ENV_OUTPUT_UNIT_SYSTEM,
    LEGACY_ENV_PORT: ENV_PORT,
    LEGACY_ENV_RAW_DATA: ENV_RAW_DATA,
}

ENV_VAR_TO_CONF_MAP = {
    ENV_BATTERY_OVERRIDES: CONF_BATTERY_OVERRIDES,
    ENV_CONFIG: CONF_CONFIG,
    ENV_DEFAULT_BATTERY_STRATEGY: CONF_DEFAULT_BATTERY_STRATEGY,
    ENV_DIAGNOSTICS: CONF_DIAGNOSTICS,
    ENV_DISABLE_CALCULATED_DATA: CONF_DISABLE_CALCULATED_DATA,
    ENV_ENDPOINT: CONF_ENDPOINT,
    ENV_HASS_DISCOVERY: CONF_HASS_DISCOVERY,
    ENV_HASS_DISCOVERY_PREFIX: CONF_HASS_DISCOVERY_PREFIX,
    ENV_HASS_ENTITY_ID_PREFIX: CONF_HASS_ENTITY_ID_PREFIX,
    ENV_INPUT_UNIT_SYSTEM: CONF_INPUT_UNIT_SYSTEM,
    ENV_MQTT_BROKER: CONF_MQTT_BROKER,
    ENV_MQTT_PASSWORD: CONF_MQTT_PASSWORD,
    ENV_MQTT_PORT: CONF_MQTT_PORT,
    ENV_MQTT_RETAIN: CONF_MQTT_RETAIN,
    ENV_MQTT_TLS: CONF_MQTT_TLS,
    ENV_MQTT_TOPIC: CONF_MQTT_TOPIC,
    ENV_MQTT_USERNAME: CONF_MQTT_USERNAME,
    ENV_OUTPUT_UNIT_SYSTEM: CONF_OUTPUT_UNIT_SYSTEM,
    ENV_PORT: CONF_PORT,
    ENV_RAW_DATA: CONF_RAW_DATA,
    ENV_VERBOSE: CONF_VERBOSE,
}


def get_env_vars() -> dict[str, str]:
    """Get environment variables."""
    env_vars = {}

    for env_var in (
        ENV_BATTERY_OVERRIDES,
        ENV_CONFIG,
        ENV_DEFAULT_BATTERY_STRATEGY,
        ENV_DIAGNOSTICS,
        ENV_DISABLE_CALCULATED_DATA,
        ENV_ENDPOINT,
        ENV_HASS_DISCOVERY,
        ENV_HASS_DISCOVERY_PREFIX,
        ENV_HASS_ENTITY_ID_PREFIX,
        ENV_INPUT_UNIT_SYSTEM,
        ENV_MQTT_BROKER,
        ENV_MQTT_PASSWORD,
        ENV_MQTT_PORT,
        ENV_MQTT_RETAIN,
        ENV_MQTT_TLS,
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
    ):
        if (env_var_value := os.getenv(env_var)) is None:
            continue

        if (replacement_env_var := DEPRECATED_ENV_VAR_MAP.get(env_var)) is not None:
            LOGGER.warning(
                "Environment variable %s is deprecated; use %s instead",
                env_var,
                replacement_env_var,
            )
            env_var = replacement_env_var

        config_option = ENV_VAR_TO_CONF_MAP[env_var]
        env_vars[config_option] = env_var_value

    return env_vars


def get_cli_arguments(args: list[str]) -> dict[str, Any]:
    """Get CLI arguments."""
    parser = argparse.ArgumentParser(
        argument_default=argparse.SUPPRESS,
        description="Send data from an Ecowitt gateway to an MQTT broker",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--battery-override",
        dest=CONF_BATTERY_OVERRIDES,
        help="A battery configuration override (format: key,value)",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest=CONF_CONFIG,
        help="A path to a YAML or JSON config file",
        metavar="config",
    )
    parser.add_argument(
        "--default-battery-strategy",
        dest=CONF_DEFAULT_BATTERY_STRATEGY,
        help=(
            "The default battery config strategy to use "
            f"(default: {BatteryStrategy.BOOLEAN})"
        ),
        metavar="default_battery_strategy",
    )
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        dest=CONF_DIAGNOSTICS,
        help="Output diagnostics",
    )
    parser.add_argument(
        "--disable-calculated-data",
        action="store_true",
        dest=CONF_DISABLE_CALCULATED_DATA,
        help="Disable the output of calculated sensors",
    )
    parser.add_argument(
        "-e",
        "--endpoint",
        dest=CONF_ENDPOINT,
        help=(
            "The relative endpoint/path to serve ecowitt2mqtt on "
            f"(default: {DEFAULT_ENDPOINT})"
        ),
        metavar="endpoint",
    )
    parser.add_argument(
        "--hass-discovery",
        action="store_true",
        dest=CONF_HASS_DISCOVERY,
        help="Publish data in the Home Assistant MQTT Discovery format",
    )
    parser.add_argument(
        "--hass-discovery-prefix",
        dest=CONF_HASS_DISCOVERY_PREFIX,
        help=(
            "The Home Assistant MQTT Discovery topic prefix to use "
            f"(default: {DEFAULT_HASS_DISCOVERY_PREFIX})"
        ),
        metavar="hass_discovery_prefix",
    )
    parser.add_argument(
        "--hass-entity-id-prefix",
        dest=CONF_HASS_ENTITY_ID_PREFIX,
        help="The prefix to use for Home Assistant entity IDs",
        metavar="hass_entity_id_prefix",
    )
    parser.add_argument(
        "--input-unit-system",
        dest=CONF_INPUT_UNIT_SYSTEM,
        help=(
            "The input unit system used by the gateway "
            f"(default: {UNIT_SYSTEM_IMPERIAL})"
        ),
        metavar="input_unit_system",
    )
    parser.add_argument(
        "-b",
        "--mqtt-broker",
        dest=CONF_MQTT_BROKER,
        help="The hostname or IP address of an MQTT broker",
        metavar="mqtt_broker",
    )
    parser.add_argument(
        "-p",
        "--mqtt-password",
        dest=CONF_MQTT_PASSWORD,
        help="A valid password for the MQTT broker",
        metavar="mqtt_password",
    )
    parser.add_argument(
        "--mqtt-port",
        dest=CONF_MQTT_PORT,
        help=f"The listenting port of the MQTT broker (default: {DEFAULT_MQTT_PORT})",
        metavar="mqtt_port",
    )
    parser.add_argument(
        "--mqtt-retain",
        action="store_true",
        dest=CONF_MQTT_RETAIN,
        help="Instruct the MQTT broker to retain messages",
    )
    parser.add_argument(
        "--mqtt-tls",
        action="store_true",
        dest=CONF_MQTT_TLS,
        help="Enable MQTT over TLS",
    )
    parser.add_argument(
        "-t",
        "--mqtt-topic",
        dest=CONF_MQTT_TOPIC,
        help="The MQTT topic to publish device data to",
        metavar="mqtt_topic",
    )
    parser.add_argument(
        "-u",
        "--mqtt-username",
        dest=CONF_MQTT_USERNAME,
        help="A valid username for the MQTT broker",
        metavar="mqtt_username",
    )
    parser.add_argument(
        "--output-unit-system",
        dest=CONF_OUTPUT_UNIT_SYSTEM,
        help=(
            "The output unit system used by the gateway "
            f"(default: {UNIT_SYSTEM_IMPERIAL})"
        ),
        metavar="output_unit_system",
    )
    parser.add_argument(
        "--port",
        dest=CONF_PORT,
        help=f"The port to serve ecowitt2mqtt on (default: {DEFAULT_PORT})",
        metavar="port",
    )
    parser.add_argument(
        "--raw-data",
        action="store_true",
        dest=CONF_RAW_DATA,
        help="Return raw data (don't attempt to translate any values)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest=CONF_VERBOSE,
        help="Increase verbosity of logged output",
    )

    arguments = parser.parse_args(args)
    return vars(arguments)


def main() -> None:
    """Run."""
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    cli_arguments = get_cli_arguments(sys.argv[1:])
    env_vars = get_env_vars()
    params: dict[str, Any] = {**env_vars, **cli_arguments}

    if CONF_DIAGNOSTICS in params:
        params[CONF_VERBOSE] = True

    ecowitt = Ecowitt(params)
    loop.run_until_complete(ecowitt.async_start())
