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
                "GW1000B_V1.6.8",
            ),
            "payload_gw1000pro.json",
        ),
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
                "Ecowitt",
                "GW1100",
                "GW1100B_V2.0.3",
            ),
            "payload_gw1100b.json",
        ),
        (
            Device(
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "Ecowitt",
                "GW2000A",
                "GW2000A_V2.1.4",
            ),
            "payload_gw2000a_1.json",
        ),
        (
            Device(
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "Misol",
                "HP2250_Pro",
                "EasyWeatherV1.5.9",
            ),
            "payload_pthp2550pro.json",
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
        (
            Device(
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "Fine Offset",
                "WH2650",
                "WH2650A_V1.7.4",
            ),
            "payload_wh2650a.json",
        ),
        (
            Device(
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "La Crosse",
                "WS-2350",
                "EasyWeatherV1.6.4",
            ),
            "payload_ws2350.json",
        ),
        (
            Device(
                "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "Ambient Weather",
                "WS-2902C",
                "EasyWeatherV1.5.9",
            ),
            "payload_ws2900.json",
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
