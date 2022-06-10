"""Define tests for the REST API server."""
from __future__ import annotations

from unittest.mock import AsyncMock, Mock, patch

from aiohttp import ClientSession
from fastapi.datastructures import FormData
import pytest

from ecowitt2mqtt.const import (
    CONF_ENDPOINT,
    CONF_MQTT_BROKER,
    CONF_MQTT_PASSWORD,
    CONF_MQTT_TOPIC,
    CONF_MQTT_USERNAME,
    CONF_VERBOSE,
)
from ecowitt2mqtt.core import Ecowitt

from tests.common import (
    TEST_ENDPOINT,
    TEST_MQTT_BROKER,
    TEST_MQTT_PASSWORD,
    TEST_MQTT_TOPIC,
    TEST_MQTT_USERNAME,
    TEST_PORT,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config,log_level",
    [
        (
            {
                CONF_ENDPOINT: TEST_ENDPOINT,
                CONF_MQTT_BROKER: TEST_MQTT_BROKER,
                CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
                CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
                CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
                CONF_VERBOSE: False,
            },
            "error",
        ),
        (
            {
                CONF_ENDPOINT: TEST_ENDPOINT,
                CONF_MQTT_BROKER: TEST_MQTT_BROKER,
                CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
                CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
                CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
                CONF_VERBOSE: True,
            },
            "debug",
        ),
    ],
)
async def test_log_levels(device_data, ecowitt, log_level):
    """Test that server log levels are set correctly."""
    assert ecowitt.server.log_level == log_level


@pytest.mark.asyncio
async def test_payload_callback(device_data, ecowitt, start_server):
    """Test firing a callback upon receiving a device payload."""
    mock_callback_1 = Mock()
    mock_callback_2 = Mock()
    mock_callback_3 = AsyncMock()

    ecowitt.server.add_device_payload_callback(mock_callback_1)
    cancel_mock_callback_2 = ecowitt.server.add_device_payload_callback(mock_callback_2)
    cancel_mock_callback_2()
    ecowitt.server.add_device_payload_callback(mock_callback_3)

    async with ClientSession() as session:
        resp = await session.request(
            "post",
            f"http://127.0.0.1:{TEST_PORT}{TEST_ENDPOINT}",
            data=device_data,
        )
        assert resp.status == 204

    mock_callback_1.assert_called_once_with(FormData(device_data))
    mock_callback_2.assert_not_called()
    mock_callback_3.assert_awaited_once_with(FormData(device_data))


def test_server_start(config):
    """Test successfully starting the server."""
    with patch("uvicorn.server.Server.serve", AsyncMock()):
        ecowitt = Ecowitt(config)
        # If we get here without error, the server has started up:
        ecowitt.start()
