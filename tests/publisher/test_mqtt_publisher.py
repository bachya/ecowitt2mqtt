"""Define tests for MQTT publishers."""
from unittest.mock import patch

from asyncio_mqtt import MqttError
import pytest

from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.publisher.mqtt import (
    MqttTopicPublisher,
    PublishError,
    generate_mqtt_payload,
    get_mqtt_publisher,
)

from tests.common import TEST_MQTT_TOPIC


def test_get_publisher(device_payload, ecowitt):
    """Test getting a publisher via the factory."""
    publisher = get_mqtt_publisher(ecowitt)
    assert isinstance(publisher, MqttTopicPublisher)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "device_payload_filename",
    [
        "payload_gw1000bpro.json",
        "payload_gw1000pro.json",
        "payload_gw1100b.json",
        "payload_gw2000a_1.json",
        "payload_gw2000a_2.json",
        "payload_pthp2550pro.json",
        "payload_ws2900.json",
    ],
)
async def test_publish_raw_data(
    device_payload,
    device_payload_filename,
    ecowitt,
):
    """Test publishing a payload to an MqttTopicPublisher."""
    publisher = get_mqtt_publisher(ecowitt)

    # Test publishing raw data:
    await publisher.async_publish(device_payload)
    publisher.client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC, generate_mqtt_payload(device_payload)
    )

    # Test publishing processed data:
    processed_data = ProcessedData(ecowitt, device_payload)
    await publisher.async_publish(processed_data.output)
    publisher.client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC, generate_mqtt_payload(processed_data.output)
    )


@pytest.mark.asyncio
async def test_publish_error_mqtt(device_payload, ecowitt):
    """Test handling an asyncio-mqtt error when publishing to an MQTT topic."""
    publisher = get_mqtt_publisher(ecowitt)
    with patch.object(publisher.client, "publish", side_effect=MqttError):
        with pytest.raises(PublishError):
            await publisher.async_publish(device_payload)


@pytest.mark.asyncio
async def test_publish_error_unserializable(ecowitt):
    """Test handling a serialization error when publishing to an MQTT topic."""
    publisher = get_mqtt_publisher(ecowitt)
    with pytest.raises(TypeError):
        await publisher.async_publish({"Test": object()})
