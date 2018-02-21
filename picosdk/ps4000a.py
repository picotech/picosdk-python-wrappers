#
# Copyright (C) 2015-2017 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the ps4000aApi.h C header
file for PicoScope 4000 Series oscilloscopes using the ps4000a driver API
functions.
"""

from ctypes import *
from picosdk.library import Library


class ps4000alib(Library):
    def __init__(self):
        super(ps4000alib, self).__init__("ps4000a")


ps4000a = ps4000alib()

doc = """ PICO_STATUS ps4000aOpenUnit
    (
        int16_t *handle,
        int8_t  *serial
    ); """
ps4000a.make_symbol("_OpenUnit", "ps4000aOpenUnit", c_uint32, [c_void_p, c_char_p], doc)

doc = """ PICO_STATUS ps4000aOpenUnitAsync
    (
        int16_t *status,
        int8_t  *serial
    ); """
ps4000a.make_symbol("_OpenUnitAsync", "ps4000aOpenUnitAsync", c_uint32, [c_void_p, c_char_p], doc)

doc = """ PICO_STATUS ps4000aOpenUnitProgress
    (
        int16_t *handle,
        int16_t *progressPercent,
        int16_t *complete
    ); """
ps4000a.make_symbol("_OpenUnitProgress", "ps4000aOpenUnitProgress", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetUnitInfo
    (
        int16_t    handle,
        int8_t    *string,
        int16_t    stringLength,
        int16_t   *requiredSize,
        PICO_INFO  info
    ); """
ps4000a.make_symbol("_GetUnitInfo", "ps4000aGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32],
                    doc)

doc = """ PICO_STATUS ps4000aFlashLed
    (
        int16_t  handle,
        int16_t  start
    ); """
