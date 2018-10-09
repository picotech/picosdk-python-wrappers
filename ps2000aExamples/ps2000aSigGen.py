#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PS2000a SIGNAL GENERATOR EXAMPLE
# This example opens a 2000a driver device, sets up the signal generator to produce a sine wave, then a square wave,
# followed by a sweep of a square wave signal

import ctypes
from picosdk.ps2000a import ps2000a as ps
import time
from picosdk.functions import assert_pico_ok


# Gives the device a handle
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps2000aOpenUnit(ctypes.byref(chandle), None)

try:
    assert_pico_ok(status["openunit"])
except:
    # powerstate becomes the status number of openunit
    powerstate = status["openunit"]

    # If powerstate is the same as 282 then it will run this if statement
    if powerstate == 282:
        # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
        status["ChangePowerSource"] = ps.ps2000aChangePowerSource(chandle, 282)
    # If the powerstate is the same as 286 then it will run this if statement
    elif powerstate == 286:
        # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
        status["ChangePowerSource"] = ps.ps2000aChangePowerSource(chandle, 286)
    else:
        raise

    assert_pico_ok(status["ChangePowerSource"])

# Generates Sine signal with a 2 V peak-to-peak with a 10 kHz frequency
# handle = chandle
# offsetVoltage = 0
# pkToPk = 2000000
# waveType = ctypes.c_int16(0) = PS2000A_SINE
# startFrequency = 10000 Hz
# stopFrequency = 10000 Hz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS2000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS2000A_SIGGEN_NONE
# triggerSource = ctypes.c_int16(0) = P2000A_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int16(0)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps2000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])

# Pauses the script to show signal
time.sleep(10)

# Generates Sqaure signal with a 2 V peak-to-peak
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS2000A_SQUARE
# startFrequency = 10000 Hz
# stopFrequency = 10000 Hz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS2000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(1) = PS2000A_SIGGEN_NONE
# triggerSource = ctypes.c_int16(1) = P2000A_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int16(1)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps2000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])

# pauses the script to show signal
time.sleep(10)

# Generates square signal with a up down sweep, starting at 10-100 in 5 kHz increments every 1 second.
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS2000A_SQUARE
# startFrequency = 10000 Hz
# stopFrequency = 100000 Hz
# increment = 5
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS2000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(0) = PS2000A_SIGGEN_NONE
# triggerSource = ctypes.c_int16(0) = P2000A_SIGGEN_NONE
# extInThreshold = 1
wavetype = ctypes.c_int16(1)
sweepType = ctypes.c_int32(2)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps2000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 100000, 5, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)
assert_pico_ok(status["SetSigGenBuiltIn"])

# Pauses the script to show signal
time.sleep(36)

# Stops the scope
# Handle = chandle
status["stop"] = ps.ps2000aStop(chandle)
assert_pico_ok(status["stop"])

# Closes the unit
# Handle = chandle
status["close"] = ps.ps2000aCloseUnit(chandle)
assert_pico_ok(status["close"])

# Displays the status returns
print(status)