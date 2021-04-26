import asyncio
import logging

from bleak import BleakClient
from bleak import BleakScanner


BT_DEVICE = "B8:27:EB:6B:C8:97"
LAMPI_SERVICE = "0001a7d3-d8a4-4fea-8174-1736e808c066"
LAMPI_ONOFF_CHARACTERISTIC = "0004a7d3-d8a4-4fea-8174-1736e808c066"


async def run():
    async with BleakScanner() as scanner:
        await asyncio.sleep(5.0)
        devices = await scanner.get_discovered_devices()
        print(devices)
    for d in devices:
        print(d.address)
        if d.address == BT_DEVICE:
            await read(d)

async def read(address):
    client = BleakClient(address)
    try:
        await client.connect()
        model_number = await client.read_gatt_char(LAMPI_ONOFF_CHARACTERISTIC)
        print("Model Number: {0}".format("".join(map(chr, model_number))))
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())