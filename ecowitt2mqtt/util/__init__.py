"""Define utility modules."""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from ecowitt2mqtt.core import Ecowitt


def execute_callback(
    ecowitt: Ecowitt, callback: Callable[..., Any], *args: Any
) -> None:
    """Schedule a callback to be called."""
    if asyncio.iscoroutinefunction(callback):
        asyncio.create_task(callback(*args))
    else:
        callback(*args)
