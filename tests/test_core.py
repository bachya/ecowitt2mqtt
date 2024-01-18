"""Test the core Ecowitt object."""
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pytest

from ecowitt2mqtt.const import CONF_VERBOSE
from ecowitt2mqtt.core import Ecowitt
from tests.common import TEST_CONFIG_JSON


@pytest.mark.parametrize("config", [TEST_CONFIG_JSON | {CONF_VERBOSE: "yes"}])
def test_ecowitt_create(config: dict[str, Any]) -> None:
    """Test the creation of an Ecowitt object.

    This is a just a quick sanity check.

    Args:
        config: A configuration dictionary.
    """
    ecowitt = Ecowitt(config)
    assert ecowitt.configs.default_config.verbose is True


@pytest.mark.parametrize("config", [{}])
def test_invalid_config(config: dict[str, Any]) -> None:
    """Test that an invalid config is caught.

    Args:
        config: A configuration dictionary.
    """
    with pytest.raises(SystemExit):
        _ = Ecowitt(config)


@pytest.mark.asyncio
async def test_unhandled_runtime_error(caplog: Mock, config: dict[str, Any]) -> None:
    """Test an unhandled runtime error.

    Args:
        caplog: A mock logging utility.
        config: A configuration dictionary.
    """
    ecowitt = Ecowitt(config)
    with patch.object(
        ecowitt.runtime,
        "async_start",
        AsyncMock(side_effect=Exception("Something horrible and unexpected happened")),
    ):
        with pytest.raises(SystemExit):
            await ecowitt.async_start()
        assert any(
            m
            for m in caplog.messages
            if "Something horrible and unexpected happened" in m
        )
