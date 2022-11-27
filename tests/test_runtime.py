"""Define tests for the runtime."""
# pylint: disable=line-too-long,too-many-arguments,unused-argument
from __future__ import annotations

import json
import urllib.parse
from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest
from aiohttp import ClientSession
from asyncio_mqtt import MqttError

from ecowitt2mqtt.const import CONF_DIAGNOSTICS, CONF_ENDPOINT, CONF_INPUT_DATA_FORMAT
from ecowitt2mqtt.core import Ecowitt
from ecowitt2mqtt.helpers.server import InputDataFormat
from tests.common import (
    TEST_CONFIG_JSON,
    TEST_ENDPOINT,
    TEST_MQTT_TOPIC,
    TEST_PORT,
    load_fixture,
)


@pytest.mark.asyncio
@pytest.mark.parametrize("mqtt_publish_side_effect", [AsyncMock(side_effect=MqttError)])
async def test_publish_failure(
    caplog: Mock,
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    setup_asyncio_mqtt: AsyncGenerator[None, None],
    setup_uvicorn_server: AsyncGenerator[None, None],
) -> None:
    """Test a failed MQTT publish.

    Args:
        caplog: A mock logging utility.
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        setup_asyncio_mqtt: A mock asyncio-mqtt client connection.
        setup_uvicorn_server: A mock Uvicorn + FastAPI application.
    """
    async with ClientSession() as session:
        await session.request(
            "post", f"http://127.0.0.1:{TEST_PORT}{TEST_ENDPOINT}", data=device_data
        )
    assert any(m for m in caplog.messages if "There was an MQTT error" in m)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        TEST_CONFIG_JSON | {CONF_INPUT_DATA_FORMAT: InputDataFormat.AMBIENT_WEATHER},
    ],
)
async def test_publish_ambient_weather_success(
    caplog: Mock,
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    mock_asyncio_mqtt_client: MagicMock,
    setup_asyncio_mqtt: AsyncGenerator[None, None],
    setup_uvicorn_server: AsyncGenerator[None, None],
) -> None:
    """Test a successful Ambient Weather payload being received and published.

    Args:
        caplog: A mock logging utility.
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        mock_asyncio_mqtt_client: A mocked asyncio-mqtt Client object.
        setup_asyncio_mqtt: A mock asyncio-mqtt client connection.
        setup_uvicorn_server: A mock Uvicorn + FastAPI application.
    """
    ambient_payload = json.loads(load_fixture("payload_ambweather.json"))
    payload_string = urllib.parse.urlencode(ambient_payload)

    async with ClientSession() as session:
        resp = await session.request(
            "get", f"http://127.0.0.1:{TEST_PORT}{TEST_ENDPOINT}{payload_string}"
        )

    assert resp.status == 204
    mock_asyncio_mqtt_client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC,
        payload=b'{"tempin": 67.3, "humidityin": 33.0, "baromrel": 29.616, "baromabs": 24.679, "temp": 53.8, "humidity": 30.0, "winddir": 99.0, "windspeed": 4.5, "windgust": 6.9, "maxdailygust": 14.8, "hourlyrain": 0.0, "eventrain": 0.0, "dailyrain": 0.0, "weeklyrain": 0.024, "monthlyrain": 0.311, "totalrain": 48.811, "solarradiation": 39.02, "uv": 0.0, "beaufortscale": 2, "dewpoint": 23.12793817902528, "feelslike": 53.8, "frostpoint": 20.34536144435649, "frostrisk": "No risk", "heatindex": 50.28999999999999, "humidex": 9, "humidex_perception": "Comfortable", "humidityabs": 0.00020090062644380612, "humidityabsin": 0.00020090062644380612, "relative_strain_index": null, "relative_strain_index_perception": null, "safe_exposure_time_skin_type_1": null, "safe_exposure_time_skin_type_2": null, "safe_exposure_time_skin_type_3": null, "safe_exposure_time_skin_type_4": null, "safe_exposure_time_skin_type_5": null, "safe_exposure_time_skin_type_6": null, "simmerindex": null, "simmerzone": null, "solarradiation_perceived": 73.87320347536115, "thermalperception": "Dry", "windchill": null}',
        retain=False,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "config",
    [
        TEST_CONFIG_JSON | {CONF_ENDPOINT: TEST_ENDPOINT},
        TEST_CONFIG_JSON | {CONF_ENDPOINT: f"{TEST_ENDPOINT}/"},
        TEST_CONFIG_JSON | {CONF_DIAGNOSTICS: True},
    ],
)
async def test_publish_ecowitt_success(
    caplog: Mock,
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    mock_asyncio_mqtt_client: MagicMock,
    setup_asyncio_mqtt: AsyncGenerator[None, None],
    setup_uvicorn_server: AsyncGenerator[None, None],
) -> None:
    """Test a successful Ecowitt payload being received and published.

    Args:
        caplog: A mock logging utility.
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        mock_asyncio_mqtt_client: A mocked asyncio-mqtt Client object.
        setup_asyncio_mqtt: A mock asyncio-mqtt client connection.
        setup_uvicorn_server: A mock Uvicorn + FastAPI application.
    """
    async with ClientSession() as session:
        resp = await session.request(
            "post",
            (
                f"http://127.0.0.1:{TEST_PORT}"
                f"{ecowitt.configs.default_config.endpoint}"
            ),
            data=device_data,
        )

    assert resp.status == 204
    mock_asyncio_mqtt_client.publish.assert_awaited_with(
        TEST_MQTT_TOPIC,
        payload=b'{"runtime": 319206.0, "tempin": 79.52, "humidityin": 31.0, "baromrel": 24.74, "baromabs": 24.74, "temp": 93.2, "humidity": 64.0, "winddir": 139.0, "windspeed": 20.89, "windgust": 1.12, "maxdailygust": 8.05, "solarradiation": 264.61, "uv": 2.0, "rainrate": 0.0, "eventrain": 0.0, "hourlyrain": 0.0, "dailyrain": 0.0, "weeklyrain": 0.0, "monthlyrain": 2.177, "yearlyrain": 4.441, "lightning_num": 13.0, "lightning": 0.6213711922373341, "lightning_time": "2022-04-20T17:17:17+00:00", "wh65batt": "OFF", "beaufortscale": 5, "dewpoint": 79.19328776816637, "feelslike": 111.0553021896001, "frostpoint": 70.28882284994654, "frostrisk": "No risk", "heatindex": 111.0553021896001, "humidex": 48, "humidex_perception": "Dangerous", "humidityabs": 0.001501643470436062, "humidityabsin": 0.001501643470436062, "relative_strain_index": 0.54, "relative_strain_index_perception": "Extreme discomfort", "safe_exposure_time_skin_type_1": 83.3, "safe_exposure_time_skin_type_2": 100.0, "safe_exposure_time_skin_type_3": 133.3, "safe_exposure_time_skin_type_4": 166.7, "safe_exposure_time_skin_type_5": 266.7, "safe_exposure_time_skin_type_6": 433.3, "simmerindex": 113.90619200000002, "simmerzone": "Danger of heatstroke", "solarradiation_perceived": 90.49958322993245, "thermalperception": "Severely high", "windchill": null}',
        retain=False,
    )

    if ecowitt.configs.default_config.diagnostics:
        assert any(m for m in caplog.messages if "DIAGNOSTICS COLLECTED" in m)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "mqtt_publish_side_effect",
    [AsyncMock(side_effect=Exception("Something horrible happened"))],
)
async def test_unknown_exception_shutdown(
    caplog: Mock,
    device_data: dict[str, Any],
    ecowitt: Ecowitt,
    setup_asyncio_mqtt: AsyncGenerator[None, None],
    setup_uvicorn_server: AsyncGenerator[None, None],
) -> None:
    """Test that an unknown exception successfully shuts down the runtime.

    Args:
        caplog: A mock logging utility.
        device_data: A dictionary of device data.
        ecowitt: A parsed Ecowitt object.
        setup_asyncio_mqtt: A mock asyncio-mqtt client connection.
        setup_uvicorn_server: A mock Uvicorn + FastAPI application.
    """
    async with ClientSession() as session:
        await session.request(
            "post", f"http://127.0.0.1:{TEST_PORT}{TEST_ENDPOINT}", data=device_data
        )
    assert any(m for m in caplog.messages if "Something horrible happened" in m)
