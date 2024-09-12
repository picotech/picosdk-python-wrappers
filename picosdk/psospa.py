#
# Copyright (C) 2024 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the psospaApi.h C header
file for PicoScope 3000 A Series oscilloscopes using the psospa driver API
functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.ctypes_wrapper import C_CALLBACK_FUNCTION_FACTORY
from picosdk.constants import make_enum
from picosdk.PicoDeviceEnums import picoEnum as enums

class Psospalib(Library):
    def __init__(self):
	    super(Psospalib, self).__init__("psospa")
	
psospa = Psospalib()

doc = """ void psospaBlockReady
    (
        int16_t    handle,
        PICO_STATUS    status,
        PICO_POINTER    pParameter
    ); """
psospa.BlockReadyType = C_CALLBACK_FUNCTION_FACTORY(None,
                                                    c_int16,
                                                    c_uint32,
                                                    c_void_p)
psospa.BlockReadyType.__doc__ = doc

doc = """ void psospaDataReady
    (
        int16_t    handle,
        PICO_STATUS    status,
        uint64_t    noOfSamples,
        int16_t    overflow,
        PICO_POINTER    pParameter
    ); """
psospa.DataReadyType = C_CALLBACK_FUNCTION_FACTORY(None,
                                                    c_int16,
                                                    c_uint32,
                                                    c_uint64,
                                                    c_int16,
                                                    c_void_p)
psospa.DataReadyType.__doc__ = doc

doc = """ PICO_STATUS psospaOpenUnit
    (
	    int16_t*    handle,
		int8_t*     serial,
		PICO_DEVICE_RESOLUTION    resolution,
		PICO_USB_POWER_DETAILS*    powerDetails
	); """
psospa.make_symbol("_OpenUnit","psospaOpenUnit", c_uint32, [c_void_p, c_char_p, c_int32, c_void_p], doc)

doc = """ PICO_STATUS psospaCloseUnit
    (
	    int16_t    handle
	); """
