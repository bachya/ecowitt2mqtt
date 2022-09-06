"""Define runtime management."""
from __future__ import annotations

import asyncio
import logging
import signal
from ssl import SSLContext
import traceback
from types import FrameType
from typing import TYPE_CHECKING

from asyncio_mqtt import Client, MqttError
from fastapi import FastAPI, Request, Response, status
import uvicorn

from ecowitt2mqtt.config import Config
from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.helpers.publisher.factory import get_publisher

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

DEFAULT_HOST = "0.0.0.0"
DEFAULT_MAX_RETRY_INTERVAL = 60

HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)

UVICORN_LOG_LEVEL_DEBUG = "debug"
UVICORN_LOG_LEVEL_ERROR = "error"


class DeSignaledUvicornServer(uvicorn.Server):  # type: ignore
    """Define a Uvicorn server that doesn't swallow signals."""

    def install_signal_handlers(self) -> None:
        """Don't swallow signals."""
        pass


class Runtime:  # pylint: disable=too-many-instance-attributes
    """Define the runtime manager."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self.ecowitt = ecowitt

        if ecowitt.configs.default_config.verbose:
            uvicorn_log_level = UVICORN_LOG_LEVEL_DEBUG
        else:
            uvicorn_log_level = UVICORN_LOG_LEVEL_ERROR

        app = FastAPI()

        for route in (
            ecowitt.configs.default_config.endpoint,
            f"{ecowitt.configs.default_config.endpoint}/",
        ):
            app.post(
                route,
                status_code=status.HTTP_204_NO_CONTENT,
                response_class=Response,
            )(self._async_post_data)

        self._server = DeSignaledUvicornServer(
            config=uvicorn.Config(
                app,
                host=DEFAULT_HOST,
                port=ecowitt.configs.default_config.port,
                log_level=uvicorn_log_level,
            )
        )

        self._payload_events: dict[str, asyncio.Event] = {}
        self._mqtt_loop_tasks: list[asyncio.Task] = []
        self._payload_lock = asyncio.Lock()
        self._payload_queues: dict[str, asyncio.Queue] = {}
        self._rest_api_server_task: asyncio.Task | None = None

        # Remove the existing Uvicorn logger handler so that we don't get duplicates:
        # https://github.com/encode/uvicorn/issues/1285
        uvicorn_logger = logging.getLogger("uvicorn")
        uvicorn_logger.removeHandler(uvicorn_logger.handlers[0])

    def _async_create_mqtt_loop_task(
        self,
        config: Config,
        queue: asyncio.Queue,
        payload_event: asyncio.Event,
    ) -> asyncio.Task:
        """Create a task that contains a new MQTT loop."""
        LOGGER.debug("Creating MQTT loop: %s", config.mqtt_connection_info)

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
                            publisher = get_publisher(config, client)
                            while True:
                                await payload_event.wait()
                                while not queue.empty():
                                    payload = await queue.get()
                                    LOGGER.debug("Publishing payload: %s", payload)
                                    await publisher.async_publish(payload)

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
            except asyncio.CancelledError:
                LOGGER.debug("Stopping MQTT process loop")
                raise
            except Exception as err:  # pylint: disable=broad-except
                LOGGER.exception("Exception caused a shutdown: %s", err)
                LOGGER.debug("".join(traceback.format_tb(err.__traceback__)))
                self.stop()

        return asyncio.create_task(create_loop())

    async def _async_post_data(self, request: Request) -> Response:
        """Define an endpoint for the Ecowitt device to post data to."""
        form_data = await request.form()
        payload = dict(form_data)
        LOGGER.debug("Received data from an Ecowitt device: %s", payload)

        config = self.ecowitt.configs.get(payload["PASSKEY"])

        # Store the payload in the appropriate queue:
        queue = self._payload_queues.setdefault(
            config.mqtt_connection_info, asyncio.Queue()
        )
        queue.put_nowait(payload)

        # If there isn't an active MQTT loop for this payload, create it first and
        # instruct it to publish the payload once it's connected:
        if (
            payload_event := self._payload_events.get(config.mqtt_connection_info)
        ) is None:
            payload_event = self._payload_events[
                config.mqtt_connection_info
            ] = asyncio.Event()
            self._mqtt_loop_tasks.append(
                self._async_create_mqtt_loop_task(config, queue, payload_event)
            )

        payload_event.set()

    async def async_start(self) -> None:
        """Start the runtime."""
        loop = asyncio.get_running_loop()

        def handle_exit_signal(sig: int, frame: FrameType | None) -> None:
            """Handle an exit signal."""
            if self._server.should_exit and sig == signal.SIGINT:
                self._server.force_exit = True
            else:
                self._server.should_exit = True
            self.stop()

        try:
            for sig in HANDLED_SIGNALS:
                loop.add_signal_handler(sig, handle_exit_signal, sig, None)
        except NotImplementedError:
            # Windows
            for sig in HANDLED_SIGNALS:
                signal.signal(sig, handle_exit_signal)

        LOGGER.debug("Starting runtime")
        self._rest_api_server_task = asyncio.create_task(self._server.serve())
        try:
            await self._rest_api_server_task
        except asyncio.CancelledError:
            for task in self._mqtt_loop_tasks:
                if task.done():
                    continue
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            LOGGER.debug("Runtime shutdown complete")

    def stop(self) -> None:
        """Stop the REST API server."""
        LOGGER.debug("Stopping runtime")
        if self._rest_api_server_task:
            self._rest_api_server_task.cancel()
