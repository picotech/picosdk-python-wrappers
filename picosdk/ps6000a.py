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

doc = """ void ps6000aBlockReady
    (
        int16_t    handle,
        PICO_STATUS    status,
        PICO_POINTER    pParameter
    ); """
ps6000a.BlockReadyType = C_CALLBACK_FUNCTION_FACTORY(None,
                                                     c_int16,
                                                     c_uint32,
                                                     c_void_p)
ps6000a.BlockReadyType.__doc__ = doc

doc = """ void ps6000aStreamingReady
    (
        int16_t    handle,
        int64_t    noOfSamples,
        uint64_t    bufferIndex,
        uint32_t    startIndex,
        int16_t    overflow,
        uint32_t    triggerAt,
        int16_t    triggered,
        int16_t    autoStop,
        PICO_POINTER    pParameter
    ); """
ps6000a.StreamingReadyType = C_CALLBACK_FUNCTION_FACTORY(None,
                                                         c_int16,
                                                         c_int64,
                                                         c_uint64,
                                                         c_uint32,
                                                         c_int16,
                                                         c_uint32,
                                                         c_int16,
                                                         c_int16,
                                                         c_void_p)
ps6000a.StreamingReadyType.__doc__ = doc

doc = """ void ps6000aDataReady
    (
        int16_t    handle,
        PICO_STATUS    status,
        uint64_t    noOfSamples,
        int16_t    overflow,
        PICO_POINTER    pParameter
    ); """
ps6000a.DataReadyType = C_CALLBACK_FUNCTION_FACTORY(None,
                                                    c_int16,
                                                    c_uint32,
                                                    c_uint64,
                                                    c_int16,
                                                    c_void_p)
ps6000a.DataReadyType.__doc__ = doc

doc = """ void ps6000aProbeInteractions
    (
        int16_t    handle,
        PICO_STATUS    status,
        PICO_USER_PROBE_INTERACTIONS    *probes,
        uint32_t    nProbes
    ); """
ps6000a.ProbeInteractionsType = C_CALLBACK_FUNCTION_FACTORY(None,
                                                            c_int16,
                                                            c_uint32,
                                                            c_void_p,
                                                            c_uint32)
ps6000a.ProbeInteractionsType.__doc__ = doc

doc = """ void ps6000aDigitalPortInteractions
    (
        int16_t    handle,
        PICO_STATUS    status,
        PICO_DIGITAL_PORT_INTERACTIONS    *ports,
        uint32_t    nPorts
    ); """
ps6000a.DigitalPortInteractionsType = C_CALLBACK_FUNCTION_FACTORY(None,
                                                                  c_int16,
                                                                  c_uint32,
                                                                  c_void_p,
                                                                  c_uint32)
ps6000a.DigitalPortInteractionsType.__doc__ = doc

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

doc = """ PICO_STATUS ps6000aFlashLed
    (
        int16_t    handle,
        int16_t    start
    ); """
