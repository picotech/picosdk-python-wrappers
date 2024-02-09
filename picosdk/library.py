#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Definition of the Library class, which is the abstract representation of a picotech device driver.
Note: Many of the functions in this class are missing: these are populated by the psN000(a).py modules, which subclass
this type and attach the missing methods.
"""

from __future__ import print_function

import sys
from ctypes import c_int16, c_int32, c_uint32, c_float, create_string_buffer, byref
from ctypes.util import find_library
import collections
import picosdk.constants as constants
import numpy

from picosdk.errors import CannotFindPicoSDKError, CannotOpenPicoSDKError, DeviceNotFoundError, \
    ArgumentOutOfRangeError, ValidRangeEnumValueNotValidForThisDevice, DeviceCannotSegmentMemoryError, \
    InvalidMemorySegmentsError, InvalidTimebaseError, InvalidTriggerParameters, InvalidCaptureParameters


from picosdk.device import Device


"""TimebaseInfo: A type for holding the particulars of a timebase configuration.
"""
TimebaseInfo = collections.namedtuple('TimebaseInfo', ['timebase_id',
                                                       'time_interval',
                                                       'time_units',
                                                       'max_samples',
                                                       'segment_id'])


def requires_device(error_message="This method requires a Device instance registered to this Library instance."):
    def check_device_decorator(method):
        def check_device_impl(self, device, *args, **kwargs):
            if not isinstance(device, Device) or device.driver != self:
                raise TypeError(error_message)
            return method(self, device, *args, **kwargs)
        return check_device_impl
    return check_device_decorator


class Library(object):
    def __init__(self, name):
        self.name = name
        self._clib = self._load()
        # ! some drivers will replace these dicts at import time, where they have different constants (notably ps2000).
        self.PICO_INFO = constants.PICO_INFO
        self.PICO_STATUS = constants.PICO_STATUS
        self.PICO_STATUS_LOOKUP = constants.PICO_STATUS_LOOKUP
        # these must be set in each driver file.
        self.PICO_CHANNEL = {}
        self.PICO_COUPLING = {}
        self.PICO_VOLTAGE_RANGE = {}

        # most series of scopes top out at 512MS.
        self.MAX_MEMORY = 2**29

        # These are set in some driver files, but not all.
        self.PICO_RATIO_MODE = {}
        self.PICO_THRESHOLD_DIRECTION = {}

    def _load(self):
        library_path = find_library(self.name)

        if library_path is None:
            env_var_name = "PATH" if sys.platform == 'win32' else "LD_LIBRARY_PATH"
            raise CannotFindPicoSDKError("PicoSDK (%s) not found, check %s" % (self.name, env_var_name))

        try:
            if sys.platform == 'win32':
                from ctypes import WinDLL
                result = WinDLL(library_path)
            else:
                from ctypes import cdll
                result = cdll.LoadLibrary(library_path)
        except OSError as e:
            raise CannotOpenPicoSDKError("PicoSDK (%s) not compatible (check 32 vs 64-bit): %s" % (self.name, e))
        return result

    def __str__(self):
        return "picosdk %s library" % self.name

    def make_symbol(self, python_name, c_name, return_type, argument_types, docstring=None):
        """Used by python wrappers for particular drivers to register C functions on the class."""
        c_function = getattr(self._clib, c_name)
        c_function.restype = return_type
        c_function.argtypes = argument_types
        if docstring is not None:
            c_function.__doc__ = docstring
        # make the functions available under *both* their original and generic names
        setattr(self, python_name, c_function)
        setattr(self, c_name, c_function)
        # AND if the function is camel case, add an "underscore-ized" version:
        if python_name.lower() != python_name:
            acc = []
            for c in python_name[1:]:
                # Be careful to exclude both digits (lower index) and lower case (higher index).
                if ord('A') <= ord(c) <= ord('Z'):
                    c = "_" + c.lower()
                acc.append(c)
            if acc[:2] == ['_', '_']:
                acc = acc[1:]
            setattr(self, "".join(acc), c_function)

    def list_units(self):
        """Returns: a list of dictionaries which identify connected devices which use this driver."""
        handles = []
        device_infos = []
        try:
            while True:
                handle = self._python_open_unit()
                device_infos.append(self._python_get_unit_info_wrapper(handle, []))
                handles.append(handle)
        except DeviceNotFoundError:
            pass

        for handle in handles:
            self._python_close_unit(handle)

        return device_infos

    def open_unit(self, serial=None, resolution=None):
        """optional arguments:
        serial: If no serial number is provided, this function opens the first device discovered.
        resolution: for some devices, you may specify a resolution as you open the device. You should retrieve this
            numeric constant from the relevant driver module.
        returns: a Device instance, which has functions on it for collecting data and using the waveform generator (if
            present).
        Note: Either use this object in a context manager, or manually call .close() on it when you are finished."""
        return Device(self, self._python_open_unit(serial=serial, resolution=resolution))

    @requires_device("close_unit requires a picosdk.device.Device instance, passed to the correct owning driver.")
    def close_unit(self, device):
        self._python_close_unit(device.handle)

    @requires_device("get_unit_info requires a picosdk.device.Device instance, passed to the correct owning driver.")
    def get_unit_info(self, device, *args):
        return self._python_get_unit_info_wrapper(device.handle, args)

    def _python_open_unit(self, serial=None, resolution=None):
        if serial is None:
            handle, status = self._python_open_any_unit(resolution)
        else:
            handle, status = self._python_open_specific_unit(serial, resolution)

        if handle < 1:
            message = ("Driver %s could find no device" % self.name) + ("s" if serial is None else
                                                                        (" matching %s" % serial))
            if status is not None:
                message += " (%s)" % constants.pico_tag(status)
            raise DeviceNotFoundError(message)

        return handle

    def _python_open_any_unit(self, resolution):
        status = None
        if len(self._open_unit.argtypes) == 3:
            if resolution is None:
                resolution = self.DEFAULT_RESOLUTION
            chandle = c_int16()
            cresolution = c_int32()
            cresolution.value = resolution
            status = self._open_unit(byref(chandle), None, cresolution)
            handle = chandle.value
        elif len(self._open_unit.argtypes) == 2:
            chandle = c_int16()
            status = self._open_unit(byref(chandle), None)
            handle = chandle.value
        else:
            handle = self._open_unit()

        return handle, status

    def _python_open_specific_unit(self, serial, resolution):
        handle = -1
        status = None
        if len(self._open_unit.argtypes) == 3:
            if resolution is None:
                resolution = self.DEFAULT_RESOLUTION
            chandle = c_int16()
            cresolution = c_int32()
            cresolution.value = resolution
            cserial = create_string_buffer(serial)
            status = self._open_unit(byref(chandle), cserial, cresolution)
            handle = chandle.value
        elif len(self._open_unit.argtypes) == 2:
            chandle = c_int16()
            cserial = create_string_buffer(serial)
            status = self._open_unit(byref(chandle), cserial)
            handle = chandle.value
        else:
            open_handles = []
            temp_handle = self._open_unit()

            while temp_handle > 0:
                this_serial = self._python_get_unit_info(temp_handle, self.PICO_INFO["PICO_BATCH_AND_SERIAL"])
                if this_serial == serial:
                    handle = temp_handle
                    break
                open_handles.append(temp_handle)
                temp_handle = self._open_unit()

            for temp_handle in open_handles:
                self._python_close_unit(temp_handle)

        return handle, status

    def _python_close_unit(self, handle):
        return self._close_unit(c_int16(handle))

    @staticmethod
    def _create_empty_string_buffer():
        try:
            return create_string_buffer("\0", 255)
        except TypeError:
            return create_string_buffer("\0".encode('utf8'), 255)

    def _python_get_unit_info(self, handle, info_type):
        string_size = 255
        info = self._create_empty_string_buffer()
        if len(self._get_unit_info.argtypes) == 4:
            info_len = self._get_unit_info(c_int16(handle), info, c_int16(string_size), c_int16(info_type))
            if info_len > 0:
                return info.value[:info_len]
        elif len(self._get_unit_info.argtypes) == 5:
            required_size = c_int16(0)
            status = self._get_unit_info(c_int16(handle),
                                         info,
                                         c_int16(string_size),
                                         byref(required_size),
                                         c_uint32(info_type))
            if status == self.PICO_STATUS['PICO_OK']:
                if required_size.value < string_size:
                    return info.value[:required_size.value]
        return ""

    def _python_get_unit_info_wrapper(self, handle, keys):
        # verify that the requested keys are valid for this driver:
        invalid_info_lines = list(set(keys) - set(self.PICO_INFO.keys()))
        if invalid_info_lines:
            raise ArgumentOutOfRangeError("%s not available for %s devices" % (",".join(invalid_info_lines), self.name))

        if not keys:
            # backwards compatible behaviour from first release of this wrapper, which works on all drivers.
            UnitInfo = collections.namedtuple('UnitInfo', ['driver', 'variant', 'serial'])
            return UnitInfo(
                driver=self,
                variant=self._python_get_unit_info(handle, self.PICO_INFO["PICO_VARIANT_INFO"]),
                serial=self._python_get_unit_info(handle, self.PICO_INFO["PICO_BATCH_AND_SERIAL"])
            )

        # make a new type here, with the relevant keys.
        UnitInfo = collections.namedtuple('UnitInfo', list(keys))

        info_lines = {}

        for line in keys:
            info_lines[line] = self._python_get_unit_info(handle, self.PICO_INFO[line])

        return UnitInfo(**info_lines)

    @requires_device("set_channel requires a picosdk.device.Device instance, passed to the correct owning driver.")
    def set_channel(self, device, channel_name='A', enabled=True, coupling='DC', range_peak=float('inf'),
                    analog_offset=None):
        """optional arguments:
        channel_name: a single channel (e.g. 'A')
        enabled: whether to enable the channel (boolean)
        coupling: string of the relevant enum member for your driver less the driver name prefix. e.g. 'DC' or 'AC'.
        range_peak: float which is the largest value you expect in the input signal. We will throw an exception if no
                    range on the device is large enough for that value.
        analog_offset: the meaning of 0 for this channel.
        return value: Max voltage of new range. Raises an exception in error cases."""

        excluded = ()
        reliably_resolved = False

        max_voltage = None

        while not reliably_resolved:
            if enabled:
                range_id, max_voltage = self._resolve_range(range_peak, excluded)
            else:
                range_id = 0
                max_voltage = None

            try:
                self._python_set_channel(device.handle,
                                         self.PICO_CHANNEL[channel_name],
                                         1 if enabled else 0,
                                         self.PICO_COUPLING[coupling],
                                         range_id,
                                         analog_offset)

                reliably_resolved = True
            except ValidRangeEnumValueNotValidForThisDevice:
                excluded += (range_id,)

        return max_voltage

    def _resolve_range(self, signal_peak, exclude=()):
        # we use >= so that someone can specify the range they want precisely.
        # we allow exclude so that if the smallest range in the header file isn't available on this device (or in this
        # configuration) we can exclude it from the collection. It should be the numerical enum constant (the key in
        # PICO_VOLTAGE_RANGE).
        possibilities = list(filter(lambda tup: tup[1] >= signal_peak and tup[0] not in exclude,
                                    self.PICO_VOLTAGE_RANGE.items()))

        if not possibilities:
            raise ArgumentOutOfRangeError("%s device doesn't support a range as wide as %sV" % (self.name, signal_peak))

        return min(possibilities, key=lambda i: i[1])

    def _python_set_channel(self, handle, channel_id, enabled, coupling_id, range_id, analog_offset):
        if len(self._set_channel.argtypes) == 5 and self._set_channel.argtypes[1] == c_int16:
            if analog_offset is not None:
                raise ArgumentOutOfRangeError("This device doesn't support analog offset")
            return_code = self._set_channel(c_int16(handle),
                                            c_int16(channel_id),
                                            c_int16(enabled),
                                            c_int16(coupling_id),
                                            c_int16(range_id))
            if return_code == 0:
                raise ValidRangeEnumValueNotValidForThisDevice("%sV is out of range for this device." % (
                    self.PICO_VOLTAGE_RANGE[range_id]))
        elif len(self._set_channel.argtypes) == 5 and self._set_channel.argtypes[1] == c_int32 or (
             len(self._set_channel.argtypes) == 6):
            status = self.PICO_STATUS['PICO_OK']
            if len(self._set_channel.argtypes) == 6:
                if analog_offset is None:
                    analog_offset = 0.0
                status = self._set_channel(c_int16(handle),
                                           c_int32(channel_id),
                                           c_int16(enabled),
                                           c_int32(coupling_id),
                                           c_int32(range_id),
                                           c_float(analog_offset))
            elif len(self._set_channel.argtypes) == 5 and self._set_channel.argtypes[1] == c_int32:
                if analog_offset is not None:
                    raise ArgumentOutOfRangeError("This device doesn't support analog offset")
                status = self._set_channel(c_int16(handle),
                                           c_int32(channel_id),
                                           c_int16(enabled),
                                           c_int16(coupling_id),
                                           c_int32(range_id))
            if status != self.PICO_STATUS['PICO_OK']:
                if status == self.PICO_STATUS['PICO_INVALID_VOLTAGE_RANGE']:
                    raise ValidRangeEnumValueNotValidForThisDevice("%sV is out of range for this device." % (
                        self.PICO_VOLTAGE_RANGE[range_id]))
                if status == self.PICO_STATUS['PICO_INVALID_CHANNEL'] and not enabled:
                    # don't throw errors if the user tried to disable a missing channel.
                    return
                raise ArgumentOutOfRangeError("problem configuring channel (%s)" % constants.pico_tag(status))

        else:
            raise NotImplementedError("not done other driver types yet")

    @requires_device("memory_segments requires a picosdk.device.Device instance, passed to the correct owning driver.")
    def memory_segments(self, device, number_segments):
        if not hasattr(self, '_memory_segments'):
            raise DeviceCannotSegmentMemoryError()
        max_samples = c_int32(0)
        status = self._memory_segments(c_int16(device.handle), c_uint32(number_segments), byref(max_samples))
        if status != self.PICO_STATUS['PICO_OK']:
            raise InvalidMemorySegmentsError("could not segment the device memory into (%s) segments (%s)" % (
                                              number_segments, constants.pico_tag(status)))
        return max_samples

    @requires_device("get_timebase requires a picosdk.device.Device instance, passed to the correct owning driver.")
    def get_timebase(self, device, timebase_id, no_of_samples, oversample=1, segment_index=0):
        """query the device about what time precision modes it can handle.
        note: the driver returns the timebase in nanoseconds, this function converts that into SI units (seconds)"""
        nanoseconds_result = self._python_get_timebase(device.handle,
                                                       timebase_id,
                                                       no_of_samples,
                                                       oversample,
                                                       segment_index)

        return TimebaseInfo(nanoseconds_result.timebase_id,
                            nanoseconds_result.time_interval * 1.e-9,
                            nanoseconds_result.time_units,
                            nanoseconds_result.max_samples,
                            nanoseconds_result.segment_id)

    def _python_get_timebase(self, handle, timebase_id, no_of_samples, oversample, segment_index):
        # We use get_timebase on ps2000 and ps3000 and parse the nanoseconds-int into a float.
        # on other drivers, we use get_timebase2, which gives us a float in the first place.
        if len(self._get_timebase.argtypes) == 7 and self._get_timebase.argtypes[1] == c_int16:
            time_interval = c_int32(0)
            time_units = c_int16(0)
            max_samples = c_int32(0)
            return_code = self._get_timebase(c_int16(handle),
                                             c_int16(timebase_id),
                                             c_int32(no_of_samples),
                                             byref(time_interval),
                                             byref(time_units),
                                             c_int16(oversample),
                                             byref(max_samples))
            if return_code == 0:
                raise InvalidTimebaseError()

            return TimebaseInfo(timebase_id, float(time_interval.value), time_units.value, max_samples.value, None)
        elif hasattr(self, '_get_timebase2') and (
                     len(self._get_timebase2.argtypes) == 7 and self._get_timebase2.argtypes[1] == c_uint32):
            time_interval = c_float(0.0)
            max_samples = c_int32(0)
            status = self._get_timebase2(c_int16(handle),
                                         c_uint32(timebase_id),
                                         c_int32(no_of_samples),
                                         byref(time_interval),
                                         c_int16(oversample),
                                         byref(max_samples),
                                         c_uint32(segment_index))
            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidTimebaseError("get_timebase2 failed (%s)" % constants.pico_tag(status))

            return TimebaseInfo(timebase_id, time_interval.value, None, max_samples.value, segment_index)
        else:
            raise NotImplementedError("not done other driver types yet")

    @requires_device()
    def set_null_trigger(self, device):
        auto_trigger_after_millis = 1
        if hasattr(self, '_set_trigger') and len(self._set_trigger.argtypes) == 6:
            PS2000_NONE = 5
            return_code = self._set_trigger(c_int16(device.handle),
                                            c_int16(PS2000_NONE),
                                            c_int16(0),
                                            c_int16(0),
                                            c_int16(0),
                                            c_int16(auto_trigger_after_millis))
            if return_code == 0:
                raise InvalidTriggerParameters()
        elif hasattr(self, '_set_simple_trigger') and len(self._set_simple_trigger.argtypes) == 7:
            enabled = False
            status = self._set_simple_trigger(c_int16(device.handle),
                                              c_int16(int(enabled)),
                                              c_int32(self.PICO_CHANNEL['A']),
                                              c_int16(0),
                                              c_int32(self.PICO_THRESHOLD_DIRECTION['NONE']),
                                              c_uint32(0),
                                              c_int16(auto_trigger_after_millis))
            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidTriggerParameters("set_simple_trigger failed (%s)" % constants.pico_tag(status))
        else:
            raise NotImplementedError("not done other driver types yet")

    @requires_device()
    def run_block(self, device, pre_trigger_samples, post_trigger_samples, timebase_id, oversample=1, segment_index=0):
        """tell the device to arm any triggers and start capturing in block mode now.
        returns: the approximate time (in seconds) which the device will take to capture with these settings."""
        return self._python_run_block(device.handle,
                                      pre_trigger_samples,
                                      post_trigger_samples,
                                      timebase_id,
                                      oversample,
                                      segment_index)

    def _python_run_block(self, handle, pre_samples, post_samples, timebase_id, oversample, segment_index):
        time_indisposed = c_int32(0)
        if len(self._run_block.argtypes) == 5:
            return_code = self._run_block(c_int16(handle),
                                          c_int32(pre_samples + post_samples),
                                          c_int16(timebase_id),
                                          c_int16(oversample),
                                          byref(time_indisposed))
            if return_code == 0:
                raise InvalidCaptureParameters()
        elif len(self._run_block.argtypes) == 9:
            status = self._run_block(c_int16(handle),
                                     c_int32(pre_samples),
                                     c_int32(post_samples),
                                     c_uint32(timebase_id),
                                     c_int16(oversample),
                                     byref(time_indisposed),
                                     c_uint32(segment_index),
                                     None,
                                     None)
            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidCaptureParameters("run_block failed (%s)" % constants.pico_tag(status))
        else:
            raise NotImplementedError("not done other driver types yet")

        return float(time_indisposed.value) * 0.001

    @requires_device()
    def is_ready(self, device):
        """poll this function to find out when block mode is ready or has triggered.
        returns: True if data is ready, False otherwise."""
        if hasattr(self, '_ready') and len(self._ready.argtypes) == 1:
            return_code = self._ready(c_int16(device.handle))
            return bool(return_code)
        elif hasattr(self, '_is_ready') and len(self._is_ready.argtypes) == 2:
            is_ready = c_int16(0)
            status = self._is_ready(c_int16(device.handle), byref(is_ready))
            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidCaptureParameters("is_ready failed (%s)" % constants.pico_tag(status))
            return bool(is_ready.value)
        else:
            raise NotImplementedError("not done other driver types yet")

    @requires_device()
    def maximum_value(self, device):
        if not hasattr(self, '_maximum_value'):
            return (2**15)-1
        max_adc = c_int16(0)
        self._maximum_value(c_int16(device.handle), byref(max_adc))
        return max_adc.value

    @requires_device()
    def get_values(self, device, active_channels, num_samples, segment_index=0):
        # Initialise buffers to hold the data:
        results = {channel: numpy.empty(num_samples, numpy.dtype('int16')) for channel in active_channels}

        overflow = c_int16(0)

        if len(self._get_values.argtypes) == 7 and self._get_timebase.argtypes[1] == c_int16:
            inputs = {k: None for k in 'ABCD'}
            for k, arr in results.items():
                inputs[k] = arr.ctypes.data
            return_code = self._get_values(c_int16(device.handle),
                                           inputs['A'],
                                           inputs['B'],
                                           inputs['C'],
                                           inputs['D'],
                                           byref(overflow),
                                           c_int32(num_samples))
            if return_code == 0:
                raise InvalidCaptureParameters()
        elif len(self._get_values.argtypes) == 7 and self._get_timebase.argtypes[1] == c_uint32:
            # For this function pattern, we first call a function (self._set_data_buffer) to register each buffer. Then,
            # we can call self._get_values to actually populate them.
            for channel, array in results.items():
                status = self._set_data_buffer(c_int16(device.handle),
                                               c_int32(self.PICO_CHANNEL[channel]),
                                               array.ctypes.data,
                                               c_int32(num_samples),
                                               c_uint32(segment_index),
                                               c_int32(self.PICO_RATIO_MODE['NONE']))
                if status != self.PICO_STATUS['PICO_OK']:
                    raise InvalidCaptureParameters("set_data_buffer failed (%s)" % constants.pico_tag(status))

            samples_collected = c_uint32(num_samples)
            status = self._get_values(c_int16(device.handle),
                                      c_uint32(0),
                                      byref(samples_collected),
                                      c_uint32(1),
                                      c_int32(self.PICO_RATIO_MODE['NONE']),
                                      c_uint32(segment_index),
                                      byref(overflow))
            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidCaptureParameters("get_values failed (%s)" % constants.pico_tag(status))

        overflow_warning = {}
        if overflow.value:
            for channel in results.keys():
                if overflow.value & (1 >> self.PICO_CHANNEL[channel]):
                    overflow_warning[channel] = True

        return results, overflow_warning

    @requires_device()
    def stop(self, device):
        if self._stop.restype == c_int16:
            return_code = self._stop(c_int16(device.handle))
            if isinstance(return_code, c_int16):
                if return_code == 0:
                    raise InvalidCaptureParameters()
        else:
            status = self._stop(c_int16(device.handle))
            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidCaptureParameters("stop failed (%s)" % constants.pico_tag(status))
