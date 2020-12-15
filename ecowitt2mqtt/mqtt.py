"""Define aiohttp routes."""
import asyncio
import json
from typing import Optional, Union

from aiohttp import web
from asyncio_mqtt import Client, MqttError

from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.data import DataProcessor
from ecowitt2mqtt.hass import HassDiscovery


def _generate_payload(data: Union[dict, float, str]) -> bytes:
    """Generate a binary MQTT payload from input data."""
    if isinstance(data, dict):
        return json.dumps(data).encode("utf-8")

    if isinstance(data, str):
        return data.encode("utf-8")

    return str(data).encode("utf-8")


async def _async_publish_to_hass_discovery(
    client: Client, data: dict, discovery_manager: HassDiscovery
) -> None:
    """Publish data to appropriate topics for Home Assistant Discovery."""
    LOGGER.debug("Publishing according to Home Assistant MQTT Discovery standard")

    try:
        async with client:
            tasks = []
            for key, value in data.items():
                config_payload = discovery_manager.get_config_payload(key)
                config_topic = discovery_manager.get_config_topic(key)

                tasks.append(
                    client.publish(config_topic, _generate_payload(config_payload))
                )
                tasks.append(
                    client.publish(
                        config_payload["availability_topic"],
                        _generate_payload("online"),
                    )
                )
                tasks.append(
                    client.publish(
                        config_payload["state_topic"], _generate_payload(value)
                    )
                )

            await asyncio.gather(*tasks)
    except MqttError as err:
        LOGGER.error("Error while publishing to HASS Discovery: %s", err)
        return

    LOGGER.info("Published to HASS discovery: %s", data)


async def _async_publish_to_topic(
    client: Client, data: dict, *, topic: Optional[str] = None
) -> None:
    """Publish data to a single MQTT topic."""
    LOGGER.debug("Publishing entire device payload to single topic: %s", topic)

    try:
        async with client:
            await client.publish(topic, _generate_payload(data))
    except MqttError as err:
        LOGGER.error("Error while publishing to %s: %s", topic, err)
        return

    LOGGER.info("Published to %s: %s", topic, data)


async def async_publish_payload(request: web.Request):
    """Define the endpoint for the Ecowitt device to post data to."""
    args = request.app["args"]

    payload = dict(await request.post())
    LOGGER.debug("Received data from Ecowitt device: %s", payload)

    data_processor = DataProcessor(payload, args.unit_system)
    data = data_processor.generate_data()

    client = Client(
        args.mqtt_broker,
        port=args.mqtt_port,
        username=args.mqtt_username,
        password=args.mqtt_password,
        logger=LOGGER,
    )

    if args.hass_discovery:
        discovery_managers = request.app["hass_discovery_managers"]

        try:
            discovery_manager = discovery_managers[data_processor.unique_id]
        except KeyError:
            if args.hass_discovery_prefix:
                discovery_manager = discovery_managers[
                    data_processor.unique_id
                ] = HassDiscovery(
                    data_processor.unique_id,
                    args.unit_system,
                    discovery_prefix=args.hass_discovery_prefix,
                )
            else:
                discovery_manager = discovery_managers[
                    data_processor.unique_id
                ] = HassDiscovery(data_processor.unique_id, args.unit_system)

        await _async_publish_to_hass_discovery(client, data, discovery_manager)
    else:
        if args.mqtt_topic:
            topic = args.mqtt_topic
        else:
            topic = f"ecowitt2mqtt/{data_processor.unique_id}"

        await _async_publish_to_topic(client, data, topic=topic)
