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
import ctypes
from ctypes import c_int16, c_int32, c_uint32, create_string_buffer
from ctypes.util import find_library
import collections

from picosdk.device import Device
import picosdk.constants as constants


class CannotFindPicoSDKError(Exception):
    pass


class CannotOpenPicoSDKError(Exception):
    pass


class DeviceNotFoundError(Exception):
    pass


class CannotCloseUnitError(Exception):
    pass


"""UnitInfo: A type for holding the particulars of a connected device.
driver = a Library subclass
variant = model name as a string
serial = batch and serial number as a string (for use with Library.open_unit)"""
UnitInfo = collections.namedtuple('UnitInfo', ['driver', 'variant', 'serial'])


PICO_OK = 0


def requires_device(error_message):
    def check_device_decorator(method):
        def check_device_impl(self, device, *args, **kwargs):
            if not isinstance(device, Device) or device.driver != self:
                raise TypeError(error_message)
            return method(self, device, *args, **kwargs)
        return check_device_impl
    return check_device_decorator



class Library(object):
    def load(self):
        result = None
        library_path = find_library(self.name)

        if library_path is None:
            env_var_name = "PATH" if sys.platform == 'win32' else "LD_LIBRARY_PATH"
            raise CannotFindPicoSDKError("PicoSDK (%s) not found, check %s" % (self.name, env_var_name))
        
        try:
            if sys.platform == 'win32':
                result = ctypes.WinDLL(library_path)
            else:
                result = ctypes.cdll.LoadLibrary(library_path)
        except OSError as e:
            raise CannotOpenPicoSDKError("PicoSDK (%s) not compatible (check 32 vs 64-bit): %s" % (self.name, e))
        return result

    def __init__(self, name):
        self.name = name
        self._clib = self.load()
        self.PICO_INFO = constants.PICO_INFO
        self.PICO_STATUS = constants.PICO_STATUS
        self.PICO_STATUS_LOOKUP = constants.PICO_STATUS_LOOKUP

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
                device_infos.append(self._python_get_unit_info_wrapper(handle))
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
        returns: a Device instance, which has functions on it for collecting data and using the waveform generator (if present).
        Note: Either use this object in a context manager, or manually call .close() on it when you are finished."""
        return Device(self, self._python_open_unit(serial=serial, resolution=resolution))

    @requires_device("close_unit requires a picosdk.device.Device instance, passed to the correct owning driver.")
    def close_unit(self, device):
        self._python_close_unit(device.handle)

    @requires_device("get_unit_info requires a picosdk.device.Device instance, passed to the correct owning driver.")
    def get_unit_info(self, device):
        return self._python_get_unit_info_wrapper(device.handle)

    def _python_open_unit(self, serial=None, resolution=None):
        handle = -1
        status = None
        if serial is None:
            if len(self._open_unit.argtypes) == 3:
                if resolution is None:
                    resolution = self.DEFAULT_RESOLUTION
                chandle = c_int16()
                cresolution = c_int32()
                cresolution.value = resolution
                status = self._open_unit(ctypes.byref(chandle), None, cresolution)
                handle = chandle.value
            elif len(self._open_unit.argtypes) == 2:
                chandle = c_int16()
                status = self._open_unit(ctypes.byref(chandle), None)
                handle = chandle.value
            else:
                handle = self._open_unit()
        else:
            if len(self._open_unit.argtypes) == 3:
                if resolution is None:
                    resolution = self.DEFAULT_RESOLUTION
                chandle = c_int16()
                cresolution = c_int32()
                cresolution.value = resolution
                cserial = create_string_buffer(serial)
                status = self._open_unit(ctypes.byref(chandle), cserial, cresolution)
                handle = chandle.value
            elif len(self._open_unit.argtypes) == 2:
                chandle = c_int16()
                cserial = create_string_buffer(serial)
                status = self._open_unit(ctypes.byref(chandle), cserial)
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

        if handle < 1:
            message = ("Driver %s could find no device" % self.name) + ("s" if serial is None else
                                                                        (" matching %s" % serial))
            if status is not None:
                message += " (%s)" % constants.pico_tag(status)
            raise DeviceNotFoundError(message)

        return handle

    def _python_close_unit(self, handle):
        return self._close_unit(c_int16(handle))

    @staticmethod
    def _create_empty_string_buffer():
        try:
            return create_string_buffer("\0", 255)
        except TypeError:
            return create_string_buffer("\0".encode('utf8'), 255)

    def _python_get_unit_info(self, handle, info_type):
        STRING_SIZE = 255
        info = self._create_empty_string_buffer()
        if len(self._get_unit_info.argtypes) == 4:
            info_len = self._get_unit_info(c_int16(handle), info, c_int16(STRING_SIZE), c_int16(info_type))
            if info_len > 0:
                return info.value[:info_len]
        elif len(self._get_unit_info.argtypes) == 5:
            required_size = c_int16(0)
            status = self._get_unit_info(c_int16(handle),
                                         info,
                                         c_int16(STRING_SIZE),
                                         ctypes.byref(required_size),
                                         c_uint32(info_type))
            if status == PICO_OK:
                if required_size.value < STRING_SIZE:
                    return info.value[:required_size.value]
        return ""

    def _python_get_unit_info_wrapper(self, handle):
        return UnitInfo(
            driver= self,
            variant= self._python_get_unit_info(handle, self.PICO_INFO["PICO_VARIANT_INFO"]),
            serial= self._python_get_unit_info(handle, self.PICO_INFO["PICO_BATCH_AND_SERIAL"])
        )










