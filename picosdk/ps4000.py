#
# Copyright (C) 2015-2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps4000Api.h C header
file for PicoScope 4000 Series oscilloscopes using the ps4000 driver API
functions.
"""

from ctypes import *
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY
from picosdk.library import Library
from picosdk.constants import make_enum


class Ps4000lib(Library):
    def __init__(self):
        super(Ps4000lib, self).__init__("ps4000")


ps4000 = Ps4000lib()

# This field is passed to the driver as a boolean, not an enum.
ps4000.PICO_COUPLING = {
    'AC': 0,
    'DC': 1
}

# A tuple in an enum like this is 2 names for the same value.
ps4000.PS4000_CHANNEL = make_enum([
    "PS4000_CHANNEL_A",
    "PS4000_CHANNEL_B",
    "PS4000_CHANNEL_C",
    "PS4000_CHANNEL_D",
    ("PS4000_EXTERNAL", "PS4000_MAX_CHANNELS"),
    "PS4000_TRIGGER_AUX",
    "PS4000_MAX_TRIGGER_SOURCE",
])

# only include the normal analog channels for now:
ps4000.PICO_CHANNEL = {k[-1]: v for k, v in ps4000.PS4000_CHANNEL.items() if "PS4000_CHANNEL_" in k}

ps4000.PS4000_RANGE = make_enum([
    "PS4000_10MV",
    "PS4000_20MV",
    "PS4000_50MV",
    "PS4000_100MV",
    "PS4000_200MV",
    "PS4000_500MV",
    "PS4000_1V",
    "PS4000_2V",
    "PS4000_5V",
    "PS4000_10V",
    "PS4000_20V",
    "PS4000_50V",
    "PS4000_100V",
    ("PS4000_RESISTANCE_100R", "PS4000_MAX_RANGES"),
    "PS4000_RESISTANCE_1K",
    "PS4000_RESISTANCE_10K",
    "PS4000_RESISTANCE_100K",
    "PS4000_RESISTANCE_1M",
    ("PS4000_ACCELEROMETER_10MV", "PS4000_MAX_RESISTANCES"),
    "PS4000_ACCELEROMETER_20MV",
    "PS4000_ACCELEROMETER_50MV",
    "PS4000_ACCELEROMETER_100MV",
    "PS4000_ACCELEROMETER_200MV",
    "PS4000_ACCELEROMETER_500MV",
    "PS4000_ACCELEROMETER_1V",
    "PS4000_ACCELEROMETER_2V",
    "PS4000_ACCELEROMETER_5V",
    "PS4000_ACCELEROMETER_10V",
    "PS4000_ACCELEROMETER_20V",
    "PS4000_ACCELEROMETER_50V",
    "PS4000_ACCELEROMETER_100V",
    ("PS4000_TEMPERATURE_UPTO_40", "PS4000_MAX_ACCELEROMETER"),
    "PS4000_TEMPERATURE_UPTO_70",
    "PS4000_TEMPERATURE_UPTO_100",
    "PS4000_TEMPERATURE_UPTO_130",
    ("PS4000_RESISTANCE_5K", "PS4000_MAX_TEMPERATURES"),
    "PS4000_RESISTANCE_25K",
    "PS4000_RESISTANCE_50K",
    "PS4000_MAX_EXTRA_RESISTANCES",
])


def process_enum(enum):
    """The PS4000 range enum is complicated enough that we need some clearer logic:"""
    import re
    pattern = re.compile(r'PS4000_([0-9]+M?)V')

    voltage_range = {}

    for enum_item_name, enum_item_value in enum.items():
        match = pattern.match(enum_item_name)
        if match is None:
            continue
        voltage_string = match.group(1)
        voltage = float(voltage_string) if voltage_string[-1] != 'M' else (0.001 * float(voltage_string[:-1]))

        voltage_range[enum_item_value] = voltage

    return voltage_range


ps4000.PICO_VOLTAGE_RANGE = process_enum(ps4000.PS4000_RANGE)

ps4000.PS4000_TIME_UNITS = make_enum([
    'PS4000_FS',
    'PS4000_PS',
    'PS4000_NS',
    'PS4000_US',
    'PS4000_MS',
    'PS4000_S',
    'PS4000_MAX_TIME_UNITS',
])

doc = """ PICO_STATUS ps4000OpenUnit
    (
        int16_t *handle
    ); """
ps4000.make_symbol("_OpenUnit0", "ps4000OpenUnit", c_uint32, [c_void_p, ], doc)

doc = """ PICO_STATUS ps4000OpenUnitAsync
    (
        int16_t *status
    ); """
ps4000.make_symbol("_OpenUnitAsync0", "ps4000OpenUnitAsync", c_uint32, [c_void_p], doc)

doc = """ PICO_STATUS ps4000OpenUnitEx
    (
        int16_t *handle,
        int8_t  *serial
    ); """
ps4000.make_symbol("_OpenUnit", "ps4000OpenUnitEx", c_uint32, [c_void_p, c_char_p], doc)

doc = """ PICO_STATUS ps4000OpenUnitAsyncEx
    (
        int16_t *status,
        int8_t  *serial
    ); """
ps4000.make_symbol("_OpenUnitAsync", "ps4000OpenUnitAsync", c_uint32, [c_void_p, c_char_p], doc)

doc = """ PICO_STATUS ps4000OpenUnitProgress
    (
        int16_t *handle,
        int16_t *progressPercent,
        int16_t *complete
    ); """
ps4000.make_symbol("_OpenUnitProgress", "ps4000OpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000GetUnitInfo
    (
        int16_t    handle,
        int8_t    *string,
        int16_t    stringLength,
        int16_t   *requiredSize,
        PICO_INFO  info
    ); """
