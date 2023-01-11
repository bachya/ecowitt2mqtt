"""Define various API server helpers."""
from __future__ import annotations

import urllib.parse
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from aiohttp import hdrs
from fastapi import FastAPI, Request, Response, status

from ecowitt2mqtt.backports.enum import StrEnum
from ecowitt2mqtt.const import LOGGER

CallbackT = Callable[[dict[str, Any]], None]


class InputDataFormat(StrEnum):
    """Define an input data format."""

    AMBIENT_WEATHER = "ambient_weather"
    ECOWITT = "ecowitt"


class APIServer(ABC):
    """Define an abstract API server class."""

    HTTP_REQUEST_VERB: str

    def __init__(self, fastapi: FastAPI, endpoint: str) -> None:
        """Initialize.

        Args:
            fastapi: A FastAPI object.
            endpoint: An API endpoint to serve.
        """
        self._endpoint = endpoint
        self._payload_received_callbacks: list[CallbackT] = []

        normalized_endpoint = self._normalize_endpoint(endpoint)

        for route in (normalized_endpoint, f"{normalized_endpoint}/"):
            fastapi.add_api_route(
                route,
                self._async_handle_query,  # type: ignore[arg-type]
                methods=[self.HTTP_REQUEST_VERB.lower()],
                response_class=Response,
                response_model=None,
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

    def _normalize_endpoint(self, endpoint: str) -> str:
        """Normalize the endpoint to work with this server.

        Args:
            endpoint: The endpoint to normalize.

        Returns:
            A normalized endpoint.
        """
        if endpoint.endswith("/"):
            return endpoint[:-1]
        return endpoint

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


class AmbientWeatherAPIServer(APIServer):
    """Define an Ambient Weather API server."""

    HTTP_REQUEST_VERB = hdrs.METH_GET

    def _normalize_endpoint(self, endpoint: str) -> str:
        """Normalize the endpoint to work with this server.

        Args:
            endpoint: The endpoint to normalize.

        Returns:
            A normalized endpoint.
        """
        return endpoint + "{param_string}"

    async def async_parse_request_payload(self, request: Request) -> dict[str, Any]:
        """Parse and return the request payload.

        Args:
            request: A FastAPI Request object.

        Returns:
            A dictionary containing the request payload.
        """
        endpoint_length = len(self._endpoint)
        param_string = request.url.path[endpoint_length:]
        params = dict(urllib.parse.parse_qsl(param_string))

        # Ambient Weather uses a MAC address (with colons) as the PASSKEY; the colons
        # can cause issues with Home Assistant MQTT Discovery, so we remove them:
        params["PASSKEY"] = params["PASSKEY"].replace(":", "")

        return params


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


API_SERVER_IMPLEMENTATION_MAP = {
    InputDataFormat.AMBIENT_WEATHER: AmbientWeatherAPIServer,
    InputDataFormat.ECOWITT: EcowittAPIServer,
}


def get_api_server(
    fastapi: FastAPI, endpoint: str, input_data_format: InputDataFormat
) -> APIServer:
    """Get the correct APIServer implementation based on input data format.

    Args:
        fastapi: A FastAPI object.
        endpoint: An API endpoint to serve.
        input_data_format: The input data format to use.

    Returns:
        An APIServer implementation.
    """
    implementation_class = API_SERVER_IMPLEMENTATION_MAP[input_data_format]
    return implementation_class(fastapi, endpoint)
