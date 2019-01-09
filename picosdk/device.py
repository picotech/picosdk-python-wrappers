# coding=utf-8
#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Definition of the Device class, which provides access to SDK functions which require a device handle, including
capturing data and configuring the AWG.
"""
from __future__ import print_function
import collections
import numpy
import math
import time
from picosdk.errors import DeviceCannotSegmentMemoryError, InvalidTimebaseError, ClosedDeviceError, \
    NoChannelsEnabledError, NoValidTimebaseForOptionsError


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


"""TimebaseOptions: A type for specifying timebase constraints (pass to Device.find_timebase or Device.capture_*)
All are optional. Please specify the options which matter to you: 
  - the maximum time interval (if you want the fastest/most precise timebase you can get),
  - the number of samples in one buffer,
  - the minimum total collection time (if you want at least x.y seconds of uninterrupted capture data)
  - the oversample (if you want to sacrifice time precision for amplitude precision - see the programming guides.)"""
TimebaseOptions = collections.namedtuple('TimebaseOptions', ['max_time_interval',
                                                             'no_of_samples',
                                                             'min_collection_time',
                                                             'oversample'])
_TIMEBASE_OPTIONS_DEFAULTS = (None, None, None, 1)
TimebaseOptions.__new__.__defaults__ = _TIMEBASE_OPTIONS_DEFAULTS


class Device(object):
    """This object caches some information about the device state which cannot be queried from the driver. Please don't
    mix and match calls to this object with calls directly to the driver (or the ctypes wrapper), as this may cause
    unwanted behaviour (e.g. throwing an exception because no channels are enabled, when you enabled them yourself
    on the driver object.)"""
    def __init__(self, driver, handle):
        self.driver = driver
        self.handle = handle
        self.is_open = handle > 0

        # if a channel is missing from here, it is disabled (or in an undefined state).
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

    def _timebase_options_are_impossible(self, options):
        device_max_samples_possible = self.driver.MAX_MEMORY
        if options.no_of_samples is not None:
            if options.no_of_samples > device_max_samples_possible:
                return True
        elif options.max_time_interval is not None and options.min_collection_time is not None:
            effective_min_no_samples = math.ceil(options.min_collection_time / options.max_time_interval)
            if effective_min_no_samples > device_max_samples_possible:
                return True
        if None not in (options.no_of_samples, options.max_time_interval, options.min_collection_time):
            # if all 3 are requested, the result can be impossible.
            effective_min_no_samples = int(math.ceil(options.min_collection_time / options.max_time_interval))
            if effective_min_no_samples > options.no_of_samples:
                return True
        # Is it still possible that this device cannot handle this request, but we don't know without making calls to
        # get_timebase.
        return False

    @staticmethod
    def _validate_timebase(timebase_options, timebase_info):
        """validate whether a timebase result matches the options requested."""
        if timebase_options.max_time_interval is not None:
            if timebase_info.time_interval > timebase_options.max_time_interval:
                return False
        if timebase_options.no_of_samples is not None:
            if timebase_options.no_of_samples > timebase_info.max_samples:
                return False
        if timebase_options.min_collection_time is not None:
            if timebase_options.min_collection_time > timebase_info.max_samples * timebase_info.time_interval:
                return False
        return True

    @requires_open()
    def find_timebase(self, timebase_options):
        timebase_id = 0
        # quickly validate that the request is not impossible.
        if self._timebase_options_are_impossible(timebase_options):
            raise NoValidTimebaseForOptionsError()
        # TODO binary search?
        last_error = None
        found_one_good = False
        while True:
            try:
                timebase_info = self.driver.get_timebase(self, timebase_id, 0, timebase_options.oversample)
                found_one_good = True
                if self._validate_timebase(timebase_options, timebase_info):
                    return timebase_info
            except InvalidTimebaseError as e:
                if found_one_good:
                    # we won't find a valid timebase.
                    last_error = e
                    break
            timebase_id += 1
        args = ()
        if last_error is not None:
            args = (last_error.args[0],)
        raise NoValidTimebaseForOptionsError(*args)

    @requires_open()
    def capture_block(self, timebase_options, channel_configs=()):
        """device.capture_block(timebase_options, channel_configs)
        timebase_options: TimebaseOptions object, specifying at least 1 constraint, and optionally oversample.
        channel_configs: a collection of ChannelConfig objects. If present, will be passed to set_channels.
        """
        # set_channel:

        if channel_configs:
            self.set_channels(*channel_configs)

        if len(self._channel_ranges) == 0:
            raise NoChannelsEnabledError("We cannot capture any data if no channels are enabled.")

        # memory_segments:
        USE_SEGMENT_ID=0
        try:
            # always force the number of memory segments on the device to 1 before computing timebases for a one-off
            # block capture.
            max_samples_possible = self.driver.memory_segments(self, USE_SEGMENT_ID+1)
            if timebase_options.no_of_samples is not None and timebase_options.no_of_samples > max_samples_possible:
                raise NoValidTimebaseForOptionsError()
        except DeviceCannotSegmentMemoryError:
            pass

        # get_timebase
        timebase_info = self.find_timebase(timebase_options)

        post_trigger_samples = timebase_options.no_of_samples
        pre_trigger_samples = 0

        if post_trigger_samples is None:
            post_trigger_samples = int(math.ceil(timebase_options.min_collection_time / timebase_info.time_interval))

        self.driver.set_null_trigger(self)

        # tell the device to capture something:
        approx_time_busy = self.driver.run_block(self,
                                                 pre_trigger_samples,
                                                 post_trigger_samples,
                                                 timebase_info.timebase_id,
                                                 timebase_options.oversample,
                                                 USE_SEGMENT_ID)

        is_ready = self.driver.is_ready(self)
        while not is_ready:
            time.sleep(approx_time_busy / 5)
            is_ready = self.driver.is_ready(self)

        raw_data, overflow_warnings = self.driver.get_values(self,
                                                             self._channel_ranges.keys(),
                                                             post_trigger_samples,
                                                             USE_SEGMENT_ID)

        self.driver.stop(self)

        times = numpy.linspace(0.,
                               post_trigger_samples * timebase_info.time_interval,
                               post_trigger_samples,
                               dtype=numpy.dtype('float32'))

        voltages = {}

        max_adc = self.driver.maximum_value(self)
        for channel, raw_array in raw_data.items():
            array = raw_array.astype(numpy.dtype('float32'), casting='safe')
            factor = self._channel_ranges[channel] / max_adc
            array = array * factor
            voltages[channel] = array

        return times, voltages, overflow_warnings
