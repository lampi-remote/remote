#!/usr/bin/env python3

from bluepy.btle import Scanner, Peripheral
from bluetooth.lampi import Lampi

LOG_DISCOVERY = False

class CentralManager:

    SCAN_DURATION = 10.0

    def __init__(self):
        self._scanner = Scanner()
        self._lamps = []

    def scan(self):
        # Clear existing connected lamps
        for lamp in self._lamps:
            lamp.disconnect()

        self._lamps = []

        # Scan for new lamps to connect to
        print("Scanning for devices...")

        scanResult = self._scanner.scan(CentralManager.SCAN_DURATION)

        # List all discovered devices (for debugging purposes)
        if (LOG_DISCOVERY):
            print("Known devices:")

            if (len(scanResult) == 0):
                print(" None")
            else:
                for device in scanResult:
                    print(" - {}".format(device.addr))
                    for (adtype, desc, value) in device.getScanData():
                        print("   - ({}) {}: {}".format(adtype, desc, value))

        # Connect to any lamps found
        for device in scanResult:
            if (Lampi.isLampCandidate(device)):
                lamp = Lampi(device)
                lamp.validate()
                if (lamp.isValid):
                    print("Connected to a lamp with MAC address {}".format(device.addr))
                    self._lamps.append(lamp)
                else:
                    lamp.disconnect()

        print("Scan complete")

    # Discard any lamps that are no longer connected
    def pruneLamps(self):
        for i in range(0, len(self._lamps)):
            lamp = self._lamps[i]
            if (not lamp.isConnected()):
                print("Pruned {}".format(lamp.addr))
                self._lamps.pop(i)
                i -= 1

    def handleDiscovery(self, device, isNewDevice, isNewData):
        pass

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
            lamp.startPreset(number)
