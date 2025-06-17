#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
Definition of the Library class, which is the abstract representation of a picotech device driver.
Note: Many of the functions in this class are missing: these are populated by the psN000(a).py modules, which subclass
this type and attach the missing methods.
"""

from __future__ import print_function

import json
import sys
from ctypes import c_int16, c_int32, c_uint32, c_float, c_void_p, create_string_buffer, byref
from ctypes.util import find_library
import collections
import time
import gc
import picosdk.constants as constants
from base64 import b64encode
import numpy
from numpy.lib.format import dtype_to_descr

from picosdk.errors import PicoError, CannotFindPicoSDKError, CannotOpenPicoSDKError, DeviceNotFoundError, \
    ArgumentOutOfRangeError, ValidRangeEnumValueNotValidForThisDevice, DeviceCannotSegmentMemoryError, \
    InvalidMemorySegmentsError, InvalidTimebaseError, InvalidTriggerParameters, InvalidCaptureParameters


from picosdk.device import Device


DEFAULT_PROBE_ATTENUATION = {
    'A': 10,
    'B': 10,
    'C': 10,
    'D': 10,
    'E': 10,
    'F': 10,
    'G': 10,
    'H': 10,
}

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


def voltage_to_logic_level(voltage):
    """Convert a voltage value into logic level for digital channels.

    Range: –32767 (–5 V) to 32767 (5 V).

    Args:
        voltage (float): Voltage in volts.

    Returns:
        int: The calculated logic level count.
    """
    clamped_voltage = min(max(-5, voltage), 5)
    logic_level = int((clamped_voltage) * (32767 / 5))
    return logic_level


def split_mso_data_fast(data_length, data):
    """Return a tuple of 8 arrays, each of which is the values over time of a different digital channel.

    The tuple contains the channels in order (D7, D6, D5, ... D0) or equivalently (D15, D14, D13, ... D8).

    Args:
        data_length (c_int32): The length of the data array.
        data (c_int16 array): The data array containing the digital port values.
    """
    num_samples = data_length.value
    # Makes an array for each digital channel
    buffer_binary_dj = tuple(numpy.empty(num_samples, dtype=numpy.uint8) for _ in range(8))
    # Splits out the individual bits from the port into the binary values for each digital channel/pin.
    for i in range(num_samples):
        for j in range(8):
            buffer_binary_dj[j][i] = 1 if (data[i] & (1 << (7-j))) else 0

    return buffer_binary_dj


def adc_to_mv(buffer_adc, channel_range, max_adc):
    """Convert a buffer of raw adc count values into millivolts.

    Args:
        buffer_adc (c_short_Array): The buffer of ADC count values.
        channel_range (int): The channel range in V.
        max_adc (int): The maximum ADC count.

    Returns:
        list: The buffer in millivolts.
    """
    buffer_mv = [(x * channel_range * 1000) / max_adc for x in buffer_adc]
    return buffer_mv


def mv_to_adc(millivolts, channel_range, max_adc):
    """Convert a voltage value into an ADC count.

    Args:
        millivolts (float): Voltage in millivolts.
        channel_range (int): The channel range in V.
        max_adc (c_int16): The maximum ADC count.

    Returns:
        int: The ADC count.
    """
    adc_value = round((millivolts * max_adc) / (channel_range * 1000))
    return adc_value


class NumpyEncoder(json.JSONEncoder):
    """Module specific json encoder class."""
    def default(self, o):
        """Default json encoder override.

        Code inspired from https://github.com/Crimson-Crow/json-numpy/blob/main/json_numpy.py
        """
        if isinstance(o, (numpy.ndarray, numpy.generic)):
            return {
                "__numpy__": b64encode(o.data if o.flags.c_contiguous else o.tobytes()).decode(),
                "dtype": dtype_to_descr(o.dtype),
                "shape": o.shape,
            }
        return super().default(o)


class SingletonScopeDataDict(dict):
    """SingletonScopeDataDict is a singleton dictionary object for sharing picoscope data between multiple classes.

    It handles both analog and digital data with uniform access patterns:
    - Analog channels are accessed by their letter (e.g. 'A', 'B', 'C', 'D')
    - Digital channels are accessed as 'D0'-'D15' (MSB channel D15 to LSB channel D0)
    - Digital ports are accessed by their number (e.g. 0, 1)
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Create new singleton dictionary instance or return existing one."""
        if cls._instance is None:
            cls._instance = super(SingletonScopeDataDict, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def clean_dict(self):
        """Remove all data from the singleton dictionary and run garbage collection."""
        self.clear()
        gc.collect()

    def __getitem__(self, key: str):
        """Get data with uniform access pattern for analog and digital channels.

        Args:
            key: Channel identifier:
                - 'A', 'B', 'C', 'D' for analog channels
                - 'D0'-'D15' for digital channels
                - 0-3 for digital ports

        Returns:
            numpy array containing the channel data

        Raises:
            KeyError: If channel doesn't exist
            ValueError: If digital channel number is invalid
        """
        # Handle digital channels (D0-D15)
        if isinstance(key, str) and key.upper().startswith('D'):
            try:
                digital_number = int(key[1:])
                if not 0 <= digital_number <= 15:
                    raise ValueError(f"Digital channel number must be 0-15, got {digital_number}")

                # Calculate which port and bit
                port_number = digital_number // 8  # Port 0 = D0-D7, Port 1 = D8-D15
                bit_number = 7 - (digital_number % 8)  # Reverse bit order within port

                # Get port data
                port_data = super().__getitem__(port_number)

                # Extract individual channel data
                return (port_data >> bit_number) & 0x1

            except (IndexError, ValueError) as e:
                raise ValueError(f"Invalid digital channel {key}: {str(e)}")

        # Handle direct port access (0-3) or analog channels
        return super().__getitem__(key)

    def set_port_data(self, port_number: int, data: numpy.ndarray):
        """Set digital port data.

        Args:
            port_number: Digital port number (0-3)
            data: Numpy array containing port data
        """
        self[port_number] = data


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

        # 'find_library' fails in Cygwin.
        if not sys.platform == 'cygwin':
            if library_path is None:
                env_var_name = "PATH" if sys.platform == 'win32' else "LD_LIBRARY_PATH"
                raise CannotFindPicoSDKError("PicoSDK (%s) not found, check %s" % (self.name, env_var_name))

        try:
            if sys.platform == 'win32':
                from ctypes import WinDLL
                result = WinDLL(library_path)
            elif sys.platform == 'cygwin':
                from ctypes import CDLL
                library_path = self.name
                result = CDLL(library_path + ".dll")
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
            python_name = python_name.lstrip('_')
            for c in python_name:
                # Be careful to exclude both digits (lower index) and lower case (higher index).
                if ord('A') <= ord(c) <= ord('Z'):
                    c = "_" + c.lower()
                acc.append(c)
            new_python_name = "".join(acc)
            if not new_python_name.startswith('_'):
                new_python_name = "_" + new_python_name
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
                    range on the device is large enough for that value. (in Voltage)
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

    @requires_device("set_digital_port requires a picosdk.device.Device instance, passed to the correct owning driver.")
    def set_digital_port(self, device, port_number=0, enabled=True, voltage_level=1.8):
        """Set the digital port

        Args:
            port_number (int): identifies the port for digital data. (e.g. 0 for digital channels 0-7)
            enabled (bool): whether or not to enable the channel (boolean)
            voltage_level (float): the voltage at which the state transitions between 0 and 1. Range: –5.0 to 5.0 (V).
        Raises:
            NotImplementedError: This device doesn't support digital ports.
            PicoError: set_digital_port failed
        """
        if hasattr(self, '_set_digital_port') and len(self._set_digital_port.argtypes) == 4:
            logic_level = voltage_to_logic_level(voltage_level)
            digital_ports = getattr(self, self.name.upper() + '_DIGITAL_PORT', None)
            if not digital_ports:
                raise NotImplementedError("This device doesn't support digital ports")
            port_id = digital_ports[self.name.upper() + "_DIGITAL_PORT" + str(port_number)]
            args = (device.handle, port_id, enabled, logic_level)
            converted_args = self._convert_args(self._set_digital_port, args)
            status = self._set_digital_port(*converted_args)
            if status != self.PICO_STATUS['PICO_OK']:
                raise PicoError(
                    f"set_digital_port failed ({constants.pico_tag(status)})")
        else:
            raise NotImplementedError("This device doesn't support digital ports or is not implemented yet")

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

            args = (handle, channel_id, enabled, coupling_id, range_id)
            converted_args = self._convert_args(self._set_channel, args)
            return_code = self._set_channel(*converted_args)

            if return_code == 0:
                raise ValidRangeEnumValueNotValidForThisDevice(
                    f"{self.PICO_VOLTAGE_RANGE[range_id]}V is out of range for this device.")
        elif len(self._set_channel.argtypes) == 5 and self._set_channel.argtypes[1] == c_int32 or (
             len(self._set_channel.argtypes) == 6):
            status = self.PICO_STATUS['PICO_OK']
            if len(self._set_channel.argtypes) == 6:
                if analog_offset is None:
                    analog_offset = 0.0
                args = (handle, channel_id, enabled, coupling_id, range_id, analog_offset)
                converted_args = self._convert_args(self._set_channel, args)
                status = self._set_channel(*converted_args)

            elif len(self._set_channel.argtypes) == 5 and self._set_channel.argtypes[1] == c_int32:
                if analog_offset is not None:
                    raise ArgumentOutOfRangeError("This device doesn't support analog offset")
                args = (handle, channel_id, enabled, coupling_id, range_id)
                converted_args = self._convert_args(self._set_channel, args)
                status = self._set_channel(*converted_args)

            if status != self.PICO_STATUS['PICO_OK']:
                if status == self.PICO_STATUS['PICO_INVALID_VOLTAGE_RANGE']:
                    raise ValidRangeEnumValueNotValidForThisDevice(
                        f"{self.PICO_VOLTAGE_RANGE[range_id]}V is out of range for this device.")
                if status == self.PICO_STATUS['PICO_INVALID_CHANNEL'] and not enabled:
                    # don't throw errors if the user tried to disable a missing channel.
                    return
                raise ArgumentOutOfRangeError(f"problem configuring channel ({constants.pico_tag(status)})")
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

            args = (handle, timebase_id, no_of_samples, time_interval,
                   time_units, oversample, max_samples)
            converted_args = self._convert_args(self._get_timebase, args)
            return_code = self._get_timebase(*converted_args)

            if return_code == 0:
                raise InvalidTimebaseError()

            return TimebaseInfo(timebase_id, float(time_interval.value), time_units.value, max_samples.value, None)
        elif hasattr(self, '_get_timebase2') and self._get_timebase2.argtypes[1] == c_uint32:
            time_interval = c_float(0.0)
            max_samples = c_int32(0)
            if len(self._get_timebase2.argtypes) == 7:
                args = (handle, timebase_id, no_of_samples, time_interval,
                        oversample, max_samples, segment_index)
                converted_args = self._convert_args(self._get_timebase2, args)
            elif len(self._get_timebase2.argtypes) == 6:
                args = (handle, timebase_id, no_of_samples, time_interval, max_samples, segment_index)
                converted_args = self._convert_args(self._get_timebase2, args)
            else:
                raise NotImplementedError("_get_timebase2 is not implemented for this driver yet")
            status = self._get_timebase2(*converted_args)

            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidTimebaseError(f"get_timebase2 failed ({constants.pico_tag(status)})")

            return TimebaseInfo(timebase_id, time_interval.value, None, max_samples.value, segment_index)
        else:
            raise NotImplementedError("_get_timebase2 or _get_timebase is not implemented for this driver yet")

    @requires_device()
    def set_null_trigger(self, device, channel="A"):
        auto_trigger_after_millis = 1
        if hasattr(self, '_set_trigger') and len(self._set_trigger.argtypes) == 6:
            PS2000_NONE = 5
            args = (device.handle, PS2000_NONE, 0, 0, 0, auto_trigger_after_millis)
            converted_args = self._convert_args(self._set_trigger, args)
            return_code = self._set_trigger(*converted_args)

            if return_code == 0:
                raise InvalidTriggerParameters()
        elif hasattr(self, '_set_simple_trigger') and len(self._set_simple_trigger.argtypes) == 7:
            threshold_direction_id = None
            if self.PICO_THRESHOLD_DIRECTION:
                threshold_direction_id = self.PICO_THRESHOLD_DIRECTION['NONE']
            else:
                threshold_directions = getattr(self, self.name.upper() + '_THRESHOLD_DIRECTION', None)
                if threshold_directions:
                    threshold_direction_id = threshold_directions[self.name.upper() + '_NONE']
                else:
                    raise NotImplementedError("This device doesn't support threshold direction")
            args = (device.handle, False, self.PICO_CHANNEL[channel], 0,
                   threshold_direction_id, 0, auto_trigger_after_millis)
            converted_args = self._convert_args(self._set_simple_trigger, args)
            status = self._set_simple_trigger(*converted_args)

            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidTriggerParameters(f"set_simple_trigger failed ({constants.pico_tag(status)})")
        else:
            raise NotImplementedError("This device doesn't support set_null_trigger (yet)")

    @requires_device()
    def set_simple_trigger(self, device, max_voltage, max_adc=None, enable=True, channel="A", threshold_mv=500,
                           direction="FALLING", delay=0, auto_trigger_ms=1000):
        """Set a simple trigger for a channel

        Args:
            device (picosdk.device.Device): The device instance
            max_voltage (int/float): The maximum voltage of the range used by the channel. (obtained from `set_channel`)
            max_adc (int): Maximum ADC value for the device (if None, obtained via `maximum_value`)
            enable (bool): False to disable the trigger, True to enable it
            channel (str): The channel on which to trigger
            threshold_mv (int): The threshold in millivolts at which the trigger will fire.
            direction (str): The direction in which the signal must move to cause a trigger.
            delay (int): The time (sample periods) between the trigger occurring and the first sample.
            auto_trigger_ms (int): The number of milliseconds the device will wait if no trigger occurs.
                If this is set to zero, the scope device will wait indefinitely for a trigger.
        """
        if hasattr(self, '_set_simple_trigger') and len(self._set_simple_trigger.argtypes) == 7:
            if not max_adc:
                max_adc = self.maximum_value(device)
            adc_threshold = mv_to_adc(threshold_mv, max_voltage, max_adc)
            threshold_direction_id = None
            if self.PICO_THRESHOLD_DIRECTION:
                threshold_direction_id = self.PICO_THRESHOLD_DIRECTION[direction]
            else:
                threshold_directions = getattr(self, self.name.upper() + '_THRESHOLD_DIRECTION', None)
                if threshold_directions:
                    threshold_direction_id = threshold_directions[self.name.upper() + f'_{direction.upper()}']
                else:
                    raise NotImplementedError("This device doesn't support threshold direction")

            args = (device.handle, enable, self.PICO_CHANNEL[channel], adc_threshold,
                   threshold_direction_id, delay, auto_trigger_ms)
            converted_args = self._convert_args(self._set_simple_trigger, args)
            status = self._set_simple_trigger(*converted_args)

            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidTriggerParameters(f"set_simple_trigger failed ({constants.pico_tag(status)})")
        else:
            raise NotImplementedError("This device doesn't support set_simple_trigger (yet)")


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

    def _python_run_block(self, handle, pre_trigger_samples, post_trigger_samples, timebase_id, oversample,
                          segment_index):
        time_indisposed = c_int32(0)
        if len(self._run_block.argtypes) == 5:
            args = (handle, pre_trigger_samples + post_trigger_samples, timebase_id,
                   oversample, time_indisposed)
            converted_args = self._convert_args(self._run_block, args)
            return_code = self._run_block(*converted_args)

            if return_code == 0:
                raise InvalidCaptureParameters()
        elif len(self._run_block.argtypes) == 8:
            args = (handle, pre_trigger_samples, post_trigger_samples, timebase_id,
                    time_indisposed, segment_index, None, None)
            converted_args = self._convert_args(self._run_block, args)
            status = self._run_block(*converted_args)

            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidCaptureParameters(f"run_block failed ({constants.pico_tag(status)})")
        elif len(self._run_block.argtypes) == 9:
            args = (handle, pre_trigger_samples, post_trigger_samples, timebase_id,
                   oversample, time_indisposed, segment_index, None, None)
            converted_args = self._convert_args(self._run_block, args)
            status = self._run_block(*converted_args)

            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidCaptureParameters(f"run_block failed ({constants.pico_tag(status)})")
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
    def stop_block_capture(self, device, timeout_minutes=5):
        """Poll the driver to see if it has finished collecting the requested samples.

        Args:
            timeout_minutes (int/float): The timeout in minutes. If the time exceeds the timeout, the poll stops.
        """
        if timeout_minutes < 0:
            raise ArgumentOutOfRangeError("timeout_minutes must be non-negative.")
        timeout = time.time() + timeout_minutes*60
        while not self.is_ready(device):
            if time.time() > timeout:
                break

    @requires_device()
    def maximum_value(self, device):
        """Get the maximum ADC value for this device."""
        if not hasattr(self, '_maximum_value'):
            return (2**15)-1
        max_adc = c_int16(0)
        args = (device.handle, max_adc)
        converted_args = self._convert_args(self._maximum_value, args)
        self._maximum_value(*converted_args)
        return max_adc.value

    @requires_device()
    def set_data_buffer(self, device, channel_or_port, buffer_length, segment_index=0, mode='NONE'):
        """Set the data buffer for a specific channel.

        Args:
            device: Device instance
            channel_or_port: Channel (e.g. 'A', 'B') or digital port (e.g. 0, 1) to set data for
            buffer_length: The size of the buffer array (equal to no_of_samples)
            segment_index: The number of the memory segment to be used (default is 0)
            mode: The ratio mode to be used (default is 'NONE')

        Raises:
            ArgumentOutOfRangeError: If parameters are invalid for device
        """
        if not hasattr(self, '_set_data_buffer'):
            raise NotImplementedError("This device doesn't support setting data buffers")
        if len(self._set_data_buffer.argtypes) != 6:
            raise NotImplementedError("set_data_buffer is not implemented for this driver")
        if isinstance(channel_or_port, str) and channel_or_port.upper() in self.PICO_CHANNEL:
            id = self.PICO_CHANNEL[channel_or_port]
        else:
            try:
                port_num = int(channel_or_port)
                digital_ports = getattr(self, self.name.upper() + '_DIGITAL_PORT', None)
                if digital_ports:
                    digital_port = self.name.upper() + '_DIGITAL_PORT' + str(port_num)
                    if digital_port not in digital_ports:
                        raise ArgumentOutOfRangeError(f"Invalid digital port number {port_num}")
                    id = digital_ports[digital_port]
            except ValueError:
                raise ArgumentOutOfRangeError(f"Invalid digital port number {port_num}")

        if mode not in self.PICO_RATIO_MODE:
            raise ArgumentOutOfRangeError(f"Invalid ratio mode '{mode}' for {self.name} driver"
                                        "or PICO_RATIO_MODE doesn't exist for this driver")
        buffer = (c_int16 * buffer_length)()
        args = (device.handle, id, buffer, buffer_length, segment_index, self.PICO_RATIO_MODE[mode])
        converted_args = self._convert_args(self._set_data_buffer, args)
        status = self._set_data_buffer(*converted_args)

        if status != self.PICO_STATUS['PICO_OK']:
            raise ArgumentOutOfRangeError(f"set_data_buffer failed ({constants.pico_tag(status)})")

        return buffer

    @requires_device()
    def get_values(self, device, buffers, samples, time_interval_sec, max_voltage={}, start_index=0, downsample_ratio=0,
                   downsample_ratio_mode="NONE", segment_index=0, output_dir=".", filename="data", save_to_file=False,
                   probe_attenuation=DEFAULT_PROBE_ATTENUATION):
        """Get stored data values from the scope and store it in a clean SingletonScopeDataDict object.

        This function is used after data collection has stopped. It gets the stored data from the scope, with or
        without downsampling, starting at the specified sample number.

        The returned captured data is converted to mV.

        Args:
            device (picosdk.device.Device): Device instance
            buffers (dict): Dictionary of buffers where the data will be stored. The keys are channel names or port numbers,
                            and the values are numpy arrays.
            samples (int): The number of samples to retrieve from the scope.
            time_interval_sec (float): The time interval between samples in seconds. (obtained from get_timebase)
            max_voltage (dict): The maximum voltage of the range used per channel. (obtained from set_channel)
            start_index (int): A zero-based index that indicates the start point for data collection. It is measured in
                               sample intervals from the start of the buffer.
            downsample_ratio (int): The downsampling factor that will be applied to the raw data.
            downsample_ratio_mode (str): Which downsampling mode to use.
            segment_index (int): Memory segment index
            output_dir (str): The output directory where the json file will be saved.
            filename (str): The name of the json file where the data will be stored
            save_to_file (bool): True if the data has to be saved to a file on the disk, False otherwise
            probe_attenuation (dict): The attenuation factor of the probe used per the channel (1 or 10).

        Returns:
            Tuple of (captured data including time, overflow warnings)
        """
        scope_data = SingletonScopeDataDict()
        scope_data.clean_dict()
        overflow = c_int16(0)
        no_of_samples = c_uint32(samples)

        if len(self._get_values.argtypes) == 7:
            args = (device.handle, start_index, no_of_samples, downsample_ratio,
                    self.PICO_RATIO_MODE[downsample_ratio_mode], segment_index, overflow)
            converted_args = self._convert_args(self._get_values, args)
            status = self._get_values(*converted_args)

            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidCaptureParameters(f"get_values failed ({constants.pico_tag(status)})")
        else:
            raise NotImplementedError("not done other driver types yet")

        num_samples_retrieved = no_of_samples.value
        for channel, arr in buffers.items():
            data = arr[:num_samples_retrieved]
            if isinstance(channel, int) or channel.isnumeric():
                scope_data[channel] = numpy.asarray(split_mso_data_fast(no_of_samples, data))
            else:
                scope_data[channel] = numpy.array(adc_to_mv(data, max_voltage[channel],
                                                            self.maximum_value(device))) * probe_attenuation[channel]

        time_sec = numpy.linspace(0,
                                  (samples - 1) * time_interval_sec,
                                  num_samples_retrieved)
        scope_data["time"] = numpy.array(time_sec)

        if save_to_file:
            with open(f"{output_dir}/{filename}.json", "w", encoding="utf-8") as json_file:
                json.dump(scope_data, json_file, indent=4, cls=NumpyEncoder)

        overflow_warning = {}
        if overflow.value:
            for channel in buffers.keys():
                if overflow.value & (1 >> self.PICO_CHANNEL[channel]):
                    overflow_warning[channel] = True

        return scope_data, overflow_warning

    @requires_device()
    def set_and_load_data(self, device, active_sources, buffer_length, time_interval_sec, max_voltage={},
                    segment_index=0, ratio_mode='NONE', start_index=0,
                    downsample_ratio=0, downsample_ratio_mode="NONE", probe_attenuation=DEFAULT_PROBE_ATTENUATION,
                    output_dir=".", filename="data", save_to_file=False):
        """Load values from the device.

        Combines set_data_buffer and get_values to load values from the device.

        Args:
            device (picosdk.device.Device): Device instance
            active_sources (lsit[str/int]): List of active channels and/or ports
            buffer_length: The size of the buffer array (equal to the number of samples)
            time_interval_sec (float): The time interval between samples in seconds. (obtained from get_timebase)
            max_voltage (dict): The maximum voltage of the range used per channel. (obtained from set_channel)
            segment_index (int): Memory segment index
            ratio_mode: The ratio mode to be used (default is 'NONE')
            start_index (int): A zero-based index that indicates the start point for data collection. It is measured in
                sample intervals from the start of the buffer.
            downsample_ratio (int): The downsampling factor that will be applied to the raw data.
            downsample_ratio_mode (str): Which downsampling mode to use.
            probe_attenuation (dict): The attenuation factor of the probe used per the channel (1 or 10).
            output_dir (str): The output directory where the json file will be saved.
            filename (str): The name of the json file where the data will be stored
            save_to_file (bool): True if the data has to be saved to a file on the disk, False otherwise

        Returns:
            Tuple of (captured data including time, overflow warnings)
        """
        buffers = {}
        for source in active_sources:
            buffers[source] = self.set_data_buffer(device, source, buffer_length, segment_index, ratio_mode)

        return self.get_values(device, buffers, buffer_length, time_interval_sec, max_voltage, start_index,
                               downsample_ratio, downsample_ratio_mode, segment_index, output_dir, filename,
                               save_to_file, probe_attenuation)

    @requires_device("set_trigger_channel_properties requires a picosdk.device.Device instance, passed to the correct owning driver.")
    def set_trigger_channel_properties(self, device, threshold_upper, threshold_upper_hysteresis, threshold_lower,
                                       threshold_lower_hysteresis, channel, threshold_mode, aux_output_enable,
                                       auto_trigger_milliseconds):
        """Set the trigger channel properties for the device.

        Args:
            device: Device instance
            threshold_upper: Upper threshold in ADC counts
            threshold_upper_hysteresis: Hysteresis for upper threshold in ADC counts
            threshold_lower: Lower threshold in ADC counts
            threshold_lower_hysteresis: Hysteresis for lower threshold in ADC counts
            channel: Channel to set properties for (e.g. 'A', 'B', 'C', 'D')
            threshold_mode: Threshold mode (e.g. "LEVEL", "WINDOW")
            aux_output_enable: Enable auxiliary output (boolean) (Not used in eg. ps2000a, ps3000a, ps4000a)
            auto_trigger_milliseconds: The number of milliseconds for which the scope device will wait for a trigger
                before timing out. If set to zero, the scope device will wait indefinitely for a trigger

        Returns:
            None

        Raises:
            ArgumentOutOfRangeError: If parameters are invalid for device
        """
        if hasattr(self, '_set_trigger_channel_properties'):
            args = (device.handle, threshold_upper, threshold_upper_hysteresis,
                   threshold_lower, threshold_lower_hysteresis,
                   self.PICO_CHANNEL[channel], self.PICO_THRESHOLD_DIRECTION[threshold_mode],
                   aux_output_enable, auto_trigger_milliseconds)
            converted_args = self._convert_args(self._set_trigger_channel_properties, args)
            status = self._set_trigger_channel_properties(*converted_args)

            if status != self.PICO_STATUS['PICO_OK']:
                raise PicoError(f"set_trigger_channel_properties failed ({constants.pico_tag(status)})")
        else:
            raise NotImplementedError("This device does not support setting trigger channel properties.")

    @requires_device()
    def stop(self, device):
        """Stop data capture."""
        args = (device.handle,)
        converted_args = self._convert_args(self._stop, args)

        if self._stop.restype == c_int16:
            return_code = self._stop(*converted_args)
            if isinstance(return_code, c_int16) and return_code == 0:
                raise InvalidCaptureParameters()
        else:
            status = self._stop(*converted_args)
            if status != self.PICO_STATUS['PICO_OK']:
                raise InvalidCaptureParameters(f"stop failed ({constants.pico_tag(status)})")

    @requires_device()
    def set_sig_gen_built_in(self, device, offset_voltage=0, pk_to_pk=2000000, wave_type="SINE",
                             start_frequency=10000, stop_frequency=10000, increment=0,
                             dwell_time=1, sweep_type="UP", operation='ES_OFF', shots=0, sweeps=0,
                             trigger_type="RISING", trigger_source="NONE", ext_in_threshold=1):
        """Set up the signal generator to output a built-in waveform.

        Args:
            device: Device instance
            offset_voltage: Offset voltage in microvolts (default 0)
            pk_to_pk: Peak-to-peak voltage in microvolts (default 2000000)
            wave_type: Type of waveform (e.g. "SINE", "SQUARE", "TRIANGLE")
            start_frequency: Start frequency in Hz (default 1000.0)
            stop_frequency: Stop frequency in Hz (default 1000.0)
            increment: Frequency increment in Hz (default 0.0)
            dwell_time: Time at each frequency in seconds (default 1.0)
            sweep_type: Sweep type (e.g. "UP", "DOWN", "UPDOWN")
            operation: Configures the white noise/PRBS (e.g. "ES_OFF", "WHITENOISE", "PRBS")
            shots: Number of shots per trigger (default 1)
            sweeps: Number of sweeps (default 1)
            trigger_type: Type of trigger (e.g. "RISING", "FALLING")
            trigger_source: Source of trigger (e.g. "NONE", "SCOPE_TRIG")
            ext_in_threshold: External trigger threshold in ADC counts

        Returns:
            None

        Raises:
            ArgumentOutOfRangeError: If parameters are invalid for device
        """
        prefix = self.name.upper()

        # Convert string parameters to enum values
        try:
            wave_type_val = getattr(self, f"{prefix}_WAVE_TYPE")[f"{prefix}_{wave_type.upper()}"]
            sweep_type_val = getattr(self, f"{prefix}_SWEEP_TYPE")[f"{prefix}_{sweep_type.upper()}"]
        except (AttributeError, KeyError) as e:
            raise ArgumentOutOfRangeError(f"Invalid wave_type or sweep_type for this device: {e}")

        # Check function signature and call appropriate version
        if len(self._set_sig_gen_built_in.argtypes) == 10:
            args = (device.handle, offset_voltage, pk_to_pk, wave_type_val,
                   start_frequency, stop_frequency, increment, dwell_time,
                   sweep_type_val, sweeps)
            converted_args = self._convert_args(self._set_sig_gen_built_in, args)
            status = self._set_sig_gen_built_in(*converted_args)

        elif len(self._set_sig_gen_built_in.argtypes) == 15:
            try:
                trigger_type_val = getattr(self, f"{prefix}_SIGGEN_TRIG_TYPE")[f"{prefix}_SIGGEN_{trigger_type.upper()}"]
                trigger_source_val = getattr(self, f"{prefix}_SIGGEN_TRIG_SOURCE")[f"{prefix}_SIGGEN_{trigger_source.upper()}"]
                extra_ops_val = getattr(self, f"{prefix}_EXTRA_OPERATIONS")[f"{prefix}_{operation.upper()}"]
            except (AttributeError, KeyError) as e:
                raise ArgumentOutOfRangeError(f"Invalid trigger parameters for this device: {e}")

            args = (device.handle, offset_voltage, pk_to_pk, wave_type_val,
                   start_frequency, stop_frequency, increment, dwell_time,
                   sweep_type_val, extra_ops_val, shots, sweeps,
                   trigger_type_val, trigger_source_val, ext_in_threshold)
            converted_args = self._convert_args(self._set_sig_gen_built_in, args)
            status = self._set_sig_gen_built_in(*converted_args)

        else:
            raise NotImplementedError("Signal generator not supported on this device")

        if status != self.PICO_STATUS["PICO_OK"]:
            raise PicoError(f"set_sig_gen_built_in failed: {constants.pico_tag(status)}")

    def _convert_args(self, func, args):
        """Convert arguments to match function argtypes.

        Args:
            func: The C function with argtypes defined
            args: Tuple of arguments to convert

        Returns:
            Tuple of converted arguments matching argtypes
        """
        if not hasattr(func, 'argtypes'):
            return args

        converted = []
        for arg, argtype in zip(args, func.argtypes):
            # Handle byref parameters
            if argtype == c_void_p and arg is not None:
                converted.append(byref(arg))
            # Handle normal parameters
            elif arg is not None:
                converted.append(argtype(arg))
            else:
                converted.append(None)
        return tuple(converted)

