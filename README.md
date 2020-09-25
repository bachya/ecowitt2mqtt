# 🔘 ecowitt2mqtt: Send Ecowitt device data to an MQTT broker

[![PyPi](https://img.shields.io/pypi/v/ecowitt2mqtt.svg)](https://pypi.python.org/pypi/ecowitt2mqtt)
[![Version](https://img.shields.io/pypi/pyversions/ecowitt2mqtt.svg)](https://pypi.python.org/pypi/ecowitt2mqtt)
[![License](https://img.shields.io/pypi/l/ecowitt2mqtt.svg)](https://github.com/bachya/ecowitt2mqtt/blob/master/LICENSE)
[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/ecowitt2mqtt/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`ecowitt2mqtt` is a small CLI/web server that allows [Ecowitt](http://www.ecowitt.com)
device data to be sent to an MQTT broker.

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Documentation](#documentation)
- [Contributing](#contributing)

# Installation

```python
pip install ecowitt2mqtt
```

# Python Versions

`ecowitt2mqtt` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8 

# Quick Start

Note that this README assumes that you have already paired your Ecowitt device with the
WS View Android/iOS app from Ecowitt.

When viewing your device in the WS View app, select `Weather Services`:

![Select Weather Services](/assets/1-weather-services.jpeg?raw=true)

# Usage

## Command Line Interface

The library is controlled via an `ecowitt2mqtt` executable:

```
usage: ecowitt2mqtt [-h] --mqtt-broker MQTT_BROKER --mqtt-topic MQTT_TOPIC [--mqtt-port MQTT_PORT] [--mqtt-username MQTT_USERNAME]
                    [--mqtt-password MQTT_PASSWORD] [--endpoint ENDPOINT] [--port PORT] [-l LOG_LEVEL]

Send data from Ecowitt devices to an MQTT broker

optional arguments:
  -h, --help            show this help message and exit
  --mqtt-broker MQTT_BROKER
                        The hostname or IP address of the MQTT broker
  --mqtt-topic MQTT_TOPIC
                        The MQTT topic to publish the device's data to
  --mqtt-port MQTT_PORT
                        The port of the MQTT broker (default: 1883)
  --mqtt-username MQTT_USERNAME
                        The username to use with the MQTT broker (default: None)
  --mqtt-password MQTT_PASSWORD
                        The password to use with the MQTT broker (default: None)
  --endpoint ENDPOINT   The relative endpoint/path to serve the web app on (default: /data/report)
  --port PORT           The port to serve the web app on (default: 8080)
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        The logging level (default: INFO)
```
When run with the appropriate parameters, the executable will launch a web server with a
single endpoint (with the default parameters, this endpoint will live at
`http://0.0.0.0:8080/data/report`).

When configured as a custom weather service in the WS View app, this endpoint will
receive data from the Ecowitt device and publish it to the defined MQTT broker.

(TODO: flesh out these docs more)

## Run in the Background

`ecowitt2mqtt` doesn't, itself, provide any sort of daemonization mechanism. The suggested
route is to use something like [`supervisord`](http://www.supervisord.org):

```
[supervisord]
nodaemon=true
loglevel=info
user=root

[program:ecowitt2mqtt]
command=ecowitt2mqtt --mqtt-broker=192.168.1.100 --mqtt-topic=My/topic
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
redirect_stderr=true
```

## Docker

The library is available via a Docker image (`bachya/ecowitt2mqtt`). It is configured by
a handful of environment variables that correspond to the command line parameters listed
above:

* `LOG_LEVEL:` the log level to use (default: `INFO`)
* `ENDPOINT:` the relative endpoint/path to serve the web app on (default: `/data/report`)
* `PORT:` the port to serve the web app on (default: `8080`)
* `MQTT_BROKER:` the hostname or IP address of the MQTT broker
* `MQTT_PORT:` the port of the MQTT broker (default: `1883`)
* `MQTT_PASSWORD:` the password to use with the MQTT broker (default: `None`)
* `MQTT_USERNAME:` the password to use with the MQTT broker (default: `None`)
* `MQTT_TOPIC:` the MQTT topic to publish the device's data to

An example `docker-compose` usage can be found in `docker-compose.dist.yml`.

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/ecowitt2mqtt/issues)
  or [initiate a discussion on one](https://github.com/bachya/ecowitt2mqtt/issues/new).
2. [Fork the repository](https://github.com/bachya/ecowitt2mqtt/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
