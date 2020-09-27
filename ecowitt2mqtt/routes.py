"""Define aiohttp routes."""
from aiohttp import web
from ecowitt2mqtt.const import LOGGER


async def respond_to_ecowitt_data(request: web.Request):
    """Define the endpoint for the Ecowitt device to post data to."""
    data = await request.post()

    LOGGER.debug("Received data from Ecowitt device: %s", data)

    await request.app["mqtt"].async_publish_topic(data)
