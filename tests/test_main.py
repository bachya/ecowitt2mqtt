"""Define tests for the main CLI."""
import logging

import pytest
from typer.testing import CliRunner

from ecowitt2mqtt.helpers.logging import TyperLoggerHandler
from ecowitt2mqtt.main import APP


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


def test_startup_logging(caplog, runner):
    """Test startup logging at various levels."""
    caplog.set_level(logging.INFO)
    runner.invoke(APP, [])
    info_log_messages = caplog.messages

    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v"])
    debug_log_messages = caplog.messages

    # There should be more DEBUG-level logs than INFO-level logs:
    assert len(debug_log_messages) > len(info_log_messages)
