"""Define dynamic fixtures."""
from __future__ import annotations

import asyncio
from multiprocessing import Process

from fastapi import FastAPI
import pytest
from typer.testing import CliRunner
import uvicorn

from ecowitt2mqtt.const import CONF_CONFIG
from ecowitt2mqtt.core import Ecowitt

from tests.common import TEST_PORT, TEST_RAW_JSON


@pytest.fixture(name="config_filepath")
def config_filepath_fixture(raw_config, tmp_path):
    """Define a fixture to return a config filepath."""
    config_filepath = f"{tmp_path}/config.json"
    with open(config_filepath, "w", encoding="utf-8") as config_file:
        config_file.write(raw_config)
    return config_filepath


@pytest.fixture(name="raw_config")
def raw_config_fixture():
    """Define a fixture to return raw configuration data."""
    return TEST_RAW_JSON


@pytest.fixture(name="runner")
def runner_fixture():
    """Define a fixture to return a Typer CLI test runner."""
    return CliRunner()


class UvicornTestServer(uvicorn.Server):
    """Mock a Uvicorn test server."""

    def __init__(self, app: FastAPI, *, host: str = "127.0.0.1", port: int = TEST_PORT):
        """Initialize."""
        self._serve_task: asyncio.Task | None = None
        self._startup_done = asyncio.Event()
        super().__init__(config=uvicorn.Config(app, host=host, port=port))

    async def startup(self, sockets: list | None = None) -> None:
        """Override Uvicorn startup."""
        await super().startup(sockets=sockets)
        self.config.setup_event_loop()
        self._startup_done.set()

    async def up(self) -> None:
        """Start up server asynchronously."""
        self._serve_task = asyncio.create_task(self.serve())
        await self._startup_done.wait()

    async def down(self) -> None:
        """Shut down server asynchronously."""
        self.should_exit = True
        await self._serve_task


@pytest.mark.asyncio
@pytest.fixture(name="server")
async def server_fixture(config_filepath):
    """Define a fixture to return a mocked API server."""
    ecowitt = Ecowitt({CONF_CONFIG: config_filepath})
    server = UvicornTestServer(ecowitt.server.app)
    await server.up()
    yield
    await server.down()
