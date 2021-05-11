#!/usr/bin/env python3
import RPi.GPIO as GPIO
from bluetooth.central import CentralManager
from input.components import RGBLED
from input.controls import Controls

class Remote:

    def __init__(self):
        self._btSetup = False

    def setup(self):
        self._setup_bluetooth()
        self._setup_controls()
        self._setup_handlers()

    def persist(self):
        try:
            message = input("Running persistently. Long-press the power button to scan for lamps.\nPress enter or ^C to exit\n\n")
        finally:
            self.cleanup()

    def _setup_bluetooth(self):
        print("Setting up bluetooth")
        self._bt = CentralManager()
        self._btSetup = True
        print("Bluetooth set up")

    def _setup_controls(self):
        print("Setting up controls")
        self._controls = Controls()
        self._controls.setup()
        print("Controls set up")

    def _setup_handlers(self):
        print("Setting up handlers")
        self._controls.power_btn.onPress = self.powerPress
        self._controls.power_btn.onLongPress = self.scan
        self._controls.bri_up_btn.onPress = self.brightnessUp
        self._controls.bri_down_btn.onPress = self.brightnessDown
        self._controls.preset_1_btn.onPress = self.preset1
        self._controls.preset_2_btn.onPress = self.preset2
        self._controls.preset_3_btn.onPress = self.preset3
        print("Handlers set up")

    def scan(self):
        if (not self._btSetup):
            print("Bluetooth scan requested, but bluetooth has not been set up yet")
        else:
            self._bt.scan()

    def powerPress(self):
        if (not self._btSetup):
            print("Power button pressed, but no devices connected to receive the event")
        else:
            self._bt.toggleOnOff()

    def brightnessUp(self):
        if (not self._btSetup):
            print("Brightness up pressed, but no devices connected to receive the event")
        else:
            self._bt.brightnessUp()

    def brightnessDown(self):
        if (not self._btSetup):
            print("Brightness down pressed, but no devices connected to receive the event")
        else:
            self._bt.brightnessDown()

    def _doPreset(self, num):
        if (not self._btSetup):
            print("Preset {} pressed, but no devices connected to receive the event".format(num))
        else:
            self._bt.preset(num)

    def preset1(self):
        self._doPreset(1)

    def preset2(self):
        self._doPreset(2)

    def preset3(self):
        self._doPreset(3)

    def cleanup(self):
        print("Cleaning up GPIO")
        self._controls.cleanup()
