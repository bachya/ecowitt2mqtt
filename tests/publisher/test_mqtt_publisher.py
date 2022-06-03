"""Define tests for MQTT publishers."""
from unittest.mock import patch

from asyncio_mqtt import MqttError
import pytest

from ecowitt2mqtt.const import CONF_RAW_DATA
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.data import ProcessedData
from ecowitt2mqtt.publisher.mqtt import (
    MqttTopicPublisher,
    PublishError,
    generate_mqtt_payload,
    get_mqtt_publisher,
)

from tests.common import TEST_MQTT_TOPIC


def test_get_publisher(device_data_gw1000pro, ecowitt):
    """Test getting a publisher via the factory."""
    publisher = get_mqtt_publisher(ecowitt)
    assert isinstance(publisher, MqttTopicPublisher)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "device_payload",
    [
        "device_data_gw1000bpro",
        "device_data_gw1000pro",
        "device_data_gw1100b",
        "device_data_gw2000a_1",
        "device_data_gw2000a_2",
        "device_data_pthp2550pro",
        "device_data_ws2900",
    ],
)
async def test_publish(config, device_payload, ecowitt, request, setup_asyncio_mqtt):
    """Test publishing a payload to an MqttTopicPublisher."""
    device_payload = request.getfixturevalue(device_payload)

    # Test publishing processed data:
    publisher = get_mqtt_publisher(ecowitt)

    await publisher.async_publish(device_payload)
    processed_data = ProcessedData(ecowitt, device_payload)
    publisher.client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC,
        generate_mqtt_payload(
            {key: value.value for key, value in processed_data.output.items()}
        ),
    )

    # Test publishing raw data:
    ecowitt = Ecowitt({**config, CONF_RAW_DATA: True})
    publisher = get_mqtt_publisher(ecowitt)

    await publisher.async_publish(device_payload)
    publisher.client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC, generate_mqtt_payload(device_payload)
    )


@pytest.mark.asyncio
async def test_publish_error_mqtt(device_data_gw1000pro, ecowitt):
    """Test handling an asyncio-mqtt error when publishing to an MQTT topic."""
    publisher = get_mqtt_publisher(ecowitt)
    with patch.object(publisher.client, "publish", side_effect=MqttError):
        with pytest.raises(PublishError):
            await publisher.async_publish(device_data_gw1000pro)


@pytest.mark.asyncio
async def test_publish_error_unserializable(
    device_data_gw1100b, ecowitt, setup_asyncio_mqtt
):
    """Test handling a serialization error when publishing to an MQTT topic."""
    device_data_gw1100b["Test"] = object()
    publisher = get_mqtt_publisher(ecowitt)
    with pytest.raises(TypeError):
        await publisher.async_publish(device_data_gw1100b)
