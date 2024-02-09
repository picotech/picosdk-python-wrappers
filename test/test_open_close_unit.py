#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Unit tests for the wrapper functions for opening and closing devices.
"""

from __future__ import print_function

from test.test_helpers import DriverTest, drivers_to_load, drivers_with_device_connected
from picosdk.errors import DeviceNotFoundError


class OpenCloseTest(DriverTest):
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
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected[:]

        def test(driver):
            threw = False
            devices = []
            try:
                devices.append(driver.open_unit())
            except DeviceNotFoundError as e:
                threw = e
            finally:
                for device in devices:
                    print("closing device %s" % device.handle)
                    device.close()
            if threw is not False:
                return "no device found (%s)." % threw
        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_close_unit_success(self):
        """test_close_unit_success
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected

        def test(driver):
            devices = []
            try:
                devices.append(driver.open_unit())
            except DeviceNotFoundError as e:
                return "no device found (%s)." % e

            device = devices.pop()
            info = device.info
            device.close()
            # To test the success of close(), we try to re-open the device.
            # If we fail, then we have not closed it correctly.
            try:
                devices.append(driver.open_unit(serial=info.serial))
            except DeviceNotFoundError as e:
                return "Could not close and then re-open the device (%s)." % e
            finally:
                for device in devices:
                    device.close()
        self.run_snippet_and_count_problems(drivers_to_use, test)

    def test_with_statement_open_close(self):
        """test_with_statement_open_close
        note: test assumes you have set test_helpers.drivers_with_device_connected"""
        if not drivers_with_device_connected:
            return
        drivers_to_use = drivers_with_device_connected[:]

        def test(driver):
            threw = False
            was_open = False
            was_closed = False
            outer_scope_device = None
            try:
                with driver.open_unit() as device:
                    was_open = device.is_open
                    outer_scope_device = device
                was_closed = not outer_scope_device.is_open
            except DeviceNotFoundError as e:
                threw = e
            finally:
                if outer_scope_device is not None and not was_closed:
                    outer_scope_device.close()
            if threw is not False:
                return "no device found (%s)." % threw
            elif not was_open:
                return "device was not opened correctly"
            elif not was_closed:
                return "device was not closed after exiting the scope"

        self.run_snippet_and_count_problems(drivers_to_use, test)
