"""Helpers for config validation using voluptuous."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from ecowitt2mqtt.helpers.calculator.battery import BatteryStrategy


def battery_override(
    value: str | tuple[str, str] | dict[str, Any]
) -> dict[str, BatteryStrategy]:
    """Validate and coerce one or more battery overrides."""
    try:
        if isinstance(value, dict):
            return {key: BatteryStrategy(val) for key, val in value.items()}

        if isinstance(value, tuple):
            return {
                pair[0]: BatteryStrategy(pair[1])
                for assignment in value
                if (pair := assignment.split("="))
            }

        return {
            pair[0]: BatteryStrategy(pair[1])
            for assignment in value.split(";")
            if (pair := assignment.split("="))
        }
    except (IndexError, ValueError) as err:
        raise vol.Invalid(f"invalid battery override: {value}") from err


optional_string = vol.Any(str, None)
port = vol.All(vol.Coerce(int), vol.Range(min=1, max=65535))
