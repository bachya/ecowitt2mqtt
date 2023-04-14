"""Define tests for the MQTT Topic publisher."""
# pylint: disable=line-too-long
from typing import Any
from unittest.mock import MagicMock

import pytest

from ecowitt2mqtt.const import CONF_MQTT_RETAIN, CONF_RAW_DATA
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.helpers.publisher import generate_mqtt_payload
from ecowitt2mqtt.helpers.publisher.factory import get_publisher
from ecowitt2mqtt.helpers.publisher.topic import TopicPublisher
from tests.common import TEST_CONFIG_JSON, TEST_MQTT_TOPIC


def test_get_publisher(ecowitt: Ecowitt, mock_asyncio_mqtt_client: MagicMock) -> None:
    """Test getting a publisher via the factory.

    Args:
        ecowitt: A parsed Ecowitt object.
        mock_asyncio_mqtt_client: A mock asyncio-mqtt Client object.
    """
    publisher = get_publisher(ecowitt.configs.default_config, mock_asyncio_mqtt_client)
    assert isinstance(publisher, TopicPublisher)


@pytest.mark.asyncio
async def test_publish_processed(
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    mock_asyncio_mqtt_client: MagicMock,
) -> None:
    """Test publishing a processed payload to an TopicPublisher.

    Args:
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        mock_asyncio_mqtt_client: A mock asyncio-mqtt Client object.
    """
    publisher = get_publisher(ecowitt.configs.default_config, mock_asyncio_mqtt_client)
    await publisher.async_publish(device_data)
    mock_asyncio_mqtt_client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC,
        payload=b'{"runtime": 319206.0, "tempin": 79.52, "humidityin": 31.0, "baromrel": 24.74, "baromabs": 24.74, "temp": 93.2, "humidity": 64.0, "winddir": 139.0, "windspeed": 20.89, "windgust": 1.12, "maxdailygust": 8.05, "solarradiation": 264.61, "uv": 2.0, "rainrate": 0.0, "eventrain": 0.0, "hourlyrain": 0.0, "dailyrain": 0.0, "weeklyrain": 0.0, "monthlyrain": 2.177, "yearlyrain": 4.441, "lightning_num": 13.0, "lightning": 0.6213711922373341, "lightning_time": "2022-04-20T17:17:17+00:00", "wh65batt": "OFF", "beaufortscale": 5, "dewpoint": 79.19328776816637, "feelslike": 111.0553021896001, "frostpoint": 70.28882284994654, "frostrisk": "No risk", "heatindex": 111.0553021896001, "humidex": 48, "humidex_perception": "Dangerous", "humidityabs": 0.001501643470436062, "humidityabsin": 0.001501643470436062, "relative_strain_index": 0.54, "relative_strain_index_perception": "Extreme discomfort", "safe_exposure_time_skin_type_1": 83.3, "safe_exposure_time_skin_type_2": 100.0, "safe_exposure_time_skin_type_3": 133.3, "safe_exposure_time_skin_type_4": 166.7, "safe_exposure_time_skin_type_5": 266.7, "safe_exposure_time_skin_type_6": 433.3, "simmerindex": 113.90619200000002, "simmerzone": "Danger of heatstroke", "solarradiation_perceived": 90.49958322993245, "thermalperception": "Severely high", "windchill": null}',  # noqa: E501
        retain=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("config", [TEST_CONFIG_JSON | {CONF_RAW_DATA: True}])
async def test_publish_raw(
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    mock_asyncio_mqtt_client: MagicMock,
) -> None:
    """Test publishing a raw payload to an TopicPublisher.

    Args:
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        mock_asyncio_mqtt_client: A mock asyncio-mqtt Client object.
    """
    publisher = get_publisher(ecowitt.configs.default_config, mock_asyncio_mqtt_client)
    await publisher.async_publish(device_data)
    mock_asyncio_mqtt_client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC, payload=generate_mqtt_payload(device_data), retain=False
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config", [TEST_CONFIG_JSON | {CONF_MQTT_RETAIN: True, CONF_RAW_DATA: True}]
)
async def test_publish_retain(
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    mock_asyncio_mqtt_client: MagicMock,
) -> None:
    """Test publishing a retained raw payload to an TopicPublisher.

    Args:
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        mock_asyncio_mqtt_client: A mock asyncio-mqtt Client object.
    """
    publisher = get_publisher(ecowitt.configs.default_config, mock_asyncio_mqtt_client)
    await publisher.async_publish(device_data)
    mock_asyncio_mqtt_client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC, payload=generate_mqtt_payload(device_data), retain=True
    )
