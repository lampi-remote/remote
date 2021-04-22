#!/usr/bin/env python3
import RPi.GPIO as GPIO
from input.components import RGBLED
from input.controls import Controls

print("Starting...")

controls = Controls()
controls.setup()

def power():
    controls.led.flash_color(RGBLED.RED)
    print("Power callback")

controls.power_btn.onPress = power

try:
    message = input("Press enter to quit\n\n")
finally:
    print("\n\nCleaning up GPIO")
    controls.cleanup()
    print()
