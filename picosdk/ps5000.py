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

ps5000.PS5000_CHANNEL = make_enum([
	"PS5000_CHANNEL_A",
	"PS5000_CHANNEL_B",
	"PS5000_CHANNEL_C",
	"PS5000_CHANNEL_D",
	("PS5000_MAX_CHANNELS", "PS5000_EXTERNAL")
	"PS5000_TRIGGER_AUX",
	"PS5000_MAX_TRIGGER_SOURCES",
])

ps5000.PS5000_RANGE = make_enum([
	"PS5000_10MV",
	"PS5000_20MV",
	"PS5000_50MV",
	"PS5000_100MV",
	"PS5000_200MV",
	"PS5000_1V",
	"PS5000_2V",
	"PS5000_5V",
	"PS5000_10V",
	"PS5000_20V",
	"PS5000_50V",
	"PS5000_MAX_RANGES",
])

ps5000.PS5000_TIME_UNITS = make_enum([
	"PS5000_FS",
	"PS5000_PS",
	"PS5000_NS",
	"PS5000_US",
	"PS5000_MS",
	"PS5000_S",
	"PS5000_MAX_TIME_UNITS",
])
	

class PWQ_CONDITIONS (Structure):
	_pack = 1
	_fields = [("channelA", c_int32),
				("channelB", c_int32),
				("channelC", c_int32),
				("channelD", c_int32),
				("external", c_int32),
				("aux", c_int32)]

ps5000.PWQ_CONDITIONS = PWQ_CONDITIONS

class TRIGGER_CONDITIONS (Structure):
	_pack = 1
	_fields = [("channelA", c_int32),
				("channelB", c_int32),
				("channelC", c_int32),
				("channelD", c_int32),
				("external", c_int32),
				("aux", c_int32),
				("pulseWidthQualifier", c_int32)]
				
ps5000.TRIGGER_CONDITIONS = TRIGGER_CONDITIONS

class TRIGGER_CHANNEL_PROPERTIES (Structure):
	_pack = 1
	_fields = [("thresholdMajor", c_int16),
				("thresholdMinor", c_int16),
				("hysteresis", c_uint16),
				("channel", c_int32),
				("thresholdMode", c_int32)]
				
ps5000.TRIGGER_CHANNEL_PROPERTIES = TRIGGER_CHANNEL_PROPERTIES
				
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
        ps5000StreamingReady  lpPs5000Ready,
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

doc = """ PICO_STATUS ps5000GetTriggerTimeOffsetBulk
	(
		short  handle,
		unsigned long  *timesUpper,
		unsigned long  *timesLower,
		PS5000_TIME_UNITS  *timeUnits,
		unsigned short   fromSegmentIndex,
		unsigned short  toSegmentIndex
	); """
ps5000.make_symbol("_GetTriggerTimeOffsetBulk", "ps5000GetTriggerTimeOffsetBulk", c_uint32, [c_int16, c_void_p, c_void_p, c_void_p, c_uint16, c_uint16], doc)

doc = """ PICO_STATUS ps5000GetTriggerTimeOffsetBulk64
	(
		short  handle,
		_int64  *times,
		PS5000_TIME_UNITS  *timeUnits,
		unsigned short  fromSegmentIndex,
		unsigned short  toSegmentIndex
	); """
ps5000.make_symbol("_GetTriggerTimeOffsetBulk64", "ps5000GetTriggerTimeOffsetBulk64", c_uint32, [c_int16, c_void_p, c_void_p, c_uint16, c_int16], doc)

doc = """ PICO_STATUS ps5000IsLedFlashing
	(
		short  handle,
		short  *status
	); """
