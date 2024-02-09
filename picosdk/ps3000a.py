#
# Copyright (C) 2014-2018 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps3000aApi.h C header
file for PicoScope 3000 Series oscilloscopes using the ps3000a driver API
functions.
"""

from ctypes import *
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY
from picosdk.library import Library
from picosdk.constants import make_enum


class Ps3000alib(Library):
    def __init__(self):
        super(Ps3000alib, self).__init__("ps3000a")


ps3000a = Ps3000alib()

ps3000a.PS3000A_COUPLING = make_enum([
    'PS3000A_AC',
    'PS3000A_DC',
])

# Just use AC and DC.
ps3000a.PICO_COUPLING = {k[-2:]: v for k, v in ps3000a.PS3000A_COUPLING.items()}

# A tuple in an enum like this is 2 names for the same value.
ps3000a.PS3000A_CHANNEL = make_enum([
    "PS3000A_CHANNEL_A",
    "PS3000A_CHANNEL_B",
    "PS3000A_CHANNEL_C",
    "PS3000A_CHANNEL_D",
    ("PS3000A_EXTERNAL", "PS3000A_MAX_CHANNELS"),
    "PS3000A_TRIGGER_AUX",
    "PS3000A_MAX_TRIGGER_SOURCE",
])

# only include the normal analog channels for now:
ps3000a.PICO_CHANNEL = {k[-1]: v for k, v in ps3000a.PS3000A_CHANNEL.items() if "PS3000A_CHANNEL_" in k}

ps3000a.PS3000A_RANGE = make_enum([
    "PS3000A_10MV",
    "PS3000A_20MV",
    "PS3000A_50MV",
    "PS3000A_100MV",
    "PS3000A_200MV",
    "PS3000A_500MV",
    "PS3000A_1V",
    "PS3000A_2V",
    "PS3000A_5V",
    "PS3000A_10V",
    "PS3000A_20V",
    "PS3000A_50V",
    "PS3000A_MAX_RANGES",
])

ps3000a.PICO_VOLTAGE_RANGE = {
    v: float(k.split('_')[1][:-1]) if k[-2] != 'M' else (0.001 * float(k.split('_')[1][:-2]))
    for k, v in ps3000a.PS3000A_RANGE.items() if k != "PS3000A_MAX_RANGES"
}

ps3000a.PS3000A_RATIO_MODE = {
    'PS3000A_RATIO_MODE_NONE': 0,
    'PS3000A_RATIO_MODE_AGGREGATE': 1,
    'PS3000A_RATIO_MODE_DECIMATE': 2,
    'PS3000A_RATIO_MODE_AVERAGE': 4,
}

ps3000a.PS3000A_TIME_UNITS = make_enum([
    'PS3000A_FS',
    'PS3000A_PS',
    'PS3000A_NS',
    'PS3000A_US',
    'PS3000A_MS',
    'PS3000A_S',
    'PS3000A_MAX_TIME_UNITS',
])

ps3000a.PS3000A_DIGITAL_CHANNEL = make_enum([
    "PS3000A_DIGITAL_CHANNEL_0",
    "PS3000A_DIGITAL_CHANNEL_1",
    "PS3000A_DIGITAL_CHANNEL_2",
    "PS3000A_DIGITAL_CHANNEL_3",
    "PS3000A_DIGITAL_CHANNEL_4",
    "PS3000A_DIGITAL_CHANNEL_5",
    "PS3000A_DIGITAL_CHANNEL_6",
    "PS3000A_DIGITAL_CHANNEL_7",
    "PS3000A_DIGITAL_CHANNEL_8",
    "PS3000A_DIGITAL_CHANNEL_9",
    "PS3000A_DIGITAL_CHANNEL_10",
    "PS3000A_DIGITAL_CHANNEL_11",
    "PS3000A_DIGITAL_CHANNEL_12",
    "PS3000A_DIGITAL_CHANNEL_13",
    "PS3000A_DIGITAL_CHANNEL_14",
    "PS3000A_DIGITAL_CHANNEL_15",
    "PS3000A_DIGITAL_CHANNEL_16",
    "PS3000A_DIGITAL_CHANNEL_17",
    "PS3000A_DIGITAL_CHANNEL_18",
    "PS3000A_DIGITAL_CHANNEL_19",
    "PS3000A_DIGITAL_CHANNEL_20",
    "PS3000A_DIGITAL_CHANNEL_21",
    "PS3000A_DIGITAL_CHANNEL_22",
    "PS3000A_DIGITAL_CHANNEL_23",
    "PS3000A_DIGITAL_CHANNEL_24",
    "PS3000A_DIGITAL_CHANNEL_25",
    "PS3000A_DIGITAL_CHANNEL_26",
    "PS3000A_DIGITAL_CHANNEL_27",
    "PS3000A_DIGITAL_CHANNEL_28",
    "PS3000A_DIGITAL_CHANNEL_29",
    "PS3000A_DIGITAL_CHANNEL_30",
    "PS3000A_DIGITAL_CHANNEL_31",
    "PS3000A_MAX_DIGITAL_CHANNELS"
])

ps3000a.PS3000A_DIGITAL_DIRECTION = make_enum([
    "PS3000A_DIGITAL_DONT_CARE",
    "PS3000A_DIGITAL_DIRECTION_LOW",
    "PS3000A_DIGITAL_DIRECTION_HIGH",
    "PS3000A_DIGITAL_DIRECTION_RISING",
    "PS3000A_DIGITAL_DIRECTION_FALLING",
    "PS3000A_DIGITAL_DIRECTION_RISING_OR_FALLING",
    "PS3000A_DIGITAL_MAX_DIRECTION"
])

def _define_digital_port():
    PS3000A_DIGITAL_PORT0 = 0x80
    PS3000A_DIGITAL_PORT1 = PS3000A_DIGITAL_PORT0 + 1
    PS3000A_DIGITAL_PORT2 = PS3000A_DIGITAL_PORT0 + 2
    PS3000A_DIGITAL_PORT3 = PS3000A_DIGITAL_PORT0 + 3
    PS3000A_MAX_DIGITAL_PORTS = (PS3000A_DIGITAL_PORT3 - PS3000A_DIGITAL_PORT0) + 1

    return {k.upper(): v for k, v in locals().items() if k.startswith("PS3000A")}

ps3000a.PS3000A_DIGITAL_PORT = _define_digital_port()

ps3000a.PS3000A_TRIGGER_STATE = make_enum([
    "PS3000A_CONDITION_DONT_CARE",
    "PS3000A_CONDITION_TRUE",
    "PS3000A_CONDITION_FALSE",
    "PS3000A_CONDITION_MAX"
    ])
    
ps3000a.PS3000A_THRESHOLD_DIRECTION = make_enum([
    ("PS3000A_ABOVE", "PS3000A_INSIDE"),
    ("PS3000A_BELOW", "PS3000A_OUTSIDE","PS3000A_NONE"),
    ("PS3000A_RISING", "PS3000A_ENTER"),
    ("PS3000A_FALLING", "PS3000A_EXIT"),
    ("PS3000A_RISING_OR_FALLING", "PS3000A_ENTER_OR_EXIT"),
    "PS3000A_ABOVE_LOWER",
    "PS3000A_BELOW_LOWER",
    "PS3000A_RISING_LOWER",
    "PS3000A_FALLING_LOWER"
    "PS3000A_POSITIVE_RUNT",
    "PS3000A_NEGATIVE_RUNT"
    ])
    
ps3000a.PS3000A_THRESHOLD_MODE = make_enum([
    "PS3000A_LEVEL",
    "PS3000A_WINDOW"
    ])

class PS3000A_DIGITAL_CHANNEL_DIRECTIONS(Structure):
    _pack_ = 1
    _fields_ = [("channel", c_int32),
                ("direction", c_int32)]
                
ps3000a.PS3000A_DIGITAL_CHANNEL_DIRECTIONS = PS3000A_DIGITAL_CHANNEL_DIRECTIONS
                
class PS3000A_TRIGGER_CONDITIONS(Structure):
    _pack_ = 1
    _fields_ = [("channelA", c_uint32),
                ("channelB", c_uint32),
                ("channelC", c_uint32),
                ("channelD", c_uint32),
                ("external", c_uint32),
                ("aux", c_uint32),
                ("pulseWidthQualifier", c_uint32)]

ps3000a.PS3000A_TRIGGER_CONDITIONS = PS3000A_TRIGGER_CONDITIONS
                
class PS3000A_TRIGGER_CONDITIONS_V2(Structure):
    _pack_ = 1
    _fields_ = [("channelA", c_uint32),
                ("channelB", c_uint32),
                ("channelC", c_uint32),
                ("channelD", c_uint32),
                ("external", c_uint32),
                ("aux", c_uint32),
                ("pulseWidthQualifier", c_uint32),
                ("digital", c_uint32)]
ps3000a.PS3000A_TRIGGER_CONDITIONS_V2 = PS3000A_TRIGGER_CONDITIONS_V2
                
class PS3000A_TRIGGER_CHANNEL_PROPERTIES(Structure):
    _pack_ = 1
    _fields_ = [("thresholdUpper", c_int16),
                ("thresholdUpperHysteresis", c_uint16),
                ("thresholdLower", c_int16),
                ("thresholdLowerHysteresis", c_uint16),
                ("channel", c_uint32),
                ("thresholdMode", c_uint32)]
ps3000a.PS3000A_TRIGGER_CHANNEL_PROPERTIES = PS3000A_TRIGGER_CHANNEL_PROPERTIES
                
doc = """ PICO_STATUS ps3000aOpenUnit
    (
        int16_t *handle,
        int8_t  *serial
    ); """
ps3000a.make_symbol("_OpenUnit", "ps3000aOpenUnit", c_uint32, [c_void_p, c_char_p], doc)

doc = """ PICO_STATUS ps3000aOpenUnitAsync
    (
        int16_t *status,
        int8_t  *serial
    ); """
ps3000a.make_symbol("_OpenUnitAsync", "ps3000aOpenUnitAsync", c_uint32, [c_void_p, c_char_p], doc)

doc = """ PICO_STATUS ps3000aOpenUnitProgress
    (
        int16_t *handle,
        int16_t *progressPercent,
        int16_t *complete
    ); """
ps3000a.make_symbol("_OpenUnitProgress", "ps3000aOpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetUnitInfo
    (
        int16_t    handle,
        int8_t    *string,
        int16_t    stringLength,
        int16_t   *requiredSize,
        PICO_INFO  info
    ); """
