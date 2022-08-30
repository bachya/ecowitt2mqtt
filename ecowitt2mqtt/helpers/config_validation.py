"""Helpers for config validation using voluptuous."""
from __future__ import annotations

from numbers import Number
from typing import Any

import voluptuous as vol

from ecowitt2mqtt.const import UNIT_SYSTEMS
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


def boolean(value: Any) -> bool:
    """Validate and coerce a boolean value."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        value = value.lower().strip()
        if value in ("1", "true", "yes", "on", "enable"):
            return True
        if value in ("0", "false", "no", "off", "disable"):
            return False
    elif isinstance(value, Number):
        # type ignore: https://github.com/python/mypy/issues/3186
        return value != 0  # type: ignore[comparison-overlap]
    raise vol.Invalid(f"invalid boolean value: {value}")


optional_string = vol.Any(str, None)
port = vol.All(vol.Coerce(int), vol.Range(min=1, max=65535))
unit_system = vol.All(vol.Coerce(str), vol.In(UNIT_SYSTEMS))
