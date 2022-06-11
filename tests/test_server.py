"""Define tests for the REST API server."""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, Mock

from aiohttp import ClientSession
from fastapi.datastructures import FormData
import pytest

from ecowitt2mqtt.const import (
    CONF_DEFAULT_BATTERY_STRATEGY,
    CONF_DIAGNOSTICS,
    CONF_ENDPOINT,
    CONF_HASS_DISCOVERY,
    CONF_HASS_DISCOVERY_PREFIX,
    CONF_HASS_ENTITY_ID_PREFIX,
    CONF_INPUT_UNIT_SYSTEM,
    CONF_MQTT_BROKER,
    CONF_MQTT_PASSWORD,
    CONF_MQTT_PORT,
    CONF_MQTT_TOPIC,
    CONF_MQTT_USERNAME,
    CONF_OUTPUT_UNIT_SYSTEM,
    CONF_PORT,
    CONF_RAW_DATA,
    CONF_VERBOSE,
)

from tests.common import (
    TEST_ENDPOINT,
    TEST_HASS_DISCOVERY_PREFIX,
    TEST_HASS_ENTITY_ID_PREFIX,
    TEST_MQTT_BROKER,
    TEST_MQTT_PASSWORD,
    TEST_MQTT_PORT,
    TEST_MQTT_TOPIC,
    TEST_MQTT_USERNAME,
    TEST_PORT,
    UNIT_SYSTEM_IMPERIAL,
)


@asynccontextmanager
async def async_run_server(ecowitt):
    """Run ecowitt2mqtt."""
    start_task = asyncio.create_task(ecowitt.async_start())
    await asyncio.sleep(0.1)
    yield
    ecowitt.server._server.should_exit = True  # pylint: disable=protected-access
    await start_task


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        {
            CONF_DEFAULT_BATTERY_STRATEGY: "boolean",
            CONF_DIAGNOSTICS: True,
            CONF_ENDPOINT: TEST_ENDPOINT,
            CONF_HASS_DISCOVERY: False,
            CONF_HASS_DISCOVERY_PREFIX: TEST_HASS_DISCOVERY_PREFIX,
            CONF_HASS_ENTITY_ID_PREFIX: TEST_HASS_ENTITY_ID_PREFIX,
            CONF_INPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_MQTT_BROKER: TEST_MQTT_BROKER,
            CONF_MQTT_PASSWORD: TEST_MQTT_PASSWORD,
            CONF_MQTT_PORT: TEST_MQTT_PORT,
            CONF_MQTT_TOPIC: TEST_MQTT_TOPIC,
            CONF_MQTT_USERNAME: TEST_MQTT_USERNAME,
            CONF_OUTPUT_UNIT_SYSTEM: UNIT_SYSTEM_IMPERIAL,
            CONF_PORT: TEST_PORT,
            CONF_RAW_DATA: False,
            CONF_VERBOSE: True,
        }
    ],
)
async def test_payload_callback(device_data, ecowitt):
    """Test firing a callback upon receiving a device payload."""
    mock_callback_1 = Mock()
    mock_callback_2 = Mock()
    mock_callback_3 = AsyncMock()

    ecowitt.server.add_device_payload_callback(mock_callback_1)
    cancel_mock_callback_2 = ecowitt.server.add_device_payload_callback(mock_callback_2)
    cancel_mock_callback_2()
    ecowitt.server.add_device_payload_callback(mock_callback_3)

    async with async_run_server(ecowitt):
        async with ClientSession() as session:
            resp = await session.request(
                "post",
                f"http://0.0.0.0:{TEST_PORT}{TEST_ENDPOINT}",
                data=device_data,
            )
            assert resp.status == 204

    mock_callback_1.assert_called_once_with(FormData(device_data))
    mock_callback_2.assert_not_called()
    mock_callback_3.assert_awaited_once_with(FormData(device_data))
