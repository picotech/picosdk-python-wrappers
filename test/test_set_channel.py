#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Unit tests for the wrapper functions for configuring channels
"""

from __future__ import print_function

from test.test_helpers import DriverTest, drivers_with_device_connected
from picosdk.errors import ArgumentOutOfRangeError
from picosdk.device import ChannelConfig


class SetChannelTest(DriverTest):
    # Both 3000a and 5000a define a 50V enum member, but neither actually has a device which
    # supports that range.
    max_volts_by_driver = {
        "ps2000": 20,
        "ps2000a": 20,
        "ps3000": 400,
        "ps3000a": 20,
        "ps4000": 100,
        "ps4000a": 50,
        "ps5000a": 20,
    }

    def test_set_channel_success(self):
        """test_set_channel_success
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected

        def test(driver):
            expected_max_volts = self.max_volts_by_driver[driver.name]
            with driver.open_unit() as device:
                config = ChannelConfig(name='A', enabled=True, coupling='DC', range_peak=expected_max_volts)
                actual_max_voltage = device.set_channel(config)

            self.assertEqual(expected_max_volts, actual_max_voltage)

        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_set_channel_very_small_peak(self):
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected

        # Some drivers specify more ranges than some of their devices actually support. Check that we handle this error
        # at the lowest voltages (at the upper range, see the relevant test below, there's nothing we can do but raise.)
        def test(driver):
            five_millivolts = 0.005

            with driver.open_unit() as device:
                config = ChannelConfig(name='A', enabled=True, coupling='DC', range_peak=five_millivolts)
                actual_max_voltage = device.set_channel(config)

            self.assertGreaterEqual(actual_max_voltage, five_millivolts)

        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_set_channel_range_too_large(self):
        """test_set_channel_range_too_large
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
