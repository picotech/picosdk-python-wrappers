#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Unit tests for the wrapper functions for computing and validating timebases
"""

from __future__ import print_function

from test.test_helpers import DriverTest, drivers_with_device_connected
import unittest
from picosdk.library import TimebaseInfo
from picosdk.errors import InvalidTimebaseError, NoValidTimebaseForOptionsError
from picosdk.device import Device, TimebaseOptions
import math


class FindTimebaseTest(DriverTest):
    def assertValidTimebases(self, input_config, output_info):
        if input_config.max_time_interval is not None:
            self.assertLessEqual(output_info.time_interval, input_config.max_time_interval)
        if input_config.no_of_samples is not None:
            self.assertGreaterEqual(output_info.max_samples, input_config.no_of_samples)
        if input_config.min_collection_time is not None:
            self.assertGreaterEqual(output_info.time_interval * output_info.max_samples,
                                    input_config.min_collection_time)

    def test_find_timebase_success(self):
        """test_find_timebase_success
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected

        def test(driver):

            with driver.open_unit() as device:
                five_milliseconds = 0.005
                config = TimebaseOptions(max_time_interval=five_milliseconds,
                                         no_of_samples=None,
                                         min_collection_time=five_milliseconds * 30,
                                         oversample=1)
                timebase_info = device.find_timebase(config)

            self.assertValidTimebases(config, timebase_info)

        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_find_timebase_terrasample(self):
        """test_find_timebase_terrasample
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected

        def test(driver):
            with driver.open_unit() as device:
                threw = False
                try:
                    # we ask for a config which requires 1TS (one terra-sample) of memory on device.
                    smallest_timebase = 1.e-8
                    one_terra_sample = 1.e12
                    duration = smallest_timebase * one_terra_sample
                    config = TimebaseOptions(max_time_interval=smallest_timebase,
                                             no_of_samples=one_terra_sample,
                                             min_collection_time=duration)
                    timebase_info = device.find_timebase(config)
                except NoValidTimebaseForOptionsError:
                    threw = True
                if not threw:
                    return "didn't throw an NoValidTimebaseForOptionsError."

        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_find_timebase_impossible(self):
        """test_find_timebase_impossible
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected

        def test(driver):
            with driver.open_unit() as device:
                threw = False
                try:
                    # we ask for a config which cannot be achieved (specifying all 3 variables can lead to invalid
                    # configs.)
                    no_of_samples = 150
                    duration = 0.4
                    computed_timebase = duration / no_of_samples
                    max_timebase_requested = computed_timebase / 4
                    config = TimebaseOptions(max_time_interval=max_timebase_requested,
                                             no_of_samples=no_of_samples,
                                             min_collection_time=duration)
                    timebase_info = device.find_timebase(config)
                except NoValidTimebaseForOptionsError:
                    threw = True
                if not threw:
                    return "didn't throw an NoValidTimebaseForOptionsError."

        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_get_timebase_throws_on_bad_params(self):
        """test_get_timebase_impossible
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected

        def test(driver):
            with driver.open_unit() as device:
                threw = False
                try:
                    # we ask for a config which cannot be achieved (specifying all 3 variables can lead to invalid
                    # configs.)
                    no_of_samples = 150
                    duration = 0.4
                    computed_timebase = duration / no_of_samples
                    max_timebase_requested = computed_timebase / 4

                    # we manually invoke the Library method, to check that if invalid options sneak through, we throw
                    # a different error:
                    timebase_info = device.driver.get_timebase(device, 1, no_of_samples)
                except InvalidTimebaseError:
                    threw = True
                if not threw:
                    return "didn't throw an InvalidTimebaseError."

        self.run_snippet_and_count_problems(drivers_to_use, test)


class TimebaseValidationTest(unittest.TestCase):
    def test_valid_config(self):
        request = TimebaseOptions(max_time_interval=0.005,
                                  no_of_samples=None,
                                  min_collection_time=1.)
        actual_timebase = 0.004
        required_max_samples = int(math.ceil(request.min_collection_time / actual_timebase))
        response = TimebaseInfo(timebase_id=7,
                                time_interval=0.004,
                                time_units=None,
                                max_samples=required_max_samples+1,
                                segment_id=0)

        self.assertTrue(Device._validate_timebase(request, response))

    def test_invalid_config(self):
        request = TimebaseOptions(max_time_interval=0.005,
                                  no_of_samples=None,
                                  min_collection_time=1.)
        actual_timebase = 0.004
        required_max_samples = int(math.ceil(request.min_collection_time / actual_timebase))
        response = TimebaseInfo(timebase_id=7,
                                time_interval=0.004,
                                time_units=None,
                                max_samples=required_max_samples-5,
                                segment_id=0)

        self.assertFalse(Device._validate_timebase(request, response))
