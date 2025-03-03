"""TheengsGateway - Decode things and devices and publish data to an MQTT broker.

Copyright: (c)Florian ROBERT

This file is part of TheengsGateway.

TheengsGateway is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TheengsGateway is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import json
import os
import sys

from .ble_gateway import run

default_config = {
    "host": "",
    "port": 1883,
    "user": "",
    "pass": "",
    "ble_scan_time": 5,
    "ble_time_between_scans": 5,
    "publish_topic": "home/TheengsGateway/BTtoMQTT",
    "lwt_topic": "home/TheengsGateway/LWT",
    "subscribe_topic": "home/+/BTtoMQTT/undecoded",
    "presence_topic": "home/TheengsGateway/presence",
    "presence": 0,
    "publish_all": 1,
    "log_level": "INFO",
    "discovery": 1,
    "hass_discovery": 1,
    "discovery_topic": "homeassistant/sensor",
    "discovery_device_name": "TheengsGateway",
    "discovery_filter": [
        "IBEACON",
    ],
    "adapter": "",
    "scanning_mode": "active",
    "time_sync": [],
    "time_format": 0,
    "publish_advdata": 0,
}

conf_path = os.path.expanduser("~") + "/theengsgw.conf"


def main() -> None:
    """Main entry point of the TheengsGateway program."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H", "--host", dest="host", type=str, help="MQTT host address"
    )
    parser.add_argument(
        "-P", "--port", dest="port", type=int, help="MQTT host port"
    )
    parser.add_argument(
        "-u", "--user", dest="user", type=str, help="MQTT username"
    )
    parser.add_argument(
        "-p", "--pass", dest="pwd", type=str, help="MQTT password"
    )
    parser.add_argument(
        "-pt",
        "--pub_topic",
        dest="pub_topic",
        type=str,
        help="MQTT publish topic",
    )
    parser.add_argument(
        "-st",
        "--sub_topic",
        dest="sub_topic",
        type=str,
        help="MQTT subscribe topic",
    )
    parser.add_argument(
        "-Lt",
        "--lwt_topic",
        dest="lwt_topic",
        type=str,
        help="MQTT LWT topic",
    )
    parser.add_argument(
        "-prt",
        "--presence_topic",
        dest="presence_topic",
        type=str,
        help="MQTT presence topic",
    )
    parser.add_argument(
        "-pr",
        "--presence",
        dest="presence",
        type=int,
        help="Enable (1) or disable (0) presence publication (default: 1)",
    )
    parser.add_argument(
        "-pa",
        "--publish_all",
        dest="publish_all",
        type=int,
        help="Publish all (1) or only decoded (0) advertisements (default: 1)",
    )
    parser.add_argument(
        "-sd",
        "--scan_duration",
        dest="scan_dur",
        type=int,
        help="BLE scan duration (seconds)",
    )
    parser.add_argument(
        "-tb",
        "--time_between",
        dest="time_between",
        type=int,
        help="Seconds to wait between scans",
    )
    parser.add_argument(
        "-ll",
        "--log_level",
        dest="log_level",
        type=str,
        help="TheengsGateway log level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    parser.add_argument(
        "-Dt",
        "--discovery-topic",
        dest="discovery_topic",
        type=str,
        help="MQTT Discovery topic",
    )
    parser.add_argument(
        "-D",
        "--discovery",
        dest="discovery",
        type=int,
        help="Enable(1) or disable(0) MQTT discovery",
    )
    parser.add_argument(
        "-Dh",
        "--hass_discovery",
        dest="hass_discovery",
        type=int,
        help="Enable(1) or disable(0) Home Assistant MQTT discovery "
        "(default: 1)",
    )
    parser.add_argument(
        "-Dn",
        "--discovery_name",
        dest="discovery_device_name",
        type=str,
        help="Device name for Home Assistant",
    )
    parser.add_argument(
        "-Df",
        "--discovery_filter",
        dest="discovery_filter",
        nargs="+",
        default=[],
        help="Device discovery filter list for Home Assistant",
    )
    parser.add_argument(
        "-a",
        "--adapter",
        dest="adapter",
        type=str,
        help="Bluetooth adapter (e.g. hci1 on Linux)",
    )
    parser.add_argument(
        "-s",
        "--scanning_mode",
        dest="scanning_mode",
        type=str,
        choices=("active", "passive"),
        help="Scanning mode (default: active)",
    )
    parser.add_argument(
        "-ts",
        "--time_sync",
        dest="time_sync",
        nargs="+",
        default=[],
        help="Addresses of Bluetooth devices to synchronize the time",
    )
    parser.add_argument(
        "-tf",
        "--time_format",
        dest="time_format",
        type=int,
        help="Use 12-hour (1) or 24-hour (0) time format for clocks "
        "(default: 0)",
    )
    parser.add_argument(
        "-padv",
        "--publish_advdata",
        dest="publish_advdata",
        type=int,
        help="Publish advertising and advanced data (1) or not (0) (default: 0)",
    )

    args = parser.parse_args()

    try:
        with open(conf_path, encoding="utf-8") as config_file:
            config = json.load(config_file)
    except (json.JSONDecodeError, OSError):
        config = default_config

    # Merge default configuration, with data read from the configuration file
    # overriding default data.
    # This guarantees that all keys we refer to are in the dictionary.
    config = {**default_config, **config}

    if args.host:
        config["host"] = args.host
    if args.port:
        config["port"] = args.port
    if args.user:
        config["user"] = args.user
    if args.pwd:
        config["pass"] = args.pwd
    if args.pub_topic:
        config["publish_topic"] = args.pub_topic
    if args.sub_topic:
        config["subscribe_topic"] = args.sub_topic
    if args.lwt_topic:
        config["lwt_topic"] = args.lwt_topic
    if args.presence_topic:
        config["presence_topic"] = args.presence_topic
    if args.presence is not None:
        config["presence"] = args.presence
    if args.publish_all is not None:
        config["publish_all"] = args.publish_all
    if args.scan_dur:
        config["ble_scan_time"] = args.scan_dur
    if args.time_between:
        config["ble_time_between_scans"] = args.time_between
    if args.log_level:
        config["log_level"] = args.log_level

    if args.discovery is not None:
        config["discovery"] = args.discovery
    elif "discovery" not in config.keys():
        config["discovery"] = default_config["discovery"]
        config["discovery_topic"] = default_config["discovery_topic"]
        config["discovery_device_name"] = default_config[
            "discovery_device_name"
        ]
        config["discovery_filter"] = default_config["discovery_filter"]

    if args.hass_discovery is not None:
        config["hass_discovery"] = args.hass_discovery

    if args.discovery_topic:
        config["discovery_topic"] = args.discovery_topic
    elif "discovery_topic" not in config.keys():
        config["discovery_topic"] = default_config["discovery_topic"]

    if args.discovery_device_name:
        config["discovery_device_name"] = args.discovery_device_name
    elif "discovery_device_name" not in config.keys():
        config["discovery_device_name"] = default_config[
            "discovery_device_name"
        ]

    if args.discovery_filter:
        config["discovery_filter"] = default_config["discovery_filter"]
        if args.discovery_filter[0] != "reset":
            for item in args.discovery_filter:
                config["discovery_filter"].append(item)
    elif "discovery_filter" not in config.keys():
        config["discovery_filter"] = default_config["discovery_filter"]

    if args.adapter:
        config["adapter"] = args.adapter

    if args.scanning_mode:
        config["scanning_mode"] = args.scanning_mode

    if args.time_sync:
        config["time_sync"] = default_config["time_sync"]
        if args.time_sync[0] != "reset":
            for item in args.time_sync:
                config["time_sync"].append(item)
    elif "time_sync" not in config.keys():
        config["time_sync"] = default_config["time_sync"]

    if args.time_format is not None:
        config["time_format"] = args.time_format

    if args.publish_advdata is not None:
        config["publish_advdata"] = args.publish_advdata

    if not config["host"]:
        sys.exit("Invalid MQTT host")

    try:
        with open(conf_path, mode="w", encoding="utf-8") as config_file:
            config_file.write(json.dumps(config, sort_keys=True, indent=4))
    except OSError as exception:
        msg = "Unable to write config file"
        raise SystemExit(msg) from exception  # noqa: TRY003

    run(conf_path)
