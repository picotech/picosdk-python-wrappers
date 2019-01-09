#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Unit tests for the wrapper function for retrieving device information.
"""

from __future__ import print_function

from test.test_helpers import DriverTest, drivers_with_device_connected
from picosdk.errors import DeviceNotFoundError, ArgumentOutOfRangeError

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

            self.assertEqual(info.driver, driver)
            self.assertIsInstance(info.variant, STRING_TYPES)
            self.assertIsInstance(info.serial, STRING_TYPES)

        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_get_info_advanced_success(self):
        """test_get_info_advanced_success
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
            # three keys present on ALL devices.
            info = driver.get_unit_info(device,
                                        "PICO_DRIVER_VERSION",
                                        "PICO_USB_VERSION",
                                        "PICO_HARDWARE_VERSION")
            device.close()

            self.assertEqual(len(info), 3)
            self.assertIsInstance(info.PICO_DRIVER_VERSION, STRING_TYPES)
            self.assertIsInstance(info.PICO_USB_VERSION, STRING_TYPES)
            self.assertIsInstance(info.PICO_HARDWARE_VERSION, STRING_TYPES)

        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_get_info_with_invalid_key_fails(self):
        """test_get_info_advanced_success
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
            threw = False
            try:
                # some valid and some invalid keys. People may pass PICO_CAL_DATE to ps2000 etc.
                info = driver.get_unit_info(device,
                                            "PICO_DRIVER_VERSION",
                                            "aillk_jasgKLASDFG_Jlasdkgfj",
                                            "PICO_HARDWARE_VERSION")
            except ArgumentOutOfRangeError:
                threw = True
            finally:
                device.close()

            if not threw:
                return "get_unit_info didn't throw exception on bad key."

        self.run_snippet_and_count_problems(drivers_to_use, test)
