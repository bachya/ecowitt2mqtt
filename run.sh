#!/bin/sh
if [ -z "${MQTT_BROKER}" ]; then
    echo "Missing required environment variable: MQTT_BROKER"
    exit 1
fi

if [ -z "${MQTT_TOPIC}" ] && [ "${HASS_DISCOVERY}" != "true" ]; then
    echo "Missing required environment variable: either MQTT_TOPIC or HASS_DISCOVERY"
    exit 1
fi

ECOWITT2MQTT_ARGS="--mqtt-broker=${MQTT_BROKER} --mqtt-topic=${MQTT_TOPIC}"

if [ -n "${LOG_LEVEL}" ]; then
    ECOWITT2MQTT_ARGS="${ECOWITT2MQTT_ARGS} --log-level=${LOG_LEVEL}"
fi

if [ -n "${MQTT_PORT}" ]; then
    ECOWITT2MQTT_ARGS="${ECOWITT2MQTT_ARGS} --mqtt-port=${MQTT_PORT}"
fi

if [ -n "${MQTT_USERNAME}" ]; then
    ECOWITT2MQTT_ARGS="${ECOWITT2MQTT_ARGS} --mqtt-username=${MQTT_USERNAME}"
fi

if [ -n "${MQTT_PASSWORD}" ]; then
    ECOWITT2MQTT_ARGS="${ECOWITT2MQTT_ARGS} --mqtt-password=${MQTT_PASSWORD}"
fi

if [ "${HASS_DISCOVERY}" = "true" ]; then
    ECOWITT2MQTT_ARGS="${ECOWITT2MQTT_ARGS} --hass-discovery"
fi

if [ -n "${HASS_DISCOVERY_PREFIX}" ]; then
    ECOWITT2MQTT_ARGS="${ECOWITT2MQTT_ARGS} --hass-discovery-prefix=${HASS_DISCOVERY_PREFIX}"
fi

if [ -n "${ENDPOINT}" ]; then
    ECOWITT2MQTT_ARGS="${ECOWITT2MQTT_ARGS} --endpoint=${ENDPOINT}"
fi

if [ -n "${PORT}" ]; then
    ECOWITT2MQTT_ARGS="${ECOWITT2MQTT_ARGS} --port=${PORT}"
fi

# Store the options string as an environment variable that supervisor can use:
export ECOWITT2MQTT_ARGS

/usr/bin/supervisord -c /etc/supervisord.conf
