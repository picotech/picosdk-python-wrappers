#
# Copyright (C) 2015-2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the usbtc08.h C header file
for TC-08 Thermocouple Data Logger using the usbtc08 driver API functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.errors import ArgumentOutOfRangeError
from picosdk.constants import make_enum

class usbtc08lib(Library):
    def __init__(self):
        super(usbtc08lib, self).__init__("usbtc08")


usbtc08 = usbtc08lib()

usbtc08.USBTC08_UNITS = make_enum([
    "USBTC08_UNITS_CENTIGRADE",
	"USBTC08_UNITS_FAHRENHEIT",
	"USBTC08_UNITS_KELVIN",
	"USBTC08_UNITS_RANKINE",
])

class USBTC08_INFO(Structure):
    _pack_ = 1
    _fields_ = [("size", c_int16),
                ("DriverVersion", c_int8),
                ("PicoppVersion", c_int16),
				("HardwareVersion", c_int16),
				("Variant", c_int16),
				("szSerial[USBTC08_MAX_SERIAL_CHAR]", c_int8),
				("szCalDate[USBTC08_MAX_DATE_CHARS]", c_int8)]

doc = """ int16_t usb_tc08_open_unit
    (
	    void
	); """
usbtc08.make_symbol("_open_unit_","usb_tc08_open_unit", c_int16, [], doc)

doc = """ int16_t usb_tc08_open_unit_async
    (
	    void
	); """
usbtc08.make_symbol("_open_unit_async_","usb_tc08_open_unit_async", c_int16, [], doc)

doc = """ int16_t usb_tc08_open_unit_progress
    (
	    int16_t  *handle,
		int16_t  *progress
	); """
usbtc08.make_symbol("_open_unit_progress_","usb_tc08_open_unit_progress", c_int16, [c_void_p, c_void_p], doc)

doc = """ int16_t usb_tc08_close_unit
    (
	    int16_t  handle
	); """
usbtc08.make_symbol("_close_unit_","usb_tc08_close_unit", c_int16, [c_int16], doc)

doc = """ int16_t usb_tc08_stop
    (
	    int16_t  handle
	); """
usbtc08.make_symbol("_stop_","usb_tc08_stop", c_int16, [c_int16], doc)

doc = """ int16 usb_tc08_set_mains
    (
	    int16_t  handle,
		int16_t  sixty_hertz
	); """
usbtc08.make_symbol("_set_mains_","usb_tc08_set_mains", c_int16, [c_int16, c_int16], doc)

doc = """ int32_t usb_tc08_get_minimum_interval_ms
    (
	    int16_t  handle
	); """
usbtc08.make_symbol("_get_minimum_interval_ms_","usb_tc08_get_minimum_interval_ms", c_int16, [c_int16], doc)

doc = """ int16_t usb_tc08_get_unit_info
    (
	    int16_t  handle
		USBTC08_INFO  *info
	); """
usbtc08.make_symbol("_get_unit_info_","usb_tc08_get_unit_info", c_int16, [c_int16, c_void_p], doc)

doc = """ int16_t usb_tc08_get_unit_info2
    (
	    int16_t  handle,
		int8_t  *string,
		int16_t  string_length,
		int16_t  line
	); """
usbtc08.make_symbol("_get_unit_info2_","usb_tc08_get_unit_info2", c_int16, [c_int16, c_void_p, c_int16, c_int16], doc)

doc = """ int16_t usb_tc08_get_formatted_info
    (
	    int16_t  handle,
		int8_t  *unit_info,
		int16_t  string_length
	); """
usbtc08.make_symbol("_get_formatted_info_","usb_tc08_get_formatted_info", c_int16, [c_int16, c_void_p, c_int16], doc)

doc = """ int16_t usb_tc08_get_last_error
    (
	    int16_t  handle
	); """
usbtc08.make_symbol("_get_last_error_","usb_tc08_get_last_error", c_int16, [c_int16], doc)

doc = """ int16_t usb_tc08_set_channel
    (
	    int16_t  handle,
		int16_t  channel,
		int8_t  tc_type
	); """
usbtc08.make_symbol("_set_channel_","usb_tc08_set_channel", c_int16, [c_int16, c_int16, c_int8], doc)

doc = """ int32_t usb_tc08_run
    (
	    int16_t  handle,
		int32_t  interval
	); """
usbtc08.make_symbol("_run_","usb_tc08_run", c_int16, [c_int16, c_int32], doc)

doc = """ int16_t usb_tc08_get_single
    (
	    int16_t  handle,
		float  *temp,
		int16_t  *overflow_flags,
		int16_t  units
	); """
usbtc08.make_symbol("_get_single_","usb_tc08_get_single", c_int16, [c_int16, c_void_p, c_void_p, c_int16], doc)

doc = """ int32_t usb_tc08_get_temp
    (
	    int16_t  handle,
		float  *temp_buffer,
		int32_t  *times_ms_buffer,
		int32_t  buffer_length,
		int16_t  *overflow,
		int16_t  channel,
		int16_t  units,
		int16_t  fill_missing
	); """
usbtc08.make_symbol("_get_temp_","usb_tc08_get_temp", c_int16, [c_int16, c_void_p, c_void_p, c_int32, c_void_p, c_void_p, c_int16, c_int16], doc)

doc = """ int32_t usb_tc08_get_temp_deskew
    (
	    int16_t  handle,
		float  *temp_buffer,
		int32_t  *times,
		int32_t  buffer_length,
		int16_t  *overflow,
		int16_t  channel,
		int16_t  units,
		int16_t  fill_missing
	); """
usbtc08.make_symbol("_get_temp_deskew_","usb_tc08_get_temp_deskew", c_int16, [c_int16, c_void_p, c_void_p, c_int32, c_void_p, c_int16, c_int16, c_int16], doc)