#!/bin/bash

# Flash firmware.bin to ESP8266

# source ../venv/bin/activate

et="esptool.py --port /dev/ttyUSB0 --chip esp8266 --baud 460800"
# $et erase_flash
$et write_flash --flash_size=detect -fm dout 0 ./bin/ESP8266_GENERIC-20241129-v1.24.1.bin
