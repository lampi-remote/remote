from bluepy.btle import Peripheral

class Lampi(Peripheral):

    MAIN_UUID = '0001A7D3-D8A4-4FEA-8174-1736E808C066'
    ONOFF_UUID = '0004A7D3-D8A4-4FEA-8174-1736E808C066'
    HSV_UUID = '0002A7D3-D8A4-4FEA-8174-1736E808C066'
    BRIGHTNESS_UUID = '0003A7D3-D8A4-4FEA-8174-1736E808C066'
    PRESET_UUID = '0005A7D3-D8A4-4FEA-8174-1736E808C066'

    def __init__(self, device):
        Peripheral.__init__(self, device.addr, addrType=device.addrType, iface=device.iface)
        self.isValid = False
        self.isChecked = False
        self.lampService = None
        self.onOffChar = None
        self.hsvChar = None
        self.brightnessChar = None
        self.presetChar = None

    # Check if this device is advertising the LampService UUID
    def isLampCandidate(device):
        for (adtype, desc, value) in device.getScanData():
            if (adtype == 6):
                return value.upper() == Lampi.MAIN_UUID

        return False

    # Check if a given UUID equals a string
    def matchingUUIDs(uuid, compareTo):
        return uuid.getCommonName().upper() == compareTo.upper()

    # Check if a given service is a LampService (has the right characteristics)
    def serviceIsLampiService(service):
        if (not Lampi.matchingUUIDs(service.uuid, Lampi.MAIN_UUID)):
            return False

        hasOnOff = False
        hasHsv = False
        hasBrightness = False
        hasPreset = False

        for c in service.getCharacteristics():
            if (Lampi.matchingUUIDs(c.uuid, Lampi.ONOFF_UUID)):
                hasOnOff = True
            elif (Lampi.matchingUUIDs(c.uuid, Lampi.HSV_UUID)):
                hasHsv = True
            elif (Lampi.matchingUUIDs(c.uuid, Lampi.BRIGHTNESS_UUID)):
                hasBrightness = True
            elif (Lampi.matchingUUIDs(c.uuid, Lampi.PRESET_UUID)):
                hasPreset = True

        return hasOnOff and hasHsv and hasBrightness and hasPreset

    # Validate whether the current device is a LAMPI or not
    def validate(self):
        self.isChecked = True
        for service in self.getServices():
            if (Lampi.serviceIsLampiService(service)):
                self.lampService = service
                self.isValid = True
                self.parseCharacteristics(service)
                return

        self.isValid = False

    # Check if the current device is connected
    def isConnected(self):
        connected = True

        try:
            self.onOffChar.read()
        except Exception as e:
            connected = False

        return connected

    # Fetch the characteristics we need from the service
    def parseCharacteristics(self, service):
        for c in service.getCharacteristics():
            if (Lampi.matchingUUIDs(c.uuid, Lampi.ONOFF_UUID)):
                self.onOffChar = c
            elif (Lampi.matchingUUIDs(c.uuid, Lampi.HSV_UUID)):
                self.hsvChar = c
            elif (Lampi.matchingUUIDs(c.uuid, Lampi.BRIGHTNESS_UUID)):
                self.brightnessChar = c
            elif (Lampi.matchingUUIDs(c.uuid, Lampi.PRESET_UUID)):
                self.presetChar = c

    # Toggle the on/off characteristic
    def toggleOnOff(self):
        current = self.onOffChar.read()[0]
        next = 1 - current
        self.onOffChar.write(bytes([next]), True)

    def writeHsv(self, h, s):
        b = bytes([h * 255.0, s * 255.0, 255.0])
        self.hsvChar.write(b, True)

    def brightnessUp(self):
        current = self.brightnessChar.read()[0] / 255.0
        next = round(min(1.0, current + 0.1) * 10.0) / 10.0
        nextBytes = bytes([round(next * 255.0)])
        self.brightnessChar.write(nextBytes, True)

    def brightnessDown(self):
        current = self.brightnessChar.read()[0] / 255.0
        next = round(max(0.0, current - 0.1) * 10.0) / 10.0
        nextBytes = bytes([round(next * 255.0)])
        self.brightnessChar.write(nextBytes, True)

    def setPreset(self, number):
        current = self.presetChar.read()[0]
        if current == number:
            self.presetChar.write(0x0, True)
        else:
            nextBytes = bytes([number])
            self.presetChar.write(nextBytes, True)