"""Define tests for the core Ecowitt object."""
from __future__ import annotations

import logging
from unittest.mock import patch

from aiohttp import ClientSession
from asyncio_mqtt import MqttError
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
    UNIT_SYSTEM_IMPERIAL,
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
    async_run_server,
)


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
async def test_get_diagnostics(caplog, device_data, ecowitt):
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
    assert any(m for m in caplog.messages if "COLLECTING DIAGNOSTICS" in m)


@pytest.mark.asyncio
async def test_publish_failure(caplog, device_data, ecowitt):
    """Test a failed MQTT publish."""
    async with async_run_server(ecowitt):
        with patch.object(
            ecowitt.mqtt_publisher.client, "publish", side_effect=MqttError
        ):
            async with ClientSession() as session:
                await session.request(
                    "post",
                    f"http://0.0.0.0:{TEST_PORT}{TEST_ENDPOINT}",
                    data=device_data,
                )
    assert any(m for m in caplog.messages if "Unable to publish payload" in m)


@pytest.mark.asyncio
async def test_publish_success(device_data, ecowitt):
    """Test a successful MQTT publish."""
    async with async_run_server(ecowitt):
        async with ClientSession() as session:
            resp = await session.request(
                "post",
                f"http://0.0.0.0:{TEST_PORT}{TEST_ENDPOINT}",
                data=device_data,
            )
            assert resp.status == 204
