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

class Psospalib(Library)
    def __init__(self):
	    super(Psospalib, self).__init__("psospa")
	
psospa = Psospalib()

doc = """ PICO_STATUS psospaOpenUnit
    (
	    int16_t*    handle,
		int8_t*     serial,
		PICO_DEVICE_RESOLUTION    resolution,
		PICO_USB_POWER_DETAILS*    powerDetails
	); """
psospa.make_symbol("psospaOpenUnit", c_uint32, [c_void_p, c_char_p, c_int32, c_void_p], doc)

doc = """ PICO_STATUS psospaCloseUnit
    (
	    int16_t    handle
	); """
psospa.make_symbol("psospaCloseUnit", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS psospaGetUnitInfo
    (
        int16_t    handle,
        int8_t*    string,
        int16_t    stringLength,
        int16_t*    requiredSize,
        PICO_INFO    info
    ); """
psospa.make_symbol("psospaGetUnitInfo", c_uint32, [c_int16, c_char_p, c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS psospaGetVariantDetails
    (
        const int8_t*    variantName,
        int16_t    variantNameLength,
        int8_t*    outputString,
        int32_t*    outputStringLength
    ); """
psospa.make_symbol("psospaGetVariantDetails", c_uint32, [c_char_p, c_int16, c_char_p, c_void_p], doc)

doc = """ PICO_STATUS psospaGetAccessoryInfo
    (
        int16_t    handle,
        PICO_CHANNEL    channel,
        int8_t*    string,
        int16_t    stringLength,
        int16_t*    requiredSize,
        PICO_INFO    info
    ); """
psospa.make_symbol("psospaGetAccessoryInfo", c_uint32, [c_int16, c_uint32, c_char_p, c_int16, c_void_p, c_uint32], doc

doc = """ PICO_STATUS psospaMemorySegments
    (
        int16_t    handle,
        uint64_t    nSegments,
        uint64_t*    nMaxSamples
    ); """
psospa.make_symbol("psospaMemorySegments", c_uint32,[c_int16, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS psospaMemorySegmentsBySamples
    (
        int16_t    handle,
        uint64_t    nSamples,
        uint64_t*    nMaxSegments
    ); """
psospa.make_symbol("psospaMemorySegmentsBySamples", c_uint32, [c_int16, c_uint64, c_void_p], doc)

doc = """ PICO_STATUS psospaGetMaximumAvaliableMemory
    (
        int16_t    handle,
        uint64_t*    nMaxSamples,
        PICO_DEVICE_RESOLUTION    resolution
    ); """
psospa.make_symbol("psospaGetMaximumAvaliableMemory", c_uint32, [c_int16, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS psospaQueryMaxSegmentsBySamples
    (
        int16_t    handle,
        uint64_t    nSamples,
        uint32_t    nChannelEnabled,
        uint64_t*    nMaxSegments,
        PICO_DEVICE_RESOLUTION    resolution
    ); """
psospa.make_symbol("psospaQueryMaxSegmentsBySamples", c_uint32, [c_int16, c_uint64, c_uint32, c_void_p, c_uint32], doc)

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
psospa.make_symbol("psospaSetChannelOn", c_uint32, [c_int16, c_uint32, c_uint32, c_int64, c_int64, c_uint32, c_double, c_uint32], doc)

doc = """ PICO_STATUS psospaSetChannelOff
    (
        int16_t    handle,
        PICO_CHANNEL    channel
    ); """
psospa.make_symbol("psospaSetChannelOff", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSetDigitalPortOn
    (
        int16_t    handle,
        PICO_CHANNEL    port,
        int16_t*    logicThresholdLevel,
        int16_t*    logicThresholdLengthLevel,
        PICO_DIGITAL_PORT_HYSTERESIS    hysteresis
    ); """
psospa.make_symbol("psospaSetDigitalPortOn", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p, c_uint32], doc)

doc = """ PICO_STATUS psospaSetDigitalPortOff
    (
        int16_t    handle,
        PICO_CHANNEL    port
    ); """
psospa.make_symbol("psospaSetDigitalPortOff", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaGetTimebase
    (
        int16_t    handle,
        uint32_t    timebase,
        uint64_t    noSamples,
        double*    timeIntervalNanoseconds,
        uint64_t*    maxSamples,
        uint64_t    segmentIndex
    ); """
psospa.make_symbol("psospaGetTimebase", c_uint32, [c_int16, c_uint32, c_uint64, c_void_p, c_void_p, c_uint64], doc)

doc = """ PICO_STATUS psospaSigGenWaveform
    (
        int16_t    handle,
        PICO_WAVE_TYPE    waveType,
        int16_t*    buffer,
        uint64_t    bufferLength
    ); """
psospa.make_symbol("psospaSigGenWaveform", c_uint32, [c_int16, c_uint32, c_void_p, c_uint64], doc)

doc = """ PICO_STATUS psospaSigGenRange
    (
        int16_t    handle,
        double    peakToPeakVolts,
        double    offsetVolts
    ); """
psospa.make_symbol("psospaSigGenRange", c_uint32, [c_int16, c_double, c_double], doc)

doc = """ PICO_STATUS psospaSigGenWaveformDutyCycle
    (
        int16_t    handle,
        double    dutyCyclePercent
    ); """
psospa.make_symbol("psospaSigGenWaveformDutyCycle", c_uint32, [c_int16, c_double], doc)

doc = """ PICO_STATUS psospaSigGenTrigger
    (
        int16_t    handle,
        PICO_SIGGEN_TRIG_TYPE    triggerType,
        PICO_SIGGEN_TRIG_SOURCE    triggerSource,
        uint64_t    cycles,
        uint64_t    autoTriggerPicoSeconds
    ); """
psospa.make_symbol("psospaSigGenTrigger", c_uint32, [c_int16, c_uint32, c_uint32, c_uint64, c_uint64], doc)

doc = """ PICO_STATUS psospaSigGenFilter
    (
        int16_t    handle,
        PICO_SIGGEN_FILTER_STATE    filterState
    ); """
psospa.make_symbol("psospaSigGenFilter", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSigGenFrequency
    (
        int16_t    handle,
        double    frequencyHz
    ); """
psospa.make_symbol("psospaSigGenFrequency", c_uint32, [c_int16, c_double], doc)

doc = """ PICO_STATUS psospaSigGenFrequencySweep
    (
        int16_t    handle,
        double    stopFrequencyHz,
        double    frequencyIncrement,
        double    dwellTimeSeconds,
        PICO_SWEEP_TYPE    sweepType
    ); """
psospa.make_symbol("psospaSigGenFrequencySweep", c_uint32, [c_int16, c_double, c_double, c_double, c_uint32], doc)

doc = """ PICO_STATUS psospaSigGenPhase
    (
        int16_t    handle,
        uint64_t    deltaPhase
    ); """
psospa.make_symbol("psospaSigGenPhase", c_uint32, [c_int16, c_uint64], doc)

doc = """ PICO_STATUS psospaSigGenPhaseSweep
    (
        int16_t    handle,
        uint64_t    stopDeltaPhase,
        uint64_t    deltaPhaseIncrement,
        uint64_t    dwellCount,
        PICO_SWEEP_TYPE    sweepType
    ); """
psospa.make_symbol("psospaSigGenPhaseSweep", c_uint32, [c_int16, c_uint64, c_uint64, c_uint64, c_uint32], doc)

doc = """ PICO_STATUS psospaSigGenClockManual
    (
        int16_t    handle,
        double    dacClockFrequency,
        uint64_t    prescaleRatio
    ); """
psospa.make_symbol("psospaSigGenClockManual", c_uint32, [c_int16, c_double, c_uint64], doc)

doc = """ PICO_STATUS psospaSigGenSoftwareTriggerControl
    (
        int16_t    handle,
        PICO_SIGGEN_TRIG_TYPE    triggerState
    ); """
psospa.make_symbol("psospaSigGenSoftwareTriggerControl", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSigGenApply
    (
        int16_t    handle,
        int16_t    sigGenEnabled,
        int16_t    sweepEnabled,
        int16_t    triggerEnabled,
        int16_t    automaticClockOptimisationEnabled,
        int16_t    overrideAutomaticClockAndPrescale,
        double*    frequency
        double*    stopFrequency,
        double*    frequencyIncrement,
        double*    dwellTime,
    ); """
psospa.make_symbol("psospaSigGenApply", c_uint32, [c_int16, c_int16, c_int16, c_int16, c_int16, c_int16, c_void_p, c_void_p, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaSigGenLimits
    (
        int16_t    handle,
        PICO_SIGGEN_PARAMETER    parameter,
        double*    minimumPermissibleValue,
        double*    maximumPermissibleValue,
        double*    step
    ); """
psospa.make_symbol("psospaSigGenLimits", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p], doc)

doc = """ PICO_STATUS psospaSigGenFrequencyLimits
    (
        int16_t    handle,
        PICO_WAVE_TYPE    waveType,
        uint64_t*    numSamples,
        double*    startFrequency,
        int16_t    sweepEnabled,
        double*    manualDacClockFrequency,
        uint64_t*    manualPrescaleRatio,
        double*    maxStopFrequencyOut,
        double*    minFrequencyStepOut,
        double*    maxFrequencyStepOut,
        double*    minDwellTimeOut,
        double*    maxDwellTimeOut
    ); """
psospa.make_symbol("psospaSigGenFrequencyLimits", c_uint32, [c_int16, c_uint32, c_void_p, c_void_p, c_int16, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p, c_void_p), doc)

doc = """ PICO_STATUS psospaSigGenPause
    (
        int16_t    handle,
    ); """
psospa.make_symbol("psospaSigGenPause", c_uint32, [c_int16], doc)

doc = """ PICO_STATUS psospaSigGenRestart
    (
        int16_t    handle
    ); """
psospa.make_symbol("psospaSigGenRestart", c_uint32, [c_int16], doc)

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
psospa.make_symbol("psospaSetSimpleTrigger", c_uint32, [c_int16, c_int16, c_uint32, c_int16, c_uint32, c_uint64, c_uint32], doc)

doc = """ PICO_STATUS psospaTriggerWithinPreTriggerSamples
    (
        int16_t    handle,
        PICO_TRIGGER_WITHIN_PRE_TRIGGER    state
    ); """
psospa.make_symbol("psospaTriggerWithinPreTriggerSamples", c_uint32, [c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSetTriggerChannelProperties
    (
        int16_t    handle,
        PICO_TRIGGER_CHANNEL_PROPERTIES*    channelProperties,
        int16_t    nChannelProperties,
        int16_t    auxOutputEnable,
        uint32_t    autoTriggerMicroSeconds
    ); """
psospa.make_symbol("psospaSetTriggerChannelProperties", c_uint32, [c_int16, c_void_p, c_int16, c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSetTriggerChannelConditions
   (
        int16_t   handle,
        PICO_CONDITION*   conditions,
        int16_t    nConditions,
        PICO_ACTION    action
    ); """
psospa.make_symbol("psospaSetTriggerChannelConditions", c_uint32, [c_int16, c_void_p, c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSetTriggerChannelDirections
    (
        int16_t    handle,
        PICO_DIRECTION*    directions,
        int16_t    nDirections
    ); """
psospa.make_symbol("psospaSetTriggerChannelDirections", c_uint32, [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS psospaSetTriggerDelay
    (
        int16_t    handle,
        uint64_t    delay
    ); """
psospa.make_symbol("psospaSetTriggerDelay", c_uint32, [c_int16, c_uint64], doc)

doc = """ PICO_STATUS psospaSetTriggerHoldoffCounterBySamples
    (
        int16_t    handle,
        uint64_t    holdoffSamples
    ); """
psospa.make_symbol("psospaSetTriggerHoldoffCounterBySamples", c_uint32, [c_int16, c_uint64], doc)

doc = """ PICO_STATUS psospaSetPulseWidthQualifierProperties
    (
        int16_t    handle,
        uint32_t    lower,
        uint32_t    upper,
        PICO_PULSE_WIDTH_TYPE    type
    ); """
psospa.make_symbol("psospaSetPulseWidthQualifierProperties", c_uint32, [c_int16, c_uint32, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS psospaSetPulseWidthQualifierConditions
   (
        int16_t    handle,
        PICO_CONDITION*    conditions,
        int16_t    nConditions,
        PICO_ACTION    action
    ); """
psospa.make_symbol("psospaSetPulseWidthQualifierConditions", c_uint32, [c_int16, c_void_p, c_int16, c_uint32], doc)

doc = """ PICO_STATUS psospaSetPulseWidthQualifierDirections
    (
        int16_t    handle,
        PICO_DIRECTION*    directions,
        int16_t    nDirections
    ); """
psospa.make_symbol("psospaSetPulseWidthQualifierDirections", c_uint32, [c_int16, c_void_p, c_int16], doc)

doc = """ PICO_STATUS psospaSetTriggerDigitalPortProperties
    (
        int16_t    handle,
        PICO_CHANNEL    port,
        PICO_DIGITAL_CHANNEL_DIRECTIONS*    directions,
        int16_t    nDirections
    ); """
psospa.make_symbol("psospaSetTriggerDigitalPortProperties", c_uint32, [c_int16, c_uint32, c_void_p, c_int16], doc)

doc = """ PICO_STATUS psospaGetTriggerTimeOffset
    (
        int16_t    handle,
        int64_t*    time,
        PICO_TIME_UNITS*    timeUnits,
        uint64_t    segmentIndex
    ); """
psospa.make_symbol("psospaGetTriggerTimeOffset", c_uint32, [c_int16, c_void_p, c_void_p, c_uint64], doc)

doc = """ PICO_STATUS psospaGetValuesTriggerTimeOffsetBulk
    (
        int16_t    handle,
        int64_t*    times,
        PICO_TIME_UNITS*    timeUnits,
        uint64_t    fromSegmentIndex,
        uint64_t    toSegmentIndex
    ); """
psospa.make_symbol("psospaGetValuesTriggerTimeOffsetBulk", c_uint32, [c_int16, c_void_p, c_void_p, c_uint64, c_uint64], doc)

doc = """ PICO_STATUS psospaSetDataBuffer
    (
        int16_t    handle,
        PICO_CHANNEL    channel,
        PICO_POINTER    buffer,
        int32_t    nSamples,
        PICO_DATA_TYPE    dataType,
        uint64_t    waveform,
        PICO_RATIO_MODE    downSampleRationMode,
        PICO_ACTION    action
    ); """
psospa.make_symbol("psospaSetDataBuffer", c_uint32, [c_int16, c_uint32, c_uint32, c_uint32, c_uint32, c_uint64, c_uint32, c_uint32], doc)

doc = """ PICO_STATUS psospaSetDataBuffers
    (
        int16_t    handle,
        PICO_CHANNEL    channel,
        PICO_POINTER    bufferMax,
        PICO_POINTER    bufferMin,
        int32_t    nSamples,
        PICO_DATA_TYPE    dataType,
        uint64_t    waveform,
        PICO_RATIO_MODE    downSampleRationMode,
        PICO_ACTION    action
    ); """
psospa.make_symbol("psospaSetDataBuffers", c_uint32, [c_int16, c_uint32, c_uint32, c_uint32, c_int32, c_uint32, c_uint64, c_uint32, c_uint32], doc)

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
psospa.make_symbol("psospaRunBlock", c_uint32, [c_int16, c_uint64, c_uint64, c_uint32, c_void_p, c_uint64, c_void_p, c_uint32], doc)