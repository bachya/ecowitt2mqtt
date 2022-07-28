"""Define tests for the API server."""
from __future__ import annotations

import logging
from unittest.mock import AsyncMock

from aiohttp import ClientSession
from asyncio_mqtt import MqttError
import pytest

from ecowitt2mqtt.const import CONF_DIAGNOSTICS

from tests.common import TEST_CONFIG_JSON, TEST_ENDPOINT, TEST_PORT, async_run_server


@pytest.mark.asyncio
@pytest.mark.parametrize("config", [{**TEST_CONFIG_JSON, CONF_DIAGNOSTICS: True}])
async def test_get_diagnostics(caplog, device_data, ecowitt, setup_asyncio_mqtt):
    """Test getting diagnostics."""
    caplog.set_level(logging.DEBUG)
    async with async_run_server(ecowitt):
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
async def test_publish_failure(caplog, device_data, ecowitt, setup_asyncio_mqtt):
    """Test a failed MQTT publish."""
    async with async_run_server(ecowitt):
        async with ClientSession() as session:
            await session.request(
                "post",
                f"http://0.0.0.0:{TEST_PORT}{TEST_ENDPOINT}",
                data=device_data,
            )
    assert any(m for m in caplog.messages if "Unable to publish payload" in m)


@pytest.mark.asyncio
async def test_publish_success(device_data, ecowitt, setup_asyncio_mqtt):
    """Test a successful MQTT publish."""
    async with async_run_server(ecowitt):
        async with ClientSession() as session:
            resp = await session.request(
                "post",
                f"http://0.0.0.0:{TEST_PORT}{TEST_ENDPOINT}",
                data=device_data,
            )
            assert resp.status == 204
