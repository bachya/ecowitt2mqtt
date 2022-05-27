"""Define tests for the REST API server."""
from aiohttp import ClientSession
import pytest
from typer.testing import CliRunner

from ecowitt2mqtt.const import CONF_CONFIG
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.server import Server

from tests.common import TEST_ENDPOINT, TEST_PORT


@pytest.mark.asyncio
async def test_endpoint(server):
    """Test posting data to the server endpoint."""
    async with ClientSession() as session:
        resp = await session.request(
            "post", f"http://127.0.0.1:{TEST_PORT}{TEST_ENDPOINT}", json={"A": "B"}
        )
        print(resp)
