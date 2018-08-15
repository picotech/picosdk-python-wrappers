#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Unit tests for the wrapper functions for configuring channels
"""

from __future__ import print_function

from test.test_helpers import DriverTest, drivers_with_device_connected
from picosdk.library import ArgumentOutOfRangeError


class SetChannelTest(DriverTest):
    max_volts_by_driver = {
        "ps2000" : 20,
        "ps2000a": 20,
        "ps3000": 400,
        "ps3000a": 20,
        "ps4000": 100,
    }
    def test_set_channel_success(self):
        """test_get_info_success
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected
        def test(driver):
            expected_max_volts = self.max_volts_by_driver[driver.name]
            with driver.open_unit() as device:
                # we don't have a device call which calls this function and only this function. So we invoke it
                # carefully from outside the class.
                actual_max_voltage = driver.set_channel(device, range_peak=expected_max_volts)

            self.assertEqual(expected_max_volts, actual_max_voltage)

        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_set_channel_range_too_large(self):
        """test_get_info_success
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected

        def test(driver):
            with driver.open_unit() as device:
                threw = False
                try:
                    driver.set_channel(device, range_peak=float('inf'))
                except ArgumentOutOfRangeError:
                    threw = True
                if not threw:
                    return "didn't throw an ArgumentOutOfRangeError."

        self.run_snippet_and_count_problems(drivers_to_use, test)