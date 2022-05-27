"""Define a REST API server for Ecowitt devices to interact with."""
from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI, Request
import uvicorn

from ecowitt2mqtt.const import LOGGER

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

DEFAULT_FASTAPI_LOG_LEVEL = "error"
DEFAULT_HOST = "127.0.0.1"


class Server:  # pylint: disable=too-few-public-methods
    """Define an Server."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self.ecowitt = ecowitt

        self.app = FastAPI()
        self.app.post(ecowitt.config.endpoint)(self._post_data)

    @staticmethod
    async def _post_data(request: Request, status_code: int = 204) -> None:
        """Define an endpoint for the Ecowitt device to post data to."""
        payload = await request.json()
        LOGGER.debug("Received data from the Ecowitt device: %s", payload)

    def start(self) -> None:
        """Start the API."""
        LOGGER.debug(
            "Starting REST API server: http://%s:%s%s",
            DEFAULT_HOST,
            self.ecowitt.config.port,
            self.ecowitt.config.endpoint,
        )
        uvicorn.run(
            self.app,
            host="127.0.0.1",
            port=self.ecowitt.config.port,
            log_level=DEFAULT_FASTAPI_LOG_LEVEL,
        )
