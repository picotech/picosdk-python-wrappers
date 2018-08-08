#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PS6000 SIGNAL GENERATOR EXAMPLE
# This example opens a 6000 driver device, sets up the singal generator to produce a sine wave, then a a square wave
# then perform a sweep of a square wave signal

import ctypes
from picosdk.ps6000 import ps6000 as ps
import time



# Gives the device a handle 
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps6000OpenUnit(ctypes.byref(chandle), None)

# powerstate becomes the status number of openunit
powerstate = status["openunit"]

# If powerstate is the same as 282 then it will run this if statement
if powerstate == 282:
    # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
    status["ChangePowerSource"] = ps.ps6000ChangePowerSource(chandle, 282)

# If the powerstate is the same as 286 then it will run this if statement
if powerstate == 286:
    # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
    status["ChangePowerSource"] = ps.ps6000ChangePowerSource(chandle, 286) 

# Generates Sine signal with a 2V pkToPk with a 10KHz frequency 
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
# triggerType = ctypes.c_int16(1) = PS6000_SIGGEN_NONE
# triggerSource = ctypes.c_int16(1) = P6000_SIGGEN_NONE 
# extInThreshold = 1
wavetype = ctypes.c_int16(0)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps6000SetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)

# pauses the script to show signal
time.sleep(10)

# Generates Sqaure signal with a 2V pkToPk 
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000
# waveType = ctypes.c_int16(1) = PS6000_Sqaure
# startFrequency = 10000 Hz
# stopFrequency = 10000 Hz
# increment = 0
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS6000_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(1) = PS6000_SIGGEN_NONE
# triggerSource = ctypes.c_int16(1) = P6000_SIGGEN_NONE 
# extInThreshold = 1
wavetype = ctypes.c_int16(1)
sweepType = ctypes.c_int32(0)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps6000SetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 10000, 0, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)

# pauses the script to show signal
time.sleep(10)

# Generates sqaure signal with a up down sweep, starting at 10-100 in 5KHz increments every 1 second. 
# handle = chandle
# offsetVoltage = -1000000
# pkToPk = 1500000 
# waveType = ctypes.c_int16(1) = PS6000_Square
# startFrequency = 10000 Hz
# stopFrequency = 100000 Hz
# increment = 5
# dwellTime = 1
# sweepType = ctypes.c_int16(1) = PS6000_UP
# operation = 0
# shots = 0
# sweeps = 0
# triggerType = ctypes.c_int16(1) = PS6000_SIGGEN_NONE
# triggerSource = ctypes.c_int16(1) = P6000_SIGGEN_NONE 
# extInThreshold = 1
wavetype = ctypes.c_int16(1)
sweepType = ctypes.c_int32(2)
triggertype = ctypes.c_int32(0)
triggerSource = ctypes.c_int32(0)

status["SetSigGenBuiltIn"] = ps.ps6000SetSigGenBuiltIn(chandle, 0, 2000000, wavetype, 10000, 100000, 5, 1, sweepType, 0, 0, 0, triggertype, triggerSource, 1)

# pauses the script to show signal 
time.sleep(36)

# Stops the scope 
# Handle = chandle
status["stop"] = ps.ps6000Stop(chandle)

# Displays the staus returns
print(status)

# Closes the unit 
# Handle = chandle 
ps.ps6000CloseUnit(chandle)
