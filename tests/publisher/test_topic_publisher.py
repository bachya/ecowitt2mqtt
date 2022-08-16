"""Define tests for the MQTT Topic publisher."""
from asyncio_mqtt import Client, MqttError
import pytest

from ecowitt2mqtt.const import CONF_MQTT_RETAIN, CONF_RAW_DATA
from ecowitt2mqtt.helpers.publisher import generate_mqtt_payload
from ecowitt2mqtt.helpers.publisher.factory import get_publisher
from ecowitt2mqtt.helpers.publisher.topic import TopicPublisher

from tests.common import TEST_CONFIG_JSON, TEST_MQTT_TOPIC


def test_get_publisher(ecowitt):
    """Test getting a publisher via the factory."""
    publisher = get_publisher(ecowitt)
    assert isinstance(publisher, TopicPublisher)


@pytest.mark.asyncio
async def test_publish_processed(
    device_data, ecowitt, mock_asyncio_mqtt_client, setup_asyncio_mqtt
):
    """Test publishing a processed payload to an TopicPublisher."""
    await ecowitt._runtime._publisher.async_publish(
        mock_asyncio_mqtt_client, device_data
    )
    mock_asyncio_mqtt_client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC,
        payload=b'{"runtime": 319206, "tempin": 79.5, "humidityin": 31, "baromrel": 24.74, "baromabs": 24.74, "temp": 93.2, "humidity": 64, "winddir": 139, "windspeed": 20.89, "windgust": 1.12, "maxdailygust": 8.05, "solarradiation": 264.61, "uv": 2, "rainrate": 0.0, "eventrain": 0.0, "hourlyrain": 0.0, "dailyrain": 0.0, "weeklyrain": 0.0, "monthlyrain": 2.177, "yearlyrain": 4.441, "lightning_num": 13, "lightning": 0.6, "lightning_time": "2022-04-20T17:17:17+00:00", "wh65batt": "OFF", "beaufortscale": 5, "dewpoint": 79.2, "feelslike": 111.1, "frostpoint": 70.3, "frostrisk": "No risk", "heatindex": 111.1, "humidityabs": 0.0, "humidityabsin": 0.0, "safe_exposure_time_skin_type_1": 83.3, "safe_exposure_time_skin_type_2": 100.0, "safe_exposure_time_skin_type_3": 133.3, "safe_exposure_time_skin_type_4": 166.7, "safe_exposure_time_skin_type_5": 266.7, "safe_exposure_time_skin_type_6": 433.3, "simmerindex": 113.9, "simmerzone": "Danger of heatstroke", "solarradiation_lux": 33494.9, "solarradiation_perceived": 90.0, "thermalperception": "Severely high", "windchill": null}',
        retain=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        {
            **TEST_CONFIG_JSON,
            CONF_RAW_DATA: True,
        }
    ],
)
async def test_publish_raw(
    device_data, ecowitt, mock_asyncio_mqtt_client, setup_asyncio_mqtt
):
    """Test publishing a raw payload to an TopicPublisher."""
    await ecowitt._runtime._publisher.async_publish(
        mock_asyncio_mqtt_client, device_data
    )
    mock_asyncio_mqtt_client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC, payload=generate_mqtt_payload(device_data), retain=False
    )


@pytest.mark.asyncio
async def test_publish_error_unserializable(
    device_data, ecowitt, mock_asyncio_mqtt_client, setup_asyncio_mqtt
):
    """Test handling a serialization error when publishing."""
    device_data["Test"] = object()
    publisher = get_publisher(ecowitt)
    with pytest.raises(TypeError):
        await publisher.async_publish(mock_asyncio_mqtt_client, device_data)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        {
            **TEST_CONFIG_JSON,
            CONF_MQTT_RETAIN: True,
            CONF_RAW_DATA: True,
        }
    ],
)
async def test_publish_retain(
    device_data, ecowitt, mock_asyncio_mqtt_client, setup_asyncio_mqtt
):
    """Test publishing a retained raw payload to an TopicPublisher."""
    await ecowitt._runtime._publisher.async_publish(
        mock_asyncio_mqtt_client, device_data
    )
    mock_asyncio_mqtt_client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC, payload=generate_mqtt_payload(device_data), retain=True
    )
