"""Define tests for the API server."""
from __future__ import annotations

from unittest.mock import AsyncMock

from aiohttp import ClientSession
from asyncio_mqtt import MqttError
import pytest

from ecowitt2mqtt.const import CONF_DIAGNOSTICS

from tests.common import TEST_CONFIG_JSON, TEST_ENDPOINT, TEST_PORT


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        {
            **TEST_CONFIG_JSON,
            CONF_DIAGNOSTICS: True,
        }
    ],
)
async def test_get_diagnostics(
    caplog, device_data, ecowitt, setup_asyncio_mqtt, setup_uvicorn_server
):
    """Test getting diagnostics."""
    async with ClientSession() as session:
        resp = await session.request(
            "post",
            f"http://0.0.0.0:{TEST_PORT}{TEST_ENDPOINT}",
            data=device_data,
        )
        assert resp.status == 204
    assert any(m for m in caplog.messages if "DIAGNOSTICS COLLECTED" in m)


@pytest.mark.asyncio
@pytest.mark.parametrize("mqtt_publish_side_effect", [AsyncMock(side_effect=MqttError)])
async def test_publish_failure(
    caplog, device_data, ecowitt, setup_asyncio_mqtt, setup_uvicorn_server
):
    """Test a failed MQTT publish."""
    async with ClientSession() as session:
        await session.request(
            "post",
            f"http://0.0.0.0:{TEST_PORT}{TEST_ENDPOINT}",
            data=device_data,
        )
    assert any(m for m in caplog.messages if "There was an MQTT error" in m)


@pytest.mark.asyncio
async def test_publish_success(
    device_data, ecowitt, setup_asyncio_mqtt, setup_uvicorn_server
):
    """Test a successful MQTT publish."""
    async with ClientSession() as session:
        resp = await session.request(
            "post",
            f"http://0.0.0.0:{TEST_PORT}{TEST_ENDPOINT}",
            data=device_data,
        )
        assert resp.status == 204


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mqtt_publish_side_effect",
    [AsyncMock(side_effect=Exception("Something horrible happened"))],
)
async def test_unknown_exception_shutdown(
    caplog, device_data, ecowitt, setup_asyncio_mqtt, setup_uvicorn_server
):
    """Test that an unknown exception successfully shuts down the runtime."""
    async with ClientSession() as session:
        await session.request(
            "post",
            f"http://0.0.0.0:{TEST_PORT}{TEST_ENDPOINT}",
            data=device_data,
        )
    assert any(m for m in caplog.messages if "Something horrible happened" in m)
