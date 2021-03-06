#!/usr/bin/env python3

import RPi.GPIO as GPIO
from input.components import *

# The maps the "controls" for our remote to their circuit components
class Controls:

    setup_complete = False

    led = RGBLED("Main", 24, 26, 32)
    power_btn = Button("Power", 8)
    bri_up_btn = Button("Brightness Up", 10)
    bri_down_btn = Button("Brightness Down", 12)
    preset_1_btn = Button("Preset 1", 16)
    preset_2_btn = Button("Preset 2", 18)
    preset_3_btn = Button("Preset 3", 22)

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

    def setup(self):
        self.led.setup()
        self.power_btn.setup()
        self.bri_up_btn.setup()
        self.bri_down_btn.setup()
        self.preset_1_btn.setup()
        self.preset_2_btn.setup()
        self.preset_3_btn.setup()

        self.setup_complete = True

    def cleanup(self):
        GPIO.cleanup()
