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
                manufacturer="Ambient Weather",
                model="Unknown Model",
                name="AMBWeather",
                station_type="AMBWeatherV4.3.4",
                unique_id="ABCDEF123456",
            ),
            "payload_ambweather.json",
        ),
        (
            Device(
                manufacturer="Ecowitt",
                model="GW1000_Pro",
                name="GW1000",
                station_type="GW1000B_V1.6.8",
                unique_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            ),
            "payload_gw1000pro.json",
        ),
        (
            Device(
                manufacturer="Ecowitt",
                model="GW1000B_Pro",
                name="GW1000",
                station_type="GW1000B_V1.7.3",
                unique_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            ),
            "payload_gw1000bpro.json",
        ),
        (
            Device(
                manufacturer="Ecowitt",
                model="GW1100B",
                name="GW1100",
                station_type="GW1100B_V2.0.3",
                unique_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            ),
            "payload_gw1100b.json",
        ),
        (
            Device(
                manufacturer="Ecowitt",
                model="GW2000A",
                name="GW2000",
                station_type="GW2000A_V2.1.4",
                unique_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            ),
            "payload_gw2000a_1.json",
        ),
        (
            Device(
                manufacturer="Fine Offset",
                model="PT-HP2550_Pro_V1.6.7",
                name="PT-HP2550",
                station_type="EasyWeatherV1.5.9",
                unique_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            ),
            "payload_pthp2550pro.json",
        ),
        (
            Device(
                manufacturer="Unknown Manufacturer",
                model="some_random_model",
                name="Unknown Device",
                station_type="UNKNOWN_Vx.x.x",
                unique_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            ),
            "payload_unknown.json",
        ),
        (
            Device(
                manufacturer="Fine Offset",
                model="WH2650A",
                name="WH2650",
                station_type="WH2650A_V1.7.4",
                unique_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            ),
            "payload_wh2650a.json",
        ),
        (
            Device(
                manufacturer="La Crosse",
                model="WS2350_V2.37",
                name="WS2350",
                station_type="EasyWeatherV1.6.4",
                unique_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            ),
            "payload_ws2350.json",
        ),
        (
            Device(
                manufacturer="Ambient Weather",
                model="WS2900_V2.01.13",
                name="WS2900",
                station_type="EasyWeatherV1.5.9",
                unique_id="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
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
