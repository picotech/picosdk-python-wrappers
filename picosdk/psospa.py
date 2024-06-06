#
# Copyright (C) 2024 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the psospaApi.h C header
file for PicoScope 3000 A Series oscilloscopes using the psospa driver API
functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY
from picosdk.constants import make_enum
from picosdk.PicoDeviceEnums import picoEnum as enums

class Psospalib(Library)
    def __init__(self):
	    super(Psospalib, self).__init__("psospa")
	
psospa = Psospalib()

doc = """ PICO_STATUS psospaOpenUnit
    (
	    int16_t*    handle,
		int8_t*     serial,
		PICO_DEVICE_RESOLUTION    resolution,
		PICO_USB_POWER_DETAILS*    powerDetails
	); """
psospa.make_symbol("psospaOpenUnit", c_uint32, [c_void_p, c_char_p, c_int32, c_void_p], doc)

doc = """ PICO_STATUS psospaCloseUnit
    (
	    int16_t    handle
	); """
psospa.make_symbol("psospaCloseUnit", c_uint32, [c_int16], doc)