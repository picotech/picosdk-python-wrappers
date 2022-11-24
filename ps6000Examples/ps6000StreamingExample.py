#
# Copyright (C) 2019 Pico Technology Ltd. See LICENSE file for terms.
#
# PS6000 Series STREAMING MODE EXAMPLE
# This example demonstrates how to call the ps6000 driver API functions in order to open a device, setup 2 channels and collects streamed data (1 buffer).
# This data is then plotted as mV against time in ns.

import ctypes
import numpy as np
from picosdk.ps6000 import ps6000 as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok
import time

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open PicoScope 6000 Series device
# Returns handle to chandle for use in future API functions
status["openunit"] = ps.ps6000OpenUnit(ctypes.byref(chandle), None)
assert_pico_ok(status["openunit"])



enabled = 1
disabled = 0
analogue_offset = 0.0

# Set up channel A
# handle = chandle
# channel = PS6000_CHANNEL_A = 0
# enabled = 1
# coupling type = PS6000_DC = 1
# range = PS6000_2V = 7
# analogue offset = 0 V
channel_range = ps.PS6000_RANGE['PS6000_2V']
status["setChA"] = ps.ps6000SetChannel(chandle,
                                        ps.PS6000_CHANNEL['PS6000_CHANNEL_A'],
                                        enabled,
                                        ps.PS6000_COUPLING['PS6000_DC_1M'],
                                        channel_range,
                                        analogue_offset,
										ps.PS6000_BANDWIDTH_LIMITER['PS6000_BW_FULL'])
assert_pico_ok(status["setChA"])

# Set up channel B
# handle = chandle
# channel = PS6000_CHANNEL_B = 1
# enabled = 1
# coupling type = PS6000_DC = 1
# range = PS6000_2V = 7
# analogue offset = 0 V
status["setChB"] = ps.ps6000SetChannel(chandle,
                                        ps.PS6000_CHANNEL['PS6000_CHANNEL_B'],
                                        enabled,
                                        ps.PS6000_COUPLING['PS6000_DC_1M'],
                                        channel_range,
                                        analogue_offset,
										ps.PS6000_BANDWIDTH_LIMITER['PS6000_BW_FULL'])
assert_pico_ok(status["setChB"])

# Size of capture
sizeOfOneBuffer = 500
numBuffersToCapture = 10

totalSamples = sizeOfOneBuffer * numBuffersToCapture

# Create buffers ready for assigning pointers for data collection
bufferAMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
bufferBMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)

# Set data buffer location for data collection from channel A
# handle = chandle
# source = PS6000_CHANNEL_A = 0
# pointer to buffer max = ctypes.byref(bufferAMax)
# pointer to buffer min = ctypes.byref(bufferAMin)
# buffer length = maxSamples
# segment index = 0
# ratio mode = PS6000_RATIO_MODE_NONE = 0
status["setDataBuffersA"] = ps.ps6000SetDataBuffers(chandle,
                                                     ps.PS6000_CHANNEL['PS6000_CHANNEL_A'],
                                                     bufferAMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer,
                                                     ps.PS6000_RATIO_MODE['PS6000_RATIO_MODE_NONE'])
assert_pico_ok(status["setDataBuffersA"])

# Set data buffer location for data collection from channel B
# handle = chandle
# source = PS6000_CHANNEL_B = 1
# pointer to buffer max = ctypes.byref(bufferBMax)
# pointer to buffer min = ctypes.byref(bufferBMin)
# buffer length = maxSamples
# segment index = 0
# ratio mode = PS6000_RATIO_MODE_NONE = 0
status["setDataBuffersB"] = ps.ps6000SetDataBuffers(chandle,
                                                     ps.PS6000_CHANNEL['PS6000_CHANNEL_B'],
                                                     bufferBMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer,
                                                     ps.PS6000_RATIO_MODE['PS6000_RATIO_MODE_NONE'])
assert_pico_ok(status["setDataBuffersB"])

# Begin streaming mode:
sampleInterval = ctypes.c_int32(250)
sampleUnits = ps.PS6000_TIME_UNITS['PS6000_US']
# We are not triggering:
maxPreTriggerSamples = 0
autoStopOn = 1
# No downsampling:
downsampleRatio = 1
status["runStreaming"] = ps.ps6000RunStreaming(chandle,
                                                ctypes.byref(sampleInterval),
                                                sampleUnits,
                                                maxPreTriggerSamples,
                                                totalSamples,
                                                autoStopOn,
                                                downsampleRatio,
                                                ps.PS6000_RATIO_MODE['PS6000_RATIO_MODE_NONE'],
                                                sizeOfOneBuffer)
assert_pico_ok(status["runStreaming"])

actualSampleInterval = sampleInterval.value
actualSampleIntervalNs = actualSampleInterval * 1000

print("Capturing at sample interval %s ns" % actualSampleIntervalNs)

# We need a big buffer, not registered with the driver, to keep our complete capture in.
bufferCompleteA = np.zeros(shape=totalSamples, dtype=np.int16)
bufferCompleteB = np.zeros(shape=totalSamples, dtype=np.int16)
nextSample = 0
autoStopOuter = False
wasCalledBack = False


def streaming_callback(handle, noOfSamples, startIndex, overflow, triggerAt, triggered, autoStop, param):
    global nextSample, autoStopOuter, wasCalledBack
    wasCalledBack = True
    destEnd = nextSample + noOfSamples
    sourceEnd = startIndex + noOfSamples
    bufferCompleteA[nextSample:destEnd] = bufferAMax[startIndex:sourceEnd]
    bufferCompleteB[nextSample:destEnd] = bufferBMax[startIndex:sourceEnd]
    nextSample += noOfSamples
    if autoStop:
        autoStopOuter = True


# Convert the python function into a C function pointer.
cFuncPtr = ps.StreamingReadyType(streaming_callback)

# Fetch data from the driver in a loop, copying it out of the registered buffers and into our complete one.
while nextSample < totalSamples and not autoStopOuter:
    wasCalledBack = False
    status["getStreamingLastestValues"] = ps.ps6000GetStreamingLatestValues(chandle, cFuncPtr, None)
    if not wasCalledBack:
        # If we weren't called back by the driver, this means no data is ready. Sleep for a short while before trying
        # again.
        time.sleep(0.01)

print("Done grabbing values.")

# Find maximum ADC count value
# handle = chandle
# pointer to value = ctypes.byref(maxADC)
maxADC = ctypes.c_int16(32512)

# Convert ADC counts data to mV
adc2mVChAMax = adc2mV(bufferCompleteA, channel_range, maxADC)
adc2mVChBMax = adc2mV(bufferCompleteB, channel_range, maxADC)

# Create time data
time = np.linspace(0, (totalSamples -1) * actualSampleIntervalNs, totalSamples)

# Plot data from channel A and B
plt.plot(time, adc2mVChAMax[:])
plt.plot(time, adc2mVChBMax[:])
plt.xlabel('Time (ns)')
plt.ylabel('Voltage (mV)')
plt.show()

# Stop the scope
# handle = chandle
status["stop"] = ps.ps6000Stop(chandle)
assert_pico_ok(status["stop"])

# Disconnect the scope
# handle = chandle
status["close"] = ps.ps6000CloseUnit(chandle)
assert_pico_ok(status["close"])

# Display status returns
print(status)
