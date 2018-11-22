#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PicoScope 5000 (A API) Signal Generator Example
# This example demonstrates how to use the PicoScope 5000 Series (ps5000a) driver API functions to set up the signal generator to do the following:
# 
# 1. Output a sine wave 
# 2. Output a square wave 
# 3. Output a sweep of a square wave signal

import ctypes
from picosdk.ps5000a import ps5000a as ps
import time
from picosdk.functions import assert_pico_ok


status = {}
chandle = ctypes.c_int16()

# Open the device
status["openUnit"] = ps.ps5000aOpenUnit(ctypes.byref(chandle), None, 1)


try:
    assert_pico_ok(status["openUnit"])
except: # PicoNotOkError:

    powerStatus = status["openUnit"]

    if powerStatus == 286:
        status["changePowerSource"] = ps.ps5000aChangePowerSource(chandle, powerStatus)
    elif powerStatus == 282:
        status["changePowerSource"] = ps.ps5000aChangePowerSource(chandle, powerStatus)
    else:
        raise

    assert_pico_ok(status["changePowerSource"])

# Output a sine wave with peak-to-peak voltage of 2 V and frequency of 10 kHz
# handle = chandle
# offsetVoltage = 0
# pkToPk = 2000000
# waveType = ctypes.c_int16(0) = PS5000A_SINE
# startFrequency = 10 kHz
# stopFrequency = 10 kHz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS5000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS5000A_SIGGEN_RISING
# triggerSource = ctypes.c_int16(0) = PS5000A_SIGGEN_NONE
# extInThreshold = 0
wavetype = ctypes.c_int32(0)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["setSigGenBuiltInV2"] = ps.ps5000aSetSigGenBuiltInV2(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 0)
assert_pico_ok(status["setSigGenBuiltInV2"])


# Pauses the script to show signal
time.sleep(10)

# Output a square wave with peak-to-peak voltage of 2 V and frequency of 10 kHz
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS5000A_SQUARE
# startFrequency = 10 kHz
# stopFrequency = 10 kHz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS5000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS5000A_SIGGEN_RISING
# triggerSource = ctypes.c_int16(0) = PS5000A_SIGGEN_NONE
# extInThreshold = 0
wavetype = ctypes.c_int32(1)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["setSigGenBuiltInV2"] = ps.ps5000aSetSigGenBuiltInV2(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 0)
assert_pico_ok(status["setSigGenBuiltInV2"])

# Pauses the script to show signal
time.sleep(10)

# Output a square wave with an up-down sweep, 10-100 kHz in 5 kHz increments every 1 second.
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS5000A_SQUARE
# startFrequency = 10 kHz
# stopFrequency = 100 kHz
# increment = 5 kHz
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS5000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS5000A_SIGGEN_RISING
# triggerSource = ctypes.c_int16(0) = PS5000A_SIGGEN_NONE
# extInThreshold = 0
wavetype = ctypes.c_int32(1)
sweepType = ctypes.c_int32(2)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["setSigGenBuiltInV2"] = ps.ps5000aSetSigGenBuiltInV2(chandle, 0, 2000000, wavetype, 10000, 100000, 5000, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 0)
assert_pico_ok(status["setSigGenBuiltInV2"])

# Pauses the script to show signal
time.sleep(36)

# Closes the unit
# Handle = chandle
status["close"] = ps.ps5000aCloseUnit(chandle)
assert_pico_ok(status["stop"])

# Displays the status returns
print(status)