#
# Copyright (C) 2014-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps2000aApi.h C header
file for PicoScope 2000 Series oscilloscopes using the ps2000a driver API functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.constants import make_enum


class Ps2000alib(Library):
    def __init__(self):
        super(Ps2000alib, self).__init__("ps2000a")


ps2000a = Ps2000alib()

# A tuple in an enum like this is 2 names for the same value.
ps2000a.PS2000A_CHANNEL = make_enum([
    "PS2000A_CHANNEL_A",
    "PS2000A_CHANNEL_B",
    "PS2000A_CHANNEL_C",
    "PS2000A_CHANNEL_D",
    ("PS2000A_EXTERNAL", "PS2000A_MAX_CHANNELS"),
    "PS2000A_TRIGGER_AUX",
    "PS2000A_MAX_TRIGGER_SOURCE",
])

# only include the normal analog channels for now:
ps2000a.PICO_CHANNEL = {k[-1]: v for k, v in ps2000a.PS2000A_CHANNEL.items() if "PS2000A_CHANNEL_" in k}


ps2000a.PS2000A_COUPLING = make_enum([
    'PS2000A_AC',
    'PS2000A_DC',
])

# Just use AC and DC.
ps2000a.PICO_COUPLING = {k[-2:]: v for k, v in ps2000a.PS2000A_COUPLING.items()}

ps2000a.PS2000A_RANGE = make_enum([
    "PS2000A_10MV",
    "PS2000A_20MV",
    "PS2000A_50MV",
    "PS2000A_100MV",
    "PS2000A_200MV",
    "PS2000A_500MV",
    "PS2000A_1V",
    "PS2000A_2V",
    "PS2000A_5V",
    "PS2000A_10V",
    "PS2000A_20V",
    "PS2000A_50V",
    "PS2000A_MAX_RANGES",
])

ps2000a.PICO_VOLTAGE_RANGE = {
    v: float(k.split('_')[1][:-1]) if k[-2] != 'M' else (0.001 * float(k.split('_')[1][:-2]))
    for k, v in ps2000a.PS2000A_RANGE.items() if k != "PS2000A_MAX_RANGES"
}


doc = """ PICO_STATUS ps2000aOpenUnit
    (
        int16_t *status,
        int8_t  *serial
    ); """
ps2000a.make_symbol("_OpenUnit", "ps2000aOpenUnit", c_uint32, [c_void_p, c_char_p], doc)

doc = """ PICO_STATUS ps2000aOpenUnitAsync
    (
        int16_t *status,
        int8_t	*serial
    ); """
ps2000a.make_symbol("_OpenUnitAsync", "ps2000aOpenUnitAsync", c_uint32, [c_void_p, c_char_p], doc)

doc = """ PICO_STATUS ps2000aOpenUnitProgress
    (
        int16_t *handle,
        int16_t *progressPercent,
        int16_t *complete
    ); """
