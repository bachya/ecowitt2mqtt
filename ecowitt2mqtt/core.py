"""Define the core application objects."""

from __future__ import annotations

import locale
import logging
import sys
from typing import Any

import colorlog

from ecowitt2mqtt.config import ConfigError, Configs
from ecowitt2mqtt.const import LOGGER, __version__
from ecowitt2mqtt.runtime import Runtime


def configure_logging(verbose: bool) -> None:
    """Configure logging.

    Args:
        verbose: Whether verbose logging should be included.
    """
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)s | %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    )

    LOGGER.setLevel(log_level)
    LOGGER.addHandler(handler)


class Ecowitt:  # pylint: disable=too-few-public-methods
    """Define the base application object."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Initialize.

        Args:
            params: CLI options and environment variables.
        """
        try:
            self.configs = Configs(params)
        except ConfigError as err:
            LOGGER.error(err)
            self.exit(1)

        configure_logging(self.configs.default_config.verbose)

        LOGGER.debug("Input CLI options/environment variables: %s", params)
        LOGGER.debug("Configs loaded: %s", self.configs)

        LOGGER.debug("Setting locale: %s", self.configs.default_config.locale)
        locale.setlocale(locale.LC_ALL, self.configs.default_config.locale)

        self.runtime = Runtime(self)

    async def async_start(self) -> None:
        """Start ecowitt2mqtt."""
        LOGGER.info("Starting ecowitt2mqtt (version %s)", __version__)
        try:
            await self.runtime.async_start()
        except Exception as err:  # pylint: disable=broad-except
            LOGGER.error(err)
            self.exit(1)

    def exit(self, status_code: int = 0) -> int:
        """Stop the application.

        Args:
            status_code: The status code to exit with.

        Returns:
            The passed status code.
        """
        return sys.exit(status_code)
