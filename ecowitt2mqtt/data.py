"""Define helpers to process data from an Ecowitt device."""
import meteocalc

from ecowitt2mqtt.const import (
    DATA_POINT_DEWPOINT,
    DATA_POINT_FEELSLIKEF,
    DATA_POINT_HEATINDEX,
    DATA_POINT_HUMIDITY,
    DATA_POINT_TEMPF,
    DATA_POINT_WINDCHILL,
    DATA_POINT_WINDSPEEDMPH,
    LOGGER,
)


def process_data_payload(data: dict) -> dict:
    """Process incoming data from an Ecowitt device."""
    for ignore_key in ("dateutc", "freq", "model", "stationtype"):
        data.pop(ignore_key, None)

    humidity = int(data[DATA_POINT_HUMIDITY])
    temperature = meteocalc.Temp(data[DATA_POINT_TEMPF], "f")
    wind_speed = float(data[DATA_POINT_WINDSPEEDMPH])

    dew_point = meteocalc.dew_point(temperature, humidity)
    data[DATA_POINT_DEWPOINT] = dew_point.f

    heat_index = meteocalc.heat_index(temperature, humidity)
    data[DATA_POINT_HEATINDEX] = heat_index.f

    try:
        wind_chill = meteocalc.wind_chill(temperature, wind_speed)
    except ValueError as err:
        LOGGER.debug(
            "%s (temperature: %s, wind speed: %s)", err, temperature.f, wind_speed,
        )
    else:
        data[DATA_POINT_WINDCHILL] = wind_chill.f

    feels_like = meteocalc.feels_like(temperature, humidity, wind_speed)
    data[DATA_POINT_FEELSLIKEF] = feels_like.f

    return data
