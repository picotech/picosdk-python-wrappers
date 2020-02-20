#
# Copyright (C) 2014-2020 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the usbDrDaqApi.h C header
file for DrDaq Data Logger using the usbDrDaq driver API
functions.
"""

from ctypes import *
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY
from picosdk.library import Library
from picosdk.constants import make_enum

class UsbDrDaqlib(Library):
    def __init__(self):
        super(UsbDrDaqlib, self).__init__("usbDrDaq")


usbDrDaq = UsbDrDaqlib()

usbDrDaq.USB_DRDAQ_INPUTS = make_enum([
    "USB_DRDAQ_CHANNEL_EXT1":1,
	"USB_DRDAQ_CHANNEL_EXT2":2,
	"USB_DRDAQ_CHANNEL_EXT3":3,
	"USB_DRDAQ_CHANNEL_SCOPE":4,
	"USB_DRDAQ_CHANNEL_PH":5,
	"USB_DRDAQ_CHANNEL_RES":6,
	"USB_DRDAQ_CHANNEL_LIGHT":7,
	"USB_DRDAQ_CHANNEL_TEMP":8,
	"USB_DRDAQ_CHANNEL_MIC_WAVE":9,
	("USB_DRDAQ_CHANNEL_MIC_LEVEL", "USB_DRDAQ_MAX_CHANNELS"):10
])

usbDrDaq.USB_DRDAQ_GPIO = make_enum([
    "USB_DRDAQ_GPIO_1":1,
	"USB_DRDAQ_GPIO_2":2,
	"USB_DRDAQ_GPIO_3":3,
	"USB_DRDAQ_GPIO_4":4
])

doc = """ PICO_STATUS UsbDrDaqCloseUnit
    (
	    int16_t    handle
	); """
usbDrDaq.make_symbol("_CloseUnit", "UsbDrDaqCloseUnit", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS UsbDrDaqEnabledRGBLED
    (
	    int16_t    handle,
		int16_t    enabled
	); """
