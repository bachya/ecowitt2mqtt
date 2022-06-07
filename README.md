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
- [Configuration](#configuration)
  * [Command Line Options](#command-line-options)
  * [Environment Variables](#environment-variables)
  * [Configuration File](#configuration-file)
  * [Merging Configuration Options](#merging-configuration-options)
- [Advanced Usage](#advanced-usage)
  * [Unit Systems](#unit-systems)
  * [Raw Data](#raw-data)
  * [Home Assistant](#home-assistant)
    + [MQTT Discovery](#mqtt-discovery)
    + [Custom Entity ID Prefix](#custom-entity-id-prefix)
  * [Running in the Background](#running-in-the-background)
    + [`supervisord`](#-supervisord-)
    + [`systemd`](#-systemd-)
  * [Docker](#docker)
- [Contributing](#contributing)

# Installation

```python
pip install ecowitt2mqtt
```

# Python Versions

`ecowitt2mqtt` is currently supported on:

* Python 3.8
* Python 3.9
* Python 3.10

# Quick Start

Note that this README assumes that:

* you have access to an MQTT broker.
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

# Configuration

`ecowitt2mqtt` can be configured via command line options, environment variables, or a
(YAML or JSON) config file.

## Command Line Options

```
Usage: ecowitt2mqtt [OPTIONS] COMMAND [ARGS]...

  ecowitt2mqtt sends Ecowitt device data to an MQTT broker.

Options:
  --battery-override TEXT         A battery configuration override
                                  (format: key,value)  [env var:
                                  ECOWITT2MQTT_BATTERY_OVERRIDE]
  -c, --config FILE               A path to a config file.  [env
                                  var: ECOWITT2MQTT_CONFIG]
  --default-battery-strategy TEXT
                                  The default battery config
                                  strategy to use.  [env var: ECOW
                                  ITT2MQTT_DEFAULT_BATTERY_STRATEG
                                  Y; default: boolean]
  -e, --endpoint TEXT             The relative endpoint/path to
                                  serve ecowitt2mqtt on.  [env
                                  var: ECOWITT2MQTT_ENDPOINT,
                                  ENDPOINT; default: /data/report]
  --hass-discovery                Publish data in the Home
                                  Assistant MQTT Discovery format.
                                  [env var:
                                  ECOWITT2MQTT_HASS_DISCOVERY,
                                  HASS_DISCOVERY]
  --hass-discovery-prefix TEXT    The Home Assistant discovery
                                  prefix to use.  [env var: ECOWIT
                                  T2MQTT_HASS_DISCOVERY_PREFIX,
                                  HASS_DISCOVERY_PREFIX; default:
                                  homeassistant]
  --hass-entity-id-prefix TEXT    The prefix to use for Home
                                  Assistant entity IDs.  [env var:
                                  ECOWITT2MQTT_HASS_ENTITY_ID_PREF
                                  IX, HASS_ENTITY_ID_PREFIX]
  --input-unit-system TEXT        The input unit system used by
                                  the device.  [env var:
                                  ECOWITT2MQTT_INPUT_UNIT_SYSTEM,
                                  INPUT_UNIT_SYSTEM; default:
                                  imperial]
  -b, --mqtt-broker TEXT          The hostname or IP address of an
                                  MQTT broker.  [env var:
                                  ECOWITT2MQTT_MQTT_BROKER,
                                  MQTT_BROKER]
  -p, --mqtt-password TEXT        A valid password for the MQTT
                                  broker.  [env var:
                                  ECOWITT2MQTT_MQTT_PASSWORD,
                                  MQTT_PASSWORD]
  --mqtt-port INTEGER             The listenting port of the MQTT
                                  broker.  [env var:
                                  ECOWITT2MQTT_MQTT_PORT,
                                  MQTT_PORT; default: 1883]
  -u, --mqtt-username TEXT        A valid username for the MQTT
                                  broker.  [env var:
                                  ECOWITT2MQTT_MQTT_USERNAME,
                                  MQTT_USERNAME]
  -t, --mqtt-topic TEXT           The MQTT topic to publish device
                                  data to.  [env var:
                                  ECOWITT2MQTT_MQTT_TOPIC,
                                  MQTT_TOPIC]
  --output-unit-system TEXT       The unit system to use in
                                  output.  [env var:
                                  ECOWITT2MQTT_OUTPUT_UNIT_SYSTEM,
                                  OUTPUT_UNIT_SYSTEM; default:
                                  imperial]
  --port INTEGER                  The port to serve ecowitt2mqtt
                                  on.  [env var:
                                  ECOWITT2MQTT_PORT, PORT;
                                  default: 8080]
  --raw-data                      Return raw data (don't attempt
                                  to translate any values).  [env
                                  var: ECOWITT2MQTT_RAW_DATA,
                                  RAW_DATA]
  -v, --verbose                   Increase verbosity of logged
                                  output.  [env var:
                                  ECOWITT2MQTT_VERBOSE]
  --install-completion            Install completion for the
                                  current shell.
  --show-completion               Show completion for the current
                                  shell, to copy it or customize
                                  the installation.
  --help                          Show this message and exit.
```

## Environment Variables

* `ECOWITT2MQTT_BATTERY_OVERRIDE`: a semicolon-delimited list of key=value battery overrides
* `ECOWITT2MQTT_CONFIG`: a path to a YAML or JSON config file
* `ECOWITT2MQTT_DEFAULT_BATTERY_STRATEGY`: The default battery config strategy to use (default: `boolean`)
* `ECOWITT2MQTT_ENDPOINT`: the relative endpoint/path to serve ecowitt2mqtt on (default: `/data/report`)
* `ECOWITT2MQTT_HASS_DISCOVERY`: publish data in the Home Assistant MQTT Discovery format Idefault: `false`)
* `ECOWITT2MQTT_HASS_DISCOVERY_PREFIX`: the Home Assistant discovery prefix to use (default: `homeassistant`)
* `ECOWITT2MQTT_HASS_ENTITY_ID_PREFIX`: the prefix to use for Home Assistant entity IDs
* `ECOWITT2MQTT_INPUT_UNIT_SYSTEM`: the input unit system used by the device (default: `imperial`)
* `ECOWITT2MQTT_MQTT_BROKER`: the hostname or IP address of an MQTT broker
* `ECOWITT2MQTT_MQTT_PASSWORD`: a valid password for the MQTT broker
* `ECOWITT2MQTT_MQTT_PORT`: the listenting port of the MQTT broker (default: `1883`)
* `ECOWITT2MQTT_MQTT_TOPIC`: the MQTT topic to publish device data to
* `ECOWITT2MQTT_MQTT_USERNAME`: a valid username for the MQTT broker
* `ECOWITT2MQTT_OUTPUT_UNIT_SYSTEM`: the unit system to use in output (default: `imperial`)
* `ECOWITT2MQTT_PORT`: the port to serve ecowitt2mqtt on (default: `8080`)
* `ECOWITT2MQTT_RAW_DATA`: return raw data (don't attempt to translate any values)
* `ECOWITT2MQTT_VERBOSE`: increase verbosity of logged output

## Configuration File

The configuration file can be formatted as either JSON:

```json
{
  "battery_override": {
    "battery_key1": "boolean"
  },
  "default_battery_strategy": "numeric",
  "endpoint": "/data/report",
  "hass_discovery": false,
  "hass_discovery_prefix": "homeassistant",
  "hass_entity_id_prefix": "test_prefix"
  "input_unit_system": "imperial",
  "mqtt_broker": "127.0.0.1",
  "mqtt_password": "password",
  "mqtt_port": 1883,
  "mqtt_topic": "Test",
  "mqtt_username": "user",
  "output_unit_system": "imperial",
  "port": 8080,
  "raw_data": false,
  "verbose": false
}
```

...or YAML


```yaml
---
battery_override:
  battery_key1: boolean
default_battery_strategy: numeric,
endpoint: /data/report,
hass_discovery: false,
hass_discovery_prefix: homeassistant,
hass_entity_id_prefix: test_prefix
input_unit_system: imperial,
mqtt_broker: 127.0.0.1,
mqtt_password: password,
mqtt_port: 1883,
mqtt_topic: Test,
mqtt_username: user,
output_unit_system: imperial,
port: 8080,
raw_data: false,
verbose: false
```

## Merging Configuration Options

When parsing configuration options, `ecowitt2mqtt` looks at the configuration sources in
the following order:

1. Configuration File
2. Environment Variables
3. CLI Options

This allows you to mix and match sources – for instance, you might have "defaults" in
the configuration file and override them via environment variables.

# Advanced Usage

## Unit Systems

`ecowitt2mqtt` allows you to specify both the input and output unit systems for a device.
This is fairly self-explanatory, but take care to use an `--input-unit-system` that is
consistent with what your device provides (otherwise, your data will be very "off").

## Raw Data

In some cases, it may be preferable to prevent `ecowitt2mqtt` from doing any data
translation (converting values to a new unit system, changing binary values – such as
might be used by a battery – into "friendly" values, etc.). Passing the `--raw-data` flag
will accomplish this: data will flow directly from the Ecowitt device to the MQTT broker
as-is.

Note that the `--raw-data` flag supersedes any that might cause data translation (such as
`--input-unit-system` or `--output-unit-system`).

## Home Assistant

### MQTT Discovery

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

### Custom Entity ID Prefix

You can provide a custom prefix for all Home Assistant entities via the
`--hass-entity-id-prefix` config parameter.

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
