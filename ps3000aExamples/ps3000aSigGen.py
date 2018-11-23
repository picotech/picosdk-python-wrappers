#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PicoScope 3000 (A API) Series Signal Generator Example
# This example demonstrates how to use the PicoScope 3000 Series (ps3000a) driver API functions to set up the signal generator to do the following:
# 
# 1. Output a sine wave 
# 2. Output a square wave 
# 3. Output a sweep of a square wave signal

import ctypes
from picosdk.ps3000a import ps3000a as ps
import time
from picosdk.functions import assert_pico_ok


# Gives the device a handle
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps3000aOpenUnit(ctypes.byref(chandle), None)

try:
    assert_pico_ok(status["openunit"])
except:

    # powerstate becomes the status number of openunit
    powerstate = status["openunit"]

    # If powerstate is the same as 282 then it will run this if statement
    if powerstate == 282:
        # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
        status["ChangePowerSource"] = ps.ps3000aChangePowerSource(chandle, 282)
    # If the powerstate is the same as 286 then it will run this if statement
    elif powerstate == 286:
        # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
        status["ChangePowerSource"] = ps.ps3000aChangePowerSource(chandle, 286)
    else:
        raise

    assert_pico_ok(status["ChangePowerSource"])

# Output a sine wave with peak-to-peak voltage of 2 V and frequency of 10 kHz
# handle = chandle
# offsetVoltage = 0
# pkToPk = 2000000
# waveType = ctypes.c_int16(0) = PS3000A_SINE
# startFrequency = 10000 Hz
# stopFrequency = 10000 Hz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS3000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS3000A_SIGGEN_RISING
# triggerSource = ctypes.c_int16(0) = P3000A_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int16(0)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps3000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])

# Pauses the script to show signal
time.sleep(10)

# Output a square wave with peak-to-peak voltage of 2 V and frequency of 10 kHz
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS3000A_SQUARE
# startFrequency = 10 kHz
# stopFrequency = 10 kHz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS3000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS3000A_SIGGEN_RISING
# triggerSource = ctypes.c_int16(0) = P3000A_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int16(1)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps3000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])

# Pauses the script to show signal
time.sleep(10)

# Output a square wave with an up-down sweep, 10-100 kHz in 5 kHz increments every 1 second.
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS3000A_Square
# startFrequency = 100 kHz
# stopFrequency = 100 kHz
# increment = 5 kHz
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS3000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS3000A_SIGGEN_RISING
# triggerSource = ctypes.c_int16(0) = P3000A_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int16(1)
sweepType = ctypes.c_int32(2)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps3000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 100000, 5000, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])

# Pauses the script to show signal
time.sleep(36)

# Closes the unit
# Handle = chandle
status["close"] = ps.ps3000aCloseUnit(chandle)
assert_pico_ok(status["close"])

# Displays the status returns
print(status)
