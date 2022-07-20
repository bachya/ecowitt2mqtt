"""Define package constants."""
import logging
from typing import Final

from ecowitt2mqtt.helpers.typing import UnitSystemType

__version__ = "2022.07.2"


LOGGER = logging.getLogger(__package__)

# Configuration keys:
CONF_BATTERY_OVERRIDES: Final = "battery_override"
CONF_CONFIG: Final = "config"
CONF_DEFAULT_BATTERY_STRATEGY: Final = "default_battery_strategy"
CONF_DIAGNOSTICS: Final = "diagnostics"
CONF_ENDPOINT: Final = "endpoint"
CONF_HASS_DISCOVERY: Final = "hass_discovery"
CONF_HASS_DISCOVERY_PREFIX: Final = "hass_discovery_prefix"
CONF_HASS_ENTITY_ID_PREFIX: Final = "hass_entity_id_prefix"
CONF_INPUT_UNIT_SYSTEM: Final = "input_unit_system"
CONF_MQTT_BROKER: Final = "mqtt_broker"
CONF_MQTT_PASSWORD: Final = "mqtt_password"
CONF_MQTT_PORT: Final = "mqtt_port"
CONF_MQTT_TLS: Final = "mqtt_tls"
CONF_MQTT_TOPIC: Final = "mqtt_topic"
CONF_MQTT_USERNAME: Final = "mqtt_username"
CONF_OUTPUT_UNIT_SYSTEM: Final = "output_unit_system"
CONF_PORT: Final = "port"
CONF_RAW_DATA: Final = "raw_data"
CONF_VERBOSE: Final = "verbose"

# Data points (glob):
DATA_POINT_GLOB_BAROM: Final = "barom"
DATA_POINT_GLOB_BATT: Final = "batt"
DATA_POINT_GLOB_GUST: Final = "gust"
DATA_POINT_GLOB_HUMIDITY: Final = "humidity"
DATA_POINT_GLOB_LEAFBATT: Final = "leaf_batt"
DATA_POINT_GLOB_LEAK: Final = "leak"
DATA_POINT_GLOB_LEAKBATT: Final = "leakbatt"
DATA_POINT_GLOB_MOISTURE: Final = "moisture"
DATA_POINT_GLOB_PM10: Final = "pm10"
DATA_POINT_GLOB_PM25: Final = "pm25"
DATA_POINT_GLOB_PM25BATT: Final = "pm25batt"
DATA_POINT_GLOB_RAIN: Final = "rain"
DATA_POINT_GLOB_R_RAIN: Final = "rrain"
DATA_POINT_GLOB_SOILBATT: Final = "soilbatt"
DATA_POINT_GLOB_TEMP: Final = "temp"
DATA_POINT_GLOB_TF: Final = "tf"
DATA_POINT_GLOB_TF_BATT: Final = "tf_batt"
DATA_POINT_GLOB_VOLT: Final = "volt"
DATA_POINT_GLOB_WETNESS: Final = "wetness"
DATA_POINT_GLOB_WIND: Final = "wind"
DATA_POINT_GLOB_WINDDIR: Final = "winddir"

