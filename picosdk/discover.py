#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
from picosdk.errors import DeviceNotFoundError
from picosdk.ps2000 import ps2000
from picosdk.ps2000a import ps2000a
from picosdk.ps3000 import ps3000
from picosdk.ps3000a import ps3000a
from picosdk.ps4000 import ps4000
from picosdk.ps4000a import ps4000a
from picosdk.ps5000a import ps5000a
from picosdk.ps6000 import ps6000
from picosdk.ps6000a import ps6000a


# the A drivers are faster to enumerate devices, so search them first.
drivers = [
    ps2000a,
    ps3000a,
    ps4000a,
    ps5000a,
    ps6000a,
    ps6000,
    ps2000,
    ps3000,
    ps4000,
]


def find_unit():
    """Search for, open and return the first device connected, on any driver."""
    for driver in drivers:
        try:
            device = driver.open_unit()
        except DeviceNotFoundError:
            continue
        return device
    raise DeviceNotFoundError("Could not find any devices on any drivers.")


def find_all_units():
    """Search for, open and return ALL devices on ALL pico drivers (supported in this SDK wrapper)."""
    devices = []
    for driver in drivers:
        try:
            device = driver.open_unit()
        except DeviceNotFoundError:
            continue
        devices.append(device)
    if not devices:
        raise DeviceNotFoundError("Could not find any devices on any drivers.")
    return devices