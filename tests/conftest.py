"""Define dynamic fixtures."""
from __future__ import annotations

import asyncio
import json
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from typer.testing import CliRunner

from ecowitt2mqtt.core import Ecowitt

from tests.common import TEST_CONFIG_JSON, load_fixture


@pytest.fixture(name="config")
def config_fixture():
    """Define a fixture to return configuration data."""
    return TEST_CONFIG_JSON


@pytest.fixture(name="config_filepath")
def config_filepath_fixture(raw_config):
    """Define a fixture to return a config filepath."""
    with tempfile.NamedTemporaryFile() as temp_file:
        with open(temp_file.name, "w", encoding="utf-8") as config_file:
            config_file.write(raw_config)
        yield temp_file.name


@pytest.fixture(name="device_data")
def device_data_fixture(device_data_filename):
    """Define a fixture to return device_data."""
    return json.loads(load_fixture(device_data_filename))


@pytest.fixture(name="device_data_filename")
def device_data_filename_fixture():
    """Define a fixture to return a filename containing device_data."""
    return "payload_gw1000bpro.json"


@pytest.fixture(name="ecowitt")
def ecowitt_fixture(config):
    """Define a fixture to return an Ecowitt object."""
    return Ecowitt(config)


@pytest.fixture(name="mock_asyncio_mqtt_client")
def mock_asyncio_mqtt_client_fixture(mqtt_publish_side_effect):
    """Define a mock asyncio-mqtt client."""
    return MagicMock(
        connect=AsyncMock(),
        disconnect=AsyncMock(),
        publish=AsyncMock(side_effect=mqtt_publish_side_effect),
    )


@pytest_asyncio.fixture(name="mqtt_publish_side_effect")
async def mqtt_publish_side_effect_fixture():
    """Define a fixture for the return value of a MQTT client publish."""
    return AsyncMock()


@pytest.fixture(name="raw_config")
def raw_config_fixture():
    """Define a fixture to return raw configuration data."""
    return json.dumps(TEST_CONFIG_JSON)


@pytest.fixture(name="runner")
def runner_fixture():
    """Define a fixture to return a Typer CLI test runner."""
    return CliRunner()


@pytest_asyncio.fixture(name="setup_asyncio_mqtt")
async def setup_asyncio_mqtt_fixture(ecowitt, mock_asyncio_mqtt_client):
    """Define a fixture to patch asyncio-mqtt properly."""
    with patch("ecowitt2mqtt.runtime.Client") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = (
            mock_asyncio_mqtt_client
        )
        yield


@pytest_asyncio.fixture(name="setup_uvicorn_server")
async def setup_uvicorn_server_fixture(ecowitt):
    """Define a fixture to patch Uvicorn properly."""
    start_task = asyncio.create_task(ecowitt.async_start())
    await asyncio.sleep(0.1)
    try:
        yield
    finally:
        await ecowitt.runtime._server.shutdown()
        start_task.cancel()
    await asyncio.sleep(0.1)
