#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Unit tests for the wrapper function for retrieving device information.
"""

from __future__ import print_function

from test.test_helpers import DriverTest, drivers_with_device_connected
from picosdk.library import DeviceNotFoundError, UnitInfo


try:
    STRING_TYPES = (str, unicode)
except:
    STRING_TYPES = (bytes, str)


class GetInfoTest(DriverTest):
    def test_get_info_success(self):
        """test_get_info_success
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
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
            info = driver.get_unit_info(device)
            device.close()

            self.assertIsInstance(info, UnitInfo)
            self.assertEqual(info.driver, driver)
            self.assertIsInstance(info.variant, STRING_TYPES)
            self.assertIsInstance(info.serial, STRING_TYPES)

        self.run_snippet_and_count_problems(drivers_to_use, test)