#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Definition of the Device class, which provides access to SDK functions which require a device handle, including
capturing data and configuring the AWG.
"""
from __future__ import print_function
import collections


def make_array(obj, dtype=None, copy=True, order='K', subok=False, ndmin=0):
    """this function emulates the numpy array constructor in an environment without numpy.
    In the case where numpy isn't available, the return type is a normal Python list."""
    try:
        import numpy
        return numpy.array(obj, dtype, copy, order, subok, ndmin)
    except ImportError:
        if not copy and dtype is None:
            return obj
        if dtype is None:
            # PEP-8 requires me to write this out with a def, rather than just use a lambda.
            def dtype(v):
                return v

        # we ignore the other arguments, since Python doesn't natively support them, or (ndmin) the feature is not
        # required by the picosdk.

        return [dtype(i) for i in iter(obj)]


class ClosedDeviceError(Exception):
    pass


class NoChannelsEnabledError(Exception):
    pass


def requires_open(error_message="This operation requires a device to be connected."):
    def check_open_decorator(method):
        def check_open_impl(self, *args, **kwargs):
            if not self.is_open:
                raise ClosedDeviceError(error_message)
            return method(self, *args, **kwargs)
        return check_open_impl
    return check_open_decorator


"""ChannelConfig: A type for specifying channel setup for capture (pass into Device.set_channel, or Device.capture_*)
name = The channel name as a string (e.g. 'A'.)
enabled = bool indicating whether the channel should be enabled or disabled.
coupling (optional) = 'AC' or 'DC', default is 'DC'.
range_peak (optional) = +/- max volts, the highest precision range which includes your value will be selected.
analog_offset (optional) = the meaning of 0 for this channel."""
ChannelConfig = collections.namedtuple('ChannelConfig', ['name', 'enabled', 'coupling', 'range_peak', 'analog_offset'])
ChannelConfig.__new__.__defaults__ = (None, None, None)


class Device(object):
    """This object caches some information about the device state which cannot be queried from the driver. Please don't
    mix and match calls to this object with calls directly to the driver (or the ctypes wrapper), as this may cause
    unwanted behaviour (e.g. throwing an exception because no channels are enabled, when you enabled them yourself
    on the driver object.)"""
    def __init__(self, driver, handle):
        self.driver = driver
        self.handle = handle
        self.is_open = handle > 0

        # if a channel is missing from here, its range is not yet defined.
        self._channel_ranges = {}
        self._channel_offsets = {}

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
    def set_channel(self, channel_config):
        name = channel_config.name
        if not channel_config.enabled:
            self.driver.set_channel(self,
                                    channel_name=name,
                                    enabled=channel_config.enabled)
            try:
                del self._channel_ranges[name]
                del self._channel_offsets[name]
            except KeyError:
                pass
            return
        # if enabled, we pass through the values from the channel config:
        self._channel_ranges[name] = self.driver.set_channel(self,
                                                             channel_name=name,
                                                             enabled=channel_config.enabled,
                                                             coupling=channel_config.coupling,
                                                             range_peak=channel_config.range_peak,
                                                             analog_offset=channel_config.analog_offset)
        self._channel_offsets[name] = channel_config.analog_offset
        return self._channel_ranges[name]

    @requires_open()
    def set_channels(self, *channel_configs):
        """ set_channels(self, *channel_configs)
        An alternative to calling set_channel for each one, you can call this method with some channel configs.
        This method will also disable any missing channels from the passed configs, and disable ALL channels if the
        collection is empty. """
        # Add channels which are missing as "disabled".
        if len(channel_configs) < len(self.driver.PICO_CHANNEL):
            channel_configs = list(channel_configs)
            present_channels = set(c.name for c in channel_configs)
            missing_channels = [cn for cn in self.driver.PICO_CHANNEL.keys() if cn not in present_channels]
            for channel_name in missing_channels:
                channel_configs.append(ChannelConfig(channel_name, False))

        for channel_config in channel_configs:
            self.set_channel(channel_config)

    @requires_open()
    def capture_block(self, channel_configs=()):
        """device.capture_block(channel_configs)
        channel_configs: a collection of ChannelConfig objects. If present, will be passed to set_channels.
        """
        times = []
        voltages = []

        if channel_configs:
            self.set_channels(*channel_configs)

        if len(self._channel_ranges) == 0:
            raise NoChannelsEnabledError("We cannot capture any data if no channels are enabled.")

        return times, voltages