ps6000a.make_symbol("_FlashLed", "ps6000aFlashLed", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps6000aMemorySegments
    (
        int16_t    handle,
        uint64_t    nSegments,
        uint64_t    *nMaxSegments
    ); """
ps6000a.make_symbol("_MemorySegments", "ps6000aMemorySegments", c_uint32, [c_int16, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS ps6000aMemorySegmentsBySamples
    (
        int16_t    handle,
        uint64_t    nSamples,
        uint64_t    *nMaxSegments
    ); """
ps6000a.make_symbol("_MemorySegmentsBySamples", "ps6000aMemorySegmentsBySamples", c_uint32, [c_int16, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS ps6000aGetMaximumAvailableMemory
    (
        int16_t    handle,
        uint64_t    *nMaxSamples,
        PICO_DEVICE_RESOLUTION    resolution
    ); """
ps6000a.make_symbol("_GetMaximumAvailableMemory", "ps6000aGetMaximumAvailableMemory", c_uint32, [c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps6000aQueryMaxSegmentsBySamples
    (
        int16_t    handle,
        uint64_t    nSamples,
        uint32_t    nChannelsEnabled,
        uint64_t    *nMaxSegments,
        PICO_DEVICE_RESOLUTION    resolution
    ); """
ps6000a.make_symbol("_QueryMaxSegmentsBySamples", "ps6000aQueryMaxSegmentsBySamples", c_uint32, [c_int16, c_uint64, c_int32, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetChannelOn
    (
        int16_t    handle,
        PICO_CHANNEL    channel,
        PICO_COUPLING    coupling,
        PICO_CONNECT_PROBE_RANGE    range,
        double    analogueOffset,
        PICO_BANDWIDTH_LIMITER    bandwidth
    ); """
ps6000a.make_symbol("_SetChannelOn", "ps6000aSetChannelOn", c_uint32, [c_int16, c_uint32, c_uint32, c_uint32, c_double, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetChannelOff
    (
        int16_t    handle,
        PICO_CHANNEL    channel
    ); """
ps6000a.make_symbol("_SetChannelOff", "ps6000aSetChannelOff", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetDigitalPortOn
    (
        int16_t    handle,
        PICO_CHANNEL    port,
        int16_t    *logicThresholdLevel,
        int16_t    logicThresholdLevelLength
        PICO_DIGITAL_PORT_HYSTERESIS    hysteresis
    ); """
ps6000a.make_symbol("_SetDigitalPortOn", "ps6000aSetDigitalPortOn", c_uint32, [c_int16, c_uint32, c_void_p, c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetDigitalPortOff
    (
        int16_t    handle,
        PICO_CHANNEL    port
    ); """
ps6000a.make_symbol("_SetDigitalPortOff", "ps6000aSetDigitalPortOff", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps6000aGetTimebase
    (
        int16_t    handle,
        uint32_t    timebase,
        uint64_t    noSamples,
        double    *timeIntervalNanoseconds,
        uint64_t    *maxSamples,
        uint64_t    segmentIndex
    ); """
ps6000a.make_symbol("_GetTimebase", "ps6000aGetTimebase", c_uint32, [c_int16, c_uint32, c_uint64, c_void_p, c_uint64, c_uint64], doc)

doc = """ PICO_STATUS ps6000aSigGenWaveform
    (
        int16_t    handle,
        PICO_WAVE_TYPE    wavetype,
        int16_t    *buffer,
        uint16    bufferLength
    ); """
ps6000a.make_symbol("_SigGenWaveform", "ps6000aSigGenWaveform", c_uint32, [c_int16, c_uint32, c_int16, c_uint16], doc)

doc = """ PICO_STATUS ps6000aSignGenRange
    (
        int16_t    handle, 
        double    peakToPeakVolts,
        double    offsetVolts
    ); """
ps6000a.make_symbol("_SigGenRange", "ps6000aSigGenRange", c_uint32, [c_int16, c_double, c_double], doc)

doc = """ PICO_STATUS ps6000aSigGenWaveformDutyCycle
    (
        int16_t    handle,
        double    dutyCyclePercent
    ); """
ps6000a.make_symbol("_SigGenWaveformDutyCycle", "ps6000aSigGenWaveformDutyCycle", c_uint32, [c_int16, c_double], doc)

doc = """ PICO_STATUS ps6000aSigGenTrigger
    (
        int16_t    handle,
        PICO_SIGGEN_TRIG_TYPE    triggerType,
        PICO_SIGGEN_TRIG_SOURCE    triggerSource,
        uint64_t    cycles,
        uint64_t    autoTriggerPicoSeconds
    ); """
ps6000a.make_symbol("_SigGenTrigger", "ps6000aSigGenTrigger", c_uint32, [c_int16, c_uint32, c_uint32, c_uint64, c_uint64], doc)

doc = """ PICO_STATUS ps6000aSigGenFilter
    (
        int16_t    handle,
        PICO_SIGGEN_FILTER_STATE    filterState
    ); """
ps6000a.make_symbol("_SigGenFilter", "ps6000aSigGenFilter", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSigGenFrequency
    (
        int16_t    handle,
        double    frequencyHz
    ); """
ps6000a.make_symbol("_SigGenFrequency", "ps6000aSigGenFrequency", c_uint32, [c_int16, c_double], doc)

doc = """ PICO_STATUS ps6000aSigGenFrequencySweep
    (
        int16_t    handle,
        double    stopFrequencyHz,
        double    frequencyIncrement,
        double    dwellTimeSeconds,
        PICO_SWEEP_TYPE    sweepType
    ); """
ps6000a.make_symbol("_SigGenFrequencySweep", "ps6000aSigGenFrequencySweep", c_uint32, [c_int16, c_double, c_double, c_double, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSigGenPhase
    (
        int16_t    handle,
        uint64_t    deltaPhase
    ); """
ps6000a.make_symbol("_SigGenPhase", "ps6000aSigGenPhase", c_uint32, [c_int16, c_uint64], doc)

doc = """ PICO_STATUS ps6000aSigGenPhaseSweep
    (
        int16_t    handle,
        uint64_t    stopDeltaPhase,
        uint64_t    deltaPhaseIncrement,
        uint64_t    dwellCount,
        PICO_SWEEP_TYPE    sweepType
    ); """
ps6000a.make_symbol("_SigGenPhaseSweep", "ps6000aSigGenPhaseSweep", c_uint32, [c_int16, c_uint64, c_uint64, c_uint64, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSigGenClockManual
    (
        int16_t    handle,
        double    dacClockFrequency,
        uint64_t    prescaleRation
    ); """
ps6000a.make_symbol("_SigGenClockManual", "ps6000aSigGenClockManual", c_uint32, [c_int16, c_double, c_uint64], doc)

doc = """ PICO_STATUS ps6000aSigGenSoftwareTriggerControl
    (
        int16_t    handle,
        PICO_SIGGEN_TRIG_TYPE    triggerState
    ); """
ps6000a.make_symbol("_SigGenSoftwareTriggerControl", "ps6000aSigGenSoftwareTriggerControl", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSigGenApply
    (
        int16_t    handle,
        int16_t    sigGenEnabled,
        int16_t    sweepEnabled,
        int16_t    triggerEnabled,
        int16_t    automaticClockOptimisationEnabled,
        int16_t    overrideAutomaticClockAndPrescale,
        double    *frequency,
        double    *stopFrequency,
        double    *frequencyIncrement,
        double    *dwellTime
    ); """
ps6000a.make_symbol("_SigGenApply", "ps6000aSigGenApply", c_uint32, [c_int16, c_int16, c_int16, c_int16, c_int16, c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aSigGenLimits
    (
        int16_t    handle,
        PICO_SIGGEN_PARAMETER    parameter,
        double    *minimumPermissibleValue,
        double    *maximumPermissibleValue,
        double    *step
    ); """
ps6000a.make_symbol("_SigGenLimits", "ps6000aSigGenLimits", c_uint32, [c_int16, c_uint32, c_double, c_double, c_double], doc)

doc = """ PICO_STATUS ps6000aSigGenFrequencyLimits
    (
        int16_t    handle,
        PICO_WAVE_TYPE    waveType,
        uint64_t    *numSamples,
        double    *startFrequency,
        int16_t    sweepEnabled,
        double    *manualDacClockFrequency,
        uint64_t    *manualPrescaleRatio,
        double    *maxStopFrequencyOut,
        double    *minFrequencyStepOut,
        double    *maxFrequencyStepOut,
        double    *minDwellTimeOut,
        double    *maxDwellTimeOut
    ); """
ps6000a.make_symbol("_SigGenFrequencyLimits", "ps6000aSigGenFrequencyLimits", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p, c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aSigGenPause
    (
        int16_t    handle
    ); """
ps6000a.make_symbol("_SigGenPause", "ps6000aSigGenPause", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS ps6000aSigGenRestart
    (
        int16_t    handle
    ); """
ps6000a.make_symbol("_SigGenRestart", "ps6000aSigGenRestart", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS ps6000aSetSimpleTrigger
    (
        int16_t    handle
        int16_t    enable,
        PICO_CHANNEL    source,
        int16_t    threshold,
        PICO_THRESHOLD_DIRECTION    direction,
        uint64_t    delay,
        uint32_t    autoTriggerMicroSeconds
    ); """
ps6000a.make_symbol("_SetSimpleTrigger", "ps6000aSetSimpleTrigger", c_uint32, [c_int16, c_int16, c_uint32, c_int16, c_uint32, c_uint64, c_uint32], doc)

doc = """ PICO_STATUS ps6000aTriggerWithinPreTriggerSamples
    (
        int16_t    handle,
        PICO_TRIGGER_WITHIN_PRE_TRIGGER    state
    ); """
ps6000a.make_symbol("_TriggerWithinPreTriggerSamples", "ps6000aTriggerWithinPreTriggerSamples", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetTriggerChannelProperties
    (
        int16_t    handle,
        PICO_TRIGGER_CHANNEL_PROPERTIES    *channelProperties,
        int16_t    nChannelProperties,
        int16_t    auxOutputEnable,
        uint32_t    autoTriggerMicroSeconds
    ); """
ps6000a.make_symbol("_SetTriggerChannelProperties", "ps6000aSetTriggerChannelProperties", c_uint32, [c_int16, c_void_p, c_int16, c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetTriggerChannelConditions
    (
        int16_t    handle,
        PICO_CONDITION    *conditions,
        int16_t    nConditions,
        PICO_ACTION    action
    ); """
ps6000a.make_symbol("_SetTriggerChannelConditions", "ps6000aSetTriggerChannelConditions", c_uint32, [c_int16, c_void_p, c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetTriggerChannelDirections
    (
        int16_t    handle,
        PICO_DIRECTION    *directions,
        int16_t    nDurections
    ); """
ps6000a.make_symbol("_SetTriggerChannelDirections", "ps6000aSetTriggerChannelDirections", c_uint32, [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps6000aSetTriggerDelay
    (
        int16_t    handle,
        uint64_t    delay
    ); """
ps6000a.make_symbol("_SetTriggerDelay", "ps6000aSetTriggerDelay", c_uint32, [c_int16, c_uint64], doc)

doc = """ PICO_STATUS ps6000aSetPulseWidthQualifierProperties
    (
        int16_t    handle,
        uint32_t    lower,
        uint32_t    upper,
        PICO_PULSE_WIDTH_TYPE    type
    ); """
ps6000a.make_symbol("_SetPulseWidthQualifierProperties", "ps6000aSetPulseWidthQualifierProperties", c_uint32, [c_int16, c_uint32, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetPulseWidthQualifierConditions
    (
        int16_t    handle,
        PICO_CONDITION    *conditions,
        int16_t    nConditions,
        PICO_ACTION    action
    ); """
ps6000a.make_symbol("_SetPulseWidthQualifierConditions", "ps6000aSetPulseWidthQualifierConditions", c_uint32, [c_int16, c_void_p, c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetPulseWidthQualifierDirections
    (
        int16_t    handle,
        PICO_DIRECTION    *directions,
        int16_t    nDirections
    ); """
ps6000a.make_symbol("_SetPulseWidthQualifierDirections", "ps6000aSetPulseWidthQualifierDirections", c_uint32, [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps6000aSetTriggerDigitalPortProperties
    (
        int16_t    handle,
        PICO_CHANNEL    port,
        PICO_DIGITAL_CHANNEL_DIRECTIONS    *directions,
        int16_t    nDirections
    ); """
ps6000a.make_symbol("_SetTriggerDigitalPortProperties", "ps6000aSetTriggerDigitalPortProperties", c_uint32, [c_int16, c_uint32, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps6000aSetPulseWidthDigitalPortProperties
    (
        int16_t    handle,
        PICO_CHANNEL    port,
        PICO_DIGITAL_CHANNEL_DIRECTIONS    *directions,
        int16_t    nDirections
    ); """
ps6000a.make_symbol("_SetPulseWidthDigitalPortProperties", "ps6000aSetPulseWidthDigitalPortProperties", c_uint32, [c_int16, c_uint32, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps6000aGetTriggerTimeOffset
    (
        int16_t    handle,
        int64_t    *time,
        PICO_TIME_UNITS    *timeUnits,
        uint64_t    segmentIndex
    ); """
ps6000a.make_symbol("_GetTriggerTimeOffset", "ps6000aGetTriggerTimeOffset", c_uint32, [c_int16, c_void_p, c_void_p, c_uint64], doc)

doc = """ PICO_STATUS ps6000aGetValuesTriggerTimeOffsetBulk
    (
        int16_t    handle,
        int64_t    *time,
        PICO_TIME_UNITS    *timeUnits,
        uint64_t    fromSegementIndex,
        uint64_t    toSegmentIndex
    ); """
ps6000a.make_symbol("_GetValuesTriggerTimeOffsetBulk", "ps6000aGetValuesTriggerTimeOffsetBulk", c_uint32, [c_int16, c_void_p, c_void_p, c_uint64, c_uint64], doc)

doc = """ PICO_STATUS ps6000aSetDataBuffer
    (
        int16_t    handle,
        PICO_CHANNEL    channel,
        PICO_POINTER    buffer,
        int32_t    nSamples,
        PICO_DATA_TYPE    dataType,
        uint64_t    waveform,
        PICO_RATIO_MODE    downSampelRationMode,
        PICO_ACTION    action
    ); """
ps6000a.make_symbol("_SetDataBuffer", "ps6000aSetDataBuffer", c_uint32, [c_int16, c_uint32, c_uint32, c_int32, c_uint32, c_uint64, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetDataBuffers
    (
        int16_t    handle,
        PICO_CHANNEL    channel,
        PICO_POINTER    bufferMax,
        PICO_POINTER    bufferMin,
        int32_t    nSamples,
        PICO_DATA_TYPE    dataType,
        uint64_t    waveform,
        PICO_RATIO_MODE    downSampleRatioMode,
        PICO_ACTION    action
    ); """
ps6000a.make_symbol("_SetDataBuffers", "ps6000aSetDataBuffers", c_uint32, [c_int16, c_uint32, c_uint32, c_int32, c_uint32, c_uint64, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps6000aRunBlock
    (
        int16_t    handle,
        uint64_t    noOfPreTriggerSamples,
        uint64_t    noOfPostTriggerSamples,
        uint32_t    timebase,
        double    *timeIndisposedMs,
        uint64_t    segmentIndex,
        ps6000aBlockReady    lpReady,
        PICO_POINTER    pParameter
    ); """
ps6000a.make_symbol("_RunBlock", "ps6000aRunBlock", c_uint32, [c_int16, c_uint64, c_uint64, c_uint32, c_void_p, c_uint64, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aIsReady
    (
        int16_t    handle,
        int16_t    *ready
    ); """
ps6000a.make_symbol("_IsReady", "ps6000aIsReady", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps6000aRunStreaming
    (
        int16_t    handle,
        double    *sampleInterval,
        PICO_TIME_UNITS    sampleIntervalTimeUnits,
        uint64_t    maxPreTriggerSamples,
        uint64_t    maxPostTriggerSamples,
        int16_t    autoStop,
        uint64_t    downSampleRatio,
        PICO_RATIO_MODE    downSampelRationMode
    ): """
ps6000a.make_symbol("_RunStreaming", "ps6000aRunStreaming", c_uint32, [c_int16, c_void_p, c_uint32, c_uint64, c_uint64, c_int16, c_uint64, c_uint32], doc)

doc = """ PICO_STATUS ps6000aGetStreamingLatestValues
    (
        int16_t    handle,
        PICO_STREAMING_DATA_INFO    *streamingDataInfo,
        uint64_t    nStreamingDataInfos,
        PICO_STREAMING_DATA_TRIGGER_INFO    *triggerInfo
    ); """
ps6000a.make_symbol("_GetStreamingLatestValues", "ps6000aGetStreamingLatestValues", c_uint32, [c_int16, c_void_p, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS ps6000aNoOfStreamingValues
    (
        int16_t    handle,
        uint64_t    *noOfValues
    ); """
ps6000a.make_symbol("_NoOfStreamingValues", "ps6000aNoOfStreamingValues", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps6000aGetValues
    (
        int16_t    handle,
        uint64_t    startIndex,
        uint64_t    *noOfSamples,
        uint64_t    downSampleRatio,
        PICO_RATIO_MODE    downSampleRatioMode,
        uint64_t    segmentIndex,
        int16_t    *overflow
    ); """
ps6000a.make_symbol("_GetValues", "ps6000aGetValues", c_uint32, [c_int16, c_uint64, c_void_p, c_uint64, c_uint32, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS ps6000aGetValuesBulk
    (
        int16_t    handle,
        uint64_t    startIndex,
        uint64_t    *noOfSamples,
        uint64_t    downSampleRatio,
        PICO_RATIO_MODE    downSampleRatioMode,
        uint64_t    segmentIndex,
        int16_t    *overflow
    ); """
ps6000a.make_symbol("_GetValuesBulk", "ps6000aGetValuesBulk", c_uint32, [c_int16, c_uint64, c_void_p, c_uint64, c_uint32, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS ps6000aGetValuesAsync
    (
        int16_t    handle,
        uint64_t    startIndex,
        uint64_t    noOfSamples,
        uint64_t    downSampleRatio,
        PICO_RATIO_MODE    downSampleRatioMode,
        uint64_t    segmentIndex,
        PICO_POINTER    lpDataReady,
        PICO_POINTER    pParameter
    ); """
ps6000a.make_symbol("_GetValuesAsync", "ps6000aGetValuesAsync", c_uint32, [c_int16, c_uint64, c_uint64, c_uint64, c_uint32, c_uint64, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aGetValuesBulkAsync
    (
        int16_t    handle,
        uint64_t    startIndex,
        uint64_t    noOfSamples,
        uint64_t    fromSegmentIndex,
        uint64_t    toSegmentIndex,
        uint64_t    downSampleRatio,
        PICO_RATIO_MODE    downSampleRatioMode,
        PICO_POINTER    lpDataReady,
        PICO_POINTER    pParameter
    ); """
ps6000a.make_symbol("_GetValuesBulkAsync", "ps6000aGetValuesBulkAsync", c_uint32, [c_int16, c_uint64, c_uint64, c_uint64, c_uint64, c_uint64, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aGetValuesOverlapped
    (
        int16_t    handle,
        uint64_t    startIndex,
        uint64_t    *noOfSamples,
        uint64_t    downSampleRatioMode,
        PICO_RATIO_MODE    downSampleRatioMode,
        uint64_t    fromSegementIndex,
        uint64_t    toSegmentIndex,
        int16_t    *overflow
    ); """
ps6000a.make_symbol("_GetValuesOverlapped", "ps6000aGetValuesOverlapped", c_uint32, [c_int16, c_uint64, c_void_p, c_uint64, c_uint32, c_uint64, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS ps6000aStopUsingGetValuesOverlapped
    (
        int16_t    handle
    ); """
ps6000a.make_symbol("_StopUsingGetValuesOverlapped", "ps6000aStopUsingGetValuesOverlapped", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS ps6000aGetNoOfCaptures
    (
        int16_t    handle,
        uint64_t    *nCaptures
    ); """
ps6000a.make_symbol("_GetNoOfCaptures", "ps6000aGetNoOfCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps6000aGetNoOfProcessedCaptures
    (
        int16_t    handle,
        uint64_t    *nProcessedCaptures
    ); """
ps6000a.make_symbol("_GetNoOfProcessedCaptures", "ps6000aGetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps6000aStop
    (
        int16_t    handle,
    ); """
ps6000a.make_symbol("_Stop", "ps6000aStop", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS ps6000aSetNoOfCaptures
    (
        int16_t    handle,
        uint64_t    nCaptures
    ); """
ps6000a.make_symbol("_SetNoOfCaptures", "ps6000aSetNoOfCaptures", c_uint32, [c_int16, c_uint64], doc)

doc = """ PICO_STATUS ps6000aGetTriggerInfo
    (
        int16_t    handle,
        PICO_TRIGGER_INFO    *triggerInfo,
        uint64_t    firstSegmentIndex,
        uint64_t    segmentCount
    ); """
ps6000a.make_symbol("_getTriggerInfo", "ps6000aGetTriggerInfo", c_uint32, [c_int16, c_void_p, c_uint64, c_uint64], doc)

doc = """ PICO_STATUS ps6000aEnumerateUnits
    (
        int16_t    *count,
        int8_t    *serials,
        int16_t    *serialLth
    ); """
ps6000a.make_symbol("_EnumerateUnits", "ps6000aEnumerateUnits", c_uint32, [c_void_p, c_char_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aPingUnit
    (
        int16_t    handle
    ); """
ps6000a.make_symbol("_PingUnit", "ps6000aPingUnit", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS ps6000aGetAnalogueOffsetLimits
    (
        int16_t    handle,
        PICO_CONNECT_PROBE_RANGE    range,
        PICO_COUPLING    coupling,
        double    *maximumVoltage,
        double    *minimumVoltage
    ); """
ps6000a.make_symbol("_GetAnalogueOffsetLimits", "ps6000aGetAnalogueOffsetLimits", c_uint32, [c_int16, c_uint32, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aGetMinimumTimebaseStateless
    (
        int16_t    handle,
        PICO_CHANNEL_FLAGS    enabledChannelFlags,
        uint32_t    *timebase,
        double    *timeInerval,
        PICO_DEVICE_RESOLUTION    resolution
    ); """
ps6000a.make_symbol("_GetMinimumTimebaseStateless", "ps6000aGetMinimumTimebaseStateless", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS ps6000aNearestSampleIntervalStateless
    (
        int16_t    handle,
        PICO_CHANNEL_FLAGS    enabledChannelFlags,
        double    timeIntervalRequested,
        PICO_DEVICE_RESOLUTION    resolution,
        uint32_t    *timebase,
        double    *timeIntervalAvailable
    ); """
ps6000a.make_symbol("_NearestSampleIntervalStateless", "ps6000aNearestSampleIntervalStateless", c_uint32, [c_int16, c_uint32, c_double, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aChannelCombinationsStateless
    (
        int16_t    handle,
        PICO_CHANNEL_FLAGS    *channelFlagsCombinations,
        uint32_t    *nChannelCombinations,
        PICO_DEVICE_RESOLUTION    resolution,
        uint32_t    timebase
    ); """
ps6000a.make_symbol("_ChannelCombinationsStateless", "ps6000aChannelCombinationsStateless", c_uint32, [c_int16, c_void_p, c_void_p, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS ps6000aSetDeviceResolution
    (
        int16_t    handle,
        PICO_DEVICE_RESOLUTION    resolution
    ); """
ps6000a.make_symbol("_SetDeviceResolution", "ps6000aSetDeviceResolution", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS ps6000aGetDeviceResolution
    (
        int16_t    handle,
        PICO_DEVICE_RESOLUTION    *resolution
    ); """
ps6000a.make_symbol("_GetDeviceResolution", "ps6000aGetDeviceResolution", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps6000aQueryOutputEdgeDetect
    (
        int16_t    handle,
        int16_t    *state
    ); """
ps6000a.make_symbol("_QueryOutputEdgeDetect", "ps6000aQueryOutputEdgeDetect", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps6000aSetOutputEdgeDetect
    (
        int16_t    handle,
        int16_t    state
    ); """
ps6000a.make_symbol("_SetOutputEdgeDetect", "ps6000aSetOutputEdgeDetect", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS ps6000aGetScalingValues
    (
        int16_t    handle,
        PICO_SCALING_FACTORS_VALUES    *scalingValues,
        int16_t    nChannels
    ); """
ps6000a.make_symbol("_GetScalingValues", "ps6000aGetScalingValues", c_uint32, [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS ps6000aGetAdcLimits
    (
        int16_t    handle,
        PICO_DEVICE_RESOLUTION    resolution,
        int16_t    *minValue,
        int16_t    *maxValue
    ); """
ps6000a.make_symbol("_GetAdcLimits", "ps6000aGetAdcLimits", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aCheckForUpdate
    (
        int16_t    handle,
        PICO_VERSION    *current,
        PICO_VERSION    *update,
        uint16_t    *updateRequired
    ); """
ps6000a.make_symbol("_CheckForUpdate", "ps6000aCheckForUpdate", c_uint32, [c_int16, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS ps6000aStartFirmwareUpdate
    (
        int16_t    handle,
        PicoUpdateFirmwareProgress    progress 
    ); """
ps6000a.make_symbol("_StartFirmwareUpdate", "ps6000aStartFirmwareUpdate", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps6000aSetProbeInteractionCallback
    (
        int16_t    handle,
        PicoProbeInteractions    callback
    ); """
ps6000a.make_symbol("_SetProbeInteractionCallback", "ps6000aSetProbeInteractionCallback", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps6000aSetExternalReferenceInteractionCallback
    (
        int16_t    handle,
        PicoExternalReferenceInteractions    callback
    ); """
ps6000a.make_symbol("_SetExternalReferenceInteractionCallback", "ps6000aSetExternalReferenceInteractionCallback", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps6000aSetAWGOverrangeInteractionCallback
    (
        int16_t    handle,
        PicoAWGOverrangeInteractions    callback
    ); """
ps6000a.make_symbol("_SetAWGOVerrangeInteractionCallback", "ps6000aSetAWGOverrangeInteractionCallback", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS ps6000aSetTemperatureSensorInteractioNCallback
    (
        int16_t    handle,
        PicoTemperatureSensorInteractions    callback
    ); """
ps6000a.make_symbol("_SetTemperatureSensroInteractionCallback", "ps6000aSetTemperatureSensorInteractionCallback", c_uint32, [c_int16, c_void_p], doc)