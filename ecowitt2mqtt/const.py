"""Define constants."""
import logging

LOGGER = logging.getLogger(__package__)

# Glob data points:
DATA_POINT_GLOB_BAROM = "barom"
DATA_POINT_GLOB_BATT = "batt"
DATA_POINT_GLOB_GUST = "gust"
DATA_POINT_GLOB_HUMIDITY = "humidity"
DATA_POINT_GLOB_MOISTURE = "moisture"
DATA_POINT_GLOB_RAIN = "rain"
DATA_POINT_GLOB_TEMP = "temp"
DATA_POINT_GLOB_WIND = "wind"

# Specific data points:
DATA_POINT_CO2 = "co2"
DATA_POINT_DEWPOINT = "dewpoint"
DATA_POINT_FEELSLIKE = "feelslike"
DATA_POINT_HEATINDEX = "heatindex"
DATA_POINT_HUMIDITY = "humidity"
DATA_POINT_PM25 = "pm25"
DATA_POINT_PM25_24H = "pm25_24h"
DATA_POINT_SOLARRADIATION = "solarradiation"
DATA_POINT_SOLARRADIATION_LUX = "solarradiation_lux"
DATA_POINT_SOLARRADIATION_PERCEIVED = "solarradiation_perceived"
DATA_POINT_TEMPF = "tempf"
DATA_POINT_UV = "uv"
DATA_POINT_WINDCHILL = "windchill"
DATA_POINT_WINDDIR = "winddir"
DATA_POINT_WINDSPEEDMPH = "windspeedmph"

# Unit systems:
UNIT_SYSTEM_IMPERIAL = "imperial"
UNIT_SYSTEM_METRIC = "metric"
