"""Define tests for the CLI."""
import logging

import pytest

from ecowitt2mqtt.cli import APP
from ecowitt2mqtt.helpers.logging import TyperLoggerHandler


@pytest.mark.parametrize(
    "args,missing_args_str",
    [
        ([], "--mqtt-broker"),
        (["-b", "127.0.0.1"], "--mqtt-topic or --hass-discovery"),
    ],
)
def test_missing_required_options(args, caplog, missing_args_str, runner):
    """Test that missing required options are handled."""
    runner.invoke(APP, args)
    assert caplog.messages[0] == f"Missing required option: {missing_args_str}"


@pytest.mark.asyncio
async def test_startup_logging(caplog, config_filepath, runner, start_server):
    """Test startup logging at various levels."""
    caplog.set_level(logging.INFO)
    runner.invoke(APP, ["-c", config_filepath])
    info_log_messages = caplog.messages

    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v", "-c", config_filepath])
    debug_log_messages = caplog.messages

    # There should be more DEBUG-level logs than INFO-level logs:
    assert len(debug_log_messages) > len(info_log_messages)


def test_typer_logging_handler(caplog, runner):
    """Test the TyperLoggerHandler helper."""
    caplog.set_level(logging.DEBUG)

    handler = TyperLoggerHandler()
    logger = logging.getLogger("test")
    logger.addHandler(handler)

    logger.critical("Test Critical Message")
    logger.debug("Test Debug Message")
    logger.error("Test Error Message")
    logger.info("Test Info Message")
    logger.warning("Test Warning Message")

    assert len(caplog.messages) == 5
