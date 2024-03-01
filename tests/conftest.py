"""Define dynamic fixtures."""

from __future__ import annotations

import asyncio
import json
import tempfile
from collections.abc import AsyncGenerator, Generator
from typing import Any, cast
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from ecowitt2mqtt.core import Ecowitt
from tests.common import TEST_CONFIG_JSON, load_fixture


@pytest.fixture(name="config")
def config_fixture() -> dict[str, Any]:
    """Define a fixture to return configuration data.

    Returns:
        Configuration data.
    """
    return TEST_CONFIG_JSON


@pytest.fixture(name="config_filepath")
def config_filepath_fixture(raw_config: str) -> Generator[str, None, None]:
    """Define a fixture to return a config filepath.

    Args:
        raw_config: A raw string of configuration data.
    """
    with tempfile.NamedTemporaryFile() as temp_file:
        with open(temp_file.name, "w", encoding="utf-8") as config_file:
            config_file.write(raw_config)
        yield temp_file.name


@pytest.fixture(name="device_data")
def device_data_fixture(device_data_filename: str) -> dict[str, Any]:
    """Define a fixture to return device_data.

    Args:
        device_data_filename: A fixture filename for device data.

    Returns:
        A dictionary of device data.
    """
    return cast(dict[str, Any], json.loads(load_fixture(device_data_filename)))


@pytest.fixture(name="device_data_filename")
def device_data_filename_fixture() -> str:
    """Define a fixture to return a filename containing device_data.

    Returns:
        A fixture filename.
    """
    return "payload_gw1000bpro.json"


@pytest.fixture(name="ecowitt")
def ecowitt_fixture(config: dict[str, Any]) -> Ecowitt:
    """Define a fixture to return an Ecowitt object.

    Args:
        config: A dictionary of configuration data.

    Returns:
        An Ecowitt object.
    """
    return Ecowitt(config)


@pytest.fixture(name="mock_aiomqtt_client")
def mock_aiomqtt_client_fixture(mqtt_publish_side_effect: AsyncMock) -> MagicMock:
    """Define a mock asyncio-mqtt client.

    Args:
        mqtt_publish_side_effect: A mocked side effect to an MQTT publish operation.

    Returns:
        A mocked asyncio-mqtt Client object.
    """
    return MagicMock(
        connect=AsyncMock(),
        disconnect=AsyncMock(),
        publish=AsyncMock(side_effect=mqtt_publish_side_effect),
    )


@pytest_asyncio.fixture(name="mqtt_publish_side_effect")
async def mqtt_publish_side_effect_fixture() -> AsyncMock:
    """Define a fixture for the return value of a MQTT client publish.

    Returns:
        A mocked side effect to an MQTT publish operation.
    """
    return AsyncMock()


@pytest.fixture(name="raw_config")
def raw_config_fixture() -> str:
    """Define a fixture to return raw configuration data.

    Returns:
        A raw string of configuration data.
    """
    return json.dumps(TEST_CONFIG_JSON)


@pytest_asyncio.fixture(name="setup_aiomqtt")
async def setup_aiomqtt_fixture(
    mock_aiomqtt_client: MagicMock,
) -> AsyncGenerator[None, None]:
    """Define a fixture to patch asyncio-mqtt properly.

    Args:
        mock_aiomqtt_client: A mocked aiomqtt Client object.
    """
    with patch("ecowitt2mqtt.runtime.Client") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = mock_aiomqtt_client
        yield


@pytest_asyncio.fixture(name="setup_uvicorn_server")
async def setup_uvicorn_server_fixture(
    ecowitt: Ecowitt,
) -> AsyncGenerator[None, None]:
    """Define a fixture to patch Uvicorn properly.

    Args:
        ecowitt: An Ecowitt object.
    """
    start_task = asyncio.create_task(ecowitt.async_start())
    await asyncio.sleep(0.1)
    try:
        yield
    finally:
        await ecowitt.runtime._uvicorn.shutdown()  # pylint: disable=protected-access
        start_task.cancel()
    await asyncio.sleep(0.1)
