"""Define runtime management."""

from __future__ import annotations

import asyncio
import traceback
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress
from ssl import SSLContext
from typing import TYPE_CHECKING, Any

import uvicorn
from aiomqtt import Client, MqttError
from fastapi import FastAPI

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.helpers.publisher.factory import get_publishers
from ecowitt2mqtt.helpers.server import APIServer, get_api_server

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

DEFAULT_HOST = "0.0.0.0"  # noqa: S104, # nosec: B104
DEFAULT_MAX_RETRY_INTERVAL = 60
DEFAULT_PENDING_CALLS_THRESHOLD = 500

UVICORN_LOG_LEVEL_DEBUG = "debug"
UVICORN_LOG_LEVEL_ERROR = "error"


class Runtime:
    """Define the runtime manager."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize.

        Args:
            ecowitt: An Ecowitt object.
        """
        self._api_servers: dict[str, APIServer] = {}
        self._mqtt_loop_tasks: list[asyncio.Task] = []
        self._payload_events: dict[str, asyncio.Event] = {}
        self._payload_lock = asyncio.Lock()
        self._payload_queues: dict[str, asyncio.Queue] = {}
        self._rest_api_server_task: asyncio.Task | None = None
        self.ecowitt = ecowitt

        @asynccontextmanager
        async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
            """Define a lifespan context manager."""
            yield

            # Upon shutdown:
            for task in self._mqtt_loop_tasks:
                if task.done():
                    continue
                with suppress(asyncio.CancelledError):
                    LOGGER.debug("Cancelling MQTT loop: %s", task.get_name())
                    task.cancel()
            LOGGER.debug("Runtime shutdown complete")

        fastapi = FastAPI(lifespan=lifespan)
        for config in ecowitt.configs.iterate():
            if config.endpoint not in self._api_servers:
                api_server = self._api_servers[config.endpoint] = get_api_server(
                    fastapi, config.endpoint, config.input_data_format
                )
                api_server.add_payload_callback(self._process_payload)

        if ecowitt.configs.default_config.verbose:
            uvicorn_log_level = UVICORN_LOG_LEVEL_DEBUG
        else:
            uvicorn_log_level = UVICORN_LOG_LEVEL_ERROR
        self._uvicorn = uvicorn.Server(
            config=uvicorn.Config(
                fastapi,
                host=DEFAULT_HOST,
                port=ecowitt.configs.default_config.port,
                log_level=uvicorn_log_level,
            )
        )

    def _async_create_mqtt_loop_task(
        self,
        config: Config,
        queue: asyncio.Queue,
        payload_event: asyncio.Event,
    ) -> asyncio.Task:
        """Create a task that contains a new MQTT loop.

        Args:
            config: A Config object.
            queue: An asyncio Queue object.
            payload_event: An asyncio Event object.

        Returns:
            An asyncio Task object.
        """
        LOGGER.debug("Creating MQTT loop: %s", config.uuid)

        async def create_loop() -> None:
            """Create the loop."""
            retry_attempt = 0
            try:
                while True:
                    try:
                        async with Client(
                            config.mqtt_broker,
                            logger=LOGGER,
                            password=config.mqtt_password,
                            port=config.mqtt_port,
                            tls_context=SSLContext() if config.mqtt_tls else None,
                            username=config.mqtt_username,
                        ) as client:
                            client.pending_calls_threshold = (
                                DEFAULT_PENDING_CALLS_THRESHOLD
                            )
                            publishers = get_publishers(config, client)
                            while True:
                                await payload_event.wait()
                                while not queue.empty():
                                    payload = await queue.get()
                                    LOGGER.debug("Publishing payload: %s", payload)
                                    tasks = [
                                        publisher.async_publish(payload)
                                        for publisher in publishers
                                    ]
                                    await asyncio.gather(*tasks)

                                if config.diagnostics:
                                    LOGGER.info("*** DIAGNOSTICS COLLECTED")
                                    self.stop()

                                payload_event.clear()
                                retry_attempt = 0
                    except MqttError as err:
                        LOGGER.error("There was an MQTT error: %s", err)
                        payload_event.clear()
                        retry_attempt += 1
                        delay = min(retry_attempt**2, DEFAULT_MAX_RETRY_INTERVAL)
                        LOGGER.info(
                            "Attempting MQTT reconnection in %s seconds (attempt %s)",
                            delay,
                            retry_attempt,
                        )
                        await asyncio.sleep(delay)
            except Exception as err:  # pylint: disable=broad-except
                LOGGER.exception("%s exception caused a shutdown: %s", type(err), err)
                LOGGER.debug("".join(traceback.format_tb(err.__traceback__)))
                self.stop()

        task = asyncio.create_task(create_loop())
        task.set_name(config.uuid)
        return task

    def _process_payload(self, payload: dict[str, Any]) -> None:
        """Define an endpoint for the Ecowitt device to post data to.

        Args:
            payload: An API request payload.
        """
        config = self.ecowitt.configs.get(payload["PASSKEY"])

        # Store the payload in the appropriate queue:
        queue = self._payload_queues.setdefault(config.uuid, asyncio.Queue())
        queue.put_nowait(payload)

        # If there isn't an active MQTT loop for this payload, create it first and
        # instruct it to publish the payload once it's connected:
        if (payload_event := self._payload_events.get(config.uuid)) is None:
            payload_event = self._payload_events[config.uuid] = asyncio.Event()
            self._mqtt_loop_tasks.append(
                self._async_create_mqtt_loop_task(config, queue, payload_event)
            )

        payload_event.set()

    async def async_start(self) -> None:
        """Start the runtime."""
        LOGGER.debug("Starting runtime")
        self._rest_api_server_task = asyncio.create_task(self._uvicorn.serve())
        try:
            await self._rest_api_server_task
        except asyncio.CancelledError:
            LOGGER.debug("Runtime task successfully cancelled")

    def stop(self) -> None:
        """Stop the REST API server."""
        LOGGER.debug("Stopping runtime")
        self._uvicorn.should_exit = True
