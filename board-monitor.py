#!/usr/bin/env python3
import sys
from os import system
from time import sleep
import RPi.GPIO as GPIO
from threading import Timer

ALL_PINS = []

# Terminal Colors
class TCOLOR:
    RESET=u"\u001b[0m"
    RED=u"\u001b[31m"
    GREEN=u"\u001b[32m"
    PURPLE=u"\u001b[35m"
    GREY=u"\u001b[38;5;245m"

class Pin:

    NEW_MSG = "{}*{}".format(TCOLOR.PURPLE, TCOLOR.RESET)
    LOW_MSG = "{}LOW{}".format(TCOLOR.RED, TCOLOR.RESET)
    HIGH_MSG = "{}HIGH{}".format(TCOLOR.GREEN, TCOLOR.RESET)

    onchangehandler = None

    def sortFn(pinInst):
        return pinInst.pin

    def __init__(self, pin_num, description="", invalid=False):
        self.pin = pin_num
        self.desc = description
        self.recently_changed = False
        self._change_timer = None
        self.invalid = invalid
        self.report_str = ""

    def read(self):
        return GPIO.input(self.pin)

    def setup(self):
        print("Setting up pin {}".format(self.pin))
        if (self.invalid):
            self.report_str = self._make_report()
            return

        GPIO.setup(self.pin, GPIO.IN)
        self._last_value = None
        self.value = self.read()

        self.report_str = self._make_report()

        GPIO.add_event_detect(self.pin, GPIO.BOTH, callback=self._evt_handler, bouncetime=10)

    def _evt_handler(self, channel):
        self._last_value = self.value
        self.value = self.read()

        if (self.value != self._last_value):
            self._changed()

    def _changed(self):
        self.recently_changed = True
        self._request_update()

        if (self._change_timer is not None):
            self._change_timer.cancel()

        self._change_timer = Timer(0.1, self._report_unchange)
        self._change_timer.start()

    def _report_unchange(self):
        if (self._change_timer is not None):
            self._change_timer.cancel()
            self._change_timer = None

        self.recently_changed = False
        self._request_update()

    def _request_update(self):
        self.report_str = self._make_report()
        if (Pin.onchangehandler is not None):
            Pin.onchangehandler(self.pin)

    def _make_report(self):
        prefix = TCOLOR.GREY if self.invalid else ""
        is_new = " "

        if (not self.invalid and self.recently_changed):
            is_new = Pin.NEW_MSG

        value_name = Pin.LOW_MSG

        if (self.invalid):
            value_name = "-\t"
        elif (self.value == GPIO.HIGH):
            value_name = Pin.HIGH_MSG

        return "{}{:>2}  {} {}\t{}".format(prefix, self.pin, is_new, value_name, self.desc)


class Watcher:

    DELAY = 0.01

    def __init__(self):
        self.pins = ALL_PINS
        self._update_timer = None
        self._performing_update = False
        self._needs_update = True
        self._change_made_during_update = False

    def setup(self):
        for pin in self.pins:
            pin.setup()

        Pin.onchangehandler = lambda pin : self.pin_changed(pin)

    def begin(self):
        self.clear_screen()
        self._do_update()

    def clear_screen(self):
        _ = system("tput clear")

    def pin_changed(self, pin):
        if (self._performing_update):
            self._change_made_during_update = True
        else:
            self._needs_update = True

    def _schedule_next_update(self):
        self._update_timer = Timer(Watcher.DELAY, self._do_update)
        self._update_timer.start()

    def _do_update(self):
        if (self._update_timer is not None):
            self._update_timer.cancel()

        self._report()
        self._schedule_next_update()

    def _report(self):
        if (not self._needs_update):
            return

        self._performing_update = True

        out = "PIN  STATUS\tDESC\n"

        for pin in self.pins:
            out += pin.report_str + TCOLOR.RESET + "\n"

        self.clear_screen()
        print(out)
        self._needs_update = self._change_made_during_update
        self._change_made_during_update = False
        self._performing_update = False

def main():
    ALL_PINS.append(Pin(1, "3.3V", True))
    ALL_PINS.append(Pin(2, "5V", True))
    ALL_PINS.append(Pin(4, "5V", True))
    ALL_PINS.append(Pin(6, "GND", True))
    ALL_PINS.append(Pin(9, "GND", True))
    ALL_PINS.append(Pin(14, "GND", True))
    ALL_PINS.append(Pin(17, "3.3V", True))
    ALL_PINS.append(Pin(20, "GND", True))
    ALL_PINS.append(Pin(25, "GND", True))
    ALL_PINS.append(Pin(27, "ID_SC", True))
    ALL_PINS.append(Pin(28, "ID_SC", True))
    ALL_PINS.append(Pin(30, "GND", True))
    ALL_PINS.append(Pin(34, "GND", True))
    ALL_PINS.append(Pin(39, "GND", True))

    for n in range(1, 41):
        taken = False
        for pin in ALL_PINS:
            if (pin.pin == n):
                taken = True
                break

        if (taken):
            continue
        else:
            ALL_PINS.append(Pin(n))

    ALL_PINS.sort(key=Pin.sortFn)

    print("Starting...")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    watcher = Watcher()
    watcher.setup()
    watcher.begin()
    message = input("Press enter to quit\n\n")
try:
    main()
finally:
    GPIO.cleanup()
