#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the picohrdl.h C header file
for ADC-20/24 Data Loggers using the picohrdl driver API functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.errors import ArgumentOutOfRangeError
from picosdk.constants import make_enum

class picohrdllib(Library):
    def __init__(self):
        super(picohrdllib, self).__init__("picohrdl")
		
picohrdl = picohrdllib()

doc = """ int16_t HRDLCloseUnit
    (
	    int16_t    handle
	); """
picohrdl.makesymbol("_closeUnit_", "HRDLCloseUnit", c_int16, [c_int16], doc)

doc = """ int16_t HRDLCollectSingleValueAsync
    (
	    int16_t    handle,
		int16_t    channel,
		int16_t    range,
		int16_t    conversionTime,
		int16_t    singleEnded
	); """
picohrdl.makesymbol("_collectSingleValue_Async_", "HRDLCollectSingleValueAsync", c_int16, [c_int16, c_int16, c_int16, c_int16, c_int16], doc)

doc = """ int16_t HRDLGetMinMaxAdcCounts
    (
	    int16_t    handle,
		int32_t    *minAdc,
		int32_t    *maxAdc,
		int16_t    channel
	); """
picohrdl.makesymbol("_getMinMaxAdcCounts_", "HRDLGetMinMaxAdcCounts", c_int16, [c_int16, c_void_p, c_void_p, c_int16], doc)

doc = """ int16_t HRDLGetNumberOfEnabledChannels
    (
	    int16_t    handle,
		int16_t    *nEnabledChannels
	); """
picohrdl.makesymbol("_getNumberOfEnabledChannels_", "HRDLGetNumberOfEnabledChannels", c_int16, [c_int16, c_void_p], doc)

doc = """ int16_t HRDLGetSingleValue
    (
	    int16_t    handle,
		int16_t    channel,
		int16_t    range,
		int16_t    conversionTime,
		int16_t    singleEnded,
		int16_t    *overflow,
		int32_t    *value
	); """
picohrdl.makesymbol("_getSingleValue_", "HRDLGetSingleValue", c_int16, [c_int16, c_int16, c_int16, c_int16, c_int16, c_void_p, c_void_p], doc)

doc = """ int16_t HRDLGetSingleValueAsync
    (
	    int16_t    handle,
		int32_t    *value,
		int16_t    *overflow
	); """
picohrdl.makesymbol("_getSingleValueAsync_", "HRDLGetSingleValueAsync", c_int16, [c_int16, c_void_p, c_void_p], doc)

doc = """ int32_t HRDLGetTimesAndVAlues
    (
	    int16_t    handle,
		int32_t    *times,
		int32_t    *values,
		int16_t    *overflow,
		int32_t    noOfValues
	); """
picohrdl.makesymbol("_getTimesAndValues_", "HRDLGetTimesAndVAlues", c_int16, [c_int16, c_void_p, c_void_p, c_void_p, c_int32], doc)

doc = """ int16_t HRDLGetUnitInfo
    (
	    int16_t    handle,
		int8_t     *string,
		int16_t    stringLength,
		int16_t    info
	); """
picohrdl.makesymbol("_getUnitInfo_", "HRDLGetUnitInfo", c_int16, [c_int16, c_void_p, c_int16, c_int16], doc)

doc = """ int32_t HRDLGetValues
    (
	    int16_t    handle,
		int32_t    *values,
		int16_t    *overflow,
		int32_t    noOfValues
	); """
picohrdl,makesymbol("_getValues_", "HRDLGetValues", c_int16, [c_int16, c_void_p, c_void_p, c_int32], doc)

doc = """ int16_t HRDLOpenUnit
    (
	    void
	); """
picohrdl.makesymbol("_openUnit_", "HRDLOpenUnit", c_int16, [], doc)

doc = """ int16_t HRDLOpenUnitAsync
    (
	    void
	); """
picohrdl.makesymbol("_openUnitAsync_", "HRDLOpenUnitAsync", c_int16, [], doc)

doc = """ int16_t HRDLOpenUnitProgress
    (
	    int16_t    *handle,
		int16_t    *progress
	); """
picohrdl.makesymbol("_openUnitProgress_", "HRDLOpenUnitProgress", c_int16, [c_void_p, c_void_p], doc)

doc = """ int16_t HRDLReady
    (
	    int16_t    handle
	); """
picohrdl.makesymbol("_ready_", "HRDLReady", c_int16, [c_int16], doc)

doc = """ int16_t HRDLRun
    (
	    int16_t    handle,
		int32_t    nValues,
		int16_t    method
	); """
picohrdl.makesymbol("_run_", "HRDLRun", c_int16, [c_int16, c_int32, c_int16], doc)

doc = """ int16_t HRDLSetAnalogInChannel
    (
	    int16_t    handle,
		int16_t    channel,
		int16_t    enabled,
		int16_t    range,
		int16_t    singleEnded
	); """
picohrdl.makesymbol("_setAnalogInChannel_", "HRDLSetAnalogInChannel", c_int16, [c_int16, c_int16, c_int16, c_int16, c_int16], doc)

doc = """ int16_t HRDLSetDigitalIOChannel
    (
	    int16_t    handle,
		int16_t    directionOut,
		int16_t    digitalOutPinState,
		int16_t    enabledDigitalIn
	); """
picohrdl.makesymbol("_setDigitalIOChannel_", "HRDLSetDigitalIOChannel", c_int16, [c_int16, c_int16, c_int16, c_int16], doc)

doc = """ int16_t HRDLSetInterval
    (
	    int16_t    handle,
		int32_t    samplesInterval_ms,
		int16_t    conversionTime
	); """
picohrdl.makesymbol("_setInterval_", "HRDLSetInterval", c_int16, [c_int16, c_int32, c_int16], doc)

doc = """ int16_t HRDLSetMains
    (
	    int16_t    handle,
		int16_t    sixtyHertz
	); """
picohrdl.makesymbol("_setMains_", "HRDLSetMains", c_int16, [c_int16, c_int16], doc)

doc = """ void HRDLStop
    (
	    int16_t    handle
	); """
picohrdl,makesymbol("_stop_", "HRDLStop", c_int16, [c_int16], doc)