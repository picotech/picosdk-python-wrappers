#
# Copyright (C) 2024 Pico Technology Ltd. See LICENSE file for terms.
#
# PSOSPA STREAMING MODE EXAMPLE
# This example opens a psospa driver device, sets up two channels then collects a streamed set of data.
# The data from channel A is then plotted as mV against time in ns.

import ctypes
import numpy as np
from picosdk.psospa import psospa as ps
from picosdk.PicoDeviceEnums import picoEnum as enums
from picosdk.PicoDeviceStructs import picoStruct as structs
import matplotlib.pyplot as plt
from picosdk.functions import adc2mVV2, assert_pico_ok, mV2adcV2
from picosdk.constants import PICO_STATUS
import time

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open a psospa driver device
# returns handle for future API functions
resolution = enums.PICO_DEVICE_RESOLUTION["PICO_DR_8BIT"]
status["openUnit"] = ps.psospaOpenUnit(ctypes.byref(chandle), None, resolution, None)
assert_pico_ok(status["openUnit"])

# Set channel A on
# handle = chandle
channelA = enums.PICO_CHANNEL["PICO_CHANNEL_A"]
coupling = enums.PICO_COUPLING["PICO_DC"]
rangeMax = 2000000000 #nV
rangeMin = -rangeMax #nV
rangeType = 0 #probes.PICO_PROBE_RANGE_INFO["PICO_PROBE_NONE_NV"]
analogueOffset = 0
bandwidth = enums.PICO_BANDWIDTH_LIMITER["PICO_BW_FULL"]
status["setChannelA"] = ps.psospaSetChannelOn(chandle, channelA, coupling, rangeMin, rangeMax, rangeType, analogueOffset, bandwidth)
assert_pico_ok(status["setChannelA"])

channelB = enums.PICO_CHANNEL["PICO_CHANNEL_B"]
status["setChannelB"] = ps.psospaSetChannelOn(chandle, channelB, coupling, rangeMin, rangeMax, rangeType, analogueOffset, bandwidth)
assert_pico_ok(status["setChannelB"])

# set channel C-D off
for x in range(2, 3, 1):
    channel = x
    status["setChannel", x] = ps.psospaSetChannelOff(chandle, channel)
    assert_pico_ok(status["setChannel", x])

# Set number of samples to be collected
noOfPreTriggerSamples = 100000
noOfPostTriggerSamples = 900000
nSamples = noOfPostTriggerSamples + noOfPreTriggerSamples

# get max ADC value
# handle = chandle
minADC = ctypes.c_int16()
maxADC = ctypes.c_int16()
status["getAdcLimits"] = ps.psospaGetAdcLimits(chandle, resolution, ctypes.byref(minADC), ctypes.byref(maxADC))
assert_pico_ok(status["getAdcLimits"])

# Set simple trigger on channel A, 1 V rising with 1 s autotrigger
# handle = chandle
# enable = 1
source = channelA
# threshold = 100 mV
direction = enums.PICO_THRESHOLD_DIRECTION["PICO_RISING"]
# delay = 0 s
# autoTriggerMicroSeconds = 1000000 us
status["setSimpleTrigger"] = ps.psospaSetSimpleTrigger(chandle, 1, source, (mV2adcV2(100,rangeMax,maxADC)), direction, 0, 1000000)
assert_pico_ok(status["setSimpleTrigger"])

# create buffers
maxBuffers = 10

bufferA = ((ctypes.c_int16 * nSamples) * 10)()
bufferB = ((ctypes.c_int16 * nSamples) * 10)()

# Set data buffers
# handle = chandle
# channel = channelA
# bufferMax = bufferAMax
# bufferMin = bufferAMin
# nSamples = nSamples
dataType = enums.PICO_DATA_TYPE["PICO_INT16_T"]
waveform = 0
downSampleMode = enums.PICO_RATIO_MODE["PICO_RATIO_MODE_RAW"]
clear = enums.PICO_ACTION["PICO_CLEAR_ALL"]
add = enums.PICO_ACTION["PICO_ADD"]
action = clear | add  # PICO_ACTION["PICO_CLEAR_WAVEFORM_CLEAR_ALL"] | PICO_ACTION["PICO_ADD"]
actionAdd = add
status["setDataBuffersA"] = ps.psospaSetDataBuffer(chandle, channelA, ctypes.byref(bufferA[0]), nSamples, dataType,
                                                   waveform, downSampleMode, action)
