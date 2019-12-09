#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps5000Api.h C header
file for PicoScope 5000 Series oscilloscopes using the ps5000 driver API
functions.
"""

from ctypes import *
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY
from picosdk.library import Library
from picosdk.constants import make_enum

class Ps5000lib(Library):
    def __init__(self):
        super(Ps5000lib, self).__init__("ps5000")


ps5000 = Ps5000lib()

doc = """ PICO_STATUS ps5000CloseUnit
    (
        short  handle
    ); """
ps5000.make_symbol("_CloseUnit", "ps5000CloseUnit", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS ps5000FlashLed
    (
        short  handle,
        short  start
    ); """
ps5000.make_symbol("_FlashLed", "ps5000FlashLed", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps5000GetMaxDownSampleRatio
    (
        short  handle,
        unsigned long  noOfUnaggregatedSamples,
        unsigned long  *maxDownSampleRatio,
        short  downSampleRatioMode,
        unsigned short  segmentIndex
    ); """
ps5000.make_symbol("_GetMaxDownSampleRatio", "ps5000GetMaxDownSampleRatio", c_uint32, [c_int16, c_uint32, c_void_p, c_int16, c_uint16], doc)

doc = """ PICO_STATUS ps5000GetStreamingLatestValues
    (
        short  handle,
        ps5000StreamignReady  lpPs5000Ready,
        void  *pParameter
    ); """
ps5000.make_symbol("_GetStreamingLatestValues", "ps5000GetStreamingLatestValues", c_uint16, [c_int16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000GetTimebase
    (
        short  handle,
        unsigned long  timebase,
        long  noSamples,
        long  *timeIntervalNanoseconds,
        short  oversample,
        long  *maxSamples,
        unsigned short  segmentIndex
    ); """
ps.make_symbol("_GetTimebase", "ps5000GetTimebase", c_uint16, [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint16], doc)

doc = """ PICO_STATUS ps5000GetTriggerTimeOffset
    (
        short  handle,
        unsigned long  *timeUpper,
        unsigned long  *timeLower,
        PS5000_TIME_UNITS  *timeUnits,
        unsigned short  segmentIndex
    ); """
ps.make_symbol("_GetTriggerTimeOffset", "ps5000GetTriggerTimeOffset", c_uint16, [c_int16, c_void_p, c_void_p, c_void_p, c_uint16], doc)

doc = """ PICO_STATUS ps5000GetTriggerTimeOffset64
    (
        short  handle,
        int64_t  *time,
        PS5000_TIME_UNITS  *timeUnits,
        unsigned short  segmentIndex
    ); """
ps.make_symbol("_GetTriggerTimeOffset64", "ps5000GetTriggerTimeOffset64", c_uint32, [c_int16, c_void_p, c_void_p, c_uint16], doc)

doc = """ PICO_STATUS ps5000GetUnitInfo
    (
        short  handle,
        char  *string,
        short  stringLength,
        short  *requiredSize,
        PICO_INFO  info
    ); """
ps.make_symbol("_GetUnitInfo", "ps5000GetUnitInfo", c_uint32, [c_int16, c_void_p, c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps5000GetValues
    (
        short  handle,
        unsigned long  startIndex,
        unsigned long  *noOfSamples,
        unsigned long  downSampleRatio,
        short  downSampleRatioMode,
        unsigned short  segmentIndex,
        short  *overflow
    ); """
ps.make_symbol("_GetValues", "ps5000GetValues", c_uint32, [c_int16, c_uint32, c_void_p, c_uint32, c_int16, c_uint16, c_void_p], doc)

doc = """ PICO_STATUS ps5000GetValuesAsync
    (
        short  handle,
        unsigned long  startIndex,
        unsigned long  noOfSamples,
        unsigned long  downSampleRatio,
        short  downSampleRatioMode,
        unsigned short  segmentIndex,
        void  *lpDataReady,
        void  *pParameter
    ); """
ps.make_symbol("_GetValuesAsync", "ps5000GetValuesAsync", c_uint32, [c_int16, c_uint32, c_uint32, c_uint32, c_int16, c_uint16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000GetValuesBulk
    (
        short  handle,
        unsigned long  *noOfSamples,
        unsigned short  fromSegmentIndex,
        unsigned short  toSegmentIndex,
        short  *overflow
    ); """
ps5000.make_symbol("_GetValuesBulk", "ps5000GetValuesBulk", c_uint32, [c_int16, c_void_p, c_uint16, c_uint16, c_void_p], doc)