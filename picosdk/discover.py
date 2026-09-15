#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
from picosdk.errors import DeviceNotFoundError, CannotFindPicoSDKError
import importlib


# the A drivers are faster to enumerate devices, so search them first.
drivers_names = [
    'ps2000a',
    'ps3000a',
    'ps4000a',
    'ps5000a',
    'ps6000a',
    'ps6000',
    'ps2000',
    'ps3000',
    'ps4000',
]


def find_unit():
    """Search for, open and return the first device connected, on any driver."""
    for driver_name in drivers_names:
        try:
            # Dynamically import the module (e.g., picosdk.ps2000a)
            module = importlib.import_module(f'picosdk.{driver_name}')
            # Get the actual driver class/object from the module
            driver = getattr(module, driver_name)
            device = driver.open_unit()
        except DeviceNotFoundError:
            continue
        return device
    raise DeviceNotFoundError("Could not find any devices on any drivers.")


def find_all_units():
    """Search for, open and return ALL devices on ALL pico drivers (supported in this SDK wrapper)."""
    devices = []
    for driver_name in drivers_names:
        try:
            # Dynamically import the module (e.g., picosdk.ps2000a)
            module = importlib.import_module(f'picosdk.{driver_name}')
            # Get the actual driver class/object from the module
            driver = getattr(module, driver_name)
            device = driver.open_unit()
        except DeviceNotFoundError:
            continue
        devices.append(device)
    if not devices:
        raise DeviceNotFoundError("Could not find any devices on any drivers.")
    return devices


def find_units_safely():
    """Search for, open and return ALL devices on ALL pico drivers (supported in this SDK wrapper).
    Ignores CannotFindPicoSDKErrors."""
    devices = []

    for driver_name in drivers_names:
        try:
            # Dynamically import the module (e.g., picosdk.ps2000a)
            module = importlib.import_module(f'picosdk.{driver_name}')
            # Get the actual driver class/object from the module
            driver = getattr(module, driver_name)
            device = driver.open_unit()
        except (CannotFindPicoSDKError, DeviceNotFoundError):
            # Go to next driver when sdk is not installed or device is not found
            continue
        devices.append(device)
    if not devices:
        raise DeviceNotFoundError("Could not find any devices on any drivers.")
    return devices
