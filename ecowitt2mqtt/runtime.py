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

LOG_LEVEL_DEBUG = "debug"
LOG_LEVEL_ERROR = "error"

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
        self._app = FastAPI()
        self._condition = asyncio.Condition()
        self._latest_payload: dict[str, Any] | None = None
        self._publisher = get_publisher(ecowitt)
        self._runtime_tasks: list[asyncio.Task] = []
        self._server = MyCustomUvicornServer(
            config=uvicorn.Config(
                self._app,
                host=DEFAULT_HOST,
                port=ecowitt.config.port,
                log_level="debug" if ecowitt.config.verbose else "info",
            )
        )
        self.ecowitt = ecowitt

        # Remove the existing Uvicorn logger handler so that we don't get duplicates:
        # https://github.com/encode/uvicorn/issues/1285
        uvicorn_logger = logging.getLogger("uvicorn")
        uvicorn_logger.removeHandler(uvicorn_logger.handlers[0])

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
                        async with self._condition:
                            await self._condition.wait()
                            LOGGER.debug("Publishing payload: %s", self._latest_payload)
                            assert self._latest_payload
                            await self._publisher.async_publish(
                                client, self._latest_payload
                            )
                        retry_attempt = 0

                        if self.ecowitt.config.diagnostics:
                            LOGGER.debug("*** DIAGNOSTICS COLLECTED")
                            await self.stop()
            except asyncio.CancelledError:
                LOGGER.debug("Stopping the MQTT process loop")
                raise
            except MqttError as err:
                LOGGER.error("There was an MQTT error: %s", err)
                LOGGER.debug("".join(traceback.format_tb(err.__traceback__)))
                should_rerun = True

            if not should_rerun:
                LOGGER.error("Can't recover MQTT process loop; shutting down")
                await self.stop()
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
        LOGGER.debug("Starting runtime server")
        self._app.post(
            self.ecowitt.config.endpoint,
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
        )(self._async_post_data)

        try:
            await self._server.serve()
        except asyncio.CancelledError:
            LOGGER.debug("Stopping the runtime server")
            raise

    async def _async_post_data(self, request: Request) -> Response:
        """Define an endpoint for the Ecowitt device to post data to."""
        payload = dict(await request.form())
        LOGGER.debug("Received data from the Ecowitt device: %s", payload)
        self._latest_payload = payload
        async with self._condition:
            self._condition.notify_all()

    async def async_start(self) -> None:
        """Start the REST API server."""
        loop = asyncio.get_running_loop()

        def handle_exit_signal(sig: int, frame: FrameType | None) -> None:  # noqa: D202
            """Handle an exit signal."""

            async def async_shutdown() -> None:
                """Shut everything down."""
                if self._server.should_exit and sig == signal.SIGINT:
                    self._server.force_exit = True
                else:
                    self._server.should_exit = True

                await self.stop()

            asyncio.create_task(async_shutdown())

        try:
            for sig in HANDLED_SIGNALS:
                loop.add_signal_handler(sig, handle_exit_signal, sig, None)
        except NotImplementedError:  # pragma: no cover
            # Windows
            for sig in HANDLED_SIGNALS:
                signal.signal(sig, handle_exit_signal)

        for coro_func in self._async_create_mqtt_loop, self._async_create_server:
            self._runtime_tasks.append(asyncio.create_task(coro_func()))

        try:
            await asyncio.gather(*self._runtime_tasks)
        except asyncio.CancelledError:
            await asyncio.sleep(0.1)
            LOGGER.debug("Shutdown complete")

    async def stop(self) -> None:
        """Stop the REST API server."""
        for task in self._runtime_tasks:
            task.cancel()
