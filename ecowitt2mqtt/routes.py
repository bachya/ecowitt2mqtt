"""Define aiohttp routes."""
import asyncio

from aiohttp import web
from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.hass import HassDiscovery


async def async_respond_to_ecowitt_data(request: web.Request):
    """Define the endpoint for the Ecowitt device to post data to."""
    args = request.app["args"]
    hass_discovery_managers = request.app["hass_discovery_managers"]
    mqtt = request.app["mqtt"]

    data = dict(await request.post())

    LOGGER.debug("Received data from Ecowitt device: %s", data)

    unique_id = data.pop("PASSKEY")

    # Remove data keys we don't care about:
    data.pop("dateutc", None)
    data.pop("freq", None)
    data.pop("model", None)

    if not request.app["args"].hass_discovery:
        LOGGER.debug("Publishing entire device payload to single topic")

        if request.app["args"].mqtt_topic:
            topic = request.app["args"].mqtt_topic
        else:
            topic = f"ecowitt2mqtt/{unique_id}"

        return await mqtt.async_publish(topic, data)

    LOGGER.debug("Publishing according to Home Assistant MQTT Discovery standard")

    try:
        discovery = hass_discovery_managers[unique_id]
    except KeyError:
        if args.hass_discovery_prefix:
            discovery = hass_discovery_managers[unique_id] = HassDiscovery(
                unique_id, discovery_prefix=args.hass_discovery_prefix
            )
        else:
            discovery = hass_discovery_managers[unique_id] = HassDiscovery(unique_id)

    for key, value in data.items():
        config_payload = discovery.get_config_payload(key)
        config_topic = discovery.get_config_topic(key)
        tasks = [
            mqtt.async_publish(config_topic, config_payload),
            mqtt.async_publish(config_payload["availability_topic"], "online"),
            mqtt.async_publish(config_payload["state_topic"], value),
        ]
        await asyncio.gather(*tasks)
