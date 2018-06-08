#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Definition of the Device class, which provides access to SDK functions which require a device handle, including
capturing data and configuring the AWG.
"""
from __future__ import print_function


class ClosedDeviceError(Exception):
    pass


def requires_open(error_message):
    def check_open_decorator(method):
        def check_open_impl(self, *args, **kwargs):
            if not self.is_open:
                raise ClosedDeviceError(error_message)
            return method(self, *args, **kwargs)
        return check_open_impl
    return check_open_decorator



class Device(object):
    def __init__(self, driver, handle):
        self.driver = driver
        self.handle = handle
        self.is_open = handle > 0

    @requires_open
    def close(self):
        self.driver.close_unit(self)
        self.handle = None
        self.is_open = False

    @property
    @requires_open
    def info(self):
        return self.driver.get_unit_info(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        if all(i is None for i in args):
            return True
        return False

