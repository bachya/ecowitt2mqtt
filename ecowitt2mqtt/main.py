"""Define the main application."""
import argparse
import logging

from aiohttp import web

from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.mqtt import DEFAULT_MQTT_PORT, MQTT
from ecowitt2mqtt.routes import async_respond_to_ecowitt_data

DEFAULT_AIOHTTP_ENDPOINT = "/data/report"
DEFAULT_AIOHTTP_PORT = 8080
DEFAULT_LOG_LEVEL_STRING = "INFO"


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
        help="The Home Assistant discovery prefix to use (default: homeassistant)",
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

    return parser.parse_args()


def main():
    """Run."""
    args = get_arguments()
    logging.basicConfig(level=getattr(logging, args.log_level))

    LOGGER.debug("Using arguments: %s", args)

    app = web.Application()
    app.add_routes([web.post(args.endpoint, async_respond_to_ecowitt_data)])

    app["args"] = args
    app["hass_discovery_managers"] = {}
    mqtt = app["mqtt"] = MQTT(
        args.mqtt_broker,
        port=args.mqtt_port,
        username=args.mqtt_username,
        password=args.mqtt_password,
    )

    async def connect_mqtt(_) -> None:
        """Connect the MQTT broker."""
        await mqtt.async_connect()

    async def disconnect_mqtt(_) -> None:
        """Disconnect the MQTT broker."""
        await mqtt.async_disconnect()

    app.on_startup.append(connect_mqtt)
    app.on_cleanup.append(disconnect_mqtt)

    web.run_app(app, port=args.port)
