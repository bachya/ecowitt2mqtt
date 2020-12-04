"""Define aiohttp routes."""
import asyncio
import json
from typing import Dict, Optional, Union

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
    client: Client,
    data_processor: DataProcessor,
    hass_discovery_managers: Dict[str, HassDiscovery],
    *,
    hass_discovery_prefix=None,
) -> None:
    """Publish data to appropriate topics for Home Assistant Discovery."""
    LOGGER.debug("Publishing according to Home Assistant MQTT Discovery standard")

    try:
        discovery = hass_discovery_managers[data_processor.unique_id]
    except KeyError:
        if hass_discovery_prefix:
            discovery = hass_discovery_managers[
                data_processor.unique_id
            ] = HassDiscovery(
                data_processor.unique_id, discovery_prefix=hass_discovery_prefix
            )
        else:
            discovery = hass_discovery_managers[
                data_processor.unique_id
            ] = HassDiscovery(data_processor.unique_id)

    async with client:
        tasks = []
        for key, value in data_processor.generated_data.items():
            config_payload = discovery.get_config_payload(key)
            config_topic = discovery.get_config_topic(key)
            tasks.append(
                client.publish(config_topic, _generate_payload(config_payload))
            )
            tasks.append(
                client.publish(
                    config_payload["availability_topic"], _generate_payload("online")
                )
            )
            tasks.append(
                client.publish(config_payload["state_topic"], _generate_payload(value))
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, MqttError):
                LOGGER.error("Error while publishing to HASS Discovery: %s", result)

    LOGGER.info("Published to HASS discovery: %s", data_processor.generated_data)


async def _async_publish_to_topic(
    client: Client, data_processor: DataProcessor, *, topic: Optional[str] = None
) -> None:
    """Publish data to a single MQTT topic."""
    LOGGER.debug("Publishing entire device payload to single topic")

    if not topic:
        topic = f"ecowitt2mqtt/{data_processor.unique_id}"

    try:
        async with client:
            await client.publish(
                topic, _generate_payload(data_processor.generated_data)
            )
    except MqttError as err:
        LOGGER.error("Error while publishing to %s: %s", topic, err)
        return

    LOGGER.info("Published to %s: %s", topic, data_processor.generated_data)


async def async_publish_payload(request: web.Request):
    """Define the endpoint for the Ecowitt device to post data to."""
    args = request.app["args"]

    payload = dict(await request.post())
    LOGGER.debug("Received data from Ecowitt device: %s", payload)

    data_processor = DataProcessor(payload)

    client = Client(
        args.mqtt_broker,
        port=args.mqtt_port,
        username=args.mqtt_username,
        password=args.mqtt_password,
        logger=LOGGER,
    )

    if args.hass_discovery:
        await _async_publish_to_hass_discovery(
            client,
            data_processor,
            request.app["hass_discovery_managers"],
            hass_discovery_prefix=args.hass_discovery_prefix,
        )
    else:
        await _async_publish_to_topic(client, data_processor, topic=args.mqtt_topic)
