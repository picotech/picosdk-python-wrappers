#
# Copyright (C) 2018-2022 Pico Technology Ltd. See LICENSE file for terms.
#
# PicoScope 5000 Series (A API) MSO Block Mode Triggered Example
# This example demonstrates how to use the PicoScope 5000 Series (ps5000a) driver API functions in order to do the
# following:
#
# Open a connection to a PicoScope 5000 Series MSO device
# Setup a digital port
# Set up a digital trigger
# Collect a block of data
# Plot data

import ctypes
from picosdk.ps5000a import ps5000a as ps
from picosdk.functions import splitMSODataFast, assert_pico_ok
import numpy as np
import matplotlib.pyplot as plt

# Gives the device a handle
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps5000aOpenUnit(ctypes.byref(chandle), None, ps.PS5000A_DEVICE_RESOLUTION["PS5000A_DR_8BIT"])

try:
    assert_pico_ok(status["openunit"])
except:
    # powerstate becomes the status number of openunit
    powerstate = status["openunit"]

    # If powerstate is the same as 282 then it will run this if statement
    if powerstate == 282:
        # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
        status["ChangePowerSource"] = ps.ps5000aChangePowerSource(chandle, 282)
    # If the powerstate is the same as 286 then it will run this if statement
    elif powerstate == 286:
        # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
        status["ChangePowerSource"] = ps.ps5000aChangePowerSource(chandle, 286)
    else:
        raise

    assert_pico_ok(status["ChangePowerSource"])


digital_port0 = ps.PS5000A_CHANNEL["PS5000A_DIGITAL_PORT0"]
# Set up digital port
# handle = chandle
# channel = ps5000a_DIGITAL_PORT0 = 0x80
# enabled = 1
# logicLevel = 10000
status["SetDigitalPort"] = ps.ps5000aSetDigitalPort( chandle, digital_port0, 1, 10000)
assert_pico_ok(status["SetDigitalPort"])

#Set a trigger on digital channel


# Set the number of sample to be collected
preTriggerSamples = 2500
postTriggerSamples = 2500
totalSamples = preTriggerSamples + postTriggerSamples

# Gets timebase information
# Warning: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
# To access these Timebases, set any unused analogue channels to off.
# handle = chandle
# timebase = 1252
# Nosample = totalSamples
# TimeIntervalNanoseconds = ctypes.byref(timeIntervalNs)
# MaxSamples = ctypes.byref(returnedMaxSamples)
# Segement index = 0
timebase = 1252
timeIntervalNs = ctypes.c_float()
returnedMaxSamples = ctypes.c_int16()
status["GetTimebase"] = ps.ps5000aGetTimebase2(chandle,
                                               timebase,
                                               totalSamples,
                                               ctypes.byref(timeIntervalNs),                                             
                                               ctypes.byref(returnedMaxSamples),
                                               0)
assert_pico_ok(status["GetTimebase"])

# Create buffers ready for assigning pointers for data collection
bufferDPort0Max = (ctypes.c_int16 * totalSamples)()
bufferDPort0Min = (ctypes.c_int16 * totalSamples)()

# Set the data buffer location for data collection from ps5000a_DIGITAL_PORT0
# handle = chandle
# source = ps5000a_DIGITAL_PORT0 = 0x80
# Buffer max = ctypes.byref(bufferDPort0Max)
# Buffer min = ctypes.byref(bufferDPort0Min)
# Buffer length = totalSamples
# Segment index = 0
# Ratio mode = ps5000a_RATIO_MODE_NONE = 0
status["SetDataBuffers"] = ps.ps5000aSetDataBuffers(chandle,
                                                    0x80,
                                                    ctypes.byref(bufferDPort0Max),
                                                    ctypes.byref(bufferDPort0Min),
                                                    totalSamples,
                                                    0,
                                                    0)
assert_pico_ok(status["SetDataBuffers"])

# set the digital trigger for a high bit on digital channel 0
conditions = ps.PS5000A_CONDITION(ps.PS5000A_CHANNEL["PS5000A_DIGITAL_PORT0"], ps.PS5000A_TRIGGER_STATE["PS5000A_CONDITION_TRUE"])
nConditions = 1
clear = 1
add = 2
info = clear + add
status["setTriggerChannelConditionsV2"] = ps.ps5000aSetTriggerChannelConditionsV2(chandle,
                                                                                  ctypes.byref(conditions),
                                                                                  nConditions,
                                                                                  info)
