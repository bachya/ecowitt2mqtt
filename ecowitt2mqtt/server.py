"""Define a REST API server for Ecowitt devices to interact with."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from fastapi import FastAPI, Request, Response, status
import uvicorn

from ecowitt2mqtt.const import LOGGER

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt

DEFAULT_FASTAPI_LOG_LEVEL = "error"
DEFAULT_HOST = "127.0.0.1"


class Server:
    """Define the server management object."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self._device_payload_callbacks: list[Callable[[dict[str, Any]], None]] = []

        self.app = FastAPI()
        self.app.post(
            ecowitt.config.endpoint,
            status_code=status.HTTP_204_NO_CONTENT,
            response_class=Response,
        )(self._post_data)

        self.ecowitt = ecowitt

    async def _post_data(self, request: Request) -> Response:
        """Define an endpoint for the Ecowitt device to post data to."""
        payload = await request.json()
        LOGGER.debug("Received data from the Ecowitt device: %s", payload)
        for callback in self._device_payload_callbacks:
            callback(payload)

    def add_device_payload_callback(
        self, callback: Callable[[dict[str, Any]], None]
    ) -> Callable[..., None]:
        """Add a callback to be executed when a new device payload is received."""
        self._device_payload_callbacks.append(callback)

        def remove() -> None:
            """Remove the callback."""
            self._device_payload_callbacks.remove(callback)

        return remove

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
