"""Define tests for the CLI."""
import logging

import pytest

from ecowitt2mqtt.cli import CLI_APP
from ecowitt2mqtt.helpers.logging import TyperLoggerHandler


def test_startup_logging(caplog, config_filepath, runner):
    """Test startup logging at various levels."""
    caplog.set_level(logging.INFO)
    runner.invoke(CLI_APP, [])
    info_log_messages = caplog.messages

    caplog.set_level(logging.DEBUG)
    runner.invoke(CLI_APP, ["-v"])
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
