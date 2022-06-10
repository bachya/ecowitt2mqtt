"""Define the main interface to the CLI."""
import asyncio
from pathlib import Path
from typing import List

import typer
import uvloop

from ecowitt2mqtt.const import (
    CONF_VERBOSE,
    ENV_BATTERY_OVERRIDE,
    ENV_CONFIG,
    ENV_DEFAULT_BATTERY_STRATEGY,
    ENV_DIAGNOSTICS,
    ENV_ENDPOINT,
    ENV_HASS_DISCOVERY,
    ENV_HASS_DISCOVERY_PREFIX,
    ENV_HASS_ENTITY_ID_PREFIX,
    ENV_INPUT_UNIT_SYSTEM,
    ENV_MQTT_BROKER,
    ENV_MQTT_PASSWORD,
    ENV_MQTT_PORT,
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
    LEGACY_ENV_MQTT_BROKER,
    LEGACY_ENV_MQTT_PASSWORD,
    LEGACY_ENV_MQTT_PORT,
    LEGACY_ENV_MQTT_TOPIC,
    LEGACY_ENV_MQTT_USERNAME,
    LEGACY_ENV_OUTPUT_UNIT_SYSTEM,
    LEGACY_ENV_PORT,
    LEGACY_ENV_RAW_DATA,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
)
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy
from ecowitt2mqtt.helpers.logging import log_exception

DEFAULT_ENDPOINT = "/data/report"
DEFAULT_HASS_DISCOVERY_PREFIX = "homeassistant"
DEFAULT_MQTT_PORT = 1883
DEFAULT_PORT = 8080


def validate_unit_system(value: str) -> str:
    """Validate a passed unit system."""
    if value not in (UNIT_SYSTEM_IMPERIAL, UNIT_SYSTEM_METRIC):
        raise typer.BadParameter(
            f"'{value}' is not one of '{UNIT_SYSTEM_IMPERIAL}', '{UNIT_SYSTEM_METRIC}'"
        )
    return value


@log_exception()
def main(  # pylint: disable=too-many-arguments,too-many-locals
    ctx: typer.Context,
    battery_override: List[str] = typer.Option(
        None,
        "--battery-override",
        envvar=[ENV_BATTERY_OVERRIDE],
        help="A battery configuration override (format: key,value)",
    ),
    config: Path = typer.Option(
        None,
        "--config",
        "-c",
        envvar=[ENV_CONFIG],
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="A path to a YAML or JSON config file.",
        resolve_path=True,
    ),
    default_battery_strategy: BatteryStrategy = typer.Option(
        BatteryStrategy.BOOLEAN,
        "--default-battery-strategy",
        envvar=[ENV_DEFAULT_BATTERY_STRATEGY],
        help="The default battery config strategy to use.",
        metavar="TEXT",
    ),
    diagnostics: bool = typer.Option(
        False,
        "--diagnostics",
        envvar=[ENV_DIAGNOSTICS],
        help="Output diagnostics.",
    ),
    endpoint: str = typer.Option(
        DEFAULT_ENDPOINT,
        "--endpoint",
        "-e",
        envvar=[ENV_ENDPOINT, LEGACY_ENV_ENDPOINT],
        help="The relative endpoint/path to serve ecowitt2mqtt on.",
    ),
    hass_discovery: bool = typer.Option(
        False,
        "--hass-discovery",
        envvar=[ENV_HASS_DISCOVERY, LEGACY_ENV_HASS_DISCOVERY],
        help="Publish data in the Home Assistant MQTT Discovery format.",
    ),
    hass_discovery_prefix: str = typer.Option(
        DEFAULT_HASS_DISCOVERY_PREFIX,
        "--hass-discovery-prefix",
        envvar=[ENV_HASS_DISCOVERY_PREFIX, LEGACY_ENV_HASS_DISCOVERY_PREFIX],
        help="The Home Assistant discovery prefix to use.",
    ),
    hass_entity_id_prefix: str = typer.Option(
        None,
        "--hass-entity-id-prefix",
        envvar=[ENV_HASS_ENTITY_ID_PREFIX, LEGACY_ENV_HASS_ENTITY_ID_PREFIX],
        help="The prefix to use for Home Assistant entity IDs.",
    ),
    input_unit_system: str = typer.Option(
        UNIT_SYSTEM_IMPERIAL,
        "--input-unit-system",
        callback=validate_unit_system,
        envvar=[ENV_INPUT_UNIT_SYSTEM, LEGACY_ENV_INPUT_UNIT_SYSTEM],
        help="The input unit system used by the device.",
    ),
    mqtt_broker: str = typer.Option(
        None,
        "--mqtt-broker",
        "-b",
        envvar=[ENV_MQTT_BROKER, LEGACY_ENV_MQTT_BROKER],
        help="The hostname or IP address of an MQTT broker.",
    ),
    mqtt_password: str = typer.Option(
        None,
        "--mqtt-password",
        "-p",
        envvar=[ENV_MQTT_PASSWORD, LEGACY_ENV_MQTT_PASSWORD],
        help="A valid password for the MQTT broker.",
    ),
    mqtt_port: int = typer.Option(
        DEFAULT_MQTT_PORT,
        "--mqtt-port",
        envvar=[ENV_MQTT_PORT, LEGACY_ENV_MQTT_PORT],
        help="The listenting port of the MQTT broker.",
    ),
    mqtt_tls: bool = typer.Option(
        False,
        "--mqtt-tls",
        envvar=[ENV_MQTT_TLS],
        help="Enable MQTT over TLS.",
    ),
    mqtt_topic: str = typer.Option(
        None,
        "--mqtt-topic",
        "-t",
        envvar=[ENV_MQTT_TOPIC, LEGACY_ENV_MQTT_TOPIC],
        help="The MQTT topic to publish device data to.",
    ),
    mqtt_username: str = typer.Option(
        None,
        "--mqtt-username",
        "-u",
        envvar=[ENV_MQTT_USERNAME, LEGACY_ENV_MQTT_USERNAME],
        help="A valid username for the MQTT broker.",
    ),
    output_unit_system: str = typer.Option(
        UNIT_SYSTEM_IMPERIAL,
        "--output-unit-system",
        callback=validate_unit_system,
        envvar=[ENV_OUTPUT_UNIT_SYSTEM, LEGACY_ENV_OUTPUT_UNIT_SYSTEM],
        help="The unit system to use in output.",
    ),
    port: int = typer.Option(
        DEFAULT_PORT,
        "--port",
        envvar=[ENV_PORT, LEGACY_ENV_PORT],
        help="The port to serve ecowitt2mqtt on.",
    ),
    raw_data: bool = typer.Option(
        False,
        "--raw-data",
        envvar=[ENV_RAW_DATA, LEGACY_ENV_RAW_DATA],
        help="Return raw data (don't attempt to translate any values).",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        envvar=[ENV_VERBOSE],
        help="Increase verbosity of logged output.",
    ),
) -> None:
    """ecowitt2mqtt sends Ecowitt device data to an MQTT broker."""
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    if diagnostics:
        ctx.params[CONF_VERBOSE] = True

    ecowitt = Ecowitt(ctx.params)
    loop.run_until_complete(ecowitt.async_start())


CLI_APP = typer.Typer(callback=main, invoke_without_command=True)
