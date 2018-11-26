#
# Copyright (C) 2018 Pico Technology Ltd. See LICENSE file for terms.
#
# PicoScope 3000 Series (A API) MSO Block Mode Example
# This example demonstrates how to use the PicoScope 3000 Series (ps3000a) driver API functions in order to do the
# following:
#
# Opens a connection to a PicoScope 3000 Series MSO device
# Setup a digital port
# Setup a trigger on a digital channel
# Collect a block of data
# Plot data

import ctypes
from picosdk.ps3000a import ps3000a as ps
from picosdk.functions import splitMSOData, assert_pico_ok
import numpy as np
import matplotlib.pyplot as plt

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

# set up digital port
# handle = chandle
# PS3000A_DIGITAL_PORT = 0x80
# Enable = 1
# logicLevel = 10000
status["SetDigitalPort"] = ps.ps3000aSetDigitalPort( chandle, 0x80, 1, 10000)
assert_pico_ok(status["SetDigitalPort"])

# Setting the number of sample to be collected
preTriggerSamples = 400
postTriggerSamples = 400
maxsamples = preTriggerSamples + postTriggerSamples

# Gets timebase information
# Handle = chandle
# Timebase = 2 = timebase
# Nosample = maxsamples
# TimeIntervalNanoseconds = ctypes.byref(timeIntervalns)
# MaxSamples = ctypes.byref(returnedMaxSamples)
# Segement index = 0
timebase = 8
timeIntervalns = ctypes.c_float()
returnedMaxSamples = ctypes.c_int16()
status["GetTimebase"] = ps.ps3000aGetTimebase2(chandle, timebase, maxsamples, ctypes.byref(timeIntervalns), 1, ctypes.byref(returnedMaxSamples), 0)
assert_pico_ok(status["GetTimebase"])

# Creates a overlow location for data
overflow = ctypes.c_int16()
# Creates converted types maxsamples
cmaxSamples = ctypes.c_int32(maxsamples)

# Create buffers ready for assigning pointers for data collection
bufferAMax = (ctypes.c_int16 * maxsamples)()
bufferAMin = (ctypes.c_int16 * maxsamples)()

# Setting the data buffer location for data collection from PS3000A_DIGITAL_PORT0
# Handle = Chandle
# source = PS3000A_DIGITAL_PORT0 = 0x80
# Buffer max = ctypes.byref(bufferAMax)
# Buffer min = ctypes.byref(bufferAMin)
# Buffer length = maxsamples
# Segment index = 0
# Ratio mode = ps3000A_Ratio_Mode_None = 0
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0x80, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin),
                                                    maxsamples, 0, 0)
assert_pico_ok(status["SetDataBuffers"])

# Starts the block capture
# Handle = chandle
# Number of prTriggerSamples
# Number of postTriggerSamples
# Timebase = 2 = 4ns (see Programmer's guide for more information on timebases)
# time indisposed ms = None (This is not needed within the example)
# Segment index = 0
# LpRead = None
# pParameter = None
status["runblock"] = ps.ps3000aRunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, 1, None, 0, None, None)
assert_pico_ok(status["runblock"])

# Creates a overlow location for data
overflow = (ctypes.c_int16 * 10)()
# Creates converted types maxsamples
cmaxSamples = ctypes.c_int32(maxsamples)

# Checks data collection to finish the capture
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    status["isReady"] = ps.ps3000aIsReady(chandle, ctypes.byref(ready))

# Handle = chandle
# start index = 0
# noOfSamples = ctypes.byref(cmaxSamples)
# DownSampleRatio = 0
# DownSampleRatioMode = 0
# SegmentIndex = 0
# Overflow = ctypes.byref(overflow)

status["GetValues"] = ps.ps3000aGetValues(chandle, 0, ctypes.byref(cmaxSamples), 0, 0, 0, ctypes.byref(overflow))
assert_pico_ok(status["GetValues"])

bufferDPort0 = splitMSOData(cmaxSamples, bufferAMax)

# Creates the time data
time = np.linspace(0, cmaxSamples.value * timeIntervalns.value, cmaxSamples.value)

# Plots the data from digital channel onto a graph
plt.plot(time, bufferDPort0[0])
plt.plot(time, bufferDPort0[1])
plt.plot(time, bufferDPort0[2])
plt.plot(time, bufferDPort0[3])
plt.plot(time, bufferDPort0[4])
plt.plot(time, bufferDPort0[5])
plt.plot(time, bufferDPort0[6])
plt.plot(time, bufferDPort0[7])
plt.xlabel('Time (ns)')
plt.ylabel('Binary')
plt.show()


# Stops the scope
# Handle = chandle
status["stop"] = ps.ps3000aStop(chandle)
assert_pico_ok(status["stop"])

# Closes the unit
# Handle = chandle
status["stop"] = ps.ps3000aCloseUnit(chandle)
assert_pico_ok(status["stop"])

# Displays the staus returns
print(status)