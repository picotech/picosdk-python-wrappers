#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PicoScope 6000 SERIES SIGNAL GENERATOR EXAMPLE
# This example demonstrates how to use the PicoScope 6000 Series (ps6000) driver API functions to set up the signal generator to do the following:
# Opens a 6000 driver device, sets up the signal generator to produce a sine wave, then a square wave
# followed by a sweep of a square wave signal

import ctypes
from picosdk.ps6000 import ps6000 as ps
import time
from picosdk.functions import assert_pico_ok


# Gives the device a handle
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps6000OpenUnit(ctypes.byref(chandle), None)
assert_pico_ok(status["openunit"])

# Output a sine wave with a 2 V peak-to-peak with a 10 kHz frequency
# handle = chandle
# offsetVoltage = 0
# pkToPk = 2000000
# waveType = ctypes.c_int16(0) = PS6000_SINE
# startFrequency = 10000 Hz
# stopFrequency = 10000 Hz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS6000_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS6000_SIGGEN_RISING
# triggerSource = ctypes.c_int16(0) = P6000_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int16(0)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps6000SetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])

# Pauses the script to show signal
time.sleep(10)

# Output a square wave with a 2 V peak-to-peak
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS6000_SQUARE
# startFrequency = 10000 Hz
# stopFrequency = 10000 Hz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS6000_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS6000_SIGGEN_RISING
# triggerSource = ctypes.c_int16(0) = P6000_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int16(1)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps6000SetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSignGenBuiltIn"])

# Pauses the script to show signal
time.sleep(10)

# Output a sweep of a square wave with a up down sweep, 10-100 kHz in 5 kHz increments every 1 second.
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS6000_SQUARE
# startFrequency = 10000 Hz
# stopFrequency = 100000 Hz
# increment = 5
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS6000_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS6000_SIGGEN_RISING
# triggerSource = ctypes.c_int16(0) = P6000_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int16(1)
sweepType = ctypes.c_int32(2)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps6000SetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 100000, 5, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])

# Pauses the script to show signal
time.sleep(36)

# Closes the unit
# Handle = chandle
status["close"] = ps.ps6000CloseUnit(chandle)
assert_pico_ok(status["close"])

# Displays the status returns
print(status)