#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the structures from the PicoDeviceStructs.h C header
file for use with PicoScope 6000 A Series oscilloscopes using the ps6000a driver API
functions.
"""

from ctypes import *
from picosdk.library import Library

class PicoStructlib(Library):
    def __init__(self):
        super(PicoStructlib, self).__init__("ps6000a")


picoStruct = PicoStructlib()

class PICO_TRIGGER_INFO(Structure):
    _pack_ = 1
    _fields_ = [("status", c_uint32),
                ("segmentIndex", c_uint64),
                ("triggerIndex", c_uint64),
                ("triggerTime", c_double),
                ("timeUnits", c_uint32),
                ("missedTriggers", c_uint64),
                ("timeStampCounter", c_uint64)]
                
picoStruct.PICO_TRIGGER_INFO = PICO_TRIGGER_INFO

class PICO_TRIGGER_CHANNEL_PROPERTIES(Structure):
    _pack_ = 1
    _fields_ = [("thresholdUpper", c_int16),
                ("thresholdUpperHysteresis", c_uint16),
                ("thresholdLower", c_int16),
                ("thresholdLowerHysteresis", c_uint16),
                ("channel", c_uint32)]
                
picoStruct.PICO_TRIGGER_CHANNEL_PROPERTIES = PICO_TRIGGER_CHANNEL_PROPERTIES

class PICO_CONDITION(Structure):
    _pack_ = 1
    _fields_ = [("source", c_uint32),
                ("condition", c_uint32)]
                
picoStruct.PICO_CONDITION = PICO_CONDITION

class PICO_DIRECTION(Structure):
    _pack_ = 1
    _fields_ = [("channel", c_uint32),
                ("direction", c_uint32),
                ("thresholdMode", c_uint32)]
                
picoStruct.PICO_DIRECTION = PICO_DIRECTION

class PICO_USER_PROBE_INTERACTIONS(Structure):
    _pack_ = 1
    _fields_ = [("connected", c_uint16),
                ("channel", c_uint32),
                ("enabled", c_uint16),
                ("probeName", c_uint32),
                ("requiresPower", c_uint8),
                ("isPowered", c_uint8),
                ("status", c_uint32),
                ("probeOff", c_uint32),
                ("rangeFirst", c_uint32),
                ("rangeLast", c_uint32),
                ("rangeCurrent", c_uint32),
                ("couplingFirst", c_uint32),
                ("couplingLast", c_uint32),
                ("couplingCurrent", c_uint32),
                ("filterFlags", c_uint32),
                ("filterCurrent", c_uint32)]
                
picoStruct.PICO_USER_PROBE_INTERACTIONS = PICO_USER_PROBE_INTERACTIONS

class PICO_DATA_BUFFERS(Structure):
    _pack_ = 1
    _fields_ = [("channel", c_uint32),
                ("waveform", c_uint64),
                ("downSampleRatioMode", c_uint32),
                ("read", c_uint32),
                ("bufferMax", c_void_p),
                ("bufferMin", c_void_p),
                ("dataType", c_uint32),
                ("nDistributionPoints", c_uint32)]
                
picoStruct.PICO_DATA_BUFFERS = PICO_DATA_BUFFERS

class PICO_STREAMING_DATA_INFO(Structure):
    _pack_ = 1
    _fields_ = [("channel", c_uint32),
                ("mode", c_uint32),
                ("type", c_uint32),
                ("noOfSamples", c_int32),
                ("bufferIndex", c_uint64),
                ("startIndex", c_int32),
                ("overflow", c_int16)]
                
picoStruct.PICO_STREAMING_DATA_INFO = PICO_STREAMING_DATA_INFO

class PICO_STREAMING_DATA_TRIGGER_INFO(Structure):
    _pack_ = 1
    _fields_ = [("triggerAt", c_uint64),
                ("triggered", c_int16),
                ("autoStop", c_int16)]
                
picoStruct.PICO_STREAMING_DATA_TRIGGER_INFO = PICO_STREAMING_DATA_TRIGGER_INFO

class PICO_SCALING_FACTORS(Structure):
    _pack_ = 1
    _fields_ = [("channel", c_uint32),
                ("range", c_uint32),
                ("offset", c_int16),
                ("scalingFactor", c_double)]
                
picoStruct.PICO_SCALING_FACTORS = PICO_SCALING_FACTORS

class PROBE_APP(Structure):
    _pack_ = 1
    _fields_ = [("id", c_int32),
                ("appMajorVersion", c_int32),
                ("appMinorVersion", c_int32)]
               
picoStruct.PROBE_APP = PROBE_APP

class DIGITAL_CHANNEL_DIRECTIONS(Structure):
    _pack_ = 1
    _fields_ = [("channel", c_uint32),
                ("direction", c_uint32)]
                
picoStruct.DIGITAL_CHANNEL_DIRECTIONS = DIGITAL_CHANNEL_DIRECTIONS

class PICO_DIGITAL_PORT_INTERACTIONS(Structure):
    _pack_ = 1
    _fields_ = [("connected", c_uint16),
                ("channel", c_uint32),
                ("digitalPortName", c_uint32),
                ("status", c_uint32),
                ("serial", c_int8),
                ("calibrationDate", c_int8)]
                
picoStruct.PICO_DIGITAL_PORT_INTERACTIONS = PICO_DIGITAL_PORT_INTERACTIONS