# Data points (specific):
DATA_POINT_CO2: Final = "co2"
DATA_POINT_CO2_24H: Final = "co2_24h"
DATA_POINT_CO2_BATT: Final = "co2_batt"
DATA_POINT_DAILY_RAIN: Final = "dailyrain"
DATA_POINT_DEWPOINT: Final = "dewpoint"
DATA_POINT_DRAIN_PIEZO: Final = "drain_piezo"
DATA_POINT_ERAIN_PIEZO: Final = "erain_piezo"
DATA_POINT_EVENT_RAIN: Final = "eventrain"
DATA_POINT_FEELSLIKE: Final = "feelslike"
DATA_POINT_FROST_POINT: Final = "frostpoint"
DATA_POINT_FROST_RISK: Final = "frostrisk"
DATA_POINT_HEATINDEX: Final = "heatindex"
DATA_POINT_HOURLY_RAIN: Final = "hourlyrain"
DATA_POINT_HRAIN_PIEZO: Final = "hrain_piezo"
DATA_POINT_HUMIDITY: Final = "humidity"
DATA_POINT_HUMIDITY_ABS: Final = "humidityabs"
DATA_POINT_HUMIDITY_ABS_IN: Final = "humidityabsin"
DATA_POINT_HUMI_CO2: Final = "humi_co2"
DATA_POINT_LIGHTNING: Final = "lightning"
DATA_POINT_LIGHTNING_NUM: Final = "lightning_num"
DATA_POINT_LIGHTNING_TIME: Final = "lightning_time"
DATA_POINT_MONTHLY_RAIN: Final = "monthlyrain"
DATA_POINT_MRAIN_PIEZO: Final = "mrain_piezo"
DATA_POINT_RAIN_RATE: Final = "rainrate"
DATA_POINT_RUNTIME: Final = "runtime"
DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_1: Final = "safe_exposure_time_skin_type_1"
DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_2: Final = "safe_exposure_time_skin_type_2"
DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_3: Final = "safe_exposure_time_skin_type_3"
DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_4: Final = "safe_exposure_time_skin_type_4"
DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_5: Final = "safe_exposure_time_skin_type_5"
DATA_POINT_SAFE_EXPOSURE_TIME_SKIN_TYPE_6: Final = "safe_exposure_time_skin_type_6"
DATA_POINT_SIMMER_INDEX: Final = "simmerindex"
DATA_POINT_SIMMER_ZONE: Final = "simmerzone"
DATA_POINT_SOLARRADIATION: Final = "solarradiation"
DATA_POINT_SOLARRADIATION_LUX: Final = "solarradiation_lux"
DATA_POINT_SOLARRADIATION_PERCEIVED: Final = "solarradiation_perceived"
DATA_POINT_TEMPF: Final = "tempf"
DATA_POINT_TEMPINF: Final = "tempinf"
DATA_POINT_TF_CO2: Final = "tf_co2"
DATA_POINT_THERMAL_PERCEPTION: Final = "thermalperception"
DATA_POINT_TOTAL_AIN: Final = "totalain"
DATA_POINT_TOTAL_RAIN: Final = "totalrain"
DATA_POINT_UV: Final = "uv"
DATA_POINT_WEEKLY_RAIN: Final = "weeklyrain"
DATA_POINT_WH25BATT: Final = "wh25batt"
DATA_POINT_WH26BATT: Final = "wh26batt"
DATA_POINT_WH40BATT: Final = "wh40batt"
DATA_POINT_WH57BATT: Final = "wh57batt"
DATA_POINT_WH65BATT: Final = "wh65batt"
DATA_POINT_WH68BATT: Final = "wh68batt"
DATA_POINT_WH80BATT: Final = "wh80batt"
DATA_POINT_WH90BATT: Final = "wh90batt"
DATA_POINT_WH90BATT_PC: Final = "wh90battpc"
DATA_POINT_WH90CAP_VOLT: Final = "ws90cap_volt"
DATA_POINT_WINDCHILL: Final = "windchill"
DATA_POINT_WINDSPEEDMPH: Final = "windspeedmph"
DATA_POINT_WRAIN_PIEZO: Final = "wrain_piezo"
DATA_POINT_YEARLY_RAIN: Final = "yearlyrain"
DATA_POINT_YRAIN_PIEZO: Final = "yrain_piezo"

# Environment variables:
ENV_BATTERY_OVERRIDE: Final = "ECOWITT2MQTT_BATTERY_OVERRIDE"
ENV_CONFIG: Final = "ECOWITT2MQTT_CONFIG"
ENV_DEFAULT_BATTERY_STRATEGY: Final = "ECOWITT2MQTT_DEFAULT_BATTERY_STRATEGY"
ENV_DIAGNOSTICS: Final = "ECOWITT2MQTT_DIAGNOSTICS"
ENV_ENDPOINT: Final = "ECOWITT2MQTT_ENDPOINT"
ENV_HASS_DISCOVERY: Final = "ECOWITT2MQTT_HASS_DISCOVERY"
ENV_HASS_DISCOVERY_PREFIX: Final = "ECOWITT2MQTT_HASS_DISCOVERY_PREFIX"
ENV_HASS_ENTITY_ID_PREFIX: Final = "ECOWITT2MQTT_HASS_ENTITY_ID_PREFIX"
ENV_INPUT_UNIT_SYSTEM: Final = "ECOWITT2MQTT_INPUT_UNIT_SYSTEM"
ENV_MQTT_BROKER: Final = "ECOWITT2MQTT_MQTT_BROKER"
ENV_MQTT_PASSWORD: Final = "ECOWITT2MQTT_MQTT_PASSWORD"
ENV_MQTT_PORT: Final = "ECOWITT2MQTT_MQTT_PORT"
ENV_MQTT_TLS: Final = "ECOWITT2MQTT_MQTT_TLS"
ENV_MQTT_TOPIC: Final = "ECOWITT2MQTT_MQTT_TOPIC"
ENV_MQTT_USERNAME: Final = "ECOWITT2MQTT_MQTT_USERNAME"
ENV_OUTPUT_UNIT_SYSTEM: Final = "ECOWITT2MQTT_OUTPUT_UNIT_SYSTEM"
ENV_PORT: Final = "ECOWITT2MQTT_PORT"
ENV_RAW_DATA: Final = "ECOWITT2MQTT_RAW_DATA"
ENV_VERBOSE: Final = "ECOWITT2MQTT_VERBOSE"

