"""Define the main interface to the CLI."""
import typer

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
    LEGACY_ENV_MQTT_BROKER,
    LEGACY_ENV_MQTT_PASSWORD,
    LEGACY_ENV_MQTT_PORT,
    LEGACY_ENV_MQTT_TOPIC,
    LEGACY_ENV_MQTT_USERNAME,
    LEGACY_ENV_OUTPUT_UNIT_SYSTEM,
    LEGACY_ENV_PORT,
    LEGACY_ENV_RAW_DATA,
    UNIT_SYSTEM_IMPERIAL,
)
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.helpers.logging import log_exception

DEFAULT_ENDPOINT = "/data/report"
DEFAULT_HASS_DISCOVERY_PREFIX = "homeassistant"
DEFAULT_MQTT_PORT = 1883
DEFAULT_PORT = 8080


@log_exception()
def main(  # pylint: disable=too-many-arguments,too-many-locals
    ctx: typer.Context,
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
    mqtt_username: str = typer.Option(
        None,
        "--mqtt-username",
        "-u",
        envvar=[ENV_MQTT_USERNAME, LEGACY_ENV_MQTT_USERNAME],
        help="A valid username for the MQTT broker.",
    ),
    mqtt_topic: str = typer.Option(
        None,
        "--mqtt-topic",
        "-t",
        envvar=[ENV_MQTT_TOPIC, LEGACY_ENV_MQTT_TOPIC],
        help="The MQTT topic to publish device data to.",
    ),
    output_unit_system: str = typer.Option(
        UNIT_SYSTEM_IMPERIAL,
        "--output-unit-system",
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
    ctx.obj = Ecowitt(ctx)


APP = typer.Typer(callback=main, invoke_without_command=True)
