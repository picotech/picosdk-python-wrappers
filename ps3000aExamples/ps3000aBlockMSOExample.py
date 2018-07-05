from __future__ import print_function
import ctypes
from picosdk.ps3000a import ps3000a as ps
from picosdk.functions import *
import numpy as np
import matplotlib.pyplot as plt
import time
from array import *

# Creates a string buffer for the serial number to enter 
def create_empty_string_buffer(buffer_size):
    try:
        return ctypes.create_string_buffer("\0", buffer_size)
    except TypeError:
        return ctypes.create_string_buffer("\0".encode('utf8'), buffer_size)


# Gives the device a handle 
status = {}
chandle = ctypes.c_int16()

# Opens the device/s
status["openunit"] = ps.ps3000aOpenUnit(ctypes.byref(chandle), None)

# powerstate becomes the status number of openunit
powerstate = status["openunit"]

# If powerstate is the same as 282 then it will run this if statement
if powerstate == 282:
    # Changes the power input to "PICO_POWER_SUPPLY_NOT_CONNECTED"
    status["ChangePowerSource"] = ps.ps3000aChangePowerSource(chandle, 282)

# If the powerstate is the same as 286 then it will run this if statement
if powerstate == 286:
    # Changes the power input to "PICO_USB3_0_DEVICE_NON_USB3_0_PORT"
    status["ChangePowerSource"] = ps.ps3000aChangePowerSource(chandle, 286) 

# Handle
# PS3000a_DIGITAL_PORT = 0x80
# Enable = 1
# logicLevel = 0

status["SetDigitalPort"] = ps.ps3000aSetDigitalPort( chandle, 0x80, 1, 10000)

# Setting the number of sample to be collected
preTriggerSamples = 400
postTriggerSamples = 400
maxsamples = preTriggerSamples + postTriggerSamples

# Gets timebase innfomation
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
status["SetDataBuffers"] = ps.ps3000aSetDataBuffers(chandle, 0x80, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxsamples, 0, 0)

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

bufferAMaxBinaryD0, bufferAMaxBinaryD1, bufferAMaxBinaryD2, bufferAMaxBinaryD3, bufferAMaxBinaryD4, bufferAMaxBinaryD5, bufferAMaxBinaryD6, bufferAMaxBinaryD7 = splitMSODataPort0(cmaxSamples, bufferAMax)

# Creates the time data 
time = np.linspace(0, (cmaxSamples.value) * timeIntervalns.value, cmaxSamples.value)

# Plots the data from digital channel onto a graph
plt.plot(time, bufferAMaxBinaryD0[:])
plt.plot(time, bufferAMaxBinaryD1[:])
plt.plot(time, bufferAMaxBinaryD2[:])
plt.plot(time, bufferAMaxBinaryD3[:])
plt.plot(time, bufferAMaxBinaryD4[:])
plt.plot(time, bufferAMaxBinaryD5[:])
plt.plot(time, bufferAMaxBinaryD6[:])
plt.plot(time, bufferAMaxBinaryD7[:])
plt.xlabel('Time (ns)')
plt.ylabel('Binary')
plt.show()


# Stops the scope 
# Handle = chandle
status["stop"] = ps.ps3000aStop(chandle)

# Displays the staus returns
print(status)

# Closes the unit 
# Handle = chandle 
ps.ps3000aCloseUnit(chandle)
