#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps6000aApi.h C header
file for PicoScope 6000 A Series oscilloscopes using the ps6000a driver API
functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY
from picosdk.constants import make_enum


class Ps6000alib(Library):
    def __init__(self):
        super(Ps6000alib, self).__init__("ps6000a")

ps6000a = Ps6000alib()

doc = """ PICO_STATUS ps6000aOpenUnit
    (
        int16_t *handle,
        int8_t  *serial
        PICO_DEVICE_RESOLUTION    resolution
    ); """
ps6000a.make_symbol("_OpenUnit", "ps6000aOpenUnit", c_uint32, [c_void_p, c_char_p, c_int32], doc)

doc = """ PICO_STATUS ps6000aOpenUnitAsync
    (
        int16_t    *handle,
        int8_t    *serial,
        PICO_DEVICE_RESOLUTION    resolution
    ); """
ps6000a.make_symbol("_OpenUnitAsync", "ps6000aOpenUnitAsync", c_uint32, [c_void_p, c_char_p, c_int32], doc)

doc = """ PICO_STATUS ps6000aOpenUnitProgress
    (
        int16_t    *handle,
        int16_t    *progressPercent,
        int16_t    *complete
    ); """
ps6000a.make_symbol("_OpenUnitProgress", "ps6000aOpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aGetUnitInfo
    (
        int16_t    handle,
        int8_t    *string,
        int16_t    stringLength,
        int16_t    *requiredSize,
        PICO_INFO    info
    ); """
ps6000a.make_symbol("_GetUnitInfo", "ps6000aGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps6000aCloseUnit
    (
        int16_t    handle
    ); """
ps6000a.make_symbol("_CloseUnit", "ps6000aCloseUnit", c_uint32, [c_int16], doc)