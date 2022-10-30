"""Define tests for devices."""
from __future__ import annotations

from typing import Any

import pytest

from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.device import Device


@pytest.mark.parametrize(
    "device,device_data_filename",
    [
        (
            Device(
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "Ecowitt",
                "GW1000",
                "GW1000B_V1.7.3",
            ),
            "payload_gw1000bpro.json",
        ),
        (
            Device(
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "Unknown",
                "Unknown Device",
                "UNKNOWN_Vx.x.x",
            ),
            "payload_unknown_1.json",
        ),
        (
            Device(
                "default",
                "Unknown",
                "Unknown Device",
                "Unknown Station Type",
            ),
            "payload_unknown_2.json",
        ),
    ],
)
def test_device(device: Device, device_data: dict[str, Any], ecowitt: Ecowitt) -> None:
    """Test that a device object is properly created from a data payload.

    Args:
        device: A parsed Device object.
        device_data: A dictionary of device data.
        ecowitt: An Ecowitt object.
    """
    processed_data = ProcessedData(ecowitt.configs.default_config, device_data)
    assert processed_data.device == device
