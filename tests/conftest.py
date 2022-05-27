"""Define dynamic fixtures."""
from __future__ import annotations

import asyncio

import pytest
from typer.testing import CliRunner
import uvicorn

from .common import TEST_PORT, TEST_RAW_JSON


class UvicornTestServer(uvicorn.Server):
    """Define a Uvicorn test server."""

    def __init__(self, app, host="127.0.0.1", port=TEST_PORT):
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
