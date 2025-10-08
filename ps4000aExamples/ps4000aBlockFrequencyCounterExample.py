#
# Copyright (C) 2025 Pico Technology Ltd. See LICENSE file for terms.
#
# PS4000 BLOCK MODE FREQUENCY COUNTER EXAMPLE
# This example opens a 4000a driver device, sets up two channels and a trigger then collects a block of data.
# This data is then plotted as Hz against time in ns.
#
# This example will only work with an automotive version of a 4000 series scope
# such as 4225A and 4425A

import ctypes
import numpy as np
from picosdk.ps4000a import ps4000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok, mV2adc
from math import *

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 4000 series PicoScope
# Returns handle to chandle for use in future API functions
status["openunit"] = ps.ps4000aOpenUnit(ctypes.byref(chandle), None)

try:
    assert_pico_ok(status["openunit"])
except:

    powerStatus = status["openunit"]

    if powerStatus == 286:
        status["changePowerSource"] = ps.ps4000aChangePowerSource(chandle, powerStatus)
    else:
        raise

    assert_pico_ok(status["changePowerSource"])

# Set up channel A
# handle = chandle
# channel = PS4000a_CHANNEL_A = 0
# enabled = 1
# coupling type = PS4000a_DC = 1
# range = PS4000a_5V = 8
# analogOffset = 0 V
chARange = 8
status["setChA"] = ps.ps4000aSetChannel(chandle, 0, 1, 1, chARange, 0)
assert_pico_ok(status["setChA"])

# Set up channel A
# handle = chandle
# channel = PS4000a_CHANNEL_A = 0
# enabled = 1
# coupling type = PS4000a_DC = 1
# range = PS4000a_5V = 8
# analogOffset = 0 V
chARange = 8
status["setChB"] = ps.ps4000aSetChannel(chandle, 1, 1, 1, chARange, 0)
assert_pico_ok(status["setChB"])

# find maximum ADC count value
# handle = chandle
# pointer to value = ctypes.byref(maxADC)
maxADC = ctypes.c_int16(32767)

# set trigger properties for channel ADC
thresholdMajor = mV2adc(300, chARange, maxADC)
thresholdMinor = mV2adc(0, chARange, maxADC)

# set up frequency counting
# handle = chandle
# channel - PS4000a_CHANNEL_A = 0
# enabled = 1
# frequency range = PS4000A_FC_200 = 0 - 200 Hz

status["setFrequencyCounter"] = ps.ps4000aSetFrequencyCounter(chandle, 0, 1, ps.PS4000A_FREQUENCY_COUNTER_RANGE["PS4000A_FC_200"],thresholdMajor,thresholdMinor)

# Set number of pre and post trigger samples to be collected
preTriggerSamples = 500000
postTriggerSamples = 500000
maxSamples = preTriggerSamples + postTriggerSamples

# Get timebase information
# WARNING: When using this example it may not be possible to access all Timebases as all channels are enabled by default when opening the scope.  
# To access these Timebases, set any unused analogue channels to off.
# handle = chandle
# timebase = 8 = timebase
# noSamples = maxSamples
# pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalns)
# pointer to maxSamples = ctypes.byref(returnedMaxSamples)
# segment index = 0
timebase = 52
timeIntervalns = ctypes.c_float()
returnedMaxSamples = ctypes.c_int32()
oversample = ctypes.c_int16(1)
status["getTimebase2"] = ps.ps4000aGetTimebase2(chandle, timebase, maxSamples, ctypes.byref(timeIntervalns), ctypes.byref(returnedMaxSamples), 0)
assert_pico_ok(status["getTimebase2"])

# Run block capture
# handle = chandle
# number of pre-trigger samples = preTriggerSamples
# number of post-trigger samples = PostTriggerSamples
# timebase = 3 = 80 ns = timebase (see Programmer's guide for mre information on timebases)
# time indisposed ms = None (not needed in the example)
# segment index = 0
# lpReady = None (using ps4000aIsReady rather than ps4000aBlockReady)
# pParameter = None
status["runBlock"] = ps.ps4000aRunBlock(chandle, preTriggerSamples, postTriggerSamples, timebase, None, 0, None, None)
assert_pico_ok(status["runBlock"])

# Check for data collection to finish using ps4000aIsReady
ready = ctypes.c_int16(0)
check = ctypes.c_int16(0)
while ready.value == check.value:
    status["isReady"] = ps.ps4000aIsReady(chandle, ctypes.byref(ready))

# Create buffers ready for assigning pointers for data collection
bufferAMax = (ctypes.c_int16 * maxSamples)()
bufferAMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example
bufferBMax = (ctypes.c_int16 * maxSamples)()
bufferBMin = (ctypes.c_int16 * maxSamples)() # used for downsampling which isn't in the scope of this example

# Set data buffer location for data collection from channel A
# handle = chandle
# source = PS4000a_CHANNEL_A = 0
# pointer to buffer max = ctypes.byref(bufferAMax)
# pointer to buffer min = ctypes.byref(bufferAMin)
# buffer length = maxSamples
# segementIndex = 0
# mode = PS4000A_RATIO_MODE_NONE = 0
status["setDataBuffersA"] = ps.ps4000aSetDataBuffers(chandle, 0, ctypes.byref(bufferAMax), ctypes.byref(bufferAMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersA"])

status["setDataBuffersB"] = ps.ps4000aSetDataBuffers(chandle, 1, ctypes.byref(bufferBMax), ctypes.byref(bufferBMin), maxSamples, 0 , 0)
assert_pico_ok(status["setDataBuffersB"])

# create overflow loaction
overflow = ctypes.c_int16()
# create converted type maxSamples
cmaxSamples = ctypes.c_int32(maxSamples)

# Retried data from scope to buffers assigned above
# handle = chandle
# start index = 0
# pointer to number of samples = ctypes.byref(cmaxSamples)
# downsample ratio = 0
# downsample ratio mode = PS4000a_RATIO_MODE_NONE
# pointer to overflow = ctypes.byref(overflow))
status["getValues"] = ps.ps4000aGetValues(chandle, 0, ctypes.byref(cmaxSamples), 0, 0, 0, ctypes.byref(overflow))
assert_pico_ok(status["getValues"])

# # convert ADC counts data to mV
adc2mVChBMax =  adc2mV(bufferBMax, chARange, maxADC)


# convert ADC counts to Hz for channel A
chAHzMax = [((x + 32767) * 200) / (2 * maxADC.value) for x in bufferAMax]

# # Create time data
time = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)

# plot data from channel A
plt.plot(time, chAHzMax)
# plt.plot(time, chAHzMin)
plt.xlabel('Time (ns)')
plt.ylabel('Frequency (Hz)')
plt.show()

# Stop the scope
# handle = chandle
status["stop"] = ps.ps4000aStop(chandle)
assert_pico_ok(status["stop"])

# Close unitDisconnect the scope
# handle = chandle
status["close"] = ps.ps4000aCloseUnit(chandle)
assert_pico_ok(status["close"])

# display status returns
print(status)
