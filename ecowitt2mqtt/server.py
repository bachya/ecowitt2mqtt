"""Define a REST API server for Ecowitt devices to interact with."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Callable, Coroutine

from fastapi import FastAPI, Request, Response, status
import uvicorn

from ecowitt2mqtt.const import LOGGER

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

DEFAULT_HOST = "0.0.0.0"

LOG_LEVEL_DEBUG = "debug"
LOG_LEVEL_ERROR = "error"


class Server:
    """Define the server management object."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self._device_payload_callbacks: list[
            Callable[[dict[str, Any]], Coroutine | None]
        ] = []
        self._loop = asyncio.get_event_loop()
        self._startup_task: asyncio.Task | None = None

        self.app = FastAPI()
        self.app.post(
            ecowitt.config.endpoint,
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
        )(self._async_post_data)

        self._server = uvicorn.Server(
            config=uvicorn.Config(
                self.app,
                host=DEFAULT_HOST,
                port=ecowitt.config.port,
                log_level="debug" if ecowitt.config.verbose else "error",
                loop=self._loop,
            )
        )

        self.ecowitt = ecowitt

    async def _async_post_data(self, request: Request) -> Response:
        """Define an endpoint for the Ecowitt device to post data to."""
        payload = await request.form()
        LOGGER.debug("Received data from the Ecowitt device: %s", dict(payload))
        for callback in self._device_payload_callbacks:
            if asyncio.iscoroutinefunction(callback):
                self._loop.create_task(callback(payload))  # type: ignore
            else:
                callback(payload)

    def add_device_payload_callback(
        self, callback: Callable[[dict[str, Any]], Coroutine | None]
    ) -> Callable[..., None]:
        """Add a callback to be executed when a new device payload is received."""
        self._device_payload_callbacks.append(callback)

        def remove() -> None:
            """Remove the callback."""
            self._device_payload_callbacks.remove(callback)

        return remove

    async def async_start(self) -> None:
        """Start the REST API server."""
        LOGGER.debug(
            "Starting REST API server: http://%s:%s%s",
            DEFAULT_HOST,
            self.ecowitt.config.port,
            self.ecowitt.config.endpoint,
        )

        self._startup_task = self._loop.create_task(self._server.serve())
        try:
            await self._startup_task
        except asyncio.CancelledError:
            LOGGER.debug("REST API server shutdown complete")

    def stop(self) -> None:
        """Stop the REST API server."""
        if self._startup_task:
            self._startup_task.cancel()
            self._startup_task = None
