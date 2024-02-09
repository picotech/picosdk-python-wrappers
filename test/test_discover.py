#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Unit tests for the wrapper functions for discovering devices
"""

from __future__ import print_function

from test.test_helpers import DriverTest, drivers_with_device_connected
from picosdk.device import Device
from picosdk.errors import DeviceNotFoundError
import picosdk.discover as dut


class OpenCloseTest(DriverTest):
    def test_find_unit_success(self):
        """test_find_unit_success
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return

        device = dut.find_unit()
        try:
            self.assertIsInstance(device, Device)
            self.assertIn(device.driver.name, drivers_with_device_connected)
        finally:
            device.close()

    def test_find_all_units_success(self):
        """test_find_all_units_success
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return

        devices = dut.find_all_units()

        try:
            for device in devices:
                self.assertIsInstance(device, Device)
                self.assertIn(device.driver.name, drivers_with_device_connected)
            self.assertEqual(set(device.driver.name for device in devices), set(drivers_with_device_connected))
        finally:
            for device in devices:
                device.close()

    def test_find_unit_failure(self):
        devices = []
        threw = False
        try:
            while len(devices) <= len(drivers_with_device_connected):
                devices.append(dut.find_unit())
        except DeviceNotFoundError:
            threw = True
        finally:
            for device in devices:
                device.close()
        self.assertEqual(len(drivers_with_device_connected), len(devices))
        self.assertTrue(threw)

    def test_find_all_units_failure(self):
        devices = []
        threw = False
        try:
            devices = dut.find_all_units()
            dut.find_all_units()
        except DeviceNotFoundError:
            threw = True
        finally:
            for device in devices:
                device.close()
        self.assertTrue(threw)
