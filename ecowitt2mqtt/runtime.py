"""Define runtime management."""
from __future__ import annotations

import asyncio
import logging
import signal
from ssl import SSLContext
import traceback
from types import FrameType
from typing import TYPE_CHECKING, Any

from asyncio_mqtt import Client, MqttError
from fastapi import FastAPI, Request, Response, status
import uvicorn

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


class MyCustomUvicornServer(uvicorn.Server):  # type: ignore
    """Define a Uvicorn server that doesn't swallow signals."""

    def install_signal_handlers(self) -> None:
        """Don't swallow signals."""
        pass


class Runtime:
    """Define the runtime manager."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self.ecowitt = ecowitt

        app = FastAPI()
        app.post(
            ecowitt.config.endpoint,
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
        )(self._async_post_data)
        self._server = MyCustomUvicornServer(
            config=uvicorn.Config(
                app,
                host=DEFAULT_HOST,
                port=ecowitt.config.port,
                log_level="debug" if ecowitt.config.verbose else "error",
            )
        )

        self._latest_payload: dict[str, Any] | None = None
        self._new_payload_condition = asyncio.Condition()
        self._publisher = get_publisher(ecowitt)
        self._runtime_tasks: list[asyncio.Task] = []

        # Remove the existing Uvicorn logger handler so that we don't get duplicates:
        # https://github.com/encode/uvicorn/issues/1285
        uvicorn_logger = logging.getLogger("uvicorn")
        uvicorn_logger.removeHandler(uvicorn_logger.handlers[0])

    async def _async_create_mqtt_loop(self) -> None:
        """Create the MQTT process loop."""
        LOGGER.debug("Starting MQTT process loop")

        retry_attempt = 0
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
                        async with self._new_payload_condition:
                            await self._new_payload_condition.wait()
                            LOGGER.debug("Publishing payload: %s", self._latest_payload)
                            assert self._latest_payload
                            await self._publisher.async_publish(
                                client, self._latest_payload
                            )
                        retry_attempt = 0

                        if self.ecowitt.config.diagnostics:
                            LOGGER.debug("*** DIAGNOSTICS COLLECTED")
                            self.stop()
            except asyncio.CancelledError:
                LOGGER.debug("Stopping MQTT process loop")
                raise
            except MqttError as err:
                LOGGER.error("There was an MQTT error: %s", err)
                LOGGER.debug("".join(traceback.format_tb(err.__traceback__)))

            retry_attempt += 1
            delay = min(retry_attempt**2, DEFAULT_MAX_RETRY_INTERVAL)
            LOGGER.info(
                "Attempting MQTT reconnection in %s seconds (attempt %s)",
                delay,
                retry_attempt,
            )
            await asyncio.sleep(delay)

    async def _async_create_server(self) -> None:
        """Create the REST API server."""
        LOGGER.debug("Starting REST API server")

        try:
            await self._server.serve()
        except asyncio.CancelledError:
            LOGGER.debug("Stopping REST API server")
            raise

    async def _async_post_data(self, request: Request) -> Response:
        """Define an endpoint for the Ecowitt device to post data to."""
        payload = dict(await request.form())
        LOGGER.debug("Received data from the Ecowitt device: %s", payload)
        async with self._new_payload_condition:
            self._latest_payload = payload
            self._new_payload_condition.notify_all()

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

        self._runtime_tasks = [
            asyncio.create_task(coro_func())
            for coro_func in (self._async_create_mqtt_loop, self._async_create_server)
        ]

        try:
            await asyncio.gather(*self._runtime_tasks)
        except asyncio.CancelledError:
            for task in self._runtime_tasks:
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            LOGGER.debug("Runtime shutdown complete")

    def stop(self) -> None:
        """Stop the REST API server."""
        for task in self._runtime_tasks:
            task.cancel()
