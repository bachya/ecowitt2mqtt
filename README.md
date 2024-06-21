![ecowitt2mqtt][logo]

[![CI][ci-badge]][ci]
[![PyPI][pypi-badge]][pypi]
[![Docker Hub][docker-hub-badge]][docker-hub]
[![Version][version-badge]][version]
[![License][license-badge]][license]
[![Code Coverage][codecov-badge]][codecov]
[![Maintainability][maintainability-badge]][maintainability]

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`ecowitt2mqtt` is a small CLI/web server that can receive data from Fine Offset weather
stations (and their numerous white-labeled counterparts, like Ecowitt and
Ambient Weather), adjust that data in numerous ways, and send it on to one or more
MQTT brokers.

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Disclaimer](#disclaimer)
- [Supported Brands](#supported-brands)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
  - [Command Line Options](#command-line-options)
  - [Environment Variables](#environment-variables)
  - [Configuration File](#configuration-file)
  - [Merging Configuration Options](#merging-configuration-options)
  - [Input Data Formats](#input-data-formats)
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

- Python 3.10
- Python 3.11
- Python 3.12

# Disclaimer

The datapoints within this library and documentation constitute estimates and are
intended to help informed decision making. They should not replace analysis, advice, or
diagnosis from trained professionals. Use this data at your own discretion.

# Supported Brands

Despite the name of the library, `ecowitt2mqtt` should support any weather station/gateway
that is produced by [Fine Offset](https://www.foshk.com/). This includes brands that
white-label Fine Offset equipment, such as:

- [Ambient Weather][ambient-weather] (U.S.)
- [Ecowitt][ecowitt] (China, Hong Kong)
- [Froggit][froggit] (Germany)

...and many others. For more information on how these brands relate to one another, see
this forum post: https://www.wxforum.net/index.php?topic=40730.0

Although there are some small differences between how these various branded devices are
configured, `ecowitt2mqtt` endeavors to incorporate them all with minimal effort on the
user's part.

# Quick Start

First, install `ecowitt2mqtt` via `pip`:

```bash
$ pip install ecowitt2mqtt
```

Next, if you haven't already, install the appropriate mobile app to configure your
device. For example:

- Ambient Weather: awnet ([iOS][awnet-ios]/[Android][awnet-google-play])
- Ecowitt: WS View ([iOS][ws-view-ios]/[Android][ws-view-google-play])

Find the appropriate location in the mobile app to configure a customized upload target
for the station's data. This will differ depending on the app, but in general, you
should select your device and find a screen entitled "Upload" (or similar).

![The "Upload" screen in the awnet app][awnet-upload-screen]
![The "Upload" screen in the WS View app][ws-view-upload-screen]

Fill out the form with the appropriate values and tap `Save`:

- `Protocol Type Same As`: pick the label that matches your brand (e.g., `Ecowitt` for
  Ecowitt devices)
- `Server IP / Hostname`: the IP address/hostname of the device running `ecowitt2mqtt`
- `Path`: `/data/report/` (the default path used by most mobile apps)
- `Port`: `8080` (the default port on which `ecowitt2mqtt` is served)
- `Upload Interval`: 16 (a reasonable short number of seconds between publishes)

Then, on the machine where you installed `ecowitt2mqtt`, run it:

```bash
$ ecowitt2mqtt \
    --mqtt-broker=192.168.1.101 \
    --mqtt-username=user \
    --mqtt-password=password \
    --mqtt-topic=ecowitt2mqtt/device_1
    --input-data-format=ecowitt
```

Within the `Upload Interval`, data should begin to appear in the MQTT broker.

# Configuration

`ecowitt2mqtt` can be configured via command line options, environment variables, or a
(YAML or JSON) config file.

## Command Line Options

```
usage: ecowitt2mqtt [-h] [--version] [--battery-override BATTERY_OVERRIDES] [--boolean-battery-true-value boolean_battery_true_value] [-c config] [--default-battery-strategy default_battery_strategy] [--diagnostics] [--disable-calculated-data] [-e endpoint] [--hass-discovery]
                    [--hass-discovery-prefix hass_discovery_prefix] [--hass-entity-id-prefix hass_entity_id_prefix] [--input-data-format input_data_format] [--input-unit-system input_unit_system] [-b mqtt_broker] [-p mqtt_password] [--mqtt-port mqtt_port] [--mqtt-retain] [--mqtt-tls] [-t mqtt_topic]
                    [-u mqtt_username] [--output-unit-system output_unit_system] [--output-unit-accumulated-precipitation output_unit_accumulated_precipitation] [--output-unit-distance output_unit_distance] [--output-unit-humidity output_unit_humidity]
                    [--output-unit-illuminance output_unit_illuminance] [--output-unit-precipitation-rate output_unit_precipitation_rate] [--output-unit-pressure output_unit_pressure] [--output-unit-speed output_unit_speed] [--output-unit-temperature output_unit_temperature] [--port port]
                    [--precision precision] [--raw-data] [-v]

Send data from an Ecowitt gateway to an MQTT broker

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --battery-override BATTERY_OVERRIDES
                        A battery configuration override (format: key,value)
  --boolean-battery-true-value boolean_battery_true_value
                        The value that boolean battery sensors use to represent a True value (default: 1)
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
                        The prefix to use for Home Assistant entity IDs. Example: A prefix of 'prefix' will prepend 'prefix_' to entity IDs
  --input-data-format input_data_format
                        The input data format used by the gateway (default: ecowitt)
  --input-unit-system input_unit_system
                        The input unit system used by the gateway (default: imperial)
  --locale locale       The locale to use (default: en_US.UTF-8)
  -b mqtt_broker, --mqtt-broker mqtt_broker
                        The hostname or IP address of an MQTT broker
  -p mqtt_password, --mqtt-password mqtt_password
                        A valid password for the MQTT broker
  --mqtt-port mqtt_port
                        The listening port of the MQTT broker (default: 1883)
  --mqtt-retain         Instruct the MQTT broker to retain messages
  --mqtt-tls            Enable MQTT over TLS
  -t mqtt_topic, --mqtt-topic mqtt_topic
                        The MQTT topic to publish device data to
  -u mqtt_username, --mqtt-username mqtt_username
                        A valid username for the MQTT broker
  --output-unit-system output_unit_system
                        The output unit system used by the gateway (default: imperial)
  --output-unit-accumulated-precipitation output_unit_accumulated_precipitation
                        The output unit to use for accumulated precipitation data points (default: the default used by the output unit system)
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
                        The precision to output data points at. Example: A value of 2 will round to two decimal places. (default: no limit)
  --raw-data            Return raw data (don't attempt to translate any values)
  -v, --verbose         Increase verbosity of logged output
```

## Environment Variables

- `ECOWITT2MQTT_BATTERY_OVERRIDE`: a semicolon-delimited list of key=value battery
  overrides (default: `numeric`)
- `ECOWITT2MQTT_BOOLEAN_BATTERY_TRUE_VALUE`: The value that boolean battery sensors use to
  represent a True value (default: `1`)
- `ECOWITT2MQTT_CONFIG`: a path to a YAML or JSON config file (default: `None`)
- `ECOWITT2MQTT_DEFAULT_BATTERY_STRATEGY`: the default battery config strategy to use
  (default: `boolean`)
- `ECOWITT2MQTT_DIAGNOSTICS`: whether to output diagnostics (default: `false`)
- `ECOWITT2MQTT_DISABLE_CALCULATED_DATA`: whether to disable the output of calculated
  sensors (default: `false`)
- `ECOWITT2MQTT_ENDPOINT`: the relative endpoint/path to serve ecowitt2mqtt on (default:
  `/data/report`)
- `ECOWITT2MQTT_HASS_DISCOVERY_PREFIX`: the Home Assistant discovery prefix to use
  (default: `homeassistant`)
- `ECOWITT2MQTT_HASS_DISCOVERY`: publish data in the Home Assistant MQTT Discovery format
  (default: `false`)
- `ECOWITT2MQTT_HASS_ENTITY_ID_PREFIX`: the prefix to use for Home Assistant entity IDs
  (default: `""`)
- `ECOWITT2MQTT_INPUT_DATA_FORMAT`: the input data format used by the gateway (default:
  `ecowitt`)
- `ECOWITT2MQTT_INPUT_UNIT_SYSTEM`: the input unit system used by the device (default:
  `imperial`)
- `ECOWITT2MQTT_LOCALE`: the locale to use (default: `en_US.UTF-8`)
- `ECOWITT2MQTT_MQTT_BROKER`: the hostname or IP address of an MQTT broker
- `ECOWITT2MQTT_MQTT_PASSWORD`: a valid password for the MQTT broker
- `ECOWITT2MQTT_MQTT_PORT`: the listening port of the MQTT broker (default: `1883`)
- `ECOWITT2MQTT_MQTT_RETAIN`: whether to instruct the MQTT broker to retain messages
  (default: `false`)
- `ECOWITT2MQTT_MQTT_TLS`: publish data via MQTT over TLS (default: `false`)
- `ECOWITT2MQTT_MQTT_TOPIC`: the MQTT topic to publish device data to
- `ECOWITT2MQTT_MQTT_USERNAME`: a valid username for the MQTT broker
- `ECOWITT2MQTT_OUTPUT_UNIT_SYSTEM`: the unit system to use in output (default: `imperial`)
- `ECOWITT2MQTT_OUTPUT_UNIT_TEMPERATURE`: the output unit to use for temperature data
  points (default: the default used by the output unit system)
- `ECOWITT2MQTT_PORT`: the port to serve ecowitt2mqtt on (default: `8080`)
- `ECOWITT2MQTT_PRECISION`: the precision to output data points at (default: no limit)
- `ECOWITT2MQTT_RAW_DATA`: return raw data (don't attempt to translate any values)
  (default: `false`)
- `ECOWITT2MQTT_VERBOSE`: increase verbosity of logged output (default: `false`)

## Configuration File

The configuration file can be formatted as either YAML:

```yaml
---
battery_override:
  battery_key1: boolean
boolean_battery_true_value: 1
default_battery_strategy: numeric
diagnostics: false
disable_calculated_data: false
endpoint: /data/report
hass_discovery: false
hass_discovery_prefix: homeassistant
hass_entity_id_prefix: test_prefix
input_data_format: ecowitt
input_unit_system: imperial
locale: en_US.UTF-8
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
  "boolean_battery_true_value": 1,
  "default_battery_strategy": "numeric",
  "diagnostics": false,
  "disable_calculated_data": false,
  "endpoint": "/data/report",
  "hass_discovery": false,
  "hass_discovery_prefix": "homeassistant",
  "hass_entity_id_prefix": "test_prefix"
  "input_data_format": "ecowitt",
  "input_unit_system": "imperial",
  "locale": "en_US.UTF-8",
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

Then, in the configuration file, simply add a `gateways` key that contains a mapping of
any of the existing configuration options (except for `--verbose` and `--diagnostics`,
which can only be defined once and are applied to _every_ configuration). Options that
remain at the root level of the file are treated as defaults.

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

## Input Data Formats

`ecowitt2mqtt` currently supports the following input data formats:

- `ambient_weather`
- `ecowitt`
- `wunderground` (Weather Underground)

Provide the correct one to `---input-data-format` based on which device brand you use.

# Advanced Usage

## Calculated Sensors

In addition to the data coming from a gateway, `ecowitt2mqtt` will automatically deduce
and published several additional, calculated data points if the requisite underlying
data exists:

- **[Absolute Humidity][absolute-humidity]:** the actual volume of water vapor in the
  air
- **[Beaufort Scale][beaufort-scale]:** the empirical measure that relates wind speed to
  observed conditions at sea or on land
- **[Dew Point][dew-point]:** the temperature to which air must be cooled to become
  saturated with water vapor, assuming constant air pressure and water content
- **[Feels Like][heat-index]:** how hot or how cold the air feels to the human body when
  factoring in variables such as relative humidity, wind speeds, the amount of sunshine,
  etc.
- **[Frost Point][frost-point]:** the temperature below 32°F (0°C) at which moisture in
  the air will condense as a layer of frost on exposed surfaces that are also at a
  temperature below the frost point
- **[Frost Risk][frost-point]:** how likely the formation of frost is (based on the
  `frostpoint`)
- **[Heat Index][heat-index]:** how hot the air feels to the human body when factoring
  in relative humidity (applicable when the apparent temperature is higher than the air
  temperature)
- **[Humidex][humidex]:** an index number used by Canadian meteorologists to describe
  how hot the weather feels to the average person, by combining the effect of heat and
  humidity
- **[Humidex Perception][humidex]:** a human-friendly interpretation of the Humidex
- **Relative Strain Index:** a measure of discomfort resulting from the combined effect
  of temperature and humidity (applicable to heat stress of manual workers under shelter
  at various metabolic rates)
- **Relative Strain Index Perception:** a human-friendly interpretation of the Relative
  Strain Index
- **[Safe Exposure Times][safe-exposure-times]:** how long different skin types can be
  in the sun (unprotected) before burning begins according to the
  [Fitzpatrick Scale][fitzpatrick-scale]
- **Solar Radiation (%):** the percentage of detected solar radiation illuminance as
  perceived by the human eye
- **[Simmer Index][simmer-index]:** an alternative to heat index that describes how how
  the air feels to the human body in relatively dry environments
- **[Simmer Zone][simmer-index]:** a human-friendly interpretation of the Simmer Index
- **[Thermal Perception][dew-point]:** a human-friendly interpretation of the Dew Point
- **[Wind Chill][wind-chill]:** how cold the air feels to the human body when factoring
  in relative humidity, wind speed, etc. (applicable when the apparent temperature is
  lower than the air temperature)
- **Wind Direction Name:** a conversion from degrees to a human-friendly label (e.g.,
  "NNW")

(Special thanks to the excellent [`thermal_comfort` library][thermal-comfort-library] for
inspiration on many of these.)

If you would prefer to not have these sensors calculated and published, you can utilize
the `--disable-calculated-data` configuration option.

## Battery Configurations

Ecowitt devices report battery levels in three different formats:

- `boolean`: `0` represents `OFF` (i.e., the battery is in normal condition) and `1` represents
  `ON` (i.e., the battery is low).
- `numeric`: the raw numeric value is interpreted as the number of volts remaining in the
  battery.
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

[Home Assistant][home-assistant] users can quickly add entities from an Ecowitt device
by using [MQTT Discovery][home-assistant-mqtt-discovery]. Once Home Assistant is
configured to accept MQTT Discovery, `ecowitt2mqtt` simply needs the `--hass-discovery`
flag:

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

[![Home Assistant Add-on][home-assistant-addon-badge]][home-assistant-addon]

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

The library is available via a Docker image from both [Docker Hub][docker-hub] and
[ghcr.io][ghcr]. It is configured by using the same environment variables listed
[above](#environment-variables).

Running the image is straightforward:

```
docker run -it \
    -e ECOWITT2MQTT_MQTT_BROKER=192.168.1.101 \
    -e ECOWITT2MQTT_MQTT_USERNAME=user \
    -e ECOWITT2MQTT_MQTT_PASSWORD=password \
    -e ECOWITT2MQTT_MQTT_TOPIC=topic \
    -p 8080:8080 \
    bachya/ecowitt2mqtt:latest
```

Note the value of the `-p` flag: you must expose the port defined by the `PORT`
environment variable. In the example above, the default port (`8080`) is used and is
exposed via the same port on the host.

[`docker-compose`][docker-compose] users can find an example configuration file at
[`docker-compose.dev.yml`](docker-compose.dev.yml). Note that this is intended to be a dev
environment for quickly testing the repo itself; in production, you should refer to one
of the published images.

# Diagnostics

You may run `ecowitt2mqtt` in diagnostics mode by providing the `--diagnostics` flag. In
this mode, the app will wait until it receives and publishes a single payload, then
exit. This allows users to collect a small-but-complete payload for use in testing,
debugging, and issue reporting.

# Contributing

Thanks to all of [our contributors][contributors] so far!

1. [Check for open features/bugs][issues] or [initiate a discussion on one][new-issue].
2. [Fork the repository][fork].
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix on a new branch.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov ecowitt2mqtt tests`
9. Update `README.md` with any new documentation.
10. Submit a pull request!

[absolute-humidity]: https://en.wikipedia.org/wiki/Humidity#Absolute_humidity
[ambient-weather]: https://ambientweather.com/
[awnet-google-play]: https://play.google.com/store/apps/details?id=com.dtston.ambienttoolplus&hl=en_US&gl=US
[awnet-ios]: https://apps.apple.com/us/app/awnet/id1341994564
[awnet-upload-screen]: resources/awnet-upload-screen.jpeg?raw=true
[beaufort-scale]: https://en.wikipedia.org/wiki/Beaufort_scale
[ci-badge]: https://img.shields.io/github/actions/workflow/status/bachya/ecowitt2mqtt/test.yml
[ci]: https://github.com/bachya/ecowitt2mqtt/actions
[codecov-badge]: https://codecov.io/gh/bachya/ecowitt2mqtt/branch/dev/graph/badge.svg
[codecov]: https://codecov.io/gh/bachya/ecowitt2mqtt
[coffee-image]: https://cdn.buymeacoffee.com/buttons/default-orange.png
[coffee]: https://www.buymeacoffee.com/bachya1208P
[contributors]: https://github.com/bachya/ecowitt2mqtt/graphs/contributors
[dew-point]: https://en.wikipedia.org/wiki/Dew_point
[docker-compose]: https://docs.docker.com/compose/
[docker-hub-badge]: https://img.shields.io/docker/pulls/bachya/ecowitt2mqtt
[docker-hub]: https://hub.docker.com/r/bachya/ecowitt2mqtt
[ecowitt]: https://www.ecowitt.com/
[fitzpatrick-scale]: https://en.wikipedia.org/wiki/Fitzpatrick_scale
[fork]: https://github.com/bachya/ecowitt2mqtt/fork
[froggit]: https://www.froggit.de/Weather-Station/
[frost-point]: https://en.wikipedia.org/wiki/Dew_point#Frost_point
[ghcr]: https://ghcr.io/bachya/ecowitt2mqtt
[heat-index]: https://en.wikipedia.org/wiki/Heat_index
[home-assistant-addon-badge]: https://my.home-assistant.io/badges/supervisor_addon.svg
[home-assistant-addon]: https://my.home-assistant.io/redirect/supervisor_addon/?addon=c35f0383_ecowitt2mqtt&repository_url=https%3A%2F%2Fgithub.com%2Fbachya%2Fhome-assistant-addons
[home-assistant-mqtt-discovery]: https://www.home-assistant.io/docs/mqtt/discovery/
[home-assistant]: https://home-assistant.io
[humidex]: https://en.wikipedia.org/wiki/Humidex
[issues]: https://github.com/bachya/ecowitt2mqtt/issues
[license-badge]: https://img.shields.io/pypi/l/ecowitt2mqtt.svg
[license]: https://github.com/bachya/ecowitt2mqtt/blob/main/LICENSE
[logo]: resources/logo-full.png
[maintainability-badge]: https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability
[maintainability]: https://codeclimate.com/github/bachya/ecowitt2mqtt/maintainability
[new-issue]: https://github.com/bachya/ecowitt2mqtt/issues/new
[pypi-badge]: https://img.shields.io/pypi/v/ecowitt2mqtt.svg
[pypi]: https://pypi.python.org/pypi/ecowitt2mqtt
[safe-exposure-times]: https://www.openuv.io/kb/skin-types-safe-exposure-time-calculation/
[simmer-index]: http://summersimmer.com/ssi_page2.htm
[thermal-comfort-library]: https://github.com/dolezsa/thermal_comfort
[version-badge]: https://img.shields.io/pypi/pyversions/ecowitt2mqtt.svg
[version]: https://pypi.python.org/pypi/ecowitt2mqtt
[wind-chill]: https://en.wikipedia.org/wiki/Wind_chill
[ws-view-google-play]: https://play.google.com/store/apps/details?id=com.ost.wsview&gl=US
[ws-view-ios]: https://apps.apple.com/us/app/ws-view/id1362944193
[ws-view-upload-screen]: resources/ws-view-upload-screen.jpeg?raw=true
