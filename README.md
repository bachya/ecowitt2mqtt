![ecowitt2mqtt](resources/logo-full.png)

[![CI](https://github.com/bachya/ecowitt2mqtt/workflows/CI/badge.svg)](https://github.com/bachya/ecowitt2mqtt/actions)
[![PyPi](https://img.shields.io/pypi/v/ecowitt2mqtt.svg)](https://pypi.python.org/pypi/ecowitt2mqtt)
[![Docker Hub](https://img.shields.io/docker/pulls/bachya/ecowitt2mqtt)](https://hub.docker.com/r/bachya/ecowitt2mqtt)
[![Version](https://img.shields.io/pypi/pyversions/ecowitt2mqtt.svg)](https://pypi.python.org/pypi/ecowitt2mqtt)
[![License](https://img.shields.io/pypi/l/ecowitt2mqtt.svg)](https://github.com/bachya/ecowitt2mqtt/blob/main/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/ecowitt2mqtt/branch/dev/graph/badge.svg)](https://codecov.io/gh/bachya/ecowitt2mqtt)
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
  - [Command Line Options](#command-line-options)
  - [Environment Variables](#environment-variables)
  - [Configuration File](#configuration-file)
  - [Merging Configuration Options](#merging-configuration-options)
- [Advanced Usage](#advanced-usage)
  - [Calculated Sensors](#calculated-sensors)
  - [Battery Configurations](#battery-configurations)
  - [Unit Systems](#unit-systems)
  - [Raw Data](#raw-data)
  - [Home Assistant](#home-assistant)
  - [Running in the Background](#running-in-the-background)
  - [Docker](#docker)
- [Diagnostics](#diagnostics)
- [Contributing](#contributing)

# Installation

```bash
pip install ecowitt2mqtt
```

# Python Versions

`ecowitt2mqtt` is currently supported on:

- Python 3.9
- Python 3.10
- Python 3.11

# Disclaimer

The datapoints within this library and documentation constitute estimates and are
intended to help informed decision making. They should not replace analysis, advice, or
diagnosis from trained professionals. Use this data at your own discretion.

# Quick Start

Note that this README assumes that:

- you have access to an MQTT broker.
- you have already paired your Ecowitt device with the WS View Android/iOS app from
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

- `Protocol Type Same As`: `Ecowitt`
- `Server IP / Hostname`: the IP address/hostname of the device running `ecowitt2mqtt`
- `Path`: `/data/report/`
- `Port`: `8080` (the default port on which `ecowitt2mqtt` is served)
- `Upload Interval`: `60` (change this to alter the frequency with which data is published)

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
usage: ecowitt2mqtt [-h] [--version] [--battery-override BATTERY_OVERRIDE] [-c config] [--default-battery-strategy default_battery_strategy]
                    [--diagnostics] [--disable-calculated-data] [-e endpoint] [--hass-discovery]
                    [--hass-discovery-prefix hass_discovery_prefix] [--hass-entity-id-prefix hass_entity_id_prefix]
                    [--input-unit-system input_unit_system] [-b mqtt_broker] [-p mqtt_password] [--mqtt-port mqtt_port] [--mqtt-retain]
                    [--mqtt-tls] [-t mqtt_topic] [-u mqtt_username] [--output-unit-system output_unit_system]
                    [--output-unit-accumulated-precipitation output_unit_accumulated_precipitation]
                    [--output-unit-distance output_unit_distance] [--output-unit-humidity output_unit_humidity]
                    [--output-unit-illuminance output_unit_illuminance] [--output-unit-precipitation-rate output_unit_precipitation_rate]
                    [--output-unit-pressure output_unit_pressure] [--output-unit-speed output_unit_speed]
                    [--output-unit-temperature output_unit_temperature] [--port port] [--precision precision] [--raw-data] [-v]

Send data from an Ecowitt gateway to an MQTT broker

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --battery-override BATTERY_OVERRIDE
                        A battery configuration override (format: key,value)
  -c config, --config config
                        A path to a YAML or JSON config file
  --default-battery-strategy default_battery_strategy
                        The default battery config strategy to use (default: boolean)
  --diagnostics         Output diagnostics
  --disable-calculated-data
                        Disable the output of calculated sensors
  -e endpoint, --endpoint endpoint
                        The relative endpoint/path to serve ecowitt2mqtt on (default: /data/report)
  --hass-discovery      Publish data in the Home Assistant MQTT Discovery format
  --hass-discovery-prefix hass_discovery_prefix
                        The Home Assistant MQTT Discovery topic prefix to use (default: homeassistant)
  --hass-entity-id-prefix hass_entity_id_prefix
                        The prefix to use for Home Assistant entity IDs
  --input-unit-system input_unit_system
                        The input unit system used by the gateway (default: imperial)
  -b mqtt_broker, --mqtt-broker mqtt_broker
                        The hostname or IP address of an MQTT broker
  -p mqtt_password, --mqtt-password mqtt_password
                        A valid password for the MQTT broker
  --mqtt-port mqtt_port
                        The listenting port of the MQTT broker (default: 1883)
  --mqtt-retain         Instruct the MQTT broker to retain messages
  --mqtt-tls            Enable MQTT over TLS
  -t mqtt_topic, --mqtt-topic mqtt_topic
                        The MQTT topic to publish device data to
  -u mqtt_username, --mqtt-username mqtt_username
                        A valid username for the MQTT broker
  --output-unit-system output_unit_system
                        The output unit system used by the gateway (default: imperial)
  --output-unit-accumulated-precipitation output_unit_accumulated_precipitation
                        The output unit to use for accumulated precipitation data points (default: the default used by the output unit
                        system)
  --output-unit-distance output_unit_distance
                        The output unit to use for distance data points (default: the default used by the output unit system)
  --output-unit-humidity output_unit_humidity
                        The output unit to use for humidity data points (default: the default used by the output unit system)
  --output-unit-illuminance output_unit_illuminance
                        The output unit to use for illuminance data points (default: the default used by the output unit system)
  --output-unit-precipitation-rate output_unit_precipitation_rate
                        The output unit to use for precipitation rate data points (default: the default used by the output unit system)
  --output-unit-pressure output_unit_pressure
                        The output unit to use for pressure data points (default: the default used by the output unit system)
  --output-unit-speed output_unit_speed
                        The output unit to use for speed data points (default: the default used by the output unit system)
  --output-unit-temperature output_unit_temperature
                        The output unit to use for temperature data points (default: the default used by the output unit system)
  --port port           The port to serve ecowitt2mqtt on (default: 8080)
  --precision precision
                        The precision to output data points at (default: no limit)
  --raw-data            Return raw data (don't attempt to translate any values)
  -v, --verbose         Increase verbosity of logged output
```

## Environment Variables

- `ECOWITT2MQTT_BATTERY_OVERRIDE`: a semicolon-delimited list of key=value battery overrides (default: `numeric`)
- `ECOWITT2MQTT_CONFIG`: a path to a YAML or JSON config file (default: `None`)
- `ECOWITT2MQTT_DEFAULT_BATTERY_STRATEGY`: the default battery config strategy to use (default: `boolean`)
- `ECOWITT2MQTT_DIAGNOSTICS`: whether to output diagnostics (default: `false`)
- `ECOWITT2MQTT_DISABLE_CALCULATED_DATA`: whether to disable the output of calculated sensors (default: `false`)
- `ECOWITT2MQTT_ENDPOINT`: the relative endpoint/path to serve ecowitt2mqtt on (default: `/data/report`)
- `ECOWITT2MQTT_HASS_DISCOVERY_PREFIX`: the Home Assistant discovery prefix to use (default: `homeassistant`)
- `ECOWITT2MQTT_HASS_DISCOVERY`: publish data in the Home Assistant MQTT Discovery format Idefault: `false`)
- `ECOWITT2MQTT_HASS_ENTITY_ID_PREFIX`: the prefix to use for Home Assistant entity IDs (default: `""`)
- `ECOWITT2MQTT_INPUT_UNIT_SYSTEM`: the input unit system used by the device (default: `imperial`)
- `ECOWITT2MQTT_MQTT_BROKER`: the hostname or IP address of an MQTT broker
- `ECOWITT2MQTT_MQTT_PASSWORD`: a valid password for the MQTT broker
- `ECOWITT2MQTT_MQTT_PORT`: the listenting port of the MQTT broker (default: `1883`)
- `ECOWITT2MQTT_MQTT_RETAIN`: whether to instruct the MQTT broker to retain messages (default: `false`)
- `ECOWITT2MQTT_MQTT_TLS`: publish data via MQTT over TLS (default: `false`)
- `ECOWITT2MQTT_MQTT_TOPIC`: the MQTT topic to publish device data to
- `ECOWITT2MQTT_MQTT_USERNAME`: a valid username for the MQTT broker
- `ECOWITT2MQTT_OUTPUT_UNIT_SYSTEM`: the unit system to use in output (default: `imperial`)
- `ECOWITT2MQTT_OUTPUT_UNIT_TEMPERATURE`: the output unit to use for temperature data points (default: the default used by the output unit system)
- `ECOWITT2MQTT_PORT`: the port to serve ecowitt2mqtt on (default: `8080`)
- `ECOWITT2MQTT_PRECISION`: the precision to output data points at (default: no limit)
- `ECOWITT2MQTT_RAW_DATA`: return raw data (don't attempt to translate any values) (default: `false`)
- `ECOWITT2MQTT_VERBOSE`: increase verbosity of logged output (default: `false`)

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
  "mqtt_retain": true,
  "mqtt_tls": false,
  "mqtt_topic": "Test",
  "mqtt_username": "user",
  "output_unit_system": "imperial",
  "port": 8080,
  "raw_data": false,
  "verbose": false
}
```

...and makes use of the same config options available to the CLI.

### Multiple Gateways

When using the configuration file, it is possible to define specific configuration
parameters for multiple Ecowitt gateways. This is useful if different gateways should
publish to different MQTT brokers, in different formats, etc.

First, you must determine the unique ID for each gateway. This can be observed in the
logs when `verbose` is enabled – look for the `PASSKEY` value that the gateway has:

```
Received data from the Ecowitt device: {'PASSKEY': 'abcde12345', ...}
```

Then, in the configuration file, simply add a `gateways` key that contains a mapping of any
of the existing configuration options. Options that remain at the root level of the file
are treated as defaults.

For example, this YAML configuration file:

```yaml
---
mqtt_broker: 127.0.0.1
mqtt_password: password
mqtt_topic: Test
mqtt_username: user

gateways:
  abcde12345:
    hass_discovery: true
```

...defines two gateway definitions:

- One that publishes to the `Test` topic on an MQTT broker at `127.0.0.1`
- One (with a `PASSKEY` of `abcde12345`) that publishes to the same broker, but in Home
  Assistant MQTT Discovery format.

In another example, this JSON configuration file:

```json
{
  "mqtt_broker": "127.0.0.1",
  "mqtt_password": "password",
  "mqtt_port": 1883,
  "mqtt_topic": "Test",
  "mqtt_username": "user",
  "gateways": {
    "abcde12345": {
      "mqtt_broker": "192.168.1.100",
      "mqtt_retain": true,
      "output_unit_system": "metric"
    }
  }
}
```

...defines two gateway definitions:

- One that publishes to the `Test` topic on an MQTT broker at `127.0.0.1`
- One (with a `PASSKEY` of `abcde12345`) that publishes to a different broker
  (`192.168.1.100`), outputs the data in metric, and retains the data on the broker

## Merging Configuration Options

When parsing configuration options, `ecowitt2mqtt` looks at the configuration sources in
the following order:

1. Configuration File (Specific Gateway)
2. Configuration File (Defaults)
3. Environment Variables
4. CLI Options

This allows you to mix and match sources – for instance, you might have "defaults" in
the configuration file and override them via environment variables.

# Advanced Usage

## Calculated Sensors

In addition to the data coming from a gateway, `ecowitt2mqtt` will automatically deduce
and published several additional, calculated data points if the requisite underlying
data exists:

- **[Absolute Humidity](https://en.wikipedia.org/wiki/Humidity#Absolute_humidity):** the actual volume of water vapor in the air
- **[Beaufort Scale](https://en.wikipedia.org/wiki/Beaufort_scale):** the empirical measure that relates wind speed to observed conditions at sea or on land
- **[Dew Point](https://en.wikipedia.org/wiki/Dew_point):** the temperature to which air must be cooled to become saturated with water vapor, assuming constant air pressure and water content
- **[Feels Like](https://en.wikipedia.org/wiki/Heat_index):** how hot or how cold the air feels to the human body when factoring in variables such as relative humidity, wind speeds, the amount of sunshine, etc.
- **[Frost Point](https://en.wikipedia.org/wiki/Dew_point#Frost_point):** the temperature below 32°F (0°C) at which moisture in the air will condense as a layer of frost on exposed surfaces that are also at a temperature below the frost point
- **[Frost Risk](https://en.wikipedia.org/wiki/Dew_point#Frost_point):** how likely the formation of frost is (based on the `frostpoint`)
- **[Heat Index](https://en.wikipedia.org/wiki/Heat_index):** how hot the air feels to the human body when factoring in relative humidity (applicable when the apparent temperature is higher than the air temperature)
- **[Safe Exposure Times](https://www.openuv.io/kb/skin-types-safe-exposure-time-calculation/):** how long different skin types can be in the sun (unprotected) before burning begins according to the [Fitzpatrick Scale](https://en.wikipedia.org/wiki/Fitzpatrick_scale)
- **Solar Radiation (%):** the percentage of detected solar radiation illuminance as perceived by the human eye
- **[Simmer Index](http://summersimmer.com/ssi_page2.htm):** an alternative to heat index that describes how how the air feels to the human body in relatively dry environments
- **Simmer Zone:** a human-friendly interpretation of the Simmer Index
- **Thermal Perception:** a human-friendly interpretation of the Dew Point
- **[Wind Chill](https://en.wikipedia.org/wiki/Wind_chill):** how cold the air feels to the human body when factoring in relative humidity, wind speed, etc. (applicable when the apparent temperature is lower than the air temperature)

If you would prefer to not have these sensors calculated and published, you can utilize
the `--disable-calculated-data` configuration option.

## Battery Configurations

Ecowitt devices report battery levels in three different formats:

- `boolean`: `0` represents `OFF` (i.e., the battery is in normal condition) and `1`
  represents `ON` (i.e., the battery is low).
- `numeric`: the raw numeric value is interpreted as the number of volts remaining in
  the battery.
- `percentage`: the raw numeric value is interpreted as the percentage of voltage
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

- Command Line Options: provide one or more `--battery-override "batt1=boolean"` options
- Environment Variables: provide a `ECOWITT2MQTT_BATTERY_OVERRIDE` variable that is a
  semicolon-delimited pair of "key=value" strings (e.g.,
  `ECOWITT2MQTT_BATTERY_OVERRIDE="batt1=boolean;batt2=numeric"`)
- Config File: include a dictionary of key/value pairs in either YAML or JSON format

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

### Input and Output

`ecowitt2mqtt` allows you to specify both the input and output unit systems for a device
via the `--input-unit-system` and `--output-unit-system` config options, respectively.
These are fairly self-explanatory, but take care to use an `--input-unit-system` that is
consistent with what your device provides (otherwise, your data will be very "off").

### Overriding Units for Data Categories

If you wish, you can change the unit for individual data categories. For example, let's
say you wanted to use metric for the output unit system, but wanted to represent all
temperature data points in Kelvin – you would provide `--output-unit-system=metric` and
`--output-unit-temperature=K` as config options. As expected, the value is properly
converted to the new unit.

#### Accumulated Precipitation

Config Option: `--output-unit-accumulated-precipitation`

- `in`
- `mm`

#### Absolute Humidity

Config Option: `--output-unit-humidity`

- `g/m³`
- `lbs/ft³`

#### Illuminance

Config Option: `--output-unit-illuminance`

- `fc`
- `kfc`
- `klx`
- `lx`
- `W/m²`

#### Precipitation Rate

Config Option: `--output-unit-precipitation-rate`

- `in/h`
- `mm/h`

#### Pressure

Config Option: `--output-unit-pressure`

- `bar`
- `cbar`
- `hPa`
- `inHg`
- `kPa`
- `mbar`
- `mmHg`
- `Pa`
- `psi`

#### Speed

Config Option: `--output-unit-speed`

- `ft/s`
- `in/d`
- `in/h`
- `km/h`
- `kn`
- `m/s`
- `mph`
- `mm/d`

#### Temperature

Config Option: `--output-unit-temperature`

- `°C`
- `°F`
- `K`

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

The library is available via a Docker image from both
[Docker Hub](https://hub.docker.com/r/bachya/ecowitt2mqtt) and
[ghcr.io](https://ghcr.io/bachya/ecowitt2mqtt). It is configured by using the same
environment variables listed [above](#environment-variables).

Running the image is straightforward:

```
docker run -it \
    -e ECOWITT2MQTT_MQTT_BROKER=192.168.1.101 \
    -e ECOWITT2MQTT_MQTT_USERNAME=user \
    -e ECOWITT2MQTT_MQTT_PASSWORD=password \
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
in production, you should refer to one of the published images.

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
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov ecowitt2mqtt tests`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!

[addon-badge]: https://my.home-assistant.io/badges/supervisor_addon.svg
[addon]: https://my.home-assistant.io/redirect/supervisor_addon/?addon=c35f0383_ecowitt2mqtt&repository_url=https%3A%2F%2Fgithub.com%2Fbachya%2Fhome-assistant-addons
