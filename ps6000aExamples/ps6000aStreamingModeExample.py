#
# Copyright (C) 2020 Pico Technology Ltd. See LICENSE file for terms.
#
# PS6000 A STREAMING MODE EXAMPLE
# This example opens a 6000a driver device, sets up one channel then collects a streamed set of data.
# This data is then plotted as mV against time in ns.

import ctypes
# import numpy as np
from picosdk.ps6000a import ps6000a as ps
from picosdk.PicoDeviceEnums import picoEnum as enums
from picosdk.PicoDeviceStructs import picoStruct as structs
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok
from picosdk.constants import PICO_STATUS
import time

# Create chandle and status ready for use
chandle = ctypes.c_int16()
status = {}

# Open 6000 A series PicoScope
# returns handle to chandle for use in future API functions
resolution = enums.PICO_DEVICE_RESOLUTION["PICO_DR_8BIT"]
status["openunit"] = ps.ps6000aOpenUnit(ctypes.byref(chandle), None, resolution)
assert_pico_ok(status["openunit"])

# Set channel A on
# handle = chandle
channelA = enums.PICO_CHANNEL["PICO_CHANNEL_A"]
coupling = enums.PICO_COUPLING["PICO_DC"]
channelRange = 7
# analogueOffset = 0 V
bandwidth = enums.PICO_BANDWIDTH_LIMITER["PICO_BW_FULL"]
status["setChannelA"] = ps.ps6000aSetChannelOn(chandle, channelA, coupling, channelRange, 0, bandwidth)
assert_pico_ok(status["setChannelA"])

# set channel B-H off
for x in range(1, 7, 1):
    channel = x
    status["setChannel", x] = ps.ps6000aSetChannelOff(chandle, channel)
    assert_pico_ok(status["setChannel", x])

# Set number of samples to be collected
noOfPreTriggerSamples = 100000
noOfPostTriggerSamples = 900000
nSamples = noOfPostTriggerSamples + noOfPreTriggerSamples

# Set simple trigger on channel A, 1 V rising with 1 s autotrigger
# handle = chandle
# enable = 1
source = channelA
# threshold = 1000 mV
direction = enums.PICO_THRESHOLD_DIRECTION["PICO_RISING"]
# delay = 0 s
# autoTriggerMicroSeconds = 1000000 us
status["setSimpleTrigger"] = ps.ps6000aSetSimpleTrigger(chandle, 1, source, 1000, direction, 0, 1000000)
assert_pico_ok(status["setSimpleTrigger"])

# create buffers
maxBuffers = 10

bufferA = ((ctypes.c_int16 * nSamples) * 10)()

print(bufferA)
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
status["setDataBuffers"] = ps.ps6000aSetDataBuffer(chandle, channelA, ctypes.byref(bufferA[0]), nSamples, dataType,
                                                   waveform, downSampleMode, action)
assert_pico_ok(status["setDataBuffers"])

# Run streaming
sampleInterval = ctypes.c_double(1)
sampleIntervalTimeUnits = enums.PICO_TIME_UNITS["PICO_US"]
autoStop = 0
downSampleRatio = 1

status["runStreaming"] = ps.ps6000aRunStreaming(chandle, ctypes.byref(sampleInterval), sampleIntervalTimeUnits,
                                                noOfPreTriggerSamples, noOfPostTriggerSamples, autoStop,
                                                downSampleRatio, downSampleMode)
assert_pico_ok(status["runStreaming"])

streamData = structs.PICO_STREAMING_DATA_INFO(channelA, downSampleRatio, dataType, 0, 0, 0, 0)

streamTrigger = structs.PICO_STREAMING_DATA_TRIGGER_INFO(0, 0, 0)

count = 1

actionB = add

picoOk = PICO_STATUS["PICO_OK"]

while count <= maxBuffers:

    status["getStreamingLatestValues"] = ps.ps6000aGetStreamingLatestValues(chandle, ctypes.byref(streamData), 1,
                                                                            ctypes.byref(streamTrigger))

    if status["getStreamingLatestValues"] == picoOk:
        # do nothing
        time.sleep(0.01)
    else:
        count = count + 1
        if count <= maxBuffers:
            status["setDataBuffer"] = ps.ps6000aSetDataBuffer(chandle, channelA, ctypes.byref(bufferA[count - 1]),
                                                              nSamples, dataType, waveform, downSampleMode, actionB)
            assert_pico_ok(status["setDataBuffer"])
            print(count)

print("streaming finished")

# get max ADC value
# handle = chandle
minADC = ctypes.c_int16()
maxADC = ctypes.c_int16()
status["getAdcLimits"] = ps.ps6000aGetAdcLimits(chandle, resolution, ctypes.byref(minADC), ctypes.byref(maxADC))
assert_pico_ok(status["getAdcLimits"])

# convert ADC counts data to mV
bufferAmV = ((ctypes.c_int16 * nSamples) * 10)()
for j in range(0, 9):
    A = bufferA[j]
    bufferAmV[j] = adc2mV(A, channelRange, maxADC)

# Close the scope
status["closeunit"] = ps.ps6000aCloseUnit(chandle)
assert_pico_ok(status["closeunit"])

print(status)
