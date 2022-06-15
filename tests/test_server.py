"""Define tests for the REST API server."""
from __future__ import annotations

from unittest.mock import AsyncMock, Mock

from aiohttp import ClientSession
from fastapi.datastructures import FormData
import pytest

from tests.common import TEST_ENDPOINT, TEST_PORT, async_run_server


@pytest.mark.asyncio
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