psospa.make_symbol("_CloseUnit", "psospaCloseUnit", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS psospaGetUnitInfo
    (
        int16_t    handle,
        int8_t*    string,
        int16_t    stringLength,
        int16_t*    requiredSize,
        PICO_INFO    info
    ); """
psospa.make_symbol("_GetUnitInfo","psospaGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS psospaGetVariantDetails
    (
        const int8_t*    variantName,
        int16_t    variantNameLength,
        int8_t*    outputString,
        int32_t*    outputStringLength
    ); """
psospa.make_symbol("_GetVariantDetails", "psospaGetVariantDetails", c_uint32, [c_char_p, c_int16, c_char_p, c_void_p], doc)

doc = """ PICO_STATUS psospaMemorySegments
    (
        int16_t    handle,
        uint64_t    nSegments,
        uint64_t*    nMaxSamples
    ); """
psospa.make_symbol("_MemorySegments","psospaMemorySegments", c_uint32,[c_int16, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS psospaMemorySegmentsBySamples
    (
        int16_t    handle,
        uint64_t    nSamples,
        uint64_t*    nMaxSegments
    ); """
psospa.make_symbol("_MemorySegmentsBySamples","psospaMemorySegmentsBySamples", c_uint32, [c_int16, c_uint64, c_void_p], doc)

# doc = """ PICO_STATUS psospaGetMaximumAvaliableMemory
    # (
        # int16_t    handle,
        # uint64_t*    nMaxSamples,
        # PICO_DEVICE_RESOLUTION    resolution
    # ); """
# psospa.make_symbol("_GetMaximumAvaliableMemory","psospaGetMaximumAvaliableMemory", c_uint32, [c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS psospaQueryMaxSegmentsBySamples
    (
        int16_t    handle,
        uint64_t    nSamples,
        uint32_t    nChannelEnabled,
        uint64_t*    nMaxSegments,
        PICO_DEVICE_RESOLUTION    resolution
    ); """
psospa.make_symbol("_QUeryMaxSegmentsBySamples","psospaQueryMaxSegmentsBySamples", c_uint32, [c_int16, c_uint64, c_uint32, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS psospaSetChannelOn
    (
        int16_t    handle,
        PICO_CHANNEL    channel,
        PICO_COUPLING    coupling,
        int64_t    rangeMin,
        int64_t    rangeMax
        PICO_PROBE_RANGE_INFO    rangeType,
        double    analogueOffset,
        PICO_BANDWIDTH_LIMITER    bandwidth
    ); """
psospa.make_symbol("_SetChannelOn","psospaSetChannelOn", c_uint32, [c_int16, c_uint32, c_uint32, c_int64, c_int64, c_uint32, c_double, c_uint32], doc)

doc = """ PICO_STATUS psospaSetChannelOff
    (
        int16_t    handle,
        PICO_CHANNEL    channel
    ); """
psospa.make_symbol("_SetChannelOff","psospaSetChannelOff", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSetDigitalPortOn
    (
        int16_t    handle,
        PICO_CHANNEL    port,
        int16_t*    logicThresholdLevel,
        int16_t*    logicThresholdLengthLevel,
        PICO_DIGITAL_PORT_HYSTERESIS    hysteresis
    ); """
psospa.make_symbol("_SetDigitalPortOn","psospaSetDigitalPortOn", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS psospaSetDigitalPortOff
    (
        int16_t    handle,
        PICO_CHANNEL    port
    ); """
psospa.make_symbol("_SetDigitalPortOff","psospaSetDigitalPortOff", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaGetTimebase
    (
        int16_t    handle,
        uint32_t    timebase,
        uint64_t    noSamples,
        double*    timeIntervalNanoseconds,
        uint64_t*    maxSamples,
        uint64_t    segmentIndex
    ); """
psospa.make_symbol("_GetTimebase","psospaGetTimebase", c_uint32, [c_int16, c_uint32, c_uint64, c_void_p, c_void_p, c_uint64], doc)

doc = """ PICO_STATUS psospaSigGenWaveform
    (
        int16_t    handle,
        PICO_WAVE_TYPE    waveType,
        int16_t*    buffer,
        uint64_t    bufferLength
    ); """
psospa.make_symbol("_SigGenWaveform","psospaSigGenWaveform", c_uint32, [c_int16, c_uint32, c_void_p, c_uint64], doc)

doc = """ PICO_STATUS psospaSigGenRange
    (
        int16_t    handle,
        double    peakToPeakVolts,
        double    offsetVolts
    ); """
psospa.make_symbol("_SigGenRange","psospaSigGenRange", c_uint32, [c_int16, c_double, c_double], doc)

doc = """ PICO_STATUS psospaSigGenWaveformDutyCycle
    (
        int16_t    handle,
        double    dutyCyclePercent
    ); """
psospa.make_symbol("_SigGenWaveformDutyCycle","psospaSigGenWaveformDutyCycle", c_uint32, [c_int16, c_double], doc)

doc = """ PICO_STATUS psospaSigGenTrigger
    (
        int16_t    handle,
        PICO_SIGGEN_TRIG_TYPE    triggerType,
        PICO_SIGGEN_TRIG_SOURCE    triggerSource,
        uint64_t    cycles,
        uint64_t    autoTriggerPicoSeconds
    ); """
psospa.make_symbol("_SigGenTrigger","psospaSigGenTrigger", c_uint32, [c_int16, c_uint32, c_uint32, c_uint64, c_uint64], doc)

doc = """ PICO_STATUS psospaSigGenFrequency
    (
        int16_t    handle,
        double    frequencyHz
    ); """
psospa.make_symbol("_SigGenFrequency","psospaSigGenFrequency", c_uint32, [c_int16, c_double], doc)

doc = """ PICO_STATUS psospaSigGenFrequencySweep
    (
        int16_t    handle,
        double    stopFrequencyHz,
        double    frequencyIncrement,
        double    dwellTimeSeconds,
        PICO_SWEEP_TYPE    sweepType
    ); """
psospa.make_symbol("_SigGenFrequencySweep","psospaSigGenFrequencySweep", c_uint32, [c_int16, c_double, c_double, c_double, c_uint32], doc)

doc = """ PICO_STATUS psospaSigGenPhase
    (
        int16_t    handle,
        uint64_t    deltaPhase
    ); """
psospa.make_symbol("_SigGenPhase","psospaSigGenPhase", c_uint32, [c_int16, c_uint64], doc)

doc = """ PICO_STATUS psospaSigGenPhaseSweep
    (
        int16_t    handle,
        uint64_t    stopDeltaPhase,
        uint64_t    deltaPhaseIncrement,
        uint64_t    dwellCount,
        PICO_SWEEP_TYPE    sweepType
    ); """
psospa.make_symbol("_SigGenPhaseSweep","psospaSigGenPhaseSweep", c_uint32, [c_int16, c_uint64, c_uint64, c_uint64, c_uint32], doc)

doc = """ PICO_STATUS psospaSigGenSoftwareTriggerControl
    (
        int16_t    handle,
        PICO_SIGGEN_TRIG_TYPE    triggerState
    ); """
psospa.make_symbol("_SigGenSoftwareTriggerControl","psospaSigGenSoftwareTriggerControl", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSigGenApply
    (
        int16_t    handle,
        int16_t    sigGenEnabled,
        int16_t    sweepEnabled,
        int16_t    triggerEnabled,
        double*    frequency
        double*    stopFrequency,
        double*    frequencyIncrement,
        double*    dwellTime,
    ); """
psospa.make_symbol("_SigGenApply","psospaSigGenApply", c_uint32, [c_int16, c_int16, c_int16, c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaSigGenLimits
    (
        int16_t    handle,
        PICO_SIGGEN_PARAMETER    parameter,
        double*    minimumPermissibleValue,
        double*    maximumPermissibleValue,
        double*    step
    ); """
psospa.make_symbol("_SigGenLimits","psospaSigGenLimits", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaSigGenFrequencyLimits
    (
        int16_t    handle,
        PICO_WAVE_TYPE    waveType,
        uint64_t*    numSamples,
        double*    minFrequencyOut,
        double*    maxFrequencyOut,
        double*    minFrequencyStepOut,
        double*    maxFrequencyStepOut,
        double*    mindDwellTimeOut,
        double*    maxDwellTimeOut
    ); """
psospa.make_symbol("_SigGenFrequencyLimits","psospaSigGenFrequencyLimits", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaSigGenPause
    (
        int16_t    handle,
    ); """
psospa.make_symbol("_SigGenPause","psospaSigGenPause", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS psospaSigGenRestart
    (
        int16_t    handle
    ); """
psospa.make_symbol("_SigGenRestart","psospaSigGenRestart", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS psospaSetSimpleTrigger
    (
        int16_t    handle,
        int16_t    enable,
        PICO_CHANNEL    source,
        int16_t    threshold,
        PICO_THRESHOLD_DIRECTION    direction,
        uint64_t    delay,
        uint32_t    autoTriggerMicroSeconds
    ); """
psospa.make_symbol("_SetSimpleTrigger","psospaSetSimpleTrigger", c_uint32, [c_int16, c_int16, c_uint32, c_int16, c_uint32, c_uint64, c_uint32], doc)

doc = """ PICO_STATUS psospaTriggerWithinPreTriggerSamples
    (
        int16_t    handle,
        PICO_TRIGGER_WITHIN_PRE_TRIGGER    state
    ); """
psospa.make_symbol("_TriggerWithinPreTriggerSamples","psospaTriggerWithinPreTriggerSamples", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSetTriggerChannelProperties
    (
        int16_t    handle,
        PICO_TRIGGER_CHANNEL_PROPERTIES*    channelProperties,
        int16_t    nChannelProperties,
        uint32_t    autoTriggerMicroSeconds
    ); """
psospa.make_symbol("_SetTriggerChannelProperties","psospaSetTriggerChannelProperties", c_uint32, [c_int16, c_void_p, c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSetTriggerChannelConditions
   (
        int16_t   handle,
        PICO_CONDITION*   conditions,
        int16_t    nConditions,
        PICO_ACTION    action
    ); """
psospa.make_symbol("_SetTriggerChannelConditions","psospaSetTriggerChannelConditions", c_uint32, [c_int16, c_void_p, c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSetTriggerChannelDirections
    (
        int16_t    handle,
        PICO_DIRECTION*    directions,
        int16_t    nDirections
    ); """
psospa.make_symbol("_SetTriggerChannelDirections","psospaSetTriggerChannelDirections", c_uint32, [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS psospaSetTriggerDelay
    (
        int16_t    handle,
        uint64_t    delay
    ); """
psospa.make_symbol("_SetTriggerDelay","psospaSetTriggerDelay", c_uint32, [c_int16, c_uint64], doc)

doc = """ PICO_STATUS psospaSetTriggerHoldoffCounterBySamples
    (
        int16_t    handle,
        uint64_t    holdoffSamples
    ); """
psospa.make_symbol("_SetTriggerHoldoffCounterBySamples","psospaSetTriggerHoldoffCounterBySamples", c_uint32, [c_int16, c_uint64], doc)

doc = """ PICO_STATUS psospaSetPulseWidthQualifierProperties
    (
        int16_t    handle,
        uint32_t    lower,
        uint32_t    upper,
        PICO_PULSE_WIDTH_TYPE    type
    ); """
psospa.make_symbol("_SetPulseWidthQualifierProperties","psospaSetPulseWidthQualifierProperties", c_uint32, [c_int16, c_uint32, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS psospaSetPulseWidthQualifierConditions
   (
        int16_t    handle,
        PICO_CONDITION*    conditions,
        int16_t    nConditions,
        PICO_ACTION    action
    ); """
psospa.make_symbol("_SetPulseWidthQualifierConditions","psospaSetPulseWidthQualifierConditions", c_uint32, [c_int16, c_void_p, c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSetPulseWidthQualifierDirections
    (
        int16_t    handle,
        PICO_DIRECTION*    directions,
        int16_t    nDirections
    ); """
psospa.make_symbol("_SetPulseWidthQualifierDirections","psospaSetPulseWidthQualifierDirections", c_uint32, [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS psospaSetTriggerDigitalPortProperties
    (
        int16_t    handle,
        PICO_CHANNEL    port,
        PICO_DIGITAL_CHANNEL_DIRECTIONS*    directions,
        int16_t    nDirections
    ); """
psospa.make_symbol("_SetTriggerDigitalPortProperties","psospaSetTriggerDigitalPortProperties", c_uint32, [c_int16, c_uint32, c_void_p, c_int16], doc)

doc = """ PICO_STATUS psospaGetTriggerTimeOffset
    (
        int16_t    handle,
        int64_t*    time,
        PICO_TIME_UNITS*    timeUnits,
        uint64_t    segmentIndex
    ); """
psospa.make_symbol("_GetTriggerTimeOffset","psospaGetTriggerTimeOffset", c_uint32, [c_int16, c_void_p, c_void_p, c_uint64], doc)

doc = """ PICO_STATUS psospaGetValuesTriggerTimeOffsetBulk
    (
        int16_t    handle,
        int64_t*    times,
        PICO_TIME_UNITS*    timeUnits,
        uint64_t    fromSegmentIndex,
        uint64_t    toSegmentIndex
    ); """
psospa.make_symbol("_GetValuesTriggerTimeOffsetBulk","psospaGetValuesTriggerTimeOffsetBulk", c_uint32, [c_int16, c_void_p, c_void_p, c_uint64, c_uint64], doc)

doc = """ PICO_STATUS psospaSetDataBuffer
    (
        int16_t    handle,
        PICO_CHANNEL    channel,
        PICO_POINTER    buffer,
        int64_t    nSamples,
        PICO_DATA_TYPE    dataType,
        uint64_t    waveform,
        PICO_RATIO_MODE    downSampleRationMode,
        PICO_ACTION    action
    ); """
psospa.make_symbol("_SetDataBuffer","psospaSetDataBuffer", c_uint32, [c_int16, c_uint32, c_void_p, c_uint64, c_uint32, c_uint64, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS psospaSetDataBuffers
    (
        int16_t    handle,
        PICO_CHANNEL    channel,
        PICO_POINTER    bufferMax,
        PICO_POINTER    bufferMin,
        int64_t    nSamples,
        PICO_DATA_TYPE    dataType,
        uint64_t    waveform,
        PICO_RATIO_MODE    downSampleRatioMode,
        PICO_ACTION    action
    ); """
psospa.make_symbol("_SetDataBuffers","psospaSetDataBuffers", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p, c_int64, c_uint32, c_uint64, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS psospaRunBlock
    (
        int16_t    handle,
        uint64_t    noOfPreTriggerSamples,
        uint64_t    noOfPostTriggerSamples,
        uint32_t    timebase,
        double*    timeIndisposedMs,
        uint64_t    segmentIndex,
        psospaBlockReady    lpReady,
        PICO_POINTER    pParameter
    ); """
psospa.make_symbol("_RunBlock","psospaRunBlock", c_uint32, [c_int16, c_uint64, c_uint64, c_uint32, c_void_p, c_uint64, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaIsReady
    (
        int16_t    handle,
        int16_t*    ready
    ); """
psospa.make_symbol("_IsReady","psospaIsReady", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS psospaRunStreaming
    (
        int16_t    handle,
        double*    sampleInterval,
        PICO_TIME_UNITS    sampleIntervalTimeUnits,
        uint64_t    maxPreTriggerSamples,
        uint64_t    maxPostPreTriggerSamples,
        int16_t    autoStop,
        uint64_t    downSampleRatio,
        PICO_RATIO_MODE    downSampleRatioMode
    ); """
psospa.make_symbol("_RunStreaming","psospaRunStreaming", c_uint32, [c_int16, c_void_p, c_uint32, c_uint64, c_uint64, c_int16, c_uint64, c_uint32], doc)

doc = """ PICO_STATUS psospaGetStreamingLatestValues
    (
        int16_t    handle,
        PICO_STREAMING_DATA_INFO*    streamingDataInfo,
        uint64_t    nStreamingDataInfos,
        PICO_STREAMING_DATA_TRIGGER_INFO*    triggerInfo
    ); """
psospa.make_symbol("_GetStreamingLatestValues","psospaGetStreamingLatestValues", c_uint32, [c_int16, c_void_p, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS psospaNoOfStreamingValues
    (
        int16_t    handle,
        uint64_t*    noOfValues
    ); """
psospa.make_symbol("_NoOfStreamingValues","psospaNoOfStreamingValues", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS psospaGetValues
    (
        int16_t    handle,
        uint64_t    startIndex,
        uint64_t*    noOfSamples,
        uint64_t    downSampleRatio,
        PICO_RATIO_MODE    downSampleRatioMode,
        uint64_t    segmentIndex,
        int16_t*    overflow
    ); """
psospa.make_symbol("_GetValues","psospaGetValues", c_uint32, [c_int16, c_uint64, c_void_p, c_uint64, c_uint32, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS psospaGetValuesBulk
    (
        int16_t    handle,
        uint64_t    startIndex,
        uint64_t*    noOfSamples,
        uint64_t    fromSegmentIndex,
        uint64_t    toSegmentIndex,
        uint64_t    downSampleRatio,
        PICO_RATIO_MODE    downSampleRatioMode,
        int16_t*    overflow
    ); """
psospa.make_symbol("_GetValuesBulk","psospaGetValuesBulk", c_uint32, [c_int16, c_uint64, c_void_p, c_uint64, c_uint64, c_uint64, c_uint32, c_void_p], doc)

doc = """ PICO_STATUS psospaGetValuesAsync
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
psospa.make_symbol("_GetValuesAsync","psospaGetValuesAsync", c_uint32, [c_int16, c_uint64, c_uint64, c_uint64, c_uint32, c_uint64, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaGetValuesBulkAsync
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
psospa.make_symbol("_GetValuesBulkAsync","psospaGetValuesBulkAsync", c_uint32, [c_int16, c_uint64, c_uint64, c_uint64, c_uint64, c_uint64, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaGetValuesOverlapped
    (
        int16_t    handle,
        uint64_t    startIndex,
        uint64_t*    noOfSamples,
        uint64_t    downSampleRatio,
        PICO_RATIO_MODE    downSampleRatioMode,
        uint64_t    fromSegmentIndex,
        uint64_t    toSegmentIndex,
        int16_t*    overflow
    ); """
psospa.make_symbol("_GetValuesOverlapped","psospaGetValuesOverlapped", c_uint32, [c_int16, c_uint64, c_void_p, c_uint64, c_uint32, c_uint64, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS psospaStopUsingGetValuesOverlapped
    (
        int16_t    handle
    ); """
psospa.make_symbol("_StopUsingGetValuesOverlapped","psospaStopUsingGetValuesOverlapped", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS psospaGetNoOfCaptures
    (
        int16_t    handle,
        uint64_t*    nCaptures
    ); """
psospa.make_symbol("_GetNoOfCaptures","psospaGetNoOfCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS psospaGetNoOfProcessedCaptures
    (
        int16_t    handle,
        uint64_t*    nProcessedCaptures
    ); """
psospa.make_symbol("_GetNoOfProcessedCaptures","psospaGetNoOfProcessedCaptures", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS psospaStop
    (
        int16_t    handle
    ); """
psospa.make_symbol("_Stop","psospaStop", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS psospaSetNoOfCaptures
    (
        int16_t    handle,
        uint64_t    nCaptures
    ); """
psospa.make_symbol("_SetNoOfCaptures","psospaSetNoOfCaptures", c_uint32, [c_int16, c_uint64], doc)

doc = """ PICO_STATUS psospaGetTriggerInfo
    (
        int16_t    handle,
        PICO_TRIGGER_INFO*    triggerInfo,
        uint64_t    firstSegmentIndex,
        uint64_t     segmentIndex
    ); """
psospa.make_symbol("_GetTriggerInfo","psospaGetTriggerInfo", c_uint32, [c_int16, c_void_p, c_uint64, c_uint64], doc)

doc = """ PICO_STATUS psospaEnumerateUnits
    (
        int16_t*    count,
        int8_t*    serials,
        int16_t*    serialLth
    ); """
psospa.make_symbol("_EnumerateUnits","psospaEnumerateUnits", c_uint32, [c_void_p, c_char_p, c_void_p], doc)

doc = """ PICO_STATUS psospaPingUnit
    (
        int16_t    handle
    ); """
psospa.make_symbol("_PingUnit","psospaPingUnit", c_uint32, [c_int16], doc)
 
doc = """ PICO_STATUS psospaGetAnalogueOffsetLimits
    (
        int16_t     handle,
        int64_t    rangeMin,
        int64_t    rangeMax,
        PICO_PROBE_RANGE_INFO    rangeType,
        PICO_COUPLING    coupling,
        double*    maximumVoltage,
        double*    minimumVoltage
    ); """
psospa.make_symbol("_GetAnalogueOffsetLimits","psospaGetAnalogueOffsetLimits", c_uint32, [c_int16, c_int64, c_int64, c_uint32, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaGetMinimumTimebaseStateless
    (
        int16_t    handle,
        PICO_CHANNEL_FLAGS    enabledChannelFlags,
        uint32_t*    timebase,
        double*    timeInterval,
        PICO_DEVICE_RESOLUTION    resolution
    ); """
psospa.make_symbol("_GetMinimumTimebaseStateless","psospaGetMinimumTimebaseStateless", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS psospaNearestSampleIntervalStateless
    (
        int16_t    handle,
        PICO_CHANNEL_FLAGS    enabledChannelFlags,
        double    timeIntervalRequested,
        uint8_t    roundFaster,
        PICO_DEVICE_RESOLUTION     resolution,
        uint32_t*    timebase,
        double*    timeIntervalAvailable
    ); """
psospa.make_symbol("_NearestSampleIntervalStateless","psospaNearestSampleIntervalStateless", c_uint32, [c_int16, c_uint32, c_double, c_char,c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaSetDeviceResolution
    (
        int16_t    handle,
        PICO_DEVICE_RESOLUTION    resolution
    ); """
psospa.make_symbol("_SetDeviceResolution","psospaSetDeviceResolution", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaGetDeviceResolution
    (
        int16_t    handle,
        PICO_DEVICE_RESOLUTION*    resolution
    ); """
psospa.make_symbol("_GetDeviceResolution","psospaGetDeviceResolution", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS psospaQueryOutputEdgeDetect
    (
        int16_t    handle,
        int16_t*    state
    ); """
psospa.make_symbol("_QueryOutputEdgeDetect","psospaQueryOutputEdgeDetect", c_uint32, [c_int16, c_void_p], doc)

doc = """ PICO_STATUS psospaSetOutputEdgeDetect
    (
        int16_t    handle
        int16_t    state
    ); """
psospa.make_symbol("_SetOutputEdgeDetect","psospaSetOutputEdgeDetect", c_uint32, [c_int16, c_int16], doc)

doc = """ PICO_STATUS psospaGetScalingValues
    (
        int16_t    handle,
        PICO_SCALING_FACTORS_FOR_RANGE_TYPES_VALUES*    scalingValues,
        int16_t    nChannels
    ); """
psospa.make_symbol("_GetScalingValues","psospaGetScalingValues", c_uint32, [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS psospaGetAdcLimits
   (
        int16_t    handle,
        PICO_DEVICE_RESOLUTION    resolution,
        int16_t*    minValue,
        int16_t*    maxValue
    ); """
psospa.make_symbol("_GetAdcLimits","psospaGetAdcLimits", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaCheckForUpdate
    (
        int16_t    handle,
        PICO_FIRMWARE_INFO*    firmwareInfos,
        int16_t*    nFirmwareInfos,
        uint16_t*    updatesRequired
    ); """
psospa.make_symbol("_CheckForUpdate","psospaCheckForUpdate", c_uint32, [c_int16, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaStartFirmwareUpdate
    (
        int16_t    handle,
        PicoUpdateFirmwareProgree    progress
    ); """
psospa.make_symbol("_StartFirmwareUpdate","psospaStartFirmwareUpdate", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaResetChannelsAndReportAllChannelsOvervoltageTripStatus
    (
        int16_t    handle,
        PICO_CHANNEL_OVERVOLTAGE_TRIPPED*    allChannelsTriggedStatus,
        uint8_t    nChannelTrippedStatus
    ); """
psospa.make_symbol("_ResetChannelsAndReportAllChannelsOVervoltageTripStatus","psospaResetChannelsAndReportAllChannelsOvervoltageTripStatus", c_uint32, [c_int16, c_void_p, c_char], doc)

doc = """ PICO_STATUS psospaReportAllChannelsOvervoltageTripStatus
    (
        int16_t    handle,
        PICO_CHANNEL_OVERVOLTAGE_TRIPPED*    allChannelsTriggedStatus,
        uint8_t    nChannelTrippedStatus
    ); """
psospa.make_symbol("_ReportAllChannelsOvervoltageTripStatus","psospaReportAllChannelsOvervoltageTripStatus", c_uint32, [c_int16, c_void_p, c_char], doc)