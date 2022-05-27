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


APP = FastAPI()


async def post_data(request: Request, status_code: int = 204) -> None:
    """Define an endpoint for the Ecowitt device to post data to."""
    payload = await request.json()
    LOGGER.debug("Received data from the Ecowitt device: %s", payload)


class Server:  # pylint: disable=too-few-public-methods
    """Define an Server."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self._ecowitt = ecowitt
        APP.post(ecowitt.config.endpoint)(post_data)

    def start(self) -> None:
        """Start the API."""
        LOGGER.debug(
            "Starting REST API server: http://%s:%s%s",
            DEFAULT_HOST,
            self._ecowitt.config.port,
            self._ecowitt.config.endpoint,
        )
        uvicorn.run(
            APP,
            host="127.0.0.1",
            port=self._ecowitt.config.port,
            log_level=DEFAULT_FASTAPI_LOG_LEVEL,
        )
