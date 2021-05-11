#!/usr/bin/env python3

import RPi.GPIO as GPIO
import threading

LOG_EVENTS = False

# Manages a simple LED circuit component, connected to any arbitrary pin
class LED:

    FLASH_TIME = 0.1

    def __init__(self, pin_num):
        self.pin = pin_num
        self.on = False
        self._shutoff_timer = None

    def setup(self):
        GPIO.setup(self.pin, GPIO.OUT)

    def flash(self):
        self.turn_on()

        if (self._shutoff_timer is not None):
            self._shutoff_timer.cancel()

        self._shutoff_timer = threading.Timer(LED.FLASH_TIME, self.turn_off)
        self._shutoff_timer.start()

    def turn_on(self):
        on = True
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        on = False
        GPIO.output(self.pin, GPIO.LOW)

        if (self._shutoff_timer is not None):
            self._shutoff_timer.cancel()
            self._shutoff_timer = None

# Manages a simple button circuit button, connected to any arbitrary pin
# Event handler can be assigned via onPress and onLongPress
class Button:

    BOUNCETIME = 100
    LONG_PRESS_TIMEOUT = 1.0

    def __init__(self, name, pin_num):
        self.name = name
        self.pin = pin_num
        self.pressed = False
        self._long_press_timer = None
        self.onPress = None
        self.onLongPress = None

    def setup(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self._gpio_evt, bouncetime=Button.BOUNCETIME)

    def _gpio_evt(self, channel):
        if (not self.pressed and GPIO.input(self.pin) == GPIO.HIGH):
            self._on_press()
        elif (self.pressed):
            self._on_unpress()

    def _on_press(self):
        if (LOG_EVENTS):
            print('Button {} pressed'.format(self.name))

        self.pressed = True
        self._long_press_timer = threading.Timer(Button.LONG_PRESS_TIMEOUT, self._on_longpress)
        self._long_press_timer.start()

    def _on_unpress(self):
        self.pressed = False

        if (LOG_EVENTS):
            print('Button {} released'.format(self.name))

        if (self._long_press_timer is not None):
            self._long_press_timer.cancel()
            self._long_press_timer = None

            if self.onPress is not None:
                self.onPress()

    def _on_longpress(self):
        if (LOG_EVENTS):
            print('Button {} long pressed'.format(self.name))

        self._long_press_timer = None
        if self.onLongPress is not None:
            self.onLongPress()

class RGBLED:

    OFF = [False, False, False]
    RED = [True, False, False]
    YELLOW = [True, True, False]
    GREEN = [False, True, False]
    CYAN = [False, True, True]
    BLUE = [False, False, True]
    PURPLE = [True, False, True]
    WHITE = [True, True, True]

    def _asVoltage(bool):
        return GPIO.HIGH if bool else GPIO.LOW

    def __init__(self, name, rpin, gpin, bpin):
        self.name = name
        self.rpin = rpin
        self.gpin = gpin
        self.bpin = bpin
        self._shutoff_timer = None
        self._flash_counter = 0
        self._flash_rgb = None

    def setup(self):
        GPIO.setup(self.rpin, GPIO.OUT)
        GPIO.setup(self.gpin, GPIO.OUT)
        GPIO.setup(self.bpin, GPIO.OUT)
        self.set_rgb(RGBLED.OFF)

    def set_rgb(self, rgb):
        GPIO.output(self.rpin, RGBLED._asVoltage(rgb[0]))
        GPIO.output(self.gpin, RGBLED._asVoltage(rgb[1]))
        GPIO.output(self.bpin, RGBLED._asVoltage(rgb[2]))

    def flash_rgb(self, rgb, times=0):
        self.set_rgb(rgb)

        if (self._shutoff_timer is not None):
            self._shutoff_timer.cancel()

        self._flash_counter = times
        self._flash_rgb = rgb

        self._shutoff_timer = threading.Timer(LED.FLASH_TIME, self.turn_off)
        self._shutoff_timer.start()

    def turn_off(self):
        self.set_rgb(RGBLED.OFF)

        if (self._shutoff_timer is not None):
            self._shutoff_timer.cancel()
            self._shutoff_timer = None

        if (self._flash_counter > 0):
            self._shutoff_timer = threading.Timer(LED.FLASH_TIME, lambda : self.flash_rgb(self._flash_rgb, self._flash_counter - 1))
            self._shutoff_timer.start()
