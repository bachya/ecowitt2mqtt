"""Define a REST API server for Ecowitt devices to interact with."""
from __future__ import annotations

import asyncio
import traceback
from typing import TYPE_CHECKING

from fastapi import FastAPI, Request, Response, status
import uvicorn

from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.helpers.publisher import PublishError
from ecowitt2mqtt.helpers.publisher.factory import get_publisher

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

DEFAULT_HOST = "0.0.0.0"

LOG_LEVEL_DEBUG = "debug"
LOG_LEVEL_ERROR = "error"


class Server:
    """Define the server management object."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self._startup_task: asyncio.Task | None = None

        self.app = FastAPI()
        self.ecowitt = ecowitt
        self.publisher = get_publisher(ecowitt)
        self.server = uvicorn.Server(
            config=uvicorn.Config(
                self.app,
                host=DEFAULT_HOST,
                port=ecowitt.config.port,
                log_level="debug" if ecowitt.config.verbose else "error",
            )
        )

    async def _async_post_data(self, request: Request) -> Response:
        """Define an endpoint for the Ecowitt device to post data to."""
        payload = await request.form()
        LOGGER.debug("Received data from the Ecowitt device: %s", dict(payload))

        try:
            await self.publisher.async_publish(payload)
        except PublishError as err:
            LOGGER.error("Unable to publish payload: %s", err)
            LOGGER.debug("".join(traceback.format_tb(err.__traceback__)))

        if self.ecowitt.config.diagnostics:
            LOGGER.debug("*** DIAGNOSTICS COLLECTED")
            self.stop()

    async def async_start(self) -> None:
        """Start the REST API server."""
        LOGGER.debug(
            "Starting REST API server: http://%s:%s%s",
            DEFAULT_HOST,
            self.ecowitt.config.port,
            self.ecowitt.config.endpoint,
        )

        self.app.post(
            self.ecowitt.config.endpoint,
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
        )(self._async_post_data)

        self._startup_task = asyncio.create_task(self.server.serve())
        try:
            await self._startup_task
        except asyncio.CancelledError:
            LOGGER.debug("REST API server shutdown complete")

    def stop(self) -> None:
        """Stop the REST API server."""
        if self._startup_task:
            self._startup_task.cancel()
            self._startup_task = None
