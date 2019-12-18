#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the pl1000.h C header
file for PicoLog 1000 Series datalogger using the pl1000 driver API functions.
"""

from ctypes import *
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY
from picosdk.library import Library
from picosdk.constants import make_enum

class Pl1000lib(Library):
    def __init__(self):
        super(Pl1000lib, self).__init__("pl1000")
		
pl1000 = Pl1000lib()

def _pl1000Inputs():
    PL1000_CHANNEL_1 = 1
    PL1000_CHANNEL_2 = 2
    PL1000_CHANNEL_3 = 3
    PL1000_CHANNEL_4 = 4
    PL1000_CHANNEL_5 = 5
    PL1000_CHANNEL_6 = 6
    PL1000_CHANNEL_7 = 7
    PL1000_CHANNEL_8 = 8
    PL1000_CHANNEL_9 = 9
    PL1000_CHANNEL_10 = 10
    PL1000_CHANNEL_11 = 11
    PL1000_CHANNEL_12 = 12
    PL1000_CHANNEL_13 = 13
    PL1000_CHANNEL_14 = 14
    PL1000_CHANNEL_15 = 15
    PL1000_CHANNEL_16 = 16
    PL1000_MAX_CHANNEL = PL1000_CHANNEL_16
	
    return {k.upper(): v for k, v in locals().items() if k.startswith("PL1000")}
	
pl1000.PL1000Inputs = _pl1000Inputs()

pl1000.PL1000DO_Channel = make_enum([
    'PL1000_DO_CHANNEL_0',
	'PL1000_DO_CHANNEL_1',
	'PL1000_DO_CHANNEL_2',
	'PL1000_DO_CHANNEL_3',
	'PL1000_DO_CHANNEL_MAX',
])

pl1000.PL1000OpenProgress = {
    'PL1000_OPEN_PROGRESS_FAIL' : -1,
	'PL1000_OPEN_PROGRESS_PENDING': 0,
	'PL1000_OPEN_PROGRESS_COMPLETE' : 1,
}

pl1000.PL1000_BLOCK_METHOD = make_enum([
	"BM_SINGLE",
	"BM_WINDOW",
	"BM_STREAM",
])

doc = """ PICO_STATUS pl1000CloseUnit
    (
	    int16_t  handle
	); """
pl1000.make_symbol("_CloseUnit_", "pl1000CloseUnit", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS pl1000GetSingle
    (
	    int16_t  handle,
		PL1000_INPUTS  channel,
		unit16_t  *value
	); """
pl1000.make_symbol("_GetSingle_", "pl1000GetSingle", c_uint32, [c_int16, c_int32, c_void_p], doc)

doc = """ PICO_STATUS pl1000GetUnitInfo
    (
	    int16_t  handle,
		int8_t  *string,
		int16_t  stringLength,
		int16_t  *requiredSize,
		PICO_INFO  info
	); """
pl1000.make_symbol("_GetUnitInfo_", "pl1000GetUnitInfo", c_uint32, [c_int16, c_void_p, c_int16, c_void_p, c_int32], doc)

doc = """ PICO_STATUS pl1000GetValues
    (
	    int16_t  handle,
		uint16_t  *values,
		uint32_t  *noOfValues,
		unit16_t  *overflow,
		uint32_t  *triggerIndex
	); """
pl1000.make_symbol("_GetValues_", "pl1000GetValues", c_uint32, [c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS pl1000MaxValue
    (
	    int16_t  handle,
		uint16_t  *maxValue
	); """
pl1000.make_symbol("_MaxValue_", "pl1000MaxValue", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS pl1000OpenUnit
    (
	    int16_t  *handle
	); """
pl1000.make_symbol("_OpenUnit_", "pl1000OpenUnit", c_uint32, [c_void_p], doc)

doc = """ PICO_STATUS pl1000OpenUnitAsync
    (
	    int16_t  *status
	); """
pl1000.make_symbol("_OpenUnitAsync_", "pl1000OpenUnitAsync", c_uint32, [c_void_p], doc)

doc = """ PICO_STATUS pl1000OpenUnitProgress
    (
	    int16_t  *handle,
		int16_t  *progress,
		int16_t  *complete
	); """
pl1000.make_symbol("_OpenUnitProgress_", "pl1000OpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS pl1000PingUnit
    (
	    int16_t  handle
	); """
pl1000.make_symbol("_PingUnit_", "pl1000PingUnit", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS pl1000Ready
    (
	    int16_t  handle,
		int16_t  *ready
	); """
pl1000.make_symbol("_Ready_", "pl1000Ready", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS pl1000Run
    (
	    int16_t  handle,
		uint32_t  no_of_values,
		BLOCK_METHOD  method
	); """
pl1000.make_symbol("_Run_", "pl1000Run", c_uint32, [c_int16, c_uint32, c_int32], doc)

doc = """ PICO_STATUS pl1000SetDo
    (
	    int16_t  handle,
		int16_t  do_value,
		int16_t  doNo
	); """
pl1000.make_symbol("_SetDo_", "pl1000SetDo", c_uint32, [c_int16, c_int16, c_int16], doc)

doc = """ PICO_STATUS pl1000SetInterval
    (
	    int16_t  handle,
		uint32_t  *us_for_block,
		uint32_t  ideal_no_of_samples,
		int16_t  *channels,
		int16_t  no_of_channels
	); """
pl1000.make_symbol("_SetInterval_", "pl1000SetInterval", c_uint32, [c_int16, c_void_p, c_uint32, c_void_p, c_int16], doc)

doc = """ PICO_STATUS pl1000SetPulseWidth
    (
	    int16_t  handle,
		uint16_t  period,
		uint8_t  cycle
	); """
pl1000.make_symbol("_SetPulseWidth_", "pl1000SetPulseWidth", c_uint32, [c_int16, c_int16, c_int8], doc)

doc = """ PICO_STATUS pl1000SetTrigger
    (
	    int16_t  handle,
		uint16_t  enabled,
		uint16_t  auto_trigger,
		uint16_t  auto_ms,
		uint16_t  channel,
		uint16_t  dir,
		uint16_t  threshold,
		uint16_t  hysteresis,
		float  delay
	); """
pl1000.make_symbol("_SetTrigger_", "pl1000SetTrigger", c_uint32, [c_int16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16, c_float], doc)

doc = """ PICO_STATUS pl1000Stop
    (
	    int16_t  handle
	); """
pl1000.make_symbol("_Stop_", "pl1000Stop", c_uint32, [c_int16], doc)

