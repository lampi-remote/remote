#!/usr/bin/env python3
import RPi.GPIO as GPIO
from bluetooth.central import CentralManager
from input.components import LED, RGBLED
from input.controls import Controls
from threading import Timer

class Remote:

    BLINK_TIME = 1

    def __init__(self):
        self._btSetup = False
        self._blinkTimer = None

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

    def _flash(self, color=RGBLED.GREEN):
        self._controls.led.flash_rgb(RGBLED.YELLOW)

    def scan(self):
        if (not self._btSetup):
            print("Bluetooth scan requested, but bluetooth has not been set up yet")
        else:
            self._blink_on()
            self._bt.scan()
            self._blinkStop()

            result = RGBLED.RED

            if (self._bt.isConnected):
                result = RGBLED.GREEN

            self._controls.led.flash_rgb(result)
            flash_timer = Timer(LED.FLASH_TIME * 2.0, lambda : self._controls.led.flash_rgb(result))
            flash_timer.start()


    def powerPress(self):
        self._flash()
        if (not self._btSetup or not self._bt.isConnected):
            print(self._bt.isConnected)
            print("Power button pressed, but no devices connected to receive the event")
        else:
            self._bt.toggleOnOff()

    def brightnessUp(self):
        self._flash()
        if (not self._btSetup or not self._bt.isConnected):
            print("Brightness up pressed, but no devices connected to receive the event")
        else:
            self._bt.brightnessUp()

    def brightnessDown(self):
        self._flash()
        if (not self._btSetup or not self._bt.isConnected):
            print("Brightness down pressed, but no devices connected to receive the event")
        else:
            self._bt.brightnessDown()

    def _doPreset(self, num):
        self._flash()
        if (not self._btSetup or not self._bt.isConnected):
            print("Preset {} pressed, but no devices connected to receive the event".format(num))
        else:
            self._bt.preset(num)

    def preset1(self):
        self._doPreset(1)

    def preset2(self):
        self._doPreset(2)

    def preset3(self):
        self._doPreset(3)

    def _blink_on(self):
        self._controls.led.set_rgb(RGBLED.WHITE)

        if (self._blinkTimer is not None):
            self._blinkTimer.cancel()

        self._blinkTimer = Timer(Remote.BLINK_TIME, self._blink_off)
        self._blinkTimer.start()

    def _blink_off(self):
        self._controls.led.turn_off()

        if (self._blinkTimer is not None):
            self._blinkTimer.cancel()

        self._blinkTimer = Timer(Remote.BLINK_TIME, self._blink_on)
        self._blinkTimer.start()

    def _blinkStop(self):
        if (self._blinkTimer is not None):
            self._blinkTimer.cancel()
        self._blinkTimer = None
        self._controls.led.turn_off()

    def cleanup(self):
        print("Cleaning up GPIO")
        self._controls.cleanup()
