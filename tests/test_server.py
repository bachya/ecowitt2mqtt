"""Define tests for the REST API server."""
from unittest.mock import Mock

from aiohttp import ClientSession
import pytest

from tests.common import TEST_ENDPOINT, TEST_PORT


@pytest.mark.asyncio
async def test_payload_callback(device_payload, ecowitt, uvicorn):
    """Test firing a callback upon receiving a device payload."""
    mock_callback_1 = Mock()
    mock_callback_2 = Mock()

    ecowitt.server.add_device_payload_callback(mock_callback_1)
    cancel_mock_callback_2 = ecowitt.server.add_device_payload_callback(mock_callback_2)

    # Test canceling one of the callbacks:
    cancel_mock_callback_2()

    ecowitt.server.start()

    async with ClientSession() as session:
        resp = await session.request(
            "post", f"http://127.0.0.1:{TEST_PORT}{TEST_ENDPOINT}", json=device_payload
        )
        assert resp.status == 204

    mock_callback_1.assert_called_once_with(device_payload)
    mock_callback_2.assert_not_called()