ps3000a.make_symbol("_GetUnitInfo", "ps3000aGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32],
                    doc)

doc = """ PICO_STATUS ps3000aFlashLed
    (
        int16_t  handle,
        int16_t  start
    ); """
ps3000a.make_symbol("_FlashLed", "ps3000aFlashLed", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps3000aCloseUnit
    (
        int16_t  handle
    ); """
ps3000a.make_symbol("_CloseUnit", "ps3000aCloseUnit", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps3000aMemorySegments
    (
        int16_t   handle,
        uint32_t  nSegments,
        int32_t  *nMaxSamples
    ); """
ps3000a.make_symbol("_MemorySegments", "ps3000aMemorySegments", c_uint32, [c_int16, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps3000aSetChannel
    (
        int16_t          handle,
        PS3000a_CHANNEL  channel,
        int16_t          enabled,
        PS3000a_COUPLING type,
        PS3000a_RANGE    range,
        float            analogOffset
    ); """
ps3000a.make_symbol("_SetChannel", "ps3000aSetChannel", c_uint32,
                    [c_int16, c_int32, c_int16, c_int32, c_int32, c_float], doc)

doc = """ PICO_STATUS ps3000aSetDigitalPort
    (
        int16_t              handle,
        PS3000a_DIGITAL_PORT port,
        int16_t              enabled,
        int16_t              logicLevel
    ); """
ps3000a.make_symbol("_SetDigitalPort", "ps3000aSetDigitalPort", c_uint32, [c_int16, c_int32, c_int16, c_int16], doc)

doc = """ PICO_STATUS ps3000aSetBandwidthFilter
    (
        int16_t                    handle,
        PS3000A_CHANNEL            channel,
        PS3000A_BANDWIDTH_LIMITER  bandwidth
    ); """
ps3000a.make_symbol("_SetBandwidthFilter", "ps3000aSetBandwidthFilter", c_uint32, [c_int16, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps3000aSetNoOfCaptures
    (
        int16_t   handle,
        uint32_t  nCaptures
    ); """
ps3000a.make_symbol("_SetNoOfCaptures", "ps3000aSetNoOfCaptures", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps3000aGetTimebase
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        int32_t  *timeIntervalNanoseconds,
        int16_t   oversample,
        int32_t  *maxSamples,
        uint32_t  segmentIndex
    ); """
ps3000a.make_symbol("_GetTimebase", "ps3000aGetTimebase", c_uint32,
                    [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint32], doc)


doc = """ PICO_STATUS ps3000aGetTimebase2
    (
        int16_t  handle,
        uint32_t timebase,
        int32_t  noSamples,
        float   *timeIntervalNanoseconds,
        int16_t  oversample,
        int32_t *maxSamples,
        uint32_t segmentIndex
    ); """
ps3000a.make_symbol("_GetTimebase2", "ps3000aGetTimebase2", c_uint32,
                    [c_int16, c_uint32, c_int32, c_void_p, c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps3000aSetSigGenArbitrary
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
        PS3000A_SWEEP_TYPE          sweepType,
        PS3000A_EXTRA_OPERATIONS    operation,
        PS3000A_INDEX_MODE          indexMode,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS3000A_SIGGEN_TRIG_TYPE    triggerType,
        PS3000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps3000a.make_symbol("_SetSigGenArbitrary", "ps3000aSetSigGenArbitrary", c_uint32,
                    [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p, c_int32, c_int32,
                     c_int32,
                     c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps3000aSetSigGenBuiltIn
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        int16_t                     waveType,
        float                       startFrequency,
        float                       stopFrequency,
        float                       increment,
        float                       dwellTime,
        PS3000A_SWEEP_TYPE          sweepType,
        PS3000A_EXTRA_OPERATIONS    operation,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS3000A_SIGGEN_TRIG_TYPE    triggerType,
        PS3000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps3000a.make_symbol("_SetSigGenBuiltIn", "ps3000aSetSigGenBuiltIn", c_uint32,
                    [c_int16, c_int32, c_uint32, c_int16, c_float, c_float, c_float, c_float, c_int32, c_int32,
                     c_uint32,
                     c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps3000aSetSigGenPropertiesArbitrary
    (
        int16_t                     handle,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        PS3000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS3000A_SIGGEN_TRIG_TYPE    triggerType,
        PS3000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps3000a.make_symbol("_SetSigGenPropertiesArbitrary", "ps3000aSetSigGenPropertiesArbitrary", c_uint32,
                    [c_int16, c_uint32, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_uint32, c_int32, c_int32,
                     c_int16], doc)

doc = """ PICO_STATUS ps3000aSetSigGenPropertiesBuiltIn
    (
        int16_t                     handle,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS3000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS3000A_SIGGEN_TRIG_TYPE    triggerType,
        PS3000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps3000a.make_symbol("_SetSigGenPropertiesBuiltIn", "ps3000aSetSigGenPropertiesBuiltIn", c_uint32,
                    [c_int16, c_double, c_double, c_double, c_double, c_int32, c_uint32, c_uint32, c_int32, c_int32,
                     c_int16], doc)

doc = """ PICO_STATUS ps3000aSigGenFrequencyToPhase
    (
        int16_t             handle,
        double              frequency,
        PS3000A_INDEX_MODE  indexMode,
        uint32_t            bufferLength,
        uint32_t           *phase
    ); """
ps3000a.make_symbol("_SigGenFrequencyToPhase", "ps3000aSigGenFrequencyToPhase", c_uint32,
                    [c_int16, c_double, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps3000aSigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
ps3000a.make_symbol("_SigGenArbitraryMinMaxValues", "ps3000aSigGenArbitraryMinMaxValues", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetMaxEtsValues
    (
        int16_t  handle,
        int16_t *etsCycles,
        int16_t *etsInterleave
    ); """
ps3000a.make_symbol("_GetMaxEtsValues", "ps3000aGetMaxEtsValues", c_uint32, [c_int16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps3000aSigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    ); """
ps3000a.make_symbol("_SigGenSoftwareControl", "ps3000aSigGenSoftwareControl", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps3000aSetEts
    (
        int16_t           handle,
        PS3000A_ETS_MODE  mode,
        int16_t           etsCycles,
        int16_t           etsInterleave,
        int32_t          *sampleTimePicoseconds
    ); """
ps3000a.make_symbol("_SetEts", "ps3000aSetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps3000aSetSimpleTrigger
    (
        int16_t                      handle,
        int16_t                      enable,
        PS3000A_CHANNEL              source,
        int16_t                      threshold,
        PS3000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     delay,
        int16_t                      autoTrigger_ms
    ); """
ps3000a.make_symbol("_SetSimpleTrigger", "ps3000aSetSimpleTrigger", c_uint32,
                    [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16], doc)

doc = """ PICO_STATUS ps3000aSetTriggerDigitalPortProperties
    (
        int16_t                             handle,
        PS3000A_DIGITAL_CHANNEL_DIRECTIONS *directions,
        int16_t                             nDirections
    ); """
ps3000a.make_symbol("_SetTriggerDigitalPortProperties", "ps3000aSetTriggerDigitalPortProperties", c_uint32,
                    [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps3000aSetPulseWidthDigitalPortProperties
    (
        int16_t                             handle,
        PS3000A_DIGITAL_CHANNEL_DIRECTIONS *directions,
        int16_t                             nDirections
    ); """
ps3000a.make_symbol("_SetPulseWidthDigitalPortProperties", "ps3000aSetPulseWidthDigitalPortProperties", c_uint32,
                    [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps3000aSetTriggerChannelProperties
    (
        int16_t                             handle,
        PS3000A_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                             nChannelProperties,
        int16_t                             auxOutputEnable,
        int32_t                             autoTriggerMilliseconds
    ); """
ps3000a.make_symbol("_SetTriggerChannelProperties", "ps3000aSetTriggerChannelProperties", c_uint32,
                    [c_int16, c_void_p, c_int16, c_int16, c_int32], doc)

doc = """ PICO_STATUS ps3000aSetTriggerChannelConditions
    (
        int16_t                     handle,
        PS3000A_TRIGGER_CONDITIONS *conditions,
        int16_t                     nConditions
    ); """
ps3000a.make_symbol("_SetTriggerChannelConditions", "ps3000aSetTriggerChannelConditions", c_uint32,
                    [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps3000aSetTriggerChannelConditionsV2
    (
        int16_t                        handle,
        PS3000A_TRIGGER_CONDITIONS_V2 *conditions,
        int16_t                        nConditions
    ); """
ps3000a.make_symbol("_SetTriggerChannelConditionsV2", "ps3000aSetTriggerChannelConditionsV2", c_uint32,
                    [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps3000aSetTriggerChannelDirections
    (
        int16_t                      handle,
        PS3000A_THRESHOLD_DIRECTION  channelA,
        PS3000A_THRESHOLD_DIRECTION  channelB,
        PS3000A_THRESHOLD_DIRECTION  channelC,
        PS3000A_THRESHOLD_DIRECTION  channelD,
        PS3000A_THRESHOLD_DIRECTION  ext,
        PS3000A_THRESHOLD_DIRECTION  aux
    ); """
ps3000a.make_symbol("_SetTriggerChannelDirections", "ps3000aSetTriggerChannelDirections", c_uint32,
                    [c_int16, c_int32, c_int32, c_int32, c_int32, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps3000aSetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
ps3000a.make_symbol("_SetTriggerDelay", "ps3000aSetTriggerDelay", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps3000aSetPulseWidthQualifier
    (
        int16_t                      handle,
        PS3000A_PWQ_CONDITIONS      *conditions,
        int16_t                      nConditions,
        PS3000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     lower,
        uint32_t                     upper,
        PS3000A_PULSE_WIDTH_TYPE     type
    ); """
ps3000a.make_symbol("_SetPulseWidthQualifier", "ps3000aSetPulseWidthQualifier", c_uint32,
                    [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps3000aSetPulseWidthQualifierV2
    (
        int16_t                      handle,
        PS3000A_PWQ_CONDITIONS_V2   *conditions,
        int16_t                      nConditions,
        PS3000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     lower,
        uint32_t                     upper,
        PS3000A_PULSE_WIDTH_TYPE     type
    ); """
ps3000a.make_symbol("_SetPulseWidthQualifierV2", "ps3000aSetPulseWidthQualifierV2", c_uint32,
                    [c_int16, c_void_p, c_int16, c_int32, c_uint32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps3000aIsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
ps3000a.make_symbol("_IsTriggerOrPulseWidthQualifierEnabled", "ps3000aIsTriggerOrPulseWidthQualifierEnabled", c_uint32,
                    [c_int16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetTriggerTimeOffset64
    (
        int16_t             handle,
        int64_t            *time,
        PS3000A_TIME_UNITS *timeUnits,
        uint32_t            segmentIndex
    ); """
ps3000a.make_symbol("_GetTriggerTimeOffset", "ps3000aGetTriggerTimeOffset64", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps3000aGetValuesTriggerTimeOffsetBulk64
    (
        int16_t             handle,
        int64_t            *times,
        PS3000A_TIME_UNITS *timeUnits,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex
    ); """
ps3000a.make_symbol("_GetValuesTriggerTimeOffsetBulk", "ps3000aGetValuesTriggerTimeOffsetBulk64", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps3000aGetNoOfCaptures
    (
        int16_t   handle,
        uint32_t *nCaptures
    ); """
ps3000a.make_symbol("_GetNoOfCaptures", "ps3000aGetNoOfCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetNoOfProcessedCaptures
    (
        int16_t   handle,
        uint32_t *nProcessedCaptures
    ); """
ps3000a.make_symbol("_GetNoOfProcessedCaptures", "ps3000aGetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps3000aSetDataBuffer
    (
        int16_t            handle,
        int32_t            channelOrPort,
        int16_t           *buffer,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS3000a_RATIO_MODE mode
    ); """
ps3000a.make_symbol("_SetDataBuffer", "ps3000aSetDataBuffer", c_uint32,
                    [c_int16, c_int32, c_void_p, c_int32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps3000aSetDataBuffers
    (
        int16_t            handle,
        int32_t            channelOrPort,
        int16_t           *bufferMax,
        int16_t           *bufferMin,
        int32_t            bufferLth,
        uint32_t           segmentIndex,
        PS3000a_RATIO_MODE mode
    ); """
ps3000a.make_symbol("_SetDataBuffers", "ps3000aSetDataBuffers", c_uint32,
                    [c_int16, c_int32, c_void_p, c_void_p, c_int32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps3000aSetEtsTimeBuffer
    (
        int16_t    handle,
        int64_t *buffer,
        int32_t     bufferLth
    ); """
ps3000a.make_symbol("_SetEtsTimeBuffer", "ps3000aSetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps3000aIsReady
    (
        int16_t  handle,
        int16_t *ready
    ); """
ps3000a.make_symbol("_IsReady", "ps3000aIsReady", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps3000aRunBlock
    (
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        int16_t            oversample,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps3000aBlockReady  lpReady,
        void              *pParameter
    ); """
ps3000a.make_symbol("_RunBlock", "ps3000aRunBlock", c_uint32,
                    [c_int16, c_int32, c_int32, c_uint32, c_int16, c_void_p, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps3000aRunStreaming
    (
        int16_t             handle,
        uint32_t            *sampleInterval,
        PS3000A_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t            maxPreTriggerSamples,
        uint32_t            maxPostPreTriggerSamples,
        int16_t             autoStop,
        uint32_t            downSampleRatio,
        PS3000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            overviewBufferSize
    ); """
ps3000a.make_symbol("_RunStreaming", "ps3000aRunStreaming", c_uint32,
                    [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32], doc)

doc = """ PICO_STATUS ps3000aGetStreamingLatestValues
    (
        int16_t                handle,
        ps3000aStreamingReady  lpPs3000aReady,
        void                   *pParameter
    ); """
ps3000a.make_symbol("_GetStreamingLatestValues", "ps3000aGetStreamingLatestValues", c_uint32,
                    [c_int16, c_void_p, c_void_p], doc)

doc = """ void *ps3000aStreamingReady
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

ps3000a.StreamingReadyType = C_CALLBACK_FUNCTION_FACTORY(None,
                                                         c_int16,
                                                         c_int32,
                                                         c_uint32,
                                                         c_int16,
                                                         c_uint32,
                                                         c_int16,
                                                         c_int16,
                                                         c_void_p)

ps3000a.StreamingReadyType.__doc__ = doc

doc = """ PICO_STATUS ps3000aNoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
ps3000a.make_symbol("_NoOfStreamingValues", "ps3000aNoOfStreamingValues", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetMaxDownSampleRatio
(
  int16_t               handle,
  uint32_t       noOfUnaggreatedSamples,
  uint32_t      *maxDownSampleRatio,
  PS3000A_RATIO_MODE  downSampleRatioMode,
  uint32_t      segmentIndex
); """
ps3000a.make_symbol("_GetMaxDownSampleRatio", "ps3000aGetMaxDownSampleRatio", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_int32, c_uint32], doc)

doc = """ PICO_STATUS ps3000aGetValues
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS3000a_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
ps3000a.make_symbol("_GetValues", "ps3000aGetValues", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetValuesBulk
    (
        int16_t             handle,
        uint32_t           *noOfSamples,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        uint32_t            downSampleRatio,
        PS3000A_RATIO_MODE  downSampleRatioMode,
        int16_t            *overflow
    ); """
ps3000a.make_symbol("_GetValuesBulk", "ps3000aGetValuesBulk", c_uint32,
                    [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetValuesAsync
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t            noOfSamples,
        uint32_t            downSampleRatio,
        PS3000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        void               *lpDataReady,
        void               *pParameter
    ); """
ps3000a.make_symbol("_GetValuesAsync", "ps3000aGetValuesAsync", c_uint32,
                    [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetValuesOverlapped
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS3000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
ps3000a.make_symbol("_GetValuesOverlapped", "ps3000aGetValuesOverlapped", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetValuesOverlappedBulk
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS3000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        int16_t            *overflow
    ); """
ps3000a.make_symbol("_GetValuesOverlappedBulk", "ps3000aGetValuesOverlappedBulk", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetTriggerInfoBulk
    (
        int16_t               handle,
        PS3000A_TRIGGER_INFO *triggerInfo,
        uint32_t              fromSegmentIndex,
        uint32_t              toSegmentIndex
    ); """
ps3000a.make_symbol("_GetTriggerInfoBulk", "ps3000aGetTriggerInfoBulk", c_uint32,
                    [c_int16, c_void_p, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps3000aStop
    (
        int16_t  handle
    ); """
ps3000a.make_symbol("_Stop", "ps3000aStop", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps3000aHoldOff
    (
        int16_t               handle,
        uint64_t              holdoff,
        PS3000A_HOLDOFF_TYPE  type
    ); """
ps3000a.make_symbol("_HoldOff", "ps3000aHoldOff", c_uint32, [c_int16, c_uint64, c_int32], doc)

doc = """ PICO_STATUS ps3000aGetChannelInformation
    (
        int16_t               handle,
        PS3000A_CHANNEL_INFO  info,
        int32_t               probe,
        int32_t              *ranges,
        int32_t              *length,
        int32_t               channels
    ); """
ps3000a.make_symbol("_GetChannelInformation", "ps3000aGetChannelInformation", c_uint32,
                    [c_int16, c_int32, c_int32, c_void_p, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps3000aEnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
ps3000a.make_symbol("_EnumerateUnits", "ps3000aEnumerateUnits", c_uint32, [c_void_p, c_char_p, c_void_p], doc)

doc = """ PICO_STATUS ps3000aPingUnit
    (
        int16_t  handle
    ); """
ps3000a.make_symbol("_PingUnit", "ps3000aPingUnit", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps3000aMaximumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
ps3000a.make_symbol("_MaximumValue", "ps3000aMaximumValue", c_uint32, [c_int16, c_void_p], doc)

doc = """" PICO_STATUS ps3000aMinimumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
ps3000a.make_symbol("_MinimumValue", "ps3000aMinimumValue", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetAnalogueOffset
    (
        int16_t           handle,
        PS3000A_RANGE     range,
        PS3000A_COUPLING  coupling,
        float            *maximumVoltage,
        float            *minimumVoltage
    ); """
ps3000a.make_symbol("_GetAnalogueOffset", "ps3000aGetAnalogueOffset", c_uint32,
                    [c_int16, c_int32, c_int32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps3000aGetMaxSegments
    (
        int16_t   handle,
        uint32_t *maxSegments
    ); """
ps3000a.make_symbol("_GetMaxSegments", "ps3000aGetMaxSegments", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps3000aChangePowerSource
    (
        int16_t     handle,
        PICO_STATUS powerState
    ); """
ps3000a.make_symbol("_ChangePowerSource", "ps3000aChangePowerSource", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps3000aCurrentPowerSource
    (
        int16_t handle
    ); """
ps3000a.make_symbol("_CurrentPowerSource", "ps3000aCurrentPowerSource", c_uint32, [c_int16, c_uint32], doc)

ps3000a.INI_LOGIC_VOLTS = 1.5
