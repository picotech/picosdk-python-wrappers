#
# Copyright (C) 2022 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the functions from the picosynth.h C header file
for the PicoSource AS108 Agile Synthesizer using the picosynth driver API functions.
"""

from ctypes import *
from picosdk.library import Library
from picosdk.errors import ArgumentOutOfRangeError
from picosdk.constants import make_enum

class Picosynthlib(library):
    def __init__(self):
        super(Picosynthlib, self).__init__("picosynth")
        
picosynth = Picosynthlib()

picosynth.PICO_SOURCE_MODEL = make_enum([
    "PICO_NONE_SPECIFIED",
    "PICO_SYNTH",
])

doc = """ PICO_STATUS picosynthOpenUnit
    (
        PICO_SOURCE_MODEL  model,
        uint32_t  *handle,
        unit8_t  *serialNumber
    );"""
picosynth.make_symbol("_OpenUnit","picosynthOpenUnit",c_uint32,[c_uint32, c_void_p, c_void_p],doc)

doc = """ PICO_STATUS picosynthEnumerateUnits
    (
        PICO_SOURCE_MODEL  model,
        uint8_t  *serials,
        unit16_t  *serialLth
    );"""
picosynth.make_symbol("_EnumerateUnits","picosynthEnumerateUnits",c_uint32,[c_uint32, c_void_p, c_void_p],doc)

doc = """ PICO_STATUS picosynthGetUnitInfo
    (
        int8_t  *string,
        unit16_t  stringLength,
        uint16_t  *requiredSize,
        PICO_INFO  deviceInfo
    );"""
picosynth.make_symbol("_GetUnitInfo","picosynthGetUnitInfo",c_uint32,[c_uint32, c_void_p, c_uint16, c_void_p, c_uint32],doc)

doc = """ PICO_STATUS picosynthPingUnit
    (
        uint32_t  *handle,
    );"""
picosynth.make_symbol("_PingUnit","picosynthPingUnit",c_uint32,[c_uint32],doc)

doc = """ PICO_STATUS picosynthCloseUnit
    (
        uint32_t  *handle,
    );"""
picosynth.make_symbol("_CloseUnit","picosynthCloseUnit",c_uint32,[c_uint32],doc)

doc = """ PICO_STATUS picosynthSetOutputOff
    (
        uint32_t  *handle,
    );"""
picosynth.make_symbol("_SetOutputOff","picosynthSetOutputOff",c_uint32,[c_uint32],doc)

doc = """ PICO_STATUS picosynthSetFrequency
    (
        uint32_t  *handle,
        double  frequencyHz,
        double  powerLeveldBm
    );"""
picosynth.make_symbol("_SetFrequency","picosynthSetFrequency",c_uint32,[c_uint32, c_double, c_double],doc)

doc = """ PICO_STATUS picosynthSetPhase
    (
        uint32_t  handle,
        double  phaseDeg
    );"""
picosynth.make_symbol("_SetPhase", "picosynthSetPhase", c_uint32,[c_uint32, c_double], doc)

doc = """ PICO_STATUS picosynthSetAmplitudeModulation
    (
        uint32_t  handle,
        double  frequencyHz,
        double  powerLeveldBm,
        double  modulationDepthPercent,
        double  modulationRateHz,
        MODULATION_SOURCE  modulationSource,
        int16_t  enabled
    );"""
picosynth.make_symbol("_SetAmplitudeModulation","picosynthSetAmplitudeModulation", c_uint32,[c_uint32,c_double,c_double,c_double,c_double,c_uint32,c_int16],doc)

doc = """ PICO_STATUS picosynthSetFrequencyModulation
    (
        uint32_t  handle,
        double  frequencyHz,
        double  powerLeveldBm,
        double  modulationDeviationHz,
        double  modulationRateHz,
        MODULATION_SOURCE  modulationSource,
        int16_t  enabled
    );"""
picosynth.make_symbol("_SetFrequencyModulation","picosynthSetFrequencyModulation",c_uint32,[c_uint32,c_double,c_double,c_double,c_double,c_uint32,c_int16],doc)

doc = """ PICO_STATUS picosynthSetPhaseModulation
    (
        uint32_t  handle,
        double  frequencyHz,
        double  powerLeveldBm,
        double  modulationDeviationHz,
        double  modulationRateHz,
        MODULATION_SOURCE  modulationSource,
        int16_t  enabled
    );"""
picosynth.make_symbol("_SetPhaseModulation","picosynthSetPhaseModulation",c_uint32,[c_uint32,c_double,c_double,c_double,c_double,c_uint32,c_int16],doc)

doc = """ PICO_STATUS picosynthSetFrequencyAndLevelSweep
    (
        uint32_t  handle,
        double  startFrequencyHz,
        double  stopFrequencyHz,
        double  startLevel,
        double  stopLevel,
        LEVEL_UNIT  levelUnit,
        double  dwellTimeUs,
        int32_t  pointsInSweep,
        SWEEP_HOP_MODE  mode,
        TRIGGER_MODE  triggerMode
    );"""
picosynth.make_symbol("_SetFrequencyAndLevelSweep","picosynthSetFrequencyAndLevelSweep", c_uint32,[c_uint32,c_double,c_double,c_double,c_double,c_uint32,c_double,c_int32,c_uint32,c_uint32],doc)

doc = """ PICO_STATUS picosynthSetPhaseAndLevelSweep
    (
        uint32_t  handle,
        double  frequencyHz,
        double  startPhaseDeg,
        double  stopPhaseDeg,
        double  startLevel,
        double  stopLevel,
        LEVEL_UNIT levelUnit,
        double  dwellTimeUs,
        int32_t  pointsInSweep,
        SWEEP_HOP_MODE  mode,
        TRIGGER_MODE  triggerMode
    );"""
picosynth.make_symbol("_SetPhaseAndLevelSweep","picosynthSetPhaseAndLevelSweep", c_uint32,[c_uint32,c_double,c_double,c_double,c_double,c_double,c_uint32,c_double,c_int32,c_uint32,c_uint32],doc)

doc = """ PICO_STATUS picosynthSetArbitraryPhaseAndLevel
    (
        uint32_t  handle,
        double  frequencyHz,
        double  *arbitraryPhaseDeg,
        double  *arbitraryPowerLeveldBm,
        int32_t  numberOfPoints,
        double  dwellTimeUs,
        TRIGGER_MODE  triggerMode
    );"""
picosynth.make_symbol("_SetArbitraryPhaseAndLevel","picosynthSetArbitraryPhaseAndLevel",c_uint32,[c_uint32,c_double,c_double,c_double,c_int32,c_double,c_uint32],doc)

doc = """ PICO_STATUS picosynthSetArbitraryFrequencyAndLevel
    (
        uint32_t  handle,
        double  *arbitraryFrequencyHz,
        double  *arbitraryPowerLeveldBm,
        int32_t  numberOfPoints,
        double  dwellTimeUs,
        TRIGGER_MODE  triggerMode
    );"""
picosynth.make_symbol("_SetArbitraryFrequencyAndLevel","picosynthSetArbitraryFrequencyAndLevel",c_uint32,[c_uint32,c_double,c_double,c_int32,c_double,c_uint32],doc)
