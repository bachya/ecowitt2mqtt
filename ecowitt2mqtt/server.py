"""Define a REST API server for Ecowitt devices to interact with."""
from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI, Request
import uvicorn

from ecowitt2mqtt.const import LOGGER

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

DEFAULT_FASTAPI_LOG_LEVEL = "error"


class Server:  # pylint: disable=too-few-public-methods
    """Define an Server."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self._ecowitt = ecowitt
        self._fastapi = FastAPI()
        self._fastapi.post(ecowitt.config.endpoint)(self._post_data)

    @staticmethod
    async def _post_data(request: Request, status_code=204):
        """Define an endpoint for the Ecowitt device to post data to."""
        payload = await request.json()
        LOGGER.debug("Received data from the Ecowitt device: %s", payload)

    def start(self) -> None:
        """Start the API."""
        LOGGER.debug(
            "Starting REST API server on port %s (endpoint: %s)",
            self._ecowitt.config.port,
            self._ecowitt.config.endpoint,
        )
        uvicorn.run(
            self._fastapi,
            host="127.0.0.1",
            port=self._ecowitt.config.port,
            log_level=DEFAULT_FASTAPI_LOG_LEVEL,
        )
