#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Unit tests for the wrapper functions for opening, listing/enumerating and closing devices.
"""

from __future__ import print_function
import importlib
import unittest
from picosdk.library import DeviceNotFoundError

drivers_to_load = [
    'ps2000',
    'ps2000a',
    'ps3000',
    'ps3000a',
]

modules = {}

for d in drivers_to_load:
    modules[d] = importlib.import_module("picosdk.%s" % d)

# PLEASE MODIFY this list before running, to indicate which drivers should
# expect to find a device.
drivers_with_device_connected = [
    # 'ps2000',
    # 'ps2000a',
    # 'ps3000',
    # 'ps3000a',
]

class error_failure(Exception):
    pass

class error(Exception):
    pass

class OpenCloseTest(unittest.TestCase):

    def _find_driver(self, name):
        # e.g. ps2000.ps2000
        module = modules[name]
        return getattr(module, name)

    def run_snippet_and_count_problems(self, drivers_to_use, fn):
        errors = []
        failures = []
        for d in drivers_to_use:
            driver = self._find_driver(d)
            try:
                result = fn(driver)
                if result is not None:
                    failures.append((d, result))
            except Exception as e:
                errors.append((d, e))
        # format the errors and failure messages for printing:
        errors = ", ".join(["%s (%s)" % e for e in errors])
        failures = ", ".join(["%s (%s)" % f for f in failures])
        if failures and errors:
            raise error_failure("drivers error'd: %s\nand drivers failed: %s" % (errors, failures))
        elif errors:
            raise error("drivers error'd: %s" % errors)
        else:
            self.assertEqual(len(failures), 0, "Drivers failed: %s" % failures)

    def test_open_unit_failure(self):
        """test_open_unit_failure
        note: test assumes that at maximum one device is attached for each driver."""
        drivers_to_use = drivers_to_load
        def test(driver):
            threw = False
            devices = []
            try:
                devices.append(driver.open_unit())
                devices.append(driver.open_unit())
            except DeviceNotFoundError:
                threw = True
            finally:
                for device in devices:
                    device.close()
            if not threw:
                return "didn't throw a DeviceNotFoundError."
        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_open_unit_success(self):
        """test_open_unit_success
        note: test assumes you have set drivers_with_device_connected above"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected[:]
        def test(driver):
            print("in test function")
            threw = False
            devices = []
            try:
                devices.append(driver.open_unit())
            except DeviceNotFoundError:
                print("caught DeviceNotFoundError")
                threw = True
            finally:
                print("closing devices")
                for device in devices:
                    print("closing device %s" % device.handle)
                    device.close()
            if threw:
                print("returning error.")
                return "no device found."
        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_close_unit_success(self):
        """test_close_unit_success
        note: test assumes you have set drivers_with_device_connected above"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected
        def test(driver):
            devices = []
            try:
                devices.append(driver.open_unit())
            except DeviceNotFoundError:
                return "no device found."

            device = devices.pop()
            info = device.info
            device.close()
            # To test the success of close(), we try to re-open the device.
            # If we fail, then we have not closed it correctly.
            try:
                devices.append(driver.open_unit(serial=info.serial))
            except DeviceNotFoundError:
                return "Could not close and then re-open the device."
            finally:
                for device in devices:
                    device.close()
        self.run_snippet_and_count_problems(drivers_to_use, test)
