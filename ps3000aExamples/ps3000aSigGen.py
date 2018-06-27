#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PS3000A SIGNAL GENERATOR EXAMPLE
# This example opens a 3000a driver device, sets up the singal generator to produce a sine wave, then a a square wave
# then perform a sweep of a square wave signal

import ctypes
from picosdk.ps3000a import ps3000a as ps
import time



# Gives the device a handle 
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps3000aOpenUnit(ctypes.byref(chandle), None)

# Generates Sine signal with a 2V pkToPk with a 10KHz frequency 
# handle = chandle
# offsetVoltage = 0
# pkToPk = 2000000
# waveType = ctypes.c_int16(0) = PS3000A_SINE
# startFrequency = 10
# stopFrequency = 10
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS3000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(1) = PS3000A_SIGGEN_NONE
# triggerSource = ctypes.c_int16(1) = P3000A_SIGGEN_NONE 
# extInThreshold = 1
wavetype = ctypes.c_int16(0)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps3000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10, 10, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)

# pauses the script to show signal
time.sleep(10)

# Generates Sqaure signal with a 2V pkToPk 
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS3000A_Sqaure
# startFrequency = 10
# stopFrequency = 10
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS3000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(1) = PS3000A_SIGGEN_NONE
# triggerSource = ctypes.c_int16(1) = P3000A_SIGGEN_NONE 
# extInThreshold = 1
wavetype = ctypes.c_int16(1)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps3000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10, 10, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)

# pauses the script to show signal
time.sleep(10)

# Generates sqaure signal with a up down sweep, starting at 10-100 in 5KHz increments every 1 second. 
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000 
# waveType = ctypes.c_int16(1) = PS3000A_Square
# startFrequency = 10
# stopFrequency = 100
# increment = 5
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS3000A_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(1) = PS3000A_SIGGEN_NONE
# triggerSource = ctypes.c_int16(1) = P3000A_SIGGEN_NONE 
# extInThreshold = 1
wavetype = ctypes.c_int16(1)
sweepType = ctypes.c_int32(2)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps3000aSetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10, 100, 5, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)

# pauses the script to show signal 
time.sleep(36)

# Stops the scope 
# Handle = chandle
status["stop"] = ps.ps3000aStop(chandle)

# Displays the staus returns
print(status)

# Closes the unit 
# Handle = chandle 
ps.ps3000aCloseUnit(chandle)
