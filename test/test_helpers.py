#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Helper methods for tests, and test configuration information.
"""

import importlib as _importlib
import unittest as _unittest

drivers_to_load = [
    'ps2000',
    'ps2000a',
    'ps3000',
    'ps3000a',
    'ps4000',
    'ps4000a',
    'ps5000a',
    'ps6000',
]

modules = {}

for _d in drivers_to_load:
    modules[_d] = _importlib.import_module("picosdk.%s" % _d)

# PLEASE MODIFY this list before running, to indicate which drivers should
# expect to find a device.
drivers_with_device_connected = [
    # 'ps2000',
    # 'ps2000a',
    # 'ps3000',
    # 'ps3000a',
    # 'ps4000',
    # 'ps4000a',
    # 'ps5000a',
    # 'ps6000',
]


class TestFailAndError(Exception):
    pass


class TestError(Exception):
    pass


class DriverTest(_unittest.TestCase):
    @staticmethod
    def _find_driver(name):
        # e.g. ps2000.ps2000
        m = modules[name]
        return getattr(m, name)

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
        errors = ", ".join(["%s (%r)" % e for e in errors])
        failures = ", ".join(["%s (%s)" % f for f in failures])
        if failures and errors:
            raise TestFailAndError("drivers error'd: %s\nand drivers failed: %s" % (errors, failures))
        elif errors:
            raise TestError("drivers error'd: %s" % errors)
        else:
            self.assertEqual(len(failures), 0, "Drivers failed: %s" % failures)
