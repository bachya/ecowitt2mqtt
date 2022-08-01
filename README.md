![ecowitt2mqtt](resources/logo-full.png)

[![CI](https://github.com/bachya/ecowitt2mqtt/workflows/CI/badge.svg)](https://github.com/bachya/ecowitt2mqtt/actions)
[![PyPi](https://img.shields.io/pypi/v/ecowitt2mqtt.svg)](https://pypi.python.org/pypi/ecowitt2mqtt)
[![Docker Hub](https://img.shields.io/docker/pulls/bachya/ecowitt2mqtt)](https://hub.docker.com/r/bachya/ecowitt2mqtt)
[![Version](https://img.shields.io/pypi/pyversions/ecowitt2mqtt.svg)](https://pypi.python.org/pypi/ecowitt2mqtt)
[![License](https://img.shields.io/pypi/l/ecowitt2mqtt.svg)](https://github.com/bachya/ecowitt2mqtt/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/ecowitt2mqtt/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/ecowitt2mqtt)
[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/ecowitt2mqtt/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`ecowitt2mqtt` is a small CLI/web server that allows [Ecowitt](http://www.ecowitt.com)
device data to be sent to an MQTT broker.

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Disclaimer](#disclaimer)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
  * [Command Line Options](#command-line-options)
  * [Environment Variables](#environment-variables)
  * [Configuration File](#configuration-file)
  * [Merging Configuration Options](#merging-configuration-options)
- [Advanced Usage](#advanced-usage)
  * [Calculated Sensors](#calculated-sensors)
  * [Battery Configurations](#battery-configurations)
  * [Unit Systems](#unit-systems)
  * [Raw Data](#raw-data)
  * [Home Assistant](#home-assistant)
  * [Running in the Background](#running-in-the-background)
  * [Docker](#docker)
- [Diagnostics](#diagnostics)
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

# Disclaimer

The datapoints within this library and documentation constitute estimates and are
intended to help informed decision making. They should not replace analysis, advice, or
diagnosis from trained professionals. Use this data at your own discretion.

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
  --battery-override TEXT         A battery configuration override (format:
                                  key,value)  [env var:
                                  ECOWITT2MQTT_BATTERY_OVERRIDE]
  -c, --config FILE               A path to a YAML or JSON config file.  [env
                                  var: ECOWITT2MQTT_CONFIG]
  --default-battery-strategy TEXT
                                  The default battery config strategy to use.
                                  [env var:
                                  ECOWITT2MQTT_DEFAULT_BATTERY_STRATEGY;
                                  default: boolean]
  --diagnostics                   Output diagnostics.  [env var:
                                  ECOWITT2MQTT_DIAGNOSTICS]
  --disable-calculated-data       Disable the output of calculated sensors.
                                  [env var:
                                  ECOWITT2MQTT_DISABLE_CALCULATED_DATA]
  -e, --endpoint TEXT             The relative endpoint/path to serve
                                  ecowitt2mqtt on.  [env var:
                                  ECOWITT2MQTT_ENDPOINT, ENDPOINT; default:
                                  /data/report]
  --hass-discovery                Publish data in the Home Assistant MQTT
                                  Discovery format.  [env var:
                                  ECOWITT2MQTT_HASS_DISCOVERY, HASS_DISCOVERY]
  --hass-discovery-prefix TEXT    The Home Assistant discovery prefix to use.
                                  [env var:
                                  ECOWITT2MQTT_HASS_DISCOVERY_PREFIX,
                                  HASS_DISCOVERY_PREFIX; default:
                                  homeassistant]
  --hass-entity-id-prefix TEXT    The prefix to use for Home Assistant entity
                                  IDs.  [env var:
                                  ECOWITT2MQTT_HASS_ENTITY_ID_PREFIX,
                                  HASS_ENTITY_ID_PREFIX]
  --input-unit-system TEXT        The input unit system used by the device.
                                  [env var: ECOWITT2MQTT_INPUT_UNIT_SYSTEM,
                                  INPUT_UNIT_SYSTEM; default: imperial]
  -b, --mqtt-broker TEXT          The hostname or IP address of an MQTT
                                  broker.  [env var: ECOWITT2MQTT_MQTT_BROKER,
                                  MQTT_BROKER]
  -p, --mqtt-password TEXT        A valid password for the MQTT broker.  [env
                                  var: ECOWITT2MQTT_MQTT_PASSWORD,
                                  MQTT_PASSWORD]
  --mqtt-port INTEGER             The listenting port of the MQTT broker.
                                  [env var: ECOWITT2MQTT_MQTT_PORT, MQTT_PORT;
                                  default: 1883]
  --mqtt-retain                   Instruct the MQTT broker to retain messages.
                                  [env var: ECOWITT2MQTT_MQTT_RETAIN]
  --mqtt-tls                      Enable MQTT over TLS.  [env var:
                                  ECOWITT2MQTT_MQTT_TLS]
  -t, --mqtt-topic TEXT           The MQTT topic to publish device data to.
                                  [env var: ECOWITT2MQTT_MQTT_TOPIC,
                                  MQTT_TOPIC]
  -u, --mqtt-username TEXT        A valid username for the MQTT broker.  [env
                                  var: ECOWITT2MQTT_MQTT_USERNAME,
                                  MQTT_USERNAME]
  --output-unit-system TEXT       The unit system to use in output.  [env var:
                                  ECOWITT2MQTT_OUTPUT_UNIT_SYSTEM,
                                  OUTPUT_UNIT_SYSTEM; default: imperial]
  --port INTEGER                  The port to serve ecowitt2mqtt on.  [env
                                  var: ECOWITT2MQTT_PORT, PORT; default: 8080]
  --raw-data                      Return raw data (don't attempt to translate
                                  any values).  [env var:
                                  ECOWITT2MQTT_RAW_DATA, RAW_DATA]
  -v, --verbose                   Increase verbosity of logged output.  [env
                                  var: ECOWITT2MQTT_VERBOSE]
  --version                       Return the application version.
  --install-completion            Install completion for the current shell.
  --show-completion               Show completion for the current shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```

## Environment Variables

* `ECOWITT2MQTT_BATTERY_OVERRIDE`: a semicolon-delimited list of key=value battery overrides (default: `numeric`)
* `ECOWITT2MQTT_CONFIG`: a path to a YAML or JSON config file (default: `None`)
* `ECOWITT2MQTT_DEFAULT_BATTERY_STRATEGY`: the default battery config strategy to use (default: `boolean`)
* `ECOWITT2MQTT_DIAGNOSTICS`: whether to output diagnostics (default: `false`)
* `ECOWITT2MQTT_DISABLE_CALCULATE_DATA`: whether to disable the output of calculated sensors (default: `false`)
* `ECOWITT2MQTT_ENDPOINT`: the relative endpoint/path to serve ecowitt2mqtt on (default: `/data/report`)
* `ECOWITT2MQTT_HASS_DISCOVERY_PREFIX`: the Home Assistant discovery prefix to use (default: `homeassistant`)
* `ECOWITT2MQTT_HASS_DISCOVERY`: publish data in the Home Assistant MQTT Discovery format Idefault: `false`)
* `ECOWITT2MQTT_HASS_ENTITY_ID_PREFIX`: the prefix to use for Home Assistant entity IDs (default: `""`)
* `ECOWITT2MQTT_INPUT_UNIT_SYSTEM`: the input unit system used by the device (default: `imperial`)
* `ECOWITT2MQTT_MQTT_BROKER`: the hostname or IP address of an MQTT broker
* `ECOWITT2MQTT_MQTT_PASSWORD`: a valid password for the MQTT broker
* `ECOWITT2MQTT_MQTT_PORT`: the listenting port of the MQTT broker (default: `1883`)
* `ECOWITT2MQTT_MQTT_RETAIN`: whether to instruct the MQTT broker to retain messages (default: `false`)
* `ECOWITT2MQTT_MQTT_TLS`: publish data via MQTT over TLS (default: `false`)
* `ECOWITT2MQTT_MQTT_TOPIC`: the MQTT topic to publish device data to
* `ECOWITT2MQTT_MQTT_USERNAME`: a valid username for the MQTT broker
* `ECOWITT2MQTT_OUTPUT_UNIT_SYSTEM`: the unit system to use in output (default: `imperial`)
* `ECOWITT2MQTT_PORT`: the port to serve ecowitt2mqtt on (default: `8080`)
* `ECOWITT2MQTT_RAW_DATA`: return raw data (don't attempt to translate any values) (default: `false`)
* `ECOWITT2MQTT_VERBOSE`: increase verbosity of logged output (default: `false`)

## Configuration File

The configuration file can be formatted as either YAML:

```yaml
---
battery_override:
  battery_key1: boolean
default_battery_strategy: numeric
diagnostics: false
disable_calculated_data: false
endpoint: /data/report
hass_discovery: false
hass_discovery_prefix: homeassistant
hass_entity_id_prefix: test_prefix
input_unit_system: imperial
mqtt_broker: 127.0.0.1
mqtt_password: password
mqtt_port: 1883
mqtt_retain: false
mqtt_tls: false
mqtt_topic: Test
mqtt_username: user
output_unit_system: imperial
port: 8080
raw_data: false
verbose: false
```

...or JSON


```json
{
  "battery_override": {
    "battery_key1": "boolean"
  },
  "default_battery_strategy": "numeric",
  "diagnostics": false,
  "disable_calculated_data": false,
  "endpoint": "/data/report",
  "hass_discovery": false,
  "hass_discovery_prefix": "homeassistant",
  "hass_entity_id_prefix": "test_prefix"
  "input_unit_system": "imperial",
  "mqtt_broker": "127.0.0.1",
  "mqtt_password": "password",
  "mqtt_port": 1883,
  "mqtt_retain": 1883,
  "mqtt_tls": false,
  "mqtt_topic": "Test",
  "mqtt_username": "user",
  "output_unit_system": "imperial",
  "port": 8080,
  "raw_data": false,
  "verbose": false
}
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

## Calculated Sensors

In addition to the data coming from a gateway, `ecowitt2mqtt` will automatically deduce
and published several additional, calculated data points if the requisite underlying
data exists:

* **[Absolute Humidity](https://en.wikipedia.org/wiki/Humidity#Absolute_humidity):** the actual volume of water vapor in the air
* **[Beaufort Scale](https://en.wikipedia.org/wiki/Beaufort_scale):** the empirical measure that relates wind speed to observed conditions at sea or on land
* **[Dew Point](https://en.wikipedia.org/wiki/Dew_point):** the temperature to which air must be cooled to become saturated with water vapor, assuming constant air pressure and water content
* **[Feels Like](https://en.wikipedia.org/wiki/Heat_index):** how hot or how cold the air feels to the human body when factoring in variables such as relative humidity, wind speeds, the amount of sunshine, etc.
* **[Frost Point](https://en.wikipedia.org/wiki/Dew_point#Frost_point):** the temperature below 32°F (0°C) at which moisture in the air will condense as a layer of frost on exposed surfaces that are also at a temperature below the frost point
* **[Frost Risk](https://en.wikipedia.org/wiki/Dew_point#Frost_point):** how likely the formation of frost is (based on the `frostpoint`)
* **[Heat Index](https://en.wikipedia.org/wiki/Heat_index):** how hot the air feels to the human body when factoring in relative humidity (applicable when the apparent temperature is higher than the air temperature)
* **[Safe Exposure Times](https://www.openuv.io/kb/skin-types-safe-exposure-time-calculation/):** how long different skin types can be in the sun (unprotected) before burning begins according to the [Fitzpatrick Scale](https://en.wikipedia.org/wiki/Fitzpatrick_scale)
* **Solar Radiation (lux):** the detected solar radiation illuminance calculated in lux
* **Solar Radiation (%):** the percentage of detected solar radiation illuminance as perceived by the human eye
* **[Simmer Index](http://summersimmer.com/ssi_page2.htm):** an alternative to heat index that describes how how the air feels to the human body in relatively dry environments
* **Simmer Zone:** a human-friendly interpretation of the Simmer Index
* **Thermal Perception:** a human-friendly interpretation of the Dew Point
* **[Wind Chill](https://en.wikipedia.org/wiki/Wind_chill):** how cold the air feels to the human body when factoring in relative humidity, wind speed, etc. (applicable when the apparent temperature is lower than the air temperature)

If you would prefer to not have these sensors calculated and published, you can utilize
the `--disable-calculated-data` configuration option.

## Battery Configurations

Ecowitt devices report battery levels in three different formats:

* `boolean`: `0` represents `OFF` (i.e., the battery is in normal condition) and `1`
   represents `ON` (i.e., the battery is low).
* `numeric`: the raw numeric value is interpreted as the number of volts remaining in
   the battery.
* `percentage`: the raw numeric value is interpreted as the percentage of voltage
   remaining the battery.

`ecowitt2mqtt` provides three mechanisms to handle this complexity:

1. A built-in mapping of all currently known battery types to their assumed strategy
2. A default battery strategy for unknown battery types
3. User-defined battery strategy overrides

### Built-in Mapping

`ecowitt2mqtt` contains an internal mapping that should automatically transform all
known battery types into their correct format.

### Default Battery Strategy

By using the `--default-battery-strategy` configuration parameter, users can specify how
unknown battery types should be treated by default.

### Battery Overrides

Individual batteries can be overridden and given a new strategy. How this is
accomplished differs slightly based on the configuration method used:

* Command Line Options: provide one or more `--battery-override "batt1=boolean"` options
* Environment Variables: provide a `ECOWITT2MQTT_BATTERY_OVERRIDE` variable that is a
  semicolon-delimited pair of "key=value" strings (e.g.,
  `ECOWITT2MQTT_BATTERY_OVERRIDE="batt1=boolean;batt2=numeric"`)
* Config File: include a dictionary of key/value pairs in either YAML or JSON format

These overrides work on both known and unknown battery types; that said, if you should
find the need to override a known battery type because `ecowitt2mqtt` has an incorrect
internal interpretation, submit an issue to get it corrected!

### Example

In this example, a user mostly has batteries that should be treated as `boolean`, but
also has one – `wh60_batt1` – that should be treated as numeric.

#### Command Line Options

```
$ ecowitt2mqtt --default-battery-strategy boolean --battery-override="wh60_batt1=numeric"
```

#### Environment Variables

```
$ ECOWITT2MQTT_DEFAULT_BATTERY_STRATEGY=boolean \
  ECOWITT2MQTT_BATTERY_OVERRIDE="wh60_batt1=numeric" \
  ecowitt2mqtt
```

#### Config File

In YAML:

```yaml
---
default_battery_strategy: boolean
battery_override:
  wh60_batt1: numeric
```

...or JSON

```json
{
  "default_battery_strategy": "boolean",
  "battery_override": {
    "wh60_batt1": "numeric"
  }
}
```

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

### Home Assistant OS Add-on

Home Assistant OS users can install the official `ecowitt2mqtt` add-on by clicking the
link below:

[![Open this add-on in your Home Assistant instance.][addon-badge]][addon]

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
Type=simple
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
by using the same environment variables listed [above](#environment-variables).

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

# Diagnostics

You may run `ecowitt2mqtt` in diagnostics mode by providing the `--diagnostics` flag. In
this mode, the app will wait until it receives and publishes a single payload, then
exit. This allows users to collect a small-but-complete payload for use in testing,
debugging, and issue reporting.

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/ecowitt2mqtt/issues)
  or [initiate a discussion on one](https://github.com/bachya/ecowitt2mqtt/issues/new).
2. [Fork the repository](https://github.com/bachya/ecowitt2mqtt/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `nox -rs coverage`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!

[addon-badge]: https://my.home-assistant.io/badges/supervisor_addon.svg
[addon]: https://my.home-assistant.io/redirect/supervisor_addon/?addon=c35f0383_ecowitt2mqtt&repository_url=https%3A%2F%2Fgithub.com%2Fbachya%2Fhome-assistant-addons