assert_pico_ok(status["setTriggerChannelConditionsV2"])

directions = ps.PS5000A_DIGITAL_CHANNEL_DIRECTIONS(ps.PS5000A_DIGITAL_CHANNEL["PS5000A_DIGITAL_CHANNEL_0"], ps.PS5000A_DIGITAL_DIRECTION["PS5000A_DIGITAL_DIRECTION_HIGH"])
nDirections = 1
status["setTriggerDigitalPortProperties"] = ps.ps5000aSetTriggerDigitalPortProperties(chandle,
                                                                                      ctypes.byref(directions),
                                                                                      nDirections)
assert_pico_ok(status["setTriggerDigitalPortProperties"])

# set autotrigger timeout value
status["autoTriggerus"] = ps.ps5000aSetAutoTriggerMicroSeconds(chandle, 10000)
assert_pico_ok(status["autoTriggerus"])

print ("Starting data collection...")

# Starts the block capture
# handle = chandle
# Number of preTriggerSamples
# Number of postTriggerSamples
# Timebase = 1252 = 10000 ns (see Programmer's guide for more information on timebases)
# time indisposed ms = None (This is not needed within the example)
# Segment index = 0
# LpRead = None
# pParameter = None
status["runblock"] = ps.ps5000aRunBlock(chandle,
                                        preTriggerSamples,
                                        postTriggerSamples,
                                        timebase,
                                        None,
                                        0,
                                        None,
                                        None)
assert_pico_ok(status["runblock"])

# Creates a overflow location for data
overflow = (ctypes.c_int16 * 10)()
# Creates converted types totalSamples
cTotalSamples = ctypes.c_int32(totalSamples)

# Checks data collection to finish the capture
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)

while ready.value == check.value:
    status["isReady"] = ps.ps5000aIsReady(chandle, ctypes.byref(ready))

# Handle = chandle
# start index = 0
# noOfSamples = ctypes.byref(cTotalSamples)
# DownSampleRatio = 1
# DownSampleRatioMode = 0
# SegmentIndex = 0
# Overflow = ctypes.byref(overflow)

status["GetValues"] = ps.ps5000aGetValues(chandle, 0, ctypes.byref(cTotalSamples), 1, 0, 0, ctypes.byref(overflow))
assert_pico_ok(status["GetValues"])

print ("Data collection complete.")

# Obtain binary for Digital Port 0
# The tuple returned contains the channels in order (D7, D6, D5, ... D0).
bufferDPort0 = splitMSODataFast(cTotalSamples, bufferDPort0Max)

# Creates the time data
time = np.linspace(0, (cTotalSamples.value - 1) * timeIntervalNs.value, cTotalSamples.value)

print ("Plotting data...")

# Plot the data from digital channels onto a graph

plt.figure(num='PicoScope 3000 Series (A API) MSO Block Capture Example')
plt.title('Plot of Digital Port 0 digital channels vs. time')
plt.plot(time, bufferDPort0[0], label='D7')  # D7 is the first array in the tuple.
plt.plot(time, bufferDPort0[1], label='D6')
plt.plot(time, bufferDPort0[2], label='D5')
plt.plot(time, bufferDPort0[3], label='D4')
plt.plot(time, bufferDPort0[4], label='D3')
plt.plot(time, bufferDPort0[5], label='D2')
plt.plot(time, bufferDPort0[6], label='D1')
plt.plot(time, bufferDPort0[7], label='D0')  # D0 is the last array in the tuple.
plt.xlabel('Time (ns)')
plt.ylabel('Logic Level')
plt.legend(loc="upper right")
plt.show()

print ("Close figure to stop the device and close the connection.")

# Stops the scope
# handle = chandle
status["stop"] = ps.ps5000aStop(chandle)
assert_pico_ok(status["stop"])

# Closes the unit
# handle = chandle
status["closeUnit"] = ps.ps5000aCloseUnit(chandle)
assert_pico_ok(status["closeUnit"])

# Displays the status returns
print(status)