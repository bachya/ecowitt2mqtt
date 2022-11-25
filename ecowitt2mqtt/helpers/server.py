"""Define various API server helpers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from fastapi import FastAPI, Request, Response, status

from ecowitt2mqtt.const import LOGGER

CallbackT = Callable[[dict[str, Any]], None]


class APIServer(ABC):
    """Define an abstract API server class."""

    def __init__(self, http_method_used: str, route: str) -> None:
        """Initialize.

        Args:
            http_method_used: The HTTP verb used to query this API.
            route: The API route to query.
        """
        self._payload_received_callbacks: list[CallbackT] = []

        self.fastapi = FastAPI()
        self.fastapi.add_api_route(
            route,
            self._async_handle_query,  # type: ignore[arg-type]
            methods=[http_method_used.lower()],
            response_class=Response,
            status_code=status.HTTP_204_NO_CONTENT,
        )

    async def _async_handle_query(self, request: Request) -> None:
        """Handle an API query.

        Args:
            request: A FastAPI Request object.
        """
        payload = await self.async_parse_request_payload(request)
        LOGGER.debug("Received data payload: %s", payload)

        for callback in self._payload_received_callbacks:
            callback(payload)

    def add_payload_callback(self, callback: CallbackT) -> None:
        """Add a callback to be called when a new payload is received.

        Args:
            callback: The callback to add.
        """
        self._payload_received_callbacks.append(callback)

    @abstractmethod
    async def async_parse_request_payload(self, request: Request) -> dict[str, Any]:
        """Parse and return the request payload.

        Args:
            request: A FastAPI Request object.

        Returns:
            A dictionary containing the request payload.
        """


class EcowittAPIServer(APIServer):
    """Define an Ecowitt API server."""

    async def async_parse_request_payload(self, request: Request) -> dict[str, Any]:
        """Parse and return the request payload.

        Args:
            request: A FastAPI Request object.

        Returns:
            A dictionary containing the request payload.
        """
        form_data = await request.form()
        return dict(form_data)
