#!/usr/bin/env python3
import RPi.GPIO as GPIO
from input.components import RGBLED
from input.controls import Controls
import argparse
import logging

# Set up the args parser and logger
parser = argparse.ArgumentParser(description="LAMPI remote")
parser.add_argument('--log', default='INFO', choices=['debug', 'DEBUG', 'info', 'INFO', 'warning', 'WARNING', 'error', 'ERROR', 'critical', 'CRITICAL'], required=False, dest='loglevel', type=str)
args = parser.parse_args()
print(args)

numeric_level = getattr(logging, args.loglevel.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)

logging.basicConfig(level=numeric_level, format='%(levelname)s: %(message)s')

logging.info("Starting...")

controls = Controls()
controls.setup()

def power():
    controls.led.flash_rgb(RGBLED.RED)

controls.power_btn.onPress = power

try:
    message = input("Press enter to quit\n\n")
finally:
    logging.info("Cleaning up GPIO")
    controls.cleanup()
    print()
