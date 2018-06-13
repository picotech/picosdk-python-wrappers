## PS5000A BLOCK MODE EXAMPLE
# This example opens a 5000a driver device, sets up two channels and a trigger then collects a block of data.
# This data is then plotted as ADC counts at each sample interval.

import ctypes
import importlib
import numpy as np
from picosdk.ps5000a import ps5000a as ps
import matplotlib.pyplot as plt

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 5000 series PicoScope
# Resolution set to 12 Bit
# PS5000A_DR_12BIT = 2
# Returns handle to chandle for use in future API functions
status["openunit"] = ps.ps5000aOpenUnit(ctypes.byref(chandle), None, 2)

# Set up channel A
# handle = chandle
# channel = PS5000A_CHANNEL_A = 0
# enabled = 1
# coupling type = PS5000A_DC = 1
# range = PS5000A_2V = 7
# analogue offset = 0 V
status["setChA"] = ps.ps5000aSetChannel(chandle, 0, 1, 1, 7, 0)

# Set up channel B
# handle = chandle
# channel = PS5000A_CHANNEL_B = 1
# enabled = 1
# coupling type = PS5000A_DC = 1
# range = PS5000A_2V = 7
# analogue offset = 0 V
status["setChB"] = ps.ps5000aSetChannel(chandle, 1, 1, 1, 7, 0)

# Set up single trigger
# handle = chandle
# enabled = 1
# source = PS5000A_CHANNEL_A = 0
# threshold = 1024 ADC counts
# direction = PS5000A_RISING = 2
# delay = 0 s
# auto Trigger = 1000 ms
status["trigger"] = ps.ps5000aSetSimpleTrigger(chandle, 1, 0, 1024, 2, 0, 1000)

# Set number of pre and post trigger samples to be collected
preTriggerSamples = 2500
postTriggerSamples = 2500
maxSamples = preTriggerSamples + postTriggerSamples

# Run block capture
# handle = chandle
# number of pre-trigger samples = preTriggerSamples
# number of post-trigger samples = PostTriggerSamples
# timebase = 8 = 80 ns (see Programmer's guide for mre information on timebases)
# time indisposed ms = None (not needed in the example)
# segment index = 0
# lpReady = None (using ps5000aIsReady rather than ps5000aBlockReady)
# pParameter = None
status["runBlock"] = ps.ps5000aRunBlock(chandle, preTriggerSamples, postTriggerSamples, 8, None, 0, None, None)

# Check for data collection to finish using ps5000aIsReady
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    status["isReady"] = ps.ps5000aIsReady(chandle, ctypes.byref(ready))

# Create buffers ready for assigning pointers for data collection
bufferAMax = (ctypes.c_int16 * maxSamples)()
bufferAMin = (ctypes.c_int16 * maxSamples)()
bufferBMax = (ctypes.c_int16 * maxSamples)()
bufferBMin = (ctypes.c_int16 * maxSamples)()

# Set data buffer location for data collection from channel A
# handle = chandle
# source = PS5000A_CHANNEL_A = 0
# pointer to buffer max = ctypes.byref(bufferAMax)
# pointer to buffer min = ctypes.byref(bufferAMin)
# buffer length = maxSamples
# segment index = 0
# ratio mode = PS5000A_RATIO_MODE_NONE = 0
status["setDataBuffersA"] = ps.ps5000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxSamples, 0, 0)

# Set data buffer location for data collection from channel B
# handle = chandle
# source = PS5000A_CHANNEL_B = 1
# pointer to buffer max = ctypes.byref(bufferBMax)
# pointer to buffer min = ctypes.byref(bufferBMin)
# buffer length = maxSamples
# segment index = 0
# ratio mode = PS5000A_RATIO_MODE_NONE = 0
status["setDataBuffersB"] = ps.ps5000aSetDataBuffers(chandle, 1, ctypes.byref(bufferBMax), ctypes.byref(bufferBMin), maxSamples, 0, 0)

# create overflow loaction
overflow = ctypes.c_int16()
# create converted type maxSamples
cmaxSamples = ctypes.c_int32(maxSamples)

# Retried data from scope to buffers assigned above
# handle = chandle
# start index = 0
# pointer to number of samples = ctypes.byref(cmaxSamples)
# downsample ratio = 0
# downsample ratio mode = PS5000A_RATIO_MODE_NONE
# pointer to overflow = ctypes.byref(overflow))
status["getValues"] = ps.ps5000aGetValues(chandle, 0, ctypes.byref(cmaxSamples), 0, 0, 0, ctypes.byref(overflow))

# plot data from channel A and B
plt.plot(bufferAMax[:])
plt.plot(bufferBMax[:])
plt.xlabel('Sample Number')
plt.ylabel('ADC Counts')
plt.show()

# Stop the scope
# handle = chandle
status["stop"] = ps.ps5000aStop(chandle)

# display status returns
print(status)

# Close unitDisconnect the scope
# handle = chandle
ps.ps5000aCloseUnit(chandle)