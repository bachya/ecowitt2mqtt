"""Define the main application."""
import argparse
import json
import logging

from aiohttp import web
from asyncio_mqtt import Client, MqttError

_LOGGER = logging.getLogger("ecowitt2mqtt")

DEFAULT_AIOHTTP_ENDPOINT = "/data/report"
DEFAULT_AIOHTTP_PORT = 8080
DEFAULT_LOG_LEVEL_STRING = "INFO"
DEFAULT_MQTT_PORT = 1883


def get_arguments() -> argparse.Namespace:
    """Get passed-in arguments."""
    parser = argparse.ArgumentParser(
        description="Send data from Ecowitt devices to an MQTT broker"
    )
    parser.add_argument(
        "--mqtt-broker",
        action="store",
        required=True,
        type=str,
        help="The hostname or IP address of the MQTT broker",
    )
    parser.add_argument(
        "--mqtt-topic",
        action="store",
        required=True,
        type=str,
        help="The MQTT topic to publish the device's data to",
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
    parser.add_argument(
        "-l",
        "--log-level",
        action="store",
        default=DEFAULT_LOG_LEVEL_STRING,
        help=f"The logging level (default: {DEFAULT_LOG_LEVEL_STRING})",
    )

    return parser.parse_args()


async def post_data(request: web.Request):
    """Define the endpoint for the Ecowitt device to post data to."""
    data = await request.post()

    _LOGGER.debug("Received data from Ecowitt device: %s", data)

    try:
        await request.app["mqtt"].publish(
            request.app["args"].mqtt_topic, json.dumps(dict(data)).encode()
        )
        _LOGGER.info("Data published to MQTT broker: %s", data)
    except MqttError as err:
        _LOGGER.error("Error while publishing data to MQTT: %s", err)


def main():
    """Run."""
    args = get_arguments()
    logging.basicConfig(level=getattr(logging, args.log_level))

    _LOGGER.debug("Using arguments: %s", args)

    app = web.Application()
    app.add_routes([web.post(args.endpoint, post_data)])
    app["args"] = args

    mqtt = app["mqtt"] = Client(
        args.mqtt_broker,
        port=args.mqtt_port,
        username=args.mqtt_username,
        password=args.mqtt_password,
    )

    async def connect_mqtt(_) -> None:
        """Connect the MQTT broker."""
        try:
            await mqtt.connect()
        except MqttError as err:
            _LOGGER.error("Error while connecting to MQTT broker: %s", err)

        _LOGGER.debug("Connected to MQTT broker")

    async def disconnect_mqtt(_) -> None:
        """Disconnect the MQTT broker."""
        try:
            await mqtt.disconnect()
        except MqttError as err:
            _LOGGER.error("Error while disconnecting from MQTT broker: %s", err)

        _LOGGER.debug("Disconnected from MQTT broker")

    app.on_startup.append(connect_mqtt)
    app.on_cleanup.append(disconnect_mqtt)

    web.run_app(app, port=args.port)