usbDrDaq.make_symbol("_EnableRGBLED", "UsbDrDaqEnableRGBLED", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS UsbDrDaqGetChannelInfo
    (
	    int16_t    handle,
		float      *min,
		float      *max,
		int16_t    *places,
		int16_t    *divider,
		USB_DRDAQ_INPUTS    channel
	); """
usbDrDaq.make_symbol("_GetChannelInfo", "UsbDrDaqGetChannelInfo", c_uint32, [c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS UsbDrDaqGetInput
    (
	    int16_t    handle,
		USB_DRDAQ_GPIO    IOChannel,
		int16_t    pullUp,
		int16_t    *value
	); """
usbDrDaq.make_symbol("_GetInput", "UsbDrDaqGetInput", c_uint32, [c_int16, c_uint32, c_int16, c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqGetPulseCount
    (
	    int16_t    handle,
		USB_DRDAQ_GPIO    IOChannel,
		int16_t    *count
	); """
usbDrDaq.make_symbol("_GetPulseCount", "UsbDrDaqGetPulseCount", c_uint32, [c_int16, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqGetScalings
    (
	    int16_t    handle,
		USB_DRDAQ_INPUTS    channel,
		int16_t    *nScales
		int16_t    *currentScale,
		int8_t     *names
		int16_t    namesSize
	); """
usbDrDaq.make_symbol("_GetScalings", "UsbDrDaqGetScalings", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p, c_void_p, c_int16], doc)

doc = """ PICO_STATUS UsbDrDaqGetSingle
    (
	    int16_t    handle,
		USB_DRDAQ_INPUTS    channel,
		int16_t    *value,
		uint16_t    *overflow
	); """
usbDrDaq.make_symbol("_GetSingle", "UsbDrDaqGetSingle", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqGetSingleF
    (
	    int16_t    handle,
		USB_DRDAQ_INPUTS    channel,
		float    *value,
		uint16_t    *overflow
	); """
usbDrDaq.make_symbol("_getSingleF", "UsbDrDaqGetSingleF", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqGetTriggerTimeOffestNs
    (
	    int16_t    handle,
		int64_t    *time
    ); """
usbDrDaq.make_symbol("_GetTriggerTimeOffsetNs", "UsbDrDaqGetTriggerTimeOffestNs", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqGetUnitInfo
    (
	    int16_t    handle,
		int8_t    *string,
		int16_t     stringLength,
		int16_t     *requiredSize,
		PICO_INFO     info
	); """
usbDrDaq.make_symbol("_GetUnitInfo", "UsbDrDaqGetUnitInfo", c_uint32, [c_int16, c_void_p, c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS UsbDrDaqGetValues
    (
	    int16_t    handle,
		int16_t    *values,
		uint32_t    *noOfValues,
		uint16_t    *overflow,
		uint32_t    *triggerIndex
	); """
usbDrDaq.make_symbol("_GetValues", "UsbDrDaqGetValues", c_uint32, [c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqGetValuesF
    (
	    int16_t    handle,
		float     *values,
		uint32_t    *noOfValues,
		uint16_t    *overflow,
		uint32_t    *triggerIndex
	); """
usbDrDaq.make_symbol("_GetValuesF", "UsbDrDaqGetValuesF", c_uint32, [c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqOpenUnit
    (
	    int16_t    *handle
	); """
usbDrDaq.make_symbol("_OpenUnit", "UsbDrDaqOpenUnit", c_uint32, [c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqOpenUnitAsync
    (
	    int16_t    *handle
	); """
usbDrDaq.make_symbol("_OpenUnitAsync", "UsbDrDaqOpenUnitAsync", c_uint32, [c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqOpenUnitProgress
    (
	    int16_t    *handle,
		int16_t    *progress,
		int16_t    *complete
	); """
usbDrDaq.make_symbol("_OpenUnitProgress", "UsbDrDaqOpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqPhTemperatureCompensation
    (
	    int16_t    handle,
		uint16_t    enabled
	); """
usbDrDaq.make_symbol("_PhTemperatureCompensation", "UsbDrDaqPhTemperatureCompensation", c_uint32, [c_int16, c_uint16], doc)

doc = """ PICO_STATUS UsbDrDaqPingUnit
    (
	    int16_t    *handle
	); """
usbDrDaq.make_symbol("_PingUnit", "UsbDrDaqPingUnit", c_uint32, [c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqReady
    (
	    int16_t    handle,
		int16_t    *ready
	); """
usbDrDaq.make_symbol("_Ready", "UsbDrDaqReady", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS UsbDrDaqRun
    (
	    int16_t    handle,
		uint32_t    no_of_values,
		BLOCK_METHOD    method
	); """
usbDrDaq.make_symbol("_Run", "UsbDrDaqRun", c_uint32, [c_int16, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS UsbDrDaqSetDO
    (
	    int16_t    handle,
		USB_DRDAQ_GPIO    IOChannel,
		int16_t    value
	); """
usbDrDaq.make_symbol("_SetDO", "UsbDrDaqSetDO", c_uint32, [c_int16, c_uint32, c_int16], doc)

doc = """ PICO_STATUS UsbDrDaqSetInterval
    (
	    int16_t    handle,
		uint32_t    *us_for_block,
		uint32_t    ideal_no_of_samples,
		USB_DRDAQ_INPUTS    *channels,
		int16_t    no_of_channels
	); """
usbDrDaq.make_symbol("_SetInterval", "UsbDrDaqSetInterval", c_uint32, [c_int16, c_void_p, c_uint32, c_void_p, c_int16], doc)

doc = """ PICO_STATUS UsbDrDaqSetIntervalF
    (
	    int16_t    handle,
		float    *us_for_block,
		uint32_t    ideal_no_of_samples,
		USB_DRDAQ_INPUTS    *channels,
		int16_t    no_of_channels
	); """
usbDrDaq.make_symbol("_SetIntervalF", "UsbDrDaqSetIntervalF", c_uint32, [c_int16, c_void_p, c_uint32, c_void_p, c_int16], doc)

doc = """ PICO_STATUS UsbDrDaqSetPWM
    (
	    int16_t    handle,
		USB_DRDAQ_GPIO    IOChannel,
		uint16_t    period,
		uint8_t    cycle
	); """
usbDrDaq.make_symbol("_SetPWM", "UsbDrDaqSetPWM", c_uint32, [c_int16, c_uint32, c_uint16, c_uint8], doc)

doc = """ PICO_STATUS UsbDrDaqSetRGBLED
    (
	    int16_t    handle,
		uint16_t    red,
		uint16_t    green,
		uint16_t    blue
	); """
usbDrDaq.make_symbol("_SetRGBLED", "UsbDrDaqSetRGBLED", c_uint32, [c_int16, c_uint16, c_uint16, c_uint16], doc)

doc = """ PICO_STATUS UsbDrDaqSetScalings
    (
	    int16_t    handle,
		USB_DRDAQ_INPUTS    channel,
		int16_t    scalingNumber
	); """
usbDrDaq.make_symbol("_SetScalings", "UsbDrDaqSetScalings", c_uint32, [c_int16, c_uint32, c_int16], doc)

doc = """ PICO_STATUS UsbDrDaqSetSigGenArbitary
    (
	    int16_t    handle,
		int32_t    offsetVoltage,
		uint32_t    pkToPk,
		int16_t    *arbitaryWaveform,
		int16_t    arbitaryWaveformSize,
		int32_t    updateRate
	); """
usbDrDaq.make_symbol("_SetSigGenArbitary", "UsbDrDaqSetSigGenArbitary", c_uint32, [c_int16, c_int32, c_uint32, c_void_p, c_int16, c_int32], doc)

doc = """ PICO_STATUS UsbDrDaqSetSigGenBuiltIn
    (
	    int16_t    handle,
		int32_t    offsetVoltage,
		uint32_t    pkToPk,
		int16_t    frequency,
		USB_DRDAQ_WAVE    waveType
	); """
usbDrDaq.make_symbol("_SetSigGenBuiltIn", "UsbDrDaqSetSigGenBuiltIn", c_uint32, [c_int16, c_int32, c_uint32, c_int16, c_uint32], doc)

doc = """ PICO_STATUS UsbDrDaqSetTrigger
    (
	    int16_t    handle,
		uint16_t    enabled,
		uint16_t    auto_trigger,
		uint16_t    auto_ms,
		uint16_t    channel,
		uint16_t    dir,
		int16_t    threshold,
		uint16_t    hysteresis,
		float    delay
	); """
usbDrDaq.make_symbol("_SetTrigger", "UsbDrDaqSetTrigger", c_uint32, [c_int16, c_uint16, c_uint16, c_uint16, c_uint16, c_uint16,c_int16, c_uint16, c_float], doc)

doc = """ PICO_STATUS UsbDrDaqStartPulseCount
    (
	    int16_t    handle,
		USB_DRDAQ_GPIO    IOChannel,
		int16_t    direction
	); """
usbDrDaq.make_symbol("_StartPulseCount", "UsbDrDaqStartPulseCount", c_uint32, [c_int16, c_uint32, c_int16], doc)

doc = """ PICO_STATUS UsbDrDaqStop
    (
	    int16_t    handle
	); """
usbDrDaq.make_symbol("_Stop", "UsbDrDaqStop", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS UsbDrDaqStopSigGen
    (
	    int16_t    handle
	); """
usbDrDaq.make_symbol("_StopSigGen", "UsbDrDaqStopSigGen", c_uint32, [c_int16], doc)