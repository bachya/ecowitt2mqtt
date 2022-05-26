"""Define a configuration management module."""
from __future__ import annotations

import typer

from ecowitt2mqtt.const import LOGGER
from ecowitt2mqtt.errors import ConfigError

CONF_HASS_DISCOVERY = "hass_discovery"
CONF_MQTT_BROKER = "mqtt_broker"
CONF_MQTT_TOPIC = "mqtt_topic"


class Config:
    """Define the configuration management object."""

    def __init__(self, ctx: typer.Context) -> None:
        """Initialize."""
        LOGGER.info("Command: %s", ctx.invoked_subcommand)
        LOGGER.info("Arguments: %s", ctx.args)
        LOGGER.info("Options: %s", ctx.params)

        self._config = ctx.params

        # If we don't have an MQTT broker, we can't proceed:
        if not self._config[CONF_MQTT_BROKER]:
            raise ConfigError("Missing required option: --mqtt-broker")

        if not self._config[CONF_MQTT_TOPIC] and not self._config[CONF_HASS_DISCOVERY]:
            raise ConfigError(
                "Missing required option: --mqtt-topic or --hass-discovery"
            )
