#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
# PS6000 A SIGNAL GENERATOR EXAMPLE
# This example opens a 6000a driver device, sets up the signal generator to do the following:
# 
# 1. Output a sine wave 
# 2. Output a square wave 
# 3. Output a sweep of a square wave signal

import ctypes
import numpy as np
from picosdk.ps6000a import ps6000a as ps
from picosdk.PicoDeviceEnums import picoEnum as enums
from picosdk.functions import adc2mV, assert_pico_ok
import time

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 6000 A series PicoScope
# returns handle to chandle for use in future API functions
resolution = enums.PICO_DEVICE_RESOLUTION["PICO_DR_8BIT"]
status["openunit"] = ps.ps6000aOpenUnit(ctypes.byref(chandle), None, resolution)
assert_pico_ok(status["openunit"])

# Set signal generator waveform
# handle = chandle
wavetype = enums.PICO_WAVE_TYPE["PICO_SINE"]
bufferlength = 1000
buffer = (ctypes.c_int16 * bufferlength)()
status["sigGenWaveform"] = ps.ps6000aSigGenWaveform(chandle, wavetype, ctypes.byref(buffer), bufferlength)
assert_pico_ok(status["sigGenWaveform"])

# Set signal generator range
# handle = chandle
peakToPeakVolts = 2
offsetVolts = 0
status["sigGenRange"] = ps.ps6000aSigGenRange(chandle, peakToPeakVolts, offsetVolts)
assert_pico_ok(status["sigGenRange"])

# Set signal generator duty cycle
# handle = chandle
dutyCyclePercent = 50
status["sigGenDutyCycle"] = ps.ps6000aSigGenWaveformDutyCycle(chandle, dutyCyclePercent)
assert_pico_ok(status["sigGenDutyCycle"])

# Set signal generator frequency
# handle = chandle
frequencyHz = 1000
status["sigGenFreq"] = ps.ps6000aSigGenFrequency(chandle, frequencyHz)
assert_pico_ok(status["sigGenFreq"])

# Apply signal generator settings
# handle = chandle
sigGenEnabled = 1
sweepEnabled = 0
triggerEnabled = 0
automaticClockOptimisationEnabled = 0
overrideAutomaticClockAndPrescale = 0
frequency = ctypes.c_int16(frequencyHz)
#stopFrequency = None
#frequencyIncrement = None
#dwellTime = None
status["sigGenApply"] = ps.ps6000aSigGenApply(chandle, 
                                              sigGenEnabled, 
                                              sweepEnabled, 
                                              triggerEnabled, 
                                              automaticClockOptimisationEnabled, 
                                              overrideAutomaticClockAndPrescale, 
                                              ctypes.byref(frequency), 
                                              None,
                                              None,
                                              None
                                              )
assert_pico_ok(status["sigGenApply"])

time.sleep(5)

# Pause signal generator
# handle = chandle
status["sigGenPause"] = ps.ps6000aSigGenPause(chandle)
assert_pico_ok(status["sigGenPause"])

time.sleep(5)

# Resume signal generator
# handle = chandle
status["sigGenRestart"] = ps.ps6000aSigGenRestart(chandle)
assert_pico_ok(status["sigGenRestart"])

time.sleep(5)

# Pause signal generator
# handle = chandle
status["sigGenPause"] = ps.ps6000aSigGenPause(chandle)
assert_pico_ok(status["sigGenPause"])

# Close the scope
status["closeunit"] = ps.ps6000aCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

print(status)