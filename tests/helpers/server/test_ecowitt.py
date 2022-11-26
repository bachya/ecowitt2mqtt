"""Define tests for the Ecowitt API server."""
# pylint: disable=unused-argument
from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock, Mock

import pytest
from aiohttp import ClientSession
from asyncio_mqtt import MqttError

from ecowitt2mqtt.const import CONF_DIAGNOSTICS, CONF_ENDPOINT
from ecowitt2mqtt.core import Ecowitt
from tests.common import TEST_CONFIG_JSON, TEST_ENDPOINT, TEST_PORT


@pytest.mark.asyncio
@pytest.mark.parametrize("config", [TEST_CONFIG_JSON | {CONF_DIAGNOSTICS: True}])
async def test_get_diagnostics(
    caplog: Mock,
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    setup_asyncio_mqtt: AsyncGenerator[None, None],
    setup_uvicorn_server: AsyncGenerator[None, None],
) -> None:
    """Test getting diagnostics.

    Args:
        caplog: A mock logging utility.
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        setup_asyncio_mqtt: A mock asyncio-mqtt client connection.
        setup_uvicorn_server: A mock Uvicorn + FastAPI application.
    """
    async with ClientSession() as session:
        resp = await session.request(
            "post", f"http://127.0.0.1:{TEST_PORT}{TEST_ENDPOINT}", data=device_data
        )
        assert resp.status == 204
    assert any(m for m in caplog.messages if "DIAGNOSTICS COLLECTED" in m)


@pytest.mark.asyncio
@pytest.mark.parametrize("mqtt_publish_side_effect", [AsyncMock(side_effect=MqttError)])
async def test_publish_failure(
    caplog: Mock,
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    setup_asyncio_mqtt: AsyncGenerator[None, None],
    setup_uvicorn_server: AsyncGenerator[None, None],
) -> None:
    """Test a failed MQTT publish.

    Args:
        caplog: A mock logging utility.
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        setup_asyncio_mqtt: A mock asyncio-mqtt client connection.
        setup_uvicorn_server: A mock Uvicorn + FastAPI application.
    """
    async with ClientSession() as session:
        await session.request(
            "post", f"http://127.0.0.1:{TEST_PORT}{TEST_ENDPOINT}", data=device_data
        )
    assert any(m for m in caplog.messages if "There was an MQTT error" in m)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        TEST_CONFIG_JSON | {CONF_ENDPOINT: TEST_ENDPOINT},
        TEST_CONFIG_JSON | {CONF_ENDPOINT: f"{TEST_ENDPOINT}/"},
    ],
)
async def test_publish_success(
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    setup_asyncio_mqtt: AsyncGenerator[None, None],
    setup_uvicorn_server: AsyncGenerator[None, None],
) -> None:
    """Test a successful MQTT publish.

    Args:
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        setup_asyncio_mqtt: A mock asyncio-mqtt client connection.
        setup_uvicorn_server: A mock Uvicorn + FastAPI application.
    """
    async with ClientSession() as session:

        resp = await session.request(
            "post",
            (
                f"http://127.0.0.1:{TEST_PORT}"
                f"{ecowitt.configs.default_config.endpoint}"
            ),
            data=device_data,
        )
        assert resp.status == 204


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mqtt_publish_side_effect",
    [AsyncMock(side_effect=Exception("Something horrible happened"))],
)
async def test_unknown_exception_shutdown(
    caplog: Mock,
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    setup_asyncio_mqtt: AsyncGenerator[None, None],
    setup_uvicorn_server: AsyncGenerator[None, None],
) -> None:
    """Test that an unknown exception successfully shuts down the runtime.

    Args:
        caplog: A mock logging utility.
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        setup_asyncio_mqtt: A mock asyncio-mqtt client connection.
        setup_uvicorn_server: A mock Uvicorn + FastAPI application.
    """
    async with ClientSession() as session:
        await session.request(
            "post", f"http://127.0.0.1:{TEST_PORT}{TEST_ENDPOINT}", data=device_data
        )
    assert any(m for m in caplog.messages if "Something horrible happened" in m)
