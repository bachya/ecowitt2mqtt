"""Define tests for the MQTT Topic publisher."""
from unittest.mock import patch

from asyncio_mqtt import MqttError
import pytest

from ecowitt2mqtt.const import CONF_RAW_DATA
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.helpers.publisher import PublishError, generate_mqtt_payload
from ecowitt2mqtt.helpers.publisher.factory import get_publisher
from ecowitt2mqtt.helpers.publisher.topic import TopicPublisher

from tests.common import TEST_MQTT_TOPIC


def test_get_publisher(ecowitt):
    """Test getting a publisher via the factory."""
    publisher = get_publisher(ecowitt)
    assert isinstance(publisher, TopicPublisher)


@pytest.mark.asyncio
async def test_publish(config, device_data, ecowitt, request, setup_asyncio_mqtt):
    """Test publishing a payload to an TopicPublisher."""
    # Test publishing processed data:
    publisher = get_publisher(ecowitt)
    await publisher.async_publish(device_data)

    publisher.client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC,
        b'{"runtime": 319206.0, "tempin": 79.5, "humidityin": 31.0, "baromrel": 24.74, "baromabs": 24.74, "temp": 19.1, "humidity": 34.0, "winddir": 139.0, "windspeed": 20.89, "windgust": 1.12, "maxdailygust": 8.05, "solarradiation": 264.61, "uv": 2.0, "rainrate": 0.0, "eventrain": 0.0, "hourlyrain": 0.0, "dailyrain": 0.0, "weeklyrain": 0.0, "monthlyrain": 2.177, "yearlyrain": 4.441, "lightning_num": 13.0, "lightning": 0.6, "lightning_time": "2022-04-20T17:17:17+00:00", "wh65batt": "OFF", "dewpoint": -4.7, "feelslike": 2.7, "heatindex": 12.3, "solarradiation_lux": 33494.9, "solarradiation_perceived": 90.0, "windchill": 2.7}',
    )

    # Test publishing raw data:
    ecowitt = Ecowitt({**config, CONF_RAW_DATA: True})
    publisher = get_publisher(ecowitt)

    await publisher.async_publish(device_data)
    publisher.client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC, generate_mqtt_payload(device_data)
    )


@pytest.mark.asyncio
async def test_publish_error_mqtt(device_data, ecowitt):
    """Test handling an asyncio-mqtt error when publishing."""
    publisher = get_publisher(ecowitt)
    with patch.object(publisher.client, "publish", side_effect=MqttError):
        with pytest.raises(PublishError):
            await publisher.async_publish(device_data)


@pytest.mark.asyncio
async def test_publish_error_unserializable(device_data, ecowitt, setup_asyncio_mqtt):
    """Test handling a serialization error when publishing."""
    device_data["Test"] = object()
    publisher = get_publisher(ecowitt)
    with pytest.raises(TypeError):
        await publisher.async_publish(device_data)