assert_pico_ok(status["setDataBuffersA"])
status["setDataBuffersB"] = ps.psospaSetDataBuffer(chandle, channelB, ctypes.byref(bufferB[0]), nSamples, dataType,
                                                   waveform, downSampleMode, actionAdd)
assert_pico_ok(status["setDataBuffersB"])

# Run streaming
sampleInterval = ctypes.c_double(1)
sampleIntervalTimeUnits = enums.PICO_TIME_UNITS["PICO_US"]
autoStop = 0
downSampleRatio = 1

status["runStreaming"] = ps.psospaRunStreaming(chandle, ctypes.byref(sampleInterval), sampleIntervalTimeUnits,
                                                noOfPreTriggerSamples, noOfPostTriggerSamples, autoStop,
                                                downSampleRatio, downSampleMode)
assert_pico_ok(status["runStreaming"])

streamData = (structs.PICO_STREAMING_DATA_INFO * 2)()
streamData[0] = structs.PICO_STREAMING_DATA_INFO(channelA, downSampleMode, dataType, 0, 0, 0, 0)
streamData[1] = structs.PICO_STREAMING_DATA_INFO(channelB, downSampleMode, dataType, 0, 0, 0, 0)

streamTrigger = structs.PICO_STREAMING_DATA_TRIGGER_INFO(0, 0, 0)

count = 0

picoOk = PICO_STATUS["PICO_OK"]

collectedSamples = 0

while collectedSamples < (maxBuffers*nSamples):

    status["getStreamingLatestValues"] = ps.psospaGetStreamingLatestValues(chandle, ctypes.byref(streamData), 1,
                                                                            ctypes.byref(streamTrigger))

    if status["getStreamingLatestValues"] == picoOk:
        # do nothing
        time.sleep(0.01)
    else:
        count = count + 1
        if count < maxBuffers:
            status["setDataBufferA"] = ps.psospaSetDataBuffer(chandle, channelA, ctypes.byref(bufferA[count]),
                                                              nSamples, dataType, waveform, downSampleMode, actionAdd)
            assert_pico_ok(status["setDataBufferA"])
            status["setDataBufferB"] = ps.psospaSetDataBuffer(chandle, channelB, ctypes.byref(bufferB[count]),
                                                              nSamples, dataType, waveform, downSampleMode, actionAdd)
            assert_pico_ok(status["setDataBufferB"])
            print(count)
            
    collectedSamples = collectedSamples + streamData[0].noOfSamples

# stop scope streaming
status["stop"] = ps.psospaStop(chandle)
assert_pico_ok(status["stop"])

# get total number of streamed data points
noOfStreamedSamples=ctypes.c_uint64()
status["noOfStreamedSamples"] = ps.psospaNoOfStreamingValues(chandle, ctypes.byref(noOfStreamedSamples))
assert_pico_ok(status["noOfStreamedSamples"])

print("streaming finished")
print("Number of samples collected during streaming")
print(noOfStreamedSamples.value)


# convert ADC counts data to mV
bufferAmV = []
for k in range (0, maxBuffers, 1):
    mvValues =  adc2mVV2(bufferA[k], rangeMax, maxADC)
    bufferAmV.append(mvValues)

time = np.linspace(0, ((nSamples -1)*maxBuffers) * sampleInterval.value * 1000000, (nSamples*maxBuffers))
startTime = 0
endTime = nSamples
# plot data
for h in range (0, maxBuffers, 1):
    plt.plot(time[startTime:endTime],bufferAmV[h])
    startTime += nSamples
    endTime += nSamples
plt.xlabel('Time (us)')
plt.ylabel('Voltage (mV)')
plt.show()


# Close the scope
status["closeunit"] = ps.psospaCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

print(status)