ps5000.make_symbol("_IsLedFlashing", "ps5000IsLedFlashing", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000IsReady
	(
		short  handle,
		short  *ready
	); """
ps5000.make_symbol("_IsReady", "ps5000IsReady", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000IsTriggerOrPulseWidthQualifierEnabled
	(
		short  handle,
		short  *triggerEnabled,
		short  *pulseWidthQualifierEnabled
	); """
ps5000.make_symbol("_IsTriggerOrPulseWidthQualifierEnabled", "ps5000IsTriggerOrPulseWidthQualifierEnabled", c_uint32, [c_int16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000MemorySegments
	(
		short  handle,
		unsigned short  nSegments,
		long  *nMaxSamples
	); """
ps5000.make_symbol("_MemorySegments", "ps5000MemorySegments", c_uint32, [c_int16, c_uint16, c_void_p], doc)

doc = """ PICO_STATUS ps5000NoOfStreamingValues
	(
		short  handle,
		unsigned long  *noOfValues
	); """
ps5000.make_symbol("_NoOfStreamingValues", "ps5000NoOfStreamingValues", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000OpenUnit
	(
		short  *handle
	); """
ps5000.make_symbol("_OpenUnit", "ps5000OpenUnit", c_uint32, [c_void_p], doc)

doc = """ PICO_STATUS ps5000OpenUnitAsync
	(
		short  *status
	); """
ps5000.make_symbol("_OpenUnitAsync", "ps5000OpenUnitAsync", c_uint32, [c_void_p], doc)

doc = """ PICO_STATUS ps5000OpenUnitProgress
	(
		short  *handle,
		short  *progressPercent,
		short  *complete
	); """
ps5000.make_symbol("_OpenUnitProgress", "ps5000OpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000RunBlock
	(
		short  handle,
		long  noOfPreTriggerSamples,
		long  noOfPostTriggerSamples,
		unsigned long  timebase,
		short  oversample,
		long  *timeIndisposedMs,
		unsigned short  segmentIndex,
		ps5000BlockReady  lpReady,
		void  *pParameter
	); """
ps5000.make_symbol("_RunBlock", "ps5000RunBlock", c_uint32, [c_int16, c_int32, c_int32, c_uint32, c_int16, c_void_p, c_uint16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps5000RunStreaming
	(
		short  handle,
		unsigned long  *sampleInterval,
		PS5000_TIME_UNITS  sampleIntervalTimeUnits,
		unsigned long  maxPreTriggerSamples,
		unsigned long  maxPostTriggerSamples,
		short  autoStop,
		unsigned long  downSampleRatio,
		unsigned long  overviewBufferSize
	); """
ps5000.make_symbol("_RunStreaming", "ps5000RunStreaming", c_uint32, [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps5000SetChannel
	(
		short  handle,
		PS5000_CHANNEL  channel,
		short  enabled,
		short  dc,
		PS5000_RANGE  range
	); """
ps5000.make_symbol("_SetChannel", "ps5000SetChannel", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_int32], doc)

doc = """ PICO_STATUS ps5000SetDataBuffer
	(
		short  handle,
		PS5000_CHANNEL  channel,
		short  *buffer,
		long  buggerLth
	); """
ps5000.make_symbol("_SetDataBuffer", "ps5000SetDataBuffer", c_uint32, [c_int16, c_int32, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps5000SetDataBufferBulk
	(
		short  handle,
		PS5000_CHANNEL  channel,
		short  *buffer,
		long  bufferLth,
		unsigned short  waveform
	); """
ps5000.make_symbol("_SetDataBufferBulk", "ps5000SetDataBufferBulk", c_uint32, [c_int16, c_int32, c_void_p, c_int32, c_uint16], doc)

doc = """ PICO_STATUS ps5000SetDataBuffers
	(
		short  handle,
		PS5000_CHANNEL  channel,
		short  *bufferMax,
		short  *bufferMin,
		long  bufferLth
	); """
ps5000.make_symbol("_SetDataBuffers", "ps5000SetDataBuffers", c_uint32, [c_int16, c_int32, c_void_p, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps5000SetEts
	(
		short  handle,
		PS5000_ETS_MODE  mode,
		short  etsCycles,
		short  etsInterleave,
		long  *sampleTimePicoseconds
	); """
ps5000.make_symbol("_SetEts", "ps5000SetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps5000SetEtsTimeBuffer
	(
		short  handle,
		_int64  *buffer,
		long  bufferLth
	); """
ps5000.make_symbol("_SetEtsTimeBuffer", "ps5000SetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps5000SetEtsTimeBuffers
	(
		short  handle,
		unsigned long  *timeUpper,
		unsigned long  *timeLower,
		long  bufferLth
	); """
ps5000.make_symbol("_SetEtsTimeBuffers", "ps5000SetEtsTimeBuffers", c_uint32, [c_int16, c_void_p, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps5000SetNoOfCaptures
	(
		short  handle,
		unsigned short  nCaptures
	); """
ps5000.make_symbol("_SetNoOfCaptures", "ps5000SetNoOfCaptures", c_uint32, [c_int16, c_uint16], doc)

doc = """ PICO_STATUS ps5000SetPulseWidthQualifier
	(
		short  handle,
		struct PWQ_CONDITIONS  *conditions,
		short  nConditions,
		THRESHOLD_DIRECTION  direction,
		unsigned long  lower,
		unsigned long  upper,
		PULSE_WIDTH_TYPE  type
	); """
ps5000.make_symbol("_SetPulseWidthQualifier", "ps5000SetPulseWidthQualifier", c_uint32, [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps5000SetSigGenArbitary
	(
		short  handle,
		long  offsetVoltage,
		unsigned long  pkToPk,
		unsigned long  startDeltaPhase,
		unsigned long  stopDeltaPhase,
		unsigned long  deltaPhaseIncrement,
		unsigned long  dwellCount,
		short  *arbitaryWaveform
		long  arbitaryWaveformSize,
		SWEEP_TYPE  sweepType,
		short  whiteNoise,
		INDEX_MODE  indexMode,
		unsigned long  shots,
		unsigned long sweeps,
		SIGGEN_TRIG_TYPE  triggerType,
		SIGGEN_TRIG_SOURCE  triggerSource,
		short  extInThreshold
	); """
ps5000.make_symbol("_SetSigGenArbitary", "ps5000SetSigGenArbitary", c_uint32, 
					[c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p, 
						c_int32, c_int32, c_int16, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps5000SetSigGenBuiltIn
	(
		short  handle,
		long  offsetVoltage,
		unsigned long  pkToPk,
		short  waveType,
		float  startFrequency,
		float  stopFrequency,
		float  increment,
		float  dwellTime,
		SWEEP_TYPE  sweepType,
		short  whiteNoise,
		unsigned long  shots,
		unsigned long  sweeps,
		SIGGEN_TRIG_TYPE  triggerType,
		SIGGEN_TRIG_SOURCE  triggerSource,
		short  extInThreshold
	); """
ps5000.make_symbol("_SetSigGenBuiltIn", "ps5000SetSigGenBuiltIn", c_uint32, 
					[c_int16, c_int32, c_uint32, c_int16, c_int64, c_int64, c_int64, c_int64, c_int64, c_int32, c_int16, c_uint32, c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps5000SetSimpleTrigger
	(
		short  handle,
		short  enable,
		PS5000_CHANNEL  source,
		short  threshold,
		THRESHOLD_DIRECTION  direction,
		unsigned long  delay,
		short  autoTrigger_ms
	); """
ps5000.make_symbol("_SetSimpleTrigger", "ps5000SetSimpleTrigger", c_uint32, [c_int16, c_int16, c_int32, c_int16 c_int32, c_uint32, c_int16], doc)

doc = """ PICO_STATUS ps5000SetTriggerChannelConditions
	(
		short  handle,
		struct TRIGGER_CONDITIONS  *conditions,
		short  nConditions
	); """
ps5000.make_symbol("_SetTriggerChannelConditions", "ps5000SetTriggerChannelConditions", c_uint32, [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps5000SetTriggerChannelDirections
	(
		short  handle,
		THRESHOLD_DIRECTION  channelA,
		THRESHOLD_DIRECTION  channelB,
		THRESHOLD_DIRECTION  channelC,
		THRESHOLD_DIRECTION  channelD,
		THRESHOLD_DIRECTION  ext,
		THRESHOLD_DIRECTION  aux
	); """
ps5000.make_symbol("_SetTriggerChannelDirections", "ps5000SetTriggerChannelDirections", c_uint32, [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps5000SetTriggerChannelProperties
	(
		short  handle,
		struct TRIGGER_CHANNEL_PROPERTIES  *channelProperties,
		short  nChannelProperties,
		short  auxOutputEnable,
		long  autoTriggerMilliseconds
	); """
ps5000.make_symbol("_SetTriggerChannelProperties", "ps5000SetTriggerChannelProperties", c_uint32, [c_int16, c_void_p, c_int16, c_int16, c_int32], doc)

doc = """ PICO_STATUS ps5000SetTriggerDelay
	(
		short  handle,
		unsigned long  delay
	); """
ps5000.make_symbol("_SetTriggerDelay", "ps5000SetTriggerDelay", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps5000SigGenSoftwareControl
	(
		short  handle,
		short  state
	); """
ps5000.make_symbol("_SigGenSoftwareControl", "ps5000SigGenSoftwareControl", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps5000Stop
	(
		short  handle
	); """
ps5000.make_symbol("_Stop", "ps5000Stop", c_uint32, [c_int16], doc)

doc = """ void ps5000BlockReady
	(
		short  handle,
		PICO_STATUS  status,
		void  *pParameter
	); """

ps5000.BlockReadyType = C_CALLBACK_FUNCTION_FACTORY(None,
													c_int16,
													c_uint32,
													c_void_p)
													
ps5000.BlockReadyType.__doc__ = doc

doc = """ void (CALLBACK *ps5000DataReady)
	(
		short  handle,
		long  noOfSamples,
		short  overflow,
		unsigned long  triggerAt,
		short  triggered,
		void  *pParameter
	); """
	
ps5000.DataReadyType = C_CALLBACK_FUNCTION_FACTORY(None,
													c_int16,
													c_int32,
													c_int16,
													c_uint32,
													c_int16,
													c_void_p)
													
ps5000.DataReadyType.__doc__ = doc

doc = """ void (CALLBACK *ps5000StreamingReady)
	(
		short  handle,
		long  noOfSamples,
		unsigned long  startIndex,
		short  overflow,
		unsigned long  triggerAt,
		short  triggered,
		short  autoStop,
		void  *pParameter
	); """

ps5000.StreamingReadyType = C_CALLBACK_FUNCTION_FACTORY(None,
														c_int16,
														c_int32,
														c_uint32, 
														c_int16,
														c_uint32,
														c_int16,
														c_int16,
														c_void_p)
														
ps5000.StreamingReadyType.__doc__ = doc