# Legacy environment variables that will be deprecated at some point:
LEGACY_ENV_ENDPOINT: Final = "ENDPOINT"
LEGACY_ENV_HASS_DISCOVERY: Final = "HASS_DISCOVERY"
LEGACY_ENV_HASS_DISCOVERY_PREFIX: Final = "HASS_DISCOVERY_PREFIX"
LEGACY_ENV_HASS_ENTITY_ID_PREFIX: Final = "HASS_ENTITY_ID_PREFIX"
LEGACY_ENV_INPUT_UNIT_SYSTEM: Final = "INPUT_UNIT_SYSTEM"
LEGACY_ENV_LOG_LEVEL: Final = "LOG_LEVEL"
LEGACY_ENV_MQTT_BROKER: Final = "MQTT_BROKER"
LEGACY_ENV_MQTT_PASSWORD: Final = "MQTT_PASSWORD"
LEGACY_ENV_MQTT_PORT: Final = "MQTT_PORT"
LEGACY_ENV_MQTT_TOPIC: Final = "MQTT_TOPIC"
LEGACY_ENV_MQTT_USERNAME: Final = "MQTT_USERNAME"
LEGACY_ENV_OUTPUT_UNIT_SYSTEM: Final = "OUTPUT_UNIT_SYSTEM"
LEGACY_ENV_PORT: Final = "PORT"
LEGACY_ENV_RAW_DATA: Final = "RAW_DATA"

# Unit systems:
UNIT_SYSTEM_IMPERIAL: UnitSystemType = "imperial"
UNIT_SYSTEM_METRIC: UnitSystemType = "metric"

# Degree units
DEGREE: Final = "°"

# Distance units:
DISTANCE_KILOMETERS: Final = "km"
DISTANCE_MILES: Final = "mi"

# Electric_potential units:
ELECTRIC_POTENTIAL_VOLT: Final = "V"

# Irradiation units
IRRADIATION_WATTS_PER_SQUARE_METER: Final = "W/m²"

# Light units:
LIGHT_LUX: Final = "lx"

# Lightning units:
STRIKES: Final = "strikes"

# Percentage units
PERCENTAGE: Final = "%"

# Pollution units:
CONCENTRATION_MICROGRAMS_PER_CUBIC_METER: Final = "µg/m³"
CONCENTRATION_PARTS_PER_MILLION: Final = "ppm"

# Pressure units:
PRESSURE_HPA: Final = "hPa"
PRESSURE_INHG: Final = "inHg"

# Speed units:
SPEED_KILOMETERS_PER_HOUR: Final = "km/h"
SPEED_MILES_PER_HOUR: Final = "mph"

# Temperature units:
TEMP_CELSIUS: Final = "°C"
TEMP_FAHRENHEIT: Final = "°F"

# Time units
TIME_MINUTES: Final = "min"
TIME_SECONDS: Final = "s"

# UV units:
UV_INDEX: Final = "UV index"

# Volume units:
RAINFALL_INCHES: Final = "in"
RAINFALL_MILLIMETERS: Final = "mm"
WATER_VAPOR_GRAMS_PER_CUBIC_METER: Final = "g/m³"
WATER_VAPOR_POUNDS_PER_CUBIC_FOOT: Final = "lbs/ft³"
