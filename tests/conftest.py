"""Define dynamic fixtures."""
from __future__ import annotations

import asyncio
import json
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from typer.testing import CliRunner
import uvicorn

from ecowitt2mqtt.core import Ecowitt

from tests.common import TEST_PORT, TEST_RAW_JSON, load_fixture


class UvicornTestServer(uvicorn.Server):
    """Mock a Uvicorn test server."""

    def __init__(self, ecowitt: Ecowitt) -> None:
        """Initialize."""
        self._serve_task: asyncio.Task | None = None
        self._startup_done = asyncio.Event()
        super().__init__(
            config=uvicorn.Config(
                app=ecowitt.server.app,
                host="0.0.0.0",
                port=TEST_PORT,
                log_level="error",
            )
        )

    async def start(self) -> None:
        """Start up server asynchronously."""
        self._serve_task = asyncio.create_task(self.serve())
        await self._startup_done.wait()

    async def startup(self, sockets: list | None = None) -> None:
        """Override Uvicorn startup."""
        await super().startup(sockets=sockets)
        self.config.setup_event_loop()
        self._startup_done.set()

    async def stop(self) -> None:
        """Shut down server asynchronously."""
        self.should_exit = True
        await self._serve_task


@pytest.fixture(name="config")
def config_fixture():
    """Define a fixture to return configuration data."""
    return json.loads(TEST_RAW_JSON)


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


@pytest.fixture(name="raw_config")
def raw_config_fixture():
    """Define a fixture to return raw configuration data."""
    return TEST_RAW_JSON


@pytest.fixture(name="runner")
def runner_fixture():
    """Define a fixture to return a Typer CLI test runner."""
    return CliRunner()


@pytest_asyncio.fixture(name="setup_asyncio_mqtt")
async def setup_asyncio_mqtt_fixture():
    """Define a fixture to patch asyncio-mqtt properly."""
    with patch(
        "ecowitt2mqtt.helpers.publisher.Client",
        MagicMock(return_value=AsyncMock(publish=AsyncMock())),
    ):
        yield


@pytest_asyncio.fixture(name="start_server")
async def start_server_fixture(ecowitt):
    """Define a fixture to return a running Uvicorn server."""
    with patch("uvicorn.server.Server", UvicornTestServer(ecowitt)) as mock_server:
        await mock_server.start()
        yield
        await mock_server.stop()