ps4000.make_symbol("_GetUnitInfo", "ps4000GetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps4000FlashLed
    (
        int16_t  handle,
        int16_t  start
    ); """
ps4000.make_symbol("_FlashLed", "ps4000FlashLed", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps4000IsLedFlashing
    (
        int16_t  handle,
        int16_t *status
    ); """
ps4000.make_symbol("_IsLedFlashing", "ps4000IsLedFlashing", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000CloseUnit
    (
        int16_t  handle
    ); """
ps4000.make_symbol("_CloseUnit", "ps4000CloseUnit", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps4000MemorySegments
    (
        int16_t   handle,
        uint16_t  nSegments,
        int32_t  *nMaxSamples
    ); """
ps4000.make_symbol("_MemorySegments", "ps4000MemorySegments", c_uint32, [c_int16, c_uint16, c_void_p], doc)

doc = """ PICO_STATUS ps4000SetChannel
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t         enabled,
        int16_t         dc,
        PS4000_RANGE    range
    ); """
ps4000.make_symbol("_SetChannel", "ps4000SetChannel", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_int32], doc)

doc = """ PICO_STATUS ps4000SetNoOfCaptures
    (
        int16_t   handle,
        uint16_t  nCaptures
    ); """
ps4000.make_symbol("_SetNoOfCaptures", "ps4000SetNoOfCaptures", c_uint32, [c_int16, c_uint16], doc)

doc = """ PICO_STATUS ps4000GetTimebase
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        int32_t  *timeIntervalNanoseconds,
        int16_t   oversample,
        int32_t  *maxSamples,
        uint16_t  segmentIndex
    ); """
ps4000.make_symbol("_GetTimebase", "ps4000GetTimebase", c_uint32,
                   [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint16], doc)

doc = """ PICO_STATUS ps4000GetTimebase2
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        float    *timeIntervalNanoseconds,
        int16_t   oversample,
        int32_t  *maxSamples,
        uint16_t  segmentIndex
    ); """
ps4000.make_symbol("_GetTimebase2", "ps4000GetTimebase2", c_uint32,
                   [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint16], doc)

doc = """ PICO_STATUS ps4000SigGenOff
    (
        int16_t handle
    ); """
ps4000.make_symbol("_SigGenOff", "ps4000SigGenOff", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps4000SetSigGenArbitrary
    (
        int16_t             handle,
        int32_t             offsetVoltage,
        uint32_t            pkToPk,
        uint32_t            startDeltaPhase,
        uint32_t            stopDeltaPhase,
        uint32_t            deltaPhaseIncrement,
        uint32_t            dwellCount,
        int16_t            *arbitraryWaveform,
        int32_t             arbitraryWaveformSize,
        SWEEP_TYPE          sweepType,
        int16_t             operationType,
        INDEX_MODE          indexMode,
        uint32_t            shots,
        uint32_t            sweeps,
        SIGGEN_TRIG_TYPE    triggerType,
        SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t             extInThreshold
    ); """
ps4000.make_symbol("_SetSigGenArbitrary", "ps4000SetSigGenArbitrary", c_uint32,
                   [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p,
                    c_int32, c_int32, c_int16, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps4000SetSigGenBuiltIn
    (
        int16_t             handle,
        int32_t             offsetVoltage,
        uint32_t            pkToPk,
        int16_t             waveType,
        float               startFrequency,
        float               stopFrequency,
        float               increment,
        float               dwellTime,
        SWEEP_TYPE          sweepType,
        int16_t             operationType,
        uint32_t            shots,
        uint32_t            sweeps,
        SIGGEN_TRIG_TYPE    triggerType,
        SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t             extInThreshold
    ); """
ps4000.make_symbol("_SetSigGenBuiltIn", "ps4000SetSigGenBuiltIn", c_uint32,
                   [c_int16, c_int32, c_uint32, c_int16, c_float, c_float, c_float, c_float,
                    c_int32, c_int16, c_uint32, c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps4000SigGenFrequencyToPhase
    (
        int16_t     handle,
        double      frequency,
        INDEX_MODE  indexMode,
        uint32_t    bufferLength,
        uint32_t   *phase
    ); """
ps4000.make_symbol("_SigGenFrequencyToPhase", "ps4000SigGenFrequencyToPhase", c_uint32,
                   [c_int16, c_double, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps4000SigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
ps4000.make_symbol("_SigGenArbitraryMinMaxValues", "ps4000SigGenArbitraryMinMaxValues", c_uint32,
                   [c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000SigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    ); """
ps4000.make_symbol("_SigGenSoftwareControl", "ps4000SigGenSoftwareControl", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps4000SetEts
    (
        int16_t          handle,
        PS4000_ETS_MODE  mode,
        int16_t          etsCycles,
        int16_t          etsInterleave,
        int32_t         *sampleTimePicoseconds
    ); """
ps4000.make_symbol("_SetEts", "ps4000SetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000SetSimpleTrigger
    (
        int16_t              handle,
        int16_t              enable,
        PS4000_CHANNEL       source,
        int16_t              threshold,
        THRESHOLD_DIRECTION  direction,
        uint32_t             delay,
        int16_t              autoTrigger_ms
    ); """
ps4000.make_symbol("_SetSimpleTrigger", "ps4000SetSimpleTrigger", c_uint32,
                   [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16], doc)

doc = """ PICO_STATUS ps4000SetTriggerChannelProperties
    (
        int16_t                     handle,
        TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                     nChannelProperties,
        int16_t                     auxOutputEnable,
        int32_t                     autoTriggerMilliseconds
    ); """
ps4000.make_symbol("_SetTriggerChannelProperties", "ps4000SetTriggerChannelProperties", c_uint32,
                   [c_int16, c_void_p, c_int16, c_int16, c_int32], doc)

doc = """ PICO_STATUS ps4000SetExtTriggerRange
    (
        int16_t       handle,
        PS4000_RANGE  extRange
    ); """
ps4000.make_symbol("_SetExtTriggerRange", "ps4000SetExtTriggerRange", c_uint32, [c_int16, c_int32], doc)

doc = """ PICO_STATUS ps4000SetTriggerChannelConditions
    (
        int16_t             handle,
        TRIGGER_CONDITIONS *conditions,
        int16_t             nConditions
    ); """
ps4000.make_symbol("_SetTriggerChannelConditions", "ps4000SetTriggerChannelConditions", c_uint32,
                   [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps4000SetTriggerChannelDirections
    (
        int16_t              handle,
        THRESHOLD_DIRECTION  channelA,
        THRESHOLD_DIRECTION  channelB,
        THRESHOLD_DIRECTION  channelC,
        THRESHOLD_DIRECTION  channelD,
        THRESHOLD_DIRECTION  ext,
        THRESHOLD_DIRECTION  aux
    ); """
ps4000.make_symbol("_SetTriggerChannelDirections", "ps4000SetTriggerChannelDirections", c_uint32,
                   [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps4000SetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
ps4000.make_symbol("_SetTriggerDelay", "ps4000SetTriggerDelay", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps4000SetPulseWidthQualifier
    (
        int16_t              handle,
        PWQ_CONDITIONS      *conditions,
        int16_t              nConditions,
        THRESHOLD_DIRECTION  direction,
        uint32_t             lower,
        uint32_t             upper,
        PULSE_WIDTH_TYPE     type
    ); """
ps4000.make_symbol("_SetPulseWidthQualifier", "ps4000SetPulseWidthQualifier", c_uint32,
                   [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps4000IsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
ps4000.make_symbol("_IsTriggerOrPulseWidthQualifierEnabled", "ps4000IsTriggerOrPulseWidthQualifierEnabled", c_uint32,
                   [c_int16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000GetTriggerTimeOffset
    (
        int16_t            handle,
        uint32_t          *timeUpper,
        uint32_t          *timeLower,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           segmentIndex
    ); """
ps4000.make_symbol("_GetTriggerTimeOffset0", "ps4000GetTriggerTimeOffset", c_uint32,
                   [c_int16, c_void_p, c_void_p, c_void_p, c_uint16], doc)

doc = """ PICO_STATUS ps4000GetTriggerChannelTimeOffset
    (
        int16_t            handle,
        uint32_t          *timeUpper,
        uint32_t          *timeLower,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           segmentIndex,
        PS4000_CHANNEL     channel
    ); """
ps4000.make_symbol("_GetTriggerChannelTimeOffset0", "ps4000GetTriggerChannelTimeOffset", c_uint32,
                   [c_int16, c_void_p, c_void_p, c_void_p, c_uint16, c_int32], doc)

doc = """ PICO_STATUS ps4000GetTriggerTimeOffset64
    (
        int16_t            handle,
        int64_t           *time,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           segmentIndex
    ); """
ps4000.make_symbol("_GetTriggerTimeOffset", "ps4000GetTriggerTimeOffset64", c_uint32,
                   [c_int16, c_void_p, c_void_p, c_uint16], doc)

doc = """ PICO_STATUS ps4000GetTriggerChannelTimeOffset64
    (
        int16_t            handle,
        int64_t           *time,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           segmentIndex,
        PS4000_CHANNEL     channel
    ); """
ps4000.make_symbol("_GetTriggerChannelTimeOffset64", "ps4000GetTriggerChannelTimeOffset64", c_uint32,
                   [c_int16, c_void_p, c_void_p, c_uint16, c_int32], doc)

doc = """ PICO_STATUS ps4000GetValuesTriggerTimeOffsetBulk
    (
        int16_t            handle,
        uint32_t          *timesUpper,
        uint32_t          *timesLower,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           fromSegmentIndex,
        uint16_t           toSegmentIndex
    ); """
ps4000.make_symbol("_GetValuesTriggerTimeOffsetBulk0", "ps4000GetValuesTriggerTimeOffsetBulk", c_uint32,
                   [c_int16, c_void_p, c_void_p, c_void_p, c_uint16, c_uint16], doc)

doc = """ PICO_STATUS ps4000GetValuesTriggerChannelTimeOffsetBulk
    (
        int16_t            handle,
        uint32_t          *timesUpper,
        uint32_t          *timesLower,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           fromSegmentIndex,
        uint16_t           toSegmentIndex,
        PS4000_CHANNEL     channel
    ); """
ps4000.make_symbol("_GetValuesTriggerChannelTimeOffsetBulk0", "ps4000GetValuesTriggerChannelTimeOffsetBulk", c_uint32,
                   [c_int16, c_void_p, c_void_p, c_void_p, c_uint16, c_uint16, c_int32], doc)

doc = """ PICO_STATUS ps4000GetValuesTriggerTimeOffsetBulk64
    (
        int16_t            handle,
        int64_t           *times,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           fromSegmentIndex,
        uint16_t           toSegmentIndex
    ); """
ps4000.make_symbol("_GetValuesTriggerTimeOffsetBulk", "ps4000GetValuesTriggerTimeOffsetBulk64", c_uint32,
                   [c_int16, c_void_p, c_void_p, c_uint16, c_uint16], doc)

doc = """ PICO_STATUS ps4000GetValuesTriggerChannelTimeOffsetBulk64
    (
        int16_t            handle,
        int64_t           *times,
        PS4000_TIME_UNITS *timeUnits,
        uint16_t           fromSegmentIndex,
        uint16_t           toSegmentIndex,
        PS4000_CHANNEL     channel
    ); """
ps4000.make_symbol("_GetValuesTriggerChannelTimeOffsetBulk", "ps4000GetValuesTriggerChannelTimeOffsetBulk64", c_uint32,
                   [c_int16, c_void_p, c_void_p, c_uint16, c_uint16, c_int32], doc)

doc = """ PICO_STATUS ps4000SetDataBufferBulk
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t        *buffer,
        int32_t         bufferLth,
        uint16_t        waveform
    ); """
ps4000.make_symbol("_SetDataBufferBulk", "ps4000SetDataBufferBulk", c_uint32,
                   [c_int16, c_int32, c_void_p, c_int32, c_uint16], doc)

doc = """ PICO_STATUS ps4000SetDataBuffers
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t        *bufferMax,
        int16_t        *bufferMin,
        int32_t         bufferLth
    ); """
ps4000.make_symbol("_SetDataBuffers", "ps4000SetDataBuffers", c_uint32, [c_int16, c_int32, c_void_p, c_void_p, c_int32],
                   doc)

doc = """ PICO_STATUS ps4000SetDataBufferWithMode
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t        *buffer,
        int32_t         bufferLth,
        RATIO_MODE      mode
    ); """
ps4000.make_symbol("_SetDataBufferWithMode", "ps4000SetDataBufferWithMode", c_uint32,
                   [c_int16, c_int32, c_void_p, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps4000SetDataBuffersWithMode
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t        *bufferMax,
        int16_t        *bufferMin,
        int32_t         bufferLth,
        RATIO_MODE      mode
    ); """
ps4000.make_symbol("_SetDataBuffersWithMode", "ps4000SetDataBuffersWithMode", c_uint32,
                   [c_int16, c_int32, c_void_p, c_void_p, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps4000SetDataBuffer
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t        *buffer,
        int32_t         bufferLth
    ); """
ps4000.make_symbol("_SetDataBuffer", "ps4000SetDataBuffer", c_uint32, [c_int16, c_int32, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps4000SetEtsTimeBuffer
    (
        int16_t  handle,
        int64_t *buffer,
        int32_t  bufferLth
    ); """
ps4000.make_symbol("_SetEtsTimeBuffer", "ps4000SetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps4000SetEtsTimeBuffers
    (
        int16_t   handle,
        uint32_t *timeUpper,
        uint32_t *timeLower,
        int32_t   bufferLth
    ); """
ps4000.make_symbol("_SetEtsTimeBuffers", "ps4000SetEtsTimeBuffers", c_uint32, [c_int16, c_void_p, c_void_p, c_int32],
                   doc)

doc = """ PICO_STATUS ps4000RunBlock
    (
        int16_t           handle,
        int32_t           noOfPreTriggerSamples,
        int32_t           noOfPostTriggerSamples,
        uint32_t          timebase,
        int16_t           oversample,
        int32_t          *timeIndisposedMs,
        uint16_t          segmentIndex,
        ps4000BlockReady  lpReady,
        void             *pParameter
    ); """
ps4000.make_symbol("_RunBlock", "ps4000RunBlock", c_uint32,
                   [c_int16, c_int32, c_int32, c_uint32, c_int16, c_void_p, c_uint16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000RunStreaming
    (
        int16_t            handle,
        uint32_t          *sampleInterval,
        PS4000_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t           maxPreTriggerSamples,
        uint32_t           maxPostPreTriggerSamples,
        int16_t            autoStop,
        uint32_t           downSampleRatio,
        uint32_t           overviewBufferSize
    ); """
ps4000.make_symbol("_RunStreaming", "ps4000RunStreaming", c_uint32,
                   [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps4000RunStreamingEx
    (
        int16_t            handle,
        uint32_t          *sampleInterval,
        PS4000_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t           maxPreTriggerSamples,
        uint32_t           maxPostPreTriggerSamples,
        int16_t            autoStop,
        uint32_t           downSampleRatio,
        int16_t            downSampleRatioMode,
        uint32_t           overviewBufferSize
    ); """
ps4000.make_symbol("_RunStreamingEx", "ps4000RunStreamingEx", c_uint32,
                   [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps4000IsReady
    (
        int16_t handle,
        int16_t * ready
    ); """
ps4000.make_symbol("_IsReady", "ps4000IsReady", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000GetStreamingLatestValues
    (
        int16_t               handle,
        ps4000StreamingReady  lpPs4000Ready,
        void                 *pParameter
    ); """
ps4000.make_symbol("_GetStreamingLatestValues", "ps4000GetStreamingLatestValues", c_uint32,
                   [c_int16, c_void_p, c_void_p], doc)
				   
doc = """ void *ps4000StreamingReady
    (
        int16_t   handle,
        int32_t   noOfSamples,
        uint32_t  startIndex,
        int16_t   overflow,
        uint32_t  triggerAt,
        int16_t   triggered,
        int16_t   autoStop,
        void     *pParameter
    );
    define a python function which accepts the correct arguments, and pass it to the constructor of this type.
    """

ps4000.StreamingReadyType = C_CALLBACK_FUNCTION_FACTORY(None,
                                                         c_int16,
                                                         c_int32,
                                                         c_uint32,
                                                         c_int16,
                                                         c_uint32,
                                                         c_int16,
                                                         c_int16,
                                                         c_void_p)

ps4000.StreamingReadyType.__doc__ = doc

doc = """ PICO_STATUS ps4000NoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
ps4000.make_symbol("_NoOfStreamingValues", "ps4000NoOfStreamingValues", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000GetMaxDownSampleRatio
    (
        int16_t   handle,
        uint32_t  noOfUnaggreatedSamples,
        uint32_t *maxDownSampleRatio,
        int16_t   downSampleRatioMode,
        uint16_t  segmentIndex
    ); """
ps4000.make_symbol("_GetMaxDownSampleRatio", "ps4000GetMaxDownSampleRatio", c_uint32,
                   [c_int16, c_uint32, c_void_p, c_int16, c_uint16], doc)

doc = """ PICO_STATUS ps4000GetValues
    (
        int16_t   handle,
        uint32_t  startIndex,
        uint32_t *noOfSamples,
        uint32_t  downSampleRatio,
        int16_t   downSampleRatioMode,
        uint16_t  segmentIndex,
        int16_t  *overflow
    ); """
ps4000.make_symbol("_GetValues", "ps4000GetValues", c_uint32,
                   [c_int16, c_uint32, c_void_p, c_uint32, c_int16, c_uint16, c_void_p], doc)

doc = """ PICO_STATUS ps4000GetValuesBulk
    (
        int16_t   handle,
        uint32_t *noOfSamples,
        uint16_t  fromSegmentIndex,
        uint16_t  toSegmentIndex,
        int16_t  *overflow
    ); """
ps4000.make_symbol("_GetValuesBulk", "ps4000GetValuesBulk", c_uint32, [c_int16, c_void_p, c_uint16, c_uint16, c_void_p],
                   doc)

doc = """ PICO_STATUS ps4000GetValuesAsync
    (
        int16_t   handle,
        uint32_t  startIndex,
        uint32_t  noOfSamples,
        uint32_t  downSampleRatio,
        int16_t   downSampleRatioMode,
        uint16_t  segmentIndex,
        void     *lpDataReady,
        void     *pParameter
    ); """
ps4000.make_symbol("_GetValuesAsync", "ps4000GetValuesAsync", c_uint32,
                   [c_int16, c_uint32, c_uint32, c_uint32, c_int16, c_uint16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000Stop
    (
        int16_t  handle
    ); """
ps4000.make_symbol("_Stop", "ps4000Stop", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps4000SetProbe
    (
        int16_t       handle,
        PS4000_PROBE  probe,
        PS4000_RANGE  range
    ); """
ps4000.make_symbol("_SetProbe", "ps4000SetProbe", c_uint32, [c_int16, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps4000HoldOff
    (
        int16_t              handle,
        uint64_t             holdoff,
        PS4000_HOLDOFF_TYPE  type
    ); """
ps4000.make_symbol("_HoldOff", "ps4000HoldOff", c_uint32, [c_int16, c_uint64, c_int32], doc)

doc = """ PICO_STATUS ps4000GetProbe
    (
        int16_t       handle,
        PS4000_PROBE *probe
    ); """
ps4000.make_symbol("_GetProbe", "ps4000GetProbe", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000GetChannelInformation
    (
        int16_t              handle,
        PS4000_CHANNEL_INFO  info,
        int32_t              probe,
        int32_t             *ranges,
        int32_t             *length,
        int32_t              channels
    ); """
ps4000.make_symbol("_GetChannelInformation", "ps4000GetChannelInformation", c_uint32,
                   [c_int16, c_int32, c_int32, c_void_p, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps4000SetFrequencyCounter
    (
        int16_t                         handle,
        PS4000_CHANNEL                  channel,
        int16_t                         enabled,
        PS4000_FREQUENCY_COUNTER_RANGE  range,
        int16_t                         thresholdMajor,
        int16_t                         thresholdMinor
    ); """
ps4000.make_symbol("_SetFrequencyCounter", "ps4000SetFrequencyCounter", c_uint32,
                   [c_int16, c_int32, c_int16, c_int32, c_int16, c_int16], doc)

doc = """ PICO_STATUS ps4000EnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
ps4000.make_symbol("_EnumerateUnits", "ps4000EnumerateUnits", c_uint32, [c_void_p, c_char_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000PingUnit
    (
        int16_t  handle
    ); """
ps4000.make_symbol("_PingUnit", "ps4000PingUnit", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps4000SetBwFilter
    (
        int16_t         handle,
        PS4000_CHANNEL  channel,
        int16_t         enable
    ); """
ps4000.make_symbol("_SetBwFilter", "ps4000SetBwFilter", c_uint32, [c_int16, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps4000TriggerWithinPreTriggerSamples
    (
        int16_t  handle,
        int16_t  state
    ); """
ps4000.make_symbol("_TriggerWithinPreTriggerSamples", "ps4000TriggerWithinPreTriggerSamples", c_uint32,
                   [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps4000GetNoOfCaptures
    (
        int16_t   handle,
        uint16_t *nCaptures
    ); """
ps4000.make_symbol("_GetNoOfCaptures", "ps4000GetNoOfCaptures", c_uint32, [c_int16, c_void_p], doc)
