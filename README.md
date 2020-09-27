# 🔘 ecowitt2mqtt: Send Ecowitt device data to an MQTT broker

[![PyPi](https://img.shields.io/pypi/v/ecowitt2mqtt.svg)](https://pypi.python.org/pypi/ecowitt2mqtt)
[![Docker Hub](https://img.shields.io/docker/cloud/build/bachya/ecowitt2mqtt.svg)](https://hub.docker.com/r/bachya/ecowitt2mqtt)
[![Version](https://img.shields.io/pypi/pyversions/ecowitt2mqtt.svg)](https://pypi.python.org/pypi/ecowitt2mqtt)
[![License](https://img.shields.io/pypi/l/ecowitt2mqtt.svg)](https://github.com/bachya/ecowitt2mqtt/blob/master/LICENSE)
[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/ecowitt2mqtt/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`ecowitt2mqtt` is a small CLI/web server that allows [Ecowitt](http://www.ecowitt.com)
device data to be sent to an MQTT broker.

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Quick Start](#quick-start)
- [Advanced Usage](#advanced-usage)
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

Note that this README assumes:

* you have access to an MQTT broker
* you have already paired your Ecowitt device with the WS View Android/iOS app from
  Ecowitt.

First, install `ecowitt2mqtt` via `pip`:

```bash
$ pip install ecowitt2mqtt
```

Then, shift over to the WS View app on your Android/iOS device. While viewing your
device in the app, select `Weather Services`:

![Select Weather Services](https://raw.githubusercontent.com/bachya/ecowitt2mqtt/dev/assets/1-weather-services.jpeg?raw=true)

Press `Next` until you reach the `Customized` screen:

![The Customized screen in the WS View app](https://raw.githubusercontent.com/bachya/ecowitt2mqtt/dev/assets/2-customized.jpeg?raw=true)

Fill out the form with these values and tap `Save`:

* `Protocol Type Same As`: `Ecowitt`
* `Server IP / Hostname`: the IP address/hostname of the device running `ecowitt2mqtt`
* `Path`: `/data/report` (note that unlike the default in the WS View App, there shouldn't
  be a trailing slash)
* `Port`: `8080`
* `Upload Interval`: `60` (change this to alter the frequency with which data is published)

Then, on the machine where you installed `ecowitt2mqtt`, run it:

```bash
$ ecowitt2mqtt \
    --mqtt-broker=192.168.1.101 \
    --mqtt-username=user \
    --mqtt-password=password \
    --mqtt-topic=ecowitt2mqtt/device_1
```

Within the `Upload Interval`, data should begin to appear in the MQTT broker.

# Advanced Usage

## Command Line Interface

The `ecowitt2mqtt` executable contains several configurable parameters:
```
usage: ecowitt2mqtt [-h] --mqtt-broker MQTT_BROKER --mqtt-topic MQTT_TOPIC [--mqtt-port MQTT_PORT]
                    [--mqtt-username MQTT_USERNAME] [--mqtt-password MQTT_PASSWORD]
                    [--endpoint ENDPOINT] [--port PORT] [-l LOG_LEVEL]

Send data from Ecowitt devices to an MQTT broker

optional arguments:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        The logging level (default: INFO)
  --mqtt-broker MQTT_BROKER
                        The hostname or IP address of the MQTT broker
  --mqtt-port MQTT_PORT
                        The port of the MQTT broker (default: 1883)
  --mqtt-username MQTT_USERNAME
                        The username to use with the MQTT broker (default: None)
  --mqtt-password MQTT_PASSWORD
                        The password to use with the MQTT broker (default: None)
  --mqtt-topic MQTT_TOPIC
                        The MQTT topic to publish the device's data to (default: ecowitt2mqtt/<ID>)
  --hass-discovery      Publish data in the Home Assistant MQTT Discovery format
  --hass-discovery-prefix HASS_DISCOVERY_PREFIX
                        The Home Assistant discovery prefix to use (default: homeassistant)
  --endpoint ENDPOINT   The relative endpoint/path to serve the web app on (default: /data/report)
  --port PORT           The port to serve the web app on (default: 8080)
```

## Running in the Background

`ecowitt2mqtt` doesn't, itself, provide any sort of daemonization mechanism. The suggested
route is to use something like [`supervisord`](http://www.supervisord.org):

```
[supervisord]
nodaemon=true
loglevel=info
user=root

[program:ecowitt2mqtt]
command=ecowitt2mqtt --mqtt-broker=192.168.1.101 --mqtt-username=user --mqtt-password=password
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
redirect_stderr=true
```

## Home Assistant MQTT Discovery

[Home Assistant](https://home-assistant.io) users can quickly add entities from an
Ecowitt device by using
[MQTT Discovery](https://www.home-assistant.io/docs/mqtt/discovery/).

Once Home Assistant is configured to accept MQTT Discovery, `ecowitt2mqtt` simply needs
the `--hass-discovery` flag:

```bash
$ ecowitt2mqtt \
    --mqtt-broker=192.168.1.101 \
    --mqtt-username=user \
    --mqtt-password=password \
    --hass-discovery
```

Note that if both `--hass-discovery` and `--mqtt-topic` are provided, `--hass-discovery` will
win out.

## Docker

The library is available via a Docker image
([`bachya/ecowitt2mqtt`](https://hub.docker.com/r/bachya/ecowitt2mqtt)). It is configured
by a handful of environment variables that correspond to the command line parameters
listed above:

* `LOG_LEVEL:` the log level to use (default: `INFO`)
* `MQTT_BROKER:` the hostname or IP address of the MQTT broker
* `MQTT_PORT:` the port of the MQTT broker (default: `1883`)
* `MQTT_PASSWORD:` the password to use with the MQTT broker (default: `None`)
* `MQTT_USERNAME:` the password to use with the MQTT broker (default: `None`)
* `MQTT_TOPIC:` the MQTT topic to publish the device's data to
* `HASS_DISCOVERY`: whether to use Home Assistant MQTT Discovery (default: `false`)
* `HASS_DISCOVERY_PREFIX`: the topic prefix to use for Home Assistant MQTT Discovery
  (default: `homeassistant`)
* `ENDPOINT:` the relative endpoint/path to serve the web app on (default: `/data/report`)
* `PORT:` the port to serve the web app on (default: `8080`)

Running the image is straightforward:

```
docker run -it \
    -e MQTT_BROKER=192.168.1.101 \
    -e MQTT_USERNAME=user \
    -e MQTT_PASSWORD=password \
    -p 8080:8080 \
    bachya/ecowitt2mqtt:latest
```

Note the value of the `-p` flag: you must expose the port defined by the `MQTT_PORT`
environment variable. In the example above, the default port (`8080`) is used and is
exposed via the same port on the host.

[`docker-compose`](https://docs.docker.com/compose/) users can find an example
configuration file at
[`docker-compose.dist.yml`](https://github.com/bachya/ecowitt2mqtt/blob/dev/docker-compose.dist.yml).

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/ecowitt2mqtt/issues)
or [initiate a discussion on one](https://github.com/bachya/ecowitt2mqtt/issues/new).
2. [Fork the repository](https://github.com/bachya/ecowitt2mqtt/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Update `README.md` with any new documentation.
8. Add yourself to `AUTHORS.md`.
9. Submit a pull request!
