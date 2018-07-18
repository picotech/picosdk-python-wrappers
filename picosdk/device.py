#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Definition of the Device class, which provides access to SDK functions which require a device handle, including
capturing data and configuring the AWG.
"""
from __future__ import print_function


def make_array(object, dtype=None, copy=True, order='K', subok=False, ndmin=0):
    """this function emulates the numpy array constructor in an environment without numpy.
    In the case where numpy isn't available, the return type is a normal Python list."""
    try:
        import numpy
        return numpy.array(object, dtype, copy, order, subok, ndmin)
    except ImportError:
        if not copy and dtype is None:
            return object
        if dtype is None:
            # PEP-8 requires me to write this out with a def, rather than just use a lambda.
            def dtype(i):
                return i

        # we ignore the other arguments, since Python doesn't natively support them, or (ndmin) the feature is not
        # required by the picosdk.

        return [dtype(i) for i in iter(object)]


class ClosedDeviceError(Exception):
    pass


def requires_open(error_message="This operation requires a device to be connected."):
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

        # if a channel is missing from here, its range is not yet defined.
        self._channel_ranges = {}

    @requires_open("The device either did not initialise correctly or has already been closed.")
    def close(self):
        self.driver.close_unit(self)
        self.handle = None
        self.is_open = False

    @property
    @requires_open()
    def info(self):
        return self.driver.get_unit_info(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
        if all(i is None for i in args):
            return True
        return False

    @requires_open()
    def capture_block(self):#, channels=('A'), range=float('inf'), coupling='DC'):
        """device.capture_block(channels=('A', 'B'), range=2)
        channels: a tuple of channel letters.
        range = +/- max volts, this code will choose the range which includes your value, if possible, or the max.
        coupling = 'AC' or 'DC', default is 'DC'.
        """
        # to start with, we only capture on channel 1, at widest available range, with no trigger.
        times = make_array([])
        voltages = make_array([])

        channel = 'A'

        # These are passing the default values explicitly for now.
        self._channel_ranges[channel] = self.driver.set_channel(self, channel_name=channel, coupling='DC', range=20.0)

        return times, voltages
