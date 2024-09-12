#
# Copyright (C) 2018-2024 Pico Technology Ltd. See LICENSE file for terms.
#
# PS5000 Series STREAMING MODE EXAMPLE
# This example demonstrates how to call the ps5000 driver API functions in order to open a device, setup 2 channels and collects streamed data (1 buffer).
# This data is then plotted as mV against time in ns.

import ctypes
import numpy as np
from picosdk.ps5000 import ps5000 as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok
import time

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open PicoScope 5000 Series device
status["openunit"] = ps.ps5000OpenUnit(ctypes.byref(chandle))

try:
    assert_pico_ok(status["openunit"])
except: # PicoNotOkError:

    powerStatus = status["openunit"]

    if powerStatus == 286:
        status["changePowerSource"] = ps.ps5000ChangePowerSource(chandle, powerStatus)
    elif powerStatus == 282:
        status["changePowerSource"] = ps.ps5000ChangePowerSource(chandle, powerStatus)
    else:
        raise

    assert_pico_ok(status["changePowerSource"])

enabled = 1
disabled = 0
coupling_type = 1

# Set up channel A
# handle = chandle
# channel = PS5000_CHANNEL_A = 0
# enabled = 1
# coupling type = PS5000A_DC = 1
# range = PS5000A_2V = 7
channel_range = ps.PS5000_RANGE["PS5000_2V"]
status["setChA"] = ps.ps5000SetChannel(chandle,
                                        ps.PS5000_CHANNEL['PS5000_CHANNEL_A'],
                                        enabled,
                                        coupling_type,
                                        channel_range)
assert_pico_ok(status["setChA"])

# Set up channel B
# handle = chandle
# channel = PS5000_CHANNEL_B = 1
# enabled = 1
# coupling type = PS5000A_DC = 1
# range = PS5000A_2V = 7

status["setChB"] = ps.ps5000SetChannel(chandle,
                                        ps.PS5000_CHANNEL['PS5000_CHANNEL_B'],
                                        enabled,
                                        coupling_type,
                                        channel_range)
assert_pico_ok(status["setChB"])

# Size of capture
sizeOfOneBuffer = 10000
numBuffersToCapture = 10
totalSamples = sizeOfOneBuffer * numBuffersToCapture

# Create buffers ready for assigning pointers for data collection
bufferAMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
bufferBMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)

memory_segment = 0

# Set data buffer location for data collection from channel A
# handle = chandle
# source = PS5000_CHANNEL_A = 0
# pointer to buffer max = ctypes.byref(bufferAMax)
# buffer length = maxSamples
status["setDataBuffersA"] = ps.ps5000SetDataBuffers(chandle,
                                                     ps.PS5000_CHANNEL['PS5000_CHANNEL_A'],
                                                     bufferAMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer
                                                     )
assert_pico_ok(status["setDataBuffersA"])

# Set data buffer location for data collection from channel B
# handle = chandle
# source = PS5000_CHANNEL_B = 1
# pointer to buffer max = ctypes.byref(bufferBMax)
# buffer length = maxSamples
status["setDataBuffersB"] = ps.ps5000SetDataBuffers(chandle,
                                                     ps.PS5000_CHANNEL['PS5000_CHANNEL_B'],
                                                     bufferBMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer)
assert_pico_ok(status["setDataBuffersB"])

# Begin streaming mode:
sampleInterval = ctypes.c_int32(200)
sampleUnits = ps.PS5000_TIME_UNITS['PS5000_US']
# We are not triggering:
maxPreTriggerSamples = 0
autoStopOn = 1
# No downsampling:
downsampleRatio = 1
status["runStreaming"] = ps.ps5000RunStreaming(chandle,
                                                ctypes.byref(sampleInterval),
                                                sampleUnits,
                                                maxPreTriggerSamples,
                                                totalSamples,
                                                autoStopOn,
                                                downsampleRatio,
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
    status["getStreamingLastestValues"] = ps.ps5000GetStreamingLatestValues(chandle, cFuncPtr, None)
    if not wasCalledBack:
        # If we weren't called back by the driver, this means no data is ready. Sleep for a short while before trying
        # again.
        time.sleep(0.01)

print("Done grabbing values.")

# Find maximum ADC count value
# handle = chandle
# pointer to value = ctypes.byref(maxADC)
maxADC = ctypes.c_int16(32767)
#status["maximumValue"] = ps.ps5000MaximumValue(chandle, ctypes.byref(maxADC))
#assert_pico_ok(status["maximumValue"])

# Convert ADC counts data to mV
adc2mVChAMax = adc2mV(bufferCompleteA, channel_range, maxADC)
adc2mVChBMax = adc2mV(bufferCompleteB, channel_range, maxADC)

# Create time data
time = np.linspace(0, (totalSamples - 1) * actualSampleIntervalNs, totalSamples)

# Plot data from channel A and B
plt.plot(time, adc2mVChAMax[:])
plt.plot(time, adc2mVChBMax[:])
plt.xlabel('Time (ns)')
plt.ylabel('Voltage (mV)')
plt.show()

# Stop the scope
# handle = chandle
status["stop"] = ps.ps5000Stop(chandle)
assert_pico_ok(status["stop"])

# Disconnect the scope
# handle = chandle
status["close"] = ps.ps5000CloseUnit(chandle)
assert_pico_ok(status["close"])

# Display status returns
print(status)