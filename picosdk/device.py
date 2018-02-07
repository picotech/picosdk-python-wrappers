#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Definition of the Device class, which provides access to SDK functions which require a device handle, including
capturing data and configuring the AWG.
"""

class Device(object):
    def __init__(self, driver, handle):
        self.driver = driver
        self.handle = handle

    def close(self):
        self.driver.close_unit(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        if all(i is None for i in args):
            return True
        return False

