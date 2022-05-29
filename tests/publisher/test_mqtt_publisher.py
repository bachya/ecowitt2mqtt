"""Define tests for MQTT publishers."""
from unittest.mock import AsyncMock

from asyncio_mqtt import MqttError
import pytest

from ecowitt2mqtt.publisher.mqtt import (
    MqttTopicPublisher,
    PublishError,
    get_mqtt_publisher,
)

from tests.common import TEST_MQTT_TOPIC


def test_get_publisher(
    asyncio_mqtt_publish, device_payload, ecowitt, setup_asyncio_mqtt
):
    """Test getting a publisher via the factory."""
    publisher = get_mqtt_publisher(ecowitt)
    assert isinstance(publisher, MqttTopicPublisher)


@pytest.mark.asyncio
async def test_publish(
    asyncio_mqtt_publish, device_payload, ecowitt, setup_asyncio_mqtt
):
    """Test publishing to an MqttTopicPublisher."""
    publisher = get_mqtt_publisher(ecowitt)
    await publisher.async_publish(device_payload)
    asyncio_mqtt_publish.assert_awaited_once_with(TEST_MQTT_TOPIC, device_payload)


@pytest.mark.asyncio
@pytest.mark.parametrize("asyncio_mqtt_publish", [AsyncMock(side_effect=MqttError)])
async def test_publish_error(
    asyncio_mqtt_publish, device_payload, ecowitt, setup_asyncio_mqtt
):
    """Test handling an error when publishing to an MQTT topic."""
    publisher = get_mqtt_publisher(ecowitt)
    with pytest.raises(PublishError):
        await publisher.async_publish(device_payload)
    asyncio_mqtt_publish.assert_awaited_once_with(TEST_MQTT_TOPIC, device_payload)