ps2000a.make_symbol("_OpenUnitProgress", "ps2000aOpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps2000aGetUnitInfo
    (
        int16_t   handle,
        int8_t   *string,
        int16_t   stringLength,
        int16_t  *requiredSize,
        PICO_INFO info
    ); """
ps2000a.make_symbol("_GetUnitInfo", "ps2000aGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32],
                    doc)

doc = """ PICO_STATUS ps2000aFlashLed
    (
        int16_t handle,
        int16_t start
    ); """
ps2000a.make_symbol("_FlashLed", "ps2000aFlashLed", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps2000aCloseUnit
    (
        int16_t handle
    ); """
ps2000a.make_symbol("_CloseUnit", "ps2000aCloseUnit", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps2000aMemorySegments
    (
        int16_t   handle,
        uint32_t  nSegments,
        int32_t  *nMaxSamples
    ); """
ps2000a.make_symbol("_MemorySegments", "ps2000aMemorySegments", c_uint32, [c_int16, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps2000aSetChannel
    (
        int16_t          handle,
        PS2000A_CHANNEL  channel,
        int16_t          enabled,
        PS2000A_COUPLING type,
        PS2000A_RANGE    range,
        float            analogOffset
    ); """
ps2000a.make_symbol("_SetChannel", "ps2000aSetChannel", c_uint32,
                    [c_int16, c_int32, c_int16, c_int32, c_int32, c_float], doc)

doc = """ PICO_STATUS ps2000aSetDigitalPort
    (
        int16_t              handle,
        PS2000A_DIGITAL_PORT port,
        int16_t              enabled,
        int16_t              logicLevel
    ); """
ps2000a.make_symbol("_SetDigitalPort", "ps2000aSetDigitalPort", c_uint32, [c_int16, c_int32, c_int16, c_int16], doc)

doc = """ PICO_STATUS ps2000aSetNoOfCaptures
    (
        int16_t  handle,
        uint32_t nCaptures
    ); """
ps2000a.make_symbol("_SetNoOfCaptures", "ps2000aSetNoOfCaptures", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps2000aGetTimebase
    (
        int16_t  handle,
        uint32_t timebase,
        int32_t  noSamples,
        int32_t *timeIntervalNanoseconds,
        int16_t  oversample,
        int32_t *maxSamples,
        uint32_t segmentIndex
    ); """
ps2000a.make_symbol("_GetTimebase", "ps2000aGetTimebase", c_uint32,
                    [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps2000aGetTimebase2
    (
        int16_t  handle,
        uint32_t timebase,
        int32_t  noSamples,
        float   *timeIntervalNanoseconds,
        int16_t  oversample,
        int32_t *maxSamples,
        uint32_t segmentIndex
    ); """
ps2000a.make_symbol("_GetTimebase2", "ps2000aGetTimebase2", c_uint32,
                    [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps2000aSetSigGenArbitrary
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        int16_t                    *arbitraryWaveform,
        int32_t                     arbitraryWaveformSize,
        PS2000A_SWEEP_TYPE          sweepType,
        PS2000A_EXTRA_OPERATIONS    operation,
        PS2000A_INDEX_MODE          indexMode,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS2000A_SIGGEN_TRIG_TYPE    triggerType,
        PS2000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps2000a.make_symbol("_SetSigGenArbitrary", "ps2000aSetSigGenArbitrary", c_uint32,
                    [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p, c_int32, c_int32,
                     c_int32,
                     c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps2000aSetSigGenBuiltIn
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        int16_t                     waveType,
        float                       startFrequency,
        float                       stopFrequency,
        float                       increment,
        float                       dwellTime,
        PS2000A_SWEEP_TYPE          sweepType,
        PS2000A_EXTRA_OPERATIONS    operation,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS2000A_SIGGEN_TRIG_TYPE    triggerType,
        PS2000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps2000a.make_symbol("_SetSigGenBuiltIn", "ps2000aSetSigGenBuiltIn", c_uint32,
                    [c_int16, c_int32, c_uint32, c_int16, c_float, c_float, c_float, c_float, c_int32, c_int32,
                     c_uint32,
                     c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps2000aSetSigGenPropertiesArbitrary
    (
        int16_t                     handle,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        PS2000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS2000A_SIGGEN_TRIG_TYPE    triggerType,
        PS2000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps2000a.make_symbol("_SetSigGenPropertiesArbitrary", "ps2000aSetSigGenPropertiesArbitrary", c_uint32,
                    [c_int16, c_uint32, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_uint32, c_int32, c_int32,
                     c_int16], doc)

doc = """ PICO_STATUS ps2000aSetSigGenPropertiesBuiltIn
    (
        int16_t                     handle,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS2000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS2000A_SIGGEN_TRIG_TYPE    triggerType,
        PS2000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps2000a.make_symbol("_SetSigGenPropertiesBuiltIn", "ps2000aSetSigGenPropertiesBuiltIn", c_uint32,
                    [c_int16, c_double, c_double, c_double, c_double, c_int32, c_uint32, c_uint32, c_int32, c_int32,
                     c_int16], doc)

doc = """ PICO_STATUS ps2000aSigGenFrequencyToPhase
    (
        int16_t             handle,
        double              frequency,
        PS2000A_INDEX_MODE  indexMode,
        uint32_t            bufferLength,
        uint32_t           *phase
    ); """
ps2000a.make_symbol("_SigGenFrequencyToPhase", "ps2000aSigGenFrequencyToPhase", c_uint32,
                    [c_int16, c_double, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps2000aSigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
ps2000a.make_symbol("_SigGenArbitraryMinMaxValues", "ps2000aSigGenArbitraryMinMaxValues", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps2000aSigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    ); """
ps2000a.make_symbol("_SigGenSoftwareControl", "ps2000aSigGenSoftwareControl", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps2000aSetEts
    (
        int16_t           handle,
        PS2000A_ETS_MODE  mode,
        int16_t           etsCycles,
        int16_t           etsInterleave,
        int32_t          *sampleTimePicoseconds
    ); """
ps2000a.make_symbol("_SetEts", "ps2000aSetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps2000aSetSimpleTrigger
    (
        int16_t                      handle,
        int16_t                      enable,
        PS2000A_CHANNEL              source,
        int16_t                      threshold,
        PS2000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     delay,
        int16_t                      autoTrigger_ms
    ); """
ps2000a.make_symbol("_SetSimpleTrigger", "ps2000aSetSimpleTrigger", c_uint32,
                    [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16], doc)

doc = """ PICO_STATUS ps2000aSetTriggerDigitalPortProperties
    (
        int16_t                             handle,
        PS2000A_DIGITAL_CHANNEL_DIRECTIONS *directions,
        int16_t                             nDirections
    ); """
ps2000a.make_symbol("_SetTriggerDigitalPortProperties", "ps2000aSetTriggerDigitalPortProperties", c_uint32,
                    [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps2000aSetDigitalAnalogTriggerOperand
    (
        int16_t handle,
        PS2000A_TRIGGER_OPERAND operand
    ); """
ps2000a.make_symbol("_SetDigitalAnalogTriggerOperand", "ps2000aSetDigitalAnalogTriggerOperand", c_uint32,
                    [c_int16, c_int32], doc)

doc = """ PICO_STATUS ps2000aSetTriggerChannelProperties
    (
        int16_t                             handle,
        PS2000A_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                             nChannelProperties,
        int16_t                             auxOutputEnable,
        int32_t                             autoTriggerMilliseconds
    ); """
ps2000a.make_symbol("_SetTriggerChannelProperties", "ps2000aSetTriggerChannelProperties", c_uint32,
                    [c_int16, c_void_p, c_int16, c_int16, c_int32], doc)

doc = """ PICO_STATUS ps2000aSetTriggerChannelConditions
    (
        int16_t                     handle,
        PS2000A_TRIGGER_CONDITIONS *conditions,
        int16_t                     nConditions
    ); """
ps2000a.make_symbol("_SetTriggerChannelConditions", "ps2000aSetTriggerChannelConditions", c_uint32,
                    [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps2000aSetTriggerChannelDirections
    (
        int16_t                      handle,
        PS2000A_THRESHOLD_DIRECTION  channelA,
        PS2000A_THRESHOLD_DIRECTION  channelB,
        PS2000A_THRESHOLD_DIRECTION  channelC,
        PS2000A_THRESHOLD_DIRECTION  channelD,
        PS2000A_THRESHOLD_DIRECTION  ext,
        PS2000A_THRESHOLD_DIRECTION  aux
    ); """
ps2000a.make_symbol("_SetTriggerChannelDirections", "ps2000aSetTriggerChannelDirections", c_uint32,
                    [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps2000aSetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
ps2000a.make_symbol("_SetTriggerDelay", "ps2000aSetTriggerDelay", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps2000aSetPulseWidthQualifier
    (
        int16_t                      handle,
        PS2000A_PWQ_CONDITIONS      *conditions,
        int16_t                      nConditions,
        PS2000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     lower,
        uint32_t                     upper,
        PS2000A_PULSE_WIDTH_TYPE     type
    ); """
ps2000a.make_symbol("_SetPulseWidthQualifier", "ps2000aSetPulseWidthQualifier", c_uint32,
                    [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps2000aIsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
ps2000a.make_symbol("_IsTriggerOrPulseWidthQualifierEnabled", "ps2000aIsTriggerOrPulseWidthQualifierEnabled", c_uint32,
                    [c_int16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps2000aGetTriggerTimeOffset64
    (
        int16_t             handle,
        int64_t            *time,
        PS2000A_TIME_UNITS *timeUnits,
        uint32_t            segmentIndex
    ); """
ps2000a.make_symbol("_GetTriggerTimeOffset", "ps2000aGetTriggerTimeOffset64", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS PREF2 PREF3 (ps2000aGetValuesTriggerTimeOffsetBulk64)
    (
        int16_t             handle,
        int64_t            *times,
        PS2000A_TIME_UNITS *timeUnits,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex
    ); """
ps2000a.make_symbol("_GetValuesTriggerTimeOffsetBulk", "ps2000aGetValuesTriggerTimeOffsetBulk64", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps2000aGetNoOfCaptures
    (
        int16_t   handle,
        uint32_t *nCaptures
    ); """
ps2000a.make_symbol("_GetNoOfCaptures", "ps2000aGetNoOfCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps2000aGetNoOfProcessedCaptures
    (
        int16_t   handle,
        uint32_t *nProcessedCaptures
    ); """
ps2000a.make_symbol("_GetNoOfProcessedCaptures", "ps2000aGetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps2000aSetDataBuffer
    (
        int16_t            handle,
        int32_t            channelOrPort,
        int16_t           *buffer,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS2000A_RATIO_MODE mode
    ); """
ps2000a.make_symbol("_SetDataBuffer", "ps2000aSetDataBuffer", c_uint32,
                    [c_int16, c_int32, c_void_p, c_int32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps2000aSetDataBuffers
    (
        int16_t            handle,
        int32_t            channelOrPort,
        int16_t           *bufferMax,
        int16_t           *bufferMin,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS2000A_RATIO_MODE mode
    ); """
ps2000a.make_symbol("_SetDataBuffers", "ps2000aSetDataBuffers", c_uint32,
                    [c_int16, c_int32, c_void_p, c_void_p, c_int32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps2000aSetEtsTimeBuffer
    (
        int16_t  handle,
        int64_t *buffer,
        int32_t  bufferLth
    ); """
ps2000a.make_symbol("_SetEtsTimeBuffer", "ps2000aSetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps2000aIsReady
    (
        int16_t  handle,
        int16_t *ready
    ); """
ps2000a.make_symbol("_IsReady", "ps2000aIsReady", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps2000aRunBlock
    (
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        int16_t            oversample,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps2000aBlockReady  lpReady,
        void              *pParameter
    ); """
ps2000a.make_symbol("_RunBlock", "ps2000aRunBlock", c_uint32,
                    [c_int16, c_int32, c_int32, c_uint32, c_int16, c_void_p, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps2000aRunStreaming
    (
        int16_t             handle,
        uint32_t            *sampleInterval,
        PS2000A_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t            maxPreTriggerSamples,
        uint32_t            maxPostPreTriggerSamples,
        int16_t             autoStop,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            overviewBufferSize
    ); """
ps2000a.make_symbol("_RunStreaming", "ps2000aRunStreaming", c_uint32,
                    [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32], doc)

doc = """ PICO_STATUS ps2000aGetStreamingLatestValues
    (
        int16_t                handle,
        ps2000aStreamingReady  lpPs2000aReady,
        void                   *pParameter
    ); """
ps2000a.make_symbol("_GetStreamingLatestValues", "ps2000aGetStreamingLatestValues", c_uint32,
                    [c_int16, c_void_p, c_void_p], doc)

# TODO sort out how to make a callback for a C function in ctypes!
# doc = """ void *ps2000aStreamingReady
#     (
#         int16_t   handle,
#         int32_t   noOfSamples,
#         uint32_t  startIndex,
#         int16_t   overflow,
#         uint32_t  triggerAt,
#         int16_t   triggered,
#         int16_t   autoStop,
#         void     *pParameter
#     ); """
# ps2000a.make_symbol("_StreamingReady", "ps2000aStreamingReady", c_void_p,
#                     [c_int16, c_int32, c_uint32, c_int16, c_uint32, c_int16, c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps2000aNoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
ps2000a.make_symbol("_NoOfStreamingValues", "ps2000aNoOfStreamingValues", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps2000aGetMaxDownSampleRatio
    (
        int16_t             handle,
        uint32_t            noOfUnaggreatedSamples,
        uint32_t           *maxDownSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex
    ); """
ps2000a.make_symbol("_GetMaxDownSampleRatio", "ps2000aGetMaxDownSampleRatio", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_int32, c_uint32], doc)

doc = """ PICO_STATUS ps2000aGetValues
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
ps2000a.make_symbol("_GetValues", "ps2000aGetValues", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps2000aGetValuesBulk
    (
        int16_t             handle,
        uint32_t           *noOfSamples,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        int16_t            *overflow
    ); """
ps2000a.make_symbol("_GetValuesBulk", "ps2000aGetValuesBulk", c_uint32,
                    [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p], doc)

doc = """ PICO_STATUS ps2000aGetValuesAsync
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t            noOfSamples,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        void               *lpDataReady,
        void               *pParameter
    ); """
ps2000a.make_symbol("_GetValuesAsync", "ps2000aGetValuesAsync", c_uint32,
                    [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps2000aGetValuesOverlapped
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
ps2000a.make_symbol("_GetValuesOverlapped", "ps2000aGetValuesOverlapped", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps2000aGetValuesOverlappedBulk
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS2000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        int16_t            *overflow
    ); """
ps2000a.make_symbol("_GetValuesOverlappedBulk", "ps2000aGetValuesOverlappedBulk", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_int32, c_void_p], doc)

doc = """ PICO_STATUS ps2000aStop
    (
        int16_t  handle
    ); """
ps2000a.make_symbol("_Stop", "ps2000aStop", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps2000aHoldOff
    (
        int16_t               handle,
        uint64_t              holdoff,
        PS2000A_HOLDOFF_TYPE  type
    ); """
ps2000a.make_symbol("_HoldOff", "ps2000aHoldOff", c_uint32, [c_int16, c_uint64, c_int32], doc)

doc = """ PICO_STATUS ps2000aGetChannelInformation
    (
        int16_t               handle,
        PS2000A_CHANNEL_INFO  info,
        int32_t               probe,
        int32_t              *ranges,
        int32_t              *length,
        int32_t               channels
    ); """
ps2000a.make_symbol("_GetChannelInformation", "ps2000aGetChannelInformation", c_uint32,
                    [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps2000aEnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
ps2000a.make_symbol("_EnumerateUnits", "ps2000aEnumerateUnits", c_uint32, [c_void_p, c_char_p, c_void_p], doc)

doc = """ PICO_STATUS ps2000aPingUnit
    (
        int16_t  handle
    ); """
ps2000a.make_symbol("_PingUnit", "ps2000aPingUnit", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps2000aMaximumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
ps2000a.make_symbol("_MaximumValue", "ps2000aMaximumValue", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps2000aMinimumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
ps2000a.make_symbol("_MinimumValue", "ps2000aMinimumValue", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps2000aGetAnalogueOffset
    (
        int16_t           handle,
        PS2000A_RANGE     range,
        PS2000A_COUPLING  coupling,
        float            *maximumVoltage,
        float            *minimumVoltage
    ); """
ps2000a.make_symbol("_GetAnalogueOffset", "ps2000aGetAnalogueOffset", c_uint32,
                    [c_int16, c_int32, c_int32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps2000aGetMaxSegments
    (
        int16_t   handle,
        uint32_t *maxSegments
    ); """
ps2000a.make_symbol("_GetMaxSegments", "ps2000aGetMaxSegments", c_uint32, [c_int16, c_void_p], doc)

ps2000a.INI_LOGIC_VOLTS = 1.5
ps2000a.variants = ("2205MSO", "2206", "2206A", "2207", "2207A", "2208", "2208A")
