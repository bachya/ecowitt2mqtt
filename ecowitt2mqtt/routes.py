"""Define aiohttp routes."""
import asyncio

from aiohttp import web

from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.data import DataProcessor
from ecowitt2mqtt.hass import HassDiscovery


async def async_respond_to_ecowitt_data(request: web.Request):
    """Define the endpoint for the Ecowitt device to post data to."""
    args = request.app["args"]
    hass_discovery_managers = request.app["hass_discovery_managers"]
    mqtt = request.app["mqtt"]

    payload = dict(await request.post())

    LOGGER.debug("Received data from Ecowitt device: %s", payload)

    processor = DataProcessor(payload)

    if not request.app["args"].hass_discovery:
        LOGGER.debug("Publishing entire device payload to single topic")
        if request.app["args"].mqtt_topic:
            topic = request.app["args"].mqtt_topic
        else:
            topic = f"ecowitt2mqtt/{processor.unique_id}"
        return await mqtt.async_publish(topic, processor.data)

    LOGGER.debug("Publishing according to Home Assistant MQTT Discovery standard")

    try:
        discovery = hass_discovery_managers[processor.unique_id]
    except KeyError:
        if args.hass_discovery_prefix:
            discovery = hass_discovery_managers[processor.unique_id] = HassDiscovery(
                processor.unique_id, discovery_prefix=args.hass_discovery_prefix
            )
        else:
            discovery = hass_discovery_managers[processor.unique_id] = HassDiscovery(
                processor.unique_id
            )

    tasks = []
    for key, value in processor.data.items():
        config_payload = discovery.get_config_payload(key)
        config_topic = discovery.get_config_topic(key)
        tasks.append(mqtt.async_publish(config_topic, config_payload))
        tasks.append(mqtt.async_publish(config_payload["availability_topic"], "online"))
        tasks.append(mqtt.async_publish(config_payload["state_topic"], value))

    await asyncio.gather(*tasks)
