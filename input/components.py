#!/usr/bin/env python3

import RPi.GPIO as GPIO
import threading

BUTTON_BOUNCETIME = 100
LONG_PRESS_TIMEOUT = 1.0
LED_FLASH_TIME = 0.1

class LED:

    pin = 0

    on = False
    _shutoff_timer = None

    def __init__(self, pin_num):
        self.pin = pin_num

    def setup(self):
        GPIO.setup(self.pin, GPIO.OUT)

    def flash(self):
        self.turn_on()

        if (self._shutoff_timer is not None):
            self._shutoff_timer.cancel()

        self._shutoff_timer = threading.Timer(LED_FLASH_TIME, self.turn_off)

    def turn_on(self):
        on = True
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        on = False
        GPIO.output(self.pin, GPIO.LOW)

        if (self._shutoff_timer is not None):
            self._shutoff_timer.cancel()
            self._shutoff_timer = None

class Button:

    # Metadata
    name = "Unnamed button"
    pin = 0

    # State
    pressed = False
    _long_press_timer = None

    # Event handlers
    onPress = None
    onLongPress = None

    def __init__(self, name, pin_num):
        self.name = name
        self.pin = pin_num

    def setup(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self._gpio_evt, bouncetime=BUTTON_BOUNCETIME)

    def _gpio_evt(self, channel):
        if (not self.pressed and GPIO.input(self.pin) == GPIO.HIGH):
            self._on_press()
        elif (self.pressed):
            self._on_unpress()

    def _on_press(self):
        self.pressed = True
        self._long_press_timer = threading.Timer(LONG_PRESS_TIMEOUT, self._on_longpress)
        self._long_press_timer.start()

        if self.onPress is not None:
            self.onPress()

    def _on_unpress(self):
        self.pressed = False
        self._long_press_timer.cancel()

    def _on_longpress(self):
        if self.onLongPress is not None:
            self.onLongPress()
