#!/usr/bin/env python3

import RPi.GPIO as GPIO
import threading
import colorsys

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

# Manages an RGB LED, with three pins to control the RGB channels
class RGBLED:

    OFF = [False, False, False]
    RED = [True, False, False]
    YELLOW = [True, True, False]
    GREEN = [False, True, False]
    CYAN = [False, True, True]
    BLUE = [False, False, True]
    PURPLE = [True, False, True]

    def __init__(self, pin_r, pin_g, pin_b):
        self.pin_r = pin_r
        self.pin_g = pin_g
        self.pin_b = pin_b
        self.on = False
        self._shutoff_timer = None

    def setup(self):
        GPIO.setup(self.pin_r, GPIO.OUT)
        GPIO.setup(self.pin_g, GPIO.OUT)
        GPIO.setup(self.pin_b, GPIO.OUT)
        self.off()

    # Expects a three element array of booleans
    def _set_rgb(self, rgb):
        GPIO.output(self.pin_r, GPIO.HIGH if rgb[0] else GPIO.LOW)
        GPIO.output(self.pin_g, GPIO.HIGH if rgb[1] else GPIO.LOW)
        GPIO.output(self.pin_b, GPIO.HIGH if rgb[2] else GPIO.LOW)

    def off(self):
        self.set_color(RGBLED.OFF)

    def set_color(self, color):
        if (self._shutoff_timer is not None):
            self._shutoff_timer.cancel()

        self._set_rgb(color)

    def flash_color(self, color, timeout=LED.FLASH_TIME):
        self.set_color(color)
        self._shutoff_timer = threading.Timer(timeout, self.off)
        self._shutoff_timer.start()


# Manages a simple button circuit button, connected to any arbitrary pin
# Event handler can be assigned via onPress and onLongPress
class Button:

    BOUNCETIME = 100
    LONG_PRESS_TIMEOUT = 1.0

    def __init__(self, name, pin_num):
        # Metadata
        self.name = name
        self.pin = pin_num

        # State managers
        self.pressed = False
        self._long_press_timer = None

        # Event handlers
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
        self.pressed = True
        self._long_press_timer = threading.Timer(Button.LONG_PRESS_TIMEOUT, self._on_longpress)
        self._long_press_timer.start()

        # print("BUTTON PRESS: {} (pin {})".format(self.name, self.pin))

        if self.onPress is not None:
            self.onPress()

    def _on_unpress(self):
        self.pressed = False
        self._long_press_timer.cancel()

    def _on_longpress(self):
        if self.onLongPress is not None:
            self.onLongPress()