ps4000a.make_symbol("_FlashLed", "ps4000aFlashLed", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps4000aSetChannelLed
    (
        int16_t                      handle,
        PS4000A_CHANNEL_LED_SETTING *ledStates,
        uint16_t                     nLedStates
    ); """
ps4000a.make_symbol("_SetChannelLed", "ps4000aSetChannelLed", c_uint32, [c_int16, c_void_p, c_uint16], doc)

doc = """ PICO_STATUS ps4000aIsLedFlashing
    (
        int16_t  handle,
        int16_t *status
    ); """
ps4000a.make_symbol("_IsLedFlashing", "ps4000aIsLedFlashing", c_uint32, [c_int16, c_void_p, c_uint16], doc)

doc = """ PICO_STATUS ps4000aCloseUnit
    (
        int16_t  handle
    ); """
ps4000a.make_symbol("_CloseUnit", "ps4000aCloseUnit", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps4000aMemorySegments
    (
        int16_t   handle,
        uint32_t  nSegments,
        int32_t  *nMaxSamples
    ); """
ps4000a.make_symbol("_MemorySegments", "ps4000aMemorySegments", c_uint32, [c_int16, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps4000aSetChannel
    (
        int16_t           handle,
        PS4000A_CHANNEL   channel,
        int16_t           enabled,
        PS4000A_COUPLING  type,
        PS4000A_RANGE     range,
        float             analogOffset
    ); """
ps4000a.make_symbol("_SetChannel", "ps4000aSetChannel", c_uint32,
                    [c_int16, c_int32, c_int16, c_int32, c_int32, c_float], doc)

doc = """ PICO_STATUS ps4000aSetBandwidthFilter
    (
        int16_t                    handle,
        PS4000A_CHANNEL            channel,
        PS4000A_BANDWIDTH_LIMITER  bandwidth
    ); """
ps4000a.make_symbol("_SetBandwidthFilter", "ps4000aSetBandwidthFilter", c_uint32, [c_int16, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps4000aApplyResistanceScaling
    (
        int16_t          handle,
        PS4000A_CHANNEL  channel,
        PS4000A_RANGE    range,
        int16_t         *bufferMax,
        int16_t         *bufferMin,
        uint32_t         buffertLth,
        int16_t         *overflow
    ); """
ps4000a.make_symbol("_ApplyResistanceScaling", "ps4000aApplyResistanceScaling", c_uint32,
                    [c_int16, c_int32, c_int32, c_int16, c_int16, c_uint32, c_int16], doc)

doc = """ PICO_STATUS ps4000aGetTimebase
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        int32_t  *timeIntervalNanoseconds,
        int32_t  *maxSamples,
        uint32_t  segmentIndex
    ); """
ps4000a.make_symbol('_GetTimebase', 'ps4000aGetTimebase', c_uint32,
                    [c_int16, c_uint32, c_int32, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps4000aGetTimebase2
    (
        int16_t   handle,
        uint32_t  timebase,
        int32_t   noSamples,
        float    *timeIntervalNanoseconds,
        int32_t  *maxSamples,
        uint32_t  segmentIndex
    ); """
ps4000a.make_symbol("_GetTimebase2", "ps4000aGetTimebase2", c_uint32,
                    [c_int16, c_uint32, c_int32, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps4000aSetSigGenArbitrary
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
        PS4000A_SWEEP_TYPE          sweepType,
        PS4000A_EXTRA_OPERATIONS    operation,
        PS4000A_INDEX_MODE          indexMode,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS4000A_SIGGEN_TRIG_TYPE    triggerType,
        PS4000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps4000a.make_symbol("_SetSigGenArbitrary", "ps4000aSetSigGenArbitrary", c_uint32,
                    [c_int16, c_int32, c_uint32, c_uint32, c_uint32, c_uint32, c_uint32, c_void_p,
                     c_int32, c_int32, c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps4000aSetSigGenBuiltIn
    (
        int16_t                     handle,
        int32_t                     offsetVoltage,
        uint32_t                    pkToPk,
        PS4000A_WAVE_TYPE           waveType,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS4000A_SWEEP_TYPE          sweepType,
        PS4000A_EXTRA_OPERATIONS    operation,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS4000A_SIGGEN_TRIG_TYPE    triggerType,
        PS4000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps4000a.make_symbol("_SetSigGenBuiltIn", "ps4000aSetSigGenBuiltIn", c_uint32,
                    [c_int16, c_int32, c_uint32, c_int32, c_double, c_double, c_double, c_double,
                     c_int32, c_int32, c_uint32, c_uint32, c_int32, c_int32, c_int16], doc)

doc = """ PICO_STATUS ps4000aSetSigGenPropertiesArbitrary
    (
        int16_t                     handle,
        uint32_t                    startDeltaPhase,
        uint32_t                    stopDeltaPhase,
        uint32_t                    deltaPhaseIncrement,
        uint32_t                    dwellCount,
        PS4000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS4000A_SIGGEN_TRIG_TYPE    triggerType,
        PS4000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps4000a.make_symbol("_SetSigGenPropertiesArbitrary", "ps4000aSetSigGenPropertiesArbitrary", c_uint32,
                    [c_int16, c_uint32, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_uint32, c_int32, c_int32,
                     c_int16], doc)

doc = """ PICO_STATUS ps4000aSetSigGenPropertiesBuiltIn
    (
        int16_t                     handle,
        double                      startFrequency,
        double                      stopFrequency,
        double                      increment,
        double                      dwellTime,
        PS4000A_SWEEP_TYPE          sweepType,
        uint32_t                    shots,
        uint32_t                    sweeps,
        PS4000A_SIGGEN_TRIG_TYPE    triggerType,
        PS4000A_SIGGEN_TRIG_SOURCE  triggerSource,
        int16_t                     extInThreshold
    ); """
ps4000a.make_symbol("_SetSigGenPropertiesBuiltIn", "ps4000aSetSigGenPropertiesBuiltIn", c_uint32,
                    [c_int16, c_double, c_double, c_double, c_double, c_int32, c_uint32, c_uint32, c_int32, c_int32,
                     c_int16], doc)

doc = """ PICO_STATUS ps4000aSigGenFrequencyToPhase
    (
        int16_t             handle,
        double              frequency,
        PS4000A_INDEX_MODE  indexMode,
        uint32_t            bufferLength,
        uint32_t           *phase
    ); """
ps4000a.make_symbol("_SigGenFrequencyToPhase", "ps4000aSigGenFrequencyToPhase", c_uint32,
                    [c_int16, c_double, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps4000aSigGenArbitraryMinMaxValues
    (
        int16_t   handle,
        int16_t  *minArbitraryWaveformValue,
        int16_t  *maxArbitraryWaveformValue,
        uint32_t *minArbitraryWaveformSize,
        uint32_t *maxArbitraryWaveformSize
    ); """
ps4000a.make_symbol("_SigGenArbitraryMinMaxValues", "ps4000aSigGenArbitraryMinMaxValues", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000aSigGenSoftwareControl
    (
        int16_t  handle,
        int16_t  state
    );"""
ps4000a.make_symbol("_SigGenSoftwareControl", "ps4000aSigGenSoftwareControl", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps4000aSetEts
    (
        int16_t           handle,
        PS4000A_ETS_MODE  mode,
        int16_t           etsCycles,
        int16_t           etsInterleave,
        int32_t          *sampleTimePicoseconds
    ); """
ps4000a.make_symbol("_SetEts", "ps4000aSetEts", c_uint32, [c_int16, c_int32, c_int16, c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000aSetTriggerChannelProperties
    (
        int16_t                             handle,
        PS4000A_TRIGGER_CHANNEL_PROPERTIES *channelProperties,
        int16_t                             nChannelProperties,
        int16_t                             auxOutputEnable,
        int32_t                             autoTriggerMilliseconds
    ); """
ps4000a.make_symbol("_SetTriggerChannelProperties", "ps4000aSetTriggerChannelProperties", c_uint32,
                    [c_int16, c_void_p, c_int16, c_int16, c_int32], doc)

doc = """ PICO_STATUS ps4000aSetTriggerChannelConditions
    (
        int16_t                  handle,
        PS4000A_CONDITION       *conditions,
        int16_t                  nConditions,
        PS4000A_CONDITIONS_INFO  info
    ); """
ps4000a.make_symbol("_SetTriggerChannelConditions", "ps4000aSetTriggerChannelConditions", c_uint32,
                    [c_int16, c_void_p, c_int16, c_int32], doc)

doc = """ PICO_STATUS ps4000aSetTriggerChannelDirections
    (
        int16_t            handle,
        PS4000A_DIRECTION *directions,
        int16_t            nDirections
    ); """
ps4000a.make_symbol("_SetTriggerChannelDirections", "ps4000aSetTriggerChannelDirections", c_uint32,
                    [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps4000aSetSimpleTrigger
    (
        int16_t                      handle,
        int16_t                      enable,
        PS4000A_CHANNEL              source,
        int16_t                      threshold,
        PS4000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     delay,
        int16_t                      autoTrigger_ms
    ); """
ps4000a.make_symbol("_SetSimpleTrigger", "ps4000aSetSimpleTrigger", c_uint32,
                    [c_int16, c_int16, c_int32, c_int16, c_int32, c_uint32, c_int16], doc)

doc = """ PICO_STATUS ps4000aSetTriggerDelay
    (
        int16_t   handle,
        uint32_t  delay
    ); """
ps4000a.make_symbol("_SetTriggerDelay", "ps4000aSetTriggerDelay", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps4000aSetPulseWidthQualifierProperties
    (
        int16_t                      handle,
        PS4000A_THRESHOLD_DIRECTION  direction,
        uint32_t                     lower,
        uint32_t                     upper,
        PS4000A_PULSE_WIDTH_TYPE     type
    ); """
ps4000a.make_symbol("_SetPulseWidthQualifierProperties", "ps4000aSetPulseWidthQualifierProperties", c_uint32,
                    [c_int16, c_int32, c_uint32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps4000aSetPulseWidthQualifierConditions
    (
        int16_t                  handle,
        PS4000A_CONDITION       *conditions,
        int16_t                  nConditions,
        PS4000A_CONDITIONS_INFO  info
    ); """
ps4000a.make_symbol("_SetPulseWidthQualifierConditions", "ps4000aSetPulseWidthQualifierConditions", c_uint32,
                    [c_int16, c_void_p, c_int16, c_int32], doc)

doc = """ PICO_STATUS ps4000aIsTriggerOrPulseWidthQualifierEnabled
    (
        int16_t  handle,
        int16_t *triggerEnabled,
        int16_t *pulseWidthQualifierEnabled
    ); """
ps4000a.make_symbol("_IsTriggerOrPulseWidthQualifierEnabled", "ps4000aIsTriggerOrPulseWidthQualifierEnabled", c_uint32,
                    [c_int16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetTriggerTimeOffset
    (
        int16_t             handle,
        uint32_t           *timeUpper,
        uint32_t           *timeLower,
        PS4000A_TIME_UNITS *timeUnits,
        uint32_t            segmentIndex
    ); """
ps4000a.make_symbol("_GetTriggerTimeOffset", "ps4000aGetTriggerTimeOffset", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps4000aGetTriggerTimeOffset64
    (
        int16_t             handle,
        int64_t            *time,
        PS4000A_TIME_UNITS *timeUnits,
        uint32_t            segmentIndex
    ); """
ps4000a.make_symbol("_GetTriggerTimeOffset64", "ps4000aGetTriggerTimeOffset64", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps4000aGetValuesTriggerTimeOffsetBulk
    (
        int16_t             handle,
        uint32_t           *timesUpper,
        uint32_t           *timesLower,
        PS4000A_TIME_UNITS *timeUnits,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex
    ); """
ps4000a.make_symbol("_GetValuesTriggerTimeOffsetBulk", "ps4000aGetValuesTriggerTimeOffsetBulk", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_void_p, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps4000aGetValuesTriggerTimeOffsetBulk64
    (
        int16_t             handle,
        int64_t            *times,
        PS4000A_TIME_UNITS *timeUnits,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex
    ); """
ps4000a.make_symbol("_GetValuesTriggerTimeOffsetBulk64", "ps4000aGetValuesTriggerTimeOffsetBulk64", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps4000aSetDataBuffers
    (
        int16_t             handle,
        PS4000A_CHANNEL     channel,
        int16_t            *bufferMax,
        int16_t            *bufferMin,
        int32_t             bufferLth,
        uint32_t            segmentIndex,
        PS4000A_RATIO_MODE  mode
    ); """
ps4000a.make_symbol("_SetDataBuffers", "ps4000aSetDataBuffers", c_uint32,
                    [c_int16, c_int32, c_void_p, c_void_p, c_int32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps4000aSetDataBuffer
    (
        int16_t             handle,
        PS4000A_CHANNEL     channel,
        int16_t            *buffer,
        int32_t             bufferLth,
        uint32_t            segmentIndex,
        PS4000A_RATIO_MODE  mode
    ); """
ps4000a.make_symbol("_SetDataBuffer", "ps4000aSetDataBuffer", c_uint32,
                    [c_int16, c_int32, c_void_p, c_int32, c_uint32, c_int32], doc)

doc = """ PICO_STATUS ps4000aSetEtsTimeBuffer
    (
        int16_t  handle,
        int64_t *buffer,
        int32_t  bufferLth
    ); """
ps4000a.make_symbol("_SetEtsTimeBuffer", "ps4000aSetEtsTimeBuffer", c_uint32, [c_int16, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps4000aSetEtsTimeBuffers
    (
        int16_t   handle,
        uint32_t *timeUpper,
        uint32_t *timeLower,
        int32_t   bufferLth
    ); """
ps4000a.make_symbol("_SetEtsTimeBuffers", "ps4000aSetEtsTimeBuffers", c_uint32, [c_int16, c_void_p, c_void_p, c_int32],
                    doc)

doc = """ PICO_STATUS ps4000aIsReady
    (
        int16_t  handle,
        int16_t *ready
    ); """
ps4000a.make_symbol("_IsReady", "ps4000aIsReady", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000aRunBlock
    (
        int16_t            handle,
        int32_t            noOfPreTriggerSamples,
        int32_t            noOfPostTriggerSamples,
        uint32_t           timebase,
        int32_t           *timeIndisposedMs,
        uint32_t           segmentIndex,
        ps4000aBlockReady  lpReady,
        void              *pParameter
    ); """
ps4000a.make_symbol("_RunBlock", "ps4000aRunBlock", c_uint32,
                    [c_int16, c_int32, c_int32, c_uint32, c_void_p, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000aRunStreaming
    (
        int16_t             handle,
        uint32_t           *sampleInterval,
        PS4000A_TIME_UNITS  sampleIntervalTimeUnits,
        uint32_t            maxPreTriggerSamples,
        uint32_t            maxPostTriggerSamples,
        int16_t             autoStop,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            overviewBufferSize
    ); """
ps4000a.make_symbol("_RunStreaming", "ps4000aRunStreaming", c_uint32,
                    [c_int16, c_void_p, c_int32, c_uint32, c_uint32, c_int16, c_uint32, c_int32, c_uint32], doc)

doc = """ PICO_STATUS ps4000aGetStreamingLatestValues
    (
        int16_t                handle,
        ps4000aStreamingReady  lpPs4000aReady,
        void                  *pParameter
    ); """
ps4000a.make_symbol("_GetStreamingLatestValues", "ps4000aGetStreamingLatestValues", c_uint32,
                    [c_int16, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000aNoOfStreamingValues
    (
        int16_t   handle,
        uint32_t *noOfValues
    ); """
ps4000a.make_symbol("_NoOfStreamingValues", "ps4000aNoOfStreamingValues", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetMaxDownSampleRatio
    (
        int16_t             handle,
        uint32_t            noOfUnaggreatedSamples,
        uint32_t           *maxDownSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex
    ); """
ps4000a.make_symbol("_GetMaxDownSampleRatio", "ps4000aGetMaxDownSampleRatio", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_int32, c_uint32], doc)

doc = """ PICO_STATUS ps4000aGetValues
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
ps4000a.make_symbol("_GetValues", "ps4000aGetValues", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetValuesAsync
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t            noOfSamples,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        void               *lpDataReady,
        void               *pParameter
    ); """
ps4000a.make_symbol("_GetValuesAsync", "ps4000aGetValuesAsync", c_uint32,
                    [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetValuesBulk
    (
        int16_t             handle,
        uint32_t           *noOfSamples,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        int16_t            *overflow
    ); """
ps4000a.make_symbol("_GetValuesBulk", "ps4000aGetValuesBulk", c_uint32,
                    [c_int16, c_void_p, c_uint32, c_uint32, c_uint32, c_int32, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetValuesOverlapped
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            segmentIndex,
        int16_t            *overflow
    ); """
ps4000a.make_symbol("_GetValuesOverlapped", "ps4000aGetValuesOverlapped", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetValuesOverlappedBulk
    (
        int16_t             handle,
        uint32_t            startIndex,
        uint32_t           *noOfSamples,
        uint32_t            downSampleRatio,
        PS4000A_RATIO_MODE  downSampleRatioMode,
        uint32_t            fromSegmentIndex,
        uint32_t            toSegmentIndex,
        int16_t            *overflow
    ); """
ps4000a.make_symbol("_GetValuesOverlappedBulk", "ps4000aGetValuesOverlappedBulk", c_uint32,
                    [c_int16, c_uint32, c_void_p, c_uint32, c_int32, c_uint32, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS ps4000aEnumerateUnits
    (
        int16_t *count,
        int8_t  *serials,
        int16_t *serialLth
    ); """
ps4000a.make_symbol("_EnumerateUnits", "ps4000aEnumerateUnits", c_uint32, [c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetChannelInformation
    (
        int16_t               handle,
        PS4000A_CHANNEL_INFO  info,
        int32_t               probe,
        int32_t              *ranges,
        int32_t              *length,
        int32_t               channels
    ); """
ps4000a.make_symbol("_GetChannelInformation", "ps4000aGetChannelInformation", c_uint32,
                    [c_int16, c_int32, c_int32, c_void_p, c_void_p, c_int32], doc)

doc = """ PICO_STATUS ps4000aConnectDetect
    (
        int16_t                 handle,
        PS4000A_CONNECT_DETECT *sensor,
        int16_t                 nSensors
    ); """
ps4000a.make_symbol("_ConnectDetect", "ps4000aConnectDetect", c_uint32, [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps4000aMaximumValue
    (
        int16_t  handle,
        int16_t *value
    ); """
ps4000a.make_symbol("_MaximumValue", "ps4000aMaximumValue", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000aMinimumValue
    (
        int16_t		handle,
        int16_t * value
    ); """
ps4000a.make_symbol("_MinimumValue", "ps4000aMinimumValue", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetAnalogueOffset
    (
        int16_t           handle,
        PS4000A_RANGE     range,
        PS4000A_COUPLING  coupling,
        float            *maximumVoltage,
        float            *minimumVoltage
    ); """
ps4000a.make_symbol("_GetAnalogueOffset", "ps4000aGetAnalogueOffset", c_uint32,
                    [c_int16, c_int32, c_int32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetMaxSegments
    (
        int16_t   handle,
        uint32_t *maxSegments
    ); """
ps4000a.make_symbol("_GetMaxSegments", "ps4000aGetMaxSegments", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000aChangePowerSource
    (
        int16_t      handle,
        PICO_STATUS  powerState
    ); """
ps4000a.make_symbol("_ChangePowerSource", "ps4000aChangePowerSource", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps4000aCurrentPowerSource
    (
        int16_t  handle
    ); """
ps4000a.make_symbol("_CurrentPowerSource", "ps4000aCurrentPowerSource", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps4000aStop
    (
        int16_t  handle
    ); """
ps4000a.make_symbol("_Stop", "ps4000aStop", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps4000aPingUnit
    (
        int16_t  handle
    ); """
ps4000a.make_symbol("_PingUnit", "ps4000aPingUnit", c_uint32, [c_int16, ], doc)

doc = """ PICO_STATUS ps4000aSetNoOfCaptures
    (
        int16_t   handle,
        uint32_t  nCaptures
    ); """
ps4000a.make_symbol("_SetNoOfCaptures", "ps4000aSetNoOfCaptures", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps4000aGetNoOfCaptures
    (
        int16_t   handle,
        uint32_t *nCaptures
    ); """
ps4000a.make_symbol("_GetNoOfCaptures", "ps4000aGetNoOfCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetNoOfProcessedCaptures
    (
        int16_t   handle,
        uint32_t *nProcessedCaptures
    ); """
ps4000a.make_symbol("_GetNoOfProcessedCaptures", "ps4000aGetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000aDeviceMetaData
    (
        int16_t                 handle,
        int8_t                 *settings,
        int32_t                *nSettingsLength,
        PS4000A_META_TYPE       type,
        PS4000A_META_OPERATION  operation,
        PS4000A_META_FORMAT     format
    ); """
ps4000a.make_symbol("_DeviceMetaData", "ps4000aDeviceMetaData", c_uint32,
                    [c_int16, c_void_p, c_void_p, c_int32, c_int32, c_int32], doc)

doc = """ PICO_STATUS ps4000aGetString
    (
        int16_t            handle,
        PICO_STRING_VALUE  stringValue,
        int8_t            *string,
        int32_t           *stringLength
    ); """
ps4000a.make_symbol("_GetString", "ps4000aGetString", c_uint32, [c_int16, c_int32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps4000aGetCommonModeOverflow
    (
        int16_t   handle,
        uint16_t *overflow
    ); """
ps4000a.make_symbol("_GetCommonModeOverflow", "ps4000aGetCommonModeOverflow", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps4000aSetFrequencyCounter
    (
        int16_t                          handle,
        PS4000A_CHANNEL                  channel,
        int16_t                          enabled,
        PS4000A_FREQUENCY_COUNTER_RANGE  range,
        int16_t                          thresholdMajor,
        int16_t                          thresholdMinor
    ); """
ps4000a.make_symbol("_SetFrequencyCounter", "ps4000aSetFrequencyCounter", c_uint32,
                    [c_int16, c_int32, c_int16, c_int32, c_int16, c_int16], doc)
