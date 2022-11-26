"""Define various API server helpers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from aiohttp import hdrs
from fastapi import FastAPI, Request, Response, status

from ecowitt2mqtt.const import LOGGER

CallbackT = Callable[[dict[str, Any]], None]


class APIServer(ABC):
    """Define an abstract API server class."""

    HTTP_REQUEST_VERB: str

    def __init__(self) -> None:
        """Initialize."""
        self._payload_received_callbacks: list[CallbackT] = []
        self.fastapi = FastAPI()

    async def _async_handle_query(self, request: Request) -> None:
        """Handle an API query.

        Args:
            request: A FastAPI Request object.
        """
        payload = await self.async_parse_request_payload(request)
        LOGGER.debug("Received data payload: %s", payload)

        for callback in self._payload_received_callbacks:
            callback(payload)

    def _normalize_route(self, route: str) -> str:
        """Normalize the route to work with this server.

        Args:
            route: The route to normalize.

        Returns:
            A normalized route.
        """
        if route.endswith("/"):
            return route[:-1]
        return route

    def add_payload_callback(self, callback: CallbackT) -> None:
        """Add a callback to be called when a new payload is received.

        Args:
            callback: The callback to add.
        """
        self._payload_received_callbacks.append(callback)

    def add_route(self, route: str) -> None:
        """Add a route to the API.

        Args:
            route: The API route to query.
        """
        self.fastapi.add_api_route(
            self._normalize_route(route),
            self._async_handle_query,  # type: ignore[arg-type]
            methods=[self.HTTP_REQUEST_VERB.lower()],
            response_class=Response,
            status_code=status.HTTP_204_NO_CONTENT,
        )

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

    HTTP_REQUEST_VERB = hdrs.METH_POST

    async def async_parse_request_payload(self, request: Request) -> dict[str, Any]:
        """Parse and return the request payload.

        Args:
            request: A FastAPI Request object.

        Returns:
            A dictionary containing the request payload.
        """
        form_data = await request.form()
        return dict(form_data)
