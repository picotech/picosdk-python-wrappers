#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
"""
This is a Python module defining the structures from the PicoDeviceStructs.h C header
file for use with PicoScope 6000 A Series oscilloscopes using the ps6000a driver API
functions.
"""

from ctypes import *

class PicoStructlib(Library):
    def __init__(self):
        super(PicoStructlib, self).__init__("PicoDeviceStructs")


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