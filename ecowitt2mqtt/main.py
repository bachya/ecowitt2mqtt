"""Define the main application."""
import argparse
import logging

from aiohttp import web

from ecowitt2mqtt.const import LOGGER, UNIT_SYSTEM_IMPERIAL
from ecowitt2mqtt.mqtt import async_publish_payload

DEFAULT_AIOHTTP_ENDPOINT = "/data/report"
DEFAULT_AIOHTTP_PORT = 8080
DEFAULT_HASS_DISCOVERY_PREFIX = "homeassistant"
DEFAULT_LOG_LEVEL_STRING = "INFO"
DEFAULT_MQTT_PORT = 1883


def get_arguments() -> argparse.Namespace:
    """Get passed-in arguments."""
    parser = argparse.ArgumentParser(
        description="Send data from Ecowitt devices to an MQTT broker"
    )

    parser.add_argument(
        "-l",
        "--log-level",
        action="store",
        default=DEFAULT_LOG_LEVEL_STRING,
        help=f"The logging level (default: {DEFAULT_LOG_LEVEL_STRING})",
    )

    # MQTT
    parser.add_argument(
        "--mqtt-broker",
        action="store",
        required=True,
        type=str,
        help="The hostname or IP address of the MQTT broker",
    )
    parser.add_argument(
        "--mqtt-port",
        action="store",
        default=DEFAULT_MQTT_PORT,
        type=int,
        help=f"The port of the MQTT broker (default: {DEFAULT_MQTT_PORT})",
    )
    parser.add_argument(
        "--mqtt-username",
        action="store",
        default=None,
        type=str,
        help="The username to use with the MQTT broker (default: None)",
    )
    parser.add_argument(
        "--mqtt-password",
        action="store",
        default=None,
        type=str,
        help="The password to use with the MQTT broker (default: None)",
    )
    parser.add_argument(
        "--mqtt-topic",
        action="store",
        type=str,
        help="The MQTT topic to publish the device's data to (default: ecowitt2mqtt/<ID>)",
    )

    # Home Assistant MQTT Discovery
    parser.add_argument(
        "--hass-discovery",
        action="store_const",
        const=True,
        help="Publish data in the Home Assistant MQTT Discovery format",
    )
    parser.add_argument(
        "--hass-discovery-prefix",
        default=DEFAULT_HASS_DISCOVERY_PREFIX,
        help=(
            "The Home Assistant discovery prefix to use "
            f"(default: {DEFAULT_HASS_DISCOVERY_PREFIX})"
        ),
    )

    # Web Server
    parser.add_argument(
        "--endpoint",
        action="store",
        default=DEFAULT_AIOHTTP_ENDPOINT,
        type=str,
        help=(
            "The relative endpoint/path to serve the web app on "
            f"(default: {DEFAULT_AIOHTTP_ENDPOINT})"
        ),
    )
    parser.add_argument(
        "--port",
        action="store",
        default=DEFAULT_AIOHTTP_PORT,
        type=int,
        help=f"The port to serve the web app on (default: {DEFAULT_AIOHTTP_PORT})",
    )

    # Misc.
    parser.add_argument(
        "--raw-data",
        action="store_const",
        const=True,
        help="Return raw data (don't attempt to translate any values)",
    )
    parser.add_argument(
        "--input-unit-system",
        action="store",
        default=UNIT_SYSTEM_IMPERIAL,
        type=str,
        help=f"The input unit system used by the device (default: {UNIT_SYSTEM_IMPERIAL})",
    )
    parser.add_argument(
        "--output-unit-system",
        action="store",
        default=UNIT_SYSTEM_IMPERIAL,
        type=str,
        help=f"The unit system to use in output (default: {UNIT_SYSTEM_IMPERIAL})",
    )

    return parser.parse_args()


def main() -> None:
    """Run."""
    args = get_arguments()
    logging.basicConfig(level=getattr(logging, args.log_level))

    LOGGER.debug("Using arguments: %s", args)

    app = web.Application()
    app.add_routes([web.post(args.endpoint, async_publish_payload)])  # type: ignore

    app["args"] = args
    app["hass_discovery_managers"] = {}

    web.run_app(app, port=args.port)


if __name__ == "__main__":
    main()
