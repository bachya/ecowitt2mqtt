"""Define runtime management."""
from __future__ import annotations

import asyncio
from ssl import SSLContext
import traceback
from typing import TYPE_CHECKING

from asyncio_mqtt import Client, MqttError
from fastapi import FastAPI, Request, Response, status
import uvicorn

from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.helpers.publisher.factory import get_publisher

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

DEFAULT_HOST = "0.0.0.0"
DEFAULT_MAX_RETRY_INTERVAL = 60

LOG_LEVEL_DEBUG = "debug"
LOG_LEVEL_ERROR = "error"


class Runtime:  # pylint: disable=too-many-instance-attributes
    """Define the runtime manager."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self._app = FastAPI()
        self._loop = asyncio.get_event_loop()
        self._payload_queue: asyncio.Queue = asyncio.Queue()
        self._publisher = get_publisher(ecowitt)
        self._runtime_tasks: list[asyncio.Task] = []
        self._server = uvicorn.Server(
            config=uvicorn.Config(
                self._app,
                host=DEFAULT_HOST,
                port=ecowitt.config.port,
                log_level="debug" if ecowitt.config.verbose else "error",
                loop=self._loop,
            )
        )
        self.ecowitt = ecowitt

    async def _async_create_mqtt_loop(self) -> None:
        """Create the MQTT process loop."""
        LOGGER.debug("Starting the MQTT process loop")

        retry_attempt = 0
        should_rerun = False

        while True:
            try:
                async with Client(
                    self.ecowitt.config.mqtt_broker,
                    logger=LOGGER,
                    password=self.ecowitt.config.mqtt_password,
                    port=self.ecowitt.config.mqtt_port,
                    tls_context=SSLContext() if self.ecowitt.config.mqtt_tls else None,
                    username=self.ecowitt.config.mqtt_username,
                ) as client:
                    while True:
                        payload = await self._payload_queue.get()
                        LOGGER.debug("Publishing payload: %s", dict(payload))
                        await self._publisher.async_publish(client, payload)
                        retry_attempt = 0

                        if self.ecowitt.config.diagnostics:
                            LOGGER.debug("*** DIAGNOSTICS COLLECTED")
                            self.stop()
            except asyncio.CancelledError:
                LOGGER.debug("MQTT process loop shutdown requested")
                raise
            except MqttError as err:
                LOGGER.error("There was an MQTT error: %s", err)
                LOGGER.debug("".join(traceback.format_tb(err.__traceback__)))
                should_rerun = True

            if not should_rerun:
                LOGGER.error("Can't recover MQTT process loop; shutting down")
                self.stop()
                return

            retry_attempt += 1
            delay = min(retry_attempt**2, DEFAULT_MAX_RETRY_INTERVAL)
            LOGGER.info(
                "Attempting MQTT reconnection in %s seconds (attempt %s)",
                delay,
                retry_attempt,
            )
            await asyncio.sleep(delay)

    async def _async_create_server(self) -> None:
        """Create the server."""
        LOGGER.debug("Starting the Uvicorn + FastAPI server")
        self._app.post(
            self.ecowitt.config.endpoint,
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
        )(self._async_post_data)

        await self._server.serve()

    async def _async_post_data(self, request: Request) -> Response:
        """Define an endpoint for the Ecowitt device to post data to."""
        payload = await request.form()
        LOGGER.debug("Received data from the Ecowitt device: %s", dict(payload))
        await self._payload_queue.put(payload)

    async def async_start(self) -> None:
        """Start the REST API server."""
        for coro_func in self._async_create_mqtt_loop, self._async_create_server:
            self._runtime_tasks.append(asyncio.create_task(coro_func()))

        try:
            await asyncio.gather(*self._runtime_tasks)
        except asyncio.CancelledError:
            LOGGER.debug("Runtime shutdown requested")
            self.stop()

    def stop(self) -> None:
        """Stop the REST API server."""
        for task in self._runtime_tasks:
            task.cancel()
        self._runtime_tasks = []
        LOGGER.debug("Runtime shutdown complete")
