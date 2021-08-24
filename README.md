# 🔘 ecowitt2mqtt: Send Ecowitt device data to an MQTT broker

[![PyPi](https://img.shields.io/pypi/v/ecowitt2mqtt.svg)](https://pypi.python.org/pypi/ecowitt2mqtt)
[![Docker Hub](https://img.shields.io/docker/pulls/bachya/ecowitt2mqtt)](https://hub.docker.com/r/bachya/ecowitt2mqtt)
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
* `Port`: `8080` (the default port on which `ecowitt2mqtt` is served)
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
  --raw-data            Return raw data (don't attempt to translate any values)
  --input-unit-system INPUT_UNIT_SYSTEM
                        The input unit system used by the device (default: imperial)
  --output-unit-system OUTPUT_UNIT_SYSTEM
                        The unit system to use in output (default: imperial)
```
## Unit Systems

`ecowitt2mqtt` allows you to specify both the input and output unit systems for a device.
This is fairly self-explanatory, but take care to use an `--input-unit-system` that is
consistent with what your device provides (otherwise, your data will be way off).

## Raw Data

In some cases, it may be preferable to prevent `ecowitt2mqtt` from doing any data
translation (converting values to a new unit system, changing binary values – such as
might be used by a battery – into "friendly" values, etc.). Passing the `--raw-data` flag
will accomplish this: data will flow directly from the Ecowitt device to the MQTT broker
as-is.

Note that the `--raw-data` flag supersedes any that might cause data translation (such as
`--input-unit-system` or `--output-unit-system`).

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

## Running in the Background

`ecowitt2mqtt` doesn't, itself, provide any sort of daemonization mechanism. The suggested
route is to use a different application.

### `supervisord`

An example `supervisord` configuration file might look like this:

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

### `systemd`

An example `systemd` service file in `/etc/systemd/system` might look like this:

```
[Unit]
Description=ECOWITT2MQTT daemon
After=network.target
 
[Service]
Type=notify
ExecStart=ecowitt2mqtt --mqtt-broker=192.168.1.101 --mqtt-username=user --mqtt-password=password
ExecReload=kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartSec=5s
 
[Install]
WantedBy=multi-user.target
```

To enable the service:

```bash
$ systemctl enable ecowitt2mqtt
```

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
* `INPUT_UNIT_SYSTEM`: the input unit system to use (`imperial` or `metric`) (default: `imperial`)
* `OUTPUT_UNIT_SYSTEM`: the output unit system to use (`imperial` or `metric`) (default: `imperial`)

Running the image is straightforward:

```
docker run -it \
    -e MQTT_BROKER=192.168.1.101 \
    -e MQTT_USERNAME=user \
    -e MQTT_PASSWORD=password \
    -p 8080:8080 \
    bachya/ecowitt2mqtt:latest
```

Note the value of the `-p` flag: you must expose the port defined by the `PORT`
environment variable. In the example above, the default port (`8080`) is used and is
exposed via the same port on the host.

[`docker-compose`](https://docs.docker.com/compose/) users can find an example
configuration file at
[`docker-compose.dev.yml`](https://github.com/bachya/ecowitt2mqtt/blob/dev/docker-compose.dev.yml).
Note that this is intended to be a dev environment for quickly testing the repo itself;
in production, you should refer to one of the
[Docker Hub](https://hub.docker.com/r/bachya/ecowitt2mqtt) images.

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
