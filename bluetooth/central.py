#!/usr/bin/env python3

from bluepy.btle import Scanner, Peripheral, DefaultDelegate
from bluetooth.lampi import Lampi

class CentralManager(DefaultDelegate):

    SCAN_COUNT = 5
    SCAN_INTERVAL = 2.0

    def __init__(self):
        DefaultDelegate.__init__(self)
        self._scanner = Scanner().withDelegate(self)
        self._lamps = []
        self._candidateFound = False
        self.isConnected = False

    def scan(self):
        self.isConnected = False

        # Clear existing connected lamps
        for lamp in self._lamps:
            lamp.disconnect()

        self._lamps = []

        # Scan for new lamps to connect to
        print("Scanning for devices...")

        self._candidateFound = False
        self._scanner.clear()
        self._scanner.start()

        for iter in range(0, CentralManager.SCAN_COUNT):
            self._scanner.process(CentralManager.SCAN_INTERVAL)
            if (self._candidateFound):
                print("Candidate found after {} scan(s). Ending early".format(iter + 1))
                break

        self._scanner.stop()

        scanResult = self._scanner.getDevices()

        # Connect to any lamps found
        for device in scanResult:
            if (Lampi.isLampCandidate(device)):
                lamp = Lampi(device)
                lamp.validate()
                if (lamp.isValid):
                    print("Connected to a lamp with MAC address {}".format(device.addr))
                    self._lamps.append(lamp)
                    self.isConnected = True
                else:
                    lamp.disconnect()

        print("Scan complete")

    def handleDiscovery(self, device, isNew, _):
        if isNew and device.connectable:
            if (Lampi.isLampCandidate(device)):
                self._candidateFound = True
                print(" • Candidate found with MAC address {}".format(device.addr))

    # Discard any lamps that are no longer connected
    def pruneLamps(self):
        for i in range(0, len(self._lamps)):
            lamp = self._lamps[i]
            if (not lamp.isConnected()):
                print("Pruned {}".format(lamp.addr))
                self._lamps.pop(i)
                i -= 1

    def toggleOnOff(self):
        print("Toggling on/off")
        self.pruneLamps()
        for lamp in self._lamps:
            lamp.toggleOnOff()

    def brightnessUp(self):
        print("Sending brightness up")
        self.pruneLamps()
        for lamp in self._lamps:
            lamp.brightnessUp()

    def brightnessDown(self):
        print("Sending brightness down")
        self.pruneLamps()
        for lamp in self._lamps:
            lamp.brightnessDown()

    def preset(self, number):
        print("Starting Preset", str(number))
        self.pruneLamps()
        for lamp in self._lamps:
            lamp.setPreset(number